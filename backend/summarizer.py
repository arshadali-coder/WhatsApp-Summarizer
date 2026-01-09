import google.generativeai as genai

genai.configure(api_key="yr_api_key")

model = genai.GenerativeModel("gemini-2.5-flash")

def summarize_chat(messages):
    if not messages:
        return "No valid messages found in the chat."

    text = " ".join(m["message"] for m in messages)
    text = text[:12000]

    prompt = f"""
    Summarize the following WhatsApp group chat.
    Focus on main topics, announcements, and tone.

    Chat:
    {text}
    """

    response = model.generate_content(prompt)
    return response.text