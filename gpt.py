import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

async def ask_gpt(text: str, model: str = "gpt-3.5-turbo") -> str:
    messages = [
        {"role": "system", "content": "Ты полезный ассистент WhatsApp. Отвечай кратко и дружелюбно."},
        {"role": "user", "content": text}
    ]
    response = await openai.ChatCompletion.acreate(
        model=model,
        messages=messages,
        max_tokens=500,
        temperature=0.7
    )
    return response.choices[0].message.content.strip() 