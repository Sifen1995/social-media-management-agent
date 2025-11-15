# Auto Brand Profile Scraper - Feature Guide

## Overview

The Auto Brand Profile Scraper is an intelligent feature that automatically researches brands by scraping their website and social media profiles, then uses AI to generate a comprehensive brand profile. This eliminates the need for manual data entry during brand onboarding.

## How It Works

### Architecture Flow

```
User Request (website + social URLs)
        ↓
  API Endpoint (/api/v1/brand/auto_profile)
        ↓
  Brand Profile Agent
        ↓
  ┌─────────────────┬─────────────────┐
  ↓                 ↓                 ↓
Website          Social Media      Data
Scraper          Scraper           Extractor
  ↓                 ↓                 ↓
  └─────────────────┴─────────────────┘
        ↓
  LLM Analysis (Gemini/Claude/OpenAI)
        ↓
  Structured Brand Profile JSON
        ↓
  Response to User
```

### Components

1. **Website Scraper** (`app/scraper/website_scraper.py`)
   - Scrapes company websites (homepage, /about, /services, /contact)
   - Uses `requests` for basic HTML scraping
   - Falls back to `playwright` for JavaScript-heavy sites
   - Extracts meta tags, JSON-LD structured data, and text content

2. **Social Media Scraper** (`app/scraper/social_scraper.py`)
   - Supports: Instagram, LinkedIn, Twitter/X, TikTok, Facebook
   - Lightweight HTML scraping (no API keys required)
   - Extracts bios, captions, hashtags, and tone indicators

3. **Data Extractor** (`app/scraper/extractor.py`)
   - Normalizes scraped data from all sources
   - Extracts key insights (hashtags, themes, tone patterns)
   - Prepares formatted text for LLM analysis

4. **Brand Profile Agent** (`app/agents/brand_profile/agent.py`)
   - Orchestrates the entire workflow
   - Calls LLM to analyze scraped data
   - Returns structured JSON brand profile

## API Endpoint

### POST /api/v1/brand/auto_profile

Automatically generates a brand profile by scraping and analyzing web data.

#### Request Body

```json
{
  "website": "https://example.com",
  "socials": {
    "instagram": "https://instagram.com/example",
    "linkedin": "https://linkedin.com/company/example",
    "twitter": "https://twitter.com/example",
    "tiktok": "https://tiktok.com/@example",
    "facebook": "https://facebook.com/example"
  },
  "use_playwright": false
}
```

**Parameters:**
- `website` (required): Company website URL
- `socials` (optional): Social media profile URLs
  - `instagram`: Instagram profile URL
  - `linkedin`: LinkedIn company page URL
  - `twitter`: Twitter/X profile URL
  - `tiktok`: TikTok profile URL
  - `facebook`: Facebook page URL
- `use_playwright` (optional, default: false): Use Playwright for JS-heavy sites

#### Response

```json
{
  "success": true,
  "message": "Brand profile generated successfully",
  "data": {
    "brand_name": "Example Inc",
    "overview": "Example Inc is a leading provider of innovative solutions...",
    "products_services": [
      "Cloud Software",
      "AI Solutions",
      "Consulting Services"
    ],
    "mission": "To empower businesses through technology innovation",
    "tone_voice": "Professional yet approachable, focusing on innovation and customer success",
    "target_audience": "Tech-savvy business leaders and decision-makers in mid-to-large enterprises",
    "brand_values": [
      "Innovation",
      "Customer Success",
      "Integrity",
      "Excellence"
    ],
    "frequently_used_hashtags": [
      "innovation",
      "technology",
      "business",
      "ai",
      "cloudsolutions"
    ],
    "content_style_summary": "moderate length, uses hashtags, includes CTAs, professional tone",
    "posting_frequency": "3-4 times per week based on observed patterns",
    "recommended_content_strategy": "Focus on thought leadership content, customer success stories, and product innovations. Mix educational content with promotional posts. Maintain consistent posting schedule during business hours.",
    "source_urls": {
      "website": "https://example.com",
      "social_platforms": {
        "instagram": "example",
        "linkedin": "example"
      }
    },
    "_metadata": {
      "data_quality": "excellent",
      "sources_used": {
        "website": true,
        "social_media": true
      }
    }
  },
  "metadata": {
    "website_scraped": true,
    "social_platforms": ["instagram", "linkedin"],
    "data_quality": "excellent"
  }
}
```

