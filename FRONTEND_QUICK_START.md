# Frontend Quick Start Guide

## 🎉 Three New Features Now Available!

The following backend agents are now fully integrated into the frontend UI:

---

## 1. 📈 Strategy Planner

**Location**: Sidebar → "Strategy Planner" or Dashboard → "Strategy Planner" card

**What it does**:
- Generates platform-specific content strategies
- Provides posting schedules, best times, and best days
- Recommends optimal hashtag counts and mixes
- Suggests content formats and engagement tactics
- Shows best practices for each platform

**How to use**:
1. Navigate to `/strategy`
2. Select your brand
3. Choose target platforms (Instagram, Facebook, LinkedIn, etc.)
4. Click "Generate Strategy"
5. View comprehensive platform recommendations

**Example output**:
- **Instagram**: Post 5-7x/week at 11am, 2pm, 8pm | Use 20-30 hashtags | Focus on Reels & Carousels
- **LinkedIn**: Post 3-5x/week on Tue-Thu mornings | Use 3-5 hashtags | Professional articles & insights

---

## 2. 🖼️ Graphics Generator

**Location**: Sidebar → "Graphics Generator" or Dashboard → "Graphics Generator" card

**What it does**:
- Creates platform-specific graphic design specifications
- Provides exact dimensions for each platform
- Generates color schemes using brand colors
- Suggests typography (fonts, sizes, hierarchy)
- Produces AI image generation prompts
- Recommends Canva templates

**How to use**:
1. Navigate to `/graphics`
2. Select your brand
3. Choose target platform
4. Enter post caption and theme
5. (Optional) Add design requirements
6. Click "Generate Graphic Spec"
7. Copy AI prompt for MidJourney/DALL-E or download JSON

**Example output**:
- **Dimensions**: 1080x1080px (Instagram Square)
- **Colors**: Primary #2C3E50, Accent #3498DB
- **Headline**: "Breakthrough Results" - Helvetica Bold 48pt
- **AI Prompt**: "Professional medical graphic with modern blue color scheme..."

---

## 3. 📤 Content Poster & Validator

**Location**: Sidebar → "Content Poster" or Dashboard → "Content Poster" card

**What it does**:
- Validates content across multiple platforms simultaneously
- Checks character limits, media requirements, formatting
- Provides platform-specific warnings and suggestions
- Posts content to multiple platforms with one click
- Shows detailed validation results per platform

**How to use**:
1. Navigate to `/poster`
2. Enter your caption
3. Select media type (Image/Video/Carousel)
4. (Optional) Add media URL
5. Choose target platforms
6. Click "Validate" to check compliance
7. Review errors, warnings, and suggestions
8. Click "Post Now" to publish (with confirmation)

**Example output**:
- **Instagram**: ✅ Valid | Caption: 2,180 chars (within 2,200 limit)
- **Twitter**: ❌ Invalid | Caption too long (350 > 280 chars) | Suggestion: Shorten or thread
- **LinkedIn**: ⚠️ Warning | Caption ok but could add more hashtags for reach

---

## Navigation Map

### Sidebar Menu (All Pages):
```
📊 Dashboard
✏️ Generate Content
📅 Content Calendar
📈 Strategy Planner      ← NEW
🖼️ Graphics Generator    ← NEW
📤 Content Poster        ← NEW
📊 Analytics
💼 Brands
🔗 Social Accounts
```

### Dashboard Quick Actions:
```
┌─────────────────┬─────────────────┬─────────────────┐
│ Generate        │ Strategy        │ Graphics        │
│ Content         │ Planner ⭐      │ Generator ⭐    │
├─────────────────┼─────────────────┼─────────────────┤
│ Content         │ View            │ View            │
│ Poster ⭐       │ Calendar        │ Analytics       │
└─────────────────┴─────────────────┴─────────────────┘
```

---

## Complete Workflow Example

Here's how to use all features together for a campaign:

