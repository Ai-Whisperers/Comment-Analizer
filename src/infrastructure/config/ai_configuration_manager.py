"""
AI Configuration Manager - Centralized configuration system
PHASE 2: Eliminates hardcoding and provides secure configuration hierarchy
"""
import os
import logging
from typing import Dict, Any, Optional, Union
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class ConfigurationSource(Enum):
    """Sources of configuration in priority order"""
    ENVIRONMENT = "environment"
    SECRETS = "streamlit_secrets"
    CONSTANTS = "ai_constants"
    DEFAULTS = "defaults"


@dataclass
class AIConfiguration:
    """Complete AI configuration with validation and sources"""
    
    # OpenAI Configuration
    api_key: str
    model: str = "gpt-4o-mini"
    temperature: float = 0.0
    max_tokens: int = 12000  # FASE 3: Increased from 8K to 12K to support larger batches
    seed: Optional[int] = 12345
    
    # Batch Processing Configuration - OPTIMIZED for better performance
    max_comments_per_batch: int = 200  # EXTREME PERFORMANCE: Optimized for parallel processing (matches config.py)
    batch_retry_count: int = 1  # PERFORMANCE: Reduced retries for faster processing
    batch_retry_base_delay: float = 0.5
    
    # Confidence and Validation Configuration
    min_confidence_threshold: float = 0.45  # Reduced from 0.5 for better success rate
    adaptive_confidence_enabled: bool = True
    confidence_adjustment_small_batch: float = -0.05  # Easier threshold for small batches
    confidence_adjustment_mini_model: float = -0.05   # Easier threshold for mini models
    
    # Cache Configuration
    cache_enabled: bool = True
    cache_max_size: int = 50
    cache_ttl_seconds: int = 3600
    
    # Retry Strategy Configuration
    intelligent_retry_enabled: bool = True
    deterministic_skip_retry: bool = True  # Skip retries if deterministic
    retry_temperature_increment: float = 0.1  # Temperature increase per retry
    max_retry_temperature: float = 0.3  # Maximum temperature for retries
    
    # Security Configuration
    mask_sensitive_logs: bool = True
    log_configuration_values: bool = False  # Don't log sensitive config
    
    # Source tracking for debugging
    configuration_sources: Dict[str, ConfigurationSource] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate configuration after initialization"""
        self._validate_configuration()
    
    def _validate_configuration(self):
        """Validate all configuration parameters"""
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        if not (0.0 <= self.temperature <= 2.0):
            raise ValueError("Temperature must be between 0.0 and 2.0")
        
        if not (0.0 <= self.min_confidence_threshold <= 1.0):
            raise ValueError("Confidence threshold must be between 0.0 and 1.0")
        
        if self.max_comments_per_batch > 120:  # Use configurable absolute limit
            raise ValueError("Max comments per batch cannot exceed 120 (configurable safety limit)")
        
        if self.max_comments_per_batch < 1:
            raise ValueError("Max comments per batch must be at least 1")
    
    def is_deterministic(self) -> bool:
        """Check if configuration is deterministic"""
        return abs(self.temperature) < 0.001 and self.seed is not None
    
    def get_effective_confidence_threshold(self, batch_size: int = 20, model: str = None) -> float:
        """Calculate effective confidence threshold with adjustments"""
        threshold = self.min_confidence_threshold
        
        if self.adaptive_confidence_enabled:
            # Adjust for small batches (less data = easier threshold)
            if batch_size < 10:
                threshold += self.confidence_adjustment_small_batch
            
            # Adjust for mini models (lower capability = easier threshold)
            if model and "mini" in model.lower():
                threshold += self.confidence_adjustment_mini_model
        
        # Ensure threshold stays within valid bounds
        return max(0.0, min(1.0, threshold))
    
    def get_retry_temperature(self, retry_attempt: int) -> float:
        """Calculate temperature for retry attempts"""
        if not self.intelligent_retry_enabled:
            return self.temperature
        
        # For deterministic configs, add small variation for retries
        retry_temp = self.temperature + (retry_attempt * self.retry_temperature_increment)
        return min(retry_temp, self.max_retry_temperature)
    
    def should_skip_retry(self, retry_attempt: int) -> bool:
        """Determine if retry should be skipped based on configuration"""
        if not self.intelligent_retry_enabled:
            return False
        
        # Skip retries for deterministic configuration (unless we're adding temperature variation)
        if self.deterministic_skip_retry and self.is_deterministic():
            # Only skip if we're not adding temperature variation
            if self.retry_temperature_increment <= 0:
                return True
        
        return False


class AIConfigurationManager:
    """
    Centralized AI configuration manager with hierarchical configuration loading
    
    Priority order:
    1. Environment variables (highest priority)
    2. Streamlit secrets
    3. AI Engine constants
    4. Default values (lowest priority)
    """
    
    def __init__(self, streamlit_secrets: Optional[Dict] = None):
        self.streamlit_secrets = streamlit_secrets or {}
        self._configuration: Optional[AIConfiguration] = None
        self._load_configuration()
    
    def _load_configuration(self):
        """Load configuration from all sources with proper hierarchy"""
        logger.info("🔧 Loading AI configuration from hierarchical sources...")
        
        # Load AI Engine constants for defaults
        try:
            from ..external_services.ai_engine_constants import AIEngineConstants
            constants_available = True
        except ImportError:
            logger.warning("⚠️ AIEngineConstants not available, using fallback defaults")
            constants_available = False
        
        config_values = {}
        sources = {}
        
        # Helper function to get value with source tracking
        def get_config_value(key: str, env_var: str, secret_key: str, 
                           constant_value: Any = None, default_value: Any = None) -> Any:
            # Priority 1: Environment variables
            env_value = os.getenv(env_var)
            if env_value is not None:
                sources[key] = ConfigurationSource.ENVIRONMENT
                return env_value
            
            # Priority 2: Streamlit secrets
            secret_value = self.streamlit_secrets.get(secret_key)
            if secret_value is not None:
                sources[key] = ConfigurationSource.SECRETS
                return secret_value
            
            # Priority 3: AI Engine constants
            if constant_value is not None:
                sources[key] = ConfigurationSource.CONSTANTS
                return constant_value
            
            # Priority 4: Default values
            sources[key] = ConfigurationSource.DEFAULTS
            return default_value
        
        # Load all configuration values
        api_key = get_config_value(
            "api_key", "OPENAI_API_KEY", "OPENAI_API_KEY", 
            default_value=None
        )
        
        model = get_config_value(
            "model", "OPENAI_MODEL", "OPENAI_MODEL",
            constant_value=getattr(AIEngineConstants, 'DEFAULT_MODEL', None) if constants_available else None,
            default_value="gpt-4o-mini"
        )
        
        temperature = float(get_config_value(
            "temperature", "OPENAI_TEMPERATURE", "OPENAI_TEMPERATURE",
            constant_value=getattr(AIEngineConstants, 'DEFAULT_TEMPERATURE', None) if constants_available else None,
            default_value="0.0"
        ))
        
        max_tokens = int(get_config_value(
            "max_tokens", "OPENAI_MAX_TOKENS", "OPENAI_MAX_TOKENS",
            default_value="12000"  # FASE 3: Increased default to match AIConfiguration
        ))
        
        max_comments = int(get_config_value(
            "max_comments_per_batch", "MAX_COMMENTS_PER_BATCH", "MAX_COMMENTS_PER_BATCH",
            default_value="40"  # FASE 1: Updated to match optimized batch size
        ))
        
        cache_ttl = int(get_config_value(
            "cache_ttl_seconds", "CACHE_TTL_SECONDS", "CACHE_TTL_SECONDS",
            constant_value=getattr(AIEngineConstants, 'DEFAULT_CACHE_TTL', None) if constants_available else None,
            default_value="3600"
        ))
        
        min_confidence = float(get_config_value(
            "min_confidence_threshold", "MIN_CONFIDENCE_THRESHOLD", "MIN_CONFIDENCE_THRESHOLD",
            constant_value=getattr(AIEngineConstants, 'MIN_CONFIDENCE_THRESHOLD', None) if constants_available else None,
            default_value="0.45"  # Reduced from 0.5 for better success rate
        ))
        
        seed_value = get_config_value(
            "seed", "AI_SEED", "AI_SEED",
            constant_value=getattr(AIEngineConstants, 'FIXED_SEED', None) if constants_available else None,
            default_value="12345"
        )
        
        # Create configuration object
        self._configuration = AIConfiguration(
            api_key=api_key,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            seed=int(seed_value) if seed_value else None,
            max_comments_per_batch=max_comments,
            cache_ttl_seconds=cache_ttl,
            min_confidence_threshold=min_confidence,
            configuration_sources=sources
        )
        
        # Log configuration summary (without sensitive data)
        self._log_configuration_summary()
    
    def _log_configuration_summary(self):
        """Log configuration summary without exposing sensitive data"""
        if not self._configuration:
            return
        
        config = self._configuration
        
        # Create safe summary
        summary = {
            "model": config.model,
            "temperature": config.temperature,
            "max_tokens": config.max_tokens,
            "max_comments_per_batch": config.max_comments_per_batch,
            "min_confidence_threshold": config.min_confidence_threshold,
            "is_deterministic": config.is_deterministic(),
            "intelligent_retry_enabled": config.intelligent_retry_enabled,
            "adaptive_confidence_enabled": config.adaptive_confidence_enabled,
            "api_key_configured": bool(config.api_key and len(config.api_key) > 10)
        }
        
        # Log source information for debugging
        source_summary = {}
        for key, source in config.configuration_sources.items():
            if key != "api_key":  # Never log API key source for security
                source_summary[key] = source.value
        
        logger.info(f"🔧 AI Configuration loaded: {summary}")
        logger.debug(f"🔍 Configuration sources: {source_summary}")
        
        # Log configuration status
        if config.is_deterministic():
            logger.info("🎯 Deterministic mode active - intelligent retry enabled for variation")
        
        if config.max_comments_per_batch > 30:
            logger.warning(f"⚠️ Large batch size configured: {config.max_comments_per_batch} - monitor token usage")
    
    def get_configuration(self) -> AIConfiguration:
        """Get the current AI configuration"""
        if not self._configuration:
            raise ValueError("Configuration not loaded")
        return self._configuration
    
    def reload_configuration(self, new_secrets: Optional[Dict] = None):
        """Reload configuration with new secrets if provided"""
        if new_secrets:
            self.streamlit_secrets = new_secrets
        self._load_configuration()
    
    def validate_configuration(self) -> bool:
        """Validate current configuration and return True if valid"""
        try:
            if not self._configuration:
                return False
            
            # Configuration validation is done in __post_init__
            return True
            
        except Exception as e:
            logger.error(f"❌ Configuration validation failed: {e}")
            return False
    
    def get_masked_config_for_display(self) -> Dict[str, Any]:
        """Get configuration for display with sensitive data masked"""
        if not self._configuration:
            return {}
        
        config = self._configuration
        
        return {
            "model": config.model,
            "temperature": config.temperature,
            "max_tokens": config.max_tokens,
            "max_comments_per_batch": config.max_comments_per_batch,
            "confidence_threshold": config.min_confidence_threshold,
            "cache_enabled": config.cache_enabled,
            "intelligent_retry": config.intelligent_retry_enabled,
            "api_key": "***" + config.api_key[-4:] if config.api_key and len(config.api_key) > 4 else "Not configured",
            "deterministic": config.is_deterministic()
        }


# Global configuration manager instance
_global_config_manager: Optional[AIConfigurationManager] = None


def get_ai_configuration_manager(streamlit_secrets: Optional[Dict] = None) -> AIConfigurationManager:
    """Get or create the global AI configuration manager"""
    global _global_config_manager
    
    if _global_config_manager is None or streamlit_secrets is not None:
        _global_config_manager = AIConfigurationManager(streamlit_secrets)
    
    return _global_config_manager


def get_ai_configuration(streamlit_secrets: Optional[Dict] = None) -> AIConfiguration:
    """Get the current AI configuration"""
    manager = get_ai_configuration_manager(streamlit_secrets)
    return manager.get_configuration()


def reload_ai_configuration(streamlit_secrets: Optional[Dict] = None):
    """Reload the global AI configuration"""
    global _global_config_manager
    if _global_config_manager:
        _global_config_manager.reload_configuration(streamlit_secrets)
    else:
        _global_config_manager = AIConfigurationManager(streamlit_secrets)