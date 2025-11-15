# Local Testing Guide - Auto Brand Profile Feature

## Current Status

✅ **Backend API**: Running on http://localhost:8000
✅ **Frontend**: Running on http://localhost:3000
✅ **Auto Profile Endpoint**: `/api/v1/brands/auto_profile` - ACTIVE

---

## How to Access the Feature

### Option 1: Through the Web UI (Recommended)

1. **Open your browser** and go to: http://localhost:3000

2. **Login** with any credentials (demo mode accepts anything):
   - Email: `demo@example.com`
   - Password: `password`

3. **Navigate to Brand Management**:
   - Click on "Brand Management" in the navigation menu
   - OR go directly to: http://localhost:3000/brands

4. **Click "Auto-Generate Brand" button**:
   - You'll see a purple button labeled "Auto-Generate Brand"
   - This opens the Auto Brand Profile modal

5. **Fill in the form**:
   - **Website URL** (required): `https://anthropic.com`
   - **Social Media URLs** (optional):
     - Instagram: Leave blank or add if you want
     - LinkedIn: `https://linkedin.com/company/anthropic`
     - Twitter: `https://twitter.com/AnthropicAI`
     - TikTok: Leave blank
     - Facebook: Leave blank

6. **Click "Generate Brand Profile"**:
   - Wait 20-60 seconds for the AI to research and analyze
   - You'll see a loading indicator

7. **Review the Generated Profile**:
   - Brand name
   - Overview
   - Products & Services
   - Mission
   - Tone of Voice
   - Target Audience
   - Brand Values
   - Frequently Used Hashtags
   - Content Style Summary
   - Recommended Content Strategy

8. **Click "Use This Profile"**:
   - The data will auto-fill the brand creation form
   - Review and save!

---

## Option 2: Test via API (cURL)

```bash
# Test the endpoint directly
curl -X POST "http://localhost:8000/api/v1/brands/auto_profile" \
  -H "Content-Type: application/json" \
  -d '{
    "website": "https://anthropic.com",
    "socials": {
      "twitter": "https://twitter.com/AnthropicAI",
      "linkedin": "https://linkedin.com/company/anthropic"
    },
    "use_playwright": false
  }'
```

---

## What You'll See in the UI

### 1. Brand Management Page
- **Header**: "Brand Management" with description
- **Two buttons**:
  - 🌐 **Auto-Generate Brand** (purple) - NEW FEATURE
  - ➕ **Add Manually** (blue) - Original button

### 2. Auto-Generate Modal
When you click "Auto-Generate Brand":

**Form Fields:**
- 🌐 Website URL* (required)
- 📸 Instagram (optional)
- 💼 LinkedIn (optional)
- 🐦 Twitter/X (optional)
- 🎵 TikTok (optional)
- 👍 Facebook (optional)
- ☑️ Use advanced scraping checkbox

**Buttons:**
- "Generate Brand Profile" (primary button)
- "Cancel" (gray button)

### 3. Loading State
- Loading spinner animation
- Message: "Researching your brand..."
- Info: "This may take 20-60 seconds..."

### 4. Success State
- ✅ Green success banner
- Complete brand profile displayed with:
  - Brand name
  - Overview paragraph
  - Products/Services tags (blue pills)
  - Mission statement
  - Tone of Voice
  - Target Audience
  - Brand Values tags (purple pills)
  - Hashtags (gray pills)
  - Content strategy recommendations
  - Data quality indicator

**Action Buttons:**
- "Use This Profile" (primary) - Auto-fills form
- "Generate New Profile" (secondary) - Start over

---

## Visual Guide

