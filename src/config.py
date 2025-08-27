"""
Configuration settings for Personal Paraguay Fiber Comments Analysis System
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Configure logging based on environment
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class Config:
    """Configuration class for API keys and settings"""
    
    # API Configuration - Loaded from .env file, NEVER hardcoded
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
    OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "4000"))
    OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
    
    # API Timeout Settings (in seconds)
    API_TIMEOUT_SHORT = int(os.getenv("API_TIMEOUT_SHORT", "10"))  # For quick operations
    API_TIMEOUT_MEDIUM = int(os.getenv("API_TIMEOUT_MEDIUM", "30"))  # For standard operations
    API_TIMEOUT_LONG = int(os.getenv("API_TIMEOUT_LONG", "60"))  # For batch operations
    API_TIMEOUT_MAX = int(os.getenv("API_TIMEOUT_MAX", "120"))  # Maximum allowed timeout
    
    # Language Settings
    PRIMARY_LANGUAGE = "es"  # Spanish
    SECONDARY_LANGUAGE = "gn"  # Guarani
    TARGET_LANGUAGE = "es"  # Translate to Spanish
    
    # Analysis Settings
    SENTIMENT_CONFIDENCE_THRESHOLD = 0.7
    TRANSLATION_CONFIDENCE_THRESHOLD = 0.8
    BATCH_SIZE = 100
    MAX_RETRIES = 3
    
    # File Paths
    RAW_DATA_PATH = "data/raw/"
    PROCESSED_DATA_PATH = "data/processed/"
    OUTPUTS_PATH = "outputs/"
    
    # Dashboard Settings
    DASHBOARD_TITLE = "Personal Paraguay - Customer Comments Analysis"
    DASHBOARD_PORT = int(os.getenv("STREAMLIT_PORT", "8501"))
    
    # Logging
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Validation function
def validate_config():
    """Validate that required configuration is present"""
    required_keys = [
        "OPENAI_API_KEY"
    ]
    
    missing_keys = []
    for key in required_keys:
        if not getattr(Config, key):
            missing_keys.append(key)
    
    if missing_keys:
        raise ValueError(f"Missing required environment variables: {missing_keys}")
    
    return True