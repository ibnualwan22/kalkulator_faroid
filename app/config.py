from __future__ import annotations

"""
Konfigurasi aplikasi Kalkulator Faroid
"""

from pydantic_settings import BaseSettings
from typing import List
import os
from pathlib import Path


# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """Settings untuk aplikasi"""
    
    # Application
    APP_NAME: str = "Kalkulator Faroid"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000"
    ]
    
    # Database PostgreSQL
    DATABASE_URL: str = "postgresql://postgres:uqdzpqb214@localhost:5432/faroid_db"
    DATABASE_ECHO: bool = False
    
    # Security (optional)
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()
