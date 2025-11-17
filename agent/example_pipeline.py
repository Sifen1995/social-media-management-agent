"""
Example: Complete Multi-Agent Pipeline

This script demonstrates the full workflow from company research to content posting.
"""
import asyncio
import json
from app.agents.base.orchestrator import orchestrator
from app.agents.brand_profile.agent import BrandProfileAgent
from app.agents.strategy.agent import StrategyAgent
from app.agents.content.agent import ContentAgent
from app.agents.graphics.agent import GraphicsAgent
from app.agents.poster.agent import PosterAgent
from app.core.config import settings
from app.services.llm_service import LLMService


async def initialize_orchestrator():
    """Initialize and register all agents with the orchestrator."""
    print("Initializing agents...")

    # Initialize LLM service
    llm_service = LLMService(
        provider=settings.LLM_PROVIDER,
        api_key=settings.GEMINI_API_KEY,
        model=settings.DEFAULT_MODEL
    )

    # Create and register agents
    agents = [
        BrandProfileAgent(llm_service=llm_service),
        StrategyAgent(llm_service=llm_service),
        ContentAgent(llm_service=llm_service),
        GraphicsAgent(llm_service=llm_service),
        PosterAgent(llm_service=llm_service)
    ]

    for agent in agents:
        orchestrator.register_agent(agent)

    print(f"Registered {len(agents)} agents")
    return orchestrator


