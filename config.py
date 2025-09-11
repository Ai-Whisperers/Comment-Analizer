# UNIFIED CONFIGURATION FOR LOCAL AND STREAMLIT CLOUD ENVIRONMENTS
# This file automatically detects the environment and applies appropriate settings

import os
from typing import Dict, Any

class EnvironmentConfig:
    """Unified configuration manager for local and Streamlit Cloud environments"""
    
    def __init__(self):
        self.is_streamlit_cloud = self._detect_streamlit_cloud()
        self._config = self._load_config()
    
    def _detect_streamlit_cloud(self) -> bool:
        """Detect if running on Streamlit Cloud"""
        return (
            os.getenv('HOSTNAME', '').startswith('streamlit-') or
            'STREAMLIT_SHARING_MODE' in os.environ or
            os.getenv('STREAMLIT_CLOUD_EMULATOR') == 'true' or
            self._has_streamlit_secrets()
        )
    
    def _has_streamlit_secrets(self) -> bool:
        """Check if Streamlit secrets are available without importing streamlit"""
        try:
            import streamlit as st
            return hasattr(st, 'secrets') and hasattr(st.secrets, 'get')
        except ImportError:
            return False
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration based on environment"""
        if self.is_streamlit_cloud:
            return self._load_streamlit_cloud_config()
        else:
            return self._load_local_config()
    
    def _load_streamlit_cloud_config(self) -> Dict[str, Any]:
        """Configuration optimized for Streamlit Cloud (1GB memory limit)"""
        try:
            import streamlit as st
            secrets = st.secrets
        except (ImportError, AttributeError):
            # Fallback to environment variables if streamlit not available
            secrets = type('MockSecrets', (), {'get': lambda k, default='': os.getenv(k, default)})()
        
        return {
            # API Configuration
            'OPENAI_API_KEY': secrets.get('OPENAI_API_KEY', ''),
            'OPENAI_MODEL': secrets.get('OPENAI_MODEL', 'gpt-4o-mini'),
            'OPENAI_MAX_TOKENS': int(secrets.get('OPENAI_MAX_TOKENS', '4000')),  # Reduced
            'OPENAI_TEMPERATURE': float(secrets.get('OPENAI_TEMPERATURE', '0.0')),
            
            # Streamlit Cloud Optimized Limits
            'MAX_COMMENTS_PER_BATCH': int(secrets.get('MAX_COMMENTS_PER_BATCH', '10')),  # Conservative
            'MAX_FILE_SIZE_MB': 3,  # Reduced for cloud
            'CACHE_TTL_SECONDS': int(secrets.get('CACHE_TTL_SECONDS', '1800')),  # 30 min
            
            # Performance Settings
            'API_RATE_LIMIT_PER_MINUTE': 30,  # Reduced for stability
            'SESSION_TIMEOUT_MINUTES': 15,   # Shorter timeout
            'ENABLE_PROGRESS_TRACKING': True,
            'BATCH_PROCESSING_DELAY': 2.0,   # Slower processing
            
            # Memory Management
            'ENABLE_MEMORY_OPTIMIZATION': True,
            'CLEAR_CACHE_INTERVAL': 900,     # 15 min
            'MAX_CACHED_ITEMS': 50,          # Reduced cache
            
            # Environment
            'APP_ENV': 'production',
            'DEBUG_MODE': False,
            'LOG_LEVEL': 'WARNING',
        }
    
    def _load_local_config(self) -> Dict[str, Any]:
        """Configuration for local development with more resources"""
        from dotenv import load_dotenv
        load_dotenv()
        
        return {
            # API Configuration
            'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY', ''),
            'OPENAI_MODEL': os.getenv('OPENAI_MODEL', 'gpt-4o-mini'),
            'OPENAI_MAX_TOKENS': int(os.getenv('OPENAI_MAX_TOKENS', '8000')),
            'OPENAI_TEMPERATURE': float(os.getenv('OPENAI_TEMPERATURE', '0.0')),
            
            # Local Development Limits (More generous)
            'MAX_COMMENTS_PER_BATCH': int(os.getenv('MAX_COMMENTS_PER_BATCH', '60')),  # Higher
            'MAX_FILE_SIZE_MB': int(os.getenv('MAX_FILE_SIZE_MB', '10')),
            'CACHE_TTL_SECONDS': int(os.getenv('CACHE_TTL_SECONDS', '3600')),  # 1 hour
            
            # Performance Settings
            'API_RATE_LIMIT_PER_MINUTE': int(os.getenv('API_RATE_LIMIT_PER_MINUTE', '60')),
            'SESSION_TIMEOUT_MINUTES': int(os.getenv('SESSION_TIMEOUT_MINUTES', '60')),
            'ENABLE_PROGRESS_TRACKING': True,
            'BATCH_PROCESSING_DELAY': 0.5,   # Faster processing
            
            # Memory Management
            'ENABLE_MEMORY_OPTIMIZATION': False,  # Not needed locally
            'CLEAR_CACHE_INTERVAL': 3600,        # 1 hour
            'MAX_CACHED_ITEMS': 200,              # More cache
            
            # Environment
            'APP_ENV': os.getenv('APP_ENV', 'development'),
            'DEBUG_MODE': os.getenv('DEBUG_MODE', 'True').lower() == 'true',
            'LOG_LEVEL': os.getenv('LOG_LEVEL', 'INFO'),
        }
    
    def get(self, key: str, default=None):
        """Get configuration value"""
        return self._config.get(key, default)
    
    def get_environment_info(self) -> Dict[str, str]:
        """Get environment information for debugging"""
        return {
            'environment': 'Streamlit Cloud' if self.is_streamlit_cloud else 'Local',
            'max_batch_size': str(self.get('MAX_COMMENTS_PER_BATCH')),
            'cache_ttl': str(self.get('CACHE_TTL_SECONDS')),
            'memory_optimization': str(self.get('ENABLE_MEMORY_OPTIMIZATION')),
            'debug_mode': str(self.get('DEBUG_MODE')),
        }

# Global configuration instance
config = EnvironmentConfig()

# Convenience functions
def get_config(key: str, default=None):
    """Get configuration value"""
    return config.get(key, default)

def is_streamlit_cloud() -> bool:
    """Check if running on Streamlit Cloud"""
    return config.is_streamlit_cloud

def get_environment_info() -> Dict[str, str]:
    """Get environment information"""
    return config.get_environment_info()