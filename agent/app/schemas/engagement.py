"""Engagement Pydantic schemas."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class EngagementItemResponse(BaseModel):
    """Schema for engagement item response."""

    id: int
    brand_id: int
    platform: str
    message_type: str  # comment, dm, mention
    content: str
    username: str
    platform_message_id: str
    status: str  # pending, replied, ignored
    suggested_reply: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class EngagementReplyRequest(BaseModel):
    """Schema for generating engagement reply."""

    brand_id: int
    message_type: str
    content: str
    username: str
    context: Optional[str] = None


class EngagementReplyResponse(BaseModel):
    """Schema for engagement reply response."""

    suggested_reply: str
    confidence: float = 1.0
    requires_human_review: bool = False


class EngagementFilterRequest(BaseModel):
    """Schema for filtering spam."""

    brand_id: int
    messages: list[dict]


class EngagementPrioritizeRequest(BaseModel):
    """Schema for prioritizing engagement items."""

    brand_id: int
    limit: int = 20
