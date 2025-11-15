"""
Prompts for Scheduler Agent.
"""

CREATE_CALENDAR_PROMPT = """You are an expert social media scheduling strategist.

Brand Context:
{brand_context}

Content to Schedule:
{content_items}

Scheduling Parameters:
- Duration: {duration_days} days
- Platforms: {platforms}
- Posts per week: {posts_per_week}
- Start date: {start_date}
- Timezone: {timezone}

Historical Performance Data:
{performance_data}

Create an optimal content calendar that:
1. Distributes content evenly across the time period
2. Posts at optimal times for each platform
3. Avoids posting too frequently (minimum 4-hour gaps)
4. Considers audience activity patterns
5. Balances content types and topics

Return as JSON:
{{
    "calendar": [
        {{
            "content_id": id,
            "scheduled_time": "ISO datetime",
            "platform": "platform name",
            "reason": "why this time slot"
        }}
    ],
    "summary": {{
        "total_posts": number,
        "posts_per_platform": {{}},
        "coverage": "how well the calendar covers the period"
    }},
    "recommendations": [
        "additional scheduling recommendations"
    ]
}}
"""

OPTIMAL_TIMES_PROMPT = """You are an expert at determining optimal posting times for social media.

Brand Context:
{brand_context}

Platform: {platform}
Target Audience: {target_audience}
Timezone: {timezone}

Historical Performance:
{historical_data}

Audience Demographics:
{demographics}

Determine the best times to post considering:
1. When the target audience is most active
2. Platform-specific best practices
3. Historical performance data
4. Time zone considerations
5. Day of week patterns

Return as JSON:
{{
    "optimal_times": [
        {{
            "day": "day of week",
            "time": "HH:MM",
            "timezone": "timezone",
            "reason": "why this time is optimal",
            "expected_reach": "estimate"
        }}
    ],
    "avoid_times": [
        {{
            "day": "day",
            "time": "HH:MM",
            "reason": "why to avoid"
        }}
    ],
    "recommendations": [
        "timing strategy recommendations"
    ]
}}
"""

SCHEDULE_CONTENT_PROMPT = """You are scheduling {count} pieces of content for {platform}.

Brand Context:
{brand_context}

Content Items:
{content_items}

Constraints:
- Already scheduled content: {existing_schedule}
- Minimum gap between posts: {min_gap_hours} hours
- Preferred posting times: {preferred_times}
- Avoid posting on: {blackout_dates}

Create a schedule that:
1. Respects existing scheduled content
2. Maintains minimum gaps
3. Uses optimal posting times
4. Spreads content evenly
5. Considers content priority/type

Return as JSON:
{{
    "schedule": [
        {{
            "content_id": id,
            "scheduled_for": "ISO datetime",
            "rationale": "scheduling decision explanation"
        }}
    ],
    "conflicts": [
        "any scheduling conflicts encountered"
    ],
    "notes": [
        "important scheduling notes"
    ]
}}
"""

RESCHEDULING_PROMPT = """You need to reschedule content due to: {reason}

Current Schedule:
{current_schedule}

Content to Reschedule:
{content_to_reschedule}

Constraints:
{constraints}

Create a new schedule that:
1. Minimizes disruption to other scheduled content
2. Maintains content distribution quality
3. Respects platform best practices
4. Considers urgency/priority

Return as JSON:
{{
    "new_schedule": [
        {{
            "content_id": id,
            "old_time": "ISO datetime",
            "new_time": "ISO datetime",
            "reason": "why moved to this time"
        }}
    ],
    "impact_analysis": {{
        "posts_affected": number,
        "distribution_quality": "assessment"
    }},
    "recommendations": [
        "suggestions for preventing similar issues"
    ]
}}
"""
