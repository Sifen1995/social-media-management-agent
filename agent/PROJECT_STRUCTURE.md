# Project Structure

```
social-media-management-agent/
│
├── agent/
│   ├── app/
│   │   ├── __init__.py
│   │   │
│   │   ├── main.py                      # FastAPI application entry point
│   │   │
│   │   ├── agents/                      # Multi-agent system
│   │   │   ├── __init__.py
│   │   │   │
│   │   │   ├── base/                    # Base agent classes
│   │   │   │   ├── __init__.py
│   │   │   │   ├── agent.py             # Abstract base agent class
│   │   │   │   └── orchestrator.py      # Agent orchestration logic
│   │   │   │
│   │   │   ├── planner/                 # Planner (Master) Agent
│   │   │   │   ├── __init__.py
│   │   │   │   ├── agent.py
│   │   │   │   └── prompts.py
│   │   │   │
│   │   │   ├── content/                 # Content Generation Agent
│   │   │   │   ├── __init__.py
│   │   │   │   ├── agent.py
│   │   │   │   └── prompts.py
│   │   │   │
│   │   │   ├── analytics/               # Analytics Agent
│   │   │   │   ├── __init__.py
│   │   │   │   ├── agent.py
│   │   │   │   └── prompts.py
│   │   │   │
│   │   │   ├── scheduler/               # Scheduler Agent
│   │   │   │   ├── __init__.py
│   │   │   │   ├── agent.py
│   │   │   │   └── prompts.py
│   │   │   │
│   │   │   ├── engagement/              # Engagement Agent
│   │   │   │   ├── __init__.py
│   │   │   │   ├── agent.py
│   │   │   │   └── prompts.py
│   │   │   │
│   │   │   ├── social_listening/        # Social Listening Agent
│   │   │   │   ├── __init__.py
│   │   │   │   ├── agent.py
│   │   │   │   └── prompts.py
│   │   │   │
│   │   │   └── optimizer/               # Optimizer Agent
│   │   │       ├── __init__.py
│   │   │       ├── agent.py
│   │   │       └── prompts.py
│   │   │
│   │   ├── api/                         # API layer
│   │   │   ├── __init__.py
│   │   │   │
│   │   │   ├── dependencies.py          # Shared dependencies (auth, db session)
│   │   │   │
│   │   │   └── v1/                      # API version 1
│   │   │       ├── __init__.py
│   │   │       ├── router.py            # Main v1 router
│   │   │       │
│   │   │       └── endpoints/           # API endpoints
│   │   │           ├── __init__.py
│   │   │           ├── auth.py          # Authentication endpoints
│   │   │           ├── brands.py        # Brand management
│   │   │           ├── content.py       # Content generation & management
│   │   │           ├── analytics.py     # Analytics endpoints
│   │   │           ├── scheduler.py     # Scheduling endpoints
│   │   │           ├── engagement.py    # Engagement endpoints
│   │   │           ├── social_accounts.py # Social account connections
│   │   │           └── tasks.py         # Task management
│   │   │
│   │   ├── core/                        # Core configurations
│   │   │   ├── __init__.py
│   │   │   ├── config.py                # App configuration
│   │   │   ├── security.py              # JWT, password hashing
│   │   │   └── logging.py               # Logging configuration
│   │   │
│   │   ├── db/                          # Database
│   │   │   ├── __init__.py
│   │   │   ├── session.py               # Database session management
│   │   │   ├── base.py                  # Base model class
│   │   │   │
│   │   │   └── models/                  # SQLAlchemy models
│   │   │       ├── __init__.py
│   │   │       ├── user.py
│   │   │       ├── brand.py
│   │   │       ├── social_account.py
│   │   │       ├── content.py
│   │   │       ├── analytics.py
│   │   │       ├── calendar.py
│   │   │       ├── engagement.py
│   │   │       └── task.py
│   │   │
│   │   ├── integrations/                # Social media platform integrations
│   │   │   ├── __init__.py
│   │   │   ├── base.py                  # Base integration class
│   │   │   │
│   │   │   ├── instagram/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── client.py            # Instagram Graph API client
│   │   │   │   └── models.py
│   │   │   │
│   │   │   ├── facebook/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── client.py
│   │   │   │   └── models.py
│   │   │   │
│   │   │   ├── tiktok/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── client.py
│   │   │   │   └── models.py
│   │   │   │
│   │   │   ├── twitter/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── client.py
│   │   │   │   └── models.py
│   │   │   │
│   │   │   ├── youtube/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── client.py
│   │   │   │   └── models.py
│   │   │   │
│   │   │   └── linkedin/
│   │   │       ├── __init__.py
│   │   │       ├── client.py
│   │   │       └── models.py
│   │   │
│   │   ├── schemas/                     # Pydantic schemas (request/response models)
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── brand.py
│   │   │   ├── content.py
│   │   │   ├── analytics.py
│   │   │   ├── calendar.py
│   │   │   ├── engagement.py
│   │   │   ├── task.py
│   │   │   └── social_account.py
│   │   │
│   │   ├── services/                    # Business logic services
│   │   │   ├── __init__.py
│   │   │   ├── llm_service.py           # LLM integration (OpenAI/Anthropic)
│   │   │   ├── content_service.py       # Content management logic
│   │   │   ├── analytics_service.py     # Analytics processing
│   │   │   ├── scheduler_service.py     # Scheduling logic
│   │   │   └── encryption_service.py    # Token encryption/decryption
│   │   │
│   │   └── utils/                       # Utility functions
│   │       ├── __init__.py
│   │       ├── datetime_utils.py
│   │       ├── text_utils.py
│   │       └── validators.py
│   │
│   ├── celery_app/                      # Celery task queue
│   │   ├── __init__.py
│   │   ├── celery.py                    # Celery configuration
│   │   ├── tasks.py                     # Background tasks
│   │   └── beat_schedule.py             # Periodic task schedule
│   │
│   ├── tests/                           # Tests
│   │   ├── __init__.py
│   │   ├── conftest.py                  # Pytest configuration
│   │   │
│   │   ├── unit/                        # Unit tests
│   │   │   ├── __init__.py
│   │   │   ├── test_agents.py
│   │   │   ├── test_services.py
│   │   │   └── test_integrations.py
│   │   │
│   │   └── integration/                 # Integration tests
│   │       ├── __init__.py
│   │       ├── test_api.py
│   │       └── test_workflows.py
│   │
│   ├── scripts/                         # Utility scripts
│   │   ├── init_db.py                   # Database initialization
│   │   ├── seed_data.py                 # Seed sample data
│   │   └── migrate.py                   # Database migrations
│   │
│   ├── alembic/                         # Database migrations (Alembic)
│   │   ├── versions/
│   │   ├── env.py
│   │   └── alembic.ini
│   │
│   ├── logs/                            # Application logs
│   ├── data/                            # Data files (if needed)
│   │
│   ├── .env.example                     # Example environment variables
│   ├── .env                             # Environment variables (gitignored)
│   ├── .gitignore
│   ├── requirements.txt                 # Python dependencies
│   ├── README.md                        # Project documentation
│   ├── ARCHITECTURE.md                  # Architecture documentation
│   └── PROJECT_STRUCTURE.md             # This file
│
└── docker-compose.yml                   # Docker services (PostgreSQL, Redis)
```

## Key Components

### 1. **app/main.py**
- FastAPI application initialization
- Middleware setup
- Router registration
- CORS configuration

### 2. **app/agents/**
- Multi-agent system implementation
- Each agent is self-contained with its own logic and prompts
- Orchestrator coordinates agent interactions

### 3. **app/api/**
- RESTful API endpoints
- Request/response validation
- Authentication and authorization

### 4. **app/db/**
- Database models and session management
- SQLAlchemy ORM configuration

### 5. **app/integrations/**
- Platform-specific API clients
- Standardized interface for all platforms

### 6. **app/services/**
- Business logic separated from API layer
- Reusable service functions

### 7. **celery_app/**
- Background job processing
- Scheduled tasks (content posting, analytics fetching)

## Data Flow

```
User Request → FastAPI Endpoint → Agent Orchestrator → Specific Agent(s)
                                                              ↓
                                                         LLM Service
                                                              ↓
                                                    DB/Integration Layer
                                                              ↓
                                                          Response
```

## Configuration Files

- **.env**: Environment-specific configuration
- **requirements.txt**: Python package dependencies
- **alembic.ini**: Database migration configuration
- **docker-compose.yml**: Development environment setup
