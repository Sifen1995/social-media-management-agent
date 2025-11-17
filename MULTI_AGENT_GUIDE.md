# Multi-Agent Social Media Management System

## Overview

This enhanced system extends the original social media management agent into a comprehensive multi-agent pipeline that automates the entire content lifecycle from brand research to multi-platform posting.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Agent Orchestrator                        │
│              (Coordinates all agents)                        │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│Brand Profile │   │  Strategy    │   │   Content    │
│    Agent     │──▶│    Agent     │──▶│    Agent     │
└──────────────┘   └──────────────┘   └──────────────┘
        │                                       │
        │                   ┌───────────────────┘
        │                   │
        ▼                   ▼
┌──────────────┐   ┌──────────────┐
│  Graphics    │   │   Poster     │
│    Agent     │   │    Agent     │
└──────────────┘   └──────────────┘
```

## Core Agents

### 1. Brand Profile Agent (✓ Already Existed)
**Location:** `agent/app/agents/brand_profile/`

**Purpose:** Automatically researches and creates comprehensive brand profiles from website and social media data.

**Capabilities:**
- Scrapes company websites (BeautifulSoup4 + Playwright)
- Extracts social media bios and profiles
- Uses LLM to analyze and structure brand information
- Generates `company_profile.json`

**Input:**
```python
{
  "website": "https://company.com",
  "socials": {
    "instagram": "https://instagram.com/company",
    "linkedin": "https://linkedin.com/company/company"
  }
}
```

**Output:**
```json
{
  "brand_name": "Company Name",
  "overview": "Brief description...",
  "mission": "Mission statement...",
  "tone_voice": "professional, friendly",
  "target_audience": "Tech-savvy millennials",
  "products_services": ["Product 1", "Product 2"],
  "brand_values": ["Innovation", "Quality"],
  "competitors": ["Competitor 1"],
  "source_urls": {...}
}
```

### 2. Strategy Agent (✓ NEW)
**Location:** `agent/app/agents/strategy/`

**Purpose:** Analyzes brand profiles and generates platform-specific content strategies.

**Capabilities:**
- Multi-platform strategy generation (Instagram, Facebook, Twitter, LinkedIn, TikTok)
- Posting schedule optimization
- Content format recommendations
- Hashtag strategy development
- Engagement tactic suggestions
- Platform-specific best practices

**Input:**
```python
{
  "brand_profile": {...},
  "platforms": ["instagram", "linkedin", "tiktok"],
  "mode": "comprehensive"  # or "quick"
}
```

**Output:** `strategy_plan.json`
```json
{
  "strategy_overview": {
    "brand_voice_alignment": "...",
    "target_audience_focus": "...",
    "primary_goals": ["engagement", "reach", "growth"]
  },
  "platforms": {
    "instagram": {
      "posting_schedule": {
        "frequency": "4-5 posts per week",
        "best_times": ["09:00", "12:00", "19:00"],
        "best_days": ["Monday", "Wednesday", "Friday"]
      },
      "content_formats": {
        "primary_formats": ["Reels", "Carousels"],
        "content_mix": {"educational": 40, "entertaining": 30, "promotional": 30}
      },
      "hashtag_strategy": {...},
      "engagement_tactics": {...},
      "platform_tips": {...}
    }
  }
}
```

### 3. Content Agent (✓ Enhanced)
**Location:** `agent/app/agents/content/`

**Purpose:** Generates platform-optimized content using brand profile and strategy data.

**Enhancements:**
- ✓ Now uses `company_profile.json` for brand alignment
- ✓ Integrates `strategy_plan.json` for optimal content generation
- ✓ Generates multiple style variations (formal, casual, promotional)
- ✓ Creates hooks, CTAs, and platform-optimized captions
- ✓ Strategic hashtag recommendations

**Input:**
```python
{
  "platform": "instagram",
  "action": "generate",
  "topic": "Product launch",
  "content_type": "post",
  "count": 3,
  "brand_profile": {...},
  "strategy_plan": {...}
}
```

**Output:** `content_batch.json`
```json
[
  {
    "variation": 1,
    "style": "Formal & Professional",
    "hook": "Attention-grabbing opener...",
    "caption": "Full post caption...",
    "hashtags": ["#brand", "#industry", "#trending"],
    "cta": "Call to action...",
    "content_format": "Reel",
    "estimated_engagement": "high",
    "strategy_alignment": "Aligns with educational content pillar"
  }
]
```

### 4. Graphics Agent (✓ NEW)
**Location:** `agent/app/agents/graphics/`

**Purpose:** Generates graphic asset specifications for social media content.

**Capabilities:**
- Creates detailed graphic design specifications
- Optimizes dimensions for each platform
- Maintains brand consistency (colors, fonts, style)
- Generates image generation prompts
- Provides Canva template suggestions
- Manual creation guides

**Input:**
```python
{
  "content": {...},
  "platform": "instagram",
  "mode": "specification",  # or "generate" with image API
  "brand_profile": {...}
}
```

**Output:** `assets/graphics_metadata.json`
```json
{
  "graphic_id": "ig_post_001",
  "platform": "instagram",
  "dimensions": {"width": 1080, "height": 1080},
  "color_scheme": {
    "background": "#FFFFFF",
    "primary": "#2C3E50",
    "accent": "#3498DB"
  },
  "typography": {...},
  "visual_elements": {...},
  "image_generation_prompt": "Detailed prompt for AI image gen...",
  "canva_template_suggestion": "Social media post - Modern"
}
```

### 5. Poster Agent (✓ NEW)
**Location:** `agent/app/agents/poster/`

**Purpose:** Automates content posting across multiple platforms.

**Capabilities:**
- Multi-platform posting (Instagram, Facebook, Twitter, LinkedIn, TikTok, YouTube)
- Content validation before posting
- Retry logic and error handling
- Queue management
- Scheduled posting support
- Status tracking and reporting

**Platform Integration:**
- ✓ Instagram - via Instagram Graph API
- ✓ Facebook - via Facebook Graph API
- ✓ Twitter - via Twitter API v2
- ✓ LinkedIn - via LinkedIn API
- ✓ TikTok - via TikTok API
- ✓ YouTube - via YouTube Data API

**Input:**
```python
{
  "content": [...],  # Batch or single content
  "platforms": ["instagram", "linkedin"],
  "credentials": {
    "instagram": {"access_token": "..."},
    "linkedin": {"access_token": "..."}
  },
  "mode": "post"  # or "validate", "schedule"
}
```

**Output:**
```json
{
  "posting_results": {
    "instagram": {
      "success": true,
      "post_id": "123456",
      "permalink": "https://instagram.com/p/...",
      "platform": "instagram"
    },
    "linkedin": {...}
  },
  "successful_platforms": ["instagram"],
  "failed_platforms": [],
  "posted_at": "2024-11-17T10:30:00Z"
}
```

## Complete Pipeline Workflow

### Automated Pipeline

The orchestrator provides `execute_complete_pipeline()` method that runs all steps:

```python
from app.agents.base.orchestrator import orchestrator

