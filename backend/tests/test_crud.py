import pytest

from app.crud import message as message_crud
from app.crud import session as session_crud


@pytest.mark.asyncio
async def test_create_session(db_session):
    session = await session_crud.create_session(db_session)
    assert session.id is not None
    assert session.created_at is not None
    await session_crud.delete_session(db_session, session.id)


@pytest.mark.asyncio
async def test_get_session(db_session):
    created_session = await session_crud.create_session(db_session)
    session_id = created_session.id
    retrieved = await session_crud.get_session(db_session, session_id)
    assert retrieved is not None
    assert retrieved.id == session_id
    assert retrieved.created_at is not None
    await session_crud.delete_session(db_session, session_id)


@pytest.mark.asyncio
async def test_create_message(db_session):
    session = await session_crud.create_session(db_session)
    message = await message_crud.create_message(
        db=db_session, session_id=session.id, role="user", content="Hello, world!"
    )
    assert message.id is not None
    assert message.session_id == session.id
    assert message.role == "user"
    assert message.content == "Hello, world!"
    assert message.created_at is not None
    await message_crud.delete_message(db_session, message.id)
    await session_crud.delete_session(db_session, session.id)


@pytest.mark.asyncio
async def test_get_message(db_session):
    session = await session_crud.create_session(db_session)
    created_message = await message_crud.create_message(
        db=db_session, session_id=session.id, role="user", content="Test message"
    )
    message_id = created_message.id
    retrieved = await message_crud.get_message(db_session, message_id)
    assert retrieved is not None
    assert retrieved.id == message_id
    assert retrieved.content == "Test message"
    await message_crud.delete_message(db_session, message_id)
    await session_crud.delete_session(db_session, session.id)


@pytest.mark.asyncio
async def test_get_messages_by_session(db_session):
    session = await session_crud.create_session(db_session)
    message1 = await message_crud.create_message(
        db=db_session, session_id=session.id, role="user", content="First message"
    )
    message2 = await message_crud.create_message(
        db=db_session, session_id=session.id, role="assistant", content="Second message"
    )
    messages = await message_crud.get_messages_by_session(db_session, session.id)
    assert len(messages) >= 2
    message_ids = [m.id for m in messages]
    assert message1.id in message_ids
    assert message2.id in message_ids
    await message_crud.delete_message(db_session, message1.id)
    await message_crud.delete_message(db_session, message2.id)
    await session_crud.delete_session(db_session, session.id)


@pytest.mark.asyncio
async def test_update_message(db_session):
    session = await session_crud.create_session(db_session)
    message = await message_crud.create_message(
        db=db_session, session_id=session.id, role="user", content="Original content"
    )
    message_id = message.id
    updated = await message_crud.update_message(
        db_session, message_id, "Updated content"
    )
    assert updated is not None
    assert updated.content == "Updated content"
    assert updated.id == message_id
    retrieved = await message_crud.get_message(db_session, message_id)
    assert retrieved.content == "Updated content"
    await message_crud.delete_message(db_session, message_id)
    await session_crud.delete_session(db_session, session.id)


@pytest.mark.asyncio
async def test_delete_message(db_session):
    session = await session_crud.create_session(db_session)
    message = await message_crud.create_message(
        db=db_session, session_id=session.id, role="user", content="To be deleted"
    )
    message_id = message.id
    result = await message_crud.delete_message(db_session, message_id)
    assert result is True
    retrieved = await message_crud.get_message(db_session, message_id)
    assert retrieved is None
    await session_crud.delete_session(db_session, session.id)
