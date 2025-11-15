"""
Demo script showcasing the multi-agent system in action.
This demonstrates real agent tasks without requiring database setup.
"""
import asyncio
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.agents.content.agent import ContentAgent
from app.agents.planner.agent import PlannerAgent
from app.agents.scheduler.agent import SchedulerAgent
from app.agents.analytics.agent import AnalyticsAgent
from app.core.config import settings


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_result(result):
    """Pretty print agent results."""
    print(json.dumps(result, indent=2, default=str))


async def demo_content_generation():
    """Demo: Content Agent generates Instagram posts."""
    print_section("DEMO 1: Content Generation Agent")
    print("Task: Generate 2 Instagram posts about fitness motivation")

    agent = ContentAgent()

    task = {
        "action": "generate",
        "platform": "instagram",
        "topic": "fitness motivation and morning workout routines",
        "content_type": "post",
        "count": 2
    }

    context = {
        "brand": {
            "name": "FitLife Pro",
            "niche": "fitness and wellness",
            "brand_voice": "motivating, energetic, authentic",
            "target_audience": "fitness enthusiasts aged 25-40",
            "goals": ["inspire daily workouts", "build community", "share fitness tips"]
        }
    }

    print("\nGenerating content...")
    result = await agent.execute(task, context)

    if result.get("success"):
        print(f"\n[SUCCESS] Generated {len(result.get('data', []))} posts:")
        for i, post in enumerate(result.get('data', []), 1):
            print(f"\n--- Post {i} ---")
            try:
                caption = post.get('caption', 'N/A')[:200]
                print(f"Caption: {caption}...")
            except UnicodeEncodeError:
                print("Caption: [Contains emoji/special chars - view in result data]")
            print(f"Hashtags: {', '.join(post.get('hashtags', [])[:8])}")
            try:
                print(f"CTA: {post.get('cta', 'N/A')}")
            except UnicodeEncodeError:
                print("CTA: [Contains emoji/special chars]")
    else:
        print(f"\n[FAILED] {result.get('message')}")

    return result


async def demo_planner_workflow():
    """Demo: Planner Agent creates multi-step campaign."""
    print_section("DEMO 2: Planner Agent - Campaign Planning")
    print("Task: Plan a 1-week Instagram fitness challenge campaign")

    agent = PlannerAgent()

    task = {
        "user_request": "Create a 1-week Instagram fitness challenge with daily posts, engagement responses, and performance tracking"
    }

    context = {
        "brand": {
            "id": 1,
            "name": "FitLife Pro",
            "niche": "fitness and wellness",
            "brand_voice": "motivating, energetic, authentic",
            "target_audience": "fitness enthusiasts aged 25-40",
            "goals": ["launch fitness challenge", "increase engagement", "grow community"]
        }
    }

    print("\nCreating execution plan...")
    result = await agent.execute(task, context)

    if result.get("success"):
        plan = result.get("data", {}).get("plan", {})
        print(f"\n[SUCCESS] Campaign Plan Created:")
        print(f"Task Type: {plan.get('task_type', 'N/A')}")
        print(f"Primary Agent: {plan.get('primary_agent', 'N/A')}")
        print(f"\nExecution Steps ({len(plan.get('steps', []))}):")
        for step in plan.get('steps', []):
            print(f"  {step.get('step')}. {step.get('agent')} - {step.get('action')}")
        print(f"\nReasoning: {plan.get('reasoning', 'N/A')}")
    else:
        print(f"\n[FAILED] {result.get('message')}")

    return result