## Installation & Setup

### 1. Install Dependencies

```bash
cd agent
pip install -r requirements.txt
```

**New dependencies added:**
- `requests==2.31.0` - HTTP client for web scraping
- `beautifulsoup4==4.12.3` - HTML parsing
- `lxml==5.1.0` - XML/HTML parser (BeautifulSoup backend)
- `playwright==1.41.0` - Browser automation for JS-heavy sites

### 2. Install Playwright Browsers (Optional)

If you plan to use `use_playwright: true` for JavaScript-heavy sites:

```bash
playwright install chromium
```

### 3. Test the Installation

```bash
# Run tests
pytest tests/test_scraper.py -v

# Run specific test
pytest tests/test_scraper.py::TestScraperBase::test_is_valid_url -v
```

## Usage Examples

### Example 1: Basic Usage with Website Only

```python
import requests

url = "http://localhost:8000/api/v1/brand/auto_profile"
headers = {"Authorization": "Bearer YOUR_JWT_TOKEN"}

data = {
    "website": "https://anthropic.com"
}

response = requests.post(url, json=data, headers=headers)
profile = response.json()

print(f"Brand: {profile['data']['brand_name']}")
print(f"Overview: {profile['data']['overview']}")
```

### Example 2: Full Research with Social Media

```python
data = {
    "website": "https://anthropic.com",
    "socials": {
        "twitter": "https://twitter.com/AnthropicAI",
        "linkedin": "https://linkedin.com/company/anthropic"
    }
}

response = requests.post(url, json=data, headers=headers)
profile = response.json()

# Auto-fill brand creation form
brand_data = {
    "name": profile['data']['brand_name'],
    "brand_voice": profile['data']['tone_voice'],
    "target_audience": profile['data']['target_audience'],
    "niche": profile['data']['products_services'][0] if profile['data']['products_services'] else ""
}
```

### Example 3: Using Playwright for JS-Heavy Sites

```python
data = {
    "website": "https://example-spa.com",
    "use_playwright": true  # Enable browser automation
}

response = requests.post(url, json=data, headers=headers)
```

### Example 4: CURL Command

```bash
curl -X POST "http://localhost:8000/api/v1/brand/auto_profile" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "website": "https://example.com",
    "socials": {
      "instagram": "https://instagram.com/example",
      "linkedin": "https://linkedin.com/company/example"
    }
  }'
```

## Testing

### Run All Tests

```bash
cd agent
pytest tests/test_scraper.py -v
```

### Run Specific Test Categories

```bash
# Test website scraper
pytest tests/test_scraper.py::TestWebsiteScraper -v

# Test social scraper
pytest tests/test_scraper.py::TestSocialScraper -v

# Test data extractor
pytest tests/test_scraper.py::TestBrandDataExtractor -v
```

### Integration Tests (Require Network)

Integration tests are skipped by default. To run them:

```bash
pytest tests/test_scraper.py -v --runintegration
```

## Error Handling

### Common Errors

1. **Insufficient Data**
   ```json
   {
     "success": false,
     "message": "Insufficient data scraped. Unable to generate brand profile.",
     "data": {
       "error": "Scraping failed or insufficient data"
     }
   }
   ```
   **Solution**: Ensure website is accessible and has content. Try adding social media links.

2. **Invalid URL**
   ```json
   {
     "success": false,
     "message": "Website URL is required"
   }
   ```
   **Solution**: Provide a valid website URL in the request.