# Initialize agents (one-time setup)
# ... register all agents ...

# Run complete pipeline
results = await orchestrator.execute_complete_pipeline(
    website_url="https://company.com",
    social_links={
        "instagram": "https://instagram.com/company",
        "linkedin": "https://linkedin.com/company/company"
    },
    platforms=["instagram", "linkedin", "tiktok"],
    content_topics=[
        "Product launch",
        "Customer success story",
        "Industry insights"
    ],
    mode="generate_only"  # or "schedule", "post"
)
```

### Pipeline Stages

1. **Brand Research** → `company_profile.json`
2. **Strategy Generation** → `strategy_plan.json`
3. **Content Creation** → `content_batch.json`
4. **Graphics Generation** → `assets/graphics_metadata.json`
5. **Posting/Scheduling** → Status reports

### Output Files

All outputs are saved to the `outputs/` directory:

```
outputs/
├── company_profile.json          # Brand research results
├── strategy_plan.json            # Platform strategies
├── content_batch.json            # Generated content
├── pipeline_results.json         # Complete pipeline results
└── assets/
    └── graphics_metadata.json    # Graphic specifications
```

## Usage Examples

### Example 1: Complete Automated Workflow

```python
import asyncio
from app.agents.base.orchestrator import orchestrator
# ... initialize agents ...

async def main():
    result = await orchestrator.execute_complete_pipeline(
        website_url="https://mycompany.com",
        social_links={
            "instagram": "https://instagram.com/mycompany",
            "linkedin": "https://linkedin.com/company/mycompany"
        },
        platforms=["instagram", "linkedin", "facebook"],
        content_topics=["New product", "Team culture", "Industry tips"],
        mode="generate_only"
    )

    print(f"Status: {result['status']}")
    print(f"Content Items: {result['summary']['content_items_generated']}")
    print(f"Graphics: {result['summary']['graphics_generated']}")

asyncio.run(main())
```

### Example 2: Step-by-Step Control

```python
# Step 1: Research brand
brand_result = await orchestrator.execute_task(
    "brand_profile",
    {"website": "https://company.com", "socials": {...}},
    context={}
)

company_profile = brand_result["data"]

# Step 2: Generate strategy
strategy_result = await orchestrator.execute_task(
    "strategy",
    {"brand_profile": company_profile, "platforms": ["instagram"]},
    context={}
)

strategy_plan = strategy_result["data"]

