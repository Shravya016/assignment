from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Video Recommendation Engine"
    
    # API Base URLs
    API_BASE_URL: str = os.getenv("API_BASE_URL", "https://api.socialverseapp.com")
    
    # Authentication
    FLIC_TOKEN: str = os.getenv("FLIC_TOKEN", "")
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./video_recommendation.db")
    
    # API Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Caching
    CACHE_TTL: int = 3600  # 1 hour in seconds
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    # Model Parameters
    EMBEDDING_DIM: int = 128
    NUM_FACTORS: int = 50
    LEARNING_RATE: float = 0.001
    
    class Config:
        case_sensitive = True

settings = Settings() 