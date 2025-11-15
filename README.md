# Social Media Management Agent

An AI-powered social media management platform that leverages intelligent agents to automate and optimize social media content creation, scheduling, analytics, and engagement across multiple platforms.

## Overview

The Social Media Management Agent is a comprehensive platform that combines the power of AI with social media management, enabling brands to create engaging content, schedule posts, analyze performance, and manage engagement across Instagram, Facebook, Twitter/X, LinkedIn, TikTok, and YouTube.


## Key Features

### Auto Brand Profile Scraper (NEW!)
- **Automated Brand Research**: Automatically scrape and analyze websites and social media profiles
- **AI-Powered Extraction**: Use LLM to extract brand name, mission, tone of voice, target audience, and values
- **Multi-Source Analysis**: Combine data from company websites and 5+ social platforms (Instagram, LinkedIn, Twitter, TikTok, Facebook)
- **One-Click Onboarding**: Auto-fill brand creation forms with comprehensive, AI-generated brand profiles
- **Smart Data Quality Assessment**: Get quality indicators (excellent/good/insufficient) for each research session

### AI-Powered Content Generation
- **Multi-Platform Support**: Generate platform-specific content optimized for Instagram, Facebook, Twitter/X, LinkedIn, TikTok, and YouTube
- **Content Variations**: Create multiple variations of posts to A/B test what resonates with your audience
- **Smart Hashtag Generation**: AI-generated hashtag strategies with niche, category, and trending tags
- **Hook & CTA Creation**: Generate attention-grabbing hooks and compelling calls-to-action
- **Caption Optimization**: Improve existing captions to increase engagement

### Intelligent Agent System
- **Brand Profile Agent**: Automatically researches brands through web scraping and LLM analysis (NEW!)
- **Content Agent**: Specialized in creating engaging, platform-specific social media content
- **Planner Agent**: Decomposes complex social media strategies into actionable tasks
- **Scheduler Agent**: Optimizes posting times based on audience activity and engagement patterns
- **Analytics Agent**: Provides insights and recommendations based on performance data
- **Engagement Agent**: Manages interactions, comments, and community engagement
- **Social Listening Agent**: Monitors trends, mentions, and competitor activities
- **Optimizer Agent**: Continuously improves content strategy based on performance

### Content Management
- **Content Calendar**: Visual calendar for planning and scheduling posts across all platforms
- **Brand Management**: Manage multiple brands with unique voice, tone, and target audiences
- **Social Account Integration**: Connect and manage multiple social media accounts
- **Draft Management**: Save, edit, and refine content before publishing

### Analytics & Insights
- **Performance Metrics**: Track engagement, reach, impressions, and follower growth
- **AI-Powered Insights**: Get actionable recommendations to improve performance
- **Competitor Analysis**: Monitor and analyze competitor strategies
- **Trend Detection**: Stay ahead with real-time trend identification

### Automation & Scheduling
- **Smart Scheduling**: AI determines optimal posting times for maximum engagement
- **Bulk Upload**: Schedule multiple posts at once
- **Auto-Publishing**: Set it and forget it with automatic post publishing
- **Queue Management**: Build and manage a content queue

## Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **AI/LLM**: Google Gemini (configurable for other providers)
- **Web Scraping**: BeautifulSoup4, Playwright (for JS-heavy sites)
- **Database**: SQLAlchemy with PostgreSQL support
- **Task Queue**: Celery for background jobs
- **Authentication**: JWT-based authentication

### Frontend
- **Framework**: React 18 with Vite
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **Routing**: React Router
- **Icons**: React Icons
- **Notifications**: React Hot Toast

## Project Structure

