import openai
import os
from datetime import datetime
from typing import Dict, List, Optional
from loguru import logger

class OpenAIService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        openai.api_key = self.api_key
        self.model = "gpt-3.5-turbo"
    
    async def generate_response(self, messages: List[Dict[str, str]], max_tokens: int = 500, temperature: float = 0.7) -> Dict:
        """
        Генерирует ответ от OpenAI API
        """
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return {
                "content": response.choices[0].message.content,
                "tokens_used": response.usage.total_tokens if hasattr(response, 'usage') else None,
                "model": self.model
            }
            
        except openai.error.OpenAIError as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error in OpenAI service: {str(e)}")
            raise e

class SessionService:
    def __init__(self):
        self.sessions: Dict[str, List[Dict]] = {}
        self.max_messages_per_session = 20
    
    def create_session(self, session_id: str) -> str:
        """Создает новую сессию"""
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        return session_id
    
    def add_message(self, session_id: str, role: str, content: str) -> None:
        """Добавляет сообщение в сессию"""
        if session_id not in self.sessions:
            self.create_session(session_id)
        
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now()
        }
        
        self.sessions[session_id].append(message)
        
        # Ограничиваем размер истории
        if len(self.sessions[session_id]) > self.max_messages_per_session:
            self.sessions[session_id] = self.sessions[session_id][-self.max_messages_per_session:]
    
    def get_session_messages(self, session_id: str, limit: int = 10) -> List[Dict]:
        """Получает сообщения сессии для контекста"""
        if session_id not in self.sessions:
            return []
        
        return self.sessions[session_id][-limit:]
    
    def delete_session(self, session_id: str) -> bool:
        """Удаляет сессию"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False
    
    def get_stats(self) -> Dict:
        """Получает статистику по сессиям"""
        total_sessions = len(self.sessions)
        total_messages = sum(len(messages) for messages in self.sessions.values())
        
        return {
            "total_sessions": total_sessions,
            "total_messages": total_messages,
            "active_sessions": total_sessions
        } 