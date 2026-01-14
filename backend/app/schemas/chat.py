from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[UUID] = None


class ChatResponse(BaseModel):
    response: str
    session_id: str
