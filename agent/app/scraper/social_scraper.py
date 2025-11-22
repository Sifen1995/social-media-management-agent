"""
Social media scraper for extracting brand information from social profiles.

Enhanced with:
- Playwright support for JS-rendered content
- Automatic profile discovery
- Better data extraction from dynamic pages

Supports:
- Instagram
- LinkedIn
- Twitter/X
- TikTok
- Facebook
"""
import logging
import re
from typing import Dict, List, Optional, Any
from bs4 import BeautifulSoup
from app.scraper.base import ScraperBase

logger = logging.getLogger(__name__)


class SocialScraper(ScraperBase):
    """
    Scrapes social media profiles to extract brand voice and content patterns.

    Enhanced with Playwright for better JS-rendered content extraction.
    Note: Uses HTML scraping only (no API keys required).
    """

    def __init__(self, timeout: int = 30, use_playwright: bool = False):
        """
        Initialize social scraper.

        Args:
            timeout: Request timeout in seconds
            use_playwright: Use Playwright for JS-heavy platforms
        """
        super().__init__(timeout)
        self.use_playwright = use_playwright
        self._playwright_browser = None
        self._playwright_context = None

    async def _init_playwright(self):
        """Initialize playwright browser if needed."""
        if not self.use_playwright:
            return

        try:
            from playwright.async_api import async_playwright
            self._playwright = await async_playwright().start()
            self._playwright_browser = await self._playwright.chromium.launch(headless=True)
            self._playwright_context = await self._playwright_browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
        except Exception as e:
            logger.warning(f"Failed to initialize playwright: {str(e)}")
            self.use_playwright = False

    async def _close_playwright(self):
        """Close playwright browser."""
        if self._playwright_browser:
            await self._playwright_browser.close()
        if hasattr(self, '_playwright'):
            await self._playwright.stop()

    async def _fetch_with_playwright(self, url: str) -> Optional[str]:
        """
        Fetch page content using playwright for JS-heavy sites.

        Args:
            url: URL to fetch

        Returns:
            HTML content or None
        """
        if not self._playwright_context:
            await self._init_playwright()

        if not self._playwright_context:
            return None

        try:
            page = await self._playwright_context.new_page()
            await page.goto(url, wait_until='networkidle', timeout=self.timeout * 1000)
            content = await page.content()
            await page.close()
            return content
        except Exception as e:
            logger.warning(f"Playwright failed for {url}: {str(e)}")
            return None

    def scrape_all_socials(self, social_links: Dict[str, str]) -> Dict[str, Any]:
        """
        Scrape all provided social media profiles.

        Args:
            social_links: Dictionary of platform names to URLs

        Returns:
            Dictionary with scraped data from all platforms
        """
        results = {
            "platforms": {},
            "combined_insights": {
                "all_captions": [],
                "all_hashtags": [],
                "tone_indicators": [],
                "content_themes": []
            },
            "errors": []
        }

        for platform, url in social_links.items():
            if not url or url.strip() == "":
                continue

            url = self.normalize_url(url)
            if not self.is_valid_url(url):
                results["errors"].append(f"Invalid {platform} URL: {url}")
                continue

            logger.info(f"Scraping {platform}: {url}")

            platform_lower = platform.lower()
            platform_data = None

            if "instagram" in platform_lower:
                platform_data = self._scrape_instagram(url)
            elif "linkedin" in platform_lower:
                platform_data = self._scrape_linkedin(url)
            elif "twitter" in platform_lower or "x.com" in platform_lower:
                platform_data = self._scrape_twitter(url)
            elif "tiktok" in platform_lower:
                platform_data = self._scrape_tiktok(url)
            elif "facebook" in platform_lower:
                platform_data = self._scrape_facebook(url)
            else:
                results["errors"].append(f"Unsupported platform: {platform}")
                continue

            if platform_data and not platform_data.get("error"):
                results["platforms"][platform] = platform_data

                # Aggregate insights
                if platform_data.get("captions"):
                    results["combined_insights"]["all_captions"].extend(platform_data["captions"])
                if platform_data.get("hashtags"):
                    results["combined_insights"]["all_hashtags"].extend(platform_data["hashtags"])
                if platform_data.get("tone_indicators"):
                    results["combined_insights"]["tone_indicators"].extend(platform_data["tone_indicators"])
                if platform_data.get("themes"):
                    results["combined_insights"]["content_themes"].extend(platform_data["themes"])
            else:
                error_msg = platform_data.get("error", "Unknown error") if platform_data else "Failed to scrape"
                results["errors"].append(f"{platform}: {error_msg}")

        # Deduplicate and summarize
        results["combined_insights"]["all_hashtags"] = list(set(results["combined_insights"]["all_hashtags"]))
        results["combined_insights"]["content_themes"] = list(set(results["combined_insights"]["content_themes"]))

        return results

    async def scrape_all_socials_async(self, social_links: Dict[str, str]) -> Dict[str, Any]:
        """
        Async version with Playwright support for better extraction.

        Args:
            social_links: Dictionary of platform names to URLs

        Returns:
            Dictionary with scraped data from all platforms
        """
        results = {
            "platforms": {},
            "combined_insights": {
                "all_captions": [],
                "all_hashtags": [],
                "tone_indicators": [],
                "content_themes": []
            },
            "errors": []
        }

        # Initialize Playwright if enabled
        if self.use_playwright:
            await self._init_playwright()

        for platform, url in social_links.items():
            if not url or url.strip() == "":
                continue

            url = self.normalize_url(url)
            if not self.is_valid_url(url):
                results["errors"].append(f"Invalid {platform} URL: {url}")
                continue

            logger.info(f"Scraping {platform}: {url}")

            platform_lower = platform.lower()
            platform_data = None

            # Try with Playwright first for JS-heavy platforms
            if self.use_playwright and platform_lower in ['instagram', 'twitter', 'tiktok']:
                html = await self._fetch_with_playwright(url)
                if html:
                    platform_data = self._scrape_platform_from_html(platform_lower, url, html)

            # Fallback to standard scraping
            if not platform_data or platform_data.get("error"):
                if "instagram" in platform_lower:
                    platform_data = self._scrape_instagram(url)
                elif "linkedin" in platform_lower:
                    platform_data = self._scrape_linkedin(url)
                elif "twitter" in platform_lower or "x.com" in platform_lower:
                    platform_data = self._scrape_twitter(url)
                elif "tiktok" in platform_lower:
                    platform_data = self._scrape_tiktok(url)
                elif "facebook" in platform_lower:
                    platform_data = self._scrape_facebook(url)
                else:
                    results["errors"].append(f"Unsupported platform: {platform}")
                    continue

            if platform_data and not platform_data.get("error"):
                results["platforms"][platform] = platform_data

                # Aggregate insights
                if platform_data.get("captions"):
                    results["combined_insights"]["all_captions"].extend(platform_data["captions"])
                if platform_data.get("hashtags"):
                    results["combined_insights"]["all_hashtags"].extend(platform_data["hashtags"])
                if platform_data.get("tone_indicators"):
                    results["combined_insights"]["tone_indicators"].extend(platform_data["tone_indicators"])
                if platform_data.get("themes"):
                    results["combined_insights"]["content_themes"].extend(platform_data["themes"])
            else:
                error_msg = platform_data.get("error", "Unknown error") if platform_data else "Failed to scrape"
                results["errors"].append(f"{platform}: {error_msg}")

        # Close Playwright
        if self.use_playwright:
            await self._close_playwright()

        # Deduplicate and summarize
        results["combined_insights"]["all_hashtags"] = list(set(results["combined_insights"]["all_hashtags"]))
        results["combined_insights"]["content_themes"] = list(set(results["combined_insights"]["content_themes"]))

        return results

    def _scrape_platform_from_html(self, platform: str, url: str, html: str) -> Dict[str, Any]:
        """
        Generic platform scraper from HTML (works with Playwright-fetched content).

        Args:
            platform: Platform name
            url: URL
            html: HTML content

        Returns:
            Platform data
        """
        soup = self.parse_html(html)
        if not soup:
            return {"error": "Failed to parse HTML"}

        # Extract all text and look for patterns
        all_text = self.extract_text_from_soup(soup)

        data = {
            "platform": platform,
            "url": url,
            "bio": "",
            "captions": [],
            "hashtags": [],
            "tone_indicators": [],
            "themes": [],
            "username": ""
        }

        # Try to extract bio from meta tags
        meta_desc = soup.find('meta', property='og:description')
        if meta_desc:
            data["bio"] = meta_desc.get('content', '')

        # Extract username from URL
        username_patterns = {
            'instagram': r'instagram\.com/([^/]+)',
            'twitter': r'(?:twitter|x)\.com/([^/]+)',
            'tiktok': r'tiktok\.com/@([^/]+)'
        }

        pattern = username_patterns.get(platform)
        if pattern:
            match = re.search(pattern, url)
            if match:
                data["username"] = match.group(1)

        # Extract captions and hashtags
        potential_captions = self._extract_potential_captions(all_text)
        data["captions"] = potential_captions[:5]

        hashtags = re.findall(r'#(\w+)', all_text)
        data["hashtags"] = list(set(hashtags))[:20]

        if data["bio"]:
            data["tone_indicators"] = self._analyze_tone(data["bio"])

        return data

    def _scrape_instagram(self, url: str) -> Dict[str, Any]:
        """
        Scrape Instagram profile (public data only).

        Args:
            url: Instagram profile URL

        Returns:
            Dictionary with profile data
        """
        try:
            # Instagram heavily uses JavaScript, so basic scraping is limited
            # We'll attempt to extract what we can from the initial HTML
            html = self.fetch_html(url)
            if not html:
                return {"error": "Failed to fetch Instagram page"}

            soup = self.parse_html(html)
            if not soup:
                return {"error": "Failed to parse Instagram page"}

            data = {
                "platform": "instagram",
                "url": url,
                "bio": "",
                "captions": [],
                "hashtags": [],
                "tone_indicators": [],
                "themes": [],
                "username": ""
            }

            # Try to extract username from URL
            username_match = re.search(r'instagram\.com/([^/]+)', url)
            if username_match:
                data["username"] = username_match.group(1)

            # Try to extract bio from meta tags
            meta_desc = soup.find('meta', property='og:description')
            if meta_desc:
                bio_text = meta_desc.get('content', '')
                data["bio"] = bio_text

                # Extract hashtags from bio
                hashtags = re.findall(r'#(\w+)', bio_text)
                data["hashtags"].extend(hashtags)

            # Try to extract JSON data (Instagram often embeds data in script tags)
            script_tags = soup.find_all('script', type='application/ld+json')
            for script in script_tags:
                try:
                    import json
                    json_data = json.loads(script.string)
                    if isinstance(json_data, dict) and json_data.get('description'):
                        data["bio"] = json_data['description']
                except:
                    continue

            # Look for any visible text that might be captions
            # This is limited but better than nothing
            all_text = self.extract_text_from_soup(soup)
            potential_captions = self._extract_potential_captions(all_text)
            data["captions"] = potential_captions[:5]  # Limit to 5

            # Extract more hashtags from any found text
            all_hashtags = re.findall(r'#(\w+)', all_text)
            data["hashtags"].extend(all_hashtags)
            data["hashtags"] = list(set(data["hashtags"]))[:20]  # Unique, max 20

            # Analyze tone from bio
            if data["bio"]:
                data["tone_indicators"] = self._analyze_tone(data["bio"])

            # Note: This is limited due to Instagram's JS rendering
            data["note"] = "Limited data due to Instagram's JavaScript rendering. Consider using Instagram API for full access."

            return data

        except Exception as e:
            logger.error(f"Error scraping Instagram: {str(e)}")
            return {"error": str(e)}

    def _scrape_linkedin(self, url: str) -> Dict[str, Any]:
        """
        Scrape LinkedIn company page (public data).

        Args:
            url: LinkedIn company URL

        Returns:
            Dictionary with company data
        """
        try:
            html = self.fetch_html(url)
            if not html:
                return {"error": "Failed to fetch LinkedIn page"}

            soup = self.parse_html(html)
            if not soup:
                return {"error": "Failed to parse LinkedIn page"}

            data = {
                "platform": "linkedin",
                "url": url,
                "description": "",
                "captions": [],
                "hashtags": [],
                "tone_indicators": [],
                "themes": [],
                "company_name": ""
            }

            # Extract company name from title or meta
            title = soup.find('title')
            if title:
                data["company_name"] = title.string.split('|')[0].strip()

            # Extract description from meta tags
            meta_desc = soup.find('meta', property='og:description')
            if meta_desc:
                data["description"] = meta_desc.get('content', '')

            # LinkedIn description is often in the meta description
            if data["description"]:
                data["tone_indicators"] = self._analyze_tone(data["description"])
                data["themes"] = self._extract_themes(data["description"])

            # Try to find any visible posts/updates
            all_text = self.extract_text_from_soup(soup)
            data["captions"] = self._extract_potential_captions(all_text)[:5]

            # Extract hashtags
            hashtags = re.findall(r'#(\w+)', all_text)
            data["hashtags"] = list(set(hashtags))[:20]

            data["note"] = "Limited data due to LinkedIn's authentication requirements. Full access requires LinkedIn API."

            return data

        except Exception as e:
            logger.error(f"Error scraping LinkedIn: {str(e)}")
            return {"error": str(e)}

    def _scrape_twitter(self, url: str) -> Dict[str, Any]:
        """
        Scrape Twitter/X profile (public data).

        Args:
            url: Twitter profile URL

        Returns:
            Dictionary with profile data
        """
        try:
            # Twitter/X also heavily uses JavaScript
            html = self.fetch_html(url)
            if not html:
                return {"error": "Failed to fetch Twitter page"}

            soup = self.parse_html(html)
            if not soup:
                return {"error": "Failed to parse Twitter page"}

            data = {
                "platform": "twitter",
                "url": url,
                "bio": "",
                "captions": [],
                "hashtags": [],
                "tone_indicators": [],
                "themes": [],
                "username": ""
            }

            # Extract username from URL
            username_match = re.search(r'(?:twitter\.com|x\.com)/([^/]+)', url)
            if username_match:
                data["username"] = username_match.group(1)

            # Extract bio from meta tags
            meta_desc = soup.find('meta', property='og:description')
            if meta_desc:
                data["bio"] = meta_desc.get('content', '')

            # Twitter often has description in meta
            twitter_desc = soup.find('meta', attrs={'name': 'description'})
            if twitter_desc and not data["bio"]:
                data["bio"] = twitter_desc.get('content', '')

            # Analyze bio
            if data["bio"]:
                data["tone_indicators"] = self._analyze_tone(data["bio"])
                hashtags_in_bio = re.findall(r'#(\w+)', data["bio"])
                data["hashtags"].extend(hashtags_in_bio)

            # Extract any visible text
            all_text = self.extract_text_from_soup(soup)
            data["captions"] = self._extract_potential_captions(all_text)[:5]

            # Find more hashtags
            all_hashtags = re.findall(r'#(\w+)', all_text)
            data["hashtags"].extend(all_hashtags)
            data["hashtags"] = list(set(data["hashtags"]))[:20]

            data["note"] = "Limited data due to Twitter's JavaScript rendering and API restrictions."

            return data

        except Exception as e:
            logger.error(f"Error scraping Twitter: {str(e)}")
            return {"error": str(e)}

    def _scrape_tiktok(self, url: str) -> Dict[str, Any]:
        """
        Scrape TikTok profile (public data).

        Args:
            url: TikTok profile URL

        Returns:
            Dictionary with profile data
        """
        try:
            html = self.fetch_html(url)
            if not html:
                return {"error": "Failed to fetch TikTok page"}

            soup = self.parse_html(html)
            if not soup:
                return {"error": "Failed to parse TikTok page"}

            data = {
                "platform": "tiktok",
                "url": url,
                "bio": "",
                "captions": [],
                "hashtags": [],
                "tone_indicators": [],
                "themes": [],
                "username": ""
            }

            # Extract username
            username_match = re.search(r'tiktok\.com/@([^/]+)', url)
            if username_match:
                data["username"] = username_match.group(1)

            # Extract from meta tags
            meta_desc = soup.find('meta', property='og:description')
            if meta_desc:
                data["bio"] = meta_desc.get('content', '')

            # TikTok embeds data in script tags
            all_text = self.extract_text_from_soup(soup)
            data["captions"] = self._extract_potential_captions(all_text)[:5]

            # Extract hashtags
            hashtags = re.findall(r'#(\w+)', all_text)
            data["hashtags"] = list(set(hashtags))[:20]

            if data["bio"]:
                data["tone_indicators"] = self._analyze_tone(data["bio"])

            data["note"] = "Limited data due to TikTok's heavy use of JavaScript. Consider using TikTok API."

            return data

        except Exception as e:
            logger.error(f"Error scraping TikTok: {str(e)}")
            return {"error": str(e)}

    def _scrape_facebook(self, url: str) -> Dict[str, Any]:
        """
        Scrape Facebook page (public data).

        Args:
            url: Facebook page URL

        Returns:
            Dictionary with page data
        """
        try:
            html = self.fetch_html(url)
            if not html:
                return {"error": "Failed to fetch Facebook page"}

            soup = self.parse_html(html)
            if not soup:
                return {"error": "Failed to parse Facebook page"}

            data = {
                "platform": "facebook",
                "url": url,
                "description": "",
                "captions": [],
                "hashtags": [],
                "tone_indicators": [],
                "themes": [],
                "page_name": ""
            }

            # Extract page info from meta tags
            og_title = soup.find('meta', property='og:title')
            if og_title:
                data["page_name"] = og_title.get('content', '')

            meta_desc = soup.find('meta', property='og:description')
            if meta_desc:
                data["description"] = meta_desc.get('content', '')

            if data["description"]:
                data["tone_indicators"] = self._analyze_tone(data["description"])

            # Extract visible text
            all_text = self.extract_text_from_soup(soup)
            data["captions"] = self._extract_potential_captions(all_text)[:5]

            # Find hashtags
            hashtags = re.findall(r'#(\w+)', all_text)
            data["hashtags"] = list(set(hashtags))[:20]

            data["note"] = "Limited data due to Facebook's authentication requirements and JavaScript rendering."

            return data

        except Exception as e:
            logger.error(f"Error scraping Facebook: {str(e)}")
            return {"error": str(e)}

    def _extract_potential_captions(self, text: str, min_length: int = 20, max_length: int = 500) -> List[str]:
        """
        Extract potential social media captions from text.

        Args:
            text: Full text to search
            min_length: Minimum caption length
            max_length: Maximum caption length

        Returns:
            List of potential captions
        """
        # Split by common separators
        sentences = re.split(r'[.!?]\s+', text)

        captions = []
        for sentence in sentences:
            sentence = sentence.strip()
            if min_length <= len(sentence) <= max_length:
                # Filter out likely navigation/UI text
                if not any(skip in sentence.lower() for skip in ['cookie', 'privacy', 'terms', 'log in', 'sign up', 'follow us']):
                    captions.append(sentence)

        return captions[:10]

    def _analyze_tone(self, text: str) -> List[str]:
        """
        Analyze tone indicators from text.

        Args:
            text: Text to analyze

        Returns:
            List of tone indicators
        """
        tone_indicators = []

        text_lower = text.lower()

        # Check for various tone markers
        if any(word in text_lower for word in ['!', 'exciting', 'amazing', 'awesome', 'incredible']):
            tone_indicators.append("enthusiastic")

        if any(word in text_lower for word in ['professional', 'expertise', 'industry', 'solution']):
            tone_indicators.append("professional")

        if any(word in text_lower for word in ['you', 'your', "we're here", 'together']):
            tone_indicators.append("conversational")

        if any(emoji in text for emoji in ['😊', '🎉', '✨', '❤️', '🔥']):
            tone_indicators.append("casual/friendly")

        if any(word in text_lower for word in ['innovative', 'cutting-edge', 'advanced', 'next-generation']):
            tone_indicators.append("innovative")

        if any(word in text_lower for word in ['empower', 'inspire', 'transform', 'achieve']):
            tone_indicators.append("inspirational")

        return list(set(tone_indicators))

    def _extract_themes(self, text: str) -> List[str]:
        """
        Extract content themes from text.

        Args:
            text: Text to analyze

        Returns:
            List of themes
        """
        themes = []
        text_lower = text.lower()

        theme_keywords = {
            "technology": ["tech", "software", "digital", "innovation", "ai", "cloud"],
            "business": ["business", "enterprise", "company", "corporate", "b2b"],
            "lifestyle": ["lifestyle", "life", "wellness", "health", "fitness"],
            "education": ["education", "learning", "teach", "training", "course"],
            "fashion": ["fashion", "style", "clothing", "apparel", "design"],
            "food": ["food", "recipe", "cooking", "restaurant", "cuisine"],
            "travel": ["travel", "adventure", "explore", "destination", "journey"],
            "finance": ["finance", "investment", "money", "banking", "financial"],
            "entertainment": ["entertainment", "media", "content", "creative", "art"],
            "sustainability": ["sustainable", "eco", "green", "environment", "planet"]
        }

        for theme, keywords in theme_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                themes.append(theme)

        return themes
