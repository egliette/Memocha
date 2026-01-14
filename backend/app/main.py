from datetime import datetime, timezone
from uuid import uuid4

from app.core.database import get_db
from app.models.message import Message
from app.models.session import Session as SessionModel
from app.schemas.chat import ChatRequest, ChatResponse
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

app = FastAPI(title="Memocha")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    if request.session_id:
        session = (
            db.query(SessionModel).filter(SessionModel.id == request.session_id).first()
        )
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
    else:
        session = SessionModel(id=uuid4(), created_at=datetime.now(timezone.utc))
        db.add(session)
        db.commit()
        db.refresh(session)

    user_message = Message(
        id=uuid4(),
        session_id=session.id,
        role="user",
        content=request.message,
        created_at=datetime.now(timezone.utc),
    )
    db.add(user_message)

    response_text = f"You said {request.message}"

    assistant_message = Message(
        id=uuid4(),
        session_id=session.id,
        role="assistant",
        content=response_text,
        created_at=datetime.now(timezone.utc),
    )
    db.add(assistant_message)
    db.commit()

    return ChatResponse(response=response_text, session_id=str(session.id))
