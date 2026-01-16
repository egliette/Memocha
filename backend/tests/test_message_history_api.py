from uuid import UUID

from app.crud import message as message_crud
from app.crud import session as session_crud


def test_create_session_api(client):
    response = client.post("/sessions")
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert "created_at" in data
    assert UUID(data["id"])


def test_get_sessions_api(client):
    client.post("/sessions")
    client.post("/sessions")

    response = client.get("/sessions?skip=0&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert "sessions" in data
    assert "total" in data
    assert len(data["sessions"]) >= 2


def test_get_session_by_id_api(client):
    create_response = client.post("/sessions")
    session_id = create_response.json()["id"]

    response = client.get(f"/sessions/{session_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == session_id


def test_get_session_not_found(client):
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/sessions/{fake_id}")
    assert response.status_code == 404


def test_get_message_history_api(client, db_session):
    session_response = client.post("/sessions")
    session_id = session_response.json()["id"]

    session = session_crud.get_session(db_session, UUID(session_id))
    message_crud.create_message(
        db=db_session, session_id=session.id, role="user", content="Test message"
    )
    message_crud.create_message(
        db=db_session, session_id=session.id, role="assistant", content="Test response"
    )
    db_session.commit()

    response = client.get(f"/sessions/{session_id}/messages")
    assert response.status_code == 200
    data = response.json()
    assert "messages" in data
    assert data["session_id"] == session_id
    assert len(data["messages"]) == 2
    assert data["messages"][0]["content"] == "Test message"
    assert data["messages"][1]["content"] == "Test response"


def test_get_message_history_pagination(client, db_session):
    session_response = client.post("/sessions")
    session_id = session_response.json()["id"]

    session = session_crud.get_session(db_session, UUID(session_id))
    for i in range(5):
        message_crud.create_message(
            db=db_session, session_id=session.id, role="user", content=f"Message {i}"
        )
    db_session.commit()

    response = client.get(f"/sessions/{session_id}/messages?skip=0&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data["messages"]) == 2
    assert data["total"] == 5


def test_get_message_history_empty(client):
    session_response = client.post("/sessions")
    session_id = session_response.json()["id"]

    response = client.get(f"/sessions/{session_id}/messages")
    assert response.status_code == 200
    data = response.json()
    assert len(data["messages"]) == 0
    assert data["total"] == 0


def test_get_message_history_invalid_session(client):
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/sessions/{fake_id}/messages")
    assert response.status_code == 404
