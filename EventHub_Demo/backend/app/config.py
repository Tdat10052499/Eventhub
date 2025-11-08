"""
Application Configuration
Loads environment variables and provides settings
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres123@localhost:5432/eventhub_db"
    
    # Auth0 Configuration
    AUTH0_DOMAIN: str = "dev-q886n3eebgb8g04f.us.auth0.com"
    AUTH0_API_AUDIENCE: str = "https://eventhub-api"
    AUTH0_ALGORITHMS: str = "RS256"
    AUTH0_ISSUER: str = "https://dev-q886n3eebgb8g04f.us.auth0.com/"
    
    # Web App Auth0 (Admin)
    AUTH0_WEB_CLIENT_ID: str = "yGm0uw9aLN9YSe8qVB2mq79ylDSvoJcL"
    AUTH0_WEB_CLIENT_SECRET: str = "N-SAuJxY5WT5nIxil9Jvqn_bTWXPj_hiVDtmapyhrspXfLGJxtZic1e-hkQZz0qr"
    
    # Mobile App Auth0 (User)
    AUTH0_MOBILE_CLIENT_ID: str = "2VjwUVUqQBdMPWvUuAIVayYILciirQwW"
    AUTH0_MOBILE_CLIENT_SECRET: str = "6hBorHxLrQXc3FR1vRxYpgYahqnVqvNfwPjuOdvmIXpt5gNpch0ykoEGG-KZoKp3"
    
    # File Upload
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: set = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
    
    # Application
    APP_NAME: str = "EventHub API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # API
    API_PREFIX: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()
