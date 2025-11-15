"""
Prompts for Social Listening Agent.
"""

MONITOR_TRENDS_PROMPT = """You are a social media trend monitoring specialist.

Brand Context:
{brand_context}

Industry/Niche: {niche}
Target Keywords: {keywords}

Recent Social Media Activity:
{social_activity}

Trending Hashtags:
{trending_hashtags}

Analyze current trends and provide:
1. Emerging trends relevant to the brand
2. Popular topics in the niche
3. Trending hashtags worth using
4. Content opportunities
5. Threats or challenges

Return as JSON:
{{
    "trending_topics": [
        {{
            "topic": "name",
            "volume": "trend volume/momentum",
            "relevance_score": 0-100,
            "why_relevant": "explanation",
            "how_to_leverage": "strategy",
            "urgency": "low/medium/high",
            "expected_lifespan": "how long trend will last"
        }}
    ],
    "trending_hashtags": [
        {{
            "hashtag": "#tag",
            "usage_count": number,
            "trend_direction": "rising/falling/stable",
            "relevance": "why it matters"
        }}
    ],
    "content_opportunities": [
        "opportunity description"
    ],
    "warnings": [
        "trends or topics to avoid"
    ],
    "recommendations": [
        "strategic recommendations"
    ]
}}
"""

COMPETITOR_ANALYSIS_PROMPT = """You are a competitive intelligence analyst for social media.

Brand Context:
{brand_context}

Competitors to Monitor:
{competitors}

Competitor Activity:
{competitor_activity}

Their Top Performing Content:
{competitor_top_content}

Analyze competitors and provide:
1. What content strategies are they using?
2. What's working well for them?
3. What gaps exist in their strategy?
4. Opportunities to differentiate
5. Best practices to adopt

Return as JSON:
{{
    "competitor_insights": [
        {{
            "competitor": "name",
            "strengths": ["strength 1", "strength 2"],
            "weaknesses": ["weakness 1", "weakness 2"],
            "content_strategy": "description",
            "engagement_level": "high/medium/low",
            "successful_tactics": ["tactic 1", "tactic 2"],
            "posting_frequency": "analysis"
        }}
    ],
    "opportunities": [
        {{
            "opportunity": "description",
            "why": "explanation",
            "how_to_capitalize": "strategy"
        }}
    ],
    "differentiation_strategies": [
        "how to stand out from competitors"
    ],
    "best_practices_to_adopt": [
        "what to learn from competitors"
    ],
    "market_gaps": [
        "unmet needs or content gaps"
    ]
}}
"""

BRAND_MENTIONS_PROMPT = """You are monitoring brand mentions across social media.

Brand: {brand_name}
Monitoring Keywords: {keywords}

Recent Mentions:
{mentions}

Analyze these mentions and provide:
1. Sentiment distribution
2. Key themes or topics
3. Influential mentions
4. Opportunities for engagement
5. Potential issues or crises

Return as JSON:
{{
    "mention_summary": {{
        "total_mentions": number,
        "sentiment_breakdown": {{
            "positive": number,
            "negative": number,
            "neutral": number
        }},
        "reach_estimate": number,
        "trend": "increasing/decreasing/stable"
    }},
    "key_themes": [
        {{
            "theme": "topic",
            "mention_count": number,
            "sentiment": "overall sentiment",
            "significance": "why it matters"
        }}
    ],
    "influential_mentions": [
        {{
            "user": "username",
            "platform": "platform",
            "content": "what they said",
            "reach": "follower count or reach",
            "sentiment": "positive/negative/neutral",
            "action_needed": "suggested response or action"
        }}
    ],
    "engagement_opportunities": [
        "opportunities to engage with mentions"
    ],
    "crisis_alerts": [
        "potential issues requiring immediate attention"
    ],
    "recommendations": [
        "strategic recommendations based on mentions"
    ]
}}
"""

