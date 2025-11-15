"""Analytics Pydantic schemas."""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class AnalyticsDataResponse(BaseModel):
    """Schema for analytics data response."""

    id: int
    content_id: int
    platform: str
    likes: int = 0
    comments: int = 0
    shares: int = 0
    saves: int = 0
    reach: int = 0
    impressions: int = 0
    engagement_rate: float = 0.0
    metadata: Optional[Dict[str, Any]] = None
    fetched_at: datetime

    class Config:
        from_attributes = True


class AnalyticsReportRequest(BaseModel):
    """Schema for analytics report request."""

    brand_id: int
    time_period: str = "last_30_days"  # last_7_days, last_30_days, last_90_days, this_month, last_month
    platforms: Optional[List[str]] = None


class AnalyticsReportResponse(BaseModel):
    """Schema for analytics report response."""

    brand_id: int
    time_period: str
    start_date: datetime
    end_date: datetime
    total_posts: int
    total_likes: int
    total_comments: int
    total_shares: int
    total_reach: int
    avg_engagement_rate: float
    top_performing_content: List[Dict[str, Any]]
    insights: List[str]
    platform_breakdown: Dict[str, Dict[str, Any]]


class TopContentRequest(BaseModel):
    """Schema for top content request."""

    brand_id: int
    limit: int = 10
    metric: str = "engagement_rate"  # likes, comments, shares, reach, engagement_rate
    time_period: str = "last_30_days"


class InsightsRequest(BaseModel):
    """Schema for insights request."""

    brand_id: int
    time_period: str = "last_30_days"


class TrendAnalysisRequest(BaseModel):
    """Schema for trend analysis request."""

    brand_id: int
    keywords: Optional[List[str]] = None
    competitors: Optional[List[str]] = None
