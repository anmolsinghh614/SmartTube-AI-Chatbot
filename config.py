"""
Configuration file for YouTube to Chatbot
"""

import os
from typing import Optional

class Config:
    """Configuration class for the YouTube to Chatbot application"""
    
    # OpenAI Configuration
    OPENAI_API_KEY: Optional[str] = os.environ.get("OPENAI_API_KEY")
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    OPENAI_TEMPERATURE: float = 0.0
    
    # LangChain Configuration
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    MAX_TOKENS: int = 4000
    
    # Vector Store Configuration
    VECTOR_STORE_TYPE: str = "chroma"
    
    # YouTube Configuration
    YOUTUBE_URL_PATTERN: str = r'(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})'
    CHANNEL_ID_PATTERN: str = r'^UC[a-zA-Z0-9_-]{22}$'
    
    # Application Configuration
    APP_NAME: str = "YouTube to Chatbot"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.environ.get("DEBUG", "False").lower() == "true"
    
    # File Paths
    OUTPUT_DIR: str = "output"
    LOG_DIR: str = "logs"
    
    @classmethod
    def validate_api_key(cls) -> bool:
        """Validate if OpenAI API key is set and has correct format"""
        if not cls.OPENAI_API_KEY:
            return False
        return cls.OPENAI_API_KEY.startswith('sk-') and len(cls.OPENAI_API_KEY) > 20
    
    @classmethod
    def get_api_key(cls) -> str:
        """Get OpenAI API key with validation"""
        if not cls.validate_api_key():
            raise ValueError("Invalid or missing OpenAI API key")
        return cls.OPENAI_API_KEY
    
    @classmethod
    def create_directories(cls):
        """Create necessary directories"""
        os.makedirs(cls.OUTPUT_DIR, exist_ok=True)
        os.makedirs(cls.LOG_DIR, exist_ok=True) 