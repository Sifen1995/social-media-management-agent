"""
FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.router import api_router
from app.db.session import init_db
from app.agents.base.orchestrator import orchestrator

# Import agents to register them
from app.agents.planner.agent import PlannerAgent
from app.agents.content.agent import ContentAgent
from app.agents.analytics.agent import AnalyticsAgent
from app.agents.scheduler.agent import SchedulerAgent
from app.agents.engagement.agent import EngagementAgent
from app.agents.social_listening.agent import SocialListeningAgent
from app.agents.optimizer.agent import OptimizerAgent

import logging

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """
    Initialize application on startup.
    """
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")

    # Initialize database (create tables if they don't exist)
    logger.info("Initializing database...")
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")

    # Register agents with orchestrator
    logger.info("Registering agents...")
    orchestrator.register_agent(PlannerAgent())
    orchestrator.register_agent(ContentAgent())
    orchestrator.register_agent(AnalyticsAgent())
    orchestrator.register_agent(SchedulerAgent())
    orchestrator.register_agent(EngagementAgent())
    orchestrator.register_agent(SocialListeningAgent())
    orchestrator.register_agent(OptimizerAgent())

    agents = orchestrator.list_agents()
    logger.info(f"Registered {len(agents)} agents: {[a['name'] for a in agents]}")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Cleanup on application shutdown.
    """
    logger.info("Shutting down application...")


# Include API router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
