"""Task Pydantic schemas."""
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime


class TaskResponse(BaseModel):
    """Schema for task response."""

    id: int
    agent_name: str
    task_type: str
    parameters: Dict[str, Any]
    status: str  # pending, running, completed, failed
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    parent_task_id: Optional[int] = None
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TaskCreate(BaseModel):
    """Schema for creating a task."""

    agent_name: str
    task_type: str
    parameters: Dict[str, Any]
    parent_task_id: Optional[int] = None


class AgentInfo(BaseModel):
    """Schema for agent information."""

    name: str
    description: str
    capabilities: List[str]


class AgentListResponse(BaseModel):
    """Schema for listing agents."""

    agents: List[AgentInfo]