3. **LLM Analysis Failed**
   ```json
   {
     "success": false,
     "message": "LLM analysis failed"
   }
   ```
   **Solution**: Check LLM service configuration and API keys.

4. **Timeout**
   - Default timeout: 30 seconds per page
   - If scraping times out, the endpoint will continue with available data

## Limitations & Considerations

### Website Scraping Limitations

1. **JavaScript-Heavy Sites**: Some modern SPAs may require `use_playwright: true`
2. **Rate Limiting**: Be mindful of making too many requests to the same domain
3. **Robots.txt**: Respects website scraping policies
4. **Dynamic Content**: Content loaded via AJAX may not be captured without Playwright

### Social Media Limitations

1. **No API Keys Required**: Uses public HTML scraping (limited data)
2. **Platform Restrictions**: Instagram, LinkedIn, etc. heavily use JavaScript
3. **Authentication Walls**: Can only access public profile information
4. **Rate Limits**: Excessive scraping may result in temporary blocks

### Best Practices

1. **Use Playwright Sparingly**: Only enable for sites that truly need it (slower)
2. **Provide Multiple Sources**: More data sources = better quality profile
3. **Cache Results**: Store generated profiles to avoid re-scraping
4. **Handle Errors Gracefully**: Not all scraping attempts will succeed
5. **Respect Rate Limits**: Don't make rapid consecutive requests

## Data Quality Indicators

The response includes a `data_quality` field:

- **excellent**: Both website and social media data successfully scraped
- **good**: Either website OR social media data scraped
- **insufficient**: Unable to scrape enough data for analysis

## Integration with Frontend

### Auto-Fill Brand Onboarding Form

```javascript
// Example React/JavaScript integration

const handleAutoProfile = async (websiteUrl, socialLinks) => {
  const response = await fetch('/api/v1/brand/auto_profile', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${authToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      website: websiteUrl,
      socials: socialLinks
    })
  });

  const result = await response.json();

  if (result.success) {
    // Auto-fill form fields
    setBrandName(result.data.brand_name);
    setBrandVoice(result.data.tone_voice);
    setTargetAudience(result.data.target_audience);
    setMission(result.data.mission);
    setProducts(result.data.products_services);
    setHashtags(result.data.frequently_used_hashtags);
  }
};
```

## Performance

- **Average Scraping Time**: 10-30 seconds (without Playwright)
- **With Playwright**: 30-60 seconds (includes browser startup)
- **LLM Analysis Time**: 5-15 seconds
- **Total Time**: ~20-60 seconds depending on configuration

## Future Enhancements

Planned improvements:

1. **Background Processing**: Move scraping to async background jobs
2. **Caching Layer**: Cache scraped data to avoid duplicate requests
3. **Social Media APIs**: Integrate official APIs for richer data
4. **Image Analysis**: Extract brand colors and visual style from images
5. **Competitor Analysis**: Compare against competitor brands
6. **Scheduled Updates**: Periodically update brand profiles
7. **Webhook Integration**: Notify when profile generation is complete

## Troubleshooting

### Playwright Installation Issues

If `playwright install` fails:

```bash
# Install specific browser
playwright install chromium

# Or skip playwright and use requests-only mode
# (don't set use_playwright: true)
```

### Import Errors

If you get import errors:

```bash
# Ensure all dependencies are installed
pip install -r requirements.txt

# Check Python path
export PYTHONPATH="${PYTHONPATH}:/path/to/agent"
```

### Permission Errors

Some websites may block scraping:

```
HTTP 403 Forbidden
```

**Solution**: This is expected for sites that block scrapers. Try providing social media links instead.

## Support

For issues or questions:

1. Check logs: `tail -f logs/app.log`
2. Run tests: `pytest tests/test_scraper.py -v`
3. Open GitHub issue with error details
4. Include sample URLs (if public) for debugging

---

**Note**: This feature uses web scraping which should be used responsibly and in compliance with website terms of service and applicable laws.
