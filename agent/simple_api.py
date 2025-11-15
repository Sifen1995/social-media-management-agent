"""
Simplified API for testing frontend without database setup.
Provides authentication and content generation endpoints.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.agents.content.agent import ContentAgent
from app.core.config import settings

app = FastAPI(title="Social Media Agent API (Simple)")

# CORS - Allow localhost and Render URLs
allowed_origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://*.onrender.com",  # Render frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https://.*\.onrender\.com|http://localhost:\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agent
content_agent = ContentAgent()

# Pydantic models
class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: str
    password: str
    full_name: str

class LoginResponse(BaseModel):
    access_token: str
    user: dict

class Brand(BaseModel):
    id: int
    name: str
    niche: Optional[str] = "General"
    brand_voice: Optional[str] = "Professional, friendly"
    target_audience: Optional[str] = "General audience"
    goals: Optional[List[str]] = ["Increase engagement"]

class ContentGenerateRequest(BaseModel):
    brand_id: int
    platform: str
    topic: str
    content_type: str = "post"
    count: int = 2
    additional_instructions: Optional[str] = None

# In-memory storage
DEMO_USER = {
    "id": 1,
    "email": "demo@example.com",
    "full_name": "Demo User",
}

DEMO_BRANDS = [
    {
        "id": 1,
        "name": "FitLife Pro",
        "niche": "Fitness & Wellness",
        "brand_voice": "Motivating, energetic, authentic",
        "target_audience": "Fitness enthusiasts aged 25-40",
        "goals": ["Inspire daily workouts", "Build community", "Share fitness tips"]
    },
    {
        "id": 2,
        "name": "Tech Innovators",
        "niche": "Technology",
        "brand_voice": "Professional, innovative, cutting-edge",
        "target_audience": "Tech professionals and enthusiasts",
        "goals": ["Share tech insights", "Educate audience", "Establish thought leadership"]
    }
]

# Routes
@app.get("/")
async def root():
    return {
        "message": "Social Media Management Agent API (Simple Demo)",
        "status": "online",
        "llm_provider": settings.LLM_PROVIDER,
        "model": settings.DEFAULT_MODEL
    }

@app.post("/api/v1/auth/login")
async def login(request: LoginRequest):
    """Simple login - accepts any credentials for demo."""
    return {
        "access_token": "demo_token_12345",
        "user": DEMO_USER
    }

@app.post("/api/v1/auth/register")
async def register(request: RegisterRequest):
    """Simple registration - always succeeds for demo."""
    return {"message": "User created successfully"}

@app.get("/api/v1/auth/me")
async def get_current_user():
    """Get current user."""
    return DEMO_USER

@app.get("/api/v1/brands")
async def get_brands():
    """Get all brands."""
    return DEMO_BRANDS

@app.post("/api/v1/brands")
async def create_brand(brand: dict):
    """Create a new brand."""
    new_brand = {
        "id": len(DEMO_BRANDS) + 1,
        **brand
    }
    DEMO_BRANDS.append(new_brand)
    return new_brand

@app.post("/api/v1/content/generate")
async def generate_content(request: ContentGenerateRequest):
    """Generate content using AI agent."""
    try:
        # Find brand
        brand = next((b for b in DEMO_BRANDS if b["id"] == request.brand_id), None)
        if not brand:
            raise HTTPException(status_code=404, detail="Brand not found")

        # Prepare task for agent
        task = {
            "action": "generate",
            "platform": request.platform,
            "topic": request.topic,
            "content_type": request.content_type,
            "count": request.count
        }

        # Prepare context
        context = {
            "brand": brand
        }

        # Execute agent
        result = await content_agent.execute(task, context)

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/content")
async def get_content(limit: int = 10):
    """Get content list."""
    return {
        "total": 0,
        "items": []
    }

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
