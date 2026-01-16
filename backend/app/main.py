from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.exceptions import (
    LLMConnectionError,
    LLMRateLimitError,
    LLMServiceError,
    LLMTimeoutError,
)
from app.core.logging import setup_logging
from app.core.prompts import BASE_SYSTEM_PROMPT
from app.crud import message as message_crud
from app.crud import session as session_crud
from app.models.message import Message
from app.models.session import Session as SessionModel
from app.schemas.chat import ChatRequest, ChatResponse
from app.schemas.message import MessageHistoryResponse, MessageResponse
from app.schemas.session import SessionListResponse, SessionResponse
from app.services.llm_service import get_llm_service

setup_logging(settings.log_level)

app = FastAPI(title="Memocha")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/sessions", response_model=SessionResponse, status_code=201)
async def create_session(db: Session = Depends(get_db)):
    session = session_crud.create_session(db)
    return SessionResponse.model_validate(session)


@app.get("/sessions", response_model=SessionListResponse)
async def get_sessions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sessions = session_crud.get_all_sessions(db, skip=skip, limit=limit)
    total = db.query(SessionModel).count()

    return SessionListResponse(
        sessions=[SessionResponse.model_validate(s) for s in sessions],
        total=total,
        skip=skip,
        limit=limit,
    )


@app.get("/sessions/{session_id}", response_model=SessionResponse)
async def get_session(session_id: UUID, db: Session = Depends(get_db)):
    session = session_crud.get_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return SessionResponse.model_validate(session)


@app.get("/sessions/{session_id}/messages", response_model=MessageHistoryResponse)
async def get_message_history(
    session_id: UUID, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    session = session_crud.get_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    messages = message_crud.get_messages_by_session(
        db, session_id, skip - skip, limit=limit
    )

    total = db.query(Message).filter(Message.session_id == session_id).count()

    return MessageHistoryResponse(
        messages=[MessageResponse.model_validate(m) for m in messages],
        session_id=session_id,
        total=total,
        skip=skip,
        limit=limit,
    )


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    if request.session_id:
        session = session_crud.get_session(db, request.session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
    else:
        session = session_crud.create_session(db)

    message_crud.create_message(
        db=db, session_id=session.id, role="user", content=request.message
    )

    history_messages = message_crud.get_messages_by_session(
        db=db,
        session_id=session.id,
        skip=0,
        limit=50,
    )

    message_history = [
        {"role": msg.role, "content": msg.content} for msg in history_messages[:-1]
    ]

    llm_service = get_llm_service()
    try:
        response_text = llm_service.chat_with_history(
            user_message=request.message,
            message_history=message_history,
            system_prompt=BASE_SYSTEM_PROMPT,
        )
    except LLMRateLimitError:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    except LLMConnectionError:
        raise HTTPException(status_code=503, detail="LLM service unavailable")
    except LLMTimeoutError:
        raise HTTPException(status_code=504, detail="LLM request timed out")
    except LLMServiceError as e:
        raise HTTPException(status_code=500, detail=f"LLM service error: {str(e)}")

    message_crud.create_message(
        db=db, session_id=session.id, role="assistant", content=response_text
    )

    return ChatResponse(response=response_text, session_id=str(session.id))
