"""
Analytics database model.
"""
from sqlalchemy import Column, String, Integer, ForeignKey, Float, DateTime, JSON
from sqlalchemy.orm import relationship
from app.db.base import BaseModel


class AnalyticsData(BaseModel):
    """
    Analytics Data model - stores performance metrics for content.
    """
    __tablename__ = "analytics_data"

    content_item_id = Column(Integer, ForeignKey("content_items.id", ondelete="CASCADE"), nullable=False)
    platform = Column(String(50), nullable=False)

    # Engagement metrics
    likes = Column(Integer, default=0, nullable=False)
    comments = Column(Integer, default=0, nullable=False)
    shares = Column(Integer, default=0, nullable=False)
    saves = Column(Integer, default=0, nullable=False)
    views = Column(Integer, default=0, nullable=False)

    # Reach and impressions
    reach = Column(Integer, default=0, nullable=False)
    impressions = Column(Integer, default=0, nullable=False)

    # Calculated metrics
    engagement_rate = Column(Float, default=0.0, nullable=False)
    click_through_rate = Column(Float, default=0.0, nullable=False)

    # Time-based metrics
    avg_watch_time = Column(Integer, nullable=True)  # In seconds
    completion_rate = Column(Float, nullable=True)  # For videos

    # Audience metrics
    audience_demographics = Column(JSON, nullable=True)
    audience_locations = Column(JSON, nullable=True)
    audience_age_ranges = Column(JSON, nullable=True)

    # Platform-specific metrics
    platform_specific_data = Column(JSON, nullable=True)

    # Tracking
    fetched_at = Column(DateTime, nullable=False)
    fetch_source = Column(String(100), nullable=True)  # API, manual, etc.

    # Relationships
    content_item = relationship("ContentItem", back_populates="analytics")

    def __repr__(self):
        return f"<AnalyticsData(id={self.id}, content_id={self.content_item_id}, engagement_rate={self.engagement_rate})>"
