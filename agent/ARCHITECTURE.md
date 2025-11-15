# Social Media Management Agent - System Architecture

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Client Applications                       │
│                    (Web UI, Mobile, API Clients)                 │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                       FastAPI Backend                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Auth API   │  │ Content API  │  │ Analytics API│         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Multi-Agent Orchestrator                        │
│                                                                   │
│    ┌──────────────────────────────────────────────────┐         │
│    │           Planner Agent (Master)                 │         │
│    │  • Analyzes user requests                        │         │
│    │  • Decomposes tasks                              │         │
│    │  • Delegates to worker agents                    │         │
│    │  • Coordinates execution                         │         │
│    └──────────────────────────────────────────────────┘         │
│                            │                                     │
│         ┌──────────────────┼──────────────────┐                │
│         ▼                  ▼                  ▼                 │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Content    │  │  Analytics   │  │  Scheduler   │          │
│  │   Agent     │  │    Agent     │  │    Agent     │          │
│  └─────────────┘  └──────────────┘  └──────────────┘          │
│         ▼                  ▼                  ▼                 │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Engagement  │  │Social Listen │  │   Optimizer  │          │
│  │   Agent     │  │    Agent     │  │    Agent     │          │
│  └─────────────┘  └──────────────┘  └──────────────┘          │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Service Layer                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  LLM Service │  │ DB Service   │  │Task Scheduler│         │
│  │  (OpenAI/    │  │ (SQLAlchemy) │  │   (Celery)   │         │
│  │  Anthropic)  │  │              │  │              │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│              Social Media Platform Integrations                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐          │
│  │Instagram │ │ Facebook │ │ TikTok   │ │ Twitter/X│          │
│  │   API    │ │   API    │ │   API    │ │   API    │          │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘          │
│  ┌──────────┐ ┌──────────┐                                     │
│  │ YouTube  │ │ LinkedIn │                                     │
│  │   API    │ │   API    │                                     │
│  └──────────┘ └──────────┘                                     │
└─────────────────────────────────────────────────────────────────┘
```

## 🤖 Multi-Agent Architecture

### Agent Hierarchy

1. **Planner Agent (Master Agent)**
   - Role: Task decomposition and orchestration
   - Responsibilities:
     - Parse user requests
     - Break down complex tasks into subtasks
     - Route tasks to appropriate worker agents
     - Aggregate results
     - Handle multi-step workflows

2. **Worker Agents (Specialized Agents)**

   **Content Agent**
   - Generate platform-specific content
   - Create captions, hashtags, CTAs
   - Adapt brand voice and tone
   - Generate content variations

   **Analytics Agent**
   - Analyze engagement metrics
   - Identify trends and patterns
   - Generate performance reports
   - Provide actionable insights

   **Scheduler Agent**
   - Create content calendars
   - Determine optimal posting times
   - Schedule posts across platforms
   - Manage posting queues

   **Engagement Agent**
   - Draft comment replies
   - Handle DM responses
   - Monitor community interactions
   - Filter spam and harmful content

   **Social Listening Agent**
   - Track trends and hashtags
   - Monitor competitor content
   - Identify content opportunities
   - Analyze audience conversations

   **Optimizer Agent**
   - A/B testing recommendations
   - Content performance optimization
   - Growth strategy suggestions
   - Campaign optimization

## 🗃️ Database Schema

### Tables

**users**
- id (PK)
- email
- hashed_password
- full_name
- created_at
- is_active

**brands**
- id (PK)
- user_id (FK)
- name
- niche
- brand_voice
- target_audience
- goals
- visual_style
- created_at

**social_accounts**
- id (PK)
- brand_id (FK)
- platform (Instagram, Facebook, TikTok, etc.)
- account_username
- access_token (encrypted)
- refresh_token (encrypted)
- token_expires_at
- is_active
- connected_at

**content_items**
- id (PK)
- brand_id (FK)
- platform
- content_type (post, reel, story, tweet, etc.)
- caption
- hashtags (JSON)
- media_urls (JSON)
- status (draft, scheduled, published, failed)
- scheduled_for
- published_at
- created_by_agent
- created_at

**analytics_data**
- id (PK)
- content_item_id (FK)
- platform
- likes
- comments
- shares
- saves
- reach
- impressions
- engagement_rate
- fetched_at

**content_calendar**
- id (PK)
- brand_id (FK)
- date
- time_slot
- platform
- content_item_id (FK, nullable)
- status (planned, scheduled, published)
- notes

**engagement_queue**
- id (PK)
- brand_id (FK)
- platform
- engagement_type (comment, dm, mention)
- source_id (platform-specific ID)
- content
- suggested_reply
- status (pending, approved, sent, ignored)
- created_at

**tasks**
- id (PK)
- brand_id (FK)
- task_type
- description
- parameters (JSON)
- status (pending, in_progress, completed, failed)
- result (JSON)
- assigned_agent
- created_at
- completed_at

## 🔄 Workflow Examples

### Workflow 1: Content Generation Request

```
User Request: "Create 5 Instagram posts about sustainable fashion"
    │
    ▼
