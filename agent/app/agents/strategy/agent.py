"""
Platform Strategy Analyzer Agent - analyzes brand profiles and creates
platform-specific content strategies.
"""
import logging
from typing import Dict, Any, List
import json
from app.agents.base.agent import BaseAgent
from app.agents.strategy.prompts import (
    STRATEGY_SYSTEM_PROMPT,
    PLATFORM_STRATEGY_PROMPT,
    QUICK_STRATEGY_PROMPT
)

logger = logging.getLogger(__name__)


class StrategyAgent(BaseAgent):
    """
    Strategy Agent - creates comprehensive platform-specific content strategies.

    Capabilities:
    - Multi-platform strategy generation
    - Posting schedule optimization
    - Content format recommendations
    - Hashtag strategy development
    - Engagement tactic suggestions
    - Platform-specific best practices
    """

    @property
    def name(self) -> str:
        return "strategy"

    @property
    def description(self) -> str:
        return "Analyzes brand profiles and creates comprehensive, platform-specific content strategies"

    def get_required_fields(self) -> list:
        return ["brand_profile", "platforms"]

    async def execute(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute strategy analysis.

        Args:
            task: Must contain 'brand_profile' and 'platforms'
            context: Execution context

        Returns:
            Comprehensive strategy plan
        """
        try:
            brand_profile = task.get("brand_profile")
            platforms = task.get("platforms", [
                "instagram", "facebook", "twitter", "linkedin", "tiktok"
            ])
            mode = task.get("mode", "comprehensive")  # or "quick"

            if not brand_profile:
                return self.create_result(
                    success=False,
                    message="Brand profile is required"
                )

            logger.info(f"Generating {mode} strategy for platforms: {platforms}")

            if mode == "quick":
                result = await self._quick_strategy(brand_profile, platforms)
            else:
                result = await self._comprehensive_strategy(brand_profile, platforms)

            # Save to file
            if result.get("success"):
                self._save_strategy_plan(result["data"], context)

            return self.create_result(
                success=True,
                data=result["data"],
                message=f"Strategy generated for {len(platforms)} platforms",
                metadata={
                    "platforms": platforms,
                    "mode": mode
                }
            )

        except Exception as e:
            logger.error(f"Error in strategy agent: {str(e)}", exc_info=e)
            return self.create_error_result(e, "Strategy generation failed")

    async def _comprehensive_strategy(
        self,
        brand_profile: Dict[str, Any],
        platforms: List[str]
    ) -> Dict[str, Any]:
        """
        Generate comprehensive strategy for all platforms.

        Args:
            brand_profile: Full brand profile data
            platforms: List of platform names

        Returns:
            Comprehensive strategy plan
        """
        # Format brand profile for prompt
        brand_profile_text = self._format_brand_profile(brand_profile)
        platforms_text = ", ".join(platforms)

        prompt = PLATFORM_STRATEGY_PROMPT.format(
            brand_profile=brand_profile_text,
            platforms=platforms_text
        )

        response = await self.llm_service.generate_completion(
            system_prompt=STRATEGY_SYSTEM_PROMPT,
            user_prompt=prompt,
            temperature=0.4,  # Lower temperature for more consistent strategic advice
            response_format="json"
        )

        try:
            strategy = json.loads(response)

            # Validate strategy structure
            if not self._validate_strategy(strategy):
                logger.warning("Strategy validation failed, attempting to fix structure")
                strategy = self._fix_strategy_structure(strategy, platforms)

            return {
                "success": True,
                "data": strategy
            }

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse strategy JSON: {str(e)}")
            return {
                "success": False,
                "error": "Failed to parse strategy response",
                "raw_response": response[:500]
            }

    async def _quick_strategy(
        self,
        brand_profile: Dict[str, Any],
        platforms: List[str]
    ) -> Dict[str, Any]:
        """
        Generate quick strategy summaries for platforms.

        Args:
            brand_profile: Brand profile data
            platforms: List of platform names

        Returns:
            Quick strategy summaries
        """
        platform_strategies = {}

        for platform in platforms:
            prompt = QUICK_STRATEGY_PROMPT.format(
                platform=platform,
                brand_name=brand_profile.get("brand_name", "Brand"),
                niche=brand_profile.get("niche", "general"),
                target_audience=brand_profile.get("target_audience", "general audience"),
                brand_voice=brand_profile.get("tone_voice", "professional")
            )

            response = await self.llm_service.generate_completion(
                system_prompt=STRATEGY_SYSTEM_PROMPT,
                user_prompt=prompt,
                temperature=0.4,
                response_format="json"
            )

            try:
                platform_strategy = json.loads(response)
                platform_strategies[platform] = platform_strategy
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse strategy for {platform}, using defaults")
                platform_strategies[platform] = self._get_default_strategy(platform)

        return {
            "success": True,
            "data": {
                "mode": "quick",
                "platforms": platform_strategies,
                "generated_at": self._get_timestamp()
            }
        }

    def _format_brand_profile(self, brand_profile: Dict[str, Any]) -> str:
        """
        Format brand profile into readable text for LLM.

        Args:
            brand_profile: Brand profile dict

        Returns:
            Formatted string
        """
        formatted = []

        formatted.append(f"**Brand Name:** {brand_profile.get('brand_name', 'N/A')}")
        formatted.append(f"\n**Overview:** {brand_profile.get('overview', 'N/A')}")
        formatted.append(f"\n**Mission:** {brand_profile.get('mission', 'N/A')}")
        formatted.append(f"\n**Tone of Voice:** {brand_profile.get('tone_voice', 'N/A')}")
        formatted.append(f"\n**Target Audience:** {brand_profile.get('target_audience', 'N/A')}")
        formatted.append(f"\n**Niche/Industry:** {brand_profile.get('niche', 'N/A')}")

        products = brand_profile.get('products_services', [])
        if products:
            formatted.append(f"\n**Products/Services:** {', '.join(products)}")

        values = brand_profile.get('brand_values', [])
        if values:
            formatted.append(f"\n**Brand Values:** {', '.join(values)}")

        competitors = brand_profile.get('competitors', [])
        if competitors:
            formatted.append(f"\n**Competitors:** {', '.join(competitors)}")

        return "\n".join(formatted)

    def _validate_strategy(self, strategy: Dict[str, Any]) -> bool:
        """
        Validate strategy structure.

        Args:
            strategy: Strategy dict to validate

        Returns:
            True if valid
        """
        required_keys = ["strategy_overview", "platforms"]

        for key in required_keys:
            if key not in strategy:
                logger.warning(f"Strategy missing required key: {key}")
                return False

        return True

    def _fix_strategy_structure(
        self,
        strategy: Dict[str, Any],
        platforms: List[str]
    ) -> Dict[str, Any]:
        """
        Attempt to fix incomplete strategy structure.

        Args:
            strategy: Incomplete strategy
            platforms: Expected platforms

        Returns:
            Fixed strategy with defaults
        """
        if "strategy_overview" not in strategy:
            strategy["strategy_overview"] = {
                "brand_voice_alignment": "Strategy aligned with brand voice",
                "target_audience_focus": "Focused on target audience engagement",
                "primary_goals": ["engagement", "reach", "growth"],
                "estimated_reach_potential": "moderate"
            }

        if "platforms" not in strategy:
            strategy["platforms"] = {}

        for platform in platforms:
            if platform not in strategy["platforms"]:
                strategy["platforms"][platform] = self._get_default_strategy(platform)

        return strategy

    def _get_default_strategy(self, platform: str) -> Dict[str, Any]:
        """
        Get default strategy for a platform.

        Args:
            platform: Platform name

        Returns:
            Default strategy dict
        """
        defaults = {
            "instagram": {
                "posting_schedule": {
                    "frequency": "4-5 posts per week",
                    "best_times": ["09:00", "12:00", "19:00"],
                    "best_days": ["Monday", "Wednesday", "Friday"],
                    "timezone": "UTC"
                },
                "content_formats": {
                    "primary_formats": ["Reels", "Carousels", "Stories"],
                    "content_mix": {"educational": 40, "entertaining": 30, "promotional": 30}
                },
                "hashtag_strategy": {
                    "optimal_count": 15,
                    "hashtag_mix": {"large": 3, "medium": 7, "niche": 5}
                }
            },
            "facebook": {
                "posting_schedule": {
                    "frequency": "3-4 posts per week",
                    "best_times": ["13:00", "15:00", "20:00"],
                    "best_days": ["Tuesday", "Thursday", "Saturday"],
                    "timezone": "UTC"
                },
                "content_formats": {
                    "primary_formats": ["Videos", "Link posts", "Photos"],
                    "content_mix": {"educational": 35, "entertaining": 35, "promotional": 30}
                },
                "hashtag_strategy": {
                    "optimal_count": 5,
                    "hashtag_mix": {"large": 1, "medium": 2, "niche": 2}
                }
            },
            "twitter": {
                "posting_schedule": {
                    "frequency": "10-15 posts per week",
                    "best_times": ["08:00", "12:00", "17:00"],
                    "best_days": ["Monday", "Tuesday", "Wednesday"],
                    "timezone": "UTC"
                },
                "content_formats": {
                    "primary_formats": ["Short tweets", "Threads", "Images"],
                    "content_mix": {"educational": 30, "engaging": 40, "promotional": 30}
                },
                "hashtag_strategy": {
                    "optimal_count": 2,
                    "hashtag_mix": {"trending": 1, "niche": 1}
                }
            },
            "linkedin": {
                "posting_schedule": {
                    "frequency": "3-5 posts per week",
                    "best_times": ["07:30", "12:00", "17:30"],
                    "best_days": ["Tuesday", "Wednesday", "Thursday"],
                    "timezone": "UTC"
                },
                "content_formats": {
                    "primary_formats": ["Articles", "Document posts", "Videos"],
                    "content_mix": {"educational": 50, "thought_leadership": 30, "promotional": 20}
                },
                "hashtag_strategy": {
                    "optimal_count": 5,
                    "hashtag_mix": {"industry": 3, "niche": 2}
                }
            },
            "tiktok": {
                "posting_schedule": {
                    "frequency": "5-7 posts per week",
                    "best_times": ["07:00", "16:00", "22:00"],
                    "best_days": ["Tuesday", "Thursday", "Friday"],
                    "timezone": "UTC"
                },
                "content_formats": {
                    "primary_formats": ["Short videos", "Trends", "Challenges"],
                    "content_mix": {"entertaining": 50, "educational": 30, "promotional": 20}
                },
                "hashtag_strategy": {
                    "optimal_count": 5,
                    "hashtag_mix": {"trending": 2, "niche": 3}
                }
            }
        }

        return defaults.get(platform, defaults["instagram"])

    def _save_strategy_plan(self, strategy: Dict[str, Any], context: Dict[str, Any]) -> None:
        """
        Save strategy plan to file.

        Args:
            strategy: Strategy data
            context: Execution context
        """
        try:
            import os

            # Create output directory if it doesn't exist
            output_dir = context.get("output_dir", "outputs")
            os.makedirs(output_dir, exist_ok=True)

            # Save strategy plan
            output_path = os.path.join(output_dir, "strategy_plan.json")
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(strategy, f, indent=2, ensure_ascii=False)

            logger.info(f"Strategy plan saved to {output_path}")

        except Exception as e:
            logger.error(f"Failed to save strategy plan: {str(e)}")

    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.utcnow().isoformat() + "Z"
