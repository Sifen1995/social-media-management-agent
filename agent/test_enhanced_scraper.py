"""
Test script for enhanced web scraping capabilities.

Demonstrates:
1. JavaScript rendering fallback
2. OCR text extraction
3. Social profile auto-discovery
4. Unified data merging

Test with challenging websites:
- cgoncology.com (minimal text, requires JS rendering)
- JS-heavy sites
- Image-heavy sites
"""
import asyncio
import logging
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.scraper.website_scraper import WebsiteScraper
from app.scraper.social_scraper import SocialScraper
from app.scraper.social_finder import SocialProfileFinder
from app.scraper.extractor import BrandDataExtractor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def test_enhanced_website_scraping(url: str):
    """
    Test enhanced website scraping with all features enabled.

    Args:
        url: Website URL to test
    """
    print("\n" + "="*80)
    print(f"TESTING ENHANCED WEBSITE SCRAPING: {url}")
    print("="*80 + "\n")

    # Create scraper with all enhancements enabled
    scraper = WebsiteScraper(
        timeout=30,
        use_playwright=True,
        auto_js_fallback=True,
        use_ocr=True
    )

    try:
        # Scrape with enhanced features
        logger.info("Starting enhanced scraping...")
        result = await scraper.scrape_website_async(url)

        # Display results
        print("\n--- SCRAPING RESULTS ---")
        print(f"Base URL: {result.get('base_url')}")
        print(f"Pages scraped: {len(result.get('pages', {}))}")

        # Extraction metadata
        metadata = result.get('extraction_metadata', {})
        print(f"\nExtraction Methods Used: {metadata.get('sources_used', [])}")
        print(f"Used JS Rendering: {metadata.get('used_js_rendering', False)}")
        print(f"Used OCR: {metadata.get('used_ocr', False)}")
        print(f"Data Quality: {metadata.get('data_quality', 'unknown')}")

        # Merge stats
        merge_stats = metadata.get('merge_stats', {})
        print(f"\nMerge Statistics:")
        print(f"  - Total chars before: {merge_stats.get('total_chars_before', 0)}")
        print(f"  - Total chars after: {merge_stats.get('total_chars_after', 0)}")
        print(f"  - Compression ratio: {merge_stats.get('compression_ratio', 0)}")

        # Show text samples
        final_corpus = result.get('final_corpus', '')
        print(f"\nFinal Corpus Length: {len(final_corpus)} chars")
        print(f"Sample (first 500 chars):")
        print(f"{final_corpus[:500]}\n...")

        # Errors
        errors = result.get('errors', [])
        if errors:
            print(f"\nErrors encountered: {len(errors)}")
            for error in errors[:5]:
                print(f"  - {error}")

        return result

    except Exception as e:
        logger.error(f"Scraping failed: {str(e)}", exc_info=True)
        return None


async def test_social_profile_discovery(url: str, company_name: str = None):
    """
    Test automatic social profile discovery.

    Args:
        url: Website URL
        company_name: Optional company name
    """
    print("\n" + "="*80)
    print(f"TESTING SOCIAL PROFILE DISCOVERY: {url}")
    print("="*80 + "\n")

    finder = SocialProfileFinder(timeout=15)

    try:
        logger.info("Discovering social profiles...")
        profiles = finder.find_all_profiles(
            website_url=url,
            company_name=company_name
        )

        print(f"\nDiscovered {len(profiles)} social profiles:")
        for platform, profile_url in profiles.items():
            print(f"  - {platform.capitalize()}: {profile_url}")

        return profiles

    except Exception as e:
        logger.error(f"Profile discovery failed: {str(e)}", exc_info=True)
        return {}


