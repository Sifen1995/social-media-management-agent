"""
Planner Agent - Master agent that coordinates task decomposition and delegation.
"""
from typing import Dict, Any
from app.agents.base.agent import BaseAgent
from app.agents.planner.prompts import (
    PLANNER_SYSTEM_PROMPT,
    TASK_DECOMPOSITION_PROMPT,
    AGENT_SELECTION_PROMPT
)
import json


class PlannerAgent(BaseAgent):
    """
    Planner Agent - analyzes user requests and creates execution plans.

    This is the master agent that:
    1. Receives user requests
    2. Determines task complexity
    3. Breaks down complex tasks
    4. Delegates to worker agents
    5. Coordinates multi-step workflows
    """

    @property
    def name(self) -> str:
        return "planner"

    @property
    def description(self) -> str:
        return "Master agent that analyzes requests, decomposes tasks, and coordinates execution"

    def get_required_fields(self) -> list:
        return ["user_request"]

    async def execute(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute planning logic.

        Args:
            task: Must contain 'user_request'
            context: Should contain 'brand' info if available

        Returns:
            Execution plan with agents and steps
        """
        try:
            user_request = task["user_request"]
            brand_context = self._prepare_brand_context(context)

            # Use LLM to decompose the task
            plan = await self._decompose_task(user_request, brand_context)

            return self.create_result(
                success=True,
                data=plan,
                message="Task planning completed successfully",
                metadata={
                    "user_request": user_request,
                    "num_steps": len(plan.get("execution_plan", []))
                }
            )

        except Exception as e:
            return self.create_error_result(e, "Failed to create execution plan")

    async def _decompose_task(self, user_request: str, brand_context: str) -> Dict[str, Any]:
        """
        Decompose user request into an execution plan.

        Args:
            user_request: User's natural language request
            brand_context: Brand information and context

        Returns:
            Execution plan dictionary
        """
        prompt = TASK_DECOMPOSITION_PROMPT.format(
            user_request=user_request,
            brand_context=brand_context
        )

        try:
            response = await self.llm_service.generate_completion(
                system_prompt=PLANNER_SYSTEM_PROMPT,
                user_prompt=prompt,
                temperature=0.3,
                response_format="json"
            )

            # Parse JSON response
            plan = json.loads(response)

            # Validate plan structure
            if not self._validate_plan(plan):
                return self._create_fallback_plan(user_request)

            return plan

        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse LLM response as JSON: {e}")
            return self._create_fallback_plan(user_request)
        except Exception as e:
            self.logger.error(f"Error in task decomposition: {e}")
            return self._create_fallback_plan(user_request)

    def _validate_plan(self, plan: Dict[str, Any]) -> bool:
        """
        Validate that the plan has required structure.

        Args:
            plan: Execution plan from LLM

        Returns:
            True if valid, False otherwise
        """
        required_keys = ["task_type", "execution_plan"]
        if not all(key in plan for key in required_keys):
            return False

        if not isinstance(plan["execution_plan"], list):
            return False

        for step in plan["execution_plan"]:
            if "agent" not in step or "action" not in step:
                return False

        return True

    def _create_fallback_plan(self, user_request: str) -> Dict[str, Any]:
        """
        Create a simple fallback plan when LLM fails.

        Args:
            user_request: Original user request

        Returns:
            Basic execution plan
        """
        # Simple heuristic-based routing
        request_lower = user_request.lower()

        if any(word in request_lower for word in ["create", "write", "generate", "post", "caption"]):
            agent = "content"
        elif any(word in request_lower for word in ["analyze", "performance", "metrics", "report"]):
            agent = "analytics"
        elif any(word in request_lower for word in ["schedule", "calendar", "plan", "when to post"]):
            agent = "scheduler"
        elif any(word in request_lower for word in ["reply", "comment", "dm", "engage"]):
            agent = "engagement"
        elif any(word in request_lower for word in ["trend", "competitor", "listening", "monitor"]):
            agent = "social_listening"
        else:
            agent = "content"  # Default to content generation

        return {
            "task_type": "single",
            "primary_agent": agent,
            "execution_plan": [
                {
                    "step": 1,
                    "agent": agent,
                    "action": user_request,
                    "parameters": {"request": user_request},
                    "critical": True
                }
            ],
            "reasoning": "Fallback plan based on keyword matching"
        }

    def _prepare_brand_context(self, context: Dict[str, Any]) -> str:
        """
        Prepare brand context for the LLM.

        Args:
            context: Context dictionary

        Returns:
            Formatted brand context string
        """
        brand = context.get("brand", {})

        if not brand:
            return "No brand context provided."

        context_parts = []

        if brand.get("name"):
            context_parts.append(f"Brand: {brand['name']}")

        if brand.get("niche"):
            context_parts.append(f"Niche: {brand['niche']}")

        if brand.get("brand_voice"):
            context_parts.append(f"Voice: {brand['brand_voice']}")

        if brand.get("target_audience"):
            context_parts.append(f"Audience: {brand['target_audience']}")

        if brand.get("goals"):
            goals = ", ".join(brand["goals"]) if isinstance(brand["goals"], list) else brand["goals"]
            context_parts.append(f"Goals: {goals}")

        return "\n".join(context_parts) if context_parts else "No brand context provided."
