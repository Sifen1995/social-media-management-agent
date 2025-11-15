"""
Optimizer Agent for A/B testing and content optimization.
"""
from typing import Dict, Any
from app.agents.base.agent import BaseAgent
from app.agents.optimizer.prompts import (
    AB_TEST_DESIGN_PROMPT,
    CONTENT_OPTIMIZATION_PROMPT,
    TIMING_OPTIMIZATION_PROMPT,
    HASHTAG_OPTIMIZATION_PROMPT,
    CAPTION_OPTIMIZATION_PROMPT,
    PERFORMANCE_PREDICTION_PROMPT,
)
from app.services.llm_service import llm_service
import json


class OptimizerAgent(BaseAgent):
    """
    Agent responsible for optimization activities:
    - A/B test design and analysis
    - Content optimization
    - Timing optimization
    - Hashtag strategy optimization
    - Caption optimization
    - Performance prediction
    """

    @property
    def name(self) -> str:
        return "optimizer"

    @property
    def description(self) -> str:
        return "Provides A/B testing, content optimization, and performance improvement recommendations"

    async def execute(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute optimization task.

        Supported actions:
        - ab_test: Design A/B tests
        - optimize_content: Optimize existing content
        - optimize_timing: Optimize posting schedule
        - optimize_hashtags: Optimize hashtag strategy
        - optimize_caption: Optimize caption text
        - predict_performance: Predict content performance
        """
        action = task.get("action", "optimize_content")

        if action == "ab_test":
            return await self._design_ab_test(task, context)
        elif action == "optimize_content":
            return await self._optimize_content(task, context)
        elif action == "optimize_timing":
            return await self._optimize_timing(task, context)
        elif action == "optimize_hashtags":
            return await self._optimize_hashtags(task, context)
        elif action == "optimize_caption":
            return await self._optimize_caption(task, context)
        elif action == "predict_performance":
            return await self._predict_performance(task, context)
        else:
            return self.format_error(f"Unknown action: {action}")

    async def _design_ab_test(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Design an A/B test for content."""
        try:
            brand_context = self._get_brand_context(context)

            content = task.get("content", {})
            goal = task.get("goal", "increase engagement")

            if not content:
                return self.format_error("No content provided for A/B test design")

            prompt = AB_TEST_DESIGN_PROMPT.format(
                brand_context=json.dumps(brand_context, indent=2),
                content=json.dumps(content, indent=2),
                goal=goal,
            )

            result = await llm_service.generate_completion(prompt, json_response=True)

            if result.get("error"):
                return self.format_error(result["error"])

            data = result.get("data", {})

            return self.format_success(
                data=data,
                message="A/B test design created successfully"
            )

        except Exception as e:
            return self.format_error(str(e))

    async def _optimize_content(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize content for better performance."""
        try:
            brand_context = self._get_brand_context(context)

            content = task.get("content", {})
            performance_data = task.get("performance_data", {})
            top_content = task.get("top_content", [])

            if not content:
                return self.format_error("No content provided for optimization")

            prompt = CONTENT_OPTIMIZATION_PROMPT.format(
                content=json.dumps(content, indent=2),
                performance_data=json.dumps(performance_data, indent=2),
                top_content=json.dumps(top_content, indent=2),
                brand_context=json.dumps(brand_context, indent=2),
            )

            result = await llm_service.generate_completion(prompt, json_response=True)

            if result.get("error"):
                return self.format_error(result["error"])

            data = result.get("data", {})

            return self.format_success(
                data=data,
                message="Content optimization recommendations generated"
            )

        except Exception as e:
            return self.format_error(str(e))

    async def _optimize_timing(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize posting timing."""
        try:
            brand_context = self._get_brand_context(context)

            platform = task.get("platform", "instagram")
            time_performance = task.get("time_performance", {})
            audience_patterns = task.get("audience_patterns", {})
            current_schedule = task.get("current_schedule", [])

            prompt = TIMING_OPTIMIZATION_PROMPT.format(
                brand_context=json.dumps(brand_context, indent=2),
                platform=platform,
                time_performance=json.dumps(time_performance, indent=2),
                audience_patterns=json.dumps(audience_patterns, indent=2),
                current_schedule=json.dumps(current_schedule, indent=2),
            )

            result = await llm_service.generate_completion(prompt, json_response=True)

            if result.get("error"):
                return self.format_error(result["error"])

            data = result.get("data", {})

            return self.format_success(
                data=data,
                message="Posting timing optimized successfully"
            )

        except Exception as e:
            return self.format_error(str(e))

    async def _optimize_hashtags(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize hashtag strategy."""
        try:
            brand_context = self._get_brand_context(context)

            platform = task.get("platform", "instagram")
            current_hashtags = task.get("current_hashtags", [])
            performance_data = task.get("performance_data", {})
            trending_hashtags = task.get("trending_hashtags", [])

            prompt = HASHTAG_OPTIMIZATION_PROMPT.format(
                brand_context=json.dumps(brand_context, indent=2),
                platform=platform,
                current_hashtags=json.dumps(current_hashtags),
                performance_data=json.dumps(performance_data, indent=2),
                trending_hashtags=json.dumps(trending_hashtags),
            )

            result = await llm_service.generate_completion(prompt, json_response=True)

            if result.get("error"):
                return self.format_error(result["error"])

            data = result.get("data", {})

            return self.format_success(
                data=data,
                message="Hashtag strategy optimized successfully"
            )

        except Exception as e:
            return self.format_error(str(e))

    async def _optimize_caption(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize caption text."""
        try:
            brand_context = self._get_brand_context(context)

            caption = task.get("caption", "")
            platform = task.get("platform", "instagram")
            performance_context = task.get("performance_context", {})
            top_captions = task.get("top_captions", [])

            if not caption:
                return self.format_error("No caption provided for optimization")

            brand_voice = brand_context.get("brand_voice", "friendly and authentic")

            prompt = CAPTION_OPTIMIZATION_PROMPT.format(
                caption=caption,
                platform=platform,
                brand_voice=brand_voice,
                performance_context=json.dumps(performance_context, indent=2),
                top_captions=json.dumps(top_captions, indent=2),
            )

            result = await llm_service.generate_completion(prompt, json_response=True)

            if result.get("error"):
                return self.format_error(result["error"])

            data = result.get("data", {})

            return self.format_success(
                data=data,
                message="Caption optimized successfully"
            )

        except Exception as e:
            return self.format_error(str(e))

    async def _predict_performance(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Predict content performance before posting."""
        try:
            brand_context = self._get_brand_context(context)

            content = task.get("content", {})
            platform = task.get("platform", "instagram")
            historical_data = task.get("historical_data", {})
            similar_content = task.get("similar_content", [])
            trends = task.get("trends", {})

            if not content:
                return self.format_error("No content provided for prediction")

            prompt = PERFORMANCE_PREDICTION_PROMPT.format(
                content=json.dumps(content, indent=2),
                platform=platform,
                historical_data=json.dumps(historical_data, indent=2),
                similar_content=json.dumps(similar_content, indent=2),
                trends=json.dumps(trends, indent=2),
            )

            result = await llm_service.generate_completion(prompt, json_response=True)

            if result.get("error"):
                return self.format_error(result["error"])

            data = result.get("data", {})

            # Provide feedback based on prediction
            prediction = data.get("prediction", {})
            performance_tier = prediction.get("performance_tier", "medium")

            if performance_tier in ["high", "viral"]:
                message = f"🚀 Great potential! Predicted {performance_tier} performance"
            elif performance_tier == "low":
                message = "⚠️ Low predicted performance - consider optimizations"
            else:
                message = "📊 Moderate predicted performance"

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

        return {
            "name": context.get("brand_name", "Unknown Brand"),
            "niche": context.get("niche", ""),
            "brand_voice": context.get("brand_voice", ""),
            "target_audience": context.get("target_audience", ""),
        }
