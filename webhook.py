from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
load_dotenv()
import logging
from gpt import ask_gpt
from whatsapp import send_whatsapp_message

router = APIRouter()
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "whatsapp_verify_token")

logging.basicConfig(level=logging.INFO)

@router.get("/webhook")
async def verify_webhook(request: Request):
    params = request.query_params
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return int(challenge)
    return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": "Verification failed"})

@router.post("/webhook")
async def receive_whatsapp_webhook(payload: dict):
    logging.info(f"Received WhatsApp webhook: {payload}")
    try:
        # Извлекаем текст и номер отправителя
        entry = payload.get("entry", [{}])[0]
        changes = entry.get("changes", [{}])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [])
        if not messages:
            return {"status": "no_message"}
        msg = messages[0]
        from_number = msg["from"]
        text = msg["text"]["body"]
        # Получаем ответ от GPT
        gpt_response = await ask_gpt(text)
        # Отправляем ответ клиенту
        await send_whatsapp_message(from_number, gpt_response)
        logging.info(f"Ответ отправлен: {gpt_response}")
        return {"status": "ok", "gpt_response": gpt_response}
    except Exception as e:
        logging.error(f"Ошибка обработки webhook: {e}")
        return JSONResponse(status_code=500, content={"detail": str(e)}) 