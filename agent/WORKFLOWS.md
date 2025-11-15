# System Workflows and Integration Guide

## 📋 Table of Contents
1. [Complete System Workflow](#complete-system-workflow)
2. [Agent Interaction Patterns](#agent-interaction-patterns)
3. [Data Flow](#data-flow)
4. [Integration Examples](#integration-examples)
5. [Error Handling](#error-handling)

---

## Complete System Workflow

### End-to-End Content Generation and Publishing

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Request                              │
│  "Create 5 Instagram posts about eco-fashion and schedule them" │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    API Layer (FastAPI)                           │
│  POST /api/v1/content/plan-and-execute                          │
│  {                                                               │
│    "brand_id": 1,                                               │
│    "user_request": "Create 5 Instagram posts..."               │
│  }                                                               │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Planner Agent                                  │
│                                                                   │
│  1. Parse user request                                          │
│  2. Identify required actions:                                  │
│     - Generate content (Content Agent)                          │
│     - Create schedule (Scheduler Agent)                         │
│  3. Create execution plan                                       │
│                                                                   │
│  Plan Output:                                                   │
│  {                                                               │
│    "execution_plan": [                                          │
│      {                                                           │
│        "step": 1,                                               │
│        "agent": "content",                                      │
│        "action": "generate 5 Instagram posts...",              │
│        "parameters": {...}                                      │
│      },                                                          │
│      {                                                           │
│        "step": 2,                                               │
│        "agent": "scheduler",                                    │
│        "action": "schedule generated content",                 │
│        "parameters": {...}                                      │
│      }                                                           │
│    ]                                                             │
│  }                                                               │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                 Agent Orchestrator                               │
│  Executes each step in sequence:                                │
└────────────────────────┬────────────────────────────────────────┘
                         │
         ┌───────────────┴───────────────┐
         │                               │
         ▼                               ▼
┌─────────────────────┐         ┌─────────────────────┐
│   Content Agent     │         │  Scheduler Agent    │
│                     │         │                     │
│ 1. Load brand voice │         │ 1. Get content IDs  │
│ 2. Generate with    │         │ 2. Determine        │
│    LLM (GPT-4/      │         │    optimal times    │
│    Claude)          │         │ 3. Create schedule  │
│ 3. Create hashtags  │         │ 4. Update DB        │
│ 4. Add CTAs         │         │                     │
│ 5. Save to DB       │         │                     │
│                     │         │                     │
│ Returns: [          │         │ Returns: {          │
│   {id: 1, ...},    │         │   "scheduled": [...] │
│   {id: 2, ...},    │         │ }                   │
│   ...              │         │                     │
│ ]                   │         │                     │
└─────────────────────┘         └─────────────────────┘
         │                               │
         └───────────────┬───────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              Orchestrator Aggregates Results                     │
│  {                                                               │
│    "step_1_result": [...content items...],                     │
│    "step_2_result": {...schedule...}                           │
│  }                                                               │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                API Returns Response to User                      │
│  {                                                               │
│    "success": true,                                             │
│    "message": "Request processed successfully",                │
│    "data": {                                                    │
│      "plan": {...},                                             │
│      "execution_results": [...]                                │
│    }                                                             │
│  }                                                               │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              Background: Celery Scheduler                        │
│                                                                   │
│  Every minute:                                                  │
│  1. Check for content where scheduled_for <= now                │
│  2. Get social account credentials                              │
│  3. Call platform integration (Instagram, Twitter, etc.)        │
│  4. Post content                                                │
│  5. Update status to "published"                                │
│  6. Store platform_post_id                                      │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│         Platform Integration (e.g., Instagram)                   │
│                                                                   │
│  1. Validate access token                                       │
│  2. Create media container                                      │
│  3. Publish to Instagram                                        │
│  4. Return post_id and permalink                                │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│           Content Successfully Published! ✅                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Agent Interaction Patterns

### Pattern 1: Single Agent Execution

```python
# User wants to generate content only
request = {
    "brand_id": 1,
    "platform": "instagram",
    "topic": "summer fashion",
    "count": 3
}

# API routes directly to Content Agent
orchestrator.execute_task("content", task, context)
```

### Pattern 2: Sequential Multi-Agent

```python
# Step 1: Content Agent generates posts
# Step 2: Scheduler Agent creates calendar
# Step 3: Analytics Agent provides recommendations

workflow = [
    {"agent": "content", "task": {...}},
    {"agent": "scheduler", "task": {...}},
    {"agent": "analytics", "task": {...}}
]

orchestrator.execute_workflow(workflow, context)
```

### Pattern 3: Planner-Driven Execution

```python
# User submits natural language request
# Planner decomposes and coordinates

orchestrator.delegate_to_planner(
    user_request="Create a content strategy for next month",
    context=brand_context
)

# Planner decides which agents to use and in what order
```

---

## Data Flow

### Database Interaction Flow

```
User Creates Brand
        ↓
    [brands table]
        ↓
User Connects Social Accounts
        ↓
    [social_accounts table] (with encrypted tokens)
        ↓
Content Agent Generates Content
        ↓
    [content_items table] (status: draft)
        ↓
Scheduler Agent Schedules Content
        ↓
    [content_items table] (status: scheduled, scheduled_for: timestamp)
        ↓
Celery Task Publishes Content
        ↓
    [content_items table] (status: published, platform_post_id: xxx)
        ↓
Analytics Fetched Daily
        ↓
    [analytics_data table] (likes, comments, reach, etc.)
        ↓
Analytics Agent Analyzes Data
        ↓
Insights Returned to User
```

### LLM Interaction Flow

```
Agent needs AI generation
        ↓
LLMService.generate_completion()
        ↓
    [Check LLM_PROVIDER config]
        ↓
    ┌─────────────┬─────────────┐
    ▼             ▼             ▼
OpenAI API   Anthropic API   Future Provider
(GPT-4)      (Claude)
    ↓             ↓             ↓
    └─────────────┴─────────────┘
        ↓
Format and return response
        ↓
Agent processes result
        ↓
Save to database
```

---

## Integration Examples

### Example 1: Complete Content Creation Workflow

```python
from app.agents.base.orchestrator import orchestrator

async def create_campaign():
    """Create a complete social media campaign."""

    context = {
        "brand": {
            "id": 1,
            "name": "EcoWear",
            "niche": "sustainable fashion",
            "brand_voice": "inspiring, eco-conscious, authentic",
            "target_audience": "millennials interested in sustainability",
            "goals": ["increase engagement", "drive website traffic"]
        }
    }

    # Step 1: Generate content
    content_task = {
        "platform": "instagram",
        "action": "generate",
        "topic": "sustainable summer fashion",
        "content_type": "post",
        "count": 5
    }

    content_result = await orchestrator.execute_task(
        "content",
        content_task,
        context
    )

    # Step 2: Create calendar
    scheduler_task = {
        "action": "create_calendar",
        "duration_days": 7,
        "platforms": ["instagram"],
        "posts_per_week": 5
    }

    calendar_result = await orchestrator.execute_task(
        "scheduler",
        scheduler_task,
        context
    )

    # Step 3: Get optimization suggestions
    optimizer_task = {
        "action": "optimize_timing",
        "content_ids": [item["id"] for item in content_result["data"]]
    }

    # Return complete campaign plan
    return {
        "content": content_result,
        "calendar": calendar_result,
        "optimization": "Applied best practices"
    }
```

### Example 2: Analytics-Driven Content Strategy

```python
async def analyze_and_recommend():
    """Analyze past performance and recommend strategy."""

    context = {"brand_id": 1}

    # Step 1: Get analytics
    analytics_task = {
        "action": "report",
        "time_period": "last_30_days"
    }

    analytics_result = await orchestrator.execute_task(
        "analytics",
        analytics_task,
        context
    )

    # Step 2: Get top performing content
    top_content_task = {
        "action": "top_content",
        "limit": 10
    }

    top_content = await orchestrator.execute_task(
        "analytics",
        top_content_task,
        context
    )

    # Step 3: Generate similar content
    content_task = {
        "platform": "instagram",
        "action": "generate",
        "topic": "Based on top performers",
        "count": 5,
        "requirements": f"Similar to: {top_content['data']}"
    }

    new_content = await orchestrator.execute_task(
        "content",
        content_task,
        context
    )

    return {
        "insights": analytics_result,
        "top_content": top_content,
        "new_content": new_content
    }
```

### Example 3: Automated Engagement Management

```python
async def manage_community_engagement():
    """Handle comments and DMs automatically."""

    # Fetch pending engagement items from database
    pending_items = fetch_pending_engagement()

    context = {"brand": get_brand_context()}

    for item in pending_items:
        # Generate reply suggestion
        engagement_task = {
            "action": "reply",
            "message_type": item.type,  # comment, dm, mention
            "content": item.content,
            "username": item.username
        }

        reply_result = await orchestrator.execute_task(
            "engagement",
            engagement_task,
            context
        )

        # Save suggested reply for human review
        save_suggested_reply(item.id, reply_result["data"])

    return {"processed": len(pending_items)}
```

---

## Error Handling

### Agent-Level Error Handling

```python
# Each agent returns standardized result
{
    "success": bool,
    "data": any,
    "message": str,
    "metadata": {
        "error_type": str (if failed),
        "error_details": str (if failed)
    },
    "agent": str,
    "timestamp": str
}
```

### Workflow Error Handling

```python
# Critical steps can halt workflow
workflow = [
    {
        "agent": "content",
        "task": {...},
        "critical": True  # If this fails, stop workflow
    },
    {
        "agent": "scheduler",
        "task": {...},
        "critical": False  # Can fail without stopping
    }
]
```

### Platform Integration Error Handling

```python
try:
    result = await instagram_client.post_content(content)
except AuthenticationError:
    # Token expired, refresh needed
    handle_token_refresh()
except RateLimitError:
    # Hit API limit, queue for later
    queue_for_retry(content)
except Exception as e:
    # Unknown error, log and alert
    log_error(e)
    alert_admin()
```

---

## Performance Considerations

### Caching Strategy

- Brand context cached in Redis
- LLM responses cached for identical requests
- Analytics data cached for 1 hour

### Rate Limiting

- Instagram: 200 requests/hour per user
- Twitter: 300 requests/15 min
- Implement queue system for high-volume posting

### Scaling

- Horizontal scaling: Multiple Uvicorn workers
- Celery workers: Scale independently
- Database: Read replicas for analytics queries

---

## Monitoring and Observability

### Key Metrics to Track

1. **Agent Performance**
   - Execution time per agent
   - Success/failure rates
   - LLM token usage

2. **Content Performance**
   - Publishing success rate
   - Average engagement per platform
   - Content generation quality (user ratings)

3. **System Health**
   - API response times
   - Database query performance
   - Celery queue depth

### Logging Strategy

```python
# Structured logging at each level
logger.info("Content generated", extra={
    "brand_id": 1,
    "platform": "instagram",
    "agent": "content",
    "count": 5,
    "execution_time_ms": 2500
})
```

---

## Security Considerations

1. **Token Security**
   - All social media tokens encrypted at rest
   - Tokens never logged
   - Automatic token refresh

2. **API Security**
   - JWT authentication on all endpoints
   - Rate limiting per user
   - Input validation with Pydantic

3. **LLM Safety**
   - Content filtering for brand safety
   - Prompt injection protection
   - Output validation

---

This workflow documentation provides a complete picture of how all components work together to create a fully autonomous social media management system.
