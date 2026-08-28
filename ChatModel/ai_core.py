import os
from groq import Groq

# Apni Groq API key yahan rakhein
GROQ_API_KEY = ""  # Apni Groq API Key yahan paste karein

client = Groq(api_key=GROQ_API_KEY)

def get_ai_response(user_prompt: str) -> str:
    system_prompt = (
        "You are PakShop AI Assistant. "
        "Strict Guidelines:\n"
        "1. Always reply in Roman Urdu (Urdu written in Latin script, e.g., 'Aap kaise hain?'). "
        "   NEVER use Hindi/Devanagari script or pure Arabic/Urdu script.\n"
        "2. Do NOT use HTML tags like <br>, <div>, or horizontal rules like '---'.\n"
        "3. Keep responses clean, concise, helpful, and natural."
    )
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=1024,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"