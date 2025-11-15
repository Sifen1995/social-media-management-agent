"""Scheduler endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.agents.base.orchestrator import orchestrator

router = APIRouter()

@router.post("/create-calendar")
async def create_content_calendar(brand_id: int, duration_days: int = 30, db: Session = Depends(get_db)):
    """Create content calendar using Scheduler Agent."""
    context = {"brand_id": brand_id}
    task = {"action": "create_calendar", "duration_days": duration_days}
    result = await orchestrator.execute_task("scheduler", task, context)
    return result
