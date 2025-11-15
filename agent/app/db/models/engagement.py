"""
Engagement database model.
"""
from sqlalchemy import Column, String, Integer, ForeignKey, Text, Enum, DateTime
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
import enum


class EngagementType(enum.Enum):
    """Types of engagement interactions."""
    COMMENT = "comment"
    DM = "dm"
    MENTION = "mention"
    TAG = "tag"
    REPLY = "reply"


class EngagementStatus(enum.Enum):
    """Status of engagement items."""
    PENDING = "pending"
    REVIEWED = "reviewed"
    APPROVED = "approved"
    SENT = "sent"
    IGNORED = "ignored"
    SPAM = "spam"


class EngagementItem(BaseModel):
    """
    Engagement Item model - stores community interactions that need responses.
    """
    __tablename__ = "engagement_queue"

    brand_id = Column(Integer, ForeignKey("brands.id", ondelete="CASCADE"), nullable=False)
    platform = Column(String(50), nullable=False)
    engagement_type = Column(Enum(EngagementType), nullable=False)

    # Source information
    source_id = Column(String(255), nullable=False)  # Platform-specific ID
    source_username = Column(String(255), nullable=True)
    source_url = Column(String(1000), nullable=True)

    # Content
    content = Column(Text, nullable=True)
    context = Column(Text, nullable=True)  # Additional context (parent comment, etc.)

    # AI-generated response
    suggested_reply = Column(Text, nullable=True)
    reply_variations = Column(Text, nullable=True)  # JSON array of alternative replies

    # Status and workflow
    status = Column(Enum(EngagementStatus), default=EngagementStatus.PENDING, nullable=False)
    processed_by_agent = Column(String(100), nullable=True)

    # Sentiment analysis
    sentiment_score = Column(String(50), nullable=True)  # positive, negative, neutral
    is_spam = Column(String(50), default="unknown", nullable=False)  # yes, no, unknown
    priority = Column(String(50), default="medium", nullable=False)  # high, medium, low

    # Response tracking
    responded_at = Column(DateTime, nullable=True)
    response_sent = Column(Text, nullable=True)

    # Relationships
    brand = relationship("Brand", back_populates="engagement_items")

    def __repr__(self):
        return f"<EngagementItem(id={self.id}, type={self.engagement_type.value}, status={self.status.value})>"
