"""
Data extractor for normalizing and preparing scraped data for LLM processing.
"""
import logging
from typing import Dict, List, Any, Optional
from collections import Counter

logger = logging.getLogger(__name__)


class BrandDataExtractor:
    """
    Extracts and normalizes brand data from scraped website and social media content.
    Prepares data for LLM analysis.
    """

    def extract_and_normalize(
        self,
        website_data: Dict[str, Any],
        social_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Extract and normalize data from both website and social scraping.

        Args:
            website_data: Scraped website data
            social_data: Scraped social media data

        Returns:
            Normalized data ready for LLM processing
        """
        normalized = {
            "website": self._normalize_website_data(website_data),
            "social": self._normalize_social_data(social_data),
            "combined_text": "",
            "key_insights": {},
            "metadata": {}
        }

        # Generate combined text for LLM
        normalized["combined_text"] = self._generate_combined_text(normalized)

        # Extract key insights
        normalized["key_insights"] = self._extract_key_insights(normalized)

        # Add metadata
        normalized["metadata"] = {
            "website_scraped": not website_data.get("error"),
            "social_platforms_scraped": len(social_data.get("platforms", {})),
            "total_hashtags_found": len(social_data.get("combined_insights", {}).get("all_hashtags", [])),
            "total_captions_found": len(social_data.get("combined_insights", {}).get("all_captions", []))
        }

        return normalized

    def _normalize_website_data(self, website_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize website scraped data (enhanced to handle new data sources).

        Args:
            website_data: Raw website data

        Returns:
            Normalized website data
        """
        if website_data.get("error"):
            return {"error": website_data["error"], "available": False}

        # Use final_corpus if available (from enhanced scraper), otherwise fallback to raw_text
        all_text = website_data.get("final_corpus") or website_data.get("raw_text", "")

        normalized = {
            "available": True,
            "base_url": website_data.get("base_url", ""),
            "meta_description": "",
            "organization_name": "",
            "key_sections": {},
            "all_text": all_text,
            "structured_data": website_data.get("structured_data", []),
            "extraction_metadata": website_data.get("extraction_metadata", {})
        }

        # Extract meta description
        meta_data = website_data.get("meta_data", {})
        normalized["meta_description"] = (
            meta_data.get("description") or
            meta_data.get("og_description") or
            ""
        )

        # Extract organization info from structured data
        for json_ld in website_data.get("structured_data", []):
            if isinstance(json_ld, dict) and json_ld.get("@type") == "Organization":
                normalized["organization_name"] = json_ld.get("name", "")
                break

        # Extract key sections
        extracted_sections = website_data.get("extracted_sections", {})
        normalized["key_sections"] = {
            "mission": extracted_sections.get("mission", ""),
            "vision": extracted_sections.get("vision", ""),
            "values": extracted_sections.get("values", ""),
            "meta_description": extracted_sections.get("meta_description", "")
        }

        return normalized

    def _normalize_social_data(self, social_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize social media scraped data.

        Args:
            social_data: Raw social media data

        Returns:
            Normalized social data
        """
        if not social_data.get("platforms"):
            return {"available": False, "platforms": {}}

        combined = social_data.get("combined_insights", {})

        normalized = {
            "available": True,
            "platforms_scraped": list(social_data.get("platforms", {}).keys()),
            "platform_data": {},
            "combined_insights": {
                "all_captions": combined.get("all_captions", []),
                "frequent_hashtags": self._get_most_common(combined.get("all_hashtags", []), top_n=20),
                "tone_patterns": self._get_most_common(combined.get("tone_indicators", []), top_n=10),
                "content_themes": combined.get("content_themes", []),
                "writing_style_summary": ""
            }
        }

        # Process each platform
        for platform_name, platform_data in social_data.get("platforms", {}).items():
            normalized["platform_data"][platform_name] = {
                "bio": platform_data.get("bio") or platform_data.get("description", ""),
                "username": platform_data.get("username") or platform_data.get("page_name", ""),
                "hashtags": platform_data.get("hashtags", []),
                "captions_sample": platform_data.get("captions", [])[:3],
                "tone": platform_data.get("tone_indicators", [])
            }

        # Generate writing style summary
        normalized["combined_insights"]["writing_style_summary"] = self._analyze_writing_style(
            combined.get("all_captions", [])
        )

        return normalized

    def _generate_combined_text(self, normalized_data: Dict[str, Any]) -> str:
        """
        Generate combined text from all sources for LLM processing.

        Args:
            normalized_data: Normalized data

        Returns:
            Combined text string
        """
        sections = []

        # Website data
        website = normalized_data.get("website", {})
        if website.get("available"):
            sections.append("=== WEBSITE DATA ===")

            if website.get("organization_name"):
                sections.append(f"Organization Name: {website['organization_name']}")

            if website.get("meta_description"):
                sections.append(f"Meta Description: {website['meta_description']}")

            key_sections = website.get("key_sections", {})
            if key_sections.get("mission"):
                sections.append(f"Mission: {key_sections['mission']}")
            if key_sections.get("vision"):
                sections.append(f"Vision: {key_sections['vision']}")
            if key_sections.get("values"):
                sections.append(f"Values: {key_sections['values']}")

            # Add sample of full text (first 2000 characters)
            all_text = website.get("all_text", "")
            if all_text:
                sections.append(f"Website Content Sample: {all_text[:2000]}")

        # Social media data
        social = normalized_data.get("social", {})
        if social.get("available"):
            sections.append("\n=== SOCIAL MEDIA DATA ===")

            sections.append(f"Platforms: {', '.join(social.get('platforms_scraped', []))}")

            # Platform-specific data
            for platform_name, platform_data in social.get("platform_data", {}).items():
                sections.append(f"\n{platform_name.upper()}:")
                if platform_data.get("bio"):
                    sections.append(f"  Bio: {platform_data['bio']}")
                if platform_data.get("captions_sample"):
                    sections.append(f"  Sample Captions: {' | '.join(platform_data['captions_sample'][:3])}")

            # Combined insights
            insights = social.get("combined_insights", {})
            if insights.get("frequent_hashtags"):
                top_hashtags = [f"#{tag}" for tag, _ in insights["frequent_hashtags"][:10]]
                sections.append(f"\nMost Used Hashtags: {', '.join(top_hashtags)}")

            if insights.get("tone_patterns"):
                tones = [tone for tone, _ in insights["tone_patterns"]]
                sections.append(f"Detected Tones: {', '.join(tones)}")

            if insights.get("content_themes"):
                sections.append(f"Content Themes: {', '.join(insights['content_themes'])}")

            if insights.get("all_captions"):
                sections.append(f"\nSample Captions:\n" + "\n".join([f"- {cap[:200]}" for cap in insights["all_captions"][:5]]))

        return "\n".join(sections)

    def _extract_key_insights(self, normalized_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract key insights from normalized data (enhanced for new data sources).

        Args:
            normalized_data: Normalized data

        Returns:
            Dictionary of key insights
        """
        insights = {
            "has_website_data": False,
            "has_social_data": False,
            "brand_name_candidates": [],
            "top_hashtags": [],
            "dominant_tones": [],
            "content_themes": [],
            "data_quality": "insufficient",
            "extraction_methods_used": []
        }

        # Check website data
        website = normalized_data.get("website", {})
        if website.get("available"):
            insights["has_website_data"] = True
            if website.get("organization_name"):
                insights["brand_name_candidates"].append(website["organization_name"])

            # Track enhanced extraction methods
            extraction_meta = website.get("extraction_metadata", {})
            if extraction_meta.get("used_js_rendering"):
                insights["extraction_methods_used"].append("javascript_rendering")
            if extraction_meta.get("used_ocr"):
                insights["extraction_methods_used"].append("ocr")

            # Use enhanced data quality assessment if available
            if extraction_meta.get("data_quality"):
                website_quality = extraction_meta["data_quality"]
            else:
                # Fallback to text length assessment
                text_length = len(website.get("all_text", ""))
                if text_length > 1500:
                    website_quality = "excellent"
                elif text_length > 500:
                    website_quality = "good"
                elif text_length > 150:
                    website_quality = "fair"
                else:
                    website_quality = "poor"

        # Check social data
        social = normalized_data.get("social", {})
        if social.get("available"):
            insights["has_social_data"] = True
            insights["extraction_methods_used"].append("social_media")

            combined = social.get("combined_insights", {})

            # Top hashtags
            if combined.get("frequent_hashtags"):
                insights["top_hashtags"] = [tag for tag, _ in combined["frequent_hashtags"][:10]]

            # Dominant tones
            if combined.get("tone_patterns"):
                insights["dominant_tones"] = [tone for tone, _ in combined["tone_patterns"][:5]]

            # Content themes
            insights["content_themes"] = combined.get("content_themes", [])

        # Enhanced data quality assessment
        if insights["has_website_data"] and insights["has_social_data"]:
            # Both sources available
            if website_quality in ["excellent", "good"]:
                insights["data_quality"] = "excellent"
            else:
                insights["data_quality"] = "good"
        elif insights["has_website_data"]:
            # Only website data
            insights["data_quality"] = website_quality
        elif insights["has_social_data"]:
            # Only social data
            insights["data_quality"] = "fair"
        else:
            insights["data_quality"] = "insufficient"

        return insights

    def _get_most_common(self, items: List[str], top_n: int = 10) -> List[tuple]:
        """
        Get most common items from a list.

        Args:
            items: List of items
            top_n: Number of top items to return

        Returns:
            List of (item, count) tuples
        """
        if not items:
            return []

        counter = Counter(items)
        return counter.most_common(top_n)

    def _analyze_writing_style(self, captions: List[str]) -> str:
        """
        Analyze writing style from captions.

        Args:
            captions: List of captions

        Returns:
            Writing style summary
        """
        if not captions:
            return "No captions available for analysis"

        # Combine all captions
        all_text = " ".join(captions)

        style_notes = []

        # Average length
        avg_length = sum(len(cap) for cap in captions) / len(captions)
        if avg_length < 50:
            style_notes.append("concise")
        elif avg_length > 200:
            style_notes.append("detailed")
        else:
            style_notes.append("moderate length")

        # Check for emojis
        emoji_pattern = r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]'
        import re
        if re.search(emoji_pattern, all_text):
            style_notes.append("uses emojis")

        # Check for questions
        if "?" in all_text:
            style_notes.append("asks questions")

        # Check for calls to action
        cta_words = ["click", "shop", "buy", "learn", "discover", "explore", "join", "sign up"]
        if any(word in all_text.lower() for word in cta_words):
            style_notes.append("includes CTAs")

        # Check for hashtags
        if "#" in all_text:
            style_notes.append("uses hashtags")

        return ", ".join(style_notes)

    def prepare_for_llm(self, normalized_data: Dict[str, Any]) -> str:
        """
        Prepare final prompt text for LLM analysis.

        Args:
            normalized_data: Normalized data

        Returns:
            Formatted text for LLM
        """
        combined_text = normalized_data.get("combined_text", "")
        key_insights = normalized_data.get("key_insights", {})

        prompt_parts = [
            "Analyze the following brand data and extract a comprehensive brand profile:",
            "",
            combined_text,
            "",
            "=== ADDITIONAL CONTEXT ===",
            f"Data Quality: {key_insights.get('data_quality', 'unknown')}",
            f"Website Data Available: {key_insights.get('has_website_data', False)}",
            f"Social Media Data Available: {key_insights.get('has_social_data', False)}",
        ]

        if key_insights.get("top_hashtags"):
            prompt_parts.append(f"Key Hashtags: {', '.join([f'#{h}' for h in key_insights['top_hashtags'][:5]])}")

        return "\n".join(prompt_parts)
