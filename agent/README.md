# Social Media Management Agent 🤖

A fully autonomous multi-agent AI system for managing social media operations across multiple platforms. Built with FastAPI, SQLAlchemy, and powered by LLMs (OpenAI/Anthropic).

## 🎯 Features

### Multi-Agent System
- **Planner Agent**: Master coordinator that decomposes complex tasks
- **Content Agent**: Generates platform-specific content, captions, and hashtags
- **Analytics Agent**: Analyzes performance metrics and provides insights
- **Scheduler Agent**: Creates content calendars and optimizes posting times
- **Engagement Agent**: Manages comments, DMs, and community interactions
- **Social Listening Agent**: Monitors trends and competitor activity
- **Optimizer Agent**: Provides A/B testing and optimization recommendations

### Platform Integrations
- Instagram (via Graph API)
- Facebook
- Twitter/X
- TikTok
- YouTube
- LinkedIn

### Core Capabilities
- Autonomous content generation with brand voice matching
- Performance analytics and reporting
- Automated content scheduling
- Community engagement management
- Trend detection and social listening
- Multi-platform content optimization

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         FastAPI Backend                  │
│                                          │
│  ┌────────────────────────────────┐    │
│  │   Multi-Agent Orchestrator     │    │
│  │                                 │    │
│  │  ┌──────────┐  ┌──────────┐   │    │
│  │  │ Planner  │  │ Content  │   │    │
│  │  │  Agent   │  │  Agent   │   │    │
│  │  └──────────┘  └──────────┘   │    │
│  │                                 │    │
│  │  ┌──────────┐  ┌──────────┐   │    │
│  │  │Analytics │  │Scheduler │   │    │
│  │  │  Agent   │  │  Agent   │   │    │
│  │  └──────────┘  └──────────┘   │    │
│  └────────────────────────────────┘    │
│                                          │
│  ┌────────────────────────────────┐    │
│  │   Database Layer (PostgreSQL)  │    │
│  └────────────────────────────────┘    │
│                                          │
│  ┌────────────────────────────────┐    │
│  │  Platform Integrations         │    │
│  │  (Instagram, Twitter, etc.)    │    │
│  └────────────────────────────────┘    │
└─────────────────────────────────────────┘
```

## 📦 Installation

### Prerequisites
- Python 3.10+
- PostgreSQL
- Redis
- OpenAI API Key or Anthropic API Key

### Setup Steps

1. **Clone the repository**
```bash
git clone <repository-url>
cd agent
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your actual credentials
```

5. **Initialize database**
```bash
# Create PostgreSQL database
createdb smm_agent

# Run migrations (or create tables)
python -c "from app.db.session import init_db; init_db()"
```

6. **Start Redis**
```bash
redis-server
```

7. **Run the application**
```bash
# Development mode
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

8. **Start Celery worker** (in separate terminal)
```bash
celery -A celery_app.celery worker --loglevel=info
```

9. **Start Celery beat** (for scheduled tasks, in separate terminal)
```bash
celery -A celery_app.celery beat --loglevel=info
```

## 🚀 Usage

### API Documentation
Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Example: Generate Content

```python
import requests

# Register a user
response = requests.post("http://localhost:8000/api/v1/auth/register", json={
    "email": "user@example.com",
    "password": "securepassword",
    "full_name": "John Doe"
})

# Login
response = requests.post("http://localhost:8000/api/v1/auth/login", data={
    "username": "user@example.com",
    "password": "securepassword"
})
token = response.json()["access_token"]

# Create a brand
headers = {"Authorization": f"Bearer {token}"}
brand_response = requests.post(
    "http://localhost:8000/api/v1/brands/",
    headers=headers,
    json={
        "name": "My Fashion Brand",
        "niche": "sustainable fashion",
        "brand_voice": "friendly, eco-conscious, inspiring",
        "target_audience": "millennials and gen-z interested in sustainable living"
    },
    params={"user_id": 1}
)
brand_id = brand_response.json()["id"]

# Generate content
content_response = requests.post(
    "http://localhost:8000/api/v1/content/generate",
    headers=headers,
    json={
        "brand_id": brand_id,
        "platform": "instagram",
        "topic": "eco-friendly summer fashion tips",
        "content_type": "post",
        "count": 3
    }
)

print(content_response.json())
```

### Example: Use Planner Agent for Complex Request

```python
# Natural language request - Planner Agent will decompose and execute
response = requests.post(
    "http://localhost:8000/api/v1/content/plan-and-execute",
    headers=headers,
    json={
        "brand_id": brand_id,
        "user_request": "Create a week's worth of Instagram content about sustainable fashion, schedule it, and give me analytics recommendations"
    }
)

# Planner will:
# 1. Generate content using Content Agent
# 2. Create calendar using Scheduler Agent
# 3. Provide recommendations using Analytics/Optimizer Agent

result = response.json()
print(result["data"]["plan"])  # See the execution plan
print(result["data"]["execution_results"])  # See results from each agent
```

