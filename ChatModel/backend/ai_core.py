import os
from groq import Groq
from dotenv import load_dotenv

# Path specify kiye bina automatic load karein
load_dotenv()

def get_ai_response(user_message: str) -> str:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY Missing! Check backend/.env file.")

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": "You are PakShop AI Assistant."},
            {"role": "user", "content": user_message}
        ]
    )
    return response.choices[0].message.content