"""
Content database model.
"""
from sqlalchemy import Column, String, Integer, ForeignKey, Text, DateTime, JSON, Enum
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
import enum


class ContentType(enum.Enum):
    """Content types across platforms."""
    POST = "post"
    REEL = "reel"
    STORY = "story"
    TWEET = "tweet"
    THREAD = "thread"
    VIDEO = "video"
    SHORT = "short"
    ARTICLE = "article"
    CAROUSEL = "carousel"


class ContentStatus(enum.Enum):
    """Content workflow status."""
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    FAILED = "failed"
    ARCHIVED = "archived"


class ContentItem(BaseModel):
    """
    Content Item model - stores all content created and managed by the system.
    """
    __tablename__ = "content_items"

    brand_id = Column(Integer, ForeignKey("brands.id", ondelete="CASCADE"), nullable=False)
    platform = Column(String(50), nullable=False)  # instagram, facebook, etc.
    content_type = Column(Enum(ContentType), nullable=False)

    # Content data
    caption = Column(Text, nullable=True)
    hashtags = Column(JSON, nullable=True)  # List of hashtags
    media_urls = Column(JSON, nullable=True)  # List of media URLs
    additional_data = Column(JSON, nullable=True)  # Platform-specific data

    # Metadata
    title = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    cta = Column(String(255), nullable=True)  # Call to action

    # Status and scheduling
    status = Column(Enum(ContentStatus), default=ContentStatus.DRAFT, nullable=False)
    scheduled_for = Column(DateTime, nullable=True)
    published_at = Column(DateTime, nullable=True)

    # Platform-specific IDs
    platform_post_id = Column(String(255), nullable=True)
    permalink = Column(String(1000), nullable=True)

    # AI metadata
    created_by_agent = Column(String(100), nullable=True)  # Which agent created this
    generation_params = Column(JSON, nullable=True)  # Parameters used for generation
    variations = Column(JSON, nullable=True)  # Alternative versions

    # Error tracking
    error_message = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0, nullable=False)

    # Relationships
    brand = relationship("Brand", back_populates="content_items")
    analytics = relationship("AnalyticsData", back_populates="content_item", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ContentItem(id={self.id}, platform={self.platform}, status={self.status.value})>"
