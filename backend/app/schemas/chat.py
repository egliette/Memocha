from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[UUID] = Field(
        default=None,
        examples=[None],
    )


class ChatResponse(BaseModel):
    response: str
    session_id: str
