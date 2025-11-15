"""
Authentication dependencies for API endpoints.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from typing import Optional

from app.core.config import settings
from app.core.security import verify_token
from app.db.session import get_db
from app.db.models.user import User

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    """
    Get current authenticated user from JWT token.

    Args:
        token: JWT access token
        db: Database session

    Returns:
        User object

    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Verify and decode token
        payload = verify_token(token)
        if payload is None:
            raise credentials_exception

        user_id: Optional[int] = payload.get("sub")
        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    # Get user from database
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Get current active user (can be extended with is_active check).

    Args:
        current_user: Current authenticated user

    Returns:
        User object

    Raises:
        HTTPException: If user is inactive
    """
    # If you add an is_active field to User model, check it here
    # if not current_user.is_active:
    #     raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_optional_user(
    token: Optional[str] = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Get current user if token is provided, otherwise return None.
    Useful for endpoints that work both authenticated and unauthenticated.

    Args:
        token: JWT access token (optional)
        db: Database session

    Returns:
        User object or None
    """
    if token is None:
        return None

    try:
        payload = verify_token(token)
        if payload is None:
            return None

        user_id: Optional[int] = payload.get("sub")
        if user_id is None:
            return None

        user = db.query(User).filter(User.id == int(user_id)).first()
        return user

    except Exception:
        return None


def require_brand_access(user: User, brand_id: int, db: Session) -> bool:
    """
    Check if user has access to a specific brand.

    Args:
        user: Current user
        brand_id: Brand ID to check access for
        db: Database session

    Returns:
        True if user has access

    Raises:
        HTTPException: If user doesn't have access
    """
    from app.db.models.brand import Brand

    brand = db.query(Brand).filter(Brand.id == brand_id).first()

    if not brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found"
        )

    if brand.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this brand",
        )

    return True


def require_content_access(user: User, content_id: int, db: Session) -> bool:
    """
    Check if user has access to a specific content item.

    Args:
        user: Current user
        content_id: Content ID to check access for
        db: Database session

    Returns:
        True if user has access

    Raises:
        HTTPException: If user doesn't have access
    """
    from app.db.models.content import ContentItem
    from app.db.models.brand import Brand

    content = db.query(ContentItem).filter(ContentItem.id == content_id).first()

    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Content not found"
        )

    # Check if user owns the brand that owns this content
    brand = db.query(Brand).filter(Brand.id == content.brand_id).first()
    if not brand or brand.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this content",
        )

    return True
