"""
OCR Text Extractor - Extracts text from images on webpages.

Supports:
- Image download and processing
- Tesseract OCR for text extraction
- Smart image filtering (only process likely text-containing images)
- Memory-efficient processing (no disk storage)
"""
import logging
import io
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class OCRExtractor:
    """
    Extracts text from images using Tesseract OCR.

    Only processes images when:
    - Website has insufficient text content
    - Images are large enough to contain meaningful text
    - Images appear to be informational (not icons/logos)
    """

    def __init__(self, min_image_size: int = 30000, max_images: int = 5):
        """
        Initialize OCR extractor.

        Args:
            min_image_size: Minimum image size in bytes to process
            max_images: Maximum number of images to process per page
        """
        self.min_image_size = min_image_size
        self.max_images = max_images
        self.ocr_available = self._check_ocr_availability()

    def _check_ocr_availability(self) -> bool:
        """
        Check if OCR dependencies are available.

        Returns:
            True if OCR is available, False otherwise
        """
        try:
            from PIL import Image
            import pytesseract
            # Try a simple test
            pytesseract.get_tesseract_version()
            return True
        except Exception as e:
            logger.warning(f"OCR not available: {str(e)}. Install tesseract-ocr to enable image text extraction.")
            return False

    def should_use_ocr(self, text_content: str, threshold: int = 200) -> bool:
        """
        Determine if OCR should be used based on extracted text length.

        Args:
            text_content: Already extracted text content
            threshold: Minimum text length to skip OCR

        Returns:
            True if OCR should be attempted, False otherwise
        """
        if not self.ocr_available:
            return False

        # Use OCR if text is insufficient
        clean_text = text_content.strip()
        return len(clean_text) < threshold

    def extract_from_page(
        self,
        html: str,
        base_url: str,
        existing_text_length: int = 0
    ) -> Dict[str, Any]:
        """
        Extract text from images in HTML page.

        Args:
            html: HTML content
            base_url: Base URL for resolving relative image paths
            existing_text_length: Length of text already extracted

        Returns:
            Dictionary with OCR results
        """
        if not self.ocr_available:
            return {
                "success": False,
                "error": "OCR not available",
                "extracted_text": "",
                "images_processed": 0
            }

        if not self.should_use_ocr("x" * existing_text_length, threshold=200):
            return {
                "success": False,
                "error": "Sufficient text already extracted",
                "extracted_text": "",
                "images_processed": 0
            }

        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')

            # Find all images
            images = self._find_processable_images(soup, base_url)

            if not images:
                return {
                    "success": True,
                    "extracted_text": "",
                    "images_processed": 0,
                    "message": "No suitable images found for OCR"
                }

            # Process images
            extracted_texts = []
            processed_count = 0

            for img_url in images[:self.max_images]:
                text = self._extract_text_from_image_url(img_url)
                if text and len(text.strip()) > 10:  # Only keep meaningful text
                    extracted_texts.append(text)
                    processed_count += 1

            combined_text = "\n\n".join(extracted_texts)

            return {
                "success": True,
                "extracted_text": combined_text,
                "images_processed": processed_count,
                "total_images_found": len(images)
            }

        except Exception as e:
            logger.error(f"OCR extraction failed: {str(e)}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "extracted_text": "",
                "images_processed": 0
            }

    def _find_processable_images(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """
        Find images that are likely to contain text.

        Args:
            soup: BeautifulSoup object
            base_url: Base URL for resolving paths

        Returns:
            List of image URLs
        """
        image_urls = []

        # Find img tags
        for img in soup.find_all('img'):
            src = img.get('src') or img.get('data-src')
            if not src:
                continue

            # Skip common non-text images
            if any(skip in src.lower() for skip in ['logo', 'icon', 'avatar', 'emoji', 'button']):
                continue

            # Resolve relative URLs
            full_url = urljoin(base_url, src)

            # Only process http/https images
            if full_url.startswith(('http://', 'https://')):
                # Check alt text for hints this might contain text
                alt = img.get('alt', '').lower()
                if any(hint in alt for hint in ['infographic', 'chart', 'graph', 'slide', 'screenshot']):
                    # Prioritize these
                    image_urls.insert(0, full_url)
                else:
                    image_urls.append(full_url)

        return image_urls

    def _extract_text_from_image_url(self, image_url: str) -> Optional[str]:
        """
        Download image and extract text using OCR.

        Args:
            image_url: URL of image to process

        Returns:
            Extracted text or None
        """
        try:
            from PIL import Image
            import pytesseract

            # Download image
            response = requests.get(image_url, timeout=10, stream=True)
            response.raise_for_status()

            # Check size
            content_length = response.headers.get('content-length')
            if content_length and int(content_length) < self.min_image_size:
                logger.debug(f"Skipping small image: {image_url}")
                return None

            # Load image from bytes (memory only, no disk)
            image_data = io.BytesIO(response.content)
            image = Image.open(image_data)

            # Skip very small images (likely icons)
            width, height = image.size
            if width < 200 or height < 200:
                logger.debug(f"Skipping small image dimensions: {width}x{height}")
                return None

            # Perform OCR
            text = pytesseract.image_to_string(image, lang='eng')

            # Clean up
            image.close()
            image_data.close()

            return text.strip()

        except requests.RequestException as e:
            logger.debug(f"Failed to download image {image_url}: {str(e)}")
            return None
        except Exception as e:
            logger.debug(f"OCR failed for {image_url}: {str(e)}")
            return None

    def extract_from_image_bytes(self, image_bytes: bytes) -> Optional[str]:
        """
        Extract text from image bytes directly.

        Args:
            image_bytes: Image data as bytes

        Returns:
            Extracted text or None
        """
        if not self.ocr_available:
            return None

        try:
            from PIL import Image
            import pytesseract

            image_data = io.BytesIO(image_bytes)
            image = Image.open(image_data)

            text = pytesseract.image_to_string(image, lang='eng')

            image.close()
            image_data.close()

            return text.strip()

        except Exception as e:
            logger.error(f"OCR from bytes failed: {str(e)}")
            return None