```
┌─────────────────────────────────────────────────────────┐
│                    Brand Management                      │
│   Manage your brand profiles and settings              │
│                                                          │
│   [🌐 Auto-Generate Brand]  [➕ Add Manually]          │
└─────────────────────────────────────────────────────────┘

When you click "Auto-Generate Brand":

┌─────────────────────────────────────────────────────────┐
│  Auto-Generate Brand Profile                            │
│  Enter your website and social media URLs...            │
│                                                          │
│  Website URL *                                          │
│  🌐 [https://anthropic.com________________]            │
│                                                          │
│  Social Media Profiles (Optional)                       │
│  📸 [Instagram URL___________________________]          │
│  💼 [LinkedIn URL____________________________]          │
│  🐦 [Twitter/X URL___________________________]          │
│  🎵 [TikTok URL______________________________]          │
│  👍 [Facebook URL____________________________]          │
│                                                          │
│  ☐ Use advanced scraping (slower)                       │
│                                                          │
│  [🌐 Generate Brand Profile]  [Cancel]                 │
└─────────────────────────────────────────────────────────┘

After clicking Generate (20-60 seconds later):

┌─────────────────────────────────────────────────────────┐
│  ✅ Brand profile generated successfully!               │
│  Review the information below and click "Use This...   │
│                                                          │
│  Generated Brand Profile                                │
│  ┌───────────────────────────────────────────────────┐ │
│  │ Brand Name: Anthropic                             │ │
│  │                                                    │ │
│  │ Overview: Anthropic is an AI safety company...   │ │
│  │                                                    │ │
│  │ Products & Services:                              │ │
│  │ [Claude] [AI Research] [AI Safety]               │ │
│  │                                                    │ │
│  │ Tone of Voice: Professional, research-focused... │ │
│  │                                                    │ │
│  │ Target Audience: Developers, researchers...      │ │
│  │                                                    │ │
│  │ Frequently Used Hashtags:                         │ │
│  │ #AI #Claude #AIsafety #research...               │ │
│  └───────────────────────────────────────────────────┘ │
│                                                          │
│  [Use This Profile]  [Generate New Profile]            │
└─────────────────────────────────────────────────────────┘
```

---

## Troubleshooting

### Issue: "Auto-Generate Brand" button not visible
**Solution**:
- Make sure you're on http://localhost:3000/brands
- Hard refresh the page (Ctrl+F5 or Cmd+Shift+R)
- Check browser console for errors

### Issue: API endpoint returns 404
**Solution**:
- Verify backend is running: `curl http://localhost:8000`
- Check if endpoint exists: `curl http://localhost:8000/docs`
- Restart backend server

### Issue: Frontend shows old version
**Solution**:
- Hard refresh: Ctrl+F5 (Windows) or Cmd+Shift+R (Mac)
- Clear browser cache
- Check if frontend dev server is running on port 3000

### Issue: "Failed to generate brand profile"
**Possible causes**:
- Invalid website URL
- Website blocks scraping
- No internet connection
- LLM API key not configured

**Solutions**:
- Try a well-known website (anthropic.com, example.com)
- Check GEMINI_API_KEY in agent/.env
- Check internet connection

---

## API Documentation

Once running, view complete API docs at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Look for: `POST /api/v1/brands/auto_profile`

---

## Test Examples

### Example 1: Anthropic (AI Company)
```json
{
  "website": "https://anthropic.com",
  "socials": {
    "twitter": "https://twitter.com/AnthropicAI"
  }
}
```

### Example 2: General Website
```json
{
  "website": "https://example.com"
}
```

### Example 3: With Multiple Social Platforms
```json
{
  "website": "https://yourcompany.com",
  "socials": {
    "instagram": "https://instagram.com/yourcompany",
    "linkedin": "https://linkedin.com/company/yourcompany",
    "twitter": "https://twitter.com/yourcompany"
  }
}
```

---

## Next Steps

1. **Test the Feature**: Follow "Option 1" above
2. **Try Different Websites**: Test with various company websites
3. **Check the Results**: See how AI analyzes different brands
4. **Use the Profiles**: Click "Use This Profile" to auto-fill forms

---

## Deployment Note

**Why you don't see it on Render:**

The deployed version on Render needs to be updated with the new code. To deploy:

1. The code is already pushed to GitHub (commit 90485aa)
2. Render should automatically redeploy
3. If not, manually trigger a deploy in Render dashboard
4. Wait 5-10 minutes for deployment

**Check deployment status**:
- Go to: https://dashboard.render.com
- Check if build is in progress
- View build logs for any errors

---

## Summary

✅ **Backend**: Running on port 8000 with auto_profile endpoint
✅ **Frontend**: Running on port 3000 with Auto-Generate button
✅ **Feature**: Fully functional and ready to use
🎯 **Access**: http://localhost:3000/brands → "Auto-Generate Brand"

**The feature is working locally!** 🎉
