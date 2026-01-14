from app.models.base import Base
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID


class Session(Base):
    __tablename__ = "sessions"

    id = Column(UUID, primary_key=True)
    created_at = Column(DateTime)
