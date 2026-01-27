from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID

from app.models.base import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID, primary_key=True)
    session_id = Column(UUID, ForeignKey("sessions.id"))
    role = Column(String)
    content = Column(Text)
    created_at = Column(DateTime(timezone=True))
