"""
Data Merger - Combines and deduplicates data from multiple scraping sources.

Handles:
- Text deduplication
- Content cleaning
- Source tracking
- Quality assessment
"""
import logging
import re
import html
from typing import Dict, List, Any, Set
from difflib import SequenceMatcher

logger = logging.getLogger(__name__)


class DataMerger:
    """
    Merges data from multiple scraping sources into unified corpus.

    Sources:
    - Standard HTML scraping
    - JavaScript-rendered content
    - OCR from images
    - Social media profiles
    """

    # Minimum sentence length to keep
    MIN_SENTENCE_LENGTH = 8

    # Common junk patterns to remove
    JUNK_PATTERNS = [
        r'cookie\s+(?:policy|consent|notice|settings)',
        r'privacy\s+(?:policy|notice|statement)',
        r'terms\s+(?:of\s+(?:service|use)|and\s+conditions)',
        r'all\s+rights\s+reserved',
        r'copyright\s+©',
        r'skip\s+to\s+(?:content|main|navigation)',
        r'accept\s+(?:all\s+)?cookies',
        r'manage\s+cookies',
        r'sign\s+(?:in|up|out)',
        r'log\s+(?:in|out)',
        r'subscribe\s+to\s+(?:our\s+)?newsletter',
        r'follow\s+us\s+on',
        r'share\s+on\s+(?:facebook|twitter|instagram)',
        r'back\s+to\s+top',
        r'home\s+›\s+',  # Breadcrumbs
        r'search\s+for:?',
        r'menu\s+toggle',
        r'close\s+menu'
    ]

    def __init__(self, similarity_threshold: float = 0.85):
        """
        Initialize data merger.

        Args:
            similarity_threshold: Threshold for considering text as duplicate (0-1)
        """
        self.similarity_threshold = similarity_threshold

    def merge_all_sources(
        self,
        raw_website_text: str = "",
        raw_js_text: str = "",
        raw_ocr_text: str = "",
        social_media_text: str = "",
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Merge all text sources into unified corpus.

        Args:
            raw_website_text: Text from standard HTML scraping
            raw_js_text: Text from JS-rendered content
            raw_ocr_text: Text extracted from images via OCR
            social_media_text: Text from social media profiles
            metadata: Additional metadata about sources

        Returns:
            Dictionary with merged data
        """
        result = {
            "raw_website_text": raw_website_text,
            "raw_js_text": raw_js_text,
            "raw_ocr_text": raw_ocr_text,
            "social_media_text": social_media_text,
            "final_corpus": "",
            "sources_used": [],
            "metadata": metadata or {},
            "stats": {
                "total_chars_before": 0,
                "total_chars_after": 0,
                "duplicates_removed": 0,
                "sentences_cleaned": 0
            }
        }

        # Track which sources provided data
        if raw_website_text.strip():
            result["sources_used"].append("website")
        if raw_js_text.strip():
            result["sources_used"].append("javascript")
        if raw_ocr_text.strip():
            result["sources_used"].append("ocr")
        if social_media_text.strip():
            result["sources_used"].append("social_media")

        # Combine all text
        all_texts = [
            ("website", raw_website_text),
            ("javascript", raw_js_text),
            ("ocr", raw_ocr_text),
            ("social", social_media_text)
        ]

        # Clean each text source
        cleaned_texts = []
        total_before = 0

        for source_name, text in all_texts:
            if not text or not text.strip():
                continue

            total_before += len(text)
            cleaned = self._clean_text(text)

            if cleaned:
                cleaned_texts.append(cleaned)

        # Deduplicate across all sources
        final_corpus = self._deduplicate_texts(cleaned_texts)

        # Final cleaning pass
        final_corpus = self._final_cleanup(final_corpus)

        # Update results
        result["final_corpus"] = final_corpus
        result["stats"]["total_chars_before"] = total_before
        result["stats"]["total_chars_after"] = len(final_corpus)
        result["stats"]["compression_ratio"] = (
            round(len(final_corpus) / total_before, 2) if total_before > 0 else 0
        )

        # Add metadata flags
        result["metadata"].update({
            "has_js_content": bool(raw_js_text.strip()),
            "has_ocr_content": bool(raw_ocr_text.strip()),
            "has_social_fallback": bool(social_media_text.strip()),
            "sources_count": len(result["sources_used"])
        })

        return result

    def _clean_text(self, text: str) -> str:
        """
        Clean individual text block.

        Args:
            text: Text to clean

        Returns:
            Cleaned text
        """
        if not text:
            return ""

        # Decode HTML entities
        text = html.unescape(text)

        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)

        # Remove navigation/UI junk
        for pattern in self.JUNK_PATTERNS:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)

        # Split into sentences
        sentences = self._split_into_sentences(text)

        # Filter sentences
        cleaned_sentences = []
        for sentence in sentences:
            # Skip short or junk sentences
            if len(sentence) < self.MIN_SENTENCE_LENGTH:
                continue

            # Skip if mostly punctuation or numbers
            alpha_chars = sum(c.isalpha() for c in sentence)
            if alpha_chars < len(sentence) * 0.5:
                continue

            # Skip likely UI text (all caps, very short)
            if sentence.isupper() and len(sentence) < 30:
                continue

            cleaned_sentences.append(sentence)

        return ' '.join(cleaned_sentences)

    def _split_into_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences.

        Args:
            text: Text to split

        Returns:
            List of sentences
        """
        # Simple sentence splitting
        sentences = re.split(r'[.!?]\s+', text)
        return [s.strip() for s in sentences if s.strip()]

    def _deduplicate_texts(self, texts: List[str]) -> str:
        """
        Remove duplicate content across multiple text blocks.

        Args:
            texts: List of text blocks

        Returns:
            Deduplicated combined text
        """
        if not texts:
            return ""

        if len(texts) == 1:
            return texts[0]

        # Split all texts into sentences
        all_sentences = []
        for text in texts:
            sentences = self._split_into_sentences(text)
            all_sentences.extend(sentences)

        # Deduplicate sentences
        unique_sentences = []
        seen_hashes: Set[str] = set()

        for sentence in all_sentences:
            # Normalize for comparison
            normalized = sentence.lower().strip()

            # Quick hash-based deduplication
            sentence_hash = hash(normalized)
            if sentence_hash in seen_hashes:
                continue

            # Check similarity with existing sentences
            is_duplicate = False
            for existing in unique_sentences[-10:]:  # Only check last 10 for performance
                similarity = self._calculate_similarity(normalized, existing.lower())
                if similarity >= self.similarity_threshold:
                    is_duplicate = True
                    break

            if not is_duplicate:
                unique_sentences.append(sentence)
                seen_hashes.add(sentence_hash)

        return ' '.join(unique_sentences)

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate similarity between two text strings.

        Args:
            text1: First text
            text2: Second text

        Returns:
            Similarity score (0-1)
        """
        return SequenceMatcher(None, text1, text2).ratio()

    def _final_cleanup(self, text: str) -> str:
        """
        Final cleanup pass on merged text.

        Args:
            text: Text to clean

        Returns:
            Cleaned text
        """
        if not text:
            return ""

        # Remove multiple spaces
        text = re.sub(r'\s+', ' ', text)

        # Remove common artifacts
        text = re.sub(r'\s+[.,;:]\s+', '. ', text)
        text = re.sub(r'\.{2,}', '.', text)

        # Ensure proper spacing after punctuation
        text = re.sub(r'([.!?])([A-Z])', r'\1 \2', text)

        # Remove control characters
        text = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f-\x9f]', '', text)

        # Final trim
        text = text.strip()

        return text

    def assess_data_quality(self, merged_data: Dict[str, Any]) -> str:
        """
        Assess quality of merged data.

        Args:
            merged_data: Result from merge_all_sources

        Returns:
            Quality rating: "excellent", "good", "fair", "poor", "insufficient"
        """
        final_corpus = merged_data.get("final_corpus", "")
        corpus_length = len(final_corpus)
        sources_count = merged_data["metadata"].get("sources_count", 0)

        # Insufficient data
        if corpus_length < 100:
            return "insufficient"

        # Poor quality
        if corpus_length < 300:
            return "poor"

        # Fair quality
        if corpus_length < 800:
            return "fair"

        # Good quality
        if corpus_length < 2000 or sources_count < 2:
            return "good"

        # Excellent quality
        return "excellent"
