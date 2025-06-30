from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class Message(BaseModel):
    text: str = Field(..., min_length=1, max_length=4000, description="Текст сообщения")
    user_id: Optional[str] = Field(None, description="ID пользователя")
    session_id: Optional[str] = Field(None, description="ID сессии")

class AIResponse(BaseModel):
    response: str
    session_id: str
    timestamp: datetime
    tokens_used: Optional[int] = None

class HealthCheck(BaseModel):
    status: str
    timestamp: datetime
    version: str

class ChatMessage(BaseModel):
    role: str
    content: str
    timestamp: datetime

class SessionHistory(BaseModel):
    session_id: str
    messages: List[ChatMessage]
    message_count: int

class Stats(BaseModel):
    total_sessions: int
    total_messages: int
    active_sessions: int
    timestamp: datetime 