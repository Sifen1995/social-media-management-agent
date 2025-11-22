# Enhanced Web Scraping Guide

## Overview

The social media management agent now includes **advanced web scraping capabilities** that can extract brand information even from challenging websites with minimal text, JavaScript-rendered content, or image-based content.

## New Features

### 1. **JavaScript Rendering Fallback**
Automatically detects when standard HTML scraping is insufficient and falls back to Playwright-powered browser automation.

**How it works:**
- Attempts standard `requests` scraping first
- If extracted text < 300 characters, automatically switches to Playwright
- Renders JavaScript and waits for page to fully load
- Extracts DOM content after all dynamic content is rendered

**Benefits:**
- Works with React, Vue, Angular, and other JS framework sites
- Handles lazy-loaded content
- Captures dynamic content that's not in initial HTML

### 2. **OCR Text Extraction**
Extracts text from images when websites use graphics instead of HTML text.

**How it works:**
- Detects images likely to contain text (infographics, charts, screenshots)
- Downloads images to memory (no disk storage)
- Uses Tesseract OCR to extract readable text
- Filters and includes meaningful text in final corpus

**Benefits:**
- Captures brand information from image-based designs
- Works with infographics and presentation slides
- No manual intervention needed

**Requirements:**
```bash
# Install Tesseract OCR engine
# Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
# Mac: brew install tesseract
# Linux: apt-get install tesseract-ocr

# Python packages (already in requirements.txt)
pip install pytesseract Pillow
```

### 3. **Automatic Social Profile Discovery**
Automatically finds social media profiles when not provided.

**How it works:**
- Extracts social links from website footer/header
- Parses social meta tags
- Constructs likely profile URLs from company name
- Validates profile accessibility

**Platforms supported:**
- Instagram
- LinkedIn (company pages)
- Twitter/X
- Facebook
- TikTok
- YouTube

### 4. **Intelligent Data Merging**
Combines data from multiple sources with deduplication.

**How it works:**
- Merges text from: standard HTML, JS-rendered content, OCR, social media
- Removes duplicate sentences using similarity matching
- Filters navigation/UI junk text
- Cleans and normalizes Unicode and HTML entities

**Benefits:**
- No duplicate information in final output
- Clean, meaningful text corpus
- Efficient compression while retaining all unique information

## Usage

### Basic Usage (Auto-enabled)

The enhanced features are **enabled by default** in the Brand Profile Agent:

```python
from app.agents.brand_profile.agent import BrandProfileAgent

agent = BrandProfileAgent()

# All enhancements are auto-enabled
result = await agent.execute({
    "website": "https://cgoncology.com",
    "company_name": "CG Oncology"  # Optional, helps with social discovery
}, context={})
```

### Advanced Configuration

You can control each feature individually:

```python
result = await agent.execute({
    "website": "https://example.com",
    "company_name": "Example Corp",

    # Scraping options (all True by default)
    "use_playwright": True,        # Enable Playwright browser
    "auto_js_fallback": True,       # Auto-detect need for JS rendering
    "use_ocr": True,                # Enable OCR extraction
    "auto_find_socials": True       # Auto-discover social profiles
}, context={})
```

### Direct Scraper Usage

For advanced use cases, use scrapers directly:

```python
from app.scraper.website_scraper import WebsiteScraper

scraper = WebsiteScraper(
    timeout=30,
    use_playwright=True,
    auto_js_fallback=True,
    use_ocr=True
)

# Async scraping with all enhancements
result = await scraper.scrape_website_async("https://example.com")

# Check what methods were used
metadata = result['extraction_metadata']
print(f"Used JS rendering: {metadata['used_js_rendering']}")
print(f"Used OCR: {metadata['used_ocr']}")
print(f"Data quality: {metadata['data_quality']}")
print(f"Final corpus length: {len(result['final_corpus'])} chars")
```

## Understanding Results

### Extraction Metadata

Every scraping result includes metadata about extraction:

```python
{
    "extraction_metadata": {
        "used_js_rendering": True,      # JS rendering was needed
        "used_ocr": True,                # OCR was used
        "sources_used": [                # All data sources
            "website",
            "javascript",
            "ocr"
        ],
        "data_quality": "good",          # Quality assessment
        "merge_stats": {
            "total_chars_before": 5200,  # Before deduplication
            "total_chars_after": 1800,   # After deduplication
            "compression_ratio": 0.35    # Efficiency metric
        }
    }
}
```

### Data Quality Ratings

- **excellent**: >2000 chars from multiple sources
- **good**: 800-2000 chars or multiple sources
- **fair**: 300-800 chars from limited sources
- **poor**: 100-300 chars
- **insufficient**: <100 chars (will trigger LLM "not_available" response)

## Testing

### Test Script

Use the included test script to verify functionality:

```bash
# Test a specific website
python agent/test_enhanced_scraper.py --url https://example.com

# Test with company name for social discovery
python agent/test_enhanced_scraper.py --url https://example.com --company "Example Corp"

# Test with known difficult websites
python agent/test_enhanced_scraper.py --test-difficult
```

### Example Test Cases

**JavaScript-Heavy Site:**
```bash
python agent/test_enhanced_scraper.py --url https://cgoncology.com
```