async def test_full_brand_profile_extraction(url: str, company_name: str = None):
    """
    Test complete brand profile extraction workflow.

    Args:
        url: Website URL
        company_name: Optional company name
    """
    print("\n" + "="*80)
    print(f"TESTING FULL BRAND PROFILE EXTRACTION: {url}")
    print("="*80 + "\n")

    try:
        # Step 1: Discover social profiles
        logger.info("Step 1: Discovering social profiles...")
        finder = SocialProfileFinder(timeout=15)
        social_links = finder.find_all_profiles(
            website_url=url,
            company_name=company_name
        )
        print(f"Found {len(social_links)} social profiles")

        # Step 2: Scrape website with enhancements
        logger.info("Step 2: Scraping website with enhancements...")
        website_scraper = WebsiteScraper(
            timeout=30,
            use_playwright=True,
            auto_js_fallback=True,
            use_ocr=True
        )
        website_data = await website_scraper.scrape_website_async(url)
        print(f"Website data quality: {website_data.get('extraction_metadata', {}).get('data_quality')}")

        # Step 3: Scrape social media
        logger.info("Step 3: Scraping social media...")
        social_scraper = SocialScraper(timeout=30, use_playwright=True)
        social_data = await social_scraper.scrape_all_socials_async(social_links)
        print(f"Scraped {len(social_data.get('platforms', {}))} social platforms")

        # Step 4: Extract and normalize
        logger.info("Step 4: Extracting and normalizing data...")
        extractor = BrandDataExtractor()
        normalized_data = extractor.extract_and_normalize(website_data, social_data)

        # Display insights
        insights = normalized_data.get('key_insights', {})
        print(f"\n--- KEY INSIGHTS ---")
        print(f"Has Website Data: {insights.get('has_website_data')}")
        print(f"Has Social Data: {insights.get('has_social_data')}")
        print(f"Data Quality: {insights.get('data_quality')}")
        print(f"Extraction Methods: {insights.get('extraction_methods_used', [])}")
        print(f"Brand Name Candidates: {insights.get('brand_name_candidates', [])}")
        print(f"Top Hashtags: {insights.get('top_hashtags', [])[:5]}")

        # Display combined text sample
        combined_text = normalized_data.get('combined_text', '')
        print(f"\nCombined Text Length: {len(combined_text)} chars")
        print(f"Sample (first 800 chars):")
        print(f"{combined_text[:800]}\n...")

        return normalized_data

    except Exception as e:
        logger.error(f"Full extraction failed: {str(e)}", exc_info=True)
        return None


async def test_difficult_websites():
    """
    Test with known difficult websites.
    """
    print("\n" + "="*80)
    print("TESTING WITH DIFFICULT WEBSITES")
    print("="*80 + "\n")

    difficult_sites = [
        {
            "url": "https://cgoncology.com",
            "name": "CG Oncology",
            "challenge": "Minimal text content, JS-heavy"
        },
        # Add more challenging sites here for testing
    ]

    for site in difficult_sites:
        print(f"\n{'='*60}")
        print(f"Testing: {site['name']}")
        print(f"URL: {site['url']}")
        print(f"Challenge: {site['challenge']}")
        print(f"{'='*60}\n")

        result = await test_enhanced_website_scraping(site['url'])

        if result:
            final_corpus_len = len(result.get('final_corpus', ''))
            metadata = result.get('extraction_metadata', {})

            print(f"\n✓ SUCCESS")
            print(f"  - Final corpus: {final_corpus_len} chars")
            print(f"  - Methods used: {metadata.get('sources_used', [])}")
            print(f"  - Quality: {metadata.get('data_quality')}")
        else:
            print(f"\n✗ FAILED")

        print("\n" + "="*60 + "\n")
        await asyncio.sleep(2)  # Be respectful with requests


async def main():
    """
    Main test runner.
    """
    import argparse

    parser = argparse.ArgumentParser(description='Test enhanced web scraping')
    parser.add_argument('--url', type=str, help='Website URL to test')
    parser.add_argument('--company', type=str, help='Company name (optional)')
    parser.add_argument('--test-all', action='store_true', help='Run all tests')
    parser.add_argument('--test-difficult', action='store_true', help='Test difficult websites')

    args = parser.parse_args()

    if args.test_difficult:
        await test_difficult_websites()

    elif args.url:
        # Test specific URL
        print("\n" + "="*80)
        print("RUNNING COMPLETE TEST SUITE")
        print("="*80)

        # Test 1: Enhanced website scraping
        await test_enhanced_website_scraping(args.url)
        await asyncio.sleep(2)

        # Test 2: Social profile discovery
        await test_social_profile_discovery(args.url, args.company)
        await asyncio.sleep(2)

        # Test 3: Full brand profile
        await test_full_brand_profile_extraction(args.url, args.company)

    else:
        print("Usage:")
        print("  python test_enhanced_scraper.py --url https://example.com")
        print("  python test_enhanced_scraper.py --url https://example.com --company 'Company Name'")
        print("  python test_enhanced_scraper.py --test-difficult")
        print("\nOptions:")
        print("  --url URL          Website to test")
        print("  --company NAME     Company name for social discovery")
        print("  --test-difficult   Test with known challenging websites")


if __name__ == "__main__":
    asyncio.run(main())
