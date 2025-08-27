"""
Enhanced Customer Satisfaction Analyzer for Personal Paraguay
Implements comprehensive NPS segmentation, emotion analysis, and business insights
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from collections import Counter
import re
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class EnhancedAnalyzer:
    """Advanced analyzer with NPS segmentation and comprehensive insights"""
    
    def __init__(self):
        self.name = "Enhanced Customer Satisfaction Analyzer"
        self.description = "Comprehensive NPS, sentiment, emotion, and topic analysis"
        
        # NPS Segmentation thresholds
        self.nps_thresholds = {
            'promoter': (9, 10),
            'passive': (7, 8),
            'detractor': (0, 6)
        }
        
        # Emotion mapping patterns
        self.emotion_patterns = {
            'frustration': [
                'no funciona', 'siempre', 'nunca', 'terrible', 'pésimo',
                'mal servicio', 'no anda', 'no sirve', 'cansado', 'harto'
            ],
            'satisfaction': [
                'excelente', 'muy bien', 'perfecto', 'satisfecho', 'contento',
                'feliz', 'buenísimo', 'recomiendo', 'mejor', 'genial'
            ],
            'disappointment': [
                'esperaba más', 'decepción', 'podría ser mejor', 'regular',
                'más o menos', 'no es lo que', 'debería', 'falta'
            ],
            'anger': [
                'enojado', 'molesto', 'indignado', 'furioso', 'bronca',
                'rabia', 'inaceptable', 'vergüenza', 'desastre'
            ],
            'gratitude': [
                'gracias', 'agradezco', 'agradecer', 'muy amable', 'atención',
                'ayuda', 'solucionó', 'resolvió'
            ]
        }
        
        # Topic patterns for clustering
        self.topic_patterns = {
            'service_reliability': [
                'conexión', 'intermitente', 'corte', 'inestable', 'cae',
                'desconecta', 'sin servicio', 'no anda', 'falla', 'interrumpe'
            ],
            'customer_service': [
                'atención', 'técnico', 'llamada', 'respuesta', 'demora',
                'trato', 'personal', 'operador', 'soporte', 'ayuda'
            ],
            'pricing_value': [
                'precio', 'caro', 'costo', 'factura', 'cobro',
                'tarifa', 'plan', 'aumentó', 'pago', 'valor'
            ],
            'technical_quality': [
                'velocidad', 'lento', 'rápido', 'mb', 'ping',
                'latencia', 'descarga', 'streaming', 'juego', 'lag'
            ],
            'billing_payment': [
                'factura', 'cobro', 'pago', 'débito', 'tarjeta',
                'vencimiento', 'mora', 'recargo', 'error cobro'
            ],
            'installation_setup': [
                'instalación', 'router', 'módem', 'configuración', 'equipo',
                'antena', 'cable', 'fibra', 'técnico instaló'
            ]
        }
        
        # Pain point keywords
        self.pain_point_keywords = [
            'no funciona', 'problema', 'error', 'falla', 'mal',
            'lento', 'corta', 'sin servicio', 'no anda', 'reclamo',
            'queja', 'demora', 'espera', 'nunca', 'siempre falla'
        ]
        
        # Success indicators
        self.success_keywords = [
            'excelente', 'rápido', 'solucionó', 'mejoro', 'funciona bien',
            'sin problemas', 'estable', 'conforme', 'recomiendo', 'perfecto'
        ]

    def analyze_batch(self, comments_df: pd.DataFrame) -> Dict:
        """
        Comprehensive batch analysis of customer comments
        
        Args:
            comments_df: DataFrame with columns [Comentario Final, Nota, etc.]
            
        Returns:
            Comprehensive analysis results dictionary
        """
        # Check if NPS data is available and validate
        has_nps_data = 'Nota' in comments_df.columns
        if not has_nps_data:
            logger.warning("'Nota' column not found - NPS-related analysis will be limited")
        else:
            # Validate NPS scores are in valid range (0-10)
            invalid_scores = comments_df[
                comments_df['Nota'].notna() & 
                ((comments_df['Nota'] < 0) | (comments_df['Nota'] > 10))
            ]
            if len(invalid_scores) > 0:
                logger.warning(f"Found {len(invalid_scores)} invalid NPS scores (outside 0-10 range)")
        
        results = {
            'nps_analysis': self._analyze_nps(comments_df),
            'sentiment_emotion': self._analyze_sentiment_emotion(comments_df),
            'topic_themes': self._extract_topics(comments_df),
            'pain_points': self._prioritize_pain_points(comments_df),
            'language_insights': self._analyze_language(comments_df),
            'improvement_opportunities': self._identify_improvements(comments_df),
            'correlation_analysis': self._analyze_correlations(comments_df),
            'summary_metrics': self._calculate_summary_metrics(comments_df),
            'has_nps_data': has_nps_data  # Add flag for consumers
        }
        
        return results
    
    def _analyze_nps(self, df: pd.DataFrame) -> Dict:
        """Analyze NPS segmentation and distribution"""
        nps_results = {
            'promoters': {'count': 0, 'percentage': 0, 'comments': []},
            'passives': {'count': 0, 'percentage': 0, 'comments': []},
            'detractors': {'count': 0, 'percentage': 0, 'comments': []},
            'nps_score': 0,
            'distribution': {}
        }
        
        if 'Nota' in df.columns:
            # Count valid NPS scores for accurate percentage calculation
            valid_scores_df = df[df['Nota'].notna()]
            total_valid_scores = len(valid_scores_df)
            
            if total_valid_scores == 0:
                logger.warning("No valid NPS scores found in 'Nota' column")
                nps_results['error'] = "No valid NPS scores available"
                return nps_results
            
            # Segment by NPS category
            for index, row in valid_scores_df.iterrows():
                try:
                    score = float(row['Nota'])
                    # Validate score is in acceptable range
                    if not (0 <= score <= 10):
                        logger.warning(f"Invalid NPS score {score} at index {index}, skipping")
                        continue
                        
                    comment = str(row.get('Comentario Final', ''))
                    
                    if 9 <= score <= 10:
                        nps_results['promoters']['count'] += 1
                        nps_results['promoters']['comments'].append({
                            'score': score,
                            'comment': comment[:200]
                        })
                    elif 7 <= score <= 8:
                        nps_results['passives']['count'] += 1
                        nps_results['passives']['comments'].append({
                            'score': score,
                            'comment': comment[:200]
                        })
                    else:  # 0 <= score <= 6
                        nps_results['detractors']['count'] += 1
                        nps_results['detractors']['comments'].append({
                            'score': score,
                            'comment': comment[:200]
                        })
                except (ValueError, TypeError) as e:
                    logger.warning(f"Error processing NPS score at index {index}: {e}")
                    continue
            
            if total_valid_scores > 0:
                # Calculate percentages based on valid scores only
                nps_results['promoters']['percentage'] = (nps_results['promoters']['count'] / total_valid_scores) * 100
                nps_results['passives']['percentage'] = (nps_results['passives']['count'] / total_valid_scores) * 100
                nps_results['detractors']['percentage'] = (nps_results['detractors']['count'] / total_valid_scores) * 100
                
                # Calculate NPS score
                nps_results['nps_score'] = nps_results['promoters']['percentage'] - nps_results['detractors']['percentage']
                
                # Score distribution from valid scores only
                score_counts = valid_scores_df['Nota'].value_counts().sort_index()
                nps_results['distribution'] = score_counts.to_dict()
                
                # Add metadata about data quality
                nps_results['data_quality'] = {
                    'total_comments': len(df),
                    'valid_scores': total_valid_scores,
                    'missing_scores': len(df) - total_valid_scores,
                    'completion_rate': (total_valid_scores / len(df)) * 100 if len(df) > 0 else 0
                }
        else:
            # When no Nota column is available, provide informative response
            nps_results['error'] = "NPS analysis unavailable - 'Nota' column not found"
            nps_results['message'] = "To enable NPS analysis, ensure your data includes a 'Nota' column with scores 0-10"
            logger.info("NPS analysis skipped - no 'Nota' column in data")
        
        return nps_results
    
    def _analyze_sentiment_emotion(self, df: pd.DataFrame) -> Dict:
        """Analyze sentiment and map to emotions"""
        emotion_results = {
            'sentiment_distribution': {'positive': 0, 'neutral': 0, 'negative': 0},
            'emotion_mapping': {},
            'sentiment_score_correlation': {},
            'misalignment_cases': []
        }
        
        for emotion in self.emotion_patterns:
            emotion_results['emotion_mapping'][emotion] = 0
        
        for index, row in df.iterrows():
            comment = str(row.get('Comentario Final', '')).lower()
            # Use actual score if available, None otherwise for proper handling
            score = row.get('Nota') if 'Nota' in df.columns and pd.notna(row.get('Nota')) else None
            
            # Sentiment analysis
            sentiment = self._detect_sentiment(comment)
            emotion_results['sentiment_distribution'][sentiment] += 1
            
            # Emotion detection
            detected_emotions = self._detect_emotions(comment)
            for emotion in detected_emotions:
                emotion_results['emotion_mapping'][emotion] += 1
            
            # Check for misalignment (high score but negative sentiment or vice versa)
            try:
                score_val = float(score)
                if (score_val >= 8 and sentiment == 'negative') or (score_val <= 3 and sentiment == 'positive'):
                    emotion_results['misalignment_cases'].append({
                        'score': score_val,
                        'sentiment': sentiment,
                        'comment': comment[:100]
                    })
            except (ValueError, TypeError) as e:
                # Expected when score is None or invalid - this is normal behavior
                logger.debug(f"Skipping misalignment check for invalid score '{score}': {str(e)}")
        
        # Calculate percentages
        total = len(df)
        if total > 0:
            for sentiment in emotion_results['sentiment_distribution']:
                count = emotion_results['sentiment_distribution'][sentiment]
                emotion_results['sentiment_distribution'][sentiment] = {
                    'count': count,
                    'percentage': (count / total) * 100
                }
        
        return emotion_results
    
    def _extract_topics(self, df: pd.DataFrame) -> Dict:
        """Extract and cluster topics from comments"""
        topic_results = {
            'main_topics': {},
            'topic_distribution': {},
            'topic_sentiment': {},
            'emerging_themes': []
        }
        
        # Initialize topic counters
        for topic in self.topic_patterns:
            topic_results['main_topics'][topic] = {
                'count': 0,
                'percentage': 0,
                'sample_comments': [],
                'avg_score': 0
            }
        
        # Analyze each comment
        for index, row in df.iterrows():
            comment = str(row.get('Comentario Final', '')).lower()
            # Use actual score if available for correlation analysis
            score = row.get('Nota') if 'Nota' in df.columns and pd.notna(row.get('Nota')) else None
            
            # Detect topics
            detected_topics = self._detect_topics(comment)
            
            for topic in detected_topics:
                topic_results['main_topics'][topic]['count'] += 1
                topic_results['main_topics'][topic]['sample_comments'].append(comment[:100])
                
                try:
                    score_val = float(score)
                    if topic_results['main_topics'][topic]['avg_score'] == 0:
                        topic_results['main_topics'][topic]['avg_score'] = score_val
                    else:
                        # Running average
                        count = topic_results['main_topics'][topic]['count']
                        prev_avg = topic_results['main_topics'][topic]['avg_score']
                        topic_results['main_topics'][topic]['avg_score'] = ((prev_avg * (count - 1)) + score_val) / count
                except (ValueError, TypeError) as e:
                    # Expected when score is None or invalid - skip score averaging for this topic
                    logger.debug(f"Skipping score averaging for topic '{topic}' due to invalid score '{score}': {str(e)}")
                    continue
        
        # Calculate percentages and limit samples
        total = len(df)
        if total > 0:
            for topic in topic_results['main_topics']:
                topic_data = topic_results['main_topics'][topic]
                topic_data['percentage'] = (topic_data['count'] / total) * 100
                topic_data['sample_comments'] = topic_data['sample_comments'][:5]  # Keep only 5 samples
        
        return topic_results
    
    def _prioritize_pain_points(self, df: pd.DataFrame) -> Dict:
        """Identify and prioritize customer pain points"""
        pain_points = {
            'high_frequency': {},
            'high_impact': [],
            'recurring_issues': {},
            'priority_matrix': []
        }
        
        pain_point_counter = Counter()
        pain_point_scores = {}
        
        for index, row in df.iterrows():
            comment = str(row.get('Comentario Final', '')).lower()
            # Use actual score if available for pain point correlation
            score = row.get('Nota') if 'Nota' in df.columns and pd.notna(row.get('Nota')) else None
            
            # Detect pain points
            detected_pains = self._detect_pain_points(comment)
            
            for pain in detected_pains:
                pain_point_counter[pain] += 1
                
                # Track average score for each pain point
                if pain not in pain_point_scores:
                    pain_point_scores[pain] = []
                try:
                    pain_point_scores[pain].append(float(score))
                except (ValueError, TypeError) as e:
                    # Expected when score is None or invalid - pain point tracking continues without score
                    logger.debug(f"Skipping score tracking for pain point '{pain}' due to invalid score '{score}': {str(e)}")
        
        # High frequency pain points
        pain_points['high_frequency'] = dict(pain_point_counter.most_common(10))
        
        # High impact (low average score)
        for pain, scores in pain_point_scores.items():
            if scores:
                avg_score = sum(scores) / len(scores)
                if avg_score < 5:  # High impact threshold
                    pain_points['high_impact'].append({
                        'issue': pain,
                        'frequency': pain_point_counter[pain],
                        'avg_score': avg_score,
                        'impact_level': 'high' if avg_score < 3 else 'medium'
                    })
        
        # Sort high impact by frequency
        pain_points['high_impact'] = sorted(
            pain_points['high_impact'], 
            key=lambda x: x['frequency'], 
            reverse=True
        )[:10]
        
        # Create priority matrix (frequency vs impact)
        for pain in pain_points['high_frequency']:
            if pain in pain_point_scores and pain_point_scores[pain]:
                avg_score = sum(pain_point_scores[pain]) / len(pain_point_scores[pain])
                frequency = pain_point_counter[pain]
                
                # Classify priority
                if frequency > 5 and avg_score < 5:
                    priority = 'critical'
                elif frequency > 3 or avg_score < 6:
                    priority = 'high'
                else:
                    priority = 'medium'
                
                pain_points['priority_matrix'].append({
                    'issue': pain,
                    'frequency': frequency,
                    'avg_score': avg_score,
                    'priority': priority
                })
        
        return pain_points
    
    def _analyze_language(self, df: pd.DataFrame) -> Dict:
        """Analyze language usage and extract keywords"""
        language_insights = {
            'language_mix': {'spanish': 0, 'guarani': 0, 'mixed': 0},
            'top_keywords': {},
            'colloquial_terms': [],
            'frequent_phrases': {}
        }
        
        # Guaraní indicators
        guarani_patterns = [
            'nde', 'che', 'ha', 'pe', 'mba', 'pora', 'vai', 'heta', 
            'katu', 'ite', 'kuera', 'ngo', 'iko', 'oiko'
        ]
        
        all_words = []
        all_phrases = []
        
        for index, row in df.iterrows():
            comment = str(row.get('Comentario Final', '')).lower()
            
            # Language detection
            has_guarani = any(pattern in comment for pattern in guarani_patterns)
            if has_guarani:
                if len(comment.split()) > 5:  # Likely mixed if longer comment
                    language_insights['language_mix']['mixed'] += 1
                else:
                    language_insights['language_mix']['guarani'] += 1
            else:
                language_insights['language_mix']['spanish'] += 1
            
            # Extract words and phrases
            words = re.findall(r'\b\w+\b', comment)
            all_words.extend(words)
            
            # Extract 2-3 word phrases
            for i in range(len(words) - 1):
                all_phrases.append(' '.join(words[i:i+2]))
                if i < len(words) - 2:
                    all_phrases.append(' '.join(words[i:i+3]))
        
        # Top keywords (excluding common stop words)
        stop_words = ['el', 'la', 'de', 'que', 'y', 'a', 'en', 'es', 'por', 'con', 'no', 'un', 'una']
        filtered_words = [w for w in all_words if w not in stop_words and len(w) > 2]
        word_counter = Counter(filtered_words)
        language_insights['top_keywords'] = dict(word_counter.most_common(20))
        
        # Frequent phrases
        phrase_counter = Counter(all_phrases)
        language_insights['frequent_phrases'] = dict(phrase_counter.most_common(15))
        
        # Detect colloquial terms (informal language)
        colloquial_patterns = [
            'nomás', 'luego', 'piko', 'kore', 'ndaje', 'voi', 
            'pio', 'mba\'e', 'porã', 'vai', 'hína'
        ]
        
        for pattern in colloquial_patterns:
            count = sum(1 for comment in df['Comentario Final'].astype(str) if pattern in comment.lower())
            if count > 0:
                language_insights['colloquial_terms'].append({
                    'term': pattern,
                    'frequency': count
                })
        
        return language_insights
    
    def _identify_improvements(self, df: pd.DataFrame) -> Dict:
        """Identify improvement opportunities"""
        improvements = {
            'quick_wins': [],
            'structural_problems': [],
            'success_patterns': [],
            'recommendations': []
        }
        
        # Analyze promoters for success patterns
        promoter_comments = df[df['Nota'] >= 9]['Comentario Final'].astype(str) if 'Nota' in df.columns else []
        detractor_comments = df[df['Nota'] <= 6]['Comentario Final'].astype(str) if 'Nota' in df.columns else []
        
        # Find what promoters praise
        success_counter = Counter()
        for comment in promoter_comments:
            comment_lower = comment.lower()
            for keyword in self.success_keywords:
                if keyword in comment_lower:
                    success_counter[keyword] += 1
        
        improvements['success_patterns'] = [
            {'pattern': pattern, 'frequency': count}
            for pattern, count in success_counter.most_common(10)
        ]
        
        # Identify quick wins (simple fixes mentioned frequently)
        quick_win_patterns = [
            ('router', 'configuración router'),
            ('velocidad', 'mejorar velocidad'),
            ('atención', 'tiempo de respuesta'),
            ('factura', 'claridad en facturación')
        ]
        
        for pattern, description in quick_win_patterns:
            count = sum(1 for comment in detractor_comments if pattern in comment.lower())
            if count > 2:  # Threshold for quick win
                improvements['quick_wins'].append({
                    'issue': description,
                    'frequency': count,
                    'effort': 'low',
                    'impact': 'high' if count > 5 else 'medium'
                })
        
        # Identify structural problems (chronic issues)
        structural_patterns = [
            ('siempre', 'problema recurrente'),
            ('meses', 'problema de larga duración'),
            ('nunca funciona', 'falla sistémica'),
            ('todos los días', 'problema diario')
        ]
        
        for pattern, description in structural_patterns:
            matching_comments = [c for c in df['Comentario Final'].astype(str) if pattern in c.lower()]
            if len(matching_comments) > 1:
                improvements['structural_problems'].append({
                    'issue': description,
                    'frequency': len(matching_comments),
                    'severity': 'critical' if len(matching_comments) > 5 else 'high',
                    'sample': matching_comments[0][:100] if matching_comments else ''
                })
        
        # Generate recommendations
        improvements['recommendations'] = self._generate_recommendations(
            improvements, 
            self._prioritize_pain_points(df)
        )
        
        return improvements
    
    def _analyze_correlations(self, df: pd.DataFrame) -> Dict:
        """Analyze correlations between scores and comment types"""
        correlations = {
            'score_sentiment_correlation': {},
            'topic_score_correlation': {},
            'emotion_score_correlation': {},
            'patterns': []
        }
        
        if 'Nota' not in df.columns:
            return correlations
        
        # Score-sentiment correlation
        for sentiment in ['positive', 'negative', 'neutral']:
            scores = []
            for index, row in df.iterrows():
                comment = str(row.get('Comentario Final', '')).lower()
                # Only use actual scores for correlation analysis
                score = row.get('Nota') if 'Nota' in df.columns and pd.notna(row.get('Nota')) else None
                
                if score is not None and self._detect_sentiment(comment) == sentiment:
                    try:
                        scores.append(float(score))
                    except (ValueError, TypeError) as e:
                        # Expected when score is None or invalid - skip this score in correlation analysis
                        logger.debug(f"Skipping correlation analysis for sentiment '{sentiment}' due to invalid score '{score}': {str(e)}")
            
            if scores:
                correlations['score_sentiment_correlation'][sentiment] = {
                    'avg_score': sum(scores) / len(scores),
                    'count': len(scores)
                }
        
        # Detect patterns
        if correlations['score_sentiment_correlation']:
            # Check if negative sentiment correlates with low scores
            neg_data = correlations['score_sentiment_correlation'].get('negative', {})
            if neg_data.get('avg_score', 10) < 5:
                correlations['patterns'].append({
                    'pattern': 'Strong correlation',
                    'description': 'Negative sentiment strongly correlates with low scores',
                    'confidence': 'high'
                })
        
        return correlations
    
    def _calculate_summary_metrics(self, df: pd.DataFrame) -> Dict:
        """Calculate summary metrics for executive dashboard"""
        total = len(df)
        
        metrics = {
            'total_feedback': total,
            'avg_nps_score': 0,
            'sentiment_index': 0,
            'response_quality': 0,
            'actionable_insights': 0
        }
        
        if 'Nota' in df.columns:
            metrics['avg_nps_score'] = df['Nota'].mean()
        
        # Calculate sentiment index (-100 to +100)
        sentiment_dist = self._analyze_sentiment_emotion(df)['sentiment_distribution']
        pos = sentiment_dist.get('positive', {'count': 0})['count'] if isinstance(sentiment_dist.get('positive'), dict) else sentiment_dist.get('positive', 0)
        neg = sentiment_dist.get('negative', {'count': 0})['count'] if isinstance(sentiment_dist.get('negative'), dict) else sentiment_dist.get('negative', 0)
        
        if total > 0:
            metrics['sentiment_index'] = ((pos - neg) / total) * 100
        
        # Response quality (based on comment length and detail)
        avg_length = df['Comentario Final'].astype(str).str.len().mean()
        metrics['response_quality'] = min(100, (avg_length / 100) * 100)  # Normalize to 0-100
        
        return metrics
    
    # Helper methods
    def _detect_sentiment(self, comment: str) -> str:
        """Simple sentiment detection"""
        comment_lower = comment.lower()
        
        positive_count = sum(1 for word in self.success_keywords if word in comment_lower)
        negative_count = sum(1 for word in self.pain_point_keywords if word in comment_lower)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
    
    def _detect_emotions(self, comment: str) -> List[str]:
        """Detect emotions in comment"""
        detected = []
        comment_lower = comment.lower()
        
        for emotion, patterns in self.emotion_patterns.items():
            if any(pattern in comment_lower for pattern in patterns):
                detected.append(emotion)
        
        return detected if detected else ['neutral']
    
    def _detect_topics(self, comment: str) -> List[str]:
        """Detect topics in comment"""
        detected = []
        comment_lower = comment.lower()
        
        for topic, patterns in self.topic_patterns.items():
            if any(pattern in comment_lower for pattern in patterns):
                detected.append(topic)
        
        return detected if detected else ['general']
    
    def _detect_pain_points(self, comment: str) -> List[str]:
        """Detect pain points in comment"""
        detected = []
        comment_lower = comment.lower()
        
        for keyword in self.pain_point_keywords:
            if keyword in comment_lower:
                detected.append(keyword)
        
        return detected
    
    def _generate_recommendations(self, improvements: Dict, pain_points: Dict) -> List[Dict]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Based on quick wins
        for quick_win in improvements.get('quick_wins', [])[:3]:
            recommendations.append({
                'type': 'quick_win',
                'priority': 'high',
                'action': f"Address {quick_win['issue']} - affecting {quick_win['frequency']} customers",
                'expected_impact': quick_win['impact'],
                'effort': quick_win['effort']
            })
        
        # Based on structural problems
        for problem in improvements.get('structural_problems', [])[:2]:
            recommendations.append({
                'type': 'structural',
                'priority': 'critical',
                'action': f"Fix {problem['issue']} - {problem['severity']} severity issue",
                'expected_impact': 'high',
                'effort': 'high'
            })
        
        # Based on success patterns
        if improvements.get('success_patterns'):
            top_success = improvements['success_patterns'][0] if improvements['success_patterns'] else None
            if top_success:
                recommendations.append({
                    'type': 'replicate_success',
                    'priority': 'medium',
                    'action': f"Expand successful pattern: {top_success['pattern']}",
                    'expected_impact': 'medium',
                    'effort': 'medium'
                })
        
        return recommendations

    def get_insights(self, analysis_results: Dict) -> Dict:
        """Generate executive insights from analysis results"""
        insights = {
            'executive_summary': self._generate_executive_summary(analysis_results),
            'key_metrics': analysis_results.get('summary_metrics', {}),
            'critical_actions': self._identify_critical_actions(analysis_results),
            'opportunity_areas': self._identify_opportunities(analysis_results)
        }
        
        return insights
    
    def _generate_executive_summary(self, results: Dict) -> str:
        """Generate executive summary text"""
        nps = results.get('nps_analysis', {})
        nps_score = nps.get('nps_score', 0)
        
        sentiment = results.get('sentiment_emotion', {}).get('sentiment_distribution', {})
        
        summary = f"NPS Score: {nps_score:.1f} | "
        summary += f"Promoters: {nps.get('promoters', {}).get('percentage', 0):.1f}% | "
        summary += f"Detractors: {nps.get('detractors', {}).get('percentage', 0):.1f}%"
        
        return summary
    
    def _identify_critical_actions(self, results: Dict) -> List[str]:
        """Identify critical actions needed"""
        actions = []
        
        # Check NPS score
        nps_score = results.get('nps_analysis', {}).get('nps_score', 0)
        if nps_score < 0:
            actions.append("Urgent: NPS is negative - immediate action required on customer satisfaction")
        
        # Check pain points
        pain_points = results.get('pain_points', {}).get('priority_matrix', [])
        critical_pains = [p for p in pain_points if p.get('priority') == 'critical']
        if critical_pains:
            actions.append(f"Address {len(critical_pains)} critical pain points immediately")
        
        return actions
    
    def _identify_opportunities(self, results: Dict) -> List[str]:
        """Identify improvement opportunities"""
        opportunities = []
        
        improvements = results.get('improvement_opportunities', {})
        
        # Quick wins
        quick_wins = improvements.get('quick_wins', [])
        if quick_wins:
            opportunities.append(f"{len(quick_wins)} quick wins identified for immediate implementation")
        
        # Success patterns to replicate
        success_patterns = improvements.get('success_patterns', [])
        if success_patterns:
            opportunities.append(f"{len(success_patterns)} success patterns can be expanded")
        
        return opportunities