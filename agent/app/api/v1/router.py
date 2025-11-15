"""
API v1 router - aggregates all v1 endpoints.
"""
from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth,
    brands,
    content,
    analytics,
    scheduler,
    engagement,
    tasks,
    social_accounts
)

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(brands.router, prefix="/brands", tags=["Brands"])
api_router.include_router(content.router, prefix="/content", tags=["Content"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
api_router.include_router(scheduler.router, prefix="/scheduler", tags=["Scheduler"])
api_router.include_router(engagement.router, prefix="/engagement", tags=["Engagement"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
api_router.include_router(social_accounts.router, prefix="/social-accounts", tags=["Social Accounts"])
