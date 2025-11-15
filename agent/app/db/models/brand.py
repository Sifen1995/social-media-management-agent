"""
Brand database model.
"""
from sqlalchemy import Column, String, Integer, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.db.base import BaseModel


class Brand(BaseModel):
    """
    Brand model - represents a social media brand/account managed by the user.
    """
    __tablename__ = "brands"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    niche = Column(String(255), nullable=True)
    brand_voice = Column(Text, nullable=True)  # Description of brand voice/tone
    target_audience = Column(Text, nullable=True)  # Description of target audience
    goals = Column(JSON, nullable=True)  # List of brand goals
    visual_style = Column(Text, nullable=True)  # Visual style guidelines

    # Additional metadata
    keywords = Column(JSON, nullable=True)  # Brand-related keywords
    competitors = Column(JSON, nullable=True)  # List of competitor accounts
    guidelines = Column(JSON, nullable=True)  # Content guidelines and restrictions

    # Relationships
    user = relationship("User", back_populates="brands")
    social_accounts = relationship("SocialAccount", back_populates="brand", cascade="all, delete-orphan")
    content_items = relationship("ContentItem", back_populates="brand", cascade="all, delete-orphan")
    calendar_items = relationship("CalendarItem", back_populates="brand", cascade="all, delete-orphan")
    engagement_items = relationship("EngagementItem", back_populates="brand", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="brand", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Brand(id={self.id}, name={self.name}, niche={self.niche})>"