```
social-media-management-agent/
├── agent/                          # Backend application
│   ├── app/
│   │   ├── agents/                # AI agents
│   │   │   ├── base/             # Base agent classes
│   │   │   ├── brand_profile/    # Brand research agent (NEW!)
│   │   │   ├── content/          # Content generation agent
│   │   │   ├── planner/          # Planning agent
│   │   │   ├── scheduler/        # Scheduling agent
│   │   │   ├── analytics/        # Analytics agent
│   │   │   ├── engagement/       # Engagement agent
│   │   │   ├── social_listening/ # Social listening agent
│   │   │   └── optimizer/        # Optimization agent
│   │   ├── scraper/              # Web scraping module (NEW!)
│   │   │   ├── website_scraper.py   # Website scraper
│   │   │   ├── social_scraper.py    # Social media scraper
│   │   │   ├── extractor.py         # Data extraction
│   │   │   └── base.py              # Scraper utilities
│   │   ├── api/                  # API endpoints
│   │   │   └── v1/
│   │   │       └── endpoints/
│   │   ├── core/                 # Core configuration
│   │   ├── db/                   # Database models
│   │   │   └── models/
│   │   ├── integrations/         # Social platform integrations
│   │   │   ├── instagram/
│   │   │   ├── facebook/
│   │   │   ├── twitter/
│   │   │   ├── linkedin/
│   │   │   ├── tiktok/
│   │   │   └── youtube/
│   │   ├── schemas/              # Pydantic schemas
│   │   ├── services/             # Business logic
│   │   └── utils/                # Utilities
│   └── celery_app/               # Celery configuration
├── frontend/                      # React frontend
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── ContentGenerator.jsx
│   │   │   ├── BrandManagement.jsx
│   │   │   ├── ContentCalendar.jsx
│   │   │   ├── Analytics.jsx
│   │   │   └── SocialAccounts.jsx
│   │   ├── services/             # API services
│   │   └── stores/               # State management
│   └── public/
└── DEPLOYMENT.md                  # Deployment guide
```

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- Google Gemini API Key (get it from [Google AI Studio](https://makersuite.google.com/app/apikey))
- Git

### Local Development Setup

#### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/social-media-management-agent.git
cd social-media-management-agent
```

#### 2. Backend Setup

```bash
# Navigate to agent directory
cd agent

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

**Environment Variables (.env)**:
```env
GEMINI_API_KEY=your_gemini_api_key_here
LLM_PROVIDER=gemini
DEFAULT_MODEL=gemini-flash-latest
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=8192
SECRET_KEY=your_secret_key_here
```

#### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env
```

**Environment Variables (.env.local)**:
```env
VITE_API_URL=http://localhost:8000/api/v1
```

#### 4. Run the Application

**Terminal 1 - Backend**:
```bash
cd agent
python simple_api.py
# Backend runs on http://localhost:8000
```

**Terminal 2 - Frontend**:
```bash
cd frontend
npm run dev
# Frontend runs on http://localhost:5173
```

Visit `http://localhost:5173` to access the application.

## Deployment

The application is configured for easy deployment on [Render](https://render.com). See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

### Quick Deploy to Render

1. Push your code to GitHub
2. Sign in to Render with GitHub
3. Create a new Blueprint and select your repository
4. Add your `GEMINI_API_KEY` environment variable
5. Deploy!

The application will be available at:
- Frontend: `https://social-media-agent-frontend.onrender.com`
- Backend API: `https://social-media-agent-api.onrender.com`

## Usage

### Auto-Generate Brand Profile (NEW!)

1. Sign up/Login to the application
2. Navigate to **Brand Management**
3. Click **Auto-Generate Brand** (purple button)
4. Enter your website URL and social media profiles:
   - Website URL (required)
   - Instagram, LinkedIn, Twitter, TikTok, Facebook (optional)
5. Click **Generate Brand Profile**
6. Wait 20-60 seconds for AI to research and analyze
7. Review the generated profile with:
   - Brand name, overview, mission
   - Tone of voice and target audience
   - Products/services and brand values
   - Frequently used hashtags
   - Content strategy recommendations
8. Click **Use This Profile** to auto-fill the brand form
9. Review and save!

**See [AUTO_BRAND_PROFILE_GUIDE.md](AUTO_BRAND_PROFILE_GUIDE.md) for detailed usage guide.**

### Creating Your First Brand (Manual)

1. Sign up/Login to the application
2. Navigate to **Brand Management**
3. Click **Add Manually**
4. Fill in brand details:
   - Brand name
   - Description
   - Brand voice (e.g., "professional and friendly")
   - Target audience (e.g., "tech-savvy millennials")
   - Niche/industry

### Generating Content

1. Go to **Content Generator**
2. Select your brand
3. Choose platform (Instagram, Facebook, etc.)
4. Select content type (Post, Story, Reel, etc.)
5. Enter topic/theme
6. Add any specific instructions (optional)
7. Click **Generate Content**
8. Review and copy the AI-generated variations

### Scheduling Posts

1. Navigate to **Content Calendar**
2. Click on a date or time slot
3. Add your content
4. Select platform(s)
5. Choose scheduling option:
   - Post now
   - Schedule for specific time
   - Add to queue
6. Click **Schedule**

### Viewing Analytics

1. Go to **Analytics** page
2. Select date range
3. View metrics:
   - Total posts
   - Engagement rate
   - Reach and impressions
   - Follower growth
   - Top performing content
4. Get AI-powered insights and recommendations

## API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Key API Endpoints

#### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `GET /api/v1/auth/me` - Get current user

#### Content
- `POST /api/v1/content/generate` - Generate AI content
- `GET /api/v1/content/` - List all content
- `POST /api/v1/content/` - Create content
- `PUT /api/v1/content/{id}` - Update content
- `DELETE /api/v1/content/{id}` - Delete content

#### Brands
- `POST /api/v1/brands/auto_profile` - Auto-generate brand profile (NEW!)
- `GET /api/v1/brands/` - List all brands
- `POST /api/v1/brands/` - Create brand
- `GET /api/v1/brands/{id}` - Get brand details
- `PUT /api/v1/brands/{id}` - Update brand
- `DELETE /api/v1/brands/{id}` - Delete brand

#### Analytics
- `GET /api/v1/analytics/overview` - Get analytics overview
- `GET /api/v1/analytics/insights` - Get AI insights

#### Scheduler
- `POST /api/v1/scheduler/schedule` - Schedule content
- `GET /api/v1/scheduler/calendar` - Get calendar view

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Roadmap

### Phase 1 (Current)
- [x] AI content generation
- [x] Multi-platform support
- [x] Basic scheduling
- [x] Brand management
- [x] User authentication

### Phase 2 (In Progress)
- [ ] Full social platform integration (OAuth)
- [ ] Auto-publishing to platforms
- [ ] Advanced analytics with charts
- [ ] A/B testing framework
- [ ] Content performance predictions

### Phase 3 (Planned)
- [ ] Competitor analysis dashboard
- [ ] Influencer collaboration tools
- [ ] Team collaboration features
- [ ] White-label options
- [ ] Mobile app (iOS/Android)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- Documentation: [Link to docs]
- Issues: [GitHub Issues](https://github.com/yourusername/social-media-management-agent/issues)
- Email: support@yourdomain.com

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Powered by [Google Gemini](https://ai.google.dev/)
- UI components from [Tailwind CSS](https://tailwindcss.com/)
- Icons by [React Icons](https://react-icons.github.io/react-icons/)

---

Made with AI and love for social media managers everywhere.
