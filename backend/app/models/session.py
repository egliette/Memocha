from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID

from app.models.base import Base


class Session(Base):
    __tablename__ = "sessions"

    id = Column(UUID, primary_key=True)
    created_at = Column(DateTime(timezone=True))
