"""
Calendar database model.
"""
from sqlalchemy import Column, String, Integer, ForeignKey, Date, Time, Text, Enum
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
import enum


class CalendarStatus(enum.Enum):
    """Status of calendar slots."""
    PLANNED = "planned"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    SKIPPED = "skipped"


class CalendarItem(BaseModel):
    """
    Calendar Item model - represents planned content slots in the content calendar.
    """
    __tablename__ = "content_calendar"

    brand_id = Column(Integer, ForeignKey("brands.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False)
    time_slot = Column(Time, nullable=True)

    # Platform and content type
    platform = Column(String(50), nullable=False)
    content_type = Column(String(50), nullable=True)

    # Reference to actual content
    content_item_id = Column(Integer, ForeignKey("content_items.id", ondelete="SET NULL"), nullable=True)

    # Planning details
    topic = Column(String(500), nullable=True)
    theme = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)

    # Status
    status = Column(Enum(CalendarStatus), default=CalendarStatus.PLANNED, nullable=False)

    # AI suggestions
    suggested_by_agent = Column(String(100), nullable=True)
    optimal_time_reason = Column(Text, nullable=True)

    # Relationships
    brand = relationship("Brand", back_populates="calendar_items")

    def __repr__(self):
        return f"<CalendarItem(id={self.id}, date={self.date}, platform={self.platform}, status={self.status.value})>"
