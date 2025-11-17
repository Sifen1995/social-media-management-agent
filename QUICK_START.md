# Quick Start Guide - Multi-Agent Pipeline

## 🚀 Get Started in 5 Minutes

### Prerequisites

- Python 3.11+
- Google Gemini API Key
- Git

### 1. Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/social-media-management-agent.git
cd social-media-management-agent

# Navigate to agent directory
cd agent

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### 2. Run the Complete Pipeline

```bash
# Run the example pipeline
python example_pipeline.py
```

Follow the prompts to choose:
1. Complete automated pipeline
2. Step-by-step manual control

### 3. Understanding the Output

After running, check the `outputs/` directory:

```
outputs/
├── company_profile.json         # Scraped brand information
├── strategy_plan.json           # Platform-specific strategies
├── content_batch.json           # Generated content variations
├── pipeline_results.json        # Complete execution results
└── assets/
    └── graphics_metadata.json   # Graphic design specifications
```

## 📖 Basic Usage

### Option 1: Complete Automated Pipeline

```python
import asyncio
from initialize_agents import get_orchestrator

async def main():
    orchestrator = get_orchestrator()

    result = await orchestrator.execute_complete_pipeline(
        website_url="https://your-company.com",
        social_links={
            "instagram": "https://instagram.com/yourcompany",
            "linkedin": "https://linkedin.com/company/yourcompany"
        },
        platforms=["instagram", "linkedin", "tiktok"],
        content_topics=[
            "Product announcement",
            "Customer story",
            "Industry insights"
        ],
        mode="generate_only"
    )

    print(f"Status: {result['status']}")
    print(f"Content generated: {result['summary']['content_items_generated']}")

asyncio.run(main())
```

### Option 2: Step-by-Step Control

```python
import asyncio
from initialize_agents import get_orchestrator

async def main():
    orchestrator = get_orchestrator()
    context = {}

    # Step 1: Research brand
    brand_result = await orchestrator.execute_task(
        "brand_profile",
        {
            "website": "https://your-company.com",
            "socials": {"instagram": "..."}
        },
        context
    )

    company_profile = brand_result["data"]

    # Step 2: Generate strategy
    strategy_result = await orchestrator.execute_task(
        "strategy",
        {
            "brand_profile": company_profile,
            "platforms": ["instagram", "linkedin"]
        },
        context
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
        context
    )

    content = content_result["data"]
    print(f"Generated {len(content)} variations")

asyncio.run(main())
```

## 🎯 Common Use Cases

### Use Case 1: Generate Content for New Brand

```python
# 1. Scrape brand info from website
# 2. Generate platform strategies
# 3. Create content for multiple platforms
# 4. Get graphic design specs

result = await orchestrator.execute_complete_pipeline(
    website_url="https://newbrand.com",
    social_links={},  # Empty if no social media yet
    platforms=["instagram", "facebook", "linkedin"],
    content_topics=["Brand introduction", "Our story", "First product"],
    mode="generate_only"
)
```

### Use Case 2: Content Calendar for Existing Brand

```python
# Generate 30 days of content
topics = [
    "Monday Motivation", "Tips Tuesday", "Wednesday Wisdom",
    "Thursday Thoughts", "Feature Friday"
] * 6  # 30 topics

result = await orchestrator.execute_complete_pipeline(
    website_url="https://existingbrand.com",
    social_links={"instagram": "...", "linkedin": "..."},
    platforms=["instagram", "linkedin"],
    content_topics=topics,
    mode="generate_only"
)
```

### Use Case 3: Analyze and Improve Strategy

```python
# Get current brand profile
brand_result = await orchestrator.execute_task(
    "brand_profile",
    {"website": "https://brand.com", "socials": {...}},
    {}
)

# Generate comprehensive strategy
strategy_result = await orchestrator.execute_task(
    "strategy",
    {
        "brand_profile": brand_result["data"],
        "platforms": ["instagram", "tiktok", "linkedin"],
        "mode": "comprehensive"
    },
    {}
)

# Review strategy_plan.json for recommendations
```

