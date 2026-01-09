import re

def parse_chat(text):
    messages = []

    # Normalize weird unicode spaces
    text = text.replace('\u202f', ' ').replace('\u200e', '')

    pattern = re.compile(
        r'^(\d{1,2}/\d{1,2}/\d{2,4}),\s'
        r'(\d{1,2}:\d{2}\s?(?:AM|PM|am|pm))\s-\s'
        r'([^:]+):\s(.*)$'
    )

    current_message = None

    for line in text.split('\n'):
        match = pattern.match(line)
        if match:
            if current_message:
                messages.append(current_message)

            current_message = {
                "date": match.group(1),
                "time": match.group(2),
                "sender": match.group(3).strip(),
                "message": match.group(4).strip()
            }
        else:
            # Continuation of previous message (multi-line)
            if current_message:
                current_message["message"] += " " + line.strip()

    if current_message:
        messages.append(current_message)

    return messages
