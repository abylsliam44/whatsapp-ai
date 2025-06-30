import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

system_prompt = (
    "Ты — интеллектуальный ассистент Caravan of Knowledge. "
    "Caravan of Knowledge — организация, основанная в 2020 году, "
    "продвигающая STEAM-образование в Казахстане. "
    "Мы реализуем проекты для учителей и учеников: курсы, мастер-классы, тренинги, гранты, "
    "летние лагеря, конференции, библиотеку методических материалов. "
    "Наша цель — сделать образование качественным, доступным и вдохновляющим для всех. "
    "Если у пользователя вопросы о программах, курсах, грантах, мероприятиях, библиотеке, "
    "или о компании — отвечай подробно и дружелюбно, используя только достоверную информацию с сайта https://caravanofknowledge.com/. "
    "Если вопрос не по теме — вежливо объясни, что ты ассистент Caravan of Knowledge и можешь рассказать только о деятельности компании."
)

async def ask_gpt(text: str, model: str = "gpt-3.5-turbo") -> str:
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": text}
    ]
    response = await client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=500,
        temperature=0.7
    )
    return response.choices[0].message.content.strip() 