### Step 1: Set Up Brand
- Go to **Brands** page
- Add your brand profile (or use auto-scraper)

### Step 2: Plan Strategy
- Go to **Strategy Planner**
- Select brand and platforms
- Generate platform-specific strategies
- Note best posting times and hashtag recommendations

### Step 3: Create Graphics
- Go to **Graphics Generator**
- Enter your campaign theme
- Generate platform-specific design specs
- Copy AI prompt for image generation

### Step 4: Generate Content
- Go to **Generate Content**
- Select brand and platform
- Enter topic based on strategy
- Generate multiple caption variations

### Step 5: Validate & Post
- Go to **Content Poster**
- Paste generated caption
- Add media URL
- Select platforms
- Validate content
- Fix any errors shown
- Post to all platforms

### Step 6: Schedule (optional)
- Go to **Content Calendar**
- Schedule posts for optimal times from Strategy recommendations

### Step 7: Monitor
- Go to **Analytics**
- Track performance across platforms

---

## Running the Application

### Start Backend:
```bash
cd agent
uvicorn app.main:app --reload
```
Backend runs at: `http://localhost:8000`

### Start Frontend:
```bash
cd frontend
npm run dev
```
Frontend runs at: `http://localhost:5173`

### Access Application:
1. Open browser: `http://localhost:5173`
2. Login with your credentials
3. Navigate to any new feature from sidebar or dashboard

---

## Key Features

### Strategy Planner:
✅ Multi-platform selection
✅ Platform-specific recommendations
✅ Posting schedules with best times
✅ Hashtag strategies
✅ Content format suggestions
✅ Engagement tactics

### Graphics Generator:
✅ Platform-correct dimensions
✅ Brand color integration
✅ Typography specifications
✅ AI image generation prompts
✅ Canva template suggestions
✅ Download specifications

### Content Poster:
✅ Multi-platform validation
✅ Character limit checking
✅ Error/warning/suggestion system
✅ Platform-specific requirements
✅ One-click posting
✅ Confirmation dialogs

---

## Tips for Best Results

### Strategy Planner:
- Select multiple platforms to compare recommendations
- Note the "best times" for scheduling posts
- Use recommended hashtag counts for each platform
- Follow content format suggestions for better engagement

### Graphics Generator:
- Provide detailed theme descriptions
- Mention specific design requirements upfront
- Use generated AI prompts with MidJourney, DALL-E, or Stable Diffusion
- Download JSON spec for sharing with designers

### Content Poster:
- Always validate before posting
- Pay attention to warnings (yellow) - they won't block posting but impact performance
- Fix all errors (red) before posting
- Review suggestions for optimization ideas

---

## Troubleshooting

### "No brands available"
→ Go to Brands page and add a brand first

### API errors
→ Ensure backend is running on port 8000
→ Check `.env` file has correct LLM API keys

### Validation fails
→ Check caption length
→ Ensure media URL is accessible
→ Review platform-specific requirements

### Empty results
→ Ensure brand profile has sufficient data
→ Check backend logs for LLM errors
→ Verify API keys are valid

---

## What's Different from Backend-Only?

### Before (Backend Only):
- ❌ Required manual API calls with curl/Postman
- ❌ JSON-only responses (hard to read)
- ❌ No visual feedback
- ❌ Technical knowledge required

### Now (Full Stack):
- ✅ Beautiful, intuitive UI
- ✅ Visual display of results
- ✅ Color-coded validation feedback
- ✅ One-click actions
- ✅ No technical knowledge needed
- ✅ Integrated with existing workflow

---

## Support

For issues:
1. Check browser console for errors
2. Check backend terminal for API errors
3. Verify all dependencies installed:
   ```bash
   cd frontend && npm install
   cd ../agent && pip install -r requirements.txt
   ```

---

**Enjoy your new features! 🎉**

All three backend agents are now accessible through the beautiful, user-friendly interface.
