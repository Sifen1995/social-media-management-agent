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
    AutoProfileRequest,
    AutoProfileResponse,
    BrandProfileData,
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


@router.post("/auto_profile", response_model=AutoProfileResponse)
async def auto_generate_brand_profile(
    request: AutoProfileRequest,
    current_user: User = Depends(get_current_active_user),
):
    """
    Automatically generate a brand profile by scraping website and social media.

    This endpoint uses web scraping and AI analysis to automatically research
    a brand and generate a comprehensive profile.

    - **website**: Website URL to scrape (required)
    - **socials**: Social media profile URLs (optional)
      - instagram: Instagram profile URL
      - linkedin: LinkedIn company page URL
      - twitter: Twitter/X profile URL
      - tiktok: TikTok profile URL
      - facebook: Facebook page URL
    - **use_playwright**: Use Playwright for JavaScript-heavy sites (optional, default: false)

    Returns:
    - Structured brand profile with brand name, overview, tone of voice, target audience, etc.
    - Source URLs used for research
    - Data quality metadata

    Example request:
    ```json
    {
      "website": "https://example.com",
      "socials": {
        "instagram": "https://instagram.com/example",
        "linkedin": "https://linkedin.com/company/example"
      },
      "use_playwright": false
    }
    ```
    """
    from app.agents.brand_profile.agent import BrandProfileAgent
    from app.services.llm_service import LLMService

    try:
        # Initialize agent
        llm_service = LLMService()
        agent = BrandProfileAgent(llm_service=llm_service)

        # Prepare task
        task = {
            "website": request.website,
            "socials": request.socials.dict() if request.socials else {},
            "use_playwright": request.use_playwright
        }

        # Execute brand profile research
        result = await agent.execute(task, context={})

        if not result.get("success"):
            return AutoProfileResponse(
                success=False,
                message=result.get("message", "Brand profile generation failed"),
                data=None,
                metadata=result.get("metadata")
            )

        # Convert result data to BrandProfileData
        profile_data = result.get("data", {})
        brand_profile = BrandProfileData(**profile_data)

        return AutoProfileResponse(
            success=True,
            message=result.get("message", "Brand profile generated successfully"),
            data=brand_profile,
            metadata=result.get("metadata")
        )

    except Exception as e:
        import logging
        logging.error(f"Error in auto_generate_brand_profile: {str(e)}", exc_info=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate brand profile: {str(e)}"
        )
