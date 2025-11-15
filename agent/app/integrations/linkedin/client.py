"""
LinkedIn API integration client.
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
import httpx
from app.integrations.base import BasePlatformIntegration


class LinkedInClient(BasePlatformIntegration):
    """LinkedIn API client for posting and analytics."""

    def __init__(self, access_token: str):
        """
        Initialize LinkedIn client.

        Args:
            access_token: LinkedIn access token
        """
        self.access_token = access_token
        self.base_url = "https://api.linkedin.com/v2"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
        }

    async def post_content(
        self,
        content_type: str,
        caption: str,
        media_url: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Post content to LinkedIn.

        Args:
            content_type: Type of content (post, article)
            caption: Post text
            media_url: URL to media file (for images/videos)
            **kwargs: Additional parameters (person_urn, organization_urn, etc.)

        Returns:
            Dict with post_id and success status
        """
        try:
            # LinkedIn requires either person or organization URN
            author = kwargs.get("person_urn") or kwargs.get("organization_urn")
            if not author:
                return {"success": False, "error": "person_urn or organization_urn is required"}

            endpoint = f"{self.base_url}/ugcPosts"

            # Build the share content
            share_content = {
                "author": author,
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": caption
                        },
                        "shareMediaCategory": "NONE"  # Default to text post
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }

            # Add media if provided
            if media_url and content_type in ["image", "photo"]:
                share_content["specificContent"]["com.linkedin.ugc.ShareContent"]["shareMediaCategory"] = "IMAGE"
                share_content["specificContent"]["com.linkedin.ugc.ShareContent"]["media"] = [
                    {
                        "status": "READY",
                        "description": {
                            "text": caption[:256]  # LinkedIn has a limit
                        },
                        "media": media_url,
                        "title": {
                            "text": kwargs.get("title", "Image")
                        }
                    }
                ]
            elif kwargs.get("link"):
                # Share a link
                share_content["specificContent"]["com.linkedin.ugc.ShareContent"]["shareMediaCategory"] = "ARTICLE"
                share_content["specificContent"]["com.linkedin.ugc.ShareContent"]["media"] = [
                    {
                        "status": "READY",
                        "originalUrl": kwargs.get("link")
                    }
                ]

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    endpoint,
                    json=share_content,
                    headers=self.headers,
                    timeout=30.0
                )
                response.raise_for_status()
                result = response.json()

                post_id = result.get("id")

                return {
                    "success": True,
                    "post_id": post_id,
                    "platform": "linkedin",
                }

        except httpx.HTTPStatusError as e:
            try:
                error_msg = e.response.json().get("message", str(e))
            except:
                error_msg = str(e)
            return {"success": False, "error": f"LinkedIn API error: {error_msg}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def get_analytics(
        self, post_id: str, **kwargs
    ) -> Dict[str, Any]:
        """
        Get analytics for a LinkedIn post.

        Args:
            post_id: LinkedIn post URN
            **kwargs: Additional parameters

        Returns:
            Dict with analytics data
        """
        try:
            # LinkedIn analytics endpoint
            endpoint = f"{self.base_url}/socialActions/{post_id}"

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    endpoint,
                    headers=self.headers,
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()

                # Parse engagement data
                likes = data.get("likesSummary", {}).get("totalLikes", 0)
                comments = data.get("commentsSummary", {}).get("totalComments", 0)
                shares = data.get("sharesSummary", {}).get("totalShares", 0)

                # Get post statistics
                stats_endpoint = f"{self.base_url}/organizationalEntityShareStatistics"
                params = {
                    "q": "organizationalEntity",
                    "organizationalEntity": kwargs.get("organization_urn", ""),
                    "shares": [post_id]
                }

                stats_response = await client.get(
                    stats_endpoint,
                    params=params,
                    headers=self.headers,
                    timeout=30.0
                )

                impressions = 0
                reach = 0
                if stats_response.status_code == 200:
                    stats = stats_response.json()
                    elements = stats.get("elements", [])
                    if elements:
                        total_stats = elements[0].get("totalShareStatistics", {})
                        impressions = total_stats.get("impressionCount", 0)
                        reach = total_stats.get("uniqueImpressionsCount", 0)

                # Calculate engagement rate
                engagement_rate = 0.0
                if impressions > 0:
                    total_engagement = likes + comments + shares
                    engagement_rate = (total_engagement / impressions) * 100

                return {
                    "likes": likes,
                    "comments": comments,
                    "shares": shares,
                    "impressions": impressions,
                    "reach": reach,
                    "engagement_rate": round(engagement_rate, 2),
                    "platform": "linkedin",
                }

        except Exception as e:
            return {"error": str(e)}

    async def get_comments(
        self, post_id: str, **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Get comments for a LinkedIn post.

        Args:
            post_id: LinkedIn post URN
            **kwargs: Additional parameters

        Returns:
            List of comments
        """
        try:
            endpoint = f"{self.base_url}/socialActions/{post_id}/comments"

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    endpoint,
                    headers=self.headers,
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()

                comments = []
                for comment in data.get("elements", []):
                    actor = comment.get("actor")
                    message = comment.get("message", {}).get("text", "")

                    comments.append({
                        "id": comment.get("$id"),
                        "user_urn": actor,
                        "text": message,
                        "created_at": comment.get("created", {}).get("time"),
                        "platform": "linkedin",
                    })

                return comments

        except Exception as e:
            return []

    async def reply_to_comment(
        self, comment_id: str, message: str, **kwargs
    ) -> Dict[str, Any]:
        """
        Reply to a comment on LinkedIn.

        Args:
            comment_id: LinkedIn comment URN
            message: Reply message
            **kwargs: Additional parameters

        Returns:
            Dict with success status
        """
        try:
            # LinkedIn comment replies are posted as new comments
            # with a parent reference
            post_urn = kwargs.get("post_urn")
            if not post_urn:
                return {"success": False, "error": "post_urn is required"}

            endpoint = f"{self.base_url}/socialActions/{post_urn}/comments"

            comment_data = {
                "actor": kwargs.get("actor_urn"),
                "message": {
                    "text": message
                },
                "parentComment": comment_id
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    endpoint,
                    json=comment_data,
                    headers=self.headers,
                    timeout=30.0
                )
                response.raise_for_status()
                result = response.json()

                return {
                    "success": True,
                    "comment_id": result.get("id"),
                }

        except Exception as e:
            return {"success": False, "error": str(e)}

    async def delete_post(self, post_id: str, **kwargs) -> Dict[str, Any]:
        """
        Delete a LinkedIn post.

        Args:
            post_id: LinkedIn post URN
            **kwargs: Additional parameters

        Returns:
            Dict with success status
        """
        try:
            endpoint = f"{self.base_url}/ugcPosts/{post_id}"

            async with httpx.AsyncClient() as client:
                response = await client.delete(
                    endpoint,
                    headers=self.headers,
                    timeout=30.0
                )
                response.raise_for_status()

                return {"success": True}

        except Exception as e:
            return {"success": False, "error": str(e)}

    async def get_profile_info(self, **kwargs) -> Dict[str, Any]:
        """
        Get LinkedIn profile information.

        Returns:
            Dict with profile data
        """
        try:
            endpoint = f"{self.base_url}/me"

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    endpoint,
                    headers=self.headers,
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()

                return {
                    "id": data.get("id"),
                    "first_name": data.get("localizedFirstName"),
                    "last_name": data.get("localizedLastName"),
                    "profile_picture": data.get("profilePicture"),
                }

        except Exception as e:
            return {"error": str(e)}
