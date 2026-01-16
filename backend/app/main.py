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
from app.schemas.chat import ChatRequest, ChatResponse
from app.schemas.message import MessageHistoryResponse, MessageResponse
from app.schemas.session import SessionCreate, SessionResponse
from app.services.llm_service import get_llm_service

setup_logging(settings.log_level)

app = FastAPI(title="Memocha")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/sessions", reponse_model=SessionResponse, status_code=201)
async def create_session(db: Session = Depends(get_db)):
    session = session_crud.create_session(db)
    return SessionResponse.model_validate(session)


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

    llm_service = get_llm_service()
    try:
        response_text = llm_service.chat(
            user_message=request.message, system_prompt=BASE_SYSTEM_PROMPT
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
