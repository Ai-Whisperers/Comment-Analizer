"""
Memory Monitoring Module for Multi-page Application
Provides memory usage tracking and optimization for Streamlit deployment
"""

import gc
import logging
import os
from typing import Dict, Tuple

logger = logging.getLogger(__name__)


def get_memory_usage() -> float:
    """
    Get current memory usage in MB
    
    Returns:
        float: Memory usage in MB, or 0 if unavailable
    """
    try:
        import psutil
        process = psutil.Process()
        memory_mb = process.memory_info().rss / 1024 / 1024
        return memory_mb
    except ImportError:
        logger.warning("psutil not available - memory monitoring disabled")
        return 0
    except Exception as e:
        logger.error(f"Error getting memory usage: {e}")
        return 0


def is_streamlit_cloud() -> bool:
    """
    Detect if running on Streamlit Cloud
    
    Returns:
        bool: True if on Streamlit Cloud environment
    """
    # Check for Streamlit Cloud environment indicators
    cloud_indicators = [
        'STREAMLIT_CLOUD',
        'STREAMLIT_SHARING', 
        'HOSTNAME' in os.environ and 'streamlit' in os.environ.get('HOSTNAME', '').lower()
    ]
    
    return any(cloud_indicators)


def get_memory_status() -> Dict[str, any]:
    """
    Get comprehensive memory status information
    
    Returns:
        dict: Memory status with usage, limits, and recommendations
    """
    memory_mb = get_memory_usage()
    cloud_environment = is_streamlit_cloud()
    
    # Set limits based on environment
    memory_limit = 690 if cloud_environment else 2048  # MB
    
    if memory_mb > 0:
        memory_pct = (memory_mb / memory_limit) * 100
        
        # Determine status level
        if memory_pct > 80:
            status = "Alto"
            color = "red"
            recommendation = "Limpiar memoria inmediatamente"
        elif memory_pct > 60:
            status = "Medio"
            color = "orange" 
            recommendation = "Considerar limpieza de memoria"
        else:
            status = "Normal"
            color = "green"
            recommendation = "Memoria en rango óptimo"
        
        return {
            'available': True,
            'usage_mb': memory_mb,
            'usage_pct': memory_pct,
            'limit_mb': memory_limit,
            'status': status,
            'color': color,
            'recommendation': recommendation,
            'environment': 'Streamlit Cloud' if cloud_environment else 'Local'
        }
    else:
        return {
            'available': False,
            'error': 'Datos de memoria no disponibles',
            'environment': 'Streamlit Cloud' if cloud_environment else 'Local'
        }


def optimize_memory() -> bool:
    """
    Perform memory optimization
    
    Returns:
        bool: True if optimization completed successfully
    """
    try:
        # Force garbage collection
        collected = gc.collect()
        
        # Clear any module caches if available
        if hasattr(gc, 'set_threshold'):
            gc.set_threshold(700, 10, 10)  # More aggressive GC
        
        logger.info(f"Memory optimization completed - collected {collected} objects")
        return True
        
    except Exception as e:
        logger.error(f"Memory optimization failed: {e}")
        return False


def format_memory_display(memory_status: Dict[str, any]) -> Tuple[str, str, str]:
    """
    Format memory status for display in UI
    
    Args:
        memory_status: Memory status dictionary from get_memory_status()
        
    Returns:
        tuple: (metric_label, metric_value, metric_delta)
    """
    if not memory_status['available']:
        return ("Memoria", "No disponible", "")
    
    status = memory_status['status']
    usage_mb = memory_status['usage_mb']
    usage_pct = memory_status['usage_pct']
    
    label = f"Memoria ({status})"
    value = f"{usage_mb:.0f}MB"
    delta = f"{usage_pct:.1f}% usado"
    
    return (label, value, delta)


# Global memory manager instance for shared use
_global_memory_manager = None

def get_global_memory_manager():
    """Get shared memory manager instance"""
    global _global_memory_manager
    if _global_memory_manager is None:
        try:
            from src.utils.memory_manager import MemoryManager
            _global_memory_manager = MemoryManager(max_memory_mb=690)  # Cloud-optimized
        except ImportError:
            logger.warning("MemoryManager not available - using basic monitoring")
            _global_memory_manager = None
    
    return _global_memory_manager