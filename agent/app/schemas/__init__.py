"""Pydantic schemas for API request/response validation."""

# User schemas
from .user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponse,
    UserLogin,
    Token,
    TokenData,
)

# Brand schemas
from .brand import (
    BrandBase,
    BrandCreate,
    BrandUpdate,
    BrandResponse,
    BrandWithStats,
)

# Content schemas
from .content import (
    ContentStatus,
    ContentType,
    Platform,
    ContentBase,
    ContentCreate,
    ContentUpdate,
    ContentResponse,
    ContentGenerateRequest,
    ContentPlanRequest,
    ContentWithAnalytics,
)

# Social Account schemas
from .social_account import (
    SocialAccountBase,
    SocialAccountCreate,
    SocialAccountUpdate,
    SocialAccountResponse,
    SocialAccountConnect,
)

# Analytics schemas
from .analytics import (
    AnalyticsDataResponse,
    AnalyticsReportRequest,
    AnalyticsReportResponse,
    TopContentRequest,
    InsightsRequest,
    TrendAnalysisRequest,
)

# Calendar schemas
from .calendar import (
    CalendarItemBase,
    CalendarItemCreate,
    CalendarItemUpdate,
    CalendarItemResponse,
    CalendarCreateRequest,
)

# Engagement schemas
from .engagement import (
    EngagementItemResponse,
    EngagementReplyRequest,
    EngagementReplyResponse,
    EngagementFilterRequest,
    EngagementPrioritizeRequest,
)

# Task schemas
from .task import (
    TaskResponse,
    TaskCreate,
    AgentInfo,
    AgentListResponse,
)

__all__ = [
    # User
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserLogin",
    "Token",
    "TokenData",
    # Brand
    "BrandBase",
    "BrandCreate",
    "BrandUpdate",
    "BrandResponse",
    "BrandWithStats",
    # Content
    "ContentStatus",
    "ContentType",
    "Platform",
    "ContentBase",
    "ContentCreate",
    "ContentUpdate",
    "ContentResponse",
    "ContentGenerateRequest",
    "ContentPlanRequest",
    "ContentWithAnalytics",
    # Social Account
    "SocialAccountBase",
    "SocialAccountCreate",
    "SocialAccountUpdate",
    "SocialAccountResponse",
    "SocialAccountConnect",
    # Analytics
    "AnalyticsDataResponse",
    "AnalyticsReportRequest",
    "AnalyticsReportResponse",
    "TopContentRequest",
    "InsightsRequest",
    "TrendAnalysisRequest",
    # Calendar
    "CalendarItemBase",
    "CalendarItemCreate",
    "CalendarItemUpdate",
    "CalendarItemResponse",
    "CalendarCreateRequest",
    # Engagement
    "EngagementItemResponse",
    "EngagementReplyRequest",
    "EngagementReplyResponse",
    "EngagementFilterRequest",
    "EngagementPrioritizeRequest",
    # Task
    "TaskResponse",
    "TaskCreate",
    "AgentInfo",
    "AgentListResponse",
]
