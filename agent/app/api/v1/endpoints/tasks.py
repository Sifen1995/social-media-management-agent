"""Task management endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Task
from app.agents.base.orchestrator import orchestrator

router = APIRouter()

@router.get("/agents")
async def list_available_agents():
    """List all registered agents."""
    agents = orchestrator.list_agents()
    return {"agents": agents}

@router.get("/{task_id}")
async def get_task(task_id: int, db: Session = Depends(get_db)):
    """Get task details."""
    task = db.query(Task).filter(Task.id == task_id).first()
    return task

@router.get("/")
async def list_tasks(brand_id: int, limit: int = 50, db: Session = Depends(get_db)):
    """List tasks for a brand."""
    tasks = db.query(Task).filter(Task.brand_id == brand_id).order_by(Task.created_at.desc()).limit(limit).all()
    return {"tasks": tasks}
