"""
Enhanced Analysis Module - Fallback implementation
Provides enhanced sentiment analysis when OpenAI is not available
"""

import pandas as pd
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class EnhancedAnalysis:
    """
    Enhanced rule-based analysis as fallback for AI analysis.
    This is a stub implementation to prevent import errors.
    """
    
    def __init__(self):
        """Initialize enhanced analysis with extended rules"""
        self.name = "EnhancedAnalysis"
        logger.info("Enhanced Analysis initialized (fallback mode)")
        
    def analyze(self, comments: List[str]) -> List[Dict[str, Any]]:
        """
        Perform enhanced rule-based sentiment analysis
        
        Args:
            comments: List of comment strings
            
        Returns:
            List of analysis results
        """
        results = []
        for comment in comments:
            # Basic fallback implementation
            sentiment = self._analyze_sentiment(comment)
            results.append({
                'text': comment,
                'sentiment': sentiment,
                'confidence': 0.7,
                'method': 'enhanced_rules'
            })
        return results
    
    def full_analysis(self, comment: str) -> Dict[str, Any]:
        """
        Perform full analysis on a single comment for compatibility with AI adapter
        
        Args:
            comment: Single comment string
            
        Returns:
            Dictionary with analysis results
        """
        if not comment:
            return {
                'text': comment,
                'sentiment': 'neutral',
                'confidence': 0.5,
                'method': 'enhanced_rules',
                'language': 'es',
                'themes': [],
                'pain_points': [],
                'emotions': ['neutral']
            }
        
        sentiment = self._analyze_sentiment(comment)
        
        # Convert sentiment format to match expected format
        if sentiment == 'positivo':
            mapped_sentiment = 'positive'
            emotions = ['satisfacción']
        elif sentiment == 'negativo':
            mapped_sentiment = 'negative'
            emotions = ['frustración']
        else:
            mapped_sentiment = 'neutral'
            emotions = ['neutral']
        
        # Basic theme extraction
        themes = self._extract_themes(comment)
        pain_points = self._extract_pain_points(comment)
        
        return {
            'text': comment,
            'sentiment': mapped_sentiment,
            'confidence': 0.7,
            'method': 'enhanced_rules',
            'language': 'es',
            'themes': themes,
            'pain_points': pain_points,
            'emotions': emotions,
            'translation': comment  # For Spanish comments, translation is the same
        }
    
    def _extract_themes(self, text: str) -> List[str]:
        """Extract basic themes from text"""
        if not text:
            return []
        
        text_lower = text.lower()
        themes = []
        
        # Service quality themes
        if any(word in text_lower for word in ['servicio', 'atención', 'calidad']):
            themes.append('calidad_servicio')
        
        # Speed themes
        if any(word in text_lower for word in ['velocidad', 'rápido', 'lento', 'conexión']):
            themes.append('velocidad')
        
        # Price themes
        if any(word in text_lower for word in ['precio', 'caro', 'barato', 'costo']):
            themes.append('precio')
        
        # Technical themes
        if any(word in text_lower for word in ['técnico', 'instalación', 'equipo', 'fibra']):
            themes.append('soporte_tecnico')
        
        return themes[:3]  # Limit to 3 themes
    
    def _extract_pain_points(self, text: str) -> List[str]:
        """Extract pain points from text"""
        if not text:
            return []
        
        text_lower = text.lower()
        pain_points = []
        
        # Connection issues
        if any(word in text_lower for word in ['se corta', 'desconecta', 'inestable']):
            pain_points.append('conexión_inestable')
        
        # Speed issues
        if any(word in text_lower for word in ['lento', 'lentitud', 'carga lento']):
            pain_points.append('velocidad_baja')
        
        # Service issues
        if any(word in text_lower for word in ['no funciona', 'falla', 'problema']):
            pain_points.append('fallas_servicio')
        
        # Support issues
        if any(word in text_lower for word in ['soporte', 'atención', 'demora']):
            pain_points.append('soporte_deficiente')
        
        return pain_points
    
    def _analyze_sentiment(self, text: str) -> str:
        """Basic sentiment analysis using extended rules"""
        if not text:
            return 'neutral'
        
        text_lower = text.lower()
        
        # Extended positive indicators
        positive_indicators = [
            'excelente', 'bueno', 'buena', 'genial', 'fantástico',
            'increíble', 'perfecto', 'mejor', 'rápido', 'eficiente',
            'satisfecho', 'contento', 'feliz', 'recomiendo'
        ]
        
        # Extended negative indicators
        negative_indicators = [
            'malo', 'mala', 'pésimo', 'terrible', 'horrible',
            'lento', 'problema', 'error', 'falla', 'no funciona',
            'caro', 'costoso', 'deficiente', 'insatisfecho'
        ]
        
        pos_score = sum(1 for word in positive_indicators if word in text_lower)
        neg_score = sum(1 for word in negative_indicators if word in text_lower)
        
        if pos_score > neg_score:
            return 'positivo'
        elif neg_score > pos_score:
            return 'negativo'
        else:
            return 'neutral'