async def demo_scheduler_optimization():
    """Demo: Scheduler Agent determines optimal posting times."""
    print_section("DEMO 3: Scheduler Agent - Optimal Timing")
    print("Task: Find best posting times for Instagram fitness content")

    agent = SchedulerAgent()

    task = {
        "action": "optimal_times",
        "platform": "instagram",
        "content_type": "fitness tips",
        "timezone": "America/New_York"
    }

    context = {
        "brand": {
            "name": "FitLife Pro",
            "niche": "fitness and wellness",
            "target_audience": "fitness enthusiasts aged 25-40"
        }
    }

    print("\nCalculating optimal posting schedule...")
    result = await agent.execute(task, context)

    if result.get("success"):
        recommendations = result.get("data", {}).get("recommendations", [])
        print(f"\n[SUCCESS] Optimal Posting Times:")
        for rec in recommendations[:5]:
            print(f"  - {rec.get('day_of_week')} at {rec.get('time')} (Score: {rec.get('score', 0):.2f})")
            print(f"    Reason: {rec.get('reason', 'N/A')}")
    else:
        print(f"\n[FAILED] {result.get('message')}")

    return result


async def demo_analytics_insights():
    """Demo: Analytics Agent provides performance insights."""
    print_section("DEMO 4: Analytics Agent - Performance Insights")
    print("Task: Analyze mock performance data and provide recommendations")

    agent = AnalyticsAgent()

    # Simulated performance data
    task = {
        "action": "insights",
        "platform": "instagram",
        "time_period": "last_7_days"
    }

    context = {
        "brand": {
            "name": "FitLife Pro",
            "niche": "fitness and wellness",
            "current_followers": 25000
        },
        "analytics_data": [
            {
                "date": "2025-11-08",
                "engagement": 1250,
                "likes": 987,
                "comments": 87,
                "shares": 34,
                "saves": 156,
                "reach": 8500,
                "impressions": 12000
            }
        ]
    }

    print("\nAnalyzing performance data...")
    result = await agent.execute(task, context)

    if result.get("success"):
        data = result.get("data", {})
        print(f"\n[SUCCESS] Performance Analysis:")

        # Handle both dict and string responses
        if isinstance(data, dict):
            insights = data.get("insights", {})
            if isinstance(insights, dict):
                print(f"Overall Performance: {insights.get('overall_score', 'N/A')}")
                print(f"\nKey Insights:")
                for insight in insights.get('key_insights', [])[:5]:
                    print(f"  - {insight}")
                print(f"\nRecommendations:")
                for rec in insights.get('recommendations', [])[:5]:
                    print(f"  - {rec}")
            else:
                print(f"Insights: {insights}")
        else:
            print(f"Analysis Result: {str(data)[:300]}...")
    else:
        print(f"\n[FAILED] {result.get('message')}")

    return result


async def main():
    """Run all agent demos."""
    print("\n" + "=" * 80)
    print("  SOCIAL MEDIA MANAGEMENT AGENT SYSTEM - LIVE DEMO")
    print("=" * 80)
    print(f"  LLM Provider: {settings.LLM_PROVIDER}")
    print(f"  Model: {settings.DEFAULT_MODEL}")
    print("=" * 80)

    # Run each demo
    demos = [
        ("Content Generation", demo_content_generation),
        ("Campaign Planning", demo_planner_workflow),
        ("Schedule Optimization", demo_scheduler_optimization),
        ("Performance Analytics", demo_analytics_insights)
    ]

    results = []
    for demo_name, demo_func in demos:
        try:
            result = await demo_func()
            results.append((demo_name, result.get("success", False)))
        except Exception as e:
            print(f"\n[ERROR] {demo_name} failed: {e}")
            import traceback
            traceback.print_exc()
            results.append((demo_name, False))

        # Small delay between demos
        await asyncio.sleep(1)

    # Print summary
    print_section("DEMO SUMMARY")
    for demo_name, success in results:
        status = "[PASS]" if success else "[FAIL]"
        print(f"{status} {demo_name}")

    all_passed = all(result[1] for result in results)
    print("\n" + "=" * 80)
    if all_passed:
        print("  ALL DEMOS COMPLETED SUCCESSFULLY!")
    else:
        print("  SOME DEMOS FAILED - CHECK OUTPUT ABOVE")
    print("=" * 80 + "\n")

    return all_passed
