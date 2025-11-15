"""
Tests for scraper components.
"""
import pytest
from app.scraper.base import ScraperBase
from app.scraper.website_scraper import WebsiteScraper
from app.scraper.social_scraper import SocialScraper
from app.scraper.extractor import BrandDataExtractor


class TestScraperBase:
    """Tests for ScraperBase utility class."""

    def test_is_valid_url(self):
        """Test URL validation."""
        scraper = ScraperBase()

        assert scraper.is_valid_url("https://example.com") is True
        assert scraper.is_valid_url("http://example.com") is True
        assert scraper.is_valid_url("invalid-url") is False
        assert scraper.is_valid_url("") is False

    def test_normalize_url(self):
        """Test URL normalization."""
        scraper = ScraperBase()

        assert scraper.normalize_url("example.com") == "https://example.com"
        assert scraper.normalize_url("https://example.com") == "https://example.com"
        assert scraper.normalize_url("http://example.com") == "http://example.com"
        assert scraper.normalize_url("  example.com  ") == "https://example.com"

    def test_clean_text(self):
        """Test text cleaning."""
        scraper = ScraperBase()

        text = "  This   has   extra    spaces  "
        cleaned = scraper.clean_text(text)
        assert cleaned == "This has extra spaces"


class TestWebsiteScraper:
    """Tests for WebsiteScraper."""

    def test_get_pages_to_scrape(self):
        """Test generation of pages to scrape."""
        scraper = WebsiteScraper()
        pages = scraper._get_pages_to_scrape("https://example.com")

        assert "homepage" in pages
        assert "about" in pages
        assert "services" in pages
        assert pages["homepage"] == "https://example.com"
        assert pages["about"] == "https://example.com/about"

    def test_extract_section_near_keyword(self):
        """Test keyword-based section extraction."""
        scraper = WebsiteScraper()

        text = "Welcome to our company. Our mission is to provide excellent service to all customers. We value quality."
        mission = scraper._extract_section_near_keyword(text, "mission", context_words=10)

        assert "mission" in mission.lower()
        assert len(mission) > 0

    @pytest.mark.skip(reason="Requires network access")
    def test_scrape_website_integration(self):
        """Integration test for scraping a real website."""
        scraper = WebsiteScraper(timeout=10)
        result = scraper.scrape_website("https://example.com")

        assert "base_url" in result
        assert result["base_url"] == "https://example.com"


class TestSocialScraper:
    """Tests for SocialScraper."""

    def test_extract_potential_captions(self):
        """Test caption extraction from text."""
        scraper = SocialScraper()

        text = "This is a great post about social media. Follow us for more tips. Cookie policy can be found here."
        captions = scraper._extract_potential_captions(text, min_length=20, max_length=100)

        # Should extract the first sentence and skip cookie policy
        assert len(captions) > 0
        assert any("great post" in cap for cap in captions)

    def test_analyze_tone(self):
        """Test tone analysis."""
        scraper = SocialScraper()

        enthusiastic_text = "This is amazing! We're so excited to announce this!"
        tones = scraper._analyze_tone(enthusiastic_text)
        assert "enthusiastic" in tones

        professional_text = "We provide professional solutions for industry leaders."
        tones = scraper._analyze_tone(professional_text)
        assert "professional" in tones

    def test_extract_themes(self):
        """Test theme extraction."""
        scraper = SocialScraper()

        tech_text = "We specialize in software development and digital innovation."
        themes = scraper._extract_themes(tech_text)
        assert "technology" in themes

        lifestyle_text = "Join us for wellness tips and healthy lifestyle advice."
        themes = scraper._extract_themes(lifestyle_text)
        assert "lifestyle" in themes

    @pytest.mark.skip(reason="Requires network access")
    def test_scrape_instagram_integration(self):
        """Integration test for Instagram scraping."""
        scraper = SocialScraper()
        result = scraper._scrape_instagram("https://instagram.com/instagram")

        assert result["platform"] == "instagram"


