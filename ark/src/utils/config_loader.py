"""
Configuration Loader Module
FIX #006, #007, #008: Centralized configuration management
Loads configuration from YAML file with fallback to defaults
"""

import yaml
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

class ConfigLoader:
    """Singleton configuration loader for the Comment Analyzer system"""
    
    _instance = None
    _config = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigLoader, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self):
        """Load configuration from YAML file"""
        try:
            # Try multiple possible config locations
            config_paths = [
                Path(__file__).parent.parent / 'analysis_config.yaml',
                Path('src/analysis_config.yaml'),
                Path('analysis_config.yaml'),
                Path(__file__).parent.parent.parent / 'config' / 'analysis_config.yaml'
            ]
            
            config_loaded = False
            for config_path in config_paths:
                if config_path.exists():
                    with open(config_path, 'r', encoding='utf-8') as f:
                        self._config = yaml.safe_load(f)
                    logger.info(f"Configuration loaded from {config_path}")
                    config_loaded = True
                    break
            
            if not config_loaded:
                logger.warning("No configuration file found, using defaults")
                self._config = self._get_default_config()
                
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            self._config = self._get_default_config()
    
    def _get_default_config(self) -> Dict:
        """Return default configuration if file not found"""
        return {
            'columns': {
                'comment': ['comentario final', 'comentario', 'comment', 'comentarios', 
                           'comments', 'feedback', 'texto', 'opinion'],
                'rating': ['nota', 'score', 'puntuacion', 'rating'],
                'nps': ['nps', 'net_promoter_score']
            },
            'competitors': {
                'primary': ['tigo', 'claro', 'copaco', 'vox', 'telecel']
            },
            'emotions': {
                'intensities': {
                    'frustración': 2.0, 'enojo': 2.5, 'satisfacción': 1.8,
                    'preocupación': 1.2, 'neutral': 1.0
                },
                'translations': {
                    'frustration': 'frustración',
                    'anger': 'enojo',
                    'satisfaction': 'satisfacción'
                }
            },
            'urgency': {
                'thresholds': {'P0': 6, 'P1': 4, 'P2': 2, 'P3': 0}
            },
            'api': {
                'models': {'primary': 'gpt-4o-mini'},
                'confidence_thresholds': {'high': 0.8, 'medium': 0.6, 'low': 0.4}
            }
        }
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation
        Example: config.get('emotions.intensities.frustración')
        """
        keys = key_path.split('.')
        value = self._config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def get_comment_columns(self) -> List[str]:
        """Get list of possible comment column names"""
        return self.get('columns.comment', ['comentario', 'comment'])
    
    def get_rating_columns(self) -> List[str]:
        """Get list of possible rating column names"""
        return self.get('columns.rating', ['nota', 'score', 'rating'])
    
    def get_nps_columns(self) -> List[str]:
        """Get list of possible NPS column names"""
        return self.get('columns.nps', ['nps'])
    
    def get_competitors(self) -> List[str]:
        """Get list of competitor names"""
        primary = self.get('competitors.primary', [])
        variations = self.get('competitors.variations', {})
        
        # Combine primary and all variations
        all_competitors = set(primary)
        for comp_variations in variations.values():
            all_competitors.update(comp_variations)
        
        return list(all_competitors)
    
    def get_emotion_intensities(self) -> Dict[str, float]:
        """Get emotion intensity mapping"""
        return self.get('emotions.intensities', {})
    
    def get_emotion_translations(self) -> Dict[str, str]:
        """Get emotion translation mapping"""
        return self.get('emotions.translations', {})
    
    def get_urgency_thresholds(self) -> Dict[str, int]:
        """Get urgency level thresholds"""
        return self.get('urgency.thresholds', {'P0': 6, 'P1': 4, 'P2': 2, 'P3': 0})
    
    def get_urgency_keywords(self, level: str) -> List[str]:
        """Get keywords for specific urgency level"""
        return self.get(f'urgency.keywords.{level}', [])
    
    def get_theme_keywords(self, theme: str) -> List[str]:
        """Get keywords for specific theme"""
        return self.get(f'themes.{theme}.keywords', [])
    
    def get_api_model(self, fallback_index: int = 0) -> str:
        """Get API model name with fallback support"""
        primary = self.get('api.models.primary', 'gpt-4o-mini')
        if fallback_index == 0:
            return primary
        
        fallbacks = self.get('api.models.fallback', [])
        if fallback_index <= len(fallbacks):
            return fallbacks[fallback_index - 1]
        
        return primary  # Return primary if no fallback available
    
    def get_confidence_threshold(self, level: str = 'medium') -> float:
        """Get confidence threshold for given level"""
        return self.get(f'api.confidence_thresholds.{level}', 0.5)
    
    def get_batch_size(self, size: str = 'medium') -> int:
        """Get batch size for API calls"""
        return self.get(f'api.batch_sizes.{size}', 25)
    
    def get_customer_segment_keywords(self, segment: str) -> List[str]:
        """Get keywords for customer segment detection"""
        return self.get(f'customer_segments.{segment}.keywords', [])
    
    def get_nps_ranges(self) -> Dict[str, Any]:
        """Get NPS score ranges"""
        return {
            'promoter_min': self.get('nps.promoter_min', 9),
            'passive_min': self.get('nps.passive_min', 7),
            'passive_max': self.get('nps.passive_max', 8),
            'detractor_max': self.get('nps.detractor_max', 6)
        }
    
    def get_quality_thresholds(self) -> Dict[str, Any]:
        """Get quality assessment thresholds"""
        return {
            'min_words': self.get('quality.comment_min_words', 3),
            'min_chars': self.get('quality.comment_min_chars', 10),
            'max_chars': self.get('quality.comment_max_chars', 5000),
            'high_quality': self.get('quality.high_quality_threshold', 6),
            'medium_quality': self.get('quality.medium_quality_threshold', 4)
        }
    
    def reload(self):
        """Reload configuration from file"""
        self._load_config()
        logger.info("Configuration reloaded")
    
    def update(self, key_path: str, value: Any):
        """Update configuration value at runtime (doesn't persist to file)"""
        keys = key_path.split('.')
        config = self._config
        
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        config[keys[-1]] = value
        logger.debug(f"Configuration updated: {key_path} = {value}")

# Singleton instance
config = ConfigLoader()

# Convenience functions for common access patterns
def get_comment_columns() -> List[str]:
    """Get comment column names from config"""
    return config.get_comment_columns()

def get_competitors() -> List[str]:
    """Get competitor list from config"""
    return config.get_competitors()

def get_emotion_intensities() -> Dict[str, float]:
    """Get emotion intensities from config"""
    return config.get_emotion_intensities()

def get_urgency_thresholds() -> Dict[str, int]:
    """Get urgency thresholds from config"""
    return config.get_urgency_thresholds()

def get_api_model() -> str:
    """Get primary API model from config"""
    return config.get_api_model()

def get_confidence_threshold(level: str = 'medium') -> float:
    """Get confidence threshold from config"""
    return config.get_confidence_threshold(level)