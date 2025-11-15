"""
Social Listening Agent for monitoring trends, competitors, and brand mentions.
"""
from typing import Dict, Any, List
from app.agents.base.agent import BaseAgent
from app.agents.social_listening.prompts import (
    MONITOR_TRENDS_PROMPT,
    COMPETITOR_ANALYSIS_PROMPT,
    BRAND_MENTIONS_PROMPT,
    AUDIENCE_INSIGHTS_PROMPT,
    VIRAL_CONTENT_ANALYSIS_PROMPT,
    CRISIS_DETECTION_PROMPT,
)
from app.services.llm_service import llm_service
import json


class SocialListeningAgent(BaseAgent):
    """
    Agent responsible for social listening activities:
    - Monitoring trends and hashtags
    - Analyzing competitors
    - Tracking brand mentions
    - Detecting crises
    - Analyzing viral content
    - Understanding audience interests
    """

    @property
    def name(self) -> str:
        return "social_listening"

    @property
    def description(self) -> str:
        return "Monitors trends, competitors, brand mentions, and provides social listening insights"

    async def execute(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute social listening task.

        Supported actions:
        - monitor_trends: Track trending topics and hashtags
        - analyze_competitors: Analyze competitor activity
        - track_mentions: Monitor brand mentions
        - audience_insights: Analyze audience behavior
        - viral_analysis: Analyze viral content patterns
        - crisis_detection: Monitor for potential crises
        """
        action = task.get("action", "monitor_trends")

        if action == "monitor_trends":
            return await self._monitor_trends(task, context)
        elif action == "analyze_competitors":
            return await self._analyze_competitors(task, context)
        elif action == "track_mentions":
            return await self._track_mentions(task, context)
        elif action == "audience_insights":
            return await self._audience_insights(task, context)
        elif action == "viral_analysis":
            return await self._viral_analysis(task, context)
        elif action == "crisis_detection":
            return await self._crisis_detection(task, context)
        else:
            return self.format_error(f"Unknown action: {action}")

    async def _monitor_trends(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Monitor trends and hashtags relevant to the brand."""
        try:
            brand_context = self._get_brand_context(context)

            # Get parameters
            keywords = task.get("keywords", [])
            niche = task.get("niche", brand_context.get("niche", ""))

            # In a real implementation, this would fetch actual social media data
            # For now, we'll use mock data or parameters passed in
            social_activity = task.get("social_activity", "Recent social media posts and discussions in the niche")
            trending_hashtags = task.get("trending_hashtags", [])

            prompt = MONITOR_TRENDS_PROMPT.format(
                brand_context=json.dumps(brand_context, indent=2),
                niche=niche,
                keywords=json.dumps(keywords),
                social_activity=social_activity,
                trending_hashtags=json.dumps(trending_hashtags),
            )

            result = await llm_service.generate_completion(prompt, json_response=True)

            if result.get("error"):
                return self.format_error(result["error"])

            data = result.get("data", {})

            return self.format_success(
                data=data,
                message="Trend monitoring completed successfully"
            )

        except Exception as e:
            return self.format_error(str(e))

    async def _analyze_competitors(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze competitor social media activity."""
        try:
            brand_context = self._get_brand_context(context)

            competitors = task.get("competitors", [])
            competitor_activity = task.get("competitor_activity", {})
            competitor_top_content = task.get("competitor_top_content", {})

            if not competitors:
                return self.format_error("No competitors specified for analysis")

            prompt = COMPETITOR_ANALYSIS_PROMPT.format(
                brand_context=json.dumps(brand_context, indent=2),
                competitors=json.dumps(competitors),
                competitor_activity=json.dumps(competitor_activity, indent=2),
                competitor_top_content=json.dumps(competitor_top_content, indent=2),
            )

            result = await llm_service.generate_completion(prompt, json_response=True)

            if result.get("error"):
                return self.format_error(result["error"])

            data = result.get("data", {})

            return self.format_success(
                data=data,
                message=f"Analyzed {len(competitors)} competitors successfully"
            )

        except Exception as e:
            return self.format_error(str(e))

    async def _track_mentions(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Track and analyze brand mentions."""
        try:
            brand_context = self._get_brand_context(context)
            brand_name = brand_context.get("name", "")

            keywords = task.get("keywords", [brand_name])
            mentions = task.get("mentions", [])

            if not mentions:
                return self.format_success(
                    data={"mention_summary": {"total_mentions": 0}},
                    message="No mentions found in the specified period"
                )

            prompt = BRAND_MENTIONS_PROMPT.format(
                brand_name=brand_name,
                keywords=json.dumps(keywords),
                mentions=json.dumps(mentions, indent=2),
            )

            result = await llm_service.generate_completion(prompt, json_response=True)

            if result.get("error"):
                return self.format_error(result["error"])

            data = result.get("data", {})

            return self.format_success(
                data=data,
                message=f"Analyzed {len(mentions)} brand mentions"
            )

        except Exception as e:
            return self.format_error(str(e))

    async def _audience_insights(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze audience behavior and interests."""
        try:
            brand_context = self._get_brand_context(context)

            audience_data = task.get("audience_data", {})
            engagement_patterns = task.get("engagement_patterns", {})
            common_topics = task.get("common_topics", [])

            prompt = AUDIENCE_INSIGHTS_PROMPT.format(
                brand_context=json.dumps(brand_context, indent=2),
                audience_data=json.dumps(audience_data, indent=2),
                engagement_patterns=json.dumps(engagement_patterns, indent=2),
                common_topics=json.dumps(common_topics),
            )

            result = await llm_service.generate_completion(prompt, json_response=True)

            if result.get("error"):
                return self.format_error(result["error"])

            data = result.get("data", {})

            return self.format_success(
                data=data,
                message="Audience insights generated successfully"
            )

        except Exception as e:
            return self.format_error(str(e))

    async def _viral_analysis(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze viral content patterns."""
        try:
            brand_context = self._get_brand_context(context)

            viral_content = task.get("viral_content", [])

            if not viral_content:
                return self.format_error("No viral content provided for analysis")

            prompt = VIRAL_CONTENT_ANALYSIS_PROMPT.format(
                brand_context=json.dumps(brand_context, indent=2),
                viral_content=json.dumps(viral_content, indent=2),
            )

            result = await llm_service.generate_completion(prompt, json_response=True)

            if result.get("error"):
                return self.format_error(result["error"])

            data = result.get("data", {})

            return self.format_success(
                data=data,
                message="Viral content analysis completed"
            )

        except Exception as e:
            return self.format_error(str(e))

    async def _crisis_detection(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Monitor for potential crises or brand issues."""
        try:
            brand_context = self._get_brand_context(context)

            recent_activity = task.get("recent_activity", {})
            sentiment_trends = task.get("sentiment_trends", {})

            prompt = CRISIS_DETECTION_PROMPT.format(
                brand_context=json.dumps(brand_context, indent=2),
                recent_activity=json.dumps(recent_activity, indent=2),
                sentiment_trends=json.dumps(sentiment_trends, indent=2),
            )

            result = await llm_service.generate_completion(prompt, json_response=True)

            if result.get("error"):
                return self.format_error(result["error"])

            data = result.get("data", {})

            # Check if there's a crisis alert
            crisis_level = data.get("crisis_level", "none")
            if crisis_level in ["high", "critical"]:
                message = f"⚠️ CRISIS ALERT: {crisis_level.upper()} level crisis detected"
            else:
                message = "Crisis monitoring completed - no major issues detected"

            return self.format_success(
                data=data,
                message=message
            )

        except Exception as e:
            return self.format_error(str(e))

    def _get_brand_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Extract brand context from the execution context."""
        if "brand" in context:
            return context["brand"]

        # Return minimal context if not available
        return {
            "name": context.get("brand_name", "Unknown Brand"),
            "niche": context.get("niche", ""),
            "brand_voice": context.get("brand_voice", ""),
            "target_audience": context.get("target_audience", ""),
        }
