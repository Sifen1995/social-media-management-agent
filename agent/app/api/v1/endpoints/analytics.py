"""Analytics endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.agents.base.orchestrator import orchestrator

router = APIRouter()

@router.post("/generate-report")
async def generate_analytics_report(brand_id: int, time_period: str = "last_30_days", db: Session = Depends(get_db)):
    """Generate analytics report using Analytics Agent."""
    context = {"brand_id": brand_id}
    task = {"action": "report", "time_period": time_period}
    result = await orchestrator.execute_task("analytics", task, context)
    return result
