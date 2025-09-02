"""
Result Converter - Format conversion responsibilities
Extracted from AIAnalysisAdapter for focused data transformation
"""

import pandas as pd
import numpy as np
import logging
from collections import Counter
from datetime import datetime
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


class ResultConverter:
    """
    Handles conversion of AI results to expected application format
    Focused responsibility for data transformation
    """
    
    def __init__(self):
        # Initialize fallback analyzers for enhanced processing
        from src.enhanced_analysis import EnhancedAnalysis
        from src.improved_analysis import ImprovedAnalysis
        
        self.enhanced_analyzer = EnhancedAnalysis()
        self.improved_analyzer = ImprovedAnalysis()
    
    def convert_ai_results_to_expected_format(self, ai_results: List[Dict], analysis_data: Dict, 
                                            uploaded_file) -> Dict[str, Any]:
        """
        Convert OpenAI results to the exact format expected by the existing system
        
        Args:
            ai_results: Results from OpenAI analysis
            analysis_data: Extracted file data
            uploaded_file: Original uploaded file
            
        Returns:
            Dictionary in expected format for UI consumption
        """
        try:
            logger.info("[RESULT_CONVERTER] Converting AI results to expected format")
            
            comments = analysis_data['comments']
            nps_data = analysis_data.get('nps_data', [])
            nota_data = analysis_data.get('nota_data', [])
            has_nps = analysis_data.get('has_nps', False)
            has_nota = analysis_data.get('has_nota', False)
            
            # Convert AI sentiments to expected Spanish format
            sentiments = self._convert_sentiments(ai_results)
            
            # Process enhanced results for comprehensive analysis
            enhanced_results = self._create_enhanced_results(ai_results, comments)
            
            # Calculate all statistics using converted data
            sentiment_stats = self._calculate_sentiment_statistics(sentiments)
            
            # Extract themes from AI results
            theme_counts, theme_examples = self._extract_themes_from_ai_results(ai_results, comments)
            
            # Calculate NPS scores
            nps_analysis = self._calculate_nps_scores(enhanced_results, nps_data, nota_data, has_nps, sentiments)
            
            # Generate emotion summary
            emotion_summary = self._generate_emotion_summary(enhanced_results)
            
            # Calculate file metrics
            file_size_kb = getattr(uploaded_file, 'size', 0) / 1024 if hasattr(uploaded_file, 'size') else 0
            avg_length = np.mean([len(str(c)) for c in comments]) if comments else 0
            
            # Return comprehensive result structure
            return self._build_final_result_structure(
                comments=comments,
                sentiments=sentiments,
                sentiment_stats=sentiment_stats,
                theme_counts=theme_counts,
                theme_examples=theme_examples,
                nps_analysis=nps_analysis,
                emotion_summary=emotion_summary,
                enhanced_results=enhanced_results,
                uploaded_file=uploaded_file,
                file_size_kb=file_size_kb,
                avg_length=avg_length
            )
            
        except Exception as e:
            logger.error(f"Failed to convert AI results: {str(e)}")
            raise
    
    def _convert_sentiments(self, ai_results: List[Dict]) -> List[str]:
        """Convert AI sentiments to expected Spanish format"""
        sentiments = []
        for result in ai_results:
            ai_sentiment = result.get('sentiment', 'neutral')
            # Convert to Spanish format expected by existing system
            if ai_sentiment == 'positive':
                sentiments.append('positivo')
            elif ai_sentiment == 'negative':
                sentiments.append('negativo')
            else:
                sentiments.append('neutral')
        return sentiments
    
    def _create_enhanced_results(self, ai_results: List[Dict], comments: List[str]) -> List[Dict]:
        """Create enhanced results structure from AI data"""
        enhanced_results = []
        
        for i, (comment, ai_result) in enumerate(zip(comments, ai_results)):
            # Convert AI emotions to expected format
            ai_emotions = ai_result.get('emotions', ['neutral'])
            emotions_formatted = {
                'intensity': self._calculate_emotion_intensity(ai_emotions, ai_result.get('confidence', 0.5)),
                'dominant': ai_emotions[0] if ai_emotions else 'neutral',
                'detected': ai_emotions
            }
            
            # Convert AI themes to extended format
            ai_themes = ai_result.get('themes', [])
            extended_themes = ai_themes  # Simplified for now
            
            # Convert AI pain points to churn risk
            ai_pain_points = ai_result.get('pain_points', [])
            churn_risk = self._convert_pain_points_to_churn_risk(ai_pain_points, ai_result.get('confidence', 0.5))
            
            enhanced_result = {
                'comment': comment,
                'emotions': emotions_formatted,
                'themes': extended_themes,
                'churn_risk': churn_risk,
                'urgency': self._determine_urgency_level(ai_pain_points, ai_emotions),
                'confidence': ai_result.get('confidence', 0.5)
            }
            
            enhanced_results.append(enhanced_result)
        
        return enhanced_results
    
    def _calculate_sentiment_statistics(self, sentiments: List[str]) -> Dict[str, Any]:
        """Calculate sentiment distribution and percentages"""
        total = len(sentiments)
        if total == 0:
            return {
                'total': 0,
                'sentiment_counts': {},
                'sentiment_percentages': {'positivo': 0, 'negativo': 0, 'neutral': 0}
            }
        
        sentiment_counts = Counter(sentiments)
        
        return {
            'total': total,
            'sentiment_counts': dict(sentiment_counts),
            'sentiment_percentages': {
                'positivo': round((sentiment_counts['positivo'] / total * 100), 1) if total > 0 else 0,
                'negativo': round((sentiment_counts['negativo'] / total * 100), 1) if total > 0 else 0,
                'neutral': round((sentiment_counts['neutral'] / total * 100), 1) if total > 0 else 0
            }
        }
    
    def _extract_themes_from_ai_results(self, ai_results: List[Dict], comments: List[str]) -> tuple:
        """Extract theme information from AI results"""
        all_themes = []
        theme_examples = {}
        
        for i, result in enumerate(ai_results):
            themes = result.get('themes', [])
            for theme in themes:
                all_themes.append(theme)
                if theme not in theme_examples:
                    theme_examples[theme] = []
                if len(theme_examples[theme]) < 3:  # Keep max 3 examples per theme
                    theme_examples[theme].append(comments[i] if i < len(comments) else "")
        
        theme_counts = dict(Counter(all_themes))
        return theme_counts, theme_examples
    
    def _calculate_nps_scores(self, enhanced_results: List[Dict], nps_data: List, nota_data: List, 
                            has_nps: bool, sentiments: List[str]) -> Dict[str, Any]:
        """Calculate NPS scores from available data"""
        if has_nps and nps_data:
            # Convert NPS data to numeric values (fix for TypeError)
            nps_scores = []
            for score in nps_data:
                if pd.notna(score):
                    try:
                        numeric_score = float(score)
                        nps_scores.append(numeric_score)
                    except (ValueError, TypeError):
                        continue
                        
            if nps_scores:
                promoters = sum(1 for score in nps_scores if score >= 9)
                detractors = sum(1 for score in nps_scores if score <= 6)
                passives = sum(1 for score in nps_scores if 7 <= score <= 8)
                nps = ((promoters - detractors) / len(nps_scores)) * 100
            else:
                promoters = detractors = passives = nps = 0
        else:
            # Calculate NPS from AI-enhanced sentiment
            nps_scores = []
            for result in enhanced_results:
                intensity = result['emotions']['intensity']
                sentiment = sentiments[len(nps_scores)] if len(nps_scores) < len(sentiments) else 'neutral'
                nps_score = self.enhanced_analyzer.calculate_nps_from_sentiment(sentiment, intensity)
                nps_scores.append(nps_score)
            
            promoters = sum(1 for score in nps_scores if score >= 50)
            passives = sum(1 for score in nps_scores if -50 <= score < 50)
            detractors = sum(1 for score in nps_scores if score < -50)
            nps = np.mean(nps_scores) if nps_scores else 0
        
        return {
            'score': round(nps, 1),
            'promoters': promoters,
            'detractors': detractors,
            'passives': passives,
            'has_real_nps': has_nps
        }
    
    def _generate_emotion_summary(self, enhanced_results: List[Dict]) -> Dict[str, Any]:
        """Generate emotion summary from enhanced results"""
        if not enhanced_results:
            return {'distribution': {}, 'avg_intensity': 0}
        
        # Collect dominant emotions
        dominant_emotions = [result['emotions']['dominant'] for result in enhanced_results]
        emotion_distribution = dict(Counter(dominant_emotions))
        
        # Calculate average intensity
        intensities = [result['emotions']['intensity'] for result in enhanced_results]
        avg_intensity = np.mean(intensities) if intensities else 0
        
        return {
            'distribution': emotion_distribution,
            'avg_intensity': round(avg_intensity, 1)
        }
    
    def _build_final_result_structure(self, **kwargs) -> Dict[str, Any]:
        """Build the final result structure expected by the UI"""
        return {
            'total': len(kwargs['comments']),
            'comments': kwargs['comments'],
            'sentiments': kwargs['sentiments'],
            'sentiment_percentages': kwargs['sentiment_stats']['sentiment_percentages'],
            'positive_count': kwargs['sentiment_stats']['sentiment_counts'].get('positivo', 0),
            'neutral_count': kwargs['sentiment_stats']['sentiment_counts'].get('neutral', 0),
            'negative_count': kwargs['sentiment_stats']['sentiment_counts'].get('negativo', 0),
            'theme_counts': kwargs['theme_counts'],
            'theme_examples': kwargs['theme_examples'],
            'emotion_summary': kwargs['emotion_summary'],
            'enhanced_results': kwargs['enhanced_results'],
            'nps': kwargs['nps_analysis'],
            'file_size': round(kwargs['file_size_kb'], 1),
            'avg_length': round(kwargs['avg_length']),
            'original_filename': kwargs['uploaded_file'].name,
            'analysis_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'analysis_method': 'AI_POWERED',
            'insights': self._generate_insights(kwargs['sentiment_stats'], kwargs['emotion_summary'], kwargs['nps_analysis'])
        }
    
    def _generate_insights(self, sentiment_stats: Dict, emotion_summary: Dict, nps_analysis: Dict) -> Dict[str, Any]:
        """Generate insights summary for UI consumption"""
        total = sentiment_stats['total']
        sentiment_percentages = sentiment_stats['sentiment_percentages']
        
        return {
            'total_comments': total,
            'sentiment_percentages': sentiment_percentages,
            'avg_confidence': 0.8,  # AI analysis typically has high confidence
            'analysis_method': 'AI_POWERED',
            'customer_satisfaction_index': max(0, min(100, nps_analysis['score'] + 50)),  # Convert NPS to 0-100 scale
            'emotional_intensity': emotion_summary.get('avg_intensity', 0),
            'dominant_sentiment': max(sentiment_percentages, key=sentiment_percentages.get) if sentiment_percentages else 'neutral'
        }
    
    def _calculate_emotion_intensity(self, emotions: List[str], confidence: float) -> float:
        """Calculate emotion intensity from detected emotions and confidence"""
        if not emotions or 'neutral' in emotions:
            return confidence * 0.5
        
        # Enhanced intensity calculation
        intense_emotions = ['enojo', 'frustración', 'alegría', 'satisfacción', 'excitement', 'anger']
        moderate_emotions = ['tristeza', 'esperanza', 'sorpresa', 'preocupación']
        
        max_intensity = confidence * 0.5  # Base intensity from confidence
        
        for emotion in emotions:
            emotion_lower = emotion.lower()
            if any(intense in emotion_lower for intense in intense_emotions):
                max_intensity = max(max_intensity, confidence * 0.9)
            elif any(moderate in emotion_lower for moderate in moderate_emotions):
                max_intensity = max(max_intensity, confidence * 0.7)
        
        return min(1.0, max_intensity)
    
    def _convert_pain_points_to_churn_risk(self, pain_points: List[str], confidence: float) -> Dict[str, Any]:
        """Convert pain points to churn risk assessment"""
        if not pain_points:
            return {'risk_level': 'low', 'risk_score': 0.1, 'factors': []}
        
        # Calculate risk based on pain point severity
        high_risk_indicators = ['conexión_inestable', 'velocidad_baja', 'soporte_deficiente']
        medium_risk_indicators = ['precio_alto', 'instalación_problemas']
        
        risk_score = 0.2  # Base risk
        risk_factors = []
        
        for pain_point in pain_points:
            if pain_point in high_risk_indicators:
                risk_score += 0.3
                risk_factors.append(pain_point)
            elif pain_point in medium_risk_indicators:
                risk_score += 0.15
                risk_factors.append(pain_point)
        
        # Adjust by confidence
        risk_score *= confidence
        risk_score = min(1.0, risk_score)
        
        # Determine risk level
        if risk_score >= 0.7:
            risk_level = 'high'
        elif risk_score >= 0.4:
            risk_level = 'medium'
        else:
            risk_level = 'low'
        
        return {
            'risk_level': risk_level,
            'risk_score': risk_score,
            'factors': risk_factors
        }
    
    def _determine_urgency_level(self, pain_points: List[str], emotions: List[str]) -> str:
        """Determine urgency level from pain points and emotions"""
        urgent_pain_points = ['conexión_inestable', 'velocidad_baja']
        urgent_emotions = ['enojo', 'frustración', 'anger']
        
        if any(pp in pain_points for pp in urgent_pain_points):
            return 'high'
        if any(em.lower() in urgent_emotions for em in emotions):
            return 'medium'
        
        return 'low'