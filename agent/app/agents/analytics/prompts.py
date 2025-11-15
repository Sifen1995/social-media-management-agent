"""
Prompts for Analytics Agent.
"""

ANALYTICS_REPORT_PROMPT = """You are an expert social media analytics specialist. Analyze the following performance data and provide a comprehensive report.

Brand Context:
{brand_context}

Analytics Data:
{analytics_data}

Time Period: {time_period}

Provide a detailed analysis including:
1. Overall performance summary
2. Key metrics and their trends
3. Top performing content and why it succeeded
4. Areas for improvement
5. Platform-specific insights
6. Actionable recommendations

Return your analysis as a JSON object with this structure:
{{
    "summary": "Brief overview of performance",
    "key_metrics": {{
        "total_posts": number,
        "avg_engagement_rate": number,
        "total_reach": number,
        "top_platform": "platform name"
    }},
    "top_content": [
        {{
            "content_id": id,
            "reason": "why it performed well"
        }}
    ],
    "insights": [
        "insight 1",
        "insight 2",
        "..."
    ],
    "recommendations": [
        "recommendation 1",
        "recommendation 2",
        "..."
    ],
    "platform_breakdown": {{
        "platform_name": {{
            "posts": number,
            "avg_engagement": number,
            "insights": "platform-specific insights"
        }}
    }}
}}
"""

TOP_CONTENT_PROMPT = """You are an expert at identifying high-performing social media content.

Brand Context:
{brand_context}

Content Data (sorted by {metric}):
{content_data}

Analyze these top-performing content items and identify patterns:
1. What content types perform best?
2. What topics resonate with the audience?
3. What posting times work best?
4. What caption styles generate engagement?
5. What hashtag strategies are effective?

Return your analysis as a JSON object:
{{
    "patterns": [
        {{
            "pattern": "description",
            "evidence": "supporting data",
            "recommendation": "how to apply this"
        }}
    ],
    "content_type_insights": {{
        "type": "insights"
    }},
    "topic_insights": [
        "topic that resonates"
    ],
    "timing_insights": {{
        "best_days": [],
        "best_hours": []
    }}
}}
"""

INSIGHTS_PROMPT = """You are a social media strategy expert. Generate actionable insights from the analytics data.

Brand Context:
{brand_context}

Recent Performance:
{performance_data}

Historical Trends:
{trends_data}

Competitor Benchmarks (if available):
{competitor_data}

Generate insights covering:
1. Content performance trends
2. Audience engagement patterns
3. Growth opportunities
4. Content gaps
5. Optimization opportunities

Return as JSON:
{{
    "engagement_insights": [
        "insight about engagement"
    ],
    "content_insights": [
        "insight about content"
    ],
    "audience_insights": [
        "insight about audience behavior"
    ],
    "growth_opportunities": [
        "opportunity to explore"
    ],
    "warnings": [
        "potential issues to address"
    ]
}}
"""

TREND_ANALYSIS_PROMPT = """You are a trend analysis expert for social media.

Brand Context:
{brand_context}

Keywords to track: {keywords}
Competitors to monitor: {competitors}

Industry Trends:
{industry_trends}

Recent viral content in niche:
{viral_content}

Analyze current trends and provide:
1. Trending topics in the brand's niche
2. Emerging content formats
3. Hashtag trends
4. Competitor strategies
5. Opportunities to capitalize on trends

Return as JSON:
{{
    "trending_topics": [
        {{
            "topic": "name",
            "relevance": "why it matters",
            "how_to_use": "application strategy"
        }}
    ],
    "trending_formats": [
        "format description"
    ],
    "trending_hashtags": [
        "#hashtag"
    ],
    "competitor_insights": [
        "what competitors are doing well"
    ],
    "recommendations": [
        "how to leverage these trends"
    ]
}}
"""
