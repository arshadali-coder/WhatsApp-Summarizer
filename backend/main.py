from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

# EXISTING imports (unchanged summariser)
from summarizer import summarize_chat

# NEW: WhatsApp ZIP adapter
from whatsapp_zip_adapter import parse_whatsapp_zip

import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_chat(file: UploadFile = File(...)):
    """
    Accepts a ZIP file containing a WhatsApp .txt export.
    Converts it into normalized messages using the adapter,
    then passes it to the existing summariser unchanged.
    """

    # Save uploaded ZIP temporarily
    zip_path = f"temp_{file.filename}"

    with open(zip_path, "wb") as f:
        f.write(await file.read())

    # Adapter layer: ZIP → normalized messages
    messages = parse_whatsapp_zip(zip_path)

    # EXISTING summariser logic (UNCHANGED)
    summary = summarize_chat(messages)

    return {"summary": summary}
