"""
Prompts for Optimizer Agent.
"""

AB_TEST_DESIGN_PROMPT = """You are an A/B testing specialist for social media content.

Brand Context:
{brand_context}

Content to Test:
{content}

Testing Goal: {goal}

Design an A/B test that:
1. Identifies what variables to test
2. Creates variations
3. Defines success metrics
4. Estimates required sample size
5. Provides implementation guidelines

Return as JSON:
{{
    "test_design": {{
        "hypothesis": "what we're testing",
        "variables_to_test": ["variable 1", "variable 2"],
        "success_metrics": ["metric 1", "metric 2"],
        "duration": "recommended test duration",
        "sample_size": "required posts/audience size"
    }},
    "variations": [
        {{
            "version": "A/B/C",
            "changes": "what's different",
            "content": "the variation",
            "expected_impact": "predicted outcome"
        }}
    ],
    "implementation_guide": [
        "step-by-step implementation instructions"
    ],
    "success_criteria": {{
        "primary_metric": "main metric to watch",
        "threshold": "what indicates success",
        "secondary_metrics": ["metric 1", "metric 2"]
    }},
    "risks": [
        "potential risks or considerations"
    ]
}}
"""

CONTENT_OPTIMIZATION_PROMPT = """You are a content optimization specialist.

Content Item:
{content}

Performance Data:
{performance_data}

Similar High-Performing Content:
{top_content}

Brand Context:
{brand_context}

Analyze this content and provide optimization recommendations:
1. What's working well?
2. What could be improved?
3. Specific changes to make
4. Expected impact
5. Priority level for each recommendation

Return as JSON:
{{
    "current_assessment": {{
        "strengths": ["strength 1", "strength 2"],
        "weaknesses": ["weakness 1", "weakness 2"],
        "overall_score": 0-100,
        "potential_improvement": "estimated percentage improvement"
    }},
    "recommendations": [
        {{
            "category": "caption/hashtags/timing/visual/cta",
            "current": "current state",
            "recommended": "suggested change",
            "reasoning": "why this change",
            "expected_impact": "predicted improvement",
            "priority": "high/medium/low",
            "effort": "low/medium/high"
        }}
    ],
    "optimized_version": {{
        "caption": "optimized caption",
        "hashtags": ["optimized hashtags"],
        "posting_time": "optimal time",
        "other_changes": {{"key": "value"}}
    }},
    "quick_wins": [
        "easy changes with high impact"
    ],
    "long_term_improvements": [
        "strategic improvements over time"
    ]
}}
"""

TIMING_OPTIMIZATION_PROMPT = """You are a posting time optimization specialist.

Brand Context:
{brand_context}

Platform: {platform}

Historical Performance by Time:
{time_performance}

Audience Activity Patterns:
{audience_patterns}

Current Posting Schedule:
{current_schedule}

Optimize the posting schedule:
1. Identify best performing times
2. Recommend schedule changes
3. Estimate impact of changes
4. Consider content type variations

Return as JSON:
{{
    "current_performance": {{
        "avg_engagement_rate": number,
        "best_performing_times": ["time 1", "time 2"],
        "worst_performing_times": ["time 1", "time 2"]
    }},
    "optimized_schedule": [
        {{
            "day": "day of week",
            "time": "HH:MM",
            "timezone": "timezone",
            "expected_engagement": "estimated rate",
            "confidence": 0-100,
            "content_type": "what to post at this time"
        }}
    ],
    "schedule_changes": [
        {{
            "change": "description of change",
            "from": "old time",
            "to": "new time",
            "expected_impact": "percentage improvement",
            "reasoning": "why this change"
        }}
    ],
    "expected_results": {{
        "engagement_improvement": "percentage",
        "reach_improvement": "percentage",
        "optimal_posting_frequency": "posts per week"
    }},
    "recommendations": [
        "strategic timing recommendations"
    ]
}}
"""

