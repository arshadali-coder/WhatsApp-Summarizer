import zipfile
import os
import re
from datetime import datetime


def parse_whatsapp_zip(file_path: str):
    """
    Accepts:
    - ZIP containing WhatsApp .txt
    - OR direct WhatsApp .txt

    Returns normalized messages for summariser.
    """

    if file_path.lower().endswith(".zip"):
        return _parse_from_zip(file_path)
    else:
        return _parse_whatsapp_txt(file_path)


# ---------- ZIP HANDLING ----------

def _parse_from_zip(zip_path):
    extract_dir = os.getcwd()   # ✅ FIX: always valid directory

    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
    except zipfile.BadZipFile:
        raise ValueError("Uploaded file is not a valid ZIP")

    txt_file = None
    for f in os.listdir(extract_dir):
        if f.lower().endswith(".txt"):
            txt_file = os.path.join(extract_dir, f)
            break

    if not txt_file:
        raise ValueError("No WhatsApp .txt file found inside ZIP")

    messages = _parse_whatsapp_txt(txt_file)

    # Cleanup
    os.remove(txt_file)
    os.remove(zip_path)

    return messages


# ---------- TXT PARSER ----------

def _parse_whatsapp_txt(txt_path):
    with open(txt_path, "r", encoding="utf-8", errors="ignore") as file:
        lines = file.readlines()

    pattern = re.compile(
        r'^(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2})\s?(am|pm)? - (.+)$',
        re.IGNORECASE
    )

    messages = []

    for line in lines:
        match = pattern.match(line.strip())
        if not match:
            continue

        date_str, time_str, meridian, body = match.groups()

        # Ignore system / group events
        if any(x in body for x in [
            "joined using this group's invite link",
            "Messages and calls are end-to-end encrypted",
            "created group",
            "added"
        ]):
            continue

        if ": " not in body:
            continue

        sender, message = body.split(": ", 1)

        messages.append({
            "sender": sender,
            "message": message,
            "date": _normalize_date(date_str),
            "timestamp": f"{time_str} {meridian.upper()}" if meridian else time_str
        })

    return messages


def _normalize_date(date_str):
    formats = [
        "%d/%m/%Y", "%d/%m/%y",
        "%m/%d/%Y", "%m/%d/%y",
        "%d-%m-%Y", "%d.%m.%Y"
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return date_str
