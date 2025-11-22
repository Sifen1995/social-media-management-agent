"""
Brand Profile Agent - automatically researches and creates brand profiles
from website and social media data.
"""
import logging
from typing import Dict, Any, Optional
import json
import asyncio
from app.agents.base.agent import BaseAgent
from app.scraper.website_scraper import WebsiteScraper
from app.scraper.social_scraper import SocialScraper
from app.scraper.extractor import BrandDataExtractor
from app.scraper.social_finder import SocialProfileFinder
from app.agents.brand_profile.prompts import (
    BRAND_PROFILE_SYSTEM_PROMPT,
    BRAND_PROFILE_ANALYSIS_PROMPT
)

logger = logging.getLogger(__name__)


class BrandProfileAgent(BaseAgent):
    """
    Brand Profile Agent - orchestrates web scraping and LLM analysis
    to automatically generate comprehensive brand profiles.

    Workflow:
    1. Scrape website using WebsiteScraper
    2. Scrape social media using SocialScraper
    3. Extract and normalize data using BrandDataExtractor
    4. Analyze with LLM to generate structured brand profile
    5. Return JSON brand profile
    """

    @property
    def name(self) -> str:
        return "brand_profile"

    @property
    def description(self) -> str:
        return "Automatically researches and generates comprehensive brand profiles from website and social media"

    def get_required_fields(self) -> list:
        return ["website"]

    async def execute(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute brand profile research with enhanced scraping.

        Args:
            task: Must contain 'website' and optionally 'socials', 'company_name'
            context: Execution context

        Returns:
            Structured brand profile or error
        """
        try:
            website_url = task.get("website", "").strip()
            social_links = task.get("socials", {})
            company_name = task.get("company_name", "")

            # Enhanced scraping options (enabled by default)
            use_playwright = task.get("use_playwright", True)  # Changed to True by default
            auto_js_fallback = task.get("auto_js_fallback", True)
            use_ocr = task.get("use_ocr", True)
            auto_find_socials = task.get("auto_find_socials", True)

            if not website_url:
                return self.create_result(
                    success=False,
                    message="Website URL is required"
                )

            logger.info(f"Starting enhanced brand profile research for: {website_url}")

            # Step 0: Auto-discover social profiles if not provided
            if auto_find_socials and (not social_links or len(social_links) < 2):
                logger.info("Step 0: Auto-discovering social media profiles...")
                social_finder = SocialProfileFinder(timeout=15)
                discovered_profiles = social_finder.find_all_profiles(
                    website_url=website_url,
                    company_name=company_name
                )

                # Merge with provided social links (provided links take precedence)
                for platform, url in discovered_profiles.items():
                    if platform not in social_links:
                        social_links[platform] = url
                        logger.info(f"Auto-discovered {platform}: {url}")

            # Step 1: Scrape website with enhanced extraction
            logger.info("Step 1: Scraping website with enhanced extraction...")
            website_scraper = WebsiteScraper(
                timeout=30,
                use_playwright=use_playwright,
                auto_js_fallback=auto_js_fallback,
                use_ocr=use_ocr
            )

            # Always use async version to support enhanced features
            website_data = await website_scraper.scrape_website_async(website_url)

            if website_data.get("error"):
                logger.warning(f"Website scraping failed: {website_data['error']}")
            else:
                extraction_meta = website_data.get("extraction_metadata", {})
                logger.info(f"Website extraction methods used: {extraction_meta.get('sources_used', [])}")
                logger.info(f"Website data quality: {extraction_meta.get('data_quality', 'unknown')}")

            # Step 2: Scrape social media with Playwright support
            logger.info("Step 2: Scraping social media...")
            social_scraper = SocialScraper(timeout=30, use_playwright=use_playwright)

            # Use async version if Playwright is enabled
            if use_playwright:
                social_data = await social_scraper.scrape_all_socials_async(social_links)
            else:
                social_data = social_scraper.scrape_all_socials(social_links)

            # Step 3: Extract and normalize data
            logger.info("Step 3: Extracting and normalizing data...")
            extractor = BrandDataExtractor()
            normalized_data = extractor.extract_and_normalize(website_data, social_data)

            # Check if we have sufficient data
            key_insights = normalized_data.get("key_insights", {})
            if key_insights.get("data_quality") == "insufficient":
                return self.create_result(
                    success=False,
                    message="Insufficient data scraped. Unable to generate brand profile.",
                    data={
                        "error": "Scraping failed or insufficient data",
                        "details": {
                            "website_errors": website_data.get("errors", []),
                            "social_errors": social_data.get("errors", [])
                        }
                    }
                )

            # Step 4: Analyze with LLM
            logger.info("Step 4: Analyzing with LLM...")
            llm_prompt = extractor.prepare_for_llm(normalized_data)
            brand_profile = await self._analyze_with_llm(llm_prompt)

            if brand_profile.get("error"):
                return self.create_result(
                    success=False,
                    message="LLM analysis failed",
                    data=brand_profile
                )

            # Step 5: Enrich with scraped metadata
            brand_profile = self._enrich_profile(brand_profile, normalized_data)

            return self.create_result(
                success=True,
                data=brand_profile,
                message="Brand profile generated successfully",
                metadata={
                    "website_scraped": key_insights.get("has_website_data"),
                    "social_platforms": normalized_data.get("social", {}).get("platforms_scraped", []),
                    "data_quality": key_insights.get("data_quality")
                }
            )

        except Exception as e:
            logger.error(f"Error in brand profile agent: {str(e)}", exc_info=e)
            return self.create_error_result(e, "Brand profile generation failed")

    async def _analyze_with_llm(self, prompt_text: str) -> Dict[str, Any]:
        """
        Analyze scraped data with LLM to generate structured brand profile.

        Args:
            prompt_text: Prepared prompt with all scraped data

        Returns:
            Structured brand profile JSON
        """
        try:
            # Format the analysis prompt with the scraped data
            full_prompt = BRAND_PROFILE_ANALYSIS_PROMPT.format(
                scraped_data=prompt_text
            )

            # Call LLM service
            response = await self.llm_service.generate_completion(
                system_prompt=BRAND_PROFILE_SYSTEM_PROMPT,
                user_prompt=full_prompt,
                temperature=0.3,  # Lower temperature for more consistent extraction
                response_format="json"
            )

            # Parse JSON response
            try:
                brand_profile = json.loads(response)
                return brand_profile
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse LLM JSON response: {str(e)}")
                logger.debug(f"LLM Response: {response}")

                # Try to extract JSON from response if it's wrapped in markdown
                import re
                json_match = re.search(r'```json\s*(\{.*\})\s*```', response, re.DOTALL)
                if json_match:
                    try:
                        brand_profile = json.loads(json_match.group(1))
                        return brand_profile
                    except:
                        pass

                return {
                    "error": "Failed to parse LLM response as JSON",
                    "raw_response": response[:500]
                }

        except Exception as e:
            logger.error(f"LLM analysis error: {str(e)}", exc_info=e)
            return {"error": str(e)}

    def _enrich_profile(self, brand_profile: Dict[str, Any], normalized_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enrich brand profile with additional metadata from scraped data.

        Args:
            brand_profile: LLM-generated brand profile
            normalized_data: Normalized scraped data

        Returns:
            Enriched brand profile
        """
        # Add source URLs
        brand_profile["source_urls"] = {
            "website": normalized_data.get("website", {}).get("base_url", ""),
            "social_platforms": {}
        }

        # Add social platform URLs
        social_platforms = normalized_data.get("social", {}).get("platform_data", {})
        for platform_name, platform_data in social_platforms.items():
            username = platform_data.get("username", "")
            if username:
                brand_profile["source_urls"]["social_platforms"][platform_name] = username

        # Add data quality indicator
        brand_profile["_metadata"] = {
            "data_quality": normalized_data.get("key_insights", {}).get("data_quality", "unknown"),
            "sources_used": {
                "website": normalized_data.get("website", {}).get("available", False),
                "social_media": normalized_data.get("social", {}).get("available", False)
            }
        }

        return brand_profile

    def _validate_brand_profile(self, profile: Dict[str, Any]) -> bool:
        """
        Validate that brand profile has required fields.

        Args:
            profile: Brand profile to validate

        Returns:
            True if valid, False otherwise
        """
        required_fields = [
            "brand_name",
            "overview",
            "tone_voice",
            "target_audience"
        ]

        for field in required_fields:
            if not profile.get(field):
                logger.warning(f"Brand profile missing required field: {field}")
                return False

        return True