# Step 3: Generate content
content_result = await orchestrator.execute_task(
    "content",
    {
        "platform": "instagram",
        "action": "generate",
        "topic": "Product launch",
        "brand_profile": company_profile,
        "strategy_plan": strategy_plan
    },
    context={}
)

# ... continue with graphics and posting ...
```

### Example 3: Posting to Platforms

```python
# Validate content first
validation_result = await orchestrator.execute_task(
    "poster",
    {
        "content": content_data,
        "platforms": ["instagram", "linkedin"],
        "mode": "validate"
    },
    context={}
)

if validation_result["data"]["all_valid"]:
    # Post to platforms
    posting_result = await orchestrator.execute_task(
        "poster",
        {
            "content": content_data,
            "platforms": ["instagram", "linkedin"],
            "credentials": {
                "instagram": {"access_token": "YOUR_TOKEN"},
                "linkedin": {"access_token": "YOUR_TOKEN"}
            },
            "mode": "post"
        },
        context={}
    )

    print(f"Posted to: {posting_result['data']['successful_platforms']}")
```

## Integration with Existing System

### Backward Compatibility

All original functionality is preserved:
- ✓ Original content agent still works without strategy data
- ✓ Existing API endpoints remain functional
- ✓ Frontend integration points unchanged
- ✓ Database models compatible

### New Endpoints to Add

```python
# API endpoint for complete pipeline
@router.post("/pipeline/execute")
async def execute_pipeline(request: PipelineRequest):
    result = await orchestrator.execute_complete_pipeline(
        website_url=request.website_url,
        social_links=request.social_links,
        platforms=request.platforms,
        content_topics=request.topics,
        mode=request.mode
    )
    return result
```

## Configuration

### Environment Variables

Add to `.env`:

```bash
# Existing
GEMINI_API_KEY=your_key_here
LLM_PROVIDER=gemini
DEFAULT_MODEL=gemini-flash-latest

# Platform Credentials (for posting)
INSTAGRAM_ACCESS_TOKEN=your_token
FACEBOOK_ACCESS_TOKEN=your_token
TWITTER_API_KEY=your_key
LINKEDIN_ACCESS_TOKEN=your_token
TIKTOK_ACCESS_TOKEN=your_token
YOUTUBE_API_KEY=your_key
```

### Agent Registration

Initialize agents once at startup:

```python
from app.agents.base.orchestrator import orchestrator
from app.agents.brand_profile.agent import BrandProfileAgent
from app.agents.strategy.agent import StrategyAgent
from app.agents.content.agent import ContentAgent
from app.agents.graphics.agent import GraphicsAgent
from app.agents.poster.agent import PosterAgent

# Register all agents
agents = [
    BrandProfileAgent(llm_service=llm_service),
    StrategyAgent(llm_service=llm_service),
    ContentAgent(llm_service=llm_service),
    GraphicsAgent(llm_service=llm_service),
    PosterAgent(llm_service=llm_service)
]

for agent in agents:
    orchestrator.register_agent(agent)
```

## Testing

### Run Example Pipeline

```bash
cd agent
python example_pipeline.py
```

### Test Individual Agents

```python
# Test brand profile agent
from app.agents.brand_profile.agent import BrandProfileAgent

agent = BrandProfileAgent(llm_service=llm_service)
result = await agent.execute(
    task={"website": "https://company.com", "socials": {}},
    context={}
)
```

## Future Enhancements

### Planned Features

1. **Image Generation Integration**
   - Connect Graphics Agent to DALL-E, Midjourney, or Stable Diffusion
   - Automatic image generation from specifications

2. **Advanced Scheduling**
   - Celery integration for background tasks
   - Queue management dashboard
   - Time zone optimization

3. **Analytics Integration**
   - Post performance tracking
   - Strategy optimization based on results
   - A/B testing framework

4. **MCP Integration**
   - Browser automation for platforms without APIs
   - Image generation MCPs
   - Data extraction MCPs

## Troubleshooting

### Common Issues

**Issue:** Agent not found
```
Solution: Ensure agent is registered with orchestrator
orchestrator.register_agent(agent)
```

**Issue:** LLM JSON parsing fails
```
Solution: Agents include fallback mechanisms. Check logs for details.
```

**Issue:** Platform posting fails
```
Solution: Verify credentials and API access tokens are valid.
Check platform API documentation for requirements.
```

## Summary

The enhanced multi-agent system provides:

✓ **Automated Brand Research** - No manual data entry needed
✓ **Strategic Content Planning** - Data-driven platform strategies
✓ **Optimized Content Generation** - Brand-aligned, strategy-driven content
✓ **Professional Graphics** - Detailed specifications for designers
✓ **Multi-Platform Posting** - Automated publishing with retry logic
✓ **Complete Pipeline** - End-to-end automation from research to posting

All while maintaining full backward compatibility with the existing system.