async def run_complete_pipeline():
    """Run the complete pipeline from brand research to content generation."""

    # Initialize orchestrator with all agents
    orch = await initialize_orchestrator()

    # Define input parameters
    company_data = {
        "website_url": "https://www.example-company.com",
        "social_links": {
            "instagram": "https://instagram.com/example",
            "linkedin": "https://linkedin.com/company/example",
            "twitter": "https://twitter.com/example",
            "facebook": "https://facebook.com/example",
            "tiktok": "https://tiktok.com/@example"
        },
        "platforms": ["instagram", "linkedin", "twitter", "facebook", "tiktok"],
        "content_topics": [
            "Product launch announcement",
            "Customer success story",
            "Industry tips and tricks"
        ],
        "mode": "generate_only"  # Options: generate_only, schedule, post
    }

    print("\n" + "="*60)
    print("STARTING COMPLETE MULTI-AGENT PIPELINE")
    print("="*60)
    print(f"\nWebsite: {company_data['website_url']}")
    print(f"Platforms: {', '.join(company_data['platforms'])}")
    print(f"Topics: {', '.join(company_data['content_topics'])}")
    print(f"Mode: {company_data['mode']}\n")

    # Execute pipeline
    results = await orch.execute_complete_pipeline(
        website_url=company_data["website_url"],
        social_links=company_data["social_links"],
        platforms=company_data["platforms"],
        content_topics=company_data["content_topics"],
        mode=company_data["mode"]
    )

    # Display results
    print("\n" + "="*60)
    print("PIPELINE EXECUTION RESULTS")
    print("="*60)

    print(f"\nStatus: {results['status']}")
    print(f"Execution Time: {results.get('summary', {}).get('execution_time', 'Unknown')}")

    # Step-by-step results
    print("\n--- Pipeline Steps ---")
    for step_name, step_data in results.get("steps", {}).items():
        status = "✓ SUCCESS" if step_data.get("success") else "✗ FAILED"
        print(f"{step_name}: {status}")

        if "items_generated" in step_data:
            print(f"  → Generated {step_data['items_generated']} items")

    # Summary statistics
    summary = results.get("summary", {})
    print("\n--- Summary Statistics ---")
    print(f"Brand: {summary.get('brand_name', 'Unknown')}")
    print(f"Content Items: {summary.get('content_items_generated', 0)}")
    print(f"Graphics: {summary.get('graphics_generated', 0)}")
    print(f"Platforms: {', '.join(summary.get('platforms_targeted', []))}")
    print(f"Successful Steps: {summary.get('successful_steps', 0)}/{summary.get('total_steps', 0)}")

    # Output files
    print("\n--- Generated Files ---")
    print("✓ outputs/company_profile.json - Brand profile from scraping")
    print("✓ outputs/strategy_plan.json - Platform-specific strategies")
    print("✓ outputs/content_batch.json - Generated content variations")
    print("✓ outputs/assets/graphics_metadata.json - Graphic specifications")

    # Save complete results
    with open("outputs/pipeline_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("✓ outputs/pipeline_results.json - Complete pipeline results")

    print("\n" + "="*60)
    print("PIPELINE COMPLETED")
    print("="*60)

    return results


async def run_step_by_step_example():
    """Example: Run pipeline step-by-step for more control."""

    orch = await initialize_orchestrator()

    print("\n" + "="*60)
    print("STEP-BY-STEP PIPELINE EXAMPLE")
    print("="*60)

    context = {"output_dir": "outputs"}

    # Step 1: Brand Profile Scraping
    print("\n[1/5] Scraping brand profile...")
    brand_task = {
        "website": "https://www.example.com",
        "socials": {
            "instagram": "https://instagram.com/example",
            "linkedin": "https://linkedin.com/company/example"
        }
    }

    brand_result = await orch.execute_task("brand_profile", brand_task, context)

    if brand_result.get("success"):
        print("✓ Brand profile created")
        company_profile = brand_result.get("data")
        context["brand_profile"] = company_profile
    else:
        print(f"✗ Failed: {brand_result.get('message')}")
        return

    # Step 2: Strategy Generation
    print("\n[2/5] Generating platform strategy...")
    strategy_task = {
        "brand_profile": company_profile,
        "platforms": ["instagram", "linkedin"],
        "mode": "comprehensive"
    }

    strategy_result = await orch.execute_task("strategy", strategy_task, context)

    if strategy_result.get("success"):
        print("✓ Strategy plan created")
        strategy_plan = strategy_result.get("data")
        context["strategy_plan"] = strategy_plan
    else:
        print("⚠ Strategy generation failed, using defaults")
        strategy_plan = {}

    # Step 3: Content Generation
    print("\n[3/5] Generating content...")
    content_task = {
        "platform": "instagram",
        "action": "generate",
        "topic": "New product launch",
        "content_type": "post",
        "count": 3,
        "brand_profile": company_profile,
        "strategy_plan": strategy_plan
    }

    content_result = await orch.execute_task("content", content_task, context)

    if content_result.get("success"):
        print(f"✓ Generated {len(content_result.get('data', []))} content variations")
        content = content_result.get("data", [])[0]  # Use first variation
    else:
        print(f"✗ Failed: {content_result.get('message')}")
        return

    # Step 4: Graphics Generation
    print("\n[4/5] Generating graphics...")
    graphics_task = {
        "content": content,
        "platform": "instagram",
        "mode": "specification",
        "brand_profile": company_profile
    }

    graphics_result = await orch.execute_task("graphics", graphics_task, context)

    if graphics_result.get("success"):
        print("✓ Graphic specification created")
    else:
        print(f"⚠ Graphics generation failed: {graphics_result.get('message')}")

    # Step 5: Posting (validation only)
    print("\n[5/5] Validating content for posting...")
    poster_task = {
        "content": content,
        "platforms": ["instagram"],
        "mode": "validate"
    }

    poster_result = await orch.execute_task("poster", poster_task, context)

    if poster_result.get("success"):
        validation = poster_result.get("data", {})
        if validation.get("all_valid"):
            print("✓ Content validated - ready to post")
        else:
            print("⚠ Content validation issues found")
    else:
        print(f"✗ Validation failed: {poster_result.get('message')}")

    print("\n" + "="*60)
    print("STEP-BY-STEP EXAMPLE COMPLETED")
    print("="*60)


async def main():
    """Main entry point."""
    print("\n" + "="*80)
    print(" "*20 + "MULTI-AGENT SOCIAL MEDIA PIPELINE")
    print("="*80)

    # Choose which example to run
    print("\nSelect example to run:")
    print("1. Complete automated pipeline")
    print("2. Step-by-step manual control")

    choice = input("\nEnter choice (1 or 2): ").strip()

    if choice == "1":
        await run_complete_pipeline()
    elif choice == "2":
        await run_step_by_step_example()
    else:
        print("Invalid choice. Running complete pipeline by default.")
        await run_complete_pipeline()


if __name__ == "__main__":
    asyncio.run(main())
