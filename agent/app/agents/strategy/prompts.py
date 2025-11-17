"""
Prompts for Platform Strategy Analyzer Agent.
"""

STRATEGY_SYSTEM_PROMPT = """You are a world-class social media strategist with deep expertise in:
- Platform-specific best practices (Instagram, TikTok, LinkedIn, Facebook, X/Twitter, YouTube)
- Content strategy and audience engagement
- Optimal posting times and frequency
- Hashtag strategies and trending topics
- Content formats and themes

Your role is to analyze brand profiles and create comprehensive, data-driven content strategies
tailored to each platform's unique characteristics and the brand's specific goals."""

PLATFORM_STRATEGY_PROMPT = """Based on the following brand profile, create a comprehensive multi-platform content strategy.

# Brand Profile
{brand_profile}

# Task
Analyze this brand and create a detailed content strategy for the following platforms:
{platforms}

For each platform, provide:

1. **Posting Schedule**
   - Recommended posting frequency (posts per week)
   - Best posting times (specific hours in UTC)
   - Best days of the week
   - Reasoning based on platform algorithms and audience behavior

2. **Content Formats**
   - Primary content types to focus on (e.g., Reels, Stories, Carousels, Videos, etc.)
   - Content mix ratios (e.g., 40% educational, 30% entertaining, 30% promotional)
   - Format-specific recommendations

3. **Hashtag Strategy**
   - Number of hashtags to use
   - Mix of hashtag sizes (large, medium, niche)
   - Branded hashtags to create/use
   - Campaign-specific hashtag ideas

4. **Content Themes**
   - Weekly or monthly content themes
   - Content pillars aligned with brand values
   - Seasonal content opportunities
   - Trending topics to leverage

5. **Audience Engagement**
   - Engagement tactics specific to this platform
   - Community building strategies
   - Call-to-action recommendations
   - Response time expectations

6. **Platform-Specific Tips**
   - Algorithm optimization tactics
   - Features to leverage (e.g., Instagram Guides, LinkedIn Articles, Twitter Spaces)
   - Common pitfalls to avoid
   - Growth hacks

Return your analysis as a JSON object with this structure:
{{
  "strategy_overview": {{
    "brand_voice_alignment": "How the strategy aligns with brand voice",
    "target_audience_focus": "Key audience considerations",
    "primary_goals": ["goal1", "goal2", "goal3"],
    "estimated_reach_potential": "conservative/moderate/aggressive"
  }},
  "platforms": {{
    "instagram": {{
      "posting_schedule": {{
        "frequency": "X posts per week",
        "best_times": ["HH:MM", "HH:MM"],
        "best_days": ["Monday", "Wednesday"],
        "timezone": "UTC",
        "reasoning": "explanation"
      }},
      "content_formats": {{
        "primary_formats": ["Reels", "Carousels"],
        "content_mix": {{"educational": 40, "entertaining": 30, "promotional": 30}},
        "format_notes": "specific recommendations"
      }},
      "hashtag_strategy": {{
        "optimal_count": 15,
        "hashtag_mix": {{"large": 3, "medium": 7, "niche": 5}},
        "branded_hashtags": ["#BrandHashtag1"],
        "campaign_ideas": ["#CampaignHashtag1"]
      }},
      "content_themes": {{
        "weekly_themes": ["Monday Motivation", "Wednesday Tips"],
        "content_pillars": ["pillar1", "pillar2"],
        "seasonal_opportunities": ["Q1 launch", "Summer campaign"]
      }},
      "engagement_tactics": {{
        "tactics": ["Use polls in Stories", "Reply within 1 hour"],
        "cta_recommendations": ["Shop now", "Link in bio"],
        "community_building": ["Host Q&A sessions"]
      }},
      "platform_tips": {{
        "algorithm_optimization": ["Post Reels for maximum reach"],
        "features_to_use": ["Instagram Guides", "Collab posts"],
        "avoid": ["Over-promotion", "Low-quality images"],
        "growth_hacks": ["Leverage trending audio"]
      }}
    }}
  }},
  "cross_platform_strategy": {{
    "content_repurposing": "How to adapt content across platforms",
    "unified_campaigns": "Campaign ideas that work across all platforms",
    "brand_consistency": "How to maintain consistent voice while adapting to each platform"
  }},
  "kpis_to_track": {{
    "primary_metrics": ["engagement_rate", "reach", "follower_growth"],
    "secondary_metrics": ["saves", "shares", "profile_visits"],
    "success_benchmarks": {{"engagement_rate": "3-5%", "reach": "10K per post"}}
  }}
}}

Ensure the strategy is:
- Actionable and specific
- Based on current platform best practices (2024-2025)
- Aligned with the brand's voice and goals
- Realistic and achievable
- Data-driven where possible
"""

QUICK_STRATEGY_PROMPT = """Create a quick content strategy summary for {platform} based on this brand:

Brand Name: {brand_name}
Niche: {niche}
Target Audience: {target_audience}
Brand Voice: {brand_voice}

Provide:
1. Best posting times (3 times)
2. Recommended posting frequency
3. Top 3 content formats
4. 5 hashtag recommendations

Return as JSON:
{{
  "platform": "{platform}",
  "posting_times": ["09:00", "12:00", "19:00"],
  "frequency": "4-5 posts per week",
  "top_formats": ["format1", "format2", "format3"],
  "hashtags": ["#tag1", "#tag2", "#tag3", "#tag4", "#tag5"],
  "quick_tip": "One actionable tip"
}}
"""
