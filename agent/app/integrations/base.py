"""
Base class for social media platform integrations.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BasePlatformIntegration(ABC):
    """
    Abstract base class for social media platform integrations.

    Each platform integration must implement:
    - Authentication flow
    - Content posting
    - Analytics fetching
    - Engagement monitoring
    """

    def __init__(self, access_token: str, account_id: Optional[str] = None):
        """
        Initialize platform integration.

        Args:
            access_token: OAuth access token
            account_id: Platform-specific account ID
        """
        self.access_token = access_token
        self.account_id = account_id
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    @property
    @abstractmethod
    def platform_name(self) -> str:
        """Return platform name."""
        pass

    @abstractmethod
    async def verify_credentials(self) -> bool:
        """
        Verify that credentials are valid.

        Returns:
            True if credentials are valid
        """
        pass

    @abstractmethod
    async def post_content(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Post content to the platform.

        Args:
            content: Content data including caption, media, etc.

        Returns:
            Result with post_id and permalink
        """
        pass

    @abstractmethod
    async def get_analytics(
        self,
        post_id: str,
        metrics: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Fetch analytics for a specific post.

        Args:
            post_id: Platform-specific post ID
            metrics: List of metrics to fetch (None = all)

        Returns:
            Analytics data
        """
        pass

    @abstractmethod
    async def get_comments(self, post_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Fetch comments on a post.

        Args:
            post_id: Platform-specific post ID
            limit: Maximum number of comments to fetch

        Returns:
            List of comments
        """
        pass

    @abstractmethod
    async def reply_to_comment(
        self,
        comment_id: str,
        reply_text: str
    ) -> Dict[str, Any]:
        """
        Reply to a comment.

        Args:
            comment_id: Platform-specific comment ID
            reply_text: Reply content

        Returns:
            Result with reply_id
        """
        pass

    def _handle_error(self, error: Exception, operation: str) -> Dict[str, Any]:
        """
        Handle and log errors.

        Args:
            error: Exception that occurred
            operation: Name of operation that failed

        Returns:
            Error result dictionary
        """
        self.logger.error(f"{self.platform_name} {operation} failed: {str(error)}", exc_info=error)
        return {
            "success": False,
            "error": str(error),
            "operation": operation,
            "platform": self.platform_name
        }
