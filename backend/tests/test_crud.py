from app.crud import message as message_crud
from app.crud import session as session_crud


def test_create_session(db_session):
    session = session_crud.create_session(db_session)
    assert session.id is not None
    assert session.created_at is not None
    session_crud.delete_session(db_session, session.id)


def test_get_session(db_session):
    created_session = session_crud.create_session(db_session)
    session_id = created_session.id
    retrieved = session_crud.get_session(db_session, session_id)
    assert retrieved is not None
    assert retrieved.id == session_id
    assert retrieved.created_at is not None
    session_crud.delete_session(db_session, session_id)


def test_create_message(db_session):
    session = session_crud.create_session(db_session)
    message = message_crud.create_message(
        db=db_session, session_id=session.id, role="user", content="Hello, world!"
    )
    assert message.id is not None
    assert message.session_id == session.id
    assert message.role == "user"
    assert message.content == "Hello, world!"
    assert message.created_at is not None
    message_crud.delete_message(db_session, message.id)
    session_crud.delete_session(db_session, session.id)


def test_get_message(db_session):
    session = session_crud.create_session(db_session)
    created_message = message_crud.create_message(
        db=db_session, session_id=session.id, role="user", content="Test message"
    )
    message_id = created_message.id
    retrieved = message_crud.get_message(db_session, message_id)
    assert retrieved is not None
    assert retrieved.id == message_id
    assert retrieved.content == "Test message"
    message_crud.delete_message(db_session, message_id)
    session_crud.delete_session(db_session, session.id)


def test_get_messages_by_session(db_session):
    session = session_crud.create_session(db_session)
    message1 = message_crud.create_message(
        db=db_session, session_id=session.id, role="user", content="First message"
    )
    message2 = message_crud.create_message(
        db=db_session, session_id=session.id, role="assistant", content="Second message"
    )
    messages = message_crud.get_messages_by_session(db_session, session.id)
    assert len(messages) >= 2
    message_ids = [m.id for m in messages]
    assert message1.id in message_ids
    assert message2.id in message_ids
    message_crud.delete_message(db_session, message1.id)
    message_crud.delete_message(db_session, message2.id)
    session_crud.delete_session(db_session, session.id)


def test_update_message(db_session):
    session = session_crud.create_session(db_session)
    message = message_crud.create_message(
        db=db_session, session_id=session.id, role="user", content="Original content"
    )
    message_id = message.id
    updated = message_crud.update_message(db_session, message_id, "Updated content")
    assert updated is not None
    assert updated.content == "Updated content"
    assert updated.id == message_id
    retrieved = message_crud.get_message(db_session, message_id)
    assert retrieved.content == "Updated content"
    message_crud.delete_message(db_session, message_id)
    session_crud.delete_session(db_session, session.id)


def test_delete_message(db_session):
    session = session_crud.create_session(db_session)
    message = message_crud.create_message(
        db=db_session, session_id=session.id, role="user", content="To be deleted"
    )
    message_id = message.id
    result = message_crud.delete_message(db_session, message_id)
    assert result is True
    retrieved = message_crud.get_message(db_session, message_id)
    assert retrieved is None
    session_crud.delete_session(db_session, session.id)
