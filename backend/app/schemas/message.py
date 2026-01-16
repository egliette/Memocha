from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class MessageBase(BaseModel):
    role: str
    content: str


class MessageCreate(MessageBase):
    session_id: UUID


class MessageResponse(MessageBase):
    id: UUID
    session_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class MessageHistoryResponse(BaseModel):
    messages: list[MessageResponse]
    session_id: UUID
    total: int
    skip: int
    limit: int