HASHTAG_OPTIMIZATION_PROMPT = """You are a hashtag strategy optimization specialist.

Brand Context:
{brand_context}

Platform: {platform}

Current Hashtags:
{current_hashtags}

Hashtag Performance Data:
{performance_data}

Trending Hashtags:
{trending_hashtags}

Optimize the hashtag strategy:
1. Analyze current hashtag performance
2. Identify underperforming hashtags
3. Recommend new hashtags
4. Create hashtag sets for different content types
5. Provide usage guidelines

Return as JSON:
{{
    "current_analysis": {{
        "total_hashtags": number,
        "avg_performance": "metric",
        "best_performing": [
            {{
                "hashtag": "#tag",
                "performance": "metrics",
                "why_it_works": "explanation"
            }}
        ],
        "underperforming": ["#tag1", "#tag2"]
    }},
    "recommended_hashtags": [
        {{
            "hashtag": "#tag",
            "category": "niche/trending/branded/community",
            "size": "small/medium/large",
            "competition": "low/medium/high",
            "relevance_score": 0-100,
            "expected_reach": "estimate",
            "why_recommended": "reasoning"
        }}
    ],
    "hashtag_sets": {{
        "content_type": [
            {{
                "name": "set name",
                "hashtags": ["#tag1", "#tag2"],
                "purpose": "when to use",
                "expected_performance": "estimate"
            }}
        ]
    }},
    "hashtags_to_remove": [
        {{
            "hashtag": "#tag",
            "reason": "why to remove"
        }}
    ]],
    "strategy_recommendations": [
        "overall hashtag strategy recommendations"
    ],
    "best_practices": [
        "platform-specific best practices"
    ]
}}
"""

CAPTION_OPTIMIZATION_PROMPT = """You are a caption optimization specialist.

Content Caption:
{caption}

Platform: {platform}

Brand Voice: {brand_voice}

Performance Context:
{performance_context}

Top Performing Captions:
{top_captions}

Optimize this caption:
1. Improve engagement potential
2. Strengthen CTA
3. Enhance readability
4. Optimize length
5. Improve hook

Return as JSON:
{{
    "current_analysis": {{
        "length": number,
        "readability_score": 0-100,
        "engagement_potential": 0-100,
        "has_cta": boolean,
        "has_hook": boolean,
        "tone_match": "how well it matches brand voice",
        "issues": ["issue 1", "issue 2"]
    }},
    "optimized_caption": "the improved caption",
    "variations": [
        {{
            "version": "version name",
            "caption": "variation text",
            "focus": "what this variation optimizes for",
            "expected_performance": "prediction"
        }}
    ],
    "specific_improvements": [
        {{
            "element": "hook/body/cta/emoji/spacing",
            "original": "original text",
            "improved": "improved text",
            "reasoning": "why this is better"
        }}
    ],
    "a_b_test_suggestion": {{
        "test_these": "elements to test",
        "versions": ["version A", "version B"],
        "metric_to_watch": "what to measure"
    }},
    "general_tips": [
        "caption writing tips for this brand"
    ]
}}
"""

PERFORMANCE_PREDICTION_PROMPT = """You are a content performance prediction specialist.

Content to Predict:
{content}

Platform: {platform}

Historical Performance Data:
{historical_data}

Similar Content Performance:
{similar_content}

Current Trends:
{trends}

Predict the performance of this content:
1. Estimated engagement metrics
2. Confidence level
3. Factors affecting performance
4. Risk assessment
5. Optimization opportunities before posting

Return as JSON:
{{
    "prediction": {{
        "estimated_likes": number,
        "estimated_comments": number,
        "estimated_shares": number,
        "estimated_reach": number,
        "estimated_engagement_rate": number,
        "confidence_level": 0-100,
        "performance_tier": "low/medium/high/viral"
    }},
    "factors": {{
        "positive_factors": [
            {{
                "factor": "what's good",
                "impact": "how much it helps",
                "weight": 0-100
            }}
        ],
        "negative_factors": [
            {{
                "factor": "what's limiting",
                "impact": "how much it hurts",
                "weight": 0-100
            }}
        ]
    }},
    "risk_assessment": {{
        "risk_level": "low/medium/high",
        "risks": ["risk 1", "risk 2"],
        "mitigation": ["how to reduce risk"]
    }},
    "pre_post_optimizations": [
        {{
            "change": "suggested improvement",
            "expected_impact": "prediction improvement",
            "priority": "high/medium/low"
        }}
    ],
    "best_case_scenario": {{
        "metrics": {{}},
        "likelihood": "percentage"
    }},
    "worst_case_scenario": {{
        "metrics": {{}},
        "likelihood": "percentage"
    }}
}}
"""
