"""Social Account Pydantic schemas."""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class SocialAccountBase(BaseModel):
    """Base social account schema."""

    platform: str = Field(..., min_length=1)
    account_name: Optional[str] = None
    account_id: Optional[str] = None


class SocialAccountCreate(BaseModel):
    """Schema for creating a social account."""

    brand_id: int
    platform: str
    account_name: Optional[str] = None
    account_id: Optional[str] = None
    access_token: str = Field(..., min_length=1)
    refresh_token: Optional[str] = None
    token_expires_at: Optional[datetime] = None


class SocialAccountUpdate(BaseModel):
    """Schema for updating a social account."""

    account_name: Optional[str] = None
    account_id: Optional[str] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_expires_at: Optional[datetime] = None


class SocialAccountResponse(BaseModel):
    """Schema for social account response (without tokens)."""

    id: int
    brand_id: int
    platform: str
    account_name: Optional[str] = None
    account_id: Optional[str] = None
    token_expires_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SocialAccountConnect(BaseModel):
    """Schema for connecting a social account (OAuth callback)."""

    brand_id: int
    platform: str
    code: str  # OAuth authorization code
    redirect_uri: Optional[str] = None
