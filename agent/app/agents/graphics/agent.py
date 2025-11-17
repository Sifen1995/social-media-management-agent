"""
Graphics Agent - generates graphic asset specifications and images for social media content.
"""
import logging
from typing import Dict, Any, List, Optional
import json
import os
from app.agents.base.agent import BaseAgent
from app.agents.graphics.prompts import (
    GRAPHICS_SYSTEM_PROMPT,
    GRAPHIC_SPEC_PROMPT,
    BATCH_GRAPHICS_PROMPT,
    IMAGE_GEN_PROMPT_TEMPLATE
)

logger = logging.getLogger(__name__)


class GraphicsAgent(BaseAgent):
    """
    Graphics Agent - creates graphic asset specifications and generates images.

    Capabilities:
    - Generate graphic design specifications
    - Create image generation prompts
    - Optimize graphics for each platform
    - Maintain brand consistency
    - Generate banners, carousels, quotes, promos
    - Integration with image generation APIs (future)
    """

    @property
    def name(self) -> str:
        return "graphics"

    @property
    def description(self) -> str:
        return "Generates graphic asset specifications and images for social media content"

    def get_required_fields(self) -> list:
        return ["content", "platform"]

    async def execute(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute graphics generation.

        Args:
            task: Must contain 'content' and 'platform', optional 'brand_profile'
            context: Execution context with brand info

        Returns:
            Graphic specifications and/or generated images
        """
        try:
            content = task.get("content")
            platform = task.get("platform")
            mode = task.get("mode", "specification")  # specification, generate, or both
            batch = task.get("batch", False)

            brand_profile = task.get("brand_profile") or context.get("brand_profile", {})

            if not content:
                return self.create_result(
                    success=False,
                    message="Content is required for graphic generation"
                )

            logger.info(f"Generating graphics for {platform} in {mode} mode")

            if batch:
                result = await self._generate_batch_graphics(
                    content,
                    brand_profile,
                    context
                )
            else:
                result = await self._generate_single_graphic(
                    content,
                    platform,
                    brand_profile,
                    context,
                    mode
                )

            # Save graphics metadata
            if result.get("success"):
                self._save_graphics_metadata(result["data"], context)

            return self.create_result(
                success=True,
                data=result["data"],
                message=f"Graphics generated successfully",
                metadata={
                    "platform": platform,
                    "mode": mode,
                    "batch": batch
                }
            )

        except Exception as e:
            logger.error(f"Error in graphics agent: {str(e)}", exc_info=e)
            return self.create_error_result(e, "Graphics generation failed")

    async def _generate_single_graphic(
        self,
        content: Dict[str, Any],
        platform: str,
        brand_profile: Dict[str, Any],
        context: Dict[str, Any],
        mode: str
    ) -> Dict[str, Any]:
        """
        Generate a single graphic specification.

        Args:
            content: Content information
            platform: Target platform
            brand_profile: Brand profile data
            context: Execution context
            mode: specification, generate, or both

        Returns:
            Graphic specification and/or generated image
        """
        # Extract brand info
        brand_name = brand_profile.get("brand_name", "Brand")
        brand_colors = self._extract_colors(brand_profile)
        brand_fonts = brand_profile.get("brand_fonts", "Sans-serif, Modern")
        brand_voice = brand_profile.get("tone_voice", "professional")

        # Extract content info
        caption = content.get("caption", "")
        content_type = content.get("content_type", "post")
        theme = content.get("theme", "general")
        requirements = content.get("requirements", "Eye-catching and on-brand")

        # Generate specification
        prompt = GRAPHIC_SPEC_PROMPT.format(
            brand_name=brand_name,
            brand_colors=brand_colors,
            brand_fonts=brand_fonts,
            brand_voice=brand_voice,
            platform=platform,
            content_type=content_type,
            caption=caption[:200],  # Limit caption length
            theme=theme,
            requirements=requirements
        )

        response = await self.llm_service.generate_completion(
            system_prompt=GRAPHICS_SYSTEM_PROMPT,
            user_prompt=prompt,
            temperature=0.6,
            response_format="json"
        )

        try:
            graphic_spec = json.loads(response)

            # Add platform dimensions if not present
            graphic_spec = self._ensure_platform_dimensions(graphic_spec, platform, content_type)

            result = {
                "specification": graphic_spec,
                "content_id": content.get("id", "unknown")
            }

            # Generate image if requested
            if mode in ["generate", "both"]:
                image_result = await self._generate_image(graphic_spec, brand_profile, context)
                result["image"] = image_result

            return {
                "success": True,
                "data": result
            }

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse graphic spec JSON: {str(e)}")
            return {
                "success": False,
                "error": "Failed to parse graphic specification",
                "raw_response": response[:500]
            }

    async def _generate_batch_graphics(
        self,
        content_batch: List[Dict[str, Any]],
        brand_profile: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate graphics for a batch of content.

        Args:
            content_batch: List of content items
            brand_profile: Brand profile data
            context: Execution context

        Returns:
            List of graphic specifications
        """
        graphics = []

        for content in content_batch:
            platform = content.get("platform", "instagram")
            result = await self._generate_single_graphic(
                content,
                platform,
                brand_profile,
                context,
                mode="specification"
            )

            if result.get("success"):
                graphics.append(result["data"])

        return {
            "success": True,
            "data": {
                "graphics": graphics,
                "total_count": len(graphics),
                "generated_at": self._get_timestamp()
            }
        }

    async def _generate_image(
        self,
        graphic_spec: Dict[str, Any],
        brand_profile: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate actual image using image generation API.

        Args:
            graphic_spec: Graphic specification
            brand_profile: Brand profile
            context: Execution context

        Returns:
            Generated image info or placeholder
        """
        # This is a placeholder for actual image generation integration
        # In production, integrate with:
        # - DALL-E API
        # - Midjourney API
        # - Stable Diffusion
        # - Canva API
        # - MCP image generation tools

        logger.info("Image generation requested - using placeholder")

        # For now, return the generation prompt that can be used with external tools
        image_gen_prompt = graphic_spec.get("image_generation_prompt", "")

        if not image_gen_prompt:
            # Build one from the spec
            image_gen_prompt = self._build_image_prompt(graphic_spec, brand_profile)

        return {
            "status": "pending_generation",
            "message": "Use this prompt with an image generation tool",
            "prompt": image_gen_prompt,
            "canva_suggestion": graphic_spec.get("canva_template_suggestion", ""),
            "dimensions": graphic_spec.get("dimensions", {}),
            "manual_creation_guide": self._create_manual_guide(graphic_spec)
        }

    def _build_image_prompt(
        self,
        graphic_spec: Dict[str, Any],
        brand_profile: Dict[str, Any]
    ) -> str:
        """
        Build detailed image generation prompt from spec.

        Args:
            graphic_spec: Graphic specification
            brand_profile: Brand profile

        Returns:
            Detailed prompt for image generation
        """
        platform = graphic_spec.get("platform", "social media")
        dimensions = graphic_spec.get("dimensions", {})
        dim_str = f"{dimensions.get('width')}x{dimensions.get('height')}"

        color_scheme = graphic_spec.get("color_scheme", {})
        colors_str = ", ".join([f"{k}: {v}" for k, v in color_scheme.items()])

        typography = graphic_spec.get("typography", {})
        headline = typography.get("headline", {}).get("text", "")

        style_notes = graphic_spec.get("style_notes", {})
        aesthetic = style_notes.get("aesthetic", "modern")
        mood = style_notes.get("mood", "professional")

        visual_elements = graphic_spec.get("visual_elements", {})
        images_desc = ", ".join(visual_elements.get("images", []))

        prompt = IMAGE_GEN_PROMPT_TEMPLATE.format(
            style=aesthetic,
            platform=platform,
            description=headline if headline else "engaging visual content",
            dimensions=dim_str,
            colors=colors_str,
            typography=f"{typography.get('headline', {}).get('font', 'Sans-serif')}",
            aesthetic=aesthetic,
            mood=mood,
            adjectives=f"{mood}, {aesthetic}, eye-catching",
            brand_voice=brand_profile.get("tone_voice", "professional"),
            target_audience=brand_profile.get("target_audience", "general audience"),
            include_elements=images_desc if images_desc else "brand-relevant imagery",
            exclude_elements="low quality, blurry, distorted text"
        )

        return prompt.strip()

    def _extract_colors(self, brand_profile: Dict[str, Any]) -> str:
        """
        Extract or infer brand colors from profile.

        Args:
            brand_profile: Brand profile data

        Returns:
            Color description string
        """
        # Try to extract colors from profile
        colors = brand_profile.get("brand_colors", [])

        if colors:
            if isinstance(colors, list):
                return ", ".join(colors)
            return str(colors)

        # Default professional color schemes based on tone
        tone = brand_profile.get("tone_voice", "").lower()

        color_schemes = {
            "professional": "#2C3E50, #3498DB, #ECF0F1",
            "playful": "#FF6B6B, #4ECDC4, #FFE66D",
            "luxury": "#2C2C2C, #D4AF37, #FFFFFF",
            "energetic": "#FF5722, #FFC107, #4CAF50",
            "calm": "#5F9EA0, #E0F2F1, #FFFFFF",
            "bold": "#E91E63, #9C27B0, #FFEB3B"
        }

        for key, scheme in color_schemes.items():
            if key in tone:
                return scheme

        return "#2C3E50, #3498DB, #ECF0F1"  # Default

    def _ensure_platform_dimensions(
        self,
        graphic_spec: Dict[str, Any],
        platform: str,
        content_type: str
    ) -> Dict[str, Any]:
        """
        Ensure graphic has correct dimensions for platform.

        Args:
            graphic_spec: Graphic specification
            platform: Target platform
            content_type: Content type

        Returns:
            Updated spec with correct dimensions
        """
        platform_dimensions = {
            "instagram": {
                "post": {"width": 1080, "height": 1080},
                "story": {"width": 1080, "height": 1920},
                "reel": {"width": 1080, "height": 1920},
                "carousel": {"width": 1080, "height": 1080}
            },
            "facebook": {
                "post": {"width": 1200, "height": 630},
                "story": {"width": 1080, "height": 1920},
                "cover": {"width": 820, "height": 312}
            },
            "twitter": {
                "post": {"width": 1200, "height": 675},
                "header": {"width": 1500, "height": 500}
            },
            "linkedin": {
                "post": {"width": 1200, "height": 627},
                "article": {"width": 1200, "height": 627},
                "cover": {"width": 1584, "height": 396}
            },
            "tiktok": {
                "video": {"width": 1080, "height": 1920}
            },
            "youtube": {
                "thumbnail": {"width": 1280, "height": 720},
                "banner": {"width": 2560, "height": 1440}
            }
        }

        if "dimensions" not in graphic_spec or not graphic_spec["dimensions"]:
            platform_dims = platform_dimensions.get(platform, {})
            type_dims = platform_dims.get(content_type, platform_dims.get("post", {}))

            if type_dims:
                graphic_spec["dimensions"] = {
                    "width": type_dims["width"],
                    "height": type_dims["height"],
                    "unit": "px"
                }

        return graphic_spec

    def _create_manual_guide(self, graphic_spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a guide for manually creating the graphic.

        Args:
            graphic_spec: Graphic specification

        Returns:
            Step-by-step creation guide
        """
        return {
            "tool_suggestions": ["Canva", "Adobe Express", "Figma", "Photoshop"],
            "steps": [
                f"1. Create new design with dimensions {graphic_spec.get('dimensions', {})}",
                f"2. Set background to {graphic_spec.get('color_scheme', {}).get('background', 'solid color')}",
                f"3. Add headline: {graphic_spec.get('typography', {}).get('headline', {}).get('text', '')}",
                "4. Apply brand colors and fonts as specified",
                "5. Add visual elements: " + ", ".join(graphic_spec.get('visual_elements', {}).get('images', [])),
                "6. Export as PNG or JPG at specified dimensions"
            ],
            "canva_search": graphic_spec.get("canva_template_suggestion", "social media post")
        }

    def _save_graphics_metadata(self, graphics_data: Dict[str, Any], context: Dict[str, Any]) -> None:
        """
        Save graphics metadata to file.

        Args:
            graphics_data: Graphics data
            context: Execution context
        """
        try:
            # Create output directory
            output_dir = context.get("output_dir", "outputs")
            assets_dir = os.path.join(output_dir, "assets")
            os.makedirs(assets_dir, exist_ok=True)

            # Save graphics metadata
            metadata_path = os.path.join(assets_dir, "graphics_metadata.json")
            with open(metadata_path, "w", encoding="utf-8") as f:
                json.dump(graphics_data, f, indent=2, ensure_ascii=False)

            logger.info(f"Graphics metadata saved to {metadata_path}")

        except Exception as e:
            logger.error(f"Failed to save graphics metadata: {str(e)}")

    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.utcnow().isoformat() + "Z"
