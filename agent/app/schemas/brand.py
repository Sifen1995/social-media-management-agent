"""Brand Pydantic schemas."""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class BrandBase(BaseModel):
    """Base brand schema."""

    name: str = Field(..., min_length=1, max_length=200)
    niche: Optional[str] = None
    brand_voice: Optional[str] = None
    target_audience: Optional[str] = None
    goals: Optional[List[str]] = None


class BrandCreate(BrandBase):
    """Schema for creating a brand."""

    pass


class BrandUpdate(BaseModel):
    """Schema for updating a brand."""

    name: Optional[str] = Field(None, min_length=1, max_length=200)
    niche: Optional[str] = None
    brand_voice: Optional[str] = None
    target_audience: Optional[str] = None
    goals: Optional[List[str]] = None


class BrandResponse(BrandBase):
    """Schema for brand response."""

    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class BrandWithStats(BrandResponse):
    """Brand response with statistics."""

    total_content: int = 0
    total_posts: int = 0
    total_accounts: int = 0
