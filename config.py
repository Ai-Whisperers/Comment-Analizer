# UNIFIED CONFIGURATION - SINGLE SOURCE OF TRUTH
# Eliminates all duplication and inconsistencies

import os
from typing import Dict, Any

def _detect_streamlit_cloud() -> bool:
    """Detect if running on Streamlit Cloud"""
    return (
        os.getenv('HOSTNAME', '').startswith('streamlit-') or
        'STREAMLIT_SHARING_MODE' in os.environ or
        _has_streamlit_secrets()
    )

def _has_streamlit_secrets() -> bool:
    """Check if Streamlit secrets are available"""
    try:
        import streamlit as st
        return hasattr(st, 'secrets') and len(dict(st.secrets)) > 0
    except:
        return False

def _load_config() -> Dict[str, Any]:
    """Load unified configuration"""
    
    # Load dotenv for local development
    if not _detect_streamlit_cloud():
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ImportError:
            pass
    
    # Get secrets/env based on environment  
    if _detect_streamlit_cloud():
        try:
            import streamlit as st
            get_value = lambda k, d: st.secrets.get(k, d)
        except ImportError:
            get_value = lambda k, d: os.getenv(k, d)
    else:
        get_value = lambda k, d: os.getenv(k, d)
    
    return {
        # UNIFIED: Single source for all configuration
        'openai_api_key': get_value('OPENAI_API_KEY', ''),
        'openai_modelo': get_value('OPENAI_MODEL', 'gpt-4o-mini'),
        'openai_max_tokens': int(get_value('OPENAI_MAX_TOKENS', '12000')),  # OPTIMIZED
        'openai_temperatura': float(get_value('OPENAI_TEMPERATURE', '0.0')),
        'max_comments': int(get_value('MAX_COMMENTS_PER_BATCH', '200')),  # EXTREME PERFORMANCE: Optimized for parallel processing
        'cache_ttl': int(get_value('CACHE_TTL_SECONDS', '3600')),
        'log_level': get_value('LOG_LEVEL', 'INFO'),
        
        # PRODUCTION LIMITS: Made configurable via environment variables
        'production_token_limit': int(get_value('PRODUCTION_TOKEN_LIMIT', '14000')),
        'token_threshold_high': int(get_value('TOKEN_THRESHOLD_HIGH', '14000')),  # 14K+ tokens
        'token_threshold_medium': int(get_value('TOKEN_THRESHOLD_MEDIUM', '11000')),  # 11K+ tokens  
        'token_threshold_low': int(get_value('TOKEN_THRESHOLD_LOW', '8000')),  # 8K+ tokens
        'max_comments_high': int(get_value('MAX_COMMENTS_HIGH', '120')),
        'max_comments_medium': int(get_value('MAX_COMMENTS_MEDIUM', '50')),
        'max_comments_low': int(get_value('MAX_COMMENTS_LOW', '40')),
        'max_comments_minimal': int(get_value('MAX_COMMENTS_MINIMAL', '30')),
        
        # VALIDATION LIMITS: Made configurable via environment variables
        'max_batch_size_absolute': int(get_value('MAX_BATCH_SIZE_ABSOLUTE', '120')),
        'min_batch_size_threshold': int(get_value('MIN_BATCH_SIZE_THRESHOLD', '50')),
        'max_file_comments': int(get_value('MAX_FILE_COMMENTS', '2000')),
        'min_file_comments_info': int(get_value('MIN_FILE_COMMENTS_INFO', '100')),
        'preview_length': int(get_value('PREVIEW_LENGTH', '100')),
        'memory_threshold_mb': int(get_value('MEMORY_THRESHOLD_MB', '400'))
    }

# Global configuration
config = _load_config()

# Convenience functions  
def is_streamlit_cloud() -> bool:
    return _detect_streamlit_cloud()

def get_environment_info() -> Dict[str, str]:
    return {
        'environment': 'Streamlit Cloud' if is_streamlit_cloud() else 'Local',
        'max_batch_size': str(config['max_comments']),
        'max_tokens': str(config['openai_max_tokens']),
        'model': config['openai_modelo']
    }