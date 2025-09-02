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
    
    def analyze_comment_quality(self, comment: str) -> Dict[str, Any]:
        """Analyze comment quality metrics (replaces fixed values)"""
        if not comment or not comment.strip():
            return {
                'quality_score': 0.0,
                'completeness': 'incomplete', 
                'clarity': 0.0,
                'constructiveness': 0.0
            }
        
        comment_lower = comment.lower()
        word_count = len(comment.split())
        
        # Dynamic quality calculation based on content
        has_specifics = any(keyword in comment_lower for keyword in 
                           ['problema', 'error', 'falla', 'bien', 'mal', 'servicio', 'velocidad'])
        has_details = any(word in comment_lower for word in
                         ['porque', 'cuando', 'donde', 'como', 'siempre', 'nunca'])
        
        quality_score = min(1.0, word_count / 20.0)
        if has_specifics:
            quality_score += 0.2
        if has_details:
            quality_score += 0.1
        
        return {
            'quality_score': min(1.0, quality_score),
            'completeness': 'complete' if word_count > 10 else ('partial' if word_count > 3 else 'incomplete'),
            'clarity': 1.0 if has_specifics else (0.7 if has_details else 0.3),
            'constructiveness': 0.9 if has_specifics and has_details else (0.6 if has_specifics else 0.3)
        }
    
    def detect_themes_improved(self, comment: str) -> List[str]:
        """Enhanced theme detection (replaces fixed 'sin_clasificar')"""
        if not comment or not comment.strip():
            return []
        
        # Use existing theme detection but expand it
        themes = self._extract_themes(comment)
        comment_lower = comment.lower()
        
        # Add specific telecom themes  
        if any(word in comment_lower for word in ['fibra', 'internet', 'wifi', 'conexion']):
            themes.append('conectividad')
        if any(word in comment_lower for word in ['instalacion', 'tecnico', 'visita']):
            themes.append('instalacion')
        if any(word in comment_lower for word in ['factura', 'cobro', 'pago', 'plan']):
            themes.append('facturacion')
        if any(word in comment_lower for word in ['atencion', 'soporte', 'ayuda', 'call']):
            themes.append('atencion_cliente')
        
        # Return at least one theme, never empty
        return themes if themes else ['comentario_general']
    
    def analyze_service_issues(self, comment: str) -> List[Dict[str, Any]]:
        """Detect service-related issues (dynamic detection)"""
        if not comment or not comment.strip():
            return []
        
        issues = []
        comment_lower = comment.lower()
        
        # Performance issues
        if any(word in comment_lower for word in ['lento', 'demora', 'espera', 'carga']):
            severity = 'high' if 'muy lento' in comment_lower else 'medium'
            issues.append({'issue': 'performance', 'severity': severity})
        
        # Connection issues  
        if any(word in comment_lower for word in ['se corta', 'desconecta', 'inestable', 'intermitente']):
            issues.append({'issue': 'connectivity', 'severity': 'high'})
        
        # Support issues
        if any(word in comment_lower for word in ['atencion', 'soporte', 'servicio malo', 'no responden']):
            issues.append({'issue': 'customer_support', 'severity': 'medium'})
        
        # Billing issues
        if any(word in comment_lower for word in ['factura', 'cobro', 'precio', 'caro']):
            issues.append({'issue': 'billing', 'severity': 'low'})
        
        return issues
    
    def enhanced_sentiment_analysis(self, comment: str, nota: int = None) -> Dict[str, Any]:
        """Enhanced sentiment analysis with rating correlation (dynamic confidence)"""
        if not comment or not comment.strip():
            return {
                'sentiment': 'neutral',
                'intensity': 0.0,
                'emotional_indicators': [],
                'sentiment_confidence': 0.0
            }
        
        # Use existing sentiment analysis
        basic_sentiment = self._analyze_sentiment_with_context(comment)
        
        # Calculate dynamic intensity based on content
        comment_lower = comment.lower()
        intensity_words = {
            'high': ['excelente', 'pésimo', 'horrible', 'increíble', 'fantástico', 'terrible'],
            'medium': ['bueno', 'malo', 'regular', 'normal'],
            'low': ['ok', 'bien', 'más o menos']
        }
        
        intensity = 0.5  # default
        if any(word in comment_lower for word in intensity_words['high']):
            intensity = 0.8
        elif any(word in comment_lower for word in intensity_words['medium']):
            intensity = 0.6
        elif any(word in comment_lower for word in intensity_words['low']):
            intensity = 0.4
        
        # Correlate with rating if available
        if nota is not None:
            if nota <= 3:
                sentiment = 'negativo'
                intensity = max(intensity, (4 - nota) / 3.0)
            elif nota >= 8:
                sentiment = 'positivo'
                intensity = max(intensity, (nota - 7) / 3.0)
            else:
                sentiment = basic_sentiment
                
        else:
            sentiment = basic_sentiment
        
        # Extract emotional indicators dynamically
        emotional_indicators = []
        if 'excelente' in comment_lower or 'fantástico' in comment_lower:
            emotional_indicators.append('satisfacción')
        if 'problema' in comment_lower or 'malo' in comment_lower:
            emotional_indicators.append('frustración')
        if 'rápido' in comment_lower:
            emotional_indicators.append('eficiencia')
        if 'lento' in comment_lower:
            emotional_indicators.append('impaciencia')
        
        return {
            'sentiment': sentiment,
            'intensity': min(1.0, intensity),
            'emotional_indicators': emotional_indicators if emotional_indicators else ['neutral'],
            'sentiment_confidence': min(1.0, intensity + 0.2)
        }