import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API Keys
    youtube_api_key: str = os.getenv("YOUTUBE_API_KEY", "your_youtube_api_key_here")
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "your_gemini_api_key_here")
    
    # API Configuration
    max_comments: int = 100
    max_transcript_length: int = 4000
    default_keywords_count: int = 10
    
    # Quality Score Weights
    content_length_weight: float = 0.25
    summary_quality_weight: float = 0.20
    keyword_richness_weight: float = 0.20
    engagement_weight: float = 0.20
    comment_activity_weight: float = 0.15
    
    # Sentiment Analysis
    sentiment_threshold_positive: float = 0.1
    sentiment_threshold_negative: float = -0.1
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()