"""
Constants for AI Engine to eliminate magic numbers
POLISH-002 FIX: Centralized configuration constants for maintainability
"""

class AIEngineConstants:
    """
    Centralized constants for AI Engine configuration
    Eliminates magic numbers and provides single source of truth for configuration
    """
    
    # Token Calculation Constants - OPTIMIZED per FASE 1-5
    BASE_TOKENS_JSON_STRUCTURE = 1200      # Base tokens for JSON response structure
    TOKENS_PER_COMMENT = 50                # OPTIMIZED: Reduced tokens per comment for faster processing
    TOKEN_BUFFER_PERCENTAGE = 1.10         # 10% buffer for variability
    SAFETY_COMMENT_LIMIT = 100             # OPTIMIZED: Increased for 1000-comment files (batch size 100)
    
    # Cache Management Constants  
    DEFAULT_CACHE_SIZE = 50                # Maximum cache entries
    DEFAULT_CACHE_TTL = 3600               # Cache TTL in seconds (1 hour)
    CACHE_CLEANUP_THRESHOLD_RATIO = 1.5    # Cleanup when timestamps > cache * ratio
    
    # AI Determinism Constants
    FIXED_SEED = 12345                     # Fixed seed for reproducible results
    DEFAULT_TEMPERATURE = 0.0              # Temperature for deterministic outputs
    
    # Model Token Limits  
    MODEL_TOKEN_LIMITS = {
        'gpt-4o-mini': 16384,              # GPT-4o mini context limit
        'gpt-4o': 16384,                   # GPT-4o context limit  
        'gpt-4': 128000,                   # GPT-4 Turbo context limit
        'gpt-4-turbo': 128000,             # GPT-4 Turbo context limit
        'gpt-3.5-turbo': 16385             # GPT-3.5 Turbo context limit
    }
    
    # Default Model Configuration
    DEFAULT_MODEL = "gpt-4o-mini"
    FALLBACK_TOKEN_LIMIT = 16384           # Conservative fallback for unknown models
    
    # Processing Constants - OPTIMIZED per configuration updates
    MAX_FILE_SIZE_MB = 5                   # Maximum upload file size
    MAX_COMMENT_LENGTH = 500               # Maximum comment length for processing
    MIN_CONFIDENCE_THRESHOLD = 0.45        # OPTIMIZED: Reduced from 0.5 for better success rate
    
    # Excel Export Constants
    EXCEL_MAX_EMOTIONS_DISPLAY = 16       # Maximum emotions to show in Excel
    EXCEL_MAX_THEMES_DISPLAY = 8          # Maximum themes to show in Excel
    EXCEL_MAX_COMMENTS_DETAIL = 50        # Maximum comments to detail in Excel
    
    # Chart Configuration Constants
    CHART_DEFAULT_HEIGHT = 400             # Default chart height in pixels
    CHART_DYNAMIC_HEIGHT_PER_ITEM = 25     # Height increment per item in dynamic charts
    CHART_MIN_HEIGHT = 300                 # Minimum chart height
    CHART_MAX_HEIGHT = 800                 # Maximum chart height
    
    # Emotion Classification Thresholds
    EMOTION_VERY_INTENSE_THRESHOLD = 0.8   # Threshold for "Muy Intensa"
    EMOTION_INTENSE_THRESHOLD = 0.6        # Threshold for "Intensa"  
    EMOTION_MODERATE_THRESHOLD = 0.4       # Threshold for "Moderada"
    EMOTION_MILD_THRESHOLD = 0.2           # Threshold for "Leve"
    
    # Color Palette Constants
    EMOTION_COLORS = {
        # Positive emotions - Green/Blue spectrum
        'satisfaccion': '#10B981',         # Emerald
        'alegria': '#06D6A0',              # Bright green  
        'entusiasmo': '#FFD23F',           # Bright yellow
        'gratitud': '#118AB2',             # Blue
        'confianza': '#073B4C',            # Dark blue
        
        # Negative emotions - Red/Orange spectrum  
        'frustracion': '#EF4444',          # Red
        'enojo': '#DC2626',                # Dark red
        'decepcion': '#991B1B',            # Very dark red
        'preocupacion': '#F97316',         # Orange
        'irritacion': '#EA580C',           # Dark orange
        'ansiedad': '#C2410C',             # Very dark orange
        'tristeza': '#7C2D12',             # Brown-red
        
        # Neutral/Mixed emotions - Purple/Gray spectrum
        'confusion': '#6B7280',            # Gray  
        'esperanza': '#8B5CF6',            # Purple
        'curiosidad': '#A855F7',           # Light purple
        'impaciencia': '#9333EA',          # Medium purple
        'neutral': '#9CA3AF'               # Light gray
    }
    
    # Default colors for fallback
    DEFAULT_EMOTION_COLOR = '#8B5CF6'      # Purple fallback
    DEFAULT_THEME_COLOR = '#06B6D4'        # Cyan fallback
    
    @classmethod
    def get_model_token_limit(cls, model: str) -> int:
        """Get token limit for specific model with fallback"""
        return cls.MODEL_TOKEN_LIMITS.get(model, cls.FALLBACK_TOKEN_LIMIT)
    
    @classmethod
    def get_emotion_color(cls, emotion: str) -> str:
        """Get color for specific emotion with fallback"""
        return cls.EMOTION_COLORS.get(emotion, cls.DEFAULT_EMOTION_COLOR)
    
    @classmethod
    def classify_emotion_intensity(cls, intensity: float) -> str:
        """Classify emotion intensity based on thresholds"""
        if intensity >= cls.EMOTION_VERY_INTENSE_THRESHOLD:
            return "Muy Intensa"
        elif intensity >= cls.EMOTION_INTENSE_THRESHOLD:
            return "Intensa"
        elif intensity >= cls.EMOTION_MODERATE_THRESHOLD:
            return "Moderada"
        elif intensity >= cls.EMOTION_MILD_THRESHOLD:
            return "Leve"
        else:
            return "Muy Leve"
    
    @classmethod
    def calculate_dynamic_chart_height(cls, item_count: int) -> int:
        """Calculate dynamic chart height based on item count"""
        calculated_height = cls.CHART_DEFAULT_HEIGHT + (item_count * cls.CHART_DYNAMIC_HEIGHT_PER_ITEM)
        return max(cls.CHART_MIN_HEIGHT, min(calculated_height, cls.CHART_MAX_HEIGHT))
    
    @classmethod
    def validate_configuration(cls) -> bool:
        """Validate that all constants are properly configured"""
        try:
            # Validate token constants
            assert cls.BASE_TOKENS_JSON_STRUCTURE > 0
            assert cls.TOKENS_PER_COMMENT > 0
            assert 1.0 <= cls.TOKEN_BUFFER_PERCENTAGE <= 2.0
            
            # Validate cache constants
            assert cls.DEFAULT_CACHE_SIZE > 0
            assert cls.DEFAULT_CACHE_TTL > 0
            
            # Validate thresholds are in correct ranges
            assert 0.0 <= cls.EMOTION_MILD_THRESHOLD <= 1.0
            assert cls.EMOTION_MILD_THRESHOLD <= cls.EMOTION_MODERATE_THRESHOLD
            assert cls.EMOTION_MODERATE_THRESHOLD <= cls.EMOTION_INTENSE_THRESHOLD
            assert cls.EMOTION_INTENSE_THRESHOLD <= cls.EMOTION_VERY_INTENSE_THRESHOLD
            
            # Validate model limits
            assert all(limit > 0 for limit in cls.MODEL_TOKEN_LIMITS.values())
            
            return True
            
        except AssertionError as e:
            raise ValueError(f"Invalid AI Engine constants configuration: {e}")
        except Exception as e:
            raise ValueError(f"Error validating AI Engine constants: {e}")