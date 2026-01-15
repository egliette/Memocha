from app.core.config import settings
from app.core.database import get_db
from app.core.logging import setup_logging
from app.crud import message as message_crud
from app.crud import session as session_crud
from app.schemas.chat import ChatRequest, ChatResponse
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

setup_logging(settings.log_level)

app = FastAPI(title="Memocha")


@app.get("/health")
def health_check():
    return {"status": "ok"}


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

    response_text = f"You said {request.message}"

    message_crud.create_message(
        db=db, session_id=session.id, role="assistant", content=response_text
    )

    return ChatResponse(response=response_text, session_id=str(session.id))
