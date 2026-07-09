from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class ChatAskRequest(BaseModel):
    document_id: UUID
    question: str


class ChatAskResponse(BaseModel):
    answer: str


class ChatHistoryItem(BaseModel):
    question: str
    answer: str
    created_at: datetime

    class Config:
        from_attributes = True