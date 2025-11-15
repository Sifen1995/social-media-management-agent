"""Content Pydantic schemas."""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class ContentStatus(str, Enum):
    """Content status enum."""

    draft = "draft"
    scheduled = "scheduled"
    published = "published"
    failed = "failed"


class ContentType(str, Enum):
    """Content type enum."""

    post = "post"
    story = "story"
    reel = "reel"
    video = "video"
    carousel = "carousel"


class Platform(str, Enum):
    """Platform enum."""

    instagram = "instagram"
    facebook = "facebook"
    twitter = "twitter"
    linkedin = "linkedin"
    tiktok = "tiktok"
    youtube = "youtube"


class ContentBase(BaseModel):
    """Base content schema."""

    platform: Platform
    content_type: ContentType
    caption: Optional[str] = None
    media_url: Optional[str] = None
    hashtags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


class ContentCreate(BaseModel):
    """Schema for creating content."""

    brand_id: int
    platform: Platform
    content_type: ContentType = ContentType.post
    caption: Optional[str] = None
    media_url: Optional[str] = None
    hashtags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None
    scheduled_for: Optional[datetime] = None


class ContentUpdate(BaseModel):
    """Schema for updating content."""

    caption: Optional[str] = None
    media_url: Optional[str] = None
    hashtags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None
    scheduled_for: Optional[datetime] = None
    status: Optional[ContentStatus] = None


class ContentResponse(BaseModel):
    """Schema for content response."""

    id: int
    brand_id: int
    platform: Platform
    content_type: ContentType
    caption: Optional[str] = None
    media_url: Optional[str] = None
    hashtags: Optional[List[str]] = None
    status: ContentStatus
    scheduled_for: Optional[datetime] = None
    published_at: Optional[datetime] = None
    platform_post_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ContentGenerateRequest(BaseModel):
    """Schema for content generation request."""

    brand_id: int
    platform: Platform
    topic: str = Field(..., min_length=1)
    content_type: ContentType = ContentType.post
    count: int = Field(default=1, ge=1, le=10)
    additional_instructions: Optional[str] = None


class ContentPlanRequest(BaseModel):
    """Schema for plan-and-execute request."""

    brand_id: int
    user_request: str = Field(..., min_length=1)


class ContentWithAnalytics(ContentResponse):
    """Content response with analytics."""

    likes: int = 0
    comments: int = 0
    shares: int = 0
    reach: int = 0
    engagement_rate: float = 0.0
