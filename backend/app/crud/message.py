from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.message import Message


async def create_message(
    db: AsyncSession, session_id: UUID, role: str, content: str
) -> Message:
    message = Message(
        id=uuid4(),
        session_id=session_id,
        role=role,
        content=content,
        created_at=datetime.now(timezone.utc),
    )
    db.add(message)
    await db.commit()
    await db.refresh(message)
    return message


async def get_message(db: AsyncSession, message_id: UUID) -> Message | None:
    result = await db.execute(select(Message).filter(Message.id == message_id))
    return result.scalar_one_or_none()


async def get_messages_by_session(
    db: AsyncSession, session_id: UUID, skip: int = 0, limit: int = 100
) -> list[Message]:
    """Get all messages for a session with pagination"""
    result = await db.execute(
        select(Message)
        .filter(Message.session_id == session_id)
        .order_by(Message.created_at)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def count_messages_by_session(db: AsyncSession, session_id: UUID) -> int | None:
    result = await db.execute(
        select(func.count())
        .select_from(Message)
        .filter(Message.session_id == session_id)
    )
    total = result.scalar()
    return total


async def update_message(
    db: AsyncSession, message_id: UUID, content: str
) -> Message | None:
    message = await get_message(db, message_id)
    if not message:
        return None
    message.content = content
    await db.commit()
    await db.refresh(message)
    return message


async def delete_message(db: AsyncSession, message_id: UUID) -> bool:
    message = await get_message(db, message_id)
    if not message:
        return False
    await db.delete(message)
    await db.commit()
    return True
