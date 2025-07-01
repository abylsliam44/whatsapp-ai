import os
import httpx
from dotenv import load_dotenv
import logging

load_dotenv()
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

logging.basicConfig(level=logging.INFO)

async def send_whatsapp_message(to_number: str, text: str) -> dict:
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": text}
    }

    # Подробное логирование для отладки
    logging.info(f"WHATSAPP_TOKEN (first 8 chars): {WHATSAPP_TOKEN[:8] if WHATSAPP_TOKEN else 'None'}")
    logging.info(f"PHONE_NUMBER_ID: {PHONE_NUMBER_ID}")
    logging.info(f"Request URL: {url}")
    logging.info(f"Request headers: {headers}")
    logging.info(f"Request payload: {data}")

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)
        logging.info(f"Response status: {response.status_code}")
        logging.info(f"Response body: {response.text}")
        return response.json() 