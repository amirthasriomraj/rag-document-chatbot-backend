from datetime import datetime
from uuid import UUID
from typing import List

from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: UUID
    filename: str
    processing_status: str
    upload_time: datetime
    summary: str | None

    class Config:
        from_attributes = True


class DocumentListItem(BaseModel):
    id: UUID
    filename: str
    processing_status: str
    upload_time: datetime
    summary: str | None = None

    class Config:
        from_attributes = True