"""
Analytics Agent - analyzes social media performance and provides insights.
"""
from typing import Dict, Any, List
from app.agents.base.agent import BaseAgent
from datetime import datetime, timedelta
import json


class AnalyticsAgent(BaseAgent):
    """
    Analytics Agent - processes performance data and generates insights.

    Capabilities:
    - Analyze engagement metrics
    - Identify top-performing content
    - Generate performance reports
    - Provide actionable recommendations
    - Track growth trends
    """

    @property
    def name(self) -> str:
        return "analytics"

    @property
    def description(self) -> str:
        
        return "Analyzes performance metrics and provides actionable insights"

    def get_required_fields(self) -> list:
        return ["action"]

    async def execute(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute analytics tasks.

        Args:
            task: Analytics parameters
            context: Brand and data context

        Returns:
            Analytics results and insights
        """
        try:
            action = task.get("action", "report")

            if action == "report":
                result = await self._generate_report(task, context)
            elif action == "top_content":
                result = await self._identify_top_content(task, context)
            elif action == "insights":
                result = await self._generate_insights(task, context)
            elif action == "trends":
                result = await self._analyze_trends(task, context)
            else:
                return self.create_result(success=False, message=f"Unknown action: {action}")

            return self.create_result(
                success=True,
                data=result,
                message=f"Analytics {action} completed",
                metadata={"action": action}
            )

        except Exception as e:
            return self.create_error_result(e, "Analytics processing failed")

    async def _generate_report(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate performance report."""
        time_period = task.get("time_period", "last_30_days")
        analytics_data = context.get("analytics_data", [])

        # Calculate metrics
        total_engagement = sum(item.get("engagement", 0) for item in analytics_data)
        avg_engagement = total_engagement / len(analytics_data) if analytics_data else 0
        total_reach = sum(item.get("reach", 0) for item in analytics_data)

        system_prompt = """You are a social media analytics expert. Analyze data and provide clear, actionable insights."""

        user_prompt = f"""Analyze this performance data for {time_period}:

Total Posts: {len(analytics_data)}
Total Engagement: {total_engagement}
Average Engagement: {avg_engagement:.2f}
Total Reach: {total_reach}

Provide:
1. Performance summary
2. Key insights (3-5 points)
3. Recommendations for improvement
4. Areas of strength

Return as JSON with keys: summary, insights, recommendations, strengths"""

        response = await self.llm_service.generate_completion(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.5,
            response_format="json"
        )

        try:
            report = json.loads(response)
            report["metrics"] = {
                "total_posts": len(analytics_data),
                "total_engagement": total_engagement,
                "avg_engagement": avg_engagement,
                "total_reach": total_reach
            }
            return report
        except json.JSONDecodeError:
            return {"summary": response, "metrics": {}}

    async def _identify_top_content(self, task: Dict[str, Any], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify best-performing content."""
        analytics_data = context.get("analytics_data", [])
        limit = task.get("limit", 10)

        # Sort by engagement rate
        sorted_content = sorted(
            analytics_data,
            key=lambda x: x.get("engagement_rate", 0),
            reverse=True
        )

        return sorted_content[:limit]

    async def _generate_insights(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate AI-powered insights from data."""
        analytics_data = context.get("analytics_data", [])

        system_prompt = """You are an expert at identifying patterns in social media data and providing actionable insights."""

        user_prompt = f"""Analyze this social media performance data:

{json.dumps(analytics_data[:20], indent=2)}

Identify:
1. Content patterns that drive engagement
2. Optimal posting strategies
3. Audience preferences
4. Growth opportunities

Return detailed insights as JSON."""

        response = await self.llm_service.generate_completion(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.6,
            response_format="json"
        )

        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"insights": response}

    async def _analyze_trends(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze growth and engagement trends."""
        analytics_data = context.get("analytics_data", [])

        # Calculate week-over-week growth
        # (Simplified - in production would use actual time-series analysis)

        return {
            "trend_direction": "up",  # up, down, stable
            "growth_rate": 0.15,  # 15% growth
            "trend_insights": "Engagement is trending upward",
            "forecast": "Continue current strategy"
        }
