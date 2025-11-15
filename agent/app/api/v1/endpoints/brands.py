"""Brand management endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.api.dependencies.auth import get_current_active_user, require_brand_access
from app.db.session import get_db
from app.db.models.user import User
from app.db.models.brand import Brand
from app.db.models.content import ContentItem
from app.db.models.social_account import SocialAccount
from app.schemas.brand import (
    BrandCreate,
    BrandUpdate,
    BrandResponse,
    BrandWithStats,
)

router = APIRouter()


@router.post("/", response_model=BrandResponse, status_code=status.HTTP_201_CREATED)
async def create_brand(
    brand_data: BrandCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Create a new brand.

    - **name**: Brand name (required)
    - **niche**: Brand niche or industry
    - **brand_voice**: Brand voice description
    - **target_audience**: Target audience description
    - **goals**: List of brand goals
    """
    # Create brand for current user
    brand = Brand(
        user_id=current_user.id,
        name=brand_data.name,
        niche=brand_data.niche,
        brand_voice=brand_data.brand_voice,
        target_audience=brand_data.target_audience,
        goals=brand_data.goals or [],
    )

    db.add(brand)
    db.commit()
    db.refresh(brand)

    return brand


@router.get("/", response_model=List[BrandResponse])
async def list_brands(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    List all brands for the current user.

    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    """
    brands = (
        db.query(Brand)
        .filter(Brand.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    return brands


@router.get("/{brand_id}", response_model=BrandResponse)
async def get_brand(
    brand_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Get brand details by ID."""
    brand = db.query(Brand).filter(Brand.id == brand_id).first()

    if not brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand not found",
        )

    # Verify user has access to this brand
    require_brand_access(current_user, brand_id, db)

    return brand


@router.get("/{brand_id}/stats", response_model=BrandWithStats)
async def get_brand_stats(
    brand_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Get brand details with statistics."""
    brand = db.query(Brand).filter(Brand.id == brand_id).first()

    if not brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand not found",
        )

    # Verify user has access to this brand
    require_brand_access(current_user, brand_id, db)

    # Get statistics
    total_content = db.query(ContentItem).filter(ContentItem.brand_id == brand_id).count()
    total_posts = (
        db.query(ContentItem)
        .filter(ContentItem.brand_id == brand_id, ContentItem.status == "published")
        .count()
    )
    total_accounts = db.query(SocialAccount).filter(SocialAccount.brand_id == brand_id).count()

    # Convert to BrandWithStats
    brand_dict = {
        "id": brand.id,
        "user_id": brand.user_id,
        "name": brand.name,
        "niche": brand.niche,
        "brand_voice": brand.brand_voice,
        "target_audience": brand.target_audience,
        "goals": brand.goals,
        "created_at": brand.created_at,
        "updated_at": brand.updated_at,
        "total_content": total_content,
        "total_posts": total_posts,
        "total_accounts": total_accounts,
    }

    return brand_dict


@router.put("/{brand_id}", response_model=BrandResponse)
async def update_brand(
    brand_id: int,
    brand_update: BrandUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Update a brand.

    Only the provided fields will be updated.
    """
    brand = db.query(Brand).filter(Brand.id == brand_id).first()

    if not brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand not found",
        )

    # Verify user has access to this brand
    require_brand_access(current_user, brand_id, db)

    # Update fields
    update_data = brand_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(brand, field, value)

    brand.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(brand)

    return brand


@router.delete("/{brand_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_brand(
    brand_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Delete a brand.

    This will also delete all associated content and social accounts.
    """
    brand = db.query(Brand).filter(Brand.id == brand_id).first()

    if not brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand not found",
        )

    # Verify user has access to this brand
    require_brand_access(current_user, brand_id, db)

    # Delete associated content
    db.query(ContentItem).filter(ContentItem.brand_id == brand_id).delete()

    # Delete associated social accounts
    db.query(SocialAccount).filter(SocialAccount.brand_id == brand_id).delete()

    # Delete the brand
    db.delete(brand)
    db.commit()

    return None
