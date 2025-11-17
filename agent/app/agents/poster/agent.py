"""
Posting Automation Agent - automates content posting across multiple social media platforms.
"""
import logging
from typing import Dict, Any, List, Optional
import json
import asyncio
from datetime import datetime
from app.agents.base.agent import BaseAgent
from app.agents.poster.prompts import POSTER_SYSTEM_PROMPT, POSTING_VALIDATION_PROMPT

logger = logging.getLogger(__name__)

# Lazy import platform clients to avoid dependency issues
def _import_platform_clients():
    """Import platform clients lazily to handle missing dependencies gracefully."""
    clients = {}

    try:
        from app.integrations.instagram.client import InstagramClient
        clients['instagram'] = InstagramClient
    except ImportError as e:
        logger.warning(f"Instagram client not available: {e}")

    try:
        from app.integrations.facebook.client import FacebookClient
        clients['facebook'] = FacebookClient
    except ImportError as e:
        logger.warning(f"Facebook client not available: {e}")

    try:
        from app.integrations.twitter.client import TwitterClient
        clients['twitter'] = TwitterClient
    except ImportError as e:
        logger.warning(f"Twitter client not available: {e}")

    try:
        from app.integrations.linkedin.client import LinkedInClient
        clients['linkedin'] = LinkedInClient
    except ImportError as e:
        logger.warning(f"LinkedIn client not available: {e}")

    try:
        from app.integrations.tiktok.client import TikTokClient
        clients['tiktok'] = TikTokClient
    except ImportError as e:
        logger.warning(f"TikTok client not available: {e}")

    try:
        from app.integrations.youtube.client import YouTubeClient
        clients['youtube'] = YouTubeClient
    except ImportError as e:
        logger.warning(f"YouTube client not available: {e}")

    return clients


