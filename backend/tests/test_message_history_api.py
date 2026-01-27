from uuid import UUID

import pytest

from app.crud import message as message_crud
from app.crud import session as session_crud


@pytest.mark.asyncio
async def test_create_session_api(client):
    response = await client.post("/sessions")
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert "created_at" in data
    assert UUID(data["id"])


@pytest.mark.asyncio
async def test_get_sessions_api(client):
    await client.post("/sessions")
    await client.post("/sessions")

    response = await client.get("/sessions?skip=0&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert "sessions" in data
    assert "total" in data
    assert len(data["sessions"]) >= 2


@pytest.mark.asyncio
async def test_get_session_by_id_api(client):
    create_response = await client.post("/sessions")
    session_id = create_response.json()["id"]

    response = await client.get(f"/sessions/{session_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == session_id


@pytest.mark.asyncio
async def test_get_session_not_found(client):
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = await client.get(f"/sessions/{fake_id}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_message_history_api(client, db_session):
    session_response = await client.post("/sessions")
    session_id = session_response.json()["id"]

    session = await session_crud.get_session(db_session, UUID(session_id))
    await message_crud.create_message(
        db=db_session, session_id=session.id, role="user", content="Test message"
    )
    await message_crud.create_message(
        db=db_session, session_id=session.id, role="assistant", content="Test response"
    )
    await db_session.commit()

    response = await client.get(f"/sessions/{session_id}/messages")
    assert response.status_code == 200
    data = response.json()
    assert "messages" in data
    assert data["session_id"] == session_id
    assert len(data["messages"]) == 2
    assert data["messages"][0]["content"] == "Test message"
    assert data["messages"][1]["content"] == "Test response"


@pytest.mark.asyncio
async def test_get_message_history_pagination(client, db_session):
    session_response = await client.post("/sessions")
    session_id = session_response.json()["id"]

    session = await session_crud.get_session(db_session, UUID(session_id))
    for i in range(5):
        await message_crud.create_message(
            db=db_session, session_id=session.id, role="user", content=f"Message {i}"
        )
    await db_session.commit()

    response = await client.get(f"/sessions/{session_id}/messages?skip=0&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data["messages"]) == 2
    assert data["total"] == 5


@pytest.mark.asyncio
async def test_get_message_history_empty(client):
    session_response = await client.post("/sessions")
    session_id = session_response.json()["id"]

    response = await client.get(f"/sessions/{session_id}/messages")
    assert response.status_code == 200
    data = response.json()
    assert len(data["messages"]) == 0
    assert data["total"] == 0


@pytest.mark.asyncio
async def test_get_message_history_invalid_session(client):
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = await client.get(f"/sessions/{fake_id}/messages")
    assert response.status_code == 404
