"""
Base Agent class - abstract base for all agents in the system.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime
from app.services.llm_service import LLMService
import logging

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """
    Abstract base class for all agents in the multi-agent system.

    Each agent must implement:
    - name: Unique identifier for the agent
    - description: What the agent does
    - execute: Main logic for processing requests
    """

    def __init__(self, llm_service: Optional[LLMService] = None):
        """
        Initialize base agent.

        Args:
            llm_service: LLM service for AI-powered operations
        """
        self.llm_service = llm_service or LLMService()
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Return the unique name of the agent.

        Returns:
            Agent name
        """
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """
        Return a description of what the agent does.

        Returns:
            Agent description
        """
        pass

    @abstractmethod
    async def execute(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent's main logic.

        Args:
            task: Task parameters and details
            context: Additional context (brand info, user data, etc.)

        Returns:
            Result dictionary containing:
                - success: bool
                - data: Any result data
                - message: str
                - metadata: Dict with execution details
        """
        pass

    async def validate_input(self, task: Dict[str, Any]) -> bool:
        """
        Validate input parameters for the task.

        Args:
            task: Task parameters

        Returns:
            True if valid, False otherwise
        """
        required_fields = self.get_required_fields()
        for field in required_fields:
            if field not in task:
                self.logger.error(f"Missing required field: {field}")
                return False
        return True

    def get_required_fields(self) -> list:
        """
        Get list of required fields for this agent.

        Returns:
            List of required field names
        """
        return []

    async def pre_execute(self, task: Dict[str, Any], context: Dict[str, Any]) -> None:
        """
        Hook for pre-execution logic (logging, validation, etc.).

        Args:
            task: Task parameters
            context: Execution context
        """
        self.logger.info(f"Executing {self.name} with task: {task.get('description', 'N/A')}")

    async def post_execute(self, result: Dict[str, Any], task: Dict[str, Any]) -> None:
        """
        Hook for post-execution logic (cleanup, logging, etc.).

        Args:
            result: Execution result
            task: Original task
        """
        self.logger.info(f"Completed {self.name} - Success: {result.get('success', False)}")

    def create_result(
        self,
        success: bool,
        data: Any = None,
        message: str = "",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a standardized result dictionary.

        Args:
            success: Whether execution was successful
            data: Result data
            message: Human-readable message
            metadata: Additional metadata

        Returns:
            Standardized result dictionary
        """
        return {
            "success": success,
            "data": data,
            "message": message,
            "metadata": metadata or {},
            "agent": self.name,
            "timestamp": datetime.utcnow().isoformat()
        }

    def create_error_result(self, error: Exception, message: str = "") -> Dict[str, Any]:
        """
        Create an error result dictionary.

        Args:
            error: The exception that occurred
            message: Custom error message

        Returns:
            Error result dictionary
        """
        error_msg = message or str(error)
        self.logger.error(f"{self.name} error: {error_msg}", exc_info=error)

        return self.create_result(
            success=False,
            message=error_msg,
            metadata={
                "error_type": type(error).__name__,
                "error_details": str(error)
            }
        )
