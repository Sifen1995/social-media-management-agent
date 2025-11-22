"""
Website scraper for extracting brand information from company websites.

Enhanced features:
- Automatic JavaScript rendering fallback
- OCR text extraction from images
- Intelligent data merging and deduplication
"""
import logging
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from app.scraper.base import ScraperBase
from app.scraper.ocr_extractor import OCRExtractor
from app.scraper.data_merger import DataMerger

logger = logging.getLogger(__name__)


class WebsiteScraper(ScraperBase):
    """
    Scrapes company websites to extract brand information.

    Automatically scrapes:
    - Homepage
    - /about pages
    - /services or /products pages
    - /contact pages
    """

    def __init__(
        self,
        timeout: int = 30,
        use_playwright: bool = False,
        auto_js_fallback: bool = True,
        use_ocr: bool = True
    ):
        """
        Initialize website scraper.

        Args:
            timeout: Request timeout in seconds
            use_playwright: Whether to use playwright for JS-heavy sites
            auto_js_fallback: Auto-detect and use JS rendering when needed
            use_ocr: Enable OCR for image text extraction
        """
        super().__init__(timeout)
        self.use_playwright = use_playwright
        self.auto_js_fallback = auto_js_fallback
        self.use_ocr = use_ocr
        self._playwright_browser = None
        self._playwright_context = None
        self.ocr_extractor = OCRExtractor() if use_ocr else None
        self.data_merger = DataMerger()

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

    def scrape_website(self, base_url: str) -> Dict[str, Any]:
        """
        Scrape entire website for brand information.

        Args:
            base_url: Base URL of the website

        Returns:
            Dictionary containing scraped data
        """
        base_url = self.normalize_url(base_url)

        if not self.is_valid_url(base_url):
            return {"error": "Invalid URL provided"}

        logger.info(f"Starting website scrape for: {base_url}")

        # Determine pages to scrape
        pages_to_scrape = self._get_pages_to_scrape(base_url)

        scraped_data = {
            "base_url": base_url,
            "pages": {},
            "structured_data": [],
            "meta_data": {},
            "raw_text": "",
            "errors": []
        }

        # Scrape each page
        for page_name, page_url in pages_to_scrape.items():
            logger.info(f"Scraping {page_name}: {page_url}")
            page_data = self._scrape_page(page_url)

            if page_data:
                scraped_data["pages"][page_name] = page_data
                scraped_data["raw_text"] += f"\n\n=== {page_name.upper()} PAGE ===\n{page_data.get('text', '')}"

                # Collect structured data
                if page_data.get('json_ld'):
                    scraped_data["structured_data"].extend(page_data['json_ld'])

                # Collect meta data from homepage
                if page_name == "homepage" and page_data.get('meta_tags'):
                    scraped_data["meta_data"] = page_data['meta_tags']
            else:
                scraped_data["errors"].append(f"Failed to scrape {page_name}")

        # Extract key sections
        scraped_data["extracted_sections"] = self._extract_key_sections(scraped_data)

        return scraped_data

    async def scrape_website_async(self, base_url: str) -> Dict[str, Any]:
        """
        Enhanced async scraping with automatic fallback strategies.

        Workflow:
        1. Try standard HTML scraping
        2. If insufficient, use JavaScript rendering
        3. If still insufficient, use OCR
        4. Merge and deduplicate all data

        Args:
            base_url: Base URL of the website

        Returns:
            Dictionary containing scraped data with enhanced extraction
        """
        base_url = self.normalize_url(base_url)

        if not self.is_valid_url(base_url):
            return {"error": "Invalid URL provided"}

        logger.info(f"Starting enhanced async website scrape for: {base_url}")

        # Initialize playwright if needed
        if self.use_playwright or self.auto_js_fallback:
            await self._init_playwright()

        pages_to_scrape = self._get_pages_to_scrape(base_url)

        scraped_data = {
            "base_url": base_url,
            "pages": {},
            "structured_data": [],
            "meta_data": {},
            "raw_text": "",
            "raw_js_text": "",
            "raw_ocr_text": "",
            "errors": [],
            "extraction_metadata": {
                "used_js_rendering": False,
                "used_ocr": False,
                "text_sources": []
            }
        }

        # Scrape each page with enhanced extraction
        for page_name, page_url in pages_to_scrape.items():
            logger.info(f"Scraping {page_name}: {page_url}")

            page_result = await self._scrape_page_enhanced(page_url, page_name)

            if page_result and not page_result.get("error"):
                scraped_data["pages"][page_name] = page_result
                scraped_data["raw_text"] += f"\n\n=== {page_name.upper()} PAGE ===\n{page_result.get('text', '')}"

                # Collect JS-rendered text
                if page_result.get('js_text'):
                    scraped_data["raw_js_text"] += f"\n\n=== {page_name.upper()} (JS) ===\n{page_result['js_text']}"
                    scraped_data["extraction_metadata"]["used_js_rendering"] = True

                # Collect OCR text
                if page_result.get('ocr_text'):
                    scraped_data["raw_ocr_text"] += f"\n\n=== {page_name.upper()} (OCR) ===\n{page_result['ocr_text']}"
                    scraped_data["extraction_metadata"]["used_ocr"] = True

                if page_result.get('json_ld'):
                    scraped_data["structured_data"].extend(page_result['json_ld'])

                if page_name == "homepage" and page_result.get('meta_tags'):
                    scraped_data["meta_data"] = page_result['meta_tags']
            else:
                error_msg = page_result.get("error", "Unknown error") if page_result else "Failed to scrape"
                scraped_data["errors"].append(f"{page_name}: {error_msg}")

        # Close playwright
        if self.use_playwright or self.auto_js_fallback:
            await self._close_playwright()

        # Merge all text sources using DataMerger
        merged_data = self.data_merger.merge_all_sources(
            raw_website_text=scraped_data["raw_text"],
            raw_js_text=scraped_data["raw_js_text"],
            raw_ocr_text=scraped_data["raw_ocr_text"],
            social_media_text="",  # No social data in website scraper
            metadata=scraped_data["extraction_metadata"]
        )

        # Update scraped data with merged results
        scraped_data["final_corpus"] = merged_data["final_corpus"]
        scraped_data["extraction_metadata"].update({
            "sources_used": merged_data["sources_used"],
            "data_quality": self.data_merger.assess_data_quality(merged_data),
            "merge_stats": merged_data["stats"]
        })

        # Extract key sections
        scraped_data["extracted_sections"] = self._extract_key_sections(scraped_data)

        return scraped_data

    async def _scrape_page_enhanced(self, url: str, page_name: str) -> Dict[str, Any]:
        """
        Scrape a page with automatic fallback strategies.

        Strategy:
        1. Standard HTML fetch
        2. If text < 300 chars, try JS rendering
        3. If still < 200 chars, try OCR
        4. Return combined results

        Args:
            url: Page URL
            page_name: Name identifier for the page

        Returns:
            Page data with all extraction methods applied
        """
        MIN_TEXT_FOR_JS_FALLBACK = 300
        MIN_TEXT_FOR_OCR = 200

        result = {
            "text": "",
            "js_text": "",
            "ocr_text": "",
            "title": "",
            "meta_tags": {},
            "json_ld": [],
            "headings": {},
            "links": []
        }

        # Step 1: Standard HTML scraping
        logger.debug(f"[{page_name}] Attempting standard HTML scraping...")
        html = self.fetch_html(url)

        if not html:
            # If standard fetch fails and we're on homepage, try JS immediately
            if page_name == "homepage" and self.auto_js_fallback:
                logger.info(f"[{page_name}] Standard fetch failed, trying JS rendering...")
                html = await self._fetch_with_playwright(url)

        if html:
            page_data = self._parse_page(html)
            result.update(page_data)

            text_length = len(result.get('text', ''))
            logger.info(f"[{page_name}] Standard scraping extracted {text_length} chars")

            # Step 2: Check if JS fallback is needed
            if text_length < MIN_TEXT_FOR_JS_FALLBACK and self.auto_js_fallback:
                logger.info(f"[{page_name}] Insufficient text ({text_length} chars), trying JS rendering...")
                js_html = await self._fetch_with_playwright(url)

                if js_html and js_html != html:  # Only if content is different
                    js_data = self._parse_page(js_html)
                    js_text = js_data.get('text', '')

                    if len(js_text) > text_length:
                        logger.info(f"[{page_name}] JS rendering extracted {len(js_text)} chars (additional)")
                        result['js_text'] = js_text

                        # Update other fields if they're better
                        if not result.get('title') and js_data.get('title'):
                            result['title'] = js_data['title']
                        if not result.get('meta_tags') and js_data.get('meta_tags'):
                            result['meta_tags'] = js_data['meta_tags']

                        text_length = max(text_length, len(js_text))

            # Step 3: Check if OCR is needed
            if text_length < MIN_TEXT_FOR_OCR and self.use_ocr and self.ocr_extractor:
                logger.info(f"[{page_name}] Still insufficient text ({text_length} chars), trying OCR...")

                # Use the most complete HTML available
                html_for_ocr = html
                if result.get('js_text'):
                    # Re-fetch with playwright to get full rendered HTML
                    html_for_ocr = await self._fetch_with_playwright(url) or html

                ocr_result = self.ocr_extractor.extract_from_page(
                    html=html_for_ocr,
                    base_url=url,
                    existing_text_length=text_length
                )

                if ocr_result.get('success') and ocr_result.get('extracted_text'):
                    ocr_text = ocr_result['extracted_text']
                    logger.info(f"[{page_name}] OCR extracted {len(ocr_text)} chars from {ocr_result.get('images_processed', 0)} images")
                    result['ocr_text'] = ocr_text

        else:
            logger.warning(f"[{page_name}] Failed to fetch page content")
            result['error'] = "Failed to fetch page"

        return result

    def _get_pages_to_scrape(self, base_url: str) -> Dict[str, str]:
        """
        Generate list of pages to scrape.

        Args:
            base_url: Base URL

        Returns:
            Dictionary of page names to URLs
        """
        parsed = urlparse(base_url)
        base = f"{parsed.scheme}://{parsed.netloc}"

        pages = {
            "homepage": base_url,
            "about": urljoin(base, "/about"),
            "about_us": urljoin(base, "/about-us"),
            "services": urljoin(base, "/services"),
            "products": urljoin(base, "/products"),
            "contact": urljoin(base, "/contact"),
            "contact_us": urljoin(base, "/contact-us"),
        }

        return pages

    def _scrape_page(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Scrape a single page.

        Args:
            url: URL to scrape

        Returns:
            Dictionary with page data or None
        """
        html = self.fetch_html(url)
        if not html:
            return None

        return self._parse_page(html)

    def _parse_page(self, html: str) -> Dict[str, Any]:
        """
        Parse HTML and extract relevant data.

        Args:
            html: HTML content

        Returns:
            Dictionary with parsed data
        """
        soup = self.parse_html(html)
        if not soup:
            return {}

        page_data = {
            "text": self.extract_text_from_soup(soup),
            "title": soup.title.string if soup.title else "",
            "meta_tags": self.extract_meta_tags(soup),
            "json_ld": self.extract_json_ld(soup),
            "headings": self._extract_headings(soup),
            "links": self._extract_internal_links(soup)
        }

        return page_data

    def _extract_headings(self, soup: BeautifulSoup) -> Dict[str, List[str]]:
        """
        Extract all headings from page.

        Args:
            soup: BeautifulSoup object

        Returns:
            Dictionary of heading levels to text
        """
        headings = {
            "h1": [h.get_text(strip=True) for h in soup.find_all('h1')],
            "h2": [h.get_text(strip=True) for h in soup.find_all('h2')],
            "h3": [h.get_text(strip=True) for h in soup.find_all('h3')],
        }
        return headings

    def _extract_internal_links(self, soup: BeautifulSoup) -> List[str]:
        """
        Extract internal links for potential further scraping.

        Args:
            soup: BeautifulSoup object

        Returns:
            List of URLs
        """
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('/'):
                links.append(href)
        return list(set(links))[:20]  # Limit to 20 unique links

    def _extract_key_sections(self, scraped_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Extract key sections from scraped data.

        Args:
            scraped_data: Full scraped data

        Returns:
            Dictionary with extracted sections
        """
        sections = {}

        # Extract from structured data
        for json_ld in scraped_data.get("structured_data", []):
            if isinstance(json_ld, dict):
                if json_ld.get("@type") == "Organization":
                    sections["organization_name"] = json_ld.get("name", "")
                    sections["organization_description"] = json_ld.get("description", "")

        # Extract from meta tags
        meta = scraped_data.get("meta_data", {})
        if meta.get("description"):
            sections["meta_description"] = meta["description"]

        # Try to identify mission/vision from headings and text
        for page_name, page_data in scraped_data.get("pages", {}).items():
            text = page_data.get("text", "").lower()

            # Look for mission statement
            if "mission" in text and not sections.get("mission"):
                sections["mission"] = self._extract_section_near_keyword(
                    page_data.get("text", ""), "mission"
                )

            # Look for vision statement
            if "vision" in text and not sections.get("vision"):
                sections["vision"] = self._extract_section_near_keyword(
                    page_data.get("text", ""), "vision"
                )

            # Look for values
            if "values" in text and not sections.get("values"):
                sections["values"] = self._extract_section_near_keyword(
                    page_data.get("text", ""), "values"
                )

        return sections

    def _extract_section_near_keyword(self, text: str, keyword: str, context_words: int = 100) -> str:
        """
        Extract text near a keyword.

        Args:
            text: Full text
            keyword: Keyword to search for
            context_words: Number of words to extract around keyword

        Returns:
            Extracted text section
        """
        words = text.split()
        keyword_lower = keyword.lower()

        for i, word in enumerate(words):
            if keyword_lower in word.lower():
                start = max(0, i - context_words // 2)
                end = min(len(words), i + context_words // 2)
                return " ".join(words[start:end])

        return ""
