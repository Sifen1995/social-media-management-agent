"""
Test script to verify Gemini integration with the agent system.
"""
import asyncio
import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.llm_service import LLMService
from app.agents.content.agent import ContentAgent
from app.agents.planner.agent import PlannerAgent
from app.core.config import settings


async def test_llm_service():
    """Test the LLM service with Gemini."""
    print("=" * 60)
    print("Testing LLM Service with Gemini")
    print("=" * 60)
    print(f"Provider: {settings.LLM_PROVIDER}")
    print(f"Model: {settings.DEFAULT_MODEL}")
    print(f"API Key (first 10 chars): {settings.GEMINI_API_KEY[:10] if settings.GEMINI_API_KEY else 'NOT SET'}...")
    print()

    try:
        llm_service = LLMService()

        print("Testing basic completion...")
        response = await llm_service.generate_completion(
            system_prompt="You are a helpful assistant.",
            user_prompt="Say 'Hello from Gemini!' and nothing else.",
            temperature=0.7
        )
        print(f"[OK] Basic completion: {response}")
        print()

        print("Testing JSON response...")
        json_response = await llm_service.generate_completion(
            system_prompt="You are a JSON response generator.",
            user_prompt='Generate a JSON object with keys "message" and "status". Message should be "Test successful", status should be "ok".',
            temperature=0.5,
            response_format="json"
        )
        print(f"[OK] JSON response: {json_response}")
        print()

        return True
    except Exception as e:
        print(f"[FAIL] Error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_content_agent():
    """Test the Content Agent with Gemini."""
    print("=" * 60)
    print("Testing Content Agent")
    print("=" * 60)

    try:
        agent = ContentAgent()

        # Create a test task
        task = {
            "action": "generate",
            "platform": "instagram",
            "topic": "healthy breakfast ideas",
            "content_type": "post",
            "count": 1
        }

        context = {
            "brand": {
                "name": "Healthy Living Co",
                "niche": "health and wellness",
                "brand_voice": "friendly, encouraging, informative",
                "target_audience": "health-conscious millennials",
                "goals": ["inspire healthy habits", "educate about nutrition"]
            }
        }

        print("Generating content...")
        result = await agent.execute(task, context)

        if result.get("success"):
            print("[OK] Content generation successful!")
            print(f"Generated {len(result.get('data', []))} content items")
            if result.get("data"):
                print("\nFirst generated content:")
                try:
                    caption = result['data'][0].get('caption', 'N/A')[:150]
                    hashtags = ', '.join(result['data'][0].get('hashtags', [])[:5])
                    print(f"Caption: {caption}...")
                    print(f"Hashtags: {hashtags}")
                except UnicodeEncodeError:
                    print("Caption: [Content contains special characters - check result data]")
                    print(f"Hashtags count: {len(result['data'][0].get('hashtags', []))}")
            print()
        else:
            print(f"[FAIL] Content generation failed: {result.get('message')}")
            print()
            return False

        return True
    except Exception as e:
        print(f"[FAIL] Error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_planner_agent():
    """Test the Planner Agent with Gemini."""
    print("=" * 60)
    print("Testing Planner Agent")
    print("=" * 60)

    try:
        agent = PlannerAgent()

        # Create a complex task
        task = {
            "user_request": "Create 3 Instagram posts about summer fitness tips and schedule them for next week"
        }

        context = {
            "brand": {
                "id": 1,
                "name": "FitLife Studio",
                "niche": "fitness and wellness",
                "brand_voice": "motivating, energetic, supportive",
                "target_audience": "fitness enthusiasts aged 25-40",
                "goals": ["promote healthy lifestyle", "build community"]
            }
        }

        print("Planning multi-agent workflow...")
        result = await agent.execute(task, context)

        if result.get("success"):
            print("[OK] Planning successful!")
            plan = result.get("data", {}).get("plan", {})
            print(f"\nExecution plan created with {len(plan.get('steps', []))} steps:")
            for i, step in enumerate(plan.get("steps", []), 1):
                print(f"  {i}. {step.get('agent')} - {step.get('action')}")
            print()
        else:
            print(f"[FAIL] Planning failed: {result.get('message')}")
            print()
            return False

        return True
    except Exception as e:
        print(f"[FAIL] Error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("GEMINI INTEGRATION TEST SUITE")
    print("=" * 60 + "\n")

    results = []

    # Test LLM Service
    results.append(("LLM Service", await test_llm_service()))

    # Test Content Agent
    results.append(("Content Agent", await test_content_agent()))

    # Test Planner Agent
    results.append(("Planner Agent", await test_planner_agent()))

    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    for test_name, passed in results:
        status = "[PASSED]" if passed else "[FAILED]"
        print(f"{test_name}: {status}")

    all_passed = all(result[1] for result in results)
    print("\n" + "=" * 60)
    if all_passed:
        print("ALL TESTS PASSED!")
    else:
        print("SOME TESTS FAILED")
    print("=" * 60 + "\n")

    return all_passed


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