## 🔧 Advanced Configuration

### Custom Output Directory

```python
result = await orchestrator.execute_complete_pipeline(
    ...,
    context={"output_dir": "custom_output_folder"}
)
```

### Content Generation Modes

```python
# Generate only (default)
mode="generate_only"

# Validate and schedule
mode="schedule"

# Post immediately (requires credentials)
mode="post"
```

### Platform Credentials

For posting mode:

```python
credentials = {
    "instagram": {"access_token": "YOUR_TOKEN"},
    "linkedin": {"access_token": "YOUR_TOKEN"},
    "facebook": {"access_token": "YOUR_TOKEN"}
}

result = await orchestrator.execute_complete_pipeline(
    ...,
    credentials=credentials,
    mode="post"
)
```

## 📊 Understanding Results

### Pipeline Results Structure

```json
{
  "status": "completed",
  "started_at": "2024-11-17T10:00:00Z",
  "completed_at": "2024-11-17T10:05:30Z",
  "steps": {
    "brand_profile": {"success": true},
    "strategy": {"success": true},
    "content_generation": {"success": true, "items_generated": 15},
    "graphics_generation": {"success": true, "items_generated": 10}
  },
  "outputs": {
    "company_profile": {...},
    "strategy_plan": {...},
    "content_batch": [...],
    "graphics": [...]
  },
  "summary": {
    "total_steps": 5,
    "successful_steps": 5,
    "content_items_generated": 15,
    "graphics_generated": 10,
    "execution_time": "330.45 seconds"
  }
}
```

## 🆘 Troubleshooting

### Issue: "GEMINI_API_KEY not found"

**Solution:** Add your API key to `.env`:
```bash
GEMINI_API_KEY=your_actual_key_here
```

### Issue: Agent not found error

**Solution:** Initialize agents properly:
```python
from initialize_agents import get_orchestrator
orchestrator = get_orchestrator()  # This auto-registers all agents
```

### Issue: Scraping fails

**Solution:** Try with Playwright for JavaScript-heavy sites:
```python
brand_task = {
    "website": "https://site.com",
    "use_playwright": True  # Enable JavaScript rendering
}
```

### Issue: JSON parsing errors

**Solution:** Agents include fallback mechanisms. Check:
- LLM temperature (lower = more structured)
- Model selection (gemini-flash vs gemini-pro)
- Logs for detailed error messages

## 📚 Next Steps

1. **Read Full Documentation:** See `MULTI_AGENT_GUIDE.md`
2. **Explore Agents:** Each agent in `agent/app/agents/*/`
3. **Customize Prompts:** Modify prompts in `*/prompts.py` files
4. **Add API Endpoints:** Integrate with FastAPI (see existing endpoints)
5. **Connect Frontend:** Use with existing React frontend

## 🔗 API Integration

Add to your FastAPI app:

```python
from fastapi import APIRouter
from initialize_agents import get_orchestrator

router = APIRouter()

@router.post("/pipeline/run")
async def run_pipeline(request: PipelineRequest):
    orchestrator = get_orchestrator()

    result = await orchestrator.execute_complete_pipeline(
        website_url=request.website_url,
        social_links=request.social_links,
        platforms=request.platforms,
        content_topics=request.topics,
        mode=request.mode
    )

    return result
```

## 💡 Pro Tips

1. **Start Small:** Test with 1-2 platforms and 2-3 topics first
2. **Review Outputs:** Check generated JSON files before posting
3. **Iterate Strategy:** Run strategy agent separately to refine approach
4. **Batch Operations:** Generate multiple content items, then post later
5. **Monitor Performance:** Track which content performs best

## 🎉 You're Ready!

The system is now configured and ready to automate your social media workflow from brand research to content posting.

For detailed documentation, see:
- `MULTI_AGENT_GUIDE.md` - Complete system documentation
- `README.md` - Original project documentation
- `AUTO_BRAND_PROFILE_GUIDE.md` - Brand scraping details

Happy automating! 🚀