class TestBrandDataExtractor:
    """Tests for BrandDataExtractor."""

    def test_normalize_website_data(self):
        """Test website data normalization."""
        extractor = BrandDataExtractor()

        website_data = {
            "base_url": "https://example.com",
            "meta_data": {"description": "Example company description"},
            "structured_data": [{"@type": "Organization", "name": "Example Inc"}],
            "raw_text": "Sample website text"
        }

        normalized = extractor._normalize_website_data(website_data)

        assert normalized["available"] is True
        assert normalized["base_url"] == "https://example.com"
        assert normalized["meta_description"] == "Example company description"
        assert normalized["organization_name"] == "Example Inc"

    def test_normalize_social_data(self):
        """Test social data normalization."""
        extractor = BrandDataExtractor()

        social_data = {
            "platforms": {
                "instagram": {
                    "bio": "Example bio",
                    "username": "example",
                    "hashtags": ["tech", "innovation", "tech"],
                    "captions": ["Great post 1", "Great post 2"]
                }
            },
            "combined_insights": {
                "all_captions": ["Great post 1", "Great post 2"],
                "all_hashtags": ["tech", "innovation", "tech"],
                "tone_indicators": ["professional"],
                "content_themes": ["technology"]
            }
        }

        normalized = extractor._normalize_social_data(social_data)

        assert normalized["available"] is True
        assert "instagram" in normalized["platforms_scraped"]
        assert len(normalized["combined_insights"]["frequent_hashtags"]) > 0

    def test_get_most_common(self):
        """Test getting most common items."""
        extractor = BrandDataExtractor()

        items = ["apple", "banana", "apple", "cherry", "banana", "apple"]
        most_common = extractor._get_most_common(items, top_n=2)

        assert len(most_common) == 2
        assert most_common[0][0] == "apple"
        assert most_common[0][1] == 3
        assert most_common[1][0] == "banana"
        assert most_common[1][1] == 2

    def test_analyze_writing_style(self):
        """Test writing style analysis."""
        extractor = BrandDataExtractor()

        captions = [
            "Short post",
            "Check out our new product! Click to learn more 🎉 #newlaunch",
            "Another brief caption"
        ]

        style = extractor._analyze_writing_style(captions)

        assert "emojis" in style.lower() or "uses emojis" in style.lower()
        assert "cta" in style.lower() or "includes CTAs" in style.lower()

    def test_extract_and_normalize_full_flow(self):
        """Test full extract and normalize flow."""
        extractor = BrandDataExtractor()

        website_data = {
            "base_url": "https://example.com",
            "meta_data": {"description": "Example description"},
            "structured_data": [],
            "raw_text": "Example website content",
            "extracted_sections": {}
        }

        social_data = {
            "platforms": {
                "instagram": {
                    "bio": "Example bio",
                    "username": "example",
                    "hashtags": ["tech"],
                    "captions": ["Great post"]
                }
            },
            "combined_insights": {
                "all_captions": ["Great post"],
                "all_hashtags": ["tech"],
                "tone_indicators": [],
                "content_themes": []
            }
        }

        normalized = extractor.extract_and_normalize(website_data, social_data)

        assert "website" in normalized
        assert "social" in normalized
        assert "combined_text" in normalized
        assert "key_insights" in normalized
        assert normalized["key_insights"]["data_quality"] == "excellent"


@pytest.mark.asyncio
class TestBrandProfileAgent:
    """Tests for BrandProfileAgent."""

    @pytest.mark.skip(reason="Requires LLM service and network access")
    async def test_brand_profile_agent_execution(self):
        """Integration test for BrandProfileAgent."""
        from app.agents.brand_profile.agent import BrandProfileAgent
        from app.services.llm_service import LLMService

        llm_service = LLMService()
        agent = BrandProfileAgent(llm_service=llm_service)

        task = {
            "website": "https://example.com",
            "socials": {}
        }

        result = await agent.execute(task, context={})

        assert "success" in result
        if result["success"]:
            assert "data" in result
            assert "brand_name" in result["data"]
