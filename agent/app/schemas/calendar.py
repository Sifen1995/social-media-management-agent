"""Calendar Pydantic schemas."""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CalendarItemBase(BaseModel):
    """Base calendar item schema."""

    scheduled_for: datetime
    platform: str
    notes: Optional[str] = None


class CalendarItemCreate(BaseModel):
    """Schema for creating a calendar item."""

    brand_id: int
    content_id: Optional[int] = None
    scheduled_for: datetime
    platform: str
    content_type: str = "post"
    notes: Optional[str] = None


class CalendarItemUpdate(BaseModel):
    """Schema for updating a calendar item."""

    scheduled_for: Optional[datetime] = None
    content_id: Optional[int] = None
    notes: Optional[str] = None


class CalendarItemResponse(BaseModel):
    """Schema for calendar item response."""

    id: int
    brand_id: int
    content_id: Optional[int] = None
    scheduled_for: datetime
    platform: str
    content_type: str
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class CalendarCreateRequest(BaseModel):
    """Schema for creating a content calendar."""

    brand_id: int
    duration_days: int = Field(default=7, ge=1, le=90)
    platforms: list[str] = Field(default=["instagram"])
    posts_per_week: int = Field(default=5, ge=1, le=14)
    start_date: Optional[datetime] = None
