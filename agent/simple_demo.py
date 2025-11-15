"""
Simple demo showcasing the agent system with direct task execution.
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.agents.content.agent import ContentAgent
from app.core.config import settings


def print_banner(title):
    """Print a banner."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


async def demo_content_agent():
    """Demonstrate content generation."""
    print_banner("SOCIAL MEDIA AGENT - CONTENT GENERATION DEMO")
    print(f"Using: {settings.LLM_PROVIDER} - {settings.DEFAULT_MODEL}\n")

    # Initialize content agent
    agent = ContentAgent()

    # Task 1: Generate Instagram post
    print("[TASK 1] Generate Instagram post about healthy smoothie recipes")
    print("-" * 70)

    task1 = {
        "action": "generate",
        "platform": "instagram",
        "topic": "healthy green smoothie recipes for energy",
        "content_type": "post",
        "count": 1
    }

    context1 = {
        "brand": {
            "name": "Wellness Kitchen",
            "niche": "healthy eating and nutrition",
            "brand_voice": "friendly, informative, encouraging",
            "target_audience": "health-conscious adults 25-45",
            "goals": ["share healthy recipes", "inspire nutrition"]
        }
    }

    print("Processing...")
    result1 = await agent.execute(task1, context1)

    if result1.get("success"):
        posts = result1.get("data", [])
        print(f"\n[SUCCESS] Generated {len(posts)} post(s)\n")

        for i, post in enumerate(posts, 1):
            print(f"POST {i}:")
            print(f"  Platform: Instagram")
            print(f"  Type: {post.get('content_type', 'post')}")
            # Safely print caption without unicode issues
            caption = post.get('caption', 'N/A')
            try:
                print(f"  Caption: {caption[:150]}...")
            except:
                print(f"  Caption: [Contains special characters - {len(caption)} chars]")

            hashtags = post.get('hashtags', [])
            if hashtags:
                print(f"  Hashtags: #{' #'.join(hashtags[:10])}")

            cta = post.get('cta', '')
            if cta:
                try:
                    print(f"  CTA: {cta}")
                except:
                    print(f"  CTA: [Contains special characters]")
    else:
        print(f"[FAILED] {result1.get('message')}")

    print("\n" + "-" * 70)

    # Task 2: Generate Twitter thread
    print("\n[TASK 2] Generate Twitter thread about productivity tips")
    print("-" * 70)

    task2 = {
        "action": "generate",
        "platform": "twitter",
        "topic": "5 productivity tips for remote workers",
        "content_type": "thread",
        "count": 1
    }

    context2 = {
        "brand": {
            "name": "ProductivityPro",
            "niche": "productivity and personal development",
            "brand_voice": "motivational, practical, concise",
            "target_audience": "remote workers and entrepreneurs",
            "goals": ["share productivity hacks", "inspire efficiency"]
        }
    }

    print("Processing...")
    result2 = await agent.execute(task2, context2)

    if result2.get("success"):
        threads = result2.get("data", [])
        print(f"\n[SUCCESS] Generated {len(threads)} thread(s)\n")

        for i, thread in enumerate(threads, 1):
            print(f"THREAD {i}:")
            print(f"  Platform: Twitter/X")
            try:
                caption = thread.get('caption', 'N/A')
                print(f"  Content: {caption[:200]}...")
            except:
                print(f"  Content: [Contains special characters]")

            hashtags = thread.get('hashtags', [])
            if hashtags:
                print(f"  Hashtags: {', '.join(['#' + h for h in hashtags[:5]])}")
    else:
        print(f"[FAILED] {result2.get('message')}")

    print("\n" + "-" * 70)

    # Summary
    print_banner("DEMO COMPLETE")
    success_count = sum([result1.get("success", False), result2.get("success", False)])
    print(f"\nSuccessful tasks: {success_count}/2")
    print(f"Agent Status: {'OPERATIONAL' if success_count > 0 else 'NEEDS ATTENTION'}")
    print("\nThe multi-agent system is ready to:")
    print("  - Generate platform-specific content")
    print("  - Plan multi-step campaigns")
    print("  - Schedule optimal posting times")
    print("  - Analyze performance metrics")
    print("  - Manage community engagement")
    print("  - Monitor trends and competitors")
    print("  - Optimize content performance")
    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    asyncio.run(demo_content_agent())
