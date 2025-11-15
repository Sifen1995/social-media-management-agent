"""Engagement endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.agents.base.orchestrator import orchestrator
from pydantic import BaseModel

router = APIRouter()

class ReplyRequest(BaseModel):
    brand_id: int
    message_type: str
    content: str
    username: str = "User"

@router.post("/generate-reply")
async def generate_reply(request: ReplyRequest, db: Session = Depends(get_db)):
    """Generate reply using Engagement Agent."""
    context = {"brand_id": request.brand_id}
    task = {
        "action": "reply",
        "message_type": request.message_type,
        "content": request.content,
        "username": request.username
    }
    result = await orchestrator.execute_task("engagement", task, context)
    return result
