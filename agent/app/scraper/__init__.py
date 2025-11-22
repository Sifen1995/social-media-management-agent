"""
Scraper module for automated brand research.

Enhanced features:
- JavaScript rendering with Playwright
- OCR text extraction from images
- Automatic social profile discovery
- Intelligent data merging and deduplication
"""
from app.scraper.website_scraper import WebsiteScraper
from app.scraper.social_scraper import SocialScraper
from app.scraper.extractor import BrandDataExtractor
from app.scraper.ocr_extractor import OCRExtractor
from app.scraper.social_finder import SocialProfileFinder
from app.scraper.data_merger import DataMerger

__all__ = [
    "WebsiteScraper",
    "SocialScraper",
    "BrandDataExtractor",
    "OCRExtractor",
    "SocialProfileFinder",
    "DataMerger"
]
