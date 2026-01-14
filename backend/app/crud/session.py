from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.models.session import Session as SessionModel
from sqlalchemy.orm import Session


def create_session(db: Session) -> SessionModel:
    session = SessionModel(id=uuid4(), created_at=datetime.now(timezone.utc))
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_session(db: Session, session_id: UUID) -> SessionModel | None:
    """Get a session by ID"""
    return db.query(SessionModel).filter(SessionModel.id == session_id).first()


def get_all_sessions(db: Session, skip: int = 0, limit: int = 100):
    """Get all sessions with pagination"""
    return db.query(SessionModel).offset(skip).limit(limit).all()


def delete_session(db: Session, session_id: UUID) -> bool:
    session = get_session(db, session_id)
    if not session:
        return False
    db.delete(session)
    db.commit()
    return True
