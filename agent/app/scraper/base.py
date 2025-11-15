"""
Base utilities for web scraping.
"""
import logging
import re
from typing import Optional, Dict, Any
from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class ScraperBase:
    """Base class for all scrapers with common utilities."""

    def __init__(self, timeout: int = 30):
        """
        Initialize scraper base.

        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def is_valid_url(self, url: str) -> bool:
        """
        Validate URL format.

        Args:
            url: URL to validate

        Returns:
            True if valid, False otherwise
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False

    def normalize_url(self, url: str) -> str:
        """
        Normalize URL by ensuring it has a scheme.

        Args:
            url: URL to normalize

        Returns:
            Normalized URL
        """
        if not url:
            return ""

        url = url.strip()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        return url

    def fetch_html(self, url: str) -> Optional[str]:
        """
        Fetch HTML content from URL using requests.

        Args:
            url: URL to fetch

        Returns:
            HTML content or None if failed
        """
        try:
            response = self.session.get(url, timeout=self.timeout, allow_redirects=True)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.warning(f"Failed to fetch {url}: {str(e)}")
            return None

    def parse_html(self, html: str) -> Optional[BeautifulSoup]:
        """
        Parse HTML content with BeautifulSoup.

        Args:
            html: HTML content

        Returns:
            BeautifulSoup object or None
        """
        try:
            return BeautifulSoup(html, 'html.parser')
        except Exception as e:
            logger.error(f"Failed to parse HTML: {str(e)}")
            return None

    def extract_text_from_soup(self, soup: BeautifulSoup) -> str:
        """
        Extract clean text from BeautifulSoup object.

        Args:
            soup: BeautifulSoup object

        Returns:
            Cleaned text content
        """
        # Remove script and style elements
        for script in soup(["script", "style", "noscript"]):
            script.decompose()

        # Get text
        text = soup.get_text(separator=' ', strip=True)

        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)

        return text

    def extract_meta_tags(self, soup: BeautifulSoup) -> Dict[str, str]:
        """
        Extract meta tags from HTML.

        Args:
            soup: BeautifulSoup object

        Returns:
            Dictionary of meta tag content
        """
        meta_data = {}

        # Description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            meta_data['description'] = meta_desc.get('content', '')

        # OG tags
        og_title = soup.find('meta', property='og:title')
        if og_title:
            meta_data['og_title'] = og_title.get('content', '')

        og_description = soup.find('meta', property='og:description')
        if og_description:
            meta_data['og_description'] = og_description.get('content', '')

        # Twitter tags
        twitter_desc = soup.find('meta', attrs={'name': 'twitter:description'})
        if twitter_desc:
            meta_data['twitter_description'] = twitter_desc.get('content', '')

        return meta_data

    def extract_json_ld(self, soup: BeautifulSoup) -> list:
        """
        Extract JSON-LD structured data.

        Args:
            soup: BeautifulSoup object

        Returns:
            List of JSON-LD objects
        """
        import json

        json_ld_data = []
        scripts = soup.find_all('script', type='application/ld+json')

        for script in scripts:
            try:
                data = json.loads(script.string)
                json_ld_data.append(data)
            except (json.JSONDecodeError, TypeError):
                continue

        return json_ld_data

    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text.

        Args:
            text: Text to clean

        Returns:
            Cleaned text
        """
        if not text:
            return ""

        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?;:()\-\'\"\/]', '', text)
        return text.strip()
