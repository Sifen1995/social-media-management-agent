"""
Facebook Graph API integration client.
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
import httpx
from app.integrations.base import BasePlatformIntegration


class FacebookClient(BasePlatformIntegration):
    """Facebook Graph API client for posting and analytics."""

    def __init__(self, access_token: str):
        """
        Initialize Facebook client.

        Args:
            access_token: Facebook Page access token
        """
        self.access_token = access_token
        self.base_url = "https://graph.facebook.com/v18.0"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

    async def post_content(
        self,
        content_type: str,
        caption: str,
        media_url: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Post content to Facebook.

        Args:
            content_type: Type of content (post, photo, video)
            caption: Post caption/message
            media_url: URL to media file (for photos/videos)
            **kwargs: Additional parameters (page_id, etc.)

        Returns:
            Dict with post_id and success status
        """
        try:
            page_id = kwargs.get("page_id")
            if not page_id:
                return {"success": False, "error": "page_id is required"}

            endpoint = f"{self.base_url}/{page_id}"

            # Different endpoints for different content types
            if content_type in ["photo", "image"] and media_url:
                endpoint = f"{endpoint}/photos"
                data = {
                    "message": caption,
                    "url": media_url,
                    "access_token": self.access_token,
                }
            elif content_type == "video" and media_url:
                endpoint = f"{endpoint}/videos"
                data = {
                    "description": caption,
                    "file_url": media_url,
                    "access_token": self.access_token,
                }
            else:
                # Regular text post
                endpoint = f"{endpoint}/feed"
                data = {
                    "message": caption,
                    "access_token": self.access_token,
                }

                # Add link if provided
                link = kwargs.get("link")
                if link:
                    data["link"] = link

            async with httpx.AsyncClient() as client:
                response = await client.post(endpoint, json=data, timeout=30.0)
                response.raise_for_status()
                result = response.json()

                return {
                    "success": True,
                    "post_id": result.get("id"),
                    "platform": "facebook",
                }

        except httpx.HTTPStatusError as e:
            error_msg = e.response.json().get("error", {}).get("message", str(e))
            return {"success": False, "error": f"Facebook API error: {error_msg}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def get_analytics(
        self, post_id: str, **kwargs
    ) -> Dict[str, Any]:
        """
        Get analytics for a Facebook post.

        Args:
            post_id: Facebook post ID
            **kwargs: Additional parameters

        Returns:
            Dict with analytics data
        """
        try:
            endpoint = f"{self.base_url}/{post_id}"

            # Request insights and engagement metrics
            params = {
                "fields": "likes.summary(true),comments.summary(true),shares,reactions.summary(true),insights.metric(post_impressions,post_engaged_users,post_reactions_by_type_total)",
                "access_token": self.access_token,
            }

            async with httpx.AsyncClient() as client:
                response = await client.get(endpoint, params=params, timeout=30.0)
                response.raise_for_status()
                data = response.json()

                # Parse the response
                likes_count = data.get("likes", {}).get("summary", {}).get("total_count", 0)
                comments_count = data.get("comments", {}).get("summary", {}).get("total_count", 0)
                shares_count = data.get("shares", {}).get("count", 0)
                reactions = data.get("reactions", {}).get("summary", {}).get("total_count", 0)

                # Parse insights
                insights = data.get("insights", {}).get("data", [])
                impressions = 0
                engaged_users = 0

                for insight in insights:
                    name = insight.get("name")
                    values = insight.get("values", [])
                    if values:
                        value = values[0].get("value", 0)
                        if name == "post_impressions":
                            impressions = value
                        elif name == "post_engaged_users":
                            engaged_users = value

                # Calculate engagement rate
                engagement_rate = 0.0
                if impressions > 0:
                    total_engagement = likes_count + comments_count + shares_count
                    engagement_rate = (total_engagement / impressions) * 100

                return {
                    "likes": likes_count,
                    "comments": comments_count,
                    "shares": shares_count,
                    "reactions": reactions,
                    "impressions": impressions,
                    "reach": engaged_users,  # Using engaged users as reach estimate
                    "engagement_rate": round(engagement_rate, 2),
                    "platform": "facebook",
                }

        except httpx.HTTPStatusError as e:
            return {"error": f"Facebook API error: {str(e)}"}
        except Exception as e:
            return {"error": str(e)}

    async def get_comments(
        self, post_id: str, **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Get comments for a Facebook post.

        Args:
            post_id: Facebook post ID
            **kwargs: Additional parameters

        Returns:
            List of comments
        """
        try:
            endpoint = f"{self.base_url}/{post_id}/comments"
            params = {
                "fields": "id,from,message,created_time,like_count",
                "access_token": self.access_token,
            }

            async with httpx.AsyncClient() as client:
                response = await client.get(endpoint, params=params, timeout=30.0)
                response.raise_for_status()
                data = response.json()

                comments = []
                for comment in data.get("data", []):
                    comments.append({
                        "id": comment.get("id"),
                        "username": comment.get("from", {}).get("name"),
                        "user_id": comment.get("from", {}).get("id"),
                        "text": comment.get("message"),
                        "created_at": comment.get("created_time"),
                        "likes": comment.get("like_count", 0),
                        "platform": "facebook",
                    })

                return comments

        except Exception as e:
            return []

    async def reply_to_comment(
        self, comment_id: str, message: str, **kwargs
    ) -> Dict[str, Any]:
        """
        Reply to a comment on Facebook.

        Args:
            comment_id: Facebook comment ID
            message: Reply message
            **kwargs: Additional parameters

        Returns:
            Dict with success status
        """
        try:
            endpoint = f"{self.base_url}/{comment_id}/comments"
            data = {
                "message": message,
                "access_token": self.access_token,
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(endpoint, json=data, timeout=30.0)
                response.raise_for_status()
                result = response.json()

                return {
                    "success": True,
                    "comment_id": result.get("id"),
                }

        except httpx.HTTPStatusError as e:
            return {"success": False, "error": str(e)}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def delete_post(self, post_id: str, **kwargs) -> Dict[str, Any]:
        """
        Delete a Facebook post.

        Args:
            post_id: Facebook post ID
            **kwargs: Additional parameters

        Returns:
            Dict with success status
        """
        try:
            endpoint = f"{self.base_url}/{post_id}"
            params = {"access_token": self.access_token}

            async with httpx.AsyncClient() as client:
                response = await client.delete(endpoint, params=params, timeout=30.0)
                response.raise_for_status()

                return {"success": True}

        except Exception as e:
            return {"success": False, "error": str(e)}

    async def get_page_insights(
        self, page_id: str, metrics: List[str], **kwargs
    ) -> Dict[str, Any]:
        """
        Get page-level insights from Facebook.

        Args:
            page_id: Facebook page ID
            metrics: List of metrics to retrieve
            **kwargs: Additional parameters (period, etc.)

        Returns:
            Dict with insights data
        """
        try:
            endpoint = f"{self.base_url}/{page_id}/insights"
            params = {
                "metric": ",".join(metrics),
                "period": kwargs.get("period", "day"),
                "access_token": self.access_token,
            }

            async with httpx.AsyncClient() as client:
                response = await client.get(endpoint, params=params, timeout=30.0)
                response.raise_for_status()
                data = response.json()

                insights = {}
                for item in data.get("data", []):
                    metric_name = item.get("name")
                    values = item.get("values", [])
                    if values:
                        insights[metric_name] = values[0].get("value", 0)

                return insights

        except Exception as e:
            return {"error": str(e)}
