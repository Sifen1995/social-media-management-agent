"""
Engagement Agent - manages community interactions and responses.
"""
from typing import Dict, Any, List
from app.agents.base.agent import BaseAgent
import json


class EngagementAgent(BaseAgent):
    """
    Engagement Agent - handles comment replies, DMs, and community management.

    Capabilities:
    - Draft comment replies
    - Generate DM responses
    - Filter spam and harmful content
    - Prioritize engagement items
    - Maintain brand voice in interactions
    """

    @property
    def name(self) -> str:
        return "engagement"

    @property
    def description(self) -> str:
        return "Manages community engagement and generates appropriate responses"

    def get_required_fields(self) -> list:
        return ["action"]

    async def execute(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute engagement tasks."""
        try:
            action = task.get("action", "reply")

            if action == "reply":
                result = await self._generate_reply(task, context)
            elif action == "filter_spam":
                result = await self._filter_spam(task, context)
            elif action == "prioritize":
                result = await self._prioritize_engagement(task, context)
            else:
                return self.create_result(success=False, message=f"Unknown action: {action}")

            return self.create_result(
                success=True,
                data=result,
                message=f"Engagement {action} completed",
                metadata={"action": action}
            )

        except Exception as e:
            return self.create_error_result(e, "Engagement processing failed")

    async def _generate_reply(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate appropriate reply to comment or message."""
        message_type = task.get("message_type", "comment")  # comment, dm, mention
        content = task.get("content", "")
        username = task.get("username", "User")

        brand = context.get("brand", {})
        brand_voice = brand.get("brand_voice", "friendly and professional")

        system_prompt = f"""You are a community manager for a brand with this voice: {brand_voice}

Your role is to engage authentically with the community while:
- Maintaining brand voice
- Being helpful and genuine
- Encouraging further engagement
- Staying concise
- Being appropriate for the platform"""

        user_prompt = f"""Generate a reply to this {message_type}:

From: {username}
Message: {content}

Provide:
1. A primary reply (recommended)
2. Two alternative reply options
3. Sentiment classification (positive/negative/neutral/question)
4. Priority level (high/medium/low)

Return as JSON."""

        response = await self.llm_service.generate_completion(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.7,
            response_format="json"
        )

        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "primary_reply": response,
                "alternatives": [],
                "sentiment": "neutral",
                "priority": "medium"
            }

    async def _filter_spam(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Detect spam and harmful content."""
        messages = task.get("messages", [])

        system_prompt = """You are a content moderation expert. Identify spam, harmful content, and genuine engagement."""

        user_prompt = f"""Analyze these messages and classify each:

{json.dumps(messages, indent=2)}

For each message, determine:
1. is_spam: true/false
2. is_harmful: true/false
3. sentiment: positive/negative/neutral
4. action: reply/ignore/flag

Return as JSON array."""

        response = await self.llm_service.generate_completion(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.3,
            response_format="json"
        )

        try:
            return {"filtered_messages": json.loads(response)}
        except json.JSONDecodeError:
            return {"filtered_messages": []}

    async def _prioritize_engagement(self, task: Dict[str, Any], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Prioritize engagement items by importance."""
        engagement_items = task.get("engagement_items", [])

        # Simple prioritization logic
        prioritized = []
        for item in engagement_items:
            priority_score = 0

            # Questions get high priority
            if "?" in item.get("content", ""):
                priority_score += 3

            # Negative sentiment needs quick response
            if item.get("sentiment") == "negative":
                priority_score += 4

            # Influencers/verified accounts
            if item.get("is_verified", False):
                priority_score += 2

            item["priority_score"] = priority_score
            prioritized.append(item)

        # Sort by priority score
        prioritized.sort(key=lambda x: x.get("priority_score", 0), reverse=True)

        return prioritized
