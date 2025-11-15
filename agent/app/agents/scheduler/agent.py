"""
Scheduler Agent - creates content calendars and determines optimal posting times.
"""
from typing import Dict, Any, List
from app.agents.base.agent import BaseAgent
from datetime import datetime, timedelta
import json


class SchedulerAgent(BaseAgent):
    """
    Scheduler Agent - manages content scheduling and calendar planning.

    Capabilities:
    - Create content calendars
    - Determine optimal posting times
    - Schedule content across platforms
    - Balance content distribution
    """

    @property
    def name(self) -> str:
        return "scheduler"

    @property
    def description(self) -> str:
        return "Creates content calendars and optimizes posting schedules"

    def get_required_fields(self) -> list:
        return ["action"]

    async def execute(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute scheduling tasks."""
        try:
            action = task.get("action", "create_calendar")

            if action == "create_calendar":
                result = await self._create_calendar(task, context)
            elif action == "optimal_times":
                result = await self._determine_optimal_times(task, context)
            elif action == "schedule_content":
                result = await self._schedule_content(task, context)
            else:
                return self.create_result(success=False, message=f"Unknown action: {action}")

            return self.create_result(
                success=True,
                data=result,
                message=f"Scheduling {action} completed",
                metadata={"action": action}
            )

        except Exception as e:
            return self.create_error_result(e, "Scheduling failed")

    async def _create_calendar(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Create a content calendar."""
        duration_days = task.get("duration_days", 30)
        platforms = task.get("platforms", ["instagram", "facebook"])
        posts_per_week = task.get("posts_per_week", 3)

        brand = context.get("brand", {})

        system_prompt = """You are a social media strategist expert at creating balanced, strategic content calendars."""

        user_prompt = f"""Create a {duration_days}-day content calendar for:

Platforms: {', '.join(platforms)}
Posting Frequency: {posts_per_week} posts per week per platform
Brand Niche: {brand.get('niche', 'general')}
Brand Goals: {brand.get('goals', 'engagement and growth')}

Provide:
1. Daily content themes
2. Platform-specific content types
3. Strategic content mix (educational, promotional, engaging, etc.)
4. Recommended posting times

Return as JSON with structure:
{{
    "calendar": [
        {{
            "date": "YYYY-MM-DD",
            "platform": "instagram",
            "content_type": "post",
            "theme": "...",
            "suggested_time": "HH:MM",
            "notes": "..."
        }}
    ],
    "strategy_notes": "..."
}}"""

        response = await self.llm_service.generate_completion(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.7,
            response_format="json"
        )

        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"calendar": [], "strategy_notes": response}

    async def _determine_optimal_times(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Determine optimal posting times based on analytics."""
        platform = task.get("platform", "instagram")
        analytics_data = context.get("analytics_data", [])

        # Analyze historical performance by time (simplified)
        optimal_times = {
            "instagram": ["09:00", "12:00", "19:00"],
            "facebook": ["13:00", "15:00", "20:00"],
            "tiktok": ["07:00", "16:00", "22:00"],
            "twitter": ["08:00", "12:00", "17:00"],
            "linkedin": ["07:30", "12:00", "17:30"]
        }

        return {
            "platform": platform,
            "optimal_times": optimal_times.get(platform, ["09:00", "12:00", "18:00"]),
            "reasoning": f"Based on {platform} best practices and audience behavior",
            "days": ["Tuesday", "Wednesday", "Thursday"],
            "avoid_times": ["01:00-06:00", "23:00-00:00"]
        }

    async def _schedule_content(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Schedule specific content items."""
        content_items = task.get("content_items", [])
        start_date = task.get("start_date", datetime.now())

        scheduled_items = []
        current_date = start_date if isinstance(start_date, datetime) else datetime.fromisoformat(start_date)

        for idx, item in enumerate(content_items):
            scheduled_time = current_date + timedelta(days=idx)
            scheduled_items.append({
                "content_id": item.get("id"),
                "scheduled_for": scheduled_time.isoformat(),
                "platform": item.get("platform"),
                "status": "scheduled"
            })

        return {
            "scheduled_items": scheduled_items,
            "total_scheduled": len(scheduled_items)
        }