class PosterAgent(BaseAgent):
    """
    Posting Automation Agent - manages multi-platform content posting.

    Capabilities:
    - Post to Instagram, Facebook, Twitter, LinkedIn, TikTok, YouTube
    - Validate content before posting
    - Handle retries and error recovery
    - Queue management
    - Scheduled posting (integrates with scheduler)
    - Status tracking and reporting
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._platform_clients = {}

    @property
    def name(self) -> str:
        return "poster"

    @property
    def description(self) -> str:
        return "Automates content posting across multiple social media platforms"

    def get_required_fields(self) -> list:
        return ["content", "platforms"]

    async def execute(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute posting automation.

        Args:
            task: Must contain 'content' and 'platforms', optional 'credentials'
            context: Execution context

        Returns:
            Posting results for all platforms
        """
        try:
            content = task.get("content")
            platforms = task.get("platforms", [])
            credentials = task.get("credentials", {})
            mode = task.get("mode", "post")  # post, schedule, validate
            schedule_time = task.get("schedule_time")

            if not content:
                return self.create_result(
                    success=False,
                    message="Content is required for posting"
                )

            if not platforms:
                return self.create_result(
                    success=False,
                    message="At least one platform is required"
                )

            logger.info(f"Posting automation for platforms: {platforms}, mode: {mode}")

            # Initialize platform clients with credentials
            self._init_platform_clients(credentials)

            if mode == "validate":
                result = await self._validate_content(content, platforms)
            elif mode == "schedule":
                result = await self._schedule_content(content, platforms, schedule_time, context)
            else:  # mode == "post"
                result = await self._post_content(content, platforms)

            return self.create_result(
                success=True,
                data=result,
                message=f"Posting automation completed for {len(platforms)} platforms",
                metadata={
                    "platforms": platforms,
                    "mode": mode
                }
            )

        except Exception as e:
            logger.error(f"Error in poster agent: {str(e)}", exc_info=e)
            return self.create_error_result(e, "Posting automation failed")

    def _init_platform_clients(self, credentials: Dict[str, Any]) -> None:
        """
        Initialize platform API clients with credentials.

        Args:
            credentials: Dict of platform credentials
        """
        # Get available platform clients
        platform_classes = _import_platform_clients()

        for platform, client_class in platform_classes.items():
            creds = credentials.get(platform, {})
            if creds:
                try:
                    access_token = creds.get("access_token")
                    if access_token:
                        self._platform_clients[platform] = client_class(access_token=access_token)
                        logger.info(f"Initialized {platform} client")
                except Exception as e:
                    logger.warning(f"Failed to initialize {platform} client: {str(e)}")

    async def _validate_content(
        self,
        content: Dict[str, Any],
        platforms: List[str]
    ) -> Dict[str, Any]:
        """
        Validate content for all platforms.

        Args:
            content: Content to validate
            platforms: Target platforms

        Returns:
            Validation results per platform
        """
        validation_results = {}

        for platform in platforms:
            requirements = self._get_platform_requirements(platform)

            prompt = POSTING_VALIDATION_PROMPT.format(
                platform=platform,
                content=json.dumps(content, indent=2),
                requirements=requirements
            )

            response = await self.llm_service.generate_completion(
                system_prompt=POSTER_SYSTEM_PROMPT,
                user_prompt=prompt,
                temperature=0.3,
                response_format="json"
            )

            try:
                validation = json.loads(response)
                validation_results[platform] = validation
            except json.JSONDecodeError:
                validation_results[platform] = {
                    "valid": True,
                    "errors": [],
                    "warnings": ["Could not perform automated validation"],
                    "suggestions": []
                }

        return {
            "validation_results": validation_results,
            "all_valid": all(v.get("valid", False) for v in validation_results.values())
        }

    async def _post_content(
        self,
        content: Dict[str, Any] | List[Dict[str, Any]],
        platforms: List[str]
    ) -> Dict[str, Any]:
        """
        Post content to multiple platforms.

        Args:
            content: Content to post (single or batch)
            platforms: Target platforms

        Returns:
            Posting results
        """
        # Handle batch posting
        if isinstance(content, list):
            return await self._batch_post(content, platforms)

        # Single content posting
        posting_results = {}

        for platform in platforms:
            if platform not in self._platform_clients:
                posting_results[platform] = {
                    "success": False,
                    "error": f"No credentials configured for {platform}",
                    "status": "credentials_missing"
                }
                continue

            try:
                client = self._platform_clients[platform]

                # Format content for platform
                formatted_content = self._format_content_for_platform(content, platform)

                # Post to platform with retry logic
                result = await self._post_with_retry(client, formatted_content, platform)

                posting_results[platform] = result

            except Exception as e:
                logger.error(f"Error posting to {platform}: {str(e)}")
                posting_results[platform] = {
                    "success": False,
                    "error": str(e),
                    "status": "error"
                }

        return {
            "posting_results": posting_results,
            "successful_platforms": [p for p, r in posting_results.items() if r.get("success")],
            "failed_platforms": [p for p, r in posting_results.items() if not r.get("success")],
            "posted_at": datetime.utcnow().isoformat() + "Z"
        }

    async def _batch_post(
        self,
        content_batch: List[Dict[str, Any]],
        platforms: List[str]
    ) -> Dict[str, Any]:
        """
        Post a batch of content items.

        Args:
            content_batch: List of content items
            platforms: Target platforms

        Returns:
            Batch posting results
        """
        batch_results = []

        for idx, content in enumerate(content_batch):
            logger.info(f"Posting item {idx + 1}/{len(content_batch)}")

            # Get platform from content or use provided platforms
            content_platform = content.get("platform")
            target_platforms = [content_platform] if content_platform else platforms

            result = await self._post_content(content, target_platforms)
            result["content_index"] = idx
            result["content_id"] = content.get("id", f"content_{idx}")

            batch_results.append(result)

            # Small delay between posts to avoid rate limiting
            await asyncio.sleep(2)

        return {
            "batch_results": batch_results,
            "total_items": len(content_batch),
            "successful_posts": sum(
                1 for r in batch_results
                if any(p.get("success") for p in r.get("posting_results", {}).values())
            )
        }

    async def _schedule_content(
        self,
        content: Dict[str, Any],
        platforms: List[str],
        schedule_time: Optional[str],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Schedule content for future posting.

        Args:
            content: Content to schedule
            platforms: Target platforms
            schedule_time: ISO format datetime string
            context: Execution context

        Returns:
            Scheduling results
        """
        # This is a placeholder for scheduling logic
        # In production, integrate with:
        # - Database to store scheduled posts
        # - Celery/Background task queue
        # - Cron jobs or scheduled tasks

        scheduled_items = []

        for platform in platforms:
            scheduled_items.append({
                "platform": platform,
                "content_id": content.get("id", "unknown"),
                "scheduled_for": schedule_time,
                "status": "scheduled",
                "created_at": datetime.utcnow().isoformat() + "Z"
            })

        logger.info(f"Scheduled {len(scheduled_items)} items for {schedule_time}")

        return {
            "scheduled_items": scheduled_items,
            "total_scheduled": len(scheduled_items),
            "schedule_time": schedule_time,
            "note": "Scheduling implementation requires background task queue (e.g., Celery)"
        }

    async def _post_with_retry(
        self,
        client: Any,
        content: Dict[str, Any],
        platform: str,
        max_retries: int = 3
    ) -> Dict[str, Any]:
        """
        Post content with retry logic.

        Args:
            client: Platform API client
            content: Formatted content
            platform: Platform name
            max_retries: Maximum retry attempts

        Returns:
            Posting result
        """
        last_error = None

        for attempt in range(max_retries):
            try:
                logger.info(f"Posting to {platform} (attempt {attempt + 1}/{max_retries})")

                result = await client.post_content(content)

                if result.get("success"):
                    logger.info(f"Successfully posted to {platform}")
                    return result

                last_error = result.get("error", "Unknown error")
                logger.warning(f"Post failed: {last_error}")

            except Exception as e:
                last_error = str(e)
                logger.error(f"Exception during post: {last_error}")

            # Wait before retry (exponential backoff)
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                logger.info(f"Retrying in {wait_time} seconds...")
                await asyncio.sleep(wait_time)

        return {
            "success": False,
            "error": f"Failed after {max_retries} attempts: {last_error}",
            "status": "failed"
        }

    def _format_content_for_platform(
        self,
        content: Dict[str, Any],
        platform: str
    ) -> Dict[str, Any]:
        """
        Format content for specific platform requirements.

        Args:
            content: Raw content
            platform: Target platform

        Returns:
            Platform-formatted content
        """
        formatted = content.copy()

        # Platform-specific formatting
        if platform == "instagram":
            # Instagram-specific formatting
            formatted["caption"] = self._truncate_text(
                content.get("caption", ""),
                2200
            )
            formatted["media_type"] = content.get("media_type", "IMAGE")

        elif platform == "twitter":
            # Twitter has 280 character limit
            formatted["text"] = self._truncate_text(
                content.get("caption", ""),
                280
            )

        elif platform == "linkedin":
            # LinkedIn formatting
            formatted["text"] = content.get("caption", "")
            formatted["visibility"] = content.get("visibility", "PUBLIC")

        elif platform == "facebook":
            # Facebook formatting
            formatted["message"] = content.get("caption", "")

        elif platform == "tiktok":
            # TikTok formatting
            formatted["desc"] = self._truncate_text(
                content.get("caption", ""),
                2200
            )

        elif platform == "youtube":
            # YouTube formatting
            formatted["snippet"] = {
                "title": content.get("title", ""),
                "description": content.get("caption", ""),
                "tags": content.get("tags", [])
            }

        return formatted

    def _truncate_text(self, text: str, max_length: int) -> str:
        """
        Truncate text to max length.

        Args:
            text: Text to truncate
            max_length: Maximum length

        Returns:
            Truncated text
        """
        if len(text) <= max_length:
            return text

        return text[:max_length - 3] + "..."

    def _get_platform_requirements(self, platform: str) -> str:
        """
        Get platform-specific requirements.

        Args:
            platform: Platform name

        Returns:
            Requirements string
        """
        requirements = {
            "instagram": "Max 2200 chars, 30 hashtags, image/video required",
            "facebook": "Max 63,206 chars, image/video optional",
            "twitter": "Max 280 chars (4000 with Twitter Blue), 4 images max",
            "linkedin": "Max 3000 chars for posts, 1300 for comments",
            "tiktok": "Max 2200 chars caption, video required (15s-10min)",
            "youtube": "Max 5000 chars description, video required"
        }

        return requirements.get(platform, "Check platform documentation for limits")
