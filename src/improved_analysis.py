"""
Improved Analysis Module - Advanced fallback implementation
Provides improved sentiment analysis with additional features
"""

import pandas as pd
from typing import List, Dict, Any
import logging
import re

logger = logging.getLogger(__name__)

class ImprovedAnalysis:
    """
    Improved analysis with pattern matching and context awareness.
    This is a stub implementation to prevent import errors.
    """
    
    def __init__(self):
        """Initialize improved analysis with pattern matching"""
        self.name = "ImprovedAnalysis"
        logger.info("Improved Analysis initialized (fallback mode)")
        
    def analyze(self, comments: List[str]) -> List[Dict[str, Any]]:
        """
        Perform improved sentiment analysis with context
        
        Args:
            comments: List of comment strings
            
        Returns:
            List of analysis results with themes
        """
        results = []
        for comment in comments:
            sentiment = self._analyze_sentiment_with_context(comment)
            themes = self._extract_themes(comment)
            results.append({
                'text': comment,
                'sentiment': sentiment,
                'confidence': 0.75,
                'themes': themes,
                'method': 'improved_rules'
            })
        return results
    
    def _analyze_sentiment_with_context(self, text: str) -> str:
        """Sentiment analysis with context and negation handling"""
        if not text:
            return 'neutral'
        
        text_lower = text.lower()
        
        # Check for negations
        negations = ['no', 'nunca', 'jamás', 'tampoco', 'ni']
        has_negation = any(neg in text_lower for neg in negations)
        
        # Positive patterns
        positive_patterns = [
            r'\bmuy\s+bu[e]?n[o]?[a]?\b',
            r'\bexcelente\b',
            r'\bme\s+gusta\b',
            r'\bsatisfech[o]?[a]?\b'
        ]
        
        # Negative patterns  
        negative_patterns = [
            r'\bmuy\s+mal[o]?[a]?\b',
            r'\bp[é]?sim[o]?[a]?\b',
            r'\bno\s+funciona\b',
            r'\bproblemas?\b'
        ]
        
        pos_matches = sum(1 for pattern in positive_patterns if re.search(pattern, text_lower))
        neg_matches = sum(1 for pattern in negative_patterns if re.search(pattern, text_lower))
        
        # Apply negation logic
        if has_negation:
            pos_matches, neg_matches = neg_matches, pos_matches
        
        if pos_matches > neg_matches:
            return 'positivo'
        elif neg_matches > pos_matches:
            return 'negativo'
        else:
            return 'neutral'
    
    def _extract_themes(self, text: str) -> List[str]:
        """Extract basic themes from text"""
        if not text:
            return []
        
        text_lower = text.lower()
        themes = []
        
        theme_patterns = {
            'velocidad': ['lento', 'rápido', 'velocidad', 'demora'],
            'servicio': ['atención', 'servicio', 'soporte'],
            'precio': ['caro', 'precio', 'costoso', 'barato'],
            'calidad': ['calidad', 'bueno', 'malo', 'excelente']
        }
        
        for theme, keywords in theme_patterns.items():
            if any(keyword in text_lower for keyword in keywords):
                themes.append(theme)
        
        return themes
    
    def calculate_real_nps(self, df_nps: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculate NPS from DataFrame with NPS column
        Compatible with AI adapter expectations
        
        Args:
            df_nps: DataFrame with 'NPS' column (scores 0-10)
            
        Returns:
            Dictionary with NPS analysis
        """
        if df_nps is None or df_nps.empty or 'NPS' not in df_nps.columns:
            return {
                'nps_score': 0,
                'promoters': 0,
                'detractors': 0,
                'passives': 0,
                'total_responses': 0
            }
        
        nps_scores = df_nps['NPS'].dropna()
        if len(nps_scores) == 0:
            return {
                'nps_score': 0,
                'promoters': 0,
                'detractors': 0,
                'passives': 0,
                'total_responses': 0
            }
        
        # Standard NPS calculation
        promoters = sum(1 for score in nps_scores if score >= 9)
        detractors = sum(1 for score in nps_scores if score <= 6)
        passives = sum(1 for score in nps_scores if 7 <= score <= 8)
        total = len(nps_scores)
        
        nps_score = ((promoters - detractors) / total) * 100 if total > 0 else 0
        
        return {
            'nps_score': round(nps_score, 1),
            'promoters': promoters,
            'detractors': detractors,
            'passives': passives,
            'total_responses': total
        }