### Example: Generate Analytics Report

```python
response = requests.post(
    "http://localhost:8000/api/v1/analytics/generate-report",
    headers=headers,
    params={
        "brand_id": brand_id,
        "time_period": "last_30_days"
    }
)

analytics = response.json()
print(analytics["data"]["insights"])
```

## 🗂️ Project Structure

```
agent/
├── app/
│   ├── agents/              # Multi-agent system
│   │   ├── base/            # Base agent classes
│   │   ├── planner/         # Planner (master) agent
│   │   ├── content/         # Content generation agent
│   │   ├── analytics/       # Analytics agent
│   │   ├── scheduler/       # Scheduling agent
│   │   ├── engagement/      # Engagement agent
│   │   └── ...
│   ├── api/                 # API routes
│   │   └── v1/
│   │       └── endpoints/   # API endpoints
│   ├── core/                # Core configuration
│   ├── db/                  # Database models
│   │   └── models/
│   ├── integrations/        # Social media integrations
│   │   ├── instagram/
│   │   ├── twitter/
│   │   └── ...
│   ├── schemas/             # Pydantic schemas
│   ├── services/            # Business logic
│   └── main.py              # FastAPI app
├── celery_app/              # Celery configuration
├── tests/                   # Tests
├── requirements.txt
├── .env.example
├── ARCHITECTURE.md          # Architecture documentation
└── README.md
```

## 🔧 Configuration

### LLM Provider
Choose between OpenAI or Anthropic in `.env`:

```bash
# For OpenAI
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
DEFAULT_MODEL=gpt-4o

# For Anthropic
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...
DEFAULT_MODEL=claude-3-5-sonnet-20241022
```

### Database
Configure PostgreSQL connection:
```bash
DATABASE_URL=postgresql://user:password@localhost:5432/smm_agent
```

## 📊 Database Models

- **User**: User accounts
- **Brand**: Social media brands managed by users
- **SocialAccount**: Connected social media accounts with tokens
- **ContentItem**: Generated and scheduled content
- **AnalyticsData**: Performance metrics
- **CalendarItem**: Content calendar entries
- **EngagementItem**: Comments and DMs to be handled
- **Task**: Agent task tracking

## 🤖 Agent System

### How It Works

1. **User submits request** via API
2. **Planner Agent** receives and analyzes the request
3. **Task decomposition**: Complex requests broken into subtasks
4. **Agent delegation**: Planner assigns tasks to specialized agents
5. **Execution**: Worker agents process their tasks
6. **Result aggregation**: Planner combines results
7. **Response**: Structured response returned to user

### Adding New Agents

1. Create agent file in `app/agents/your_agent/`
2. Extend `BaseAgent` class
3. Implement `name`, `description`, and `execute` methods
4. Register in `app/main.py` startup event

## 🔐 Security

- JWT-based authentication
- Password hashing with bcrypt
- Token encryption for social media credentials
- Environment-based secret management
- CORS configuration

## 📈 Monitoring

- Application logs in `logs/app.log`
- Celery Flower for task monitoring: `http://localhost:5555`
- Database query logging (enable with DEBUG=True)

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/unit/test_agents.py
```

## 🚢 Deployment

### Docker Deployment (Recommended)

```bash
# Build and run with docker-compose
docker-compose up -d
```

### Manual Deployment

1. Set up production database
2. Configure environment variables
3. Run with Gunicorn or Uvicorn
4. Set up reverse proxy (Nginx)
5. Configure SSL certificates
6. Set up process manager (systemd/supervisor)

## 📝 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get token

### Brands
- `POST /api/v1/brands/` - Create brand
- `GET /api/v1/brands/{id}` - Get brand details

### Content
- `POST /api/v1/content/generate` - Generate content
- `POST /api/v1/content/plan-and-execute` - Complex multi-step requests
- `GET /api/v1/content/` - List content
- `GET /api/v1/content/{id}` - Get content details

### Analytics
- `POST /api/v1/analytics/generate-report` - Generate report

### Scheduler
- `POST /api/v1/scheduler/create-calendar` - Create content calendar

### Engagement
- `POST /api/v1/engagement/generate-reply` - Generate reply

### Tasks
- `GET /api/v1/tasks/agents` - List available agents
- `GET /api/v1/tasks/` - List tasks
- `GET /api/v1/tasks/{id}` - Get task details

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes with tests
4. Submit pull request

## 📄 License

MIT License

## 🆘 Support

For issues and questions:
- Check documentation
- Review architecture docs
- Open an issue on GitHub

## 🔮 Future Enhancements

- [ ] Real-time WebSocket notifications
- [ ] Advanced A/B testing framework
- [ ] Image generation integration (DALL-E, Midjourney)
- [ ] Video editing automation
- [ ] Influencer discovery and outreach
- [ ] Sentiment analysis dashboard
- [ ] Multi-brand management dashboard
- [ ] Mobile app
- [ ] Webhook integrations

---

Built with ❤️ using FastAPI, SQLAlchemy, and AI agents
