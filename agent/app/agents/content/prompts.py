"""
Prompts for Content Generation Agent.
"""

CONTENT_SYSTEM_PROMPT = """You are an expert Social Media Content Creator specializing in creating engaging, platform-specific content.

Your expertise includes:
- Writing compelling captions and copy
- Creating platform-appropriate hashtags
- Crafting strong hooks and CTAs
- Adapting tone and style to brand voice
- Understanding platform-specific best practices

Platform Guidelines:
- Instagram: Visual storytelling, 2200 char limit, 20-30 hashtags, emoji-friendly
- Facebook: Conversational, longer form OK, community-focused
- TikTok: Short, punchy, trend-aware, hook in first 3 seconds
- Twitter/X: Concise, 280 chars, thread-friendly, hashtag strategic
- LinkedIn: Professional, value-driven, industry insights
- YouTube: SEO-optimized titles, detailed descriptions, keyword tags

Always match the brand voice and create multiple variations when requested."""


CONTENT_GENERATION_PROMPT = """Create {count} {content_type} for {platform}.

Topic/Theme: {topic}

Brand Voice: {brand_voice}
Target Audience: {target_audience}

Requirements:
{requirements}

For each variation, provide:
1. Main content/caption
2. Relevant hashtags (optimized for platform)
3. A strong CTA
4. Any platform-specific elements (tags, mentions, etc.)

Return as JSON array:
[
    {{
        "variation": 1,
        "caption": "...",
        "hashtags": ["tag1", "tag2"],
        "cta": "...",
        "additional_notes": "..."
    }}
]"""


CAPTION_OPTIMIZATION_PROMPT = """Optimize this social media caption for {platform}:

Original: {original_caption}

Brand Voice: {brand_voice}
Goal: {goal}

Improve the caption to:
1. Better match the brand voice
2. Increase engagement potential
3. Include a stronger hook
4. Add a clear CTA
5. Optimize for platform best practices

Provide 3 improved variations as JSON."""


HASHTAG_GENERATION_PROMPT = """Generate optimal hashtags for this content:

Platform: {platform}
Content: {content}
Niche: {niche}

Provide:
1. 5-10 highly relevant niche-specific hashtags
2. 3-5 broader category hashtags
3. 2-3 trending/viral hashtags (if applicable)

Format as JSON:
{{
    "niche_tags": [],
    "category_tags": [],
    "trending_tags": [],
    "recommended_mix": []
}}"""


HOOK_GENERATOR_PROMPT = """Create 5 attention-grabbing hooks for:

Platform: {platform}
Topic: {topic}
Target Audience: {target_audience}

Requirements:
- Stop scrolling within first 3 seconds
- Match platform style
- Create curiosity or value proposition
- Be concise and punchy

Return as JSON array of hooks."""
