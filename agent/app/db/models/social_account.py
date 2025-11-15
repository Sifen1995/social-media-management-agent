"""
Social Account database model.
"""
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
import enum


class PlatformType(enum.Enum):
    """Supported social media platforms."""
    INSTAGRAM = "instagram"
    FACEBOOK = "facebook"
    TIKTOK = "tiktok"
    TWITTER = "twitter"
    YOUTUBE = "youtube"
    LINKEDIN = "linkedin"


class SocialAccount(BaseModel):
    """
    Social Account model - stores connected social media accounts and their credentials.
    """
    __tablename__ = "social_accounts"

    brand_id = Column(Integer, ForeignKey("brands.id", ondelete="CASCADE"), nullable=False)
    platform = Column(Enum(PlatformType), nullable=False)
    account_username = Column(String(255), nullable=False)
    account_id = Column(String(255), nullable=True)  # Platform-specific account ID

    # Encrypted tokens (will be encrypted before storage)
    access_token = Column(Text, nullable=True)
    refresh_token = Column(Text, nullable=True)
    token_expires_at = Column(DateTime, nullable=True)

    # Account status
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

    # Metadata
    connected_at = Column(DateTime, nullable=True)
    last_sync_at = Column(DateTime, nullable=True)

    # Relationships
    brand = relationship("Brand", back_populates="social_accounts")

    def __repr__(self):
        return f"<SocialAccount(id={self.id}, platform={self.platform.value}, username={self.account_username})>"
