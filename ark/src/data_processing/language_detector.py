"""
Language Detection Module
Provides lightweight language detection for pre-filtering comments
"""

import re
from typing import Dict, List, Tuple, Any
import logging

# Try to import langdetect, but provide fallback if not available
try:
    from langdetect import detect, DetectorFactory
    # Make langdetect deterministic
    DetectorFactory.seed = 0
    LANGDETECT_AVAILABLE = True
except ImportError:
    LANGDETECT_AVAILABLE = False

logger = logging.getLogger(__name__)

# Define Guarani-specific words and patterns
GUARANI_COMMON_WORDS = [
    'ñande', 'ore', 'che', 'nde', 'ha', 'hína', 'ko', 'la', 'mba\'e', 'oĩ', 'umi', 'avei',
    'porã', 'vai', 'heta', 'ningo', 'voi', 'upéi', 'upéicha', 'iporã', 'ndaipori',
    'vy\'a', 'avy\'a', 'rehe', 'ndaje', 'araka\'e', 'péicha', 'oĩmba'
]

# Define patterns for special Guarani characters
GUARANI_CHAR_PATTERN = r'[ãẽĩõũỹñ\'ĝǰỹŷ]'

class LanguageDetector:
    """
    Lightweight language detector with special handling for 
    Spanish, Guarani, and mixed language texts (Jopara)
    """
    
    def __init__(self):
        """Initialize the language detector"""
        self.guarani_pattern = re.compile('|'.join(
            r'\b' + re.escape(word) + r'\b' 
            for word in GUARANI_COMMON_WORDS
        ), re.IGNORECASE)
        
        self.guarani_char_regex = re.compile(GUARANI_CHAR_PATTERN)
        
    def detect_language(self, text: str) -> Dict[str, Any]:
        """
        Detect the language of the given text
        
        Args:
            text: The text to analyze
            
        Returns:
            Dictionary with language code and confidence level
        """
        if not text or len(text.strip()) < 3:
            return {
                "language": "es",  # Default to Spanish for very short texts
                "confidence": 0.5,
                "details": "Text too short for reliable detection"
            }
        
        # Check for Guarani indicators
        guarani_word_matches = len(re.findall(self.guarani_pattern, text))
        guarani_char_matches = len(re.findall(self.guarani_char_regex, text))
        
        # Calculate word count for reference
        word_count = len(text.split())
        
        # If significant Guarani markers are found
        guarani_word_ratio = guarani_word_matches / max(1, word_count)
        guarani_indicator = guarani_word_matches > 1 or guarani_char_matches > 2 or guarani_word_ratio > 0.2
        
        # Try to use langdetect for Spanish detection if available
        detected_lang = None
        langdetect_confidence = 0.0
        
        if LANGDETECT_AVAILABLE:
            try:
                # Detect primary language
                detected_lang = detect(text)
                langdetect_confidence = 0.7  # Arbitrary base confidence for langdetect
            except Exception as e:
                logger.warning(f"Language detection failed: {e}")
        
        # Decision logic
        if guarani_indicator:
            # Check if it's mixed (Jopara) or pure Guarani
            if detected_lang == 'es' and guarani_word_ratio < 0.5:
                return {
                    "language": "mixed",
                    "confidence": min(0.6 + (guarani_word_ratio * 0.4), 0.95),
                    "details": f"Detected Spanish with Guarani elements ({guarani_word_matches} Guarani words)"
                }
            else:
                return {
                    "language": "gn",
                    "confidence": min(0.7 + (guarani_word_ratio * 0.3), 0.95),
                    "details": f"Detected primary Guarani ({guarani_word_matches} words matched)"
                }
        elif detected_lang == 'es' or (not LANGDETECT_AVAILABLE and not guarani_indicator):
            # Spanish detected or fallback if langdetect not available
            return {
                "language": "es",
                "confidence": langdetect_confidence if LANGDETECT_AVAILABLE else 0.6,
                "details": "Spanish detected" if LANGDETECT_AVAILABLE else "Defaulted to Spanish (no Guarani markers)"
            }
        else:
            # Some other language or uncertain
            return {
                "language": "es",  # Default to Spanish for other cases
                "confidence": 0.5,
                "details": f"Uncertain language (detected: {detected_lang})"
            }

def get_comment_language(comment: str) -> str:
    """
    Simple utility function to get just the language code for a comment
    
    Args:
        comment: Text to analyze
        
    Returns:
        Language code ('es', 'gn', or 'mixed')
    """
    detector = LanguageDetector()
    result = detector.detect_language(comment)
    return result["language"] 