"""
Celery background tasks.
"""
from celery_app.celery import celery_app
from app.db.session import SessionLocal
from app.db.models import ContentItem, SocialAccount, AnalyticsData
from app.integrations.instagram.client import InstagramClient
from app.integrations.twitter.client import TwitterClient
from app.utils.encryption import decrypt_token
from datetime import datetime
import logging
import asyncio

logger = logging.getLogger(__name__)


@celery_app.task(name="celery_app.tasks.publish_scheduled_content")
def publish_scheduled_content():
    """
    Background task to publish scheduled content.
    Runs every minute to check for content that needs to be published.
    """
    logger.info("Checking for scheduled content to publish...")

    db = SessionLocal()
    try:
        # Find content scheduled for now or earlier
        now = datetime.utcnow()
        scheduled_items = db.query(ContentItem).filter(
            ContentItem.status == "scheduled",
            ContentItem.scheduled_for <= now
        ).all()

        logger.info(f"Found {len(scheduled_items)} items to publish")

        for item in scheduled_items:
            try:
                # Get social account credentials
                social_account = db.query(SocialAccount).filter(
                    SocialAccount.brand_id == item.brand_id,
                    SocialAccount.platform == item.platform,
                    SocialAccount.is_active == True
                ).first()

                if not social_account:
                    logger.error(f"No active social account found for {item.platform}")
                    item.status = "failed"
                    item.error_message = "No active social account"
                    continue

                # Decrypt access token
                access_token = decrypt_token(social_account.access_token)

                # Publish based on platform
                result = None
                if item.platform == "instagram":
                    client = InstagramClient(access_token, social_account.account_id)
                    # Run async method in sync context
                    result = asyncio.run(client.post_content(
                        content_type="photo" if item.media_url else "text",
                        caption=item.caption,
                        media_url=item.media_url
                    ))

                elif item.platform == "twitter":
                    client = TwitterClient(access_token, social_account.account_id)
                    result = asyncio.run(client.post_content(
                        content_type="tweet",
                        caption=item.caption,
                        media_url=item.media_url
                    ))

                # Update status
                if result and result.get("success"):
                    item.status = "published"
                    item.published_at = datetime.utcnow()
                    item.platform_post_id = result.get("post_id")
                    item.permalink = result.get("permalink")
                    logger.info(f"Published content item {item.id} to {item.platform}")
                else:
                    item.status = "failed"
                    item.error_message = "Publishing failed"
                    item.retry_count += 1

            except Exception as e:
                logger.error(f"Error publishing item {item.id}: {e}")
                item.status = "failed"
                item.error_message = str(e)
                item.retry_count += 1

        db.commit()

    except Exception as e:
        logger.error(f"Error in publish_scheduled_content task: {e}")
        db.rollback()
    finally:
        db.close()


@celery_app.task(name="celery_app.tasks.fetch_daily_analytics")
def fetch_daily_analytics():
    """
    Background task to fetch analytics for published content.
    Runs daily to update performance metrics.
    """
    logger.info("Fetching analytics for published content...")

    db = SessionLocal()
    try:
        # Get recently published content without recent analytics
        published_items = db.query(ContentItem).filter(
            ContentItem.status == "published",
            ContentItem.platform_post_id.isnot(None)
        ).limit(100).all()

        logger.info(f"Fetching analytics for {len(published_items)} items")

        for item in published_items:
            try:
                # Get social account
                social_account = db.query(SocialAccount).filter(
                    SocialAccount.brand_id == item.brand_id,
                    SocialAccount.platform == item.platform,
                    SocialAccount.is_active == True
                ).first()

                if not social_account:
                    continue

                # Decrypt access token
                access_token = decrypt_token(social_account.access_token)

                # Fetch analytics based on platform
                analytics_result = None
                if item.platform == "instagram":
                    client = InstagramClient(access_token, social_account.account_id)
                    analytics_result = asyncio.run(client.get_analytics(item.platform_post_id))

                elif item.platform == "twitter":
                    client = TwitterClient(access_token, social_account.account_id)
                    analytics_result = asyncio.run(client.get_analytics(item.platform_post_id))

                # Save analytics
                if analytics_result and not analytics_result.get("error"):
                    analytics = AnalyticsData(
                        content_item_id=item.id,
                        platform=item.platform,
                        likes=analytics_result.get("likes", 0),
                        comments=analytics_result.get("comments", 0),
                        shares=analytics_result.get("shares", 0),
                        saves=analytics_result.get("saves", 0),
                        views=analytics_result.get("views", 0),
                        reach=analytics_result.get("reach", 0),
                        impressions=analytics_result.get("impressions", 0),
                        fetched_at=datetime.utcnow()
                    )

                    # Calculate engagement rate
                    if analytics.reach > 0:
                        analytics.engagement_rate = (
                            (analytics.likes + analytics.comments + analytics.shares) /
                            analytics.reach * 100
                        )

                    db.add(analytics)
                    logger.info(f"Saved analytics for content {item.id}")

            except Exception as e:
                logger.error(f"Error fetching analytics for item {item.id}: {e}")

        db.commit()

    except Exception as e:
        logger.error(f"Error in fetch_daily_analytics task: {e}")
        db.rollback()
    finally:
        db.close()


@celery_app.task(name="celery_app.tasks.process_engagement_queue")
def process_engagement_queue():
    """
    Process pending engagement items (comments, DMs).
    Can be triggered manually or scheduled.
    """
    logger.info("Processing engagement queue...")
    # Implementation would fetch pending engagement items
    # and use Engagement Agent to generate responses
    pass
