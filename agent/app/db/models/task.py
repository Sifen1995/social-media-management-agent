"""
Task database model.
"""
from sqlalchemy import Column, String, Integer, ForeignKey, Text, Enum, DateTime, JSON
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
import enum


class TaskType(enum.Enum):
    """Types of tasks agents can perform."""
    CONTENT_GENERATION = "content_generation"
    ANALYTICS_REPORT = "analytics_report"
    SCHEDULE_PLANNING = "schedule_planning"
    ENGAGEMENT_RESPONSE = "engagement_response"
    SOCIAL_LISTENING = "social_listening"
    OPTIMIZATION = "optimization"
    MULTI_STEP = "multi_step"


class TaskStatus(enum.Enum):
    """Status of task execution."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Task(BaseModel):
    """
    Task model - represents work items for the multi-agent system.
    """
    __tablename__ = "tasks"

    brand_id = Column(Integer, ForeignKey("brands.id", ondelete="CASCADE"), nullable=False)
    task_type = Column(Enum(TaskType), nullable=False)

    # Task details
    description = Column(Text, nullable=False)
    parameters = Column(JSON, nullable=True)  # Input parameters for the task

    # Execution details
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING, nullable=False)
    assigned_agent = Column(String(100), nullable=True)  # Which agent is handling this
    priority = Column(Integer, default=5, nullable=False)  # 1 (highest) to 10 (lowest)

    # Results
    result = Column(JSON, nullable=True)  # Task output
    error_message = Column(Text, nullable=True)

    # Timing
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    # Parent-child relationships for multi-step tasks
    parent_task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=True)

    # Relationships
    brand = relationship("Brand", back_populates="tasks")
    subtasks = relationship("Task", backref="parent_task", remote_side="Task.id")

    def __repr__(self):
        return f"<Task(id={self.id}, type={self.task_type.value}, status={self.status.value})>"
