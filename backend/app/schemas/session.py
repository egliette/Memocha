from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class SessionBase(BaseModel):
    pass


class SessionCreate(SessionBase):
    pass


class SessionResponse(SessionBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class SessionListResponse(BaseModel):
    sessions: list[SessionResponse]
    total: int
    skip: int
    limit: int
