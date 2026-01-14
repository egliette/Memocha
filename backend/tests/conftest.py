from collections.abc import Generator

import pytest
from app.core.database import SessionLocal, engine
from app.main import app
from app.models.message import Message
from app.models.session import Session as SessionModel
from fastapi.testclient import TestClient
from sqlalchemy import delete
from sqlalchemy.orm import Session


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session
        statement = delete(Message)
        session.execute(statement)
        statement = delete(SessionModel)
        session.execute(statement)
        session.commit()


@pytest.fixture(scope="function")
def db_session(db: Session) -> Generator[Session, None, None]:
    yield db
    db.rollback()


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c
