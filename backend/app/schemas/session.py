from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SessionBase(BaseModel):
    pass


class SessionCreate(SessionBase):
    pass


class SessionResponse(SessionBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime


class SessionListResponse(BaseModel):
    sessions: list[SessionResponse]
    total: int
    skip: int
    limit: int
