from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.session import Session as SessionModel


async def create_session(db: AsyncSession) -> SessionModel:
    session = SessionModel(id=uuid4(), created_at=datetime.now(timezone.utc))
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session


async def get_session(db: AsyncSession, session_id: UUID) -> SessionModel | None:
    result = await db.execute(
        select(SessionModel).filter(SessionModel.id == session_id)
    )
    return result.scalar_one_or_none()


async def get_all_sessions(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> list[SessionModel]:
    """Get all sessions with pagination"""
    result = await db.execute(select(SessionModel).offset(skip).limit(limit))
    return result.scalars().all()


async def count_sessions(db: AsyncSession) -> int | None:
    result = await db.execute(select(func.count()).select_from(SessionModel))
    total = result.scalar()
    return total


async def delete_session(db: AsyncSession, session_id: UUID) -> bool:
    session = await get_session(db, session_id)
    if not session:
        return False
    await db.delete(session)
    await db.commit()
    return True