Planner Agent receives request
    │
    ├─ Extracts parameters: platform=Instagram, count=5, topic=sustainable fashion
    │
    ├─ Delegates to Content Agent
    │
    ▼
Content Agent processes
    │
    ├─ Fetches brand voice and style
    ├─ Generates 5 post variations using LLM
    ├─ Creates hashtags and CTAs
    │
    ▼
Returns results to Planner Agent
    │
    ▼
Planner Agent formats response
    │
    ▼
API returns to user
```

### Workflow 2: Analytics Report Generation

```
User Request: "Analyze last month's performance"
    │
    ▼
Planner Agent receives request
    │
    ├─ Delegates to Analytics Agent
    │
    ▼
Analytics Agent processes
    │
    ├─ Fetches analytics data from DB
    ├─ Calculates metrics and trends
    ├─ Uses LLM to generate insights
    ├─ Creates recommendations
    │
    ▼
Returns report to Planner Agent
    │
    ▼
API returns formatted report
```

### Workflow 3: Automated Posting

```
Scheduler runs every minute (Celery Beat)
    │
    ▼
Checks content_items where status='scheduled' AND scheduled_for <= now
    │
    ▼
For each item:
    │
    ├─ Get platform and credentials
    ├─ Call platform integration
    ├─ Post content
    ├─ Update status to 'published'
    ├─ Store post_id for analytics
    │
    ▼
Log results
```

## 🔐 Security Considerations

1. **Token Encryption**: All social media access tokens encrypted in DB
2. **API Authentication**: JWT-based authentication for all endpoints
3. **Rate Limiting**: Implemented per platform API limits
4. **Input Validation**: Pydantic models for all inputs
5. **Secret Management**: Environment variables for sensitive data

## 📊 Technology Stack

- **Backend Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Task Queue**: Celery with Redis broker
- **LLM Integration**: OpenAI API / Anthropic Claude API
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt
- **Social Media APIs**: Official SDKs where available
- **Caching**: Redis
- **Environment Management**: python-decouple

## 🚀 Deployment Architecture

```
┌─────────────┐
│   Nginx     │ (Reverse Proxy)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  FastAPI    │ (Uvicorn workers)
│  Application│
└──────┬──────┘
       │
       ├──────────────┐
       │              │
       ▼              ▼
┌─────────────┐  ┌─────────────┐
│ PostgreSQL  │  │   Redis     │
│  Database   │  │ (Cache/Queue)│
└─────────────┘  └─────────────┘
                       │
                       ▼
                 ┌─────────────┐
                 │   Celery    │
                 │   Workers   │
                 └─────────────┘
```

## 📝 API Design Principles

1. RESTful design
2. Versioned endpoints (/api/v1/)
3. Clear error messages
4. Pagination for list endpoints
5. Filtering and sorting support
6. Comprehensive documentation (OpenAPI/Swagger)
