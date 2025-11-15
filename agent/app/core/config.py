"""
Application configuration management.
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    # Application
    APP_NAME: str = "Social Media Management Agent"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"

    # Security
    SECRET_KEY: str = "CHANGE_THIS_TO_A_RANDOM_SECRET_KEY"
    TOKEN_ENCRYPTION_KEY: str = "CHANGE_THIS_TO_A_32_BYTE_BASE64_KEY"  # For encrypting social media tokens
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    ALGORITHM: str = "HS256"

    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/smm_agent"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # LLM Configuration
    LLM_PROVIDER: str = "gemini"  # openai, anthropic, gemini
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    DEFAULT_MODEL: str = "gemini-1.5-pro"  # gpt-4o, claude-3-5-sonnet-20241022, gemini-1.5-pro, gemini-1.5-flash
    LLM_TEMPERATURE: float = 0.7
    LLM_MAX_TOKENS: int = 8192  # Increased for Gemini's larger context

    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    # CORS
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]

    # Social Media Platform API Keys
    INSTAGRAM_APP_ID: Optional[str] = None
    INSTAGRAM_APP_SECRET: Optional[str] = None

    FACEBOOK_APP_ID: Optional[str] = None
    FACEBOOK_APP_SECRET: Optional[str] = None

    TWITTER_API_KEY: Optional[str] = None
    TWITTER_API_SECRET: Optional[str] = None
    TWITTER_BEARER_TOKEN: Optional[str] = None

    TIKTOK_CLIENT_KEY: Optional[str] = None
    TIKTOK_CLIENT_SECRET: Optional[str] = None

    YOUTUBE_CLIENT_ID: Optional[str] = None
    YOUTUBE_CLIENT_SECRET: Optional[str] = None

    LINKEDIN_CLIENT_ID: Optional[str] = None
    LINKEDIN_CLIENT_SECRET: Optional[str] = None

    # Encryption for storing tokens
    ENCRYPTION_KEY: Optional[str] = None  # Fernet key for encrypting tokens

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
