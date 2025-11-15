"""
Content generation and management endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.db.models import ContentItem, Brand
from app.agents.base.orchestrator import orchestrator
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


# Request/Response Schemas
class ContentGenerationRequest(BaseModel):
    """Request to generate content."""
    brand_id: int
    platform: str
    topic: str
    content_type: str = "post"
    count: int = 3
    requirements: str = ""


class ContentResponse(BaseModel):
    """Content item response."""
    id: int
    platform: str
    content_type: str
    caption: str
    hashtags: list
    status: str

    class Config:
        from_attributes = True


class AgentTaskRequest(BaseModel):
    """Generic agent task request."""
    brand_id: int
    user_request: str


@router.post("/generate")
async def generate_content(
    request: ContentGenerationRequest,
    db: Session = Depends(get_db)
):
    """
    Generate social media content using the Content Agent.

    This endpoint demonstrates the complete workflow:
    1. Fetch brand context from database
    2. Prepare task for Content Agent
    3. Execute agent
    4. Save generated content to database
    5. Return results
    """
    try:
        # Fetch brand information
        brand = db.query(Brand).filter(Brand.id == request.brand_id).first()

        if not brand:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Brand with id {request.brand_id} not found"
            )

        # Prepare context for agent
        context = {
            "brand": {
                "id": brand.id,
                "name": brand.name,
                "niche": brand.niche,
                "brand_voice": brand.brand_voice,
                "target_audience": brand.target_audience,
                "goals": brand.goals
            }
        }

        # Prepare task for Content Agent
        task = {
            "platform": request.platform,
            "action": "generate",
            "topic": request.topic,
            "content_type": request.content_type,
            "count": request.count,
            "requirements": request.requirements
        }

        # Execute Content Agent
        result = await orchestrator.execute_task("content", task, context)

        if not result.get("success"):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get("message", "Content generation failed")
            )

        # Save generated content to database
        generated_items = result.get("data", [])
        saved_items = []

        for item in generated_items:
            content_item = ContentItem(
                brand_id=brand.id,
                platform=request.platform,
                content_type=request.content_type,
                caption=item.get("caption", ""),
                hashtags=item.get("hashtags", []),
                cta=item.get("cta", ""),
                status="draft",
                created_by_agent="content"
            )
            db.add(content_item)
            saved_items.append(content_item)

        db.commit()

        # Refresh to get IDs
        for item in saved_items:
            db.refresh(item)

        logger.info(f"Generated and saved {len(saved_items)} content items for brand {brand.id}")

        return {
            "success": True,
            "message": f"Generated {len(saved_items)} content variations",
            "data": {
                "content_items": [
                    {
                        "id": item.id,
                        "caption": item.caption,
                        "hashtags": item.hashtags,
                        "cta": item.cta,
                        "platform": item.platform
                    }
                    for item in saved_items
                ]
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Content generation error: {e}", exc_info=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )


@router.post("/plan-and-execute")
async def plan_and_execute(
    request: AgentTaskRequest,
    db: Session = Depends(get_db)
):
    """
    Use Planner Agent to decompose and execute complex requests.

    This demonstrates the multi-agent workflow:
    1. User submits natural language request
    2. Planner Agent analyzes and creates execution plan
    3. Orchestrator executes plan using specialized agents
    4. Results are aggregated and returned
    """
    try:
        # Fetch brand
        brand = db.query(Brand).filter(Brand.id == request.brand_id).first()

        if not brand:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Brand with id {request.brand_id} not found"
            )

        # Prepare context
        context = {
            "brand": {
                "id": brand.id,
                "name": brand.name,
                "niche": brand.niche,
                "brand_voice": brand.brand_voice,
                "target_audience": brand.target_audience,
                "goals": brand.goals
            }
        }

        # Delegate to Planner Agent
        plan_result = await orchestrator.delegate_to_planner(
            request.user_request,
            context
        )

        if not plan_result.get("success"):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Planning failed"
            )

        plan = plan_result.get("data", {})
        execution_plan = plan.get("execution_plan", [])

        # Execute the plan
        workflow_results = await orchestrator.execute_workflow(execution_plan, context)

        return {
            "success": True,
            "message": "Request processed successfully",
            "data": {
                "plan": plan,
                "execution_results": workflow_results
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Plan-and-execute error: {e}", exc_info=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )


@router.get("/{content_id}", response_model=ContentResponse)
async def get_content(content_id: int, db: Session = Depends(get_db)):
    """Get a specific content item."""
    content = db.query(ContentItem).filter(ContentItem.id == content_id).first()

    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Content with id {content_id} not found"
        )

    return content


@router.get("/", response_model=List[ContentResponse])
async def list_content(
    brand_id: int,
    platform: str = None,
    status: str = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """List content items with optional filters."""
    query = db.query(ContentItem).filter(ContentItem.brand_id == brand_id)

    if platform:
        query = query.filter(ContentItem.platform == platform)

    if status:
        query = query.filter(ContentItem.status == status)

    content_items = query.order_by(ContentItem.created_at.desc()).limit(limit).all()

    return content_items
