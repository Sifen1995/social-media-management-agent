"""
Content Agent - specialized agent for generating social media content.
"""
from typing import Dict, Any, List
from app.agents.base.agent import BaseAgent
from app.agents.content.prompts import (
    CONTENT_SYSTEM_PROMPT,
    CONTENT_GENERATION_PROMPT,
    HASHTAG_GENERATION_PROMPT,
    CAPTION_OPTIMIZATION_PROMPT,
    HOOK_GENERATOR_PROMPT
)
import json


class ContentAgent(BaseAgent):
    """
    Content Agent - generates platform-specific social media content.

    Capabilities:
    - Generate posts, captions, scripts
    - Create hashtag strategies
    - Write hooks and CTAs
    - Optimize existing content
    - Generate content variations
    """

    @property
    def name(self) -> str:
        return "content"

    @property
    def description(self) -> str:
        return "Generates engaging, platform-specific social media content"

    def get_required_fields(self) -> list:
        return ["platform", "action"]

    async def execute(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute content generation based on action type.

        Args:
            task: Must contain 'platform' and 'action'
            context: Brand context

        Returns:
            Generated content
        """
        try:
            action = task.get("action", "generate")
            platform = task["platform"]

            # Route to specific content generation method
            if action == "generate":
                result = await self._generate_content(task, context)
            elif action == "optimize":
                result = await self._optimize_caption(task, context)
            elif action == "hashtags":
                result = await self._generate_hashtags(task, context)
            elif action == "hooks":
                result = await self._generate_hooks(task, context)
            else:
                return self.create_result(
                    success=False,
                    message=f"Unknown action: {action}"
                )

            return self.create_result(
                success=True,
                data=result,
                message=f"Content {action} completed for {platform}",
                metadata={"platform": platform, "action": action}
            )

        except Exception as e:
            return self.create_error_result(e, "Content generation failed")

    async def _generate_content(self, task: Dict[str, Any], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate social media content.

        Args:
            task: Content generation parameters
            context: Brand context

        Returns:
            List of content variations
        """
        platform = task["platform"]
        topic = task.get("topic", "")
        content_type = task.get("content_type", "post")
        count = task.get("count", 3)

        brand = context.get("brand", {})
        brand_voice = brand.get("brand_voice", "professional and engaging")
        target_audience = brand.get("target_audience", "general audience")

        requirements = task.get("requirements", "")
        if not requirements:
            requirements = "- Be engaging and authentic\n- Include a clear CTA\n- Use appropriate hashtags"

        prompt = CONTENT_GENERATION_PROMPT.format(
            count=count,
            content_type=content_type,
            platform=platform,
            topic=topic,
            brand_voice=brand_voice,
            target_audience=target_audience,
            requirements=requirements
        )

        response = await self.llm_service.generate_completion(
            system_prompt=CONTENT_SYSTEM_PROMPT,
            user_prompt=prompt,
            temperature=0.8,
            response_format="json"
        )

        try:
            content_variations = json.loads(response)
            return content_variations if isinstance(content_variations, list) else [content_variations]
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            return [{
                "variation": 1,
                "caption": response,
                "hashtags": [],
                "cta": "Engage with us!",
                "additional_notes": "Generated with fallback"
            }]

    async def _optimize_caption(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Optimize an existing caption.

        Args:
            task: Contains original caption and optimization goals
            context: Brand context

        Returns:
            Optimized caption variations
        """
        platform = task["platform"]
        original_caption = task.get("original_caption", "")
        goal = task.get("goal", "increase engagement")

        brand = context.get("brand", {})
        brand_voice = brand.get("brand_voice", "professional and engaging")

        prompt = CAPTION_OPTIMIZATION_PROMPT.format(
            platform=platform,
            original_caption=original_caption,
            brand_voice=brand_voice,
            goal=goal
        )

        response = await self.llm_service.generate_completion(
            system_prompt=CONTENT_SYSTEM_PROMPT,
            user_prompt=prompt,
            temperature=0.7,
            response_format="json"
        )

        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"optimized_caption": response}

    async def _generate_hashtags(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate optimal hashtags for content.

        Args:
            task: Content and platform info
            context: Brand context

        Returns:
            Categorized hashtags
        """
        platform = task["platform"]
        content = task.get("content", "")

        brand = context.get("brand", {})
        niche = brand.get("niche", "general")

        prompt = HASHTAG_GENERATION_PROMPT.format(
            platform=platform,
            content=content,
            niche=niche
        )

        response = await self.llm_service.generate_completion(
            system_prompt=CONTENT_SYSTEM_PROMPT,
            user_prompt=prompt,
            temperature=0.6,
            response_format="json"
        )

        try:
            return json.loads(response)
        except json.JSONDecodeError:
            # Extract hashtags from text if JSON fails
            hashtags = [word for word in response.split() if word.startswith('#')]
            return {
                "niche_tags": hashtags[:10],
                "category_tags": [],
                "trending_tags": [],
                "recommended_mix": hashtags[:15]
            }

    async def _generate_hooks(self, task: Dict[str, Any], context: Dict[str, Any]) -> List[str]:
        """
        Generate attention-grabbing hooks.

        Args:
            task: Topic and platform
            context: Brand context

        Returns:
            List of hooks
        """
        platform = task["platform"]
        topic = task.get("topic", "")

        brand = context.get("brand", {})
        target_audience = brand.get("target_audience", "general audience")

        prompt = HOOK_GENERATOR_PROMPT.format(
            platform=platform,
            topic=topic,
            target_audience=target_audience
        )

        response = await self.llm_service.generate_completion(
            system_prompt=CONTENT_SYSTEM_PROMPT,
            user_prompt=prompt,
            temperature=0.9,
            response_format="json"
        )

        try:
            hooks = json.loads(response)
            return hooks if isinstance(hooks, list) else [hooks]
        except json.JSONDecodeError:
            # Return response split by lines as fallback
            return [line.strip() for line in response.split('\n') if line.strip()]
