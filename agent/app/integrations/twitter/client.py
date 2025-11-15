"""
Twitter/X integration using Twitter API v2.
"""
from typing import Dict, Any, List, Optional
from app.integrations.base import BasePlatformIntegration
import aiohttp
import logging

logger = logging.getLogger(__name__)


class TwitterClient(BasePlatformIntegration):
    """
    Twitter API v2 client.

    Requires: Twitter API v2 access with OAuth 2.0
    """

    BASE_URL = "https://api.twitter.com/2"

    @property
    def platform_name(self) -> str:
        return "twitter"

    async def verify_credentials(self) -> bool:
        """Verify access token."""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.BASE_URL}/users/me"
                headers = {"Authorization": f"Bearer {self.access_token}"}

                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.account_id = data.get("data", {}).get("id")
                        return True
                    return False

        except Exception as e:
            self.logger.error(f"Credential verification failed: {e}")
            return False

    async def post_content(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Post a tweet.

        Args:
            content: Dict with 'text' (and optional 'media_ids')

        Returns:
            Result with tweet_id
        """
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.BASE_URL}/tweets"
                headers = {
                    "Authorization": f"Bearer {self.access_token}",
                    "Content-Type": "application/json"
                }

                payload = {"text": content.get("text", content.get("caption", ""))}

                if "media_ids" in content:
                    payload["media"] = {"media_ids": content["media_ids"]}

                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status == 201:
                        data = await response.json()
                        tweet_id = data.get("data", {}).get("id")

                        return {
                            "success": True,
                            "post_id": tweet_id,
                            "permalink": f"https://twitter.com/i/web/status/{tweet_id}",
                            "platform": self.platform_name
                        }
                    else:
                        error_data = await response.json()
                        return self._handle_error(
                            Exception(f"Tweet failed: {error_data}"),
                            "post_content"
                        )

        except Exception as e:
            return self._handle_error(e, "post_content")

    async def get_analytics(self, post_id: str, metrics: Optional[List[str]] = None) -> Dict[str, Any]:
        """Fetch tweet analytics (requires elevated access)."""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.BASE_URL}/tweets/{post_id}"
                params = {
                    "tweet.fields": "public_metrics,created_at"
                }
                headers = {"Authorization": f"Bearer {self.access_token}"}

                async with session.get(url, headers=headers, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        metrics_data = data.get("data", {}).get("public_metrics", {})

                        analytics = {
                            "post_id": post_id,
                            "platform": self.platform_name,
                            "likes": metrics_data.get("like_count", 0),
                            "retweets": metrics_data.get("retweet_count", 0),
                            "replies": metrics_data.get("reply_count", 0),
                            "impressions": metrics_data.get("impression_count", 0)
                        }

                        return {"success": True, "data": analytics}
                    else:
                        return self._handle_error(
                            Exception(f"Analytics fetch failed: {response.status}"),
                            "get_analytics"
                        )

        except Exception as e:
            return self._handle_error(e, "get_analytics")

    async def get_comments(self, post_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Fetch replies to a tweet."""
        # Implementation would use search/recent endpoint with conversation_id
        return []

    async def reply_to_comment(self, comment_id: str, reply_text: str) -> Dict[str, Any]:
        """Reply to a tweet."""
        return await self.post_content({
            "text": reply_text,
            "reply": {"in_reply_to_tweet_id": comment_id}
        })
