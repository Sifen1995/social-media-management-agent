"""
Social accounts API endpoints for connecting and managing platform accounts.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies.auth import get_current_active_user, require_brand_access
from app.db.session import get_db
from app.db.models.user import User
from app.db.models.social_account import SocialAccount
from app.db.models.brand import Brand
from app.schemas.social_account import (
    SocialAccountCreate,
    SocialAccountUpdate,
    SocialAccountResponse,
    SocialAccountConnect,
)
from app.utils.encryption import encrypt_token, decrypt_token
from datetime import datetime

router = APIRouter()


@router.post("/", response_model=SocialAccountResponse, status_code=status.HTTP_201_CREATED)
async def create_social_account(
    account: SocialAccountCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Create a new social account connection.

    - **brand_id**: ID of the brand to connect this account to
    - **platform**: Platform name (instagram, facebook, twitter, etc.)
    - **access_token**: Platform access token (will be encrypted)
    - **refresh_token**: Optional refresh token
    - **account_name**: Display name for the account
    - **account_id**: Platform-specific account ID
    """
    # Verify brand access
    require_brand_access(current_user, account.brand_id, db)

    # Check if account already exists for this brand/platform
    existing = (
        db.query(SocialAccount)
        .filter(
            SocialAccount.brand_id == account.brand_id,
            SocialAccount.platform == account.platform,
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Social account for {account.platform} already exists for this brand",
        )

    # Encrypt tokens before storing
    encrypted_access_token = encrypt_token(account.access_token)
    encrypted_refresh_token = (
        encrypt_token(account.refresh_token) if account.refresh_token else None
    )

    # Create social account
    db_account = SocialAccount(
        brand_id=account.brand_id,
        platform=account.platform,
        account_name=account.account_name,
        account_id=account.account_id,
        access_token=encrypted_access_token,
        refresh_token=encrypted_refresh_token,
        token_expires_at=account.token_expires_at,
    )

    db.add(db_account)
    db.commit()
    db.refresh(db_account)

    return db_account


@router.get("/{account_id}", response_model=SocialAccountResponse)
async def get_social_account(
    account_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Get a specific social account by ID."""
    account = db.query(SocialAccount).filter(SocialAccount.id == account_id).first()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Social account not found",
        )

    # Verify user has access to this brand
    require_brand_access(current_user, account.brand_id, db)

    return account


@router.get("/brand/{brand_id}", response_model=List[SocialAccountResponse])
async def list_brand_social_accounts(
    brand_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """List all social accounts for a brand."""
    # Verify brand access
    require_brand_access(current_user, brand_id, db)

    accounts = (
        db.query(SocialAccount)
        .filter(SocialAccount.brand_id == brand_id)
        .all()
    )

    return accounts


@router.put("/{account_id}", response_model=SocialAccountResponse)
async def update_social_account(
    account_id: int,
    account_update: SocialAccountUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Update a social account."""
    account = db.query(SocialAccount).filter(SocialAccount.id == account_id).first()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Social account not found",
        )

    # Verify user has access to this brand
    require_brand_access(current_user, account.brand_id, db)

    # Update fields
    if account_update.account_name is not None:
        account.account_name = account_update.account_name

    if account_update.account_id is not None:
        account.account_id = account_update.account_id

    if account_update.access_token is not None:
        account.access_token = encrypt_token(account_update.access_token)

    if account_update.refresh_token is not None:
        account.refresh_token = encrypt_token(account_update.refresh_token)

    if account_update.token_expires_at is not None:
        account.token_expires_at = account_update.token_expires_at

    account.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(account)

    return account


@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_social_account(
    account_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Delete a social account connection."""
    account = db.query(SocialAccount).filter(SocialAccount.id == account_id).first()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Social account not found",
        )

    # Verify user has access to this brand
    require_brand_access(current_user, account.brand_id, db)

    db.delete(account)
    db.commit()

    return None


@router.post("/connect", response_model=SocialAccountResponse, status_code=status.HTTP_201_CREATED)
async def connect_social_account(
    connection: SocialAccountConnect,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Connect a social account via OAuth callback.

    This endpoint handles the OAuth callback after user authorizes the app.

    - **brand_id**: ID of the brand to connect
    - **platform**: Platform name
    - **code**: OAuth authorization code
    - **redirect_uri**: OAuth redirect URI (optional)
    """
    # Verify brand access
    require_brand_access(current_user, connection.brand_id, db)

    # In a real implementation, this would:
    # 1. Exchange the authorization code for access token
    # 2. Get account information from the platform
    # 3. Store the encrypted tokens

    # For now, return error indicating OAuth exchange needs to be implemented
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="OAuth token exchange not yet implemented. Use direct token creation endpoint instead.",
    )


@router.get("/{account_id}/refresh", response_model=SocialAccountResponse)
async def refresh_social_account_token(
    account_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Refresh an expired access token using the refresh token.

    This endpoint attempts to refresh the access token for a social account.
    """
    account = db.query(SocialAccount).filter(SocialAccount.id == account_id).first()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Social account not found",
        )

    # Verify user has access to this brand
    require_brand_access(current_user, account.brand_id, db)

    if not account.refresh_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No refresh token available for this account",
        )

    # In a real implementation, this would:
    # 1. Decrypt the refresh token
    # 2. Call the platform's token refresh endpoint
    # 3. Update the access token and expiry

    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Token refresh not yet implemented for this platform",
    )
