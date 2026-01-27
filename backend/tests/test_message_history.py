import pytest

from app.crud import message as message_crud
from app.crud import session as session_crud


@pytest.mark.asyncio
async def test_create_message_via_crud(db_session):
    session = await session_crud.create_session(db_session)
    message = await message_crud.create_message(
        db=db_session, session_id=session.id, role="user", content="Test message"
    )
    assert message.id is not None
    assert message.session_id == session.id
    assert message.role == "user"
    assert message.content == "Test message"
    assert message.created_at is not None


@pytest.mark.asyncio
async def test_get_message_history_by_session(db_session):
    session = await session_crud.create_session(db_session)

    await message_crud.create_message(
        db=db_session, session_id=session.id, role="user", content="Message 1"
    )
    await message_crud.create_message(
        db=db_session, session_id=session.id, role="assistant", content="Response 1"
    )
    await message_crud.create_message(
        db=db_session, session_id=session.id, role="user", content="Message 2"
    )

    messages = await message_crud.get_messages_by_session(db_session, session.id)
    assert len(messages) == 3
    assert messages[0].content == "Message 1"
    assert messages[1].content == "Response 1"
    assert messages[2].content == "Message 2"


@pytest.mark.asyncio
async def test_message_history_pagination(db_session):
    session = await session_crud.create_session(db_session)

    for i in range(5):
        await message_crud.create_message(
            db=db_session, session_id=session.id, role="user", content=f"Message {i}"
        )

    messages_page1 = await message_crud.get_messages_by_session(
        db_session, session.id, skip=0, limit=2
    )
    assert len(messages_page1) == 2

    messages_page2 = await message_crud.get_messages_by_session(
        db_session, session.id, skip=2, limit=2
    )
    assert len(messages_page2) == 2
    assert messages_page1[0].id != messages_page2[0].id


@pytest.mark.asyncio
async def test_message_history_empty_session(db_session):
    session = await session_crud.create_session(db_session)
    messages = await message_crud.get_messages_by_session(db_session, session.id)
    assert len(messages) == 0


@pytest.mark.asyncio
async def test_message_history_isolation(db_session):
    session1 = await session_crud.create_session(db_session)
    session2 = await session_crud.create_session(db_session)

    await message_crud.create_message(
        db=db_session, session_id=session1.id, role="user", content="Session 1 message"
    )
    await message_crud.create_message(
        db=db_session, session_id=session2.id, role="user", content="Session 2 message"
    )

    messages1 = await message_crud.get_messages_by_session(db_session, session1.id)
    messages2 = await message_crud.get_messages_by_session(db_session, session2.id)

    assert len(messages1) == 1
    assert len(messages2) == 1
    assert messages1[0].session_id == session1.id
    assert messages2[0].session_id == session2.id