AUDIENCE_INSIGHTS_PROMPT = """You are analyzing audience behavior and interests.

Brand Context:
{brand_context}

Audience Data:
{audience_data}

Engagement Patterns:
{engagement_patterns}

Common Questions/Concerns:
{common_topics}

Provide insights about:
1. What the audience cares about
2. Content preferences
3. Pain points and needs
4. Engagement patterns
5. Content gaps to fill

Return as JSON:
{{
    "audience_interests": [
        {{
            "interest": "topic or category",
            "strength": "how strong the interest is",
            "evidence": "supporting data",
            "content_ideas": ["idea 1", "idea 2"]
        }}
    ],
    "content_preferences": {{
        "preferred_formats": ["format 1", "format 2"],
        "preferred_topics": ["topic 1", "topic 2"],
        "preferred_tone": "description",
        "best_engagement_triggers": ["trigger 1", "trigger 2"]
    }},
    "pain_points": [
        {{
            "pain_point": "description",
            "frequency": "how often mentioned",
            "content_solution": "how to address this"
        }}
    ],
    "engagement_patterns": {{
        "most_active_times": ["time 1", "time 2"],
        "most_engaged_content_types": ["type 1", "type 2"],
        "engagement_triggers": ["what drives engagement"]
    }},
    "content_gaps": [
        "topics or needs not being addressed"
    ],
    "recommendations": [
        "strategic recommendations"
    ]
}}
"""

VIRAL_CONTENT_ANALYSIS_PROMPT = """You are analyzing viral content in the brand's niche.

Brand Context:
{brand_context}

Viral Content Examples:
{viral_content}

Analyze what made this content viral:
1. Common patterns and elements
2. Emotional triggers used
3. Format and style
4. Timing factors
5. How to apply these lessons

Return as JSON:
{{
    "viral_patterns": [
        {{
            "pattern": "description",
            "frequency": "how often this pattern appears",
            "examples": ["example 1", "example 2"],
            "how_to_apply": "application strategy"
        }}
    ],
    "emotional_triggers": [
        {{
            "trigger": "emotion or hook",
            "effectiveness": "why it works",
            "usage_guide": "how to use it authentically"
        }}
    ],
    "format_insights": {{
        "successful_formats": ["format 1", "format 2"],
        "optimal_length": "content length insights",
        "visual_elements": "visual patterns",
        "copy_style": "writing style insights"
    }},
    "timing_factors": [
        "insights about when content went viral"
    ],
    "actionable_takeaways": [
        "specific things to implement"
    ],
    "warnings": [
        "what to avoid when trying to create viral content"
    ]
}}
"""

CRISIS_DETECTION_PROMPT = """You are monitoring for potential PR crises or brand issues.

Brand Context:
{brand_context}

Recent Activity:
{recent_activity}

Sentiment Trends:
{sentiment_trends}

Monitor for:
1. Sudden negative sentiment spikes
2. Controversial mentions
3. Misinformation spread
4. Customer complaints escalating
5. Coordinated negative campaigns

Return as JSON:
{{
    "crisis_level": "none/low/medium/high/critical",
    "alerts": [
        {{
            "type": "sentiment_spike/controversy/misinformation/complaint/attack",
            "severity": "low/medium/high/critical",
            "description": "what's happening",
            "evidence": "supporting data",
            "potential_impact": "possible consequences",
            "recommended_action": "immediate action to take",
            "urgency": "how quickly to respond"
        }}
    ],
    "sentiment_analysis": {{
        "current_sentiment": "overall sentiment",
        "trend": "improving/declining/stable",
        "concerning_patterns": ["pattern 1", "pattern 2"]
    }},
    "risk_assessment": {{
        "current_risk_level": "low/medium/high",
        "escalation_probability": 0-100,
        "factors": ["contributing factors"]
    }},
    "response_plan": [
        "recommended steps to address the situation"
    ]
}}
"""
