"""
Instagram integration using Instagram Graph API.
"""
from typing import Dict, Any, List, Optional
from app.integrations.base import BasePlatformIntegration
import aiohttp
import logging

logger = logging.getLogger(__name__)


class InstagramClient(BasePlatformIntegration):
    """
    Instagram Graph API client for business/creator accounts.

    Uses Facebook Graph API to interact with Instagram.
    Requires: Instagram Business or Creator account linked to Facebook Page
    """

    BASE_URL = "https://graph.facebook.com/v18.0"

    @property
    def platform_name(self) -> str:
        return "instagram"

    async def verify_credentials(self) -> bool:
        """Verify access token and get account info."""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.BASE_URL}/me"
                params = {
                    "fields": "id,username",
                    "access_token": self.access_token
                }

                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.account_id = data.get("id")
                        self.logger.info(f"Instagram credentials verified for account: {data.get('username')}")
                        return True
                    else:
                        self.logger.error(f"Credential verification failed: {response.status}")
                        return False

        except Exception as e:
            self.logger.error(f"Error verifying credentials: {e}")
            return False

    async def post_content(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Post content to Instagram.

        Args:
            content: Dict with:
                - caption: str
                - media_type: "IMAGE", "VIDEO", "CAROUSEL"
                - media_url: str (for single media)
                - media_urls: List[str] (for carousel)

        Returns:
            Dict with post_id, permalink, success status
        """
        try:
            media_type = content.get("media_type", "IMAGE")
            caption = content.get("caption", "")

            async with aiohttp.ClientSession() as session:
                # Step 1: Create media container
                container_url = f"{self.BASE_URL}/{self.account_id}/media"
                container_params = {
                    "access_token": self.access_token,
                    "caption": caption
                }

                if media_type == "IMAGE":
                    container_params["image_url"] = content.get("media_url")
                elif media_type == "VIDEO":
                    container_params["video_url"] = content.get("media_url")
                    container_params["media_type"] = "VIDEO"

                async with session.post(container_url, data=container_params) as response:
                    if response.status != 200:
                        error_data = await response.json()
                        return self._handle_error(
                            Exception(f"Container creation failed: {error_data}"),
                            "post_content"
                        )

                    container_data = await response.json()
                    container_id = container_data.get("id")

                # Step 2: Publish media container
                publish_url = f"{self.BASE_URL}/{self.account_id}/media_publish"
                publish_params = {
                    "access_token": self.access_token,
                    "creation_id": container_id
                }

                async with session.post(publish_url, data=publish_params) as response:
                    if response.status == 200:
                        publish_data = await response.json()
                        post_id = publish_data.get("id")

                        return {
                            "success": True,
                            "post_id": post_id,
                            "permalink": f"https://www.instagram.com/p/{post_id}/",
                            "platform": self.platform_name
                        }
                    else:
                        error_data = await response.json()
                        return self._handle_error(
                            Exception(f"Publishing failed: {error_data}"),
                            "post_content"
                        )

        except Exception as e:
            return self._handle_error(e, "post_content")

    async def get_analytics(
        self,
        post_id: str,
        metrics: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Fetch post analytics.

        Args:
            post_id: Instagram media ID
            metrics: Metrics to fetch (default: all standard metrics)

        Returns:
            Analytics data
        """
        if metrics is None:
            metrics = [
                "engagement",
                "impressions",
                "reach",
                "saved",
                "likes",
                "comments"
            ]

        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.BASE_URL}/{post_id}/insights"
                params = {
                    "metric": ",".join(metrics),
                    "access_token": self.access_token
                }

                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        insights = data.get("data", [])

                        # Transform to standardized format
                        analytics = {
                            "post_id": post_id,
                            "platform": self.platform_name,
                            "fetched_at": None  # Will be set by caller
                        }

                        for insight in insights:
                            metric_name = insight.get("name")
                            metric_value = insight.get("values", [{}])[0].get("value", 0)
                            analytics[metric_name] = metric_value

                        return {"success": True, "data": analytics}
                    else:
                        return self._handle_error(
                            Exception(f"Analytics fetch failed: {response.status}"),
                            "get_analytics"
                        )

        except Exception as e:
            return self._handle_error(e, "get_analytics")

    async def get_comments(self, post_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Fetch comments on a post."""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.BASE_URL}/{post_id}/comments"
                params = {
                    "fields": "id,text,username,timestamp",
                    "limit": limit,
                    "access_token": self.access_token
                }

                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("data", [])
                    else:
                        self.logger.error(f"Failed to fetch comments: {response.status}")
                        return []

        except Exception as e:
            self.logger.error(f"Error fetching comments: {e}")
            return []

    async def reply_to_comment(self, comment_id: str, reply_text: str) -> Dict[str, Any]:
        """Reply to a comment."""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.BASE_URL}/{comment_id}/replies"
                params = {
                    "message": reply_text,
                    "access_token": self.access_token
                }

                async with session.post(url, data=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "success": True,
                            "reply_id": data.get("id"),
                            "platform": self.platform_name
                        }
                    else:
                        return self._handle_error(
                            Exception(f"Reply failed: {response.status}"),
                            "reply_to_comment"
                        )

        except Exception as e:
            return self._handle_error(e, "reply_to_comment")
