"""
🌩️ Configuración específica para emular Streamlit Cloud
Este archivo sobrescribe configuraciones para forzar el comportamiento de Streamlit Cloud
"""

import os
import streamlit as st
from typing import Dict, Any

class StreamlitCloudConfig:
    """Configuración que fuerza el comportamiento de Streamlit Cloud"""
    
    def __init__(self):
        # Force cloud environment detection
        os.environ['STREAMLIT_CLOUD_EMULATOR'] = 'true'
        self._config = self._get_cloud_optimized_config()
    
    def _get_cloud_optimized_config(self) -> Dict[str, Any]:
        """Configuración optimizada específicamente para Streamlit Cloud"""
        return {
            # API Configuration (conservative for 1GB limit)
            'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY', ''),
            'OPENAI_MODEL': 'gpt-4o-mini',  # Most efficient model
            'OPENAI_MAX_TOKENS': 4000,      # Reduced for memory
            'OPENAI_TEMPERATURE': 0.0,
            
            # STRICT Cloud Limits (more conservative than real cloud)
            'MAX_COMMENTS_PER_BATCH': 8,    # Very conservative
            'MAX_FILE_SIZE_MB': 2,          # Smaller files only
            'CACHE_TTL_SECONDS': 1200,      # 20 minutes
            
            # Performance Settings (cloud-optimized)
            'API_RATE_LIMIT_PER_MINUTE': 20,
            'SESSION_TIMEOUT_MINUTES': 10,
            'ENABLE_PROGRESS_TRACKING': True,
            'BATCH_PROCESSING_DELAY': 3.0,  # Slower processing
            
            # Aggressive Memory Management
            'ENABLE_MEMORY_OPTIMIZATION': True,
            'CLEAR_CACHE_INTERVAL': 600,    # 10 minutes
            'MAX_CACHED_ITEMS': 25,         # Very small cache
            'FORCE_GARBAGE_COLLECTION': True,
            'MEMORY_CHECK_INTERVAL': 30,    # Check every 30 seconds
            
            # Cloud Environment Settings
            'APP_ENV': 'streamlit_cloud_emulation',
            'DEBUG_MODE': False,
            'LOG_LEVEL': 'WARNING',
            'ENABLE_DETAILED_LOGGING': False,
            
            # UI Optimizations for limited resources
            'SHOW_PROGRESS_BAR': True,
            'SHOW_RESOURCE_WARNINGS': True,
            'ENABLE_BATCH_SIZE_AUTO_ADJUSTMENT': True,
            
            # Safety Limits
            'MAX_CONCURRENT_USERS': 3,      # Limit concurrent processing
            'AUTO_RESTART_ON_HIGH_MEMORY': True,
            'MEMORY_WARNING_THRESHOLD': 0.8, # 80% of 1GB
            'MEMORY_CRITICAL_THRESHOLD': 0.9, # 90% of 1GB
        }
    
    def get(self, key: str, default=None):
        """Get configuration value"""
        return self._config.get(key, default)
    
    def is_memory_critical(self) -> bool:
        """Check if memory usage is critical"""
        try:
            import psutil
            memory_percent = psutil.virtual_memory().percent / 100
            return memory_percent > self.get('MEMORY_CRITICAL_THRESHOLD', 0.9)
        except:
            return False
    
    def should_show_memory_warning(self) -> bool:
        """Check if should show memory warning"""
        try:
            import psutil
            memory_percent = psutil.virtual_memory().percent / 100
            return memory_percent > self.get('MEMORY_WARNING_THRESHOLD', 0.8)
        except:
            return False
    
    def get_environment_info(self) -> Dict[str, str]:
        """Get environment information"""
        return {
            'environment': '🌩️ Streamlit Cloud Emulator',
            'max_batch_size': str(self.get('MAX_COMMENTS_PER_BATCH')),
            'memory_limit': '1GB (Docker enforced)',
            'cpu_limit': '1 CPU (Docker enforced)',
            'cache_ttl': f"{self.get('CACHE_TTL_SECONDS')}s",
            'memory_optimization': 'ENABLED (Aggressive)',
            'auto_restart': str(self.get('AUTO_RESTART_ON_HIGH_MEMORY')),
        }
    
    def apply_streamlit_cloud_limits(self):
        """Apply Streamlit Cloud specific limits to Streamlit"""
        # Configure Streamlit for cloud limits
        if hasattr(st, 'set_page_config'):
            try:
                st.set_page_config(
                    page_title="Comment Analyzer (Cloud Emulator)",
                    layout="centered",  # Use centered layout to save memory
                    initial_sidebar_state="collapsed"  # Start with sidebar collapsed
                )
            except:
                pass  # Ignore if already configured
        
        # Set resource warnings
        if self.should_show_memory_warning():
            st.warning("⚠️ Uso de memoria alto - Comportamiento similar a Streamlit Cloud")
        
        if self.is_memory_critical():
            st.error("🚨 MEMORIA CRÍTICA - La app se reiniciaría en Streamlit Cloud")

# Global cloud configuration instance
cloud_config = StreamlitCloudConfig()

# Export functions for compatibility
def get_cloud_config(key: str, default=None):
    """Get cloud-optimized configuration value"""
    return cloud_config.get(key, default)

def is_cloud_emulator() -> bool:
    """Check if running in cloud emulator mode"""
    return os.getenv('STREAMLIT_CLOUD_EMULATOR') == 'true'

def get_cloud_environment_info() -> Dict[str, str]:
    """Get cloud emulator environment information"""
    return cloud_config.get_environment_info()

def apply_cloud_limits():
    """Apply cloud limits to current session"""
    return cloud_config.apply_streamlit_cloud_limits()