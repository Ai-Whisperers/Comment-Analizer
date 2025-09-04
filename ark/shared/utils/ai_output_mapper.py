"""
AI Output Mapper - Dynamic mapping between AI outputs and UI expectations
Handles translation and normalization of AI results to UI-compatible formats
"""

from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)


class AIOutputMapper:
    """
    Maps dynamic AI outputs to fixed UI component expectations
    Ensures compatibility between real AI analysis and existing UI components
    """
    
    def __init__(self):
        # Sentiment mapping: AI output → UI expected
        self.sentiment_mapping = {
            # English → Spanish
            'positive': 'positivo',
            'negative': 'negativo', 
            'neutral': 'neutral',
            'mixed': 'neutral',  # Fallback
            'complex': 'neutral',  # Fallback
            
            # Already Spanish (passthrough)
            'positivo': 'positivo',
            'negativo': 'negativo'
        }
        
        # Emotion mapping: AI output → Spanish UI expected
        self.emotion_mapping = {
            # English → Spanish
            'joy': 'alegría',
            'happiness': 'alegría',
            'satisfaction': 'satisfacción',
            'anger': 'enojo',
            'fury': 'enojo',
            'frustration': 'frustración',
            'sadness': 'tristeza',
            'disappointment': 'desilusión',
            'fear': 'miedo',
            'worry': 'preocupación',
            'anxiety': 'ansiedad',
            'surprise': 'sorpresa',
            'disgust': 'irritación',
            'trust': 'confianza',
            'confidence': 'confianza',
            'anticipation': 'esperanza',
            'hope': 'esperanza',
            'optimism': 'optimismo',
            'gratitude': 'agradecimiento',
            'calm': 'tranquilidad',
            'peace': 'tranquilidad',
            'pessimism': 'pesimismo',
            
            # Already Spanish (passthrough)
            'alegría': 'alegría',
            'satisfacción': 'satisfacción',
            'enojo': 'enojo',
            'frustración': 'frustración',
            'tristeza': 'tristeza',
            'miedo': 'miedo',
            'sorpresa': 'sorpresa',
            'confianza': 'confianza',
            'optimismo': 'optimismo',
            'agradecimiento': 'agradecimiento',
            'tranquilidad': 'tranquilidad',
            'preocupación': 'preocupación',
            'ansiedad': 'ansiedad',
            'desilusión': 'desilusión',
            'irritación': 'irritación',
            'esperanza': 'esperanza',
            'pesimismo': 'pesimismo'
        }
        
        # Intensity mapping: AI output → UI expected
        self.intensity_mapping = {
            'very_high': 'Alta',
            'high': 'Alta', 
            'medium': 'Media',
            'moderate': 'Media',
            'low': 'Baja',
            'very_low': 'Baja',
            
            # Numeric to text mapping (0-10 scale)
            10: 'Alta', 9: 'Alta', 8: 'Alta',
            7: 'Alta', 6: 'Media', 5: 'Media',
            4: 'Media', 3: 'Baja', 2: 'Baja',
            1: 'Baja', 0: 'Baja',
            
            # Spanish passthrough
            'Alta': 'Alta',
            'Media': 'Media', 
            'Baja': 'Baja'
        }
        
        # Satisfaction mapping: AI output → UI expected  
        self.satisfaction_mapping = {
            'excellent': 'Alto',
            'very_good': 'Alto',
            'good': 'Alto',
            'fair': 'Medio',
            'average': 'Medio',
            'poor': 'Bajo',
            'very_poor': 'Bajo',
            'terrible': 'Bajo',
            
            # Numeric to text (0-100 scale)
            # This will be handled by normalize_satisfaction_index
            
            # Spanish passthrough
            'Alto': 'Alto',
            'Medio': 'Medio',
            'Bajo': 'Bajo'
        }
    
    def normalize_sentiments(self, ai_sentiments: List[str]) -> List[str]:
        """
        Convert AI sentiment outputs to UI-expected format
        
        Args:
            ai_sentiments: List of sentiments from AI (can be English or varied)
            
        Returns:
            List of normalized sentiments: ['positivo', 'negativo', 'neutral']
        """
        normalized = []
        
        for sentiment in ai_sentiments:
            if isinstance(sentiment, str):
                sentiment_lower = sentiment.lower().strip()
                mapped = self.sentiment_mapping.get(sentiment_lower, 'neutral')
                normalized.append(mapped)
            else:
                # Handle non-string sentiments
                normalized.append('neutral')
        
        return normalized
    
    def normalize_emotions(self, ai_emotions: Dict[str, int]) -> Dict[str, int]:
        """
        Convert AI emotion outputs to UI-expected Spanish format
        
        Args:
            ai_emotions: Dict of emotions from AI (can be English or varied)
            
        Returns:
            Dict with Spanish emotion names expected by UI
        """
        normalized = {}
        
        for emotion, count in ai_emotions.items():
            if isinstance(emotion, str):
                emotion_lower = emotion.lower().strip()
                mapped_emotion = self.emotion_mapping.get(emotion_lower, emotion)
                normalized[mapped_emotion] = count
            else:
                # Handle non-string emotions
                normalized[str(emotion)] = count
        
        return normalized
    
    def normalize_intensity_level(self, ai_intensity: Any) -> str:
        """
        Convert AI intensity output to UI-expected format
        
        Args:
            ai_intensity: Intensity from AI (can be numeric, text, or varied)
            
        Returns:
            String: 'Alta', 'Media', or 'Baja'
        """
        if isinstance(ai_intensity, (int, float)):
            # Handle numeric intensity (0-10 scale)
            if ai_intensity >= 7:
                return 'Alta'
            elif ai_intensity >= 4:
                return 'Media'
            else:
                return 'Baja'
        
        elif isinstance(ai_intensity, str):
            intensity_lower = ai_intensity.lower().strip()
            return self.intensity_mapping.get(intensity_lower, 'Media')
        
        else:
            # Fallback for unknown types
            return 'Media'
    
    def normalize_satisfaction_index(self, ai_satisfaction: Any) -> tuple:
        """
        Convert AI satisfaction to UI-expected format
        
        Args:
            ai_satisfaction: Satisfaction from AI (can be numeric, text, or varied)
            
        Returns:
            Tuple: (numeric_value, text_level) e.g., (75, 'Alto')
        """
        if isinstance(ai_satisfaction, (int, float)):
            # Handle numeric satisfaction (0-100 scale)
            numeric_value = max(0, min(100, int(ai_satisfaction)))
            
            if numeric_value >= 70:
                text_level = 'Alto'
            elif numeric_value >= 40:
                text_level = 'Medio'
            else:
                text_level = 'Bajo'
                
            return numeric_value, text_level
        
        elif isinstance(ai_satisfaction, str):
            satisfaction_lower = ai_satisfaction.lower().strip()
            text_level = self.satisfaction_mapping.get(satisfaction_lower, 'Medio')
            
            # Convert text back to numeric for consistency
            numeric_mapping = {'Alto': 80, 'Medio': 60, 'Bajo': 30}
            numeric_value = numeric_mapping.get(text_level, 60)
            
            return numeric_value, text_level
        
        else:
            # Fallback for unknown types
            return 60, 'Medio'
    
    def normalize_quality_level(self, ai_quality: Any) -> str:
        """
        Convert AI quality assessment to UI-expected format
        
        Args:
            ai_quality: Quality from AI (can be varied text or numeric)
            
        Returns:
            String: 'high', 'medium', or 'basic'
        """
        if isinstance(ai_quality, str):
            quality_lower = ai_quality.lower().strip()
            
            # Map various AI quality outputs to UI expectations
            if quality_lower in ['exceptional', 'excellent', 'outstanding', 'superior']:
                return 'high'
            elif quality_lower in ['good', 'fine', 'adequate', 'satisfactory']:
                return 'medium' 
            elif quality_lower in ['poor', 'bad', 'inadequate', 'unsatisfactory']:
                return 'basic'
            else:
                # Direct mapping or fallback
                return quality_lower if quality_lower in ['high', 'medium', 'basic'] else 'medium'
        
        elif isinstance(ai_quality, (int, float)):
            # Handle numeric quality (0-100 scale)
            if ai_quality >= 80:
                return 'high'
            elif ai_quality >= 50:
                return 'medium'
            else:
                return 'basic'
        
        else:
            return 'medium'
    
    def normalize_ai_results(self, ai_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Complete normalization of AI results for UI compatibility
        
        Args:
            ai_results: Raw results from AI analysis
            
        Returns:
            Normalized results compatible with existing UI components
        """
        try:
            normalized = ai_results.copy()
            
            # Normalize sentiments
            if 'sentiments' in ai_results:
                normalized['sentiments'] = self.normalize_sentiments(ai_results['sentiments'])
            
            # Normalize emotion summary
            if 'emotion_summary' in ai_results and 'distribution' in ai_results['emotion_summary']:
                original_emotions = ai_results['emotion_summary']['distribution']
                normalized_emotions = self.normalize_emotions(original_emotions)
                normalized['emotion_summary']['distribution'] = normalized_emotions
            
            # Normalize insights
            if 'insights' in ai_results:
                insights = ai_results['insights']
                
                # Normalize satisfaction index
                if 'customer_satisfaction_index' in insights:
                    numeric_val, text_level = self.normalize_satisfaction_index(
                        insights['customer_satisfaction_index']
                    )
                    normalized['insights']['customer_satisfaction_index'] = numeric_val
                    normalized['insights']['satisfaction_level'] = text_level
                
                # Normalize emotional intensity
                if 'emotional_intensity' in insights:
                    normalized['insights']['emotional_intensity'] = self.normalize_intensity_level(
                        insights['emotional_intensity']
                    )
                
                # Normalize quality levels
                if 'analysis_quality' in insights:
                    normalized['insights']['analysis_quality'] = self.normalize_quality_level(
                        insights['analysis_quality']
                    )
            
            # Calculate sentiment percentages from normalized sentiments
            if 'sentiments' in normalized:
                sentiment_counts = {}
                total_sentiments = len(normalized['sentiments'])
                
                for sentiment in normalized['sentiments']:
                    sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1
                
                # Convert to percentages
                sentiment_percentages = {}
                for sentiment, count in sentiment_counts.items():
                    percentage = round((count / total_sentiments) * 100, 1) if total_sentiments > 0 else 0
                    sentiment_percentages[sentiment] = percentage
                
                normalized['sentiment_percentages'] = sentiment_percentages
            
            logger.info("✅ AI results successfully normalized for UI compatibility")
            return normalized
            
        except Exception as e:
            logger.error(f"Error normalizing AI results: {e}")
            # Return original results as fallback
            return ai_results
    
    def create_ui_safe_defaults(self, total_comments: int = 0) -> Dict[str, Any]:
        """
        Create safe default results when AI fails completely
        
        Args:
            total_comments: Number of comments processed
            
        Returns:
            Default results structure compatible with UI
        """
        return {
            'total': total_comments,
            'sentiments': ['neutral'] * total_comments,
            'sentiment_percentages': {'positivo': 0, 'negativo': 0, 'neutral': 100},
            'emotion_summary': {
                'distribution': {'neutral': total_comments},
                'avg_intensity': 5.0
            },
            'insights': {
                'customer_satisfaction_index': 60,
                'satisfaction_level': 'Medio',
                'emotional_intensity': 'Media',
                'sentiment_stability': 'balanceado',
                'engagement_quality': 'medium',
                'analysis_quality': 'medium',
                'priority_action_areas': ['analizar_comentarios_adicionales']
            },
            'theme_counts': {'general': total_comments},
            'recommendations': ['Analizar más comentarios para obtener insights específicos'],
            'analysis_method': 'FALLBACK_SAFE',
            'ai_insights_enabled': False
        }


# Global mapper instance for easy access
_global_mapper = None

def get_ai_output_mapper() -> AIOutputMapper:
    """Get global AI output mapper instance"""
    global _global_mapper
    if _global_mapper is None:
        _global_mapper = AIOutputMapper()
    return _global_mapper


def normalize_ai_for_ui(ai_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience function to normalize AI results for UI
    
    Args:
        ai_results: Raw AI analysis results
        
    Returns:
        Normalized results compatible with UI components
    """
    mapper = get_ai_output_mapper()
    return mapper.normalize_ai_results(ai_results)


def create_safe_fallback(total_comments: int = 0) -> Dict[str, Any]:
    """
    Convenience function to create safe fallback results
    
    Args:
        total_comments: Number of comments processed
        
    Returns:
        Safe default results for UI
    """
    mapper = get_ai_output_mapper()
    return mapper.create_ui_safe_defaults(total_comments)