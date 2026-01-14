from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.models.message import Message
from sqlalchemy.orm import Session


def create_message(db: Session, session_id: UUID, role: str, content: str) -> Message:
    message = Message(
        id=uuid4(),
        session_id=session_id,
        role=role,
        content=content,
        created_at=datetime.now(timezone.utc),
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def get_message(db: Session, message_id: UUID) -> Message | None:
    """Get a message by ID"""
    return db.query(Message).filter(Message.id == message_id).first()


def get_messages_by_session(
    db: Session, session_id: UUID, skip: int = 0, limit: int = 100
):
    """Get all messages for a session with pagination"""
    return (
        db.query(Message)
        .filter(Message.session_id == session_id)
        .order_by(Message.created_at)
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_message(db: Session, message_id: UUID, content: str) -> Message | None:
    message = get_message(db, message_id)
    if not message:
        return None
    message.content = content
    db.commit()
    db.refresh(message)
    return message


def delete_message(db: Session, message_id: UUID) -> bool:
    message = get_message(db, message_id)
    if not message:
        return False
    db.delete(message)
    db.commit()
    return True
