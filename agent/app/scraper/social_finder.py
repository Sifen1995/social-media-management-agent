"""
Social Profile Finder - Automatically discovers social media profiles.

Strategies:
1. Extract social links from website HTML
2. Search for profiles based on company/domain name
3. Validate and return discovered profiles
"""
import logging
import re
from typing import Dict, List, Optional, Set
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import requests

logger = logging.getLogger(__name__)


class SocialProfileFinder:
    """
    Finds social media profiles for a brand/company.

    Methods:
    - Extract from website HTML (footer, header, social icons)
    - Search by company name
    - Validate profile accessibility
    """

    # Common social media domains and patterns
    SOCIAL_PATTERNS = {
        'instagram': {
            'domains': ['instagram.com', 'www.instagram.com'],
            'pattern': r'(?:https?://)?(?:www\.)?instagram\.com/([^/\s?]+)',
            'base_url': 'https://www.instagram.com/'
        },
        'linkedin': {
            'domains': ['linkedin.com', 'www.linkedin.com'],
            'pattern': r'(?:https?://)?(?:www\.)?linkedin\.com/(?:company|in)/([^/\s?]+)',
            'base_url': 'https://www.linkedin.com/company/'
        },
        'twitter': {
            'domains': ['twitter.com', 'www.twitter.com', 'x.com', 'www.x.com'],
            'pattern': r'(?:https?://)?(?:www\.)?(?:twitter|x)\.com/([^/\s?]+)',
            'base_url': 'https://twitter.com/'
        },
        'facebook': {
            'domains': ['facebook.com', 'www.facebook.com', 'fb.com'],
            'pattern': r'(?:https?://)?(?:www\.)?(?:facebook|fb)\.com/([^/\s?]+)',
            'base_url': 'https://www.facebook.com/'
        },
        'tiktok': {
            'domains': ['tiktok.com', 'www.tiktok.com'],
            'pattern': r'(?:https?://)?(?:www\.)?tiktok\.com/@([^/\s?]+)',
            'base_url': 'https://www.tiktok.com/@'
        },
        'youtube': {
            'domains': ['youtube.com', 'www.youtube.com'],
            'pattern': r'(?:https?://)?(?:www\.)?youtube\.com/(?:c/|channel/|user/|@)?([^/\s?]+)',
            'base_url': 'https://www.youtube.com/'
        }
    }

    def __init__(self, timeout: int = 15):
        """
        Initialize social profile finder.

        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def find_profiles_from_website(self, website_url: str, html: Optional[str] = None) -> Dict[str, str]:
        """
        Extract social media profiles from website HTML.

        Args:
            website_url: Website URL
            html: Optional HTML content (if already fetched)

        Returns:
            Dictionary of platform -> URL
        """
        if not html:
            html = self._fetch_html(website_url)

        if not html:
            logger.warning(f"Could not fetch HTML from {website_url}")
            return {}

        soup = BeautifulSoup(html, 'html.parser')

        profiles = {}

        # Strategy 1: Find links in footer, header, and social sections
        social_links = self._extract_social_links(soup)

        # Strategy 2: Look for meta tags
        meta_profiles = self._extract_from_meta_tags(soup)

        # Merge results
        profiles.update(social_links)
        profiles.update(meta_profiles)

        logger.info(f"Found {len(profiles)} social profiles from website")
        return profiles

    def find_profiles_by_search(self, company_name: str, domain: Optional[str] = None) -> Dict[str, str]:
        """
        Search for social profiles by company name.

        Args:
            company_name: Company/brand name
            domain: Optional domain name for validation

        Returns:
            Dictionary of platform -> URL
        """
        profiles = {}

        # Extract brand name from domain if provided
        if domain:
            parsed = urlparse(domain if domain.startswith('http') else f'https://{domain}')
            domain_name = parsed.netloc.replace('www.', '').split('.')[0]
        else:
            domain_name = None

        # Try common username patterns
        search_terms = [
            company_name.lower().replace(' ', ''),
            company_name.lower().replace(' ', '_'),
            company_name.lower().replace(' ', '-'),
        ]

        if domain_name:
            search_terms.append(domain_name.lower())

        # Try to construct likely profile URLs
        for platform, config in self.SOCIAL_PATTERNS.items():
            for term in search_terms:
                # Clean term (alphanumeric and underscores only for most platforms)
                clean_term = re.sub(r'[^a-zA-Z0-9_-]', '', term)
                if not clean_term:
                    continue

                # Construct potential URL
                if platform == 'tiktok':
                    potential_url = f"{config['base_url']}{clean_term}"
                elif platform == 'linkedin':
                    potential_url = f"{config['base_url']}{clean_term}"
                else:
                    potential_url = f"{config['base_url']}{clean_term}"

                # Quick validation (just check if URL is accessible)
                # Note: This is lightweight and doesn't guarantee accuracy
                if self._quick_validate_url(potential_url):
                    profiles[platform] = potential_url
                    logger.info(f"Found {platform} profile: {potential_url}")
                    break  # Found one for this platform, move to next

        return profiles

    def find_all_profiles(
        self,
        website_url: str,
        company_name: Optional[str] = None,
        html: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Find all social profiles using multiple strategies.

        Args:
            website_url: Website URL
            company_name: Optional company name for search
            html: Optional pre-fetched HTML

        Returns:
            Dictionary of platform -> URL
        """
        all_profiles = {}

        # Strategy 1: Extract from website
        website_profiles = self.find_profiles_from_website(website_url, html)
        all_profiles.update(website_profiles)

        # Strategy 2: Search by company name (if not all found)
        if company_name and len(all_profiles) < 3:
            domain = website_url
            search_profiles = self.find_profiles_by_search(company_name, domain)

            # Only add if not already found
            for platform, url in search_profiles.items():
                if platform not in all_profiles:
                    all_profiles[platform] = url

        return all_profiles

    def _extract_social_links(self, soup: BeautifulSoup) -> Dict[str, str]:
        """
        Extract social media links from HTML.

        Args:
            soup: BeautifulSoup object

        Returns:
            Dictionary of platform -> URL
        """
        profiles = {}
        found_urls: Set[str] = set()

        # Find all links
        for link in soup.find_all('a', href=True):
            href = link['href']

            # Check each social platform
            for platform, config in self.SOCIAL_PATTERNS.items():
                # Check if link matches this platform
                if any(domain in href for domain in config['domains']):
                    match = re.search(config['pattern'], href)
                    if match:
                        # Construct clean URL
                        username = match.group(1)
                        # Skip generic/common paths
                        if username.lower() in ['share', 'sharer', 'intent', 'widgets', 'home', 'login']:
                            continue

                        if platform == 'tiktok':
                            clean_url = f"{config['base_url']}{username}"
                        elif platform == 'youtube':
                            clean_url = href  # Keep original YouTube URL
                        else:
                            clean_url = f"{config['base_url']}{username}"

                        # Avoid duplicates
                        if clean_url not in found_urls:
                            profiles[platform] = clean_url
                            found_urls.add(clean_url)

        return profiles

    def _extract_from_meta_tags(self, soup: BeautifulSoup) -> Dict[str, str]:
        """
        Extract social profiles from meta tags.

        Args:
            soup: BeautifulSoup object

        Returns:
            Dictionary of platform -> URL
        """
        profiles = {}

        # Check Open Graph tags
        og_tags = soup.find_all('meta', property=re.compile(r'og:.*'))
        for tag in og_tags:
            content = tag.get('content', '')
            for platform, config in self.SOCIAL_PATTERNS.items():
                if any(domain in content for domain in config['domains']):
                    match = re.search(config['pattern'], content)
                    if match and platform not in profiles:
                        profiles[platform] = content

        # Check for specific social meta tags
        social_metas = [
            ('twitter:site', 'twitter'),
            ('twitter:creator', 'twitter')
        ]

        for meta_name, platform in social_metas:
            tag = soup.find('meta', attrs={'name': meta_name})
            if tag and platform not in profiles:
                content = tag.get('content', '')
                if content.startswith('@'):
                    username = content[1:]
                    profiles[platform] = f"{self.SOCIAL_PATTERNS[platform]['base_url']}{username}"

        return profiles

    def _fetch_html(self, url: str) -> Optional[str]:
        """
        Fetch HTML from URL.

        Args:
            url: URL to fetch

        Returns:
            HTML content or None
        """
        try:
            response = self.session.get(url, timeout=self.timeout, allow_redirects=True)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.debug(f"Failed to fetch {url}: {str(e)}")
            return None

    def _quick_validate_url(self, url: str) -> bool:
        """
        Quick validation to check if URL is accessible.

        Args:
            url: URL to validate

        Returns:
            True if accessible, False otherwise
        """
        try:
            response = self.session.head(url, timeout=5, allow_redirects=True)
            # Accept 200 OK or 999 (some sites like LinkedIn return this for bots)
            return response.status_code in [200, 999] or response.status_code < 400
        except Exception:
            return False
