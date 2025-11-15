"""
Celery configuration for background tasks.
"""
from celery import Celery
from app.core.config import settings

# Create Celery app
celery_app = Celery(
    "social_media_agent",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["celery_app.tasks"]
)

# Configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
)

# Optional: Configure periodic tasks
celery_app.conf.beat_schedule = {
    "fetch-scheduled-posts-every-minute": {
        "task": "celery_app.tasks.publish_scheduled_content",
        "schedule": 60.0,  # Every 60 seconds
    },
    "fetch-analytics-daily": {
        "task": "celery_app.tasks.fetch_daily_analytics",
        "schedule": 86400.0,  # Every 24 hours
    },
}
