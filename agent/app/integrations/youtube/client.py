"""
YouTube Data API integration client.
"""
from typing import Dict, Any, List, Optional
import httpx
from app.integrations.base import BasePlatformIntegration


class YouTubeClient(BasePlatformIntegration):
    """YouTube Data API client for video management and analytics."""

    def __init__(self, access_token: str):
        """
        Initialize YouTube client.

        Args:
            access_token: YouTube/Google OAuth access token
        """
        self.access_token = access_token
        self.base_url = "https://www.googleapis.com/youtube/v3"
        self.upload_url = "https://www.googleapis.com/upload/youtube/v3"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        }

    async def post_content(
        self,
        content_type: str,
        caption: str,
        media_url: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Upload a video to YouTube.

        Args:
            content_type: Type of content (must be 'video')
            caption: Video description
            media_url: URL or path to video file
            **kwargs: Additional parameters (title, tags, category_id, privacy_status)

        Returns:
            Dict with post_id (video_id) and success status

        Note: Actual video file upload requires multipart/form-data
        This is a simplified implementation outline.
        """
        try:
            if content_type != "video":
                return {"success": False, "error": "YouTube only supports video content"}

            title = kwargs.get("title", "Untitled Video")
            tags = kwargs.get("tags", [])
            category_id = kwargs.get("category_id", "22")  # People & Blogs
            privacy_status = kwargs.get("privacy_status", "public")  # public, private, unlisted

            # Video metadata
            video_metadata = {
                "snippet": {
                    "title": title,
                    "description": caption,
                    "tags": tags,
                    "categoryId": category_id
                },
                "status": {
                    "privacyStatus": privacy_status,
                    "selfDeclaredMadeForKids": False
                }
            }

            # In a real implementation, this would:
            # 1. Upload the video file to YouTube using resumable upload
            # 2. Set the metadata
            # This requires handling multipart file uploads

            endpoint = f"{self.upload_url}/videos"
            params = {
                "part": "snippet,status",
                "uploadType": "resumable"
            }

            async with httpx.AsyncClient() as client:
                # Initialize the upload
                response = await client.post(
                    endpoint,
                    json=video_metadata,
                    params=params,
                    headers=self.headers,
                    timeout=30.0
                )

                if response.status_code in [200, 201]:
                    upload_url = response.headers.get("Location")

                    # In a real implementation, you would upload the video file here
                    # using the upload_url and then get the video ID

                    return {
                        "success": True,
                        "post_id": "upload_initiated",  # Would be actual video ID
                        "platform": "youtube",
                        "upload_url": upload_url,
                        "status": "processing",
                        "note": "Video upload initiated - processing may take time"
                    }
                else:
                    response.raise_for_status()

        except httpx.HTTPStatusError as e:
            try:
                error_data = e.response.json()
                error_msg = error_data.get("error", {}).get("message", str(e))
            except:
                error_msg = str(e)
            return {"success": False, "error": f"YouTube API error: {error_msg}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def get_analytics(
        self, post_id: str, **kwargs
    ) -> Dict[str, Any]:
        """
        Get analytics for a YouTube video.

        Args:
            post_id: YouTube video ID
            **kwargs: Additional parameters

        Returns:
            Dict with analytics data
        """
        try:
            endpoint = f"{self.base_url}/videos"
            params = {
                "part": "statistics,contentDetails",
                "id": post_id
            }

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    endpoint,
                    params=params,
                    headers=self.headers,
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()

                items = data.get("items", [])
                if not items:
                    return {"error": "Video not found"}

                stats = items[0].get("statistics", {})

                views = int(stats.get("viewCount", 0))
                likes = int(stats.get("likeCount", 0))
                comments = int(stats.get("commentCount", 0))

                # YouTube doesn't provide shares directly
                # Calculate engagement rate based on likes and comments
                engagement_rate = 0.0
                if views > 0:
                    total_engagement = likes + comments
                    engagement_rate = (total_engagement / views) * 100

                return {
                    "views": views,
                    "likes": likes,
                    "comments": comments,
                    "favorites": int(stats.get("favoriteCount", 0)),
                    "reach": views,  # Views = reach for YouTube
                    "engagement_rate": round(engagement_rate, 2),
                    "platform": "youtube",
                }

        except Exception as e:
            return {"error": str(e)}

    async def get_comments(
        self, post_id: str, **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Get comments for a YouTube video.

        Args:
            post_id: YouTube video ID
            **kwargs: Additional parameters (max_results, page_token)

        Returns:
            List of comments
        """
        try:
            endpoint = f"{self.base_url}/commentThreads"
            params = {
                "part": "snippet",
                "videoId": post_id,
                "maxResults": kwargs.get("max_results", 50),
                "textFormat": "plainText"
            }

            if kwargs.get("page_token"):
                params["pageToken"] = kwargs["page_token"]

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    endpoint,
                    params=params,
                    headers=self.headers,
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()

                comments = []
                for item in data.get("items", []):
                    snippet = item.get("snippet", {}).get("topLevelComment", {}).get("snippet", {})

                    comments.append({
                        "id": item.get("id"),
                        "username": snippet.get("authorDisplayName"),
                        "text": snippet.get("textDisplay"),
                        "created_at": snippet.get("publishedAt"),
                        "likes": snippet.get("likeCount", 0),
                        "reply_count": item.get("snippet", {}).get("totalReplyCount", 0),
                        "platform": "youtube",
                    })

                return comments

        except Exception as e:
            return []

    async def reply_to_comment(
        self, comment_id: str, message: str, **kwargs
    ) -> Dict[str, Any]:
        """
        Reply to a comment on YouTube.

        Args:
            comment_id: YouTube comment ID
            message: Reply message
            **kwargs: Additional parameters

        Returns:
            Dict with success status
        """
        try:
            endpoint = f"{self.base_url}/comments"
            params = {"part": "snippet"}

            comment_data = {
                "snippet": {
                    "parentId": comment_id,
                    "textOriginal": message
                }
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    endpoint,
                    json=comment_data,
                    params=params,
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
        Delete a YouTube video.

        Args:
            post_id: YouTube video ID
            **kwargs: Additional parameters

        Returns:
            Dict with success status
        """
        try:
            endpoint = f"{self.base_url}/videos"
            params = {"id": post_id}

            async with httpx.AsyncClient() as client:
                response = await client.delete(
                    endpoint,
                    params=params,
                    headers=self.headers,
                    timeout=30.0
                )
                response.raise_for_status()

                return {"success": True}

        except Exception as e:
            return {"success": False, "error": str(e)}

    async def update_video(
        self, video_id: str, title: Optional[str] = None,
        description: Optional[str] = None, **kwargs
    ) -> Dict[str, Any]:
        """
        Update YouTube video metadata.

        Args:
            video_id: YouTube video ID
            title: New title
            description: New description
            **kwargs: Additional metadata

        Returns:
            Dict with success status
        """
        try:
            # First get current video data
            get_endpoint = f"{self.base_url}/videos"
            get_params = {
                "part": "snippet,status",
                "id": video_id
            }

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    get_endpoint,
                    params=get_params,
                    headers=self.headers,
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()

                if not data.get("items"):
                    return {"success": False, "error": "Video not found"}

                video_data = data["items"][0]

                # Update the fields
                if title:
                    video_data["snippet"]["title"] = title
                if description:
                    video_data["snippet"]["description"] = description

                # Update the video
                update_endpoint = f"{self.base_url}/videos"
                update_params = {"part": "snippet,status"}

                update_response = await client.put(
                    update_endpoint,
                    json=video_data,
                    params=update_params,
                    headers=self.headers,
                    timeout=30.0
                )
                update_response.raise_for_status()

                return {"success": True}

        except Exception as e:
            return {"success": False, "error": str(e)}