**Image-Heavy Site:**
```bash
# Add your own test cases to test_enhanced_scraper.py
```

## Architecture

### Component Overview

```
┌─────────────────────────────────────────────────────┐
│           BrandProfileAgent                          │
│  (Orchestrates complete workflow)                    │
└────────────────┬────────────────────────────────────┘
                 │
        ┌────────┴────────┐
        │                 │
┌───────▼──────┐   ┌─────▼────────┐
│  Website     │   │   Social     │
│  Scraper     │   │   Scraper    │
└───────┬──────┘   └──────┬───────┘
        │                 │
        │  ┌──────────────┼─────────────────┐
        │  │              │                 │
   ┌────▼──▼───┐   ┌─────▼─────┐   ┌──────▼──────┐
   │  Playwright│   │    OCR    │   │   Social    │
   │  Renderer  │   │ Extractor │   │   Finder    │
   └────┬───────┘   └─────┬─────┘   └──────┬──────┘
        │                 │                 │
        └─────────┬───────┴─────────────────┘
                  │
           ┌──────▼────────┐
           │  Data Merger  │
           │  (Deduplicate)│
           └───────┬───────┘
                   │
          ┌────────▼─────────┐
          │  Brand Data      │
          │  Extractor       │
          └──────────────────┘
```

### Key Modules

1. **`website_scraper.py`**: Enhanced website scraping with fallbacks
2. **`social_scraper.py`**: Social media scraping with Playwright
3. **`ocr_extractor.py`**: Image text extraction via Tesseract
4. **`social_finder.py`**: Automatic social profile discovery
5. **`data_merger.py`**: Intelligent data merging and deduplication
6. **`extractor.py`**: Data normalization and preparation for LLM

## Performance Considerations

### Speed vs. Completeness

- **Standard scraping**: ~2-5 seconds per site
- **With JS rendering**: ~10-15 seconds per site
- **With OCR**: +5-10 seconds per page (only when needed)

### When Each Method Triggers

| Condition | Action |
|-----------|--------|
| Text < 300 chars | Trigger JS rendering |
| Text < 200 chars (after JS) | Trigger OCR |
| No social links provided | Auto-discover profiles |
| Always | Merge and deduplicate all sources |

### Resource Usage

- **Playwright**: Launches headless Chromium (~100MB RAM)
- **OCR**: Processes up to 5 images per page (memory only, no disk)
- **Caching**: No caching between runs (fresh data each time)

## Error Handling

### Graceful Degradation

The system follows a graceful degradation pattern:

1. Try standard HTML scraping
2. If insufficient → try JS rendering
3. If still insufficient → try OCR
4. If all fail → use social media data only
5. If no data at all → mark fields as "not_available"

### No Hallucination Policy

When data is truly insufficient, the LLM will return:

```json
{
    "brand_name": "not_available",
    "overview": "not_available",
    "reason": "Insufficient extractable text from website"
}
```

This prevents hallucinated brand information.

## Troubleshooting

### OCR Not Working

**Error**: `"OCR not available"`

**Solution**:
```bash
# Install Tesseract OCR
# Windows: https://github.com/UB-Mannheim/tesseract/wiki
# Mac: brew install tesseract
# Linux: apt-get install tesseract-ocr

# Verify installation
tesseract --version

# Install Python packages
pip install pytesseract Pillow
```

### Playwright Issues

**Error**: `"Failed to initialize playwright"`

**Solution**:
```bash
# Install Playwright browsers
python -m playwright install chromium

# Or install all browsers
python -m playwright install
```

### Social Discovery Not Finding Profiles

**Reason**: Some platforms block bots or require authentication

**Solution**: Provide social links manually when possible:

```python
result = await agent.execute({
    "website": "https://example.com",
    "socials": {
        "instagram": "https://instagram.com/example",
        "linkedin": "https://linkedin.com/company/example"
    }
}, context={})
```

## Best Practices

1. **Always provide company name** when available for better social discovery
2. **Enable all features by default** for maximum data extraction
3. **Use async methods** for better performance with multiple concurrent scrapes
4. **Monitor extraction metadata** to understand data quality
5. **Test with difficult sites** to validate robustness

## Migration from Old Scraper

The enhanced scraper is **backward compatible**. Existing code will work without changes, but to leverage new features:

**Before:**
```python
scraper = WebsiteScraper(timeout=30, use_playwright=False)
data = scraper.scrape_website(url)
```

**After (recommended):**
```python
scraper = WebsiteScraper(
    timeout=30,
    use_playwright=True,
    auto_js_fallback=True,
    use_ocr=True
)
data = await scraper.scrape_website_async(url)
```

## Future Enhancements

Planned features:
- [ ] Video transcript extraction (YouTube, Vimeo)
- [ ] PDF document parsing
- [ ] Parallel page scraping
- [ ] Smart retry with exponential backoff
- [ ] Content caching layer
- [ ] Support for authenticated social scraping via official APIs

## Support

For issues or questions:
1. Check logs for detailed error messages
2. Run test script with `--url` to isolate problems
3. Review extraction metadata for insights
4. Refer to module docstrings for API details
