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


class SocialLinks(BaseModel):
    """Social media links for brand research."""

    instagram: Optional[str] = None
    linkedin: Optional[str] = None
    twitter: Optional[str] = None
    tiktok: Optional[str] = None
    facebook: Optional[str] = None


class AutoProfileRequest(BaseModel):
    """Request schema for auto brand profile generation."""

    website: str = Field(..., min_length=1, description="Website URL to scrape")
    socials: Optional[SocialLinks] = Field(default=None, description="Social media profile URLs")
    use_playwright: Optional[bool] = Field(default=False, description="Use Playwright for JS-heavy sites")


class BrandProfileData(BaseModel):
    """Generated brand profile data."""

    brand_name: str
    overview: str
    products_services: List[str] = Field(default_factory=list)
    mission: str = ""
    tone_voice: str = ""
    target_audience: str = ""
    brand_values: List[str] = Field(default_factory=list)
    frequently_used_hashtags: List[str] = Field(default_factory=list)
    content_style_summary: str = ""
    posting_frequency: str = ""
    recommended_content_strategy: str = ""
    source_urls: Optional[dict] = None
    _metadata: Optional[dict] = None


class AutoProfileResponse(BaseModel):
    """Response schema for auto brand profile generation."""

    success: bool
    message: str
    data: Optional[BrandProfileData] = None
    metadata: Optional[dict] = None
