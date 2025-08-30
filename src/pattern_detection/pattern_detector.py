"""
Pattern Detection Module for Comment Analysis
Detects recurring patterns, trends, and anomalies in customer feedback
"""

import re
from typing import Dict, List, Tuple, Optional, Any
from collections import Counter, defaultdict
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class PatternDetector:
    """Advanced pattern detection for customer comments"""
    
    def __init__(self):
        """Initialize pattern detector with predefined patterns"""
        self.service_patterns = {
            'connection_issues': [
                r'no.*(?:funciona|sirve|anda)',
                r'(?:se|me).*(?:corta|cae|desconecta)',
                r'(?:sin|no hay).*(?:señal|internet|conexión)',
                r'(?:intermitente|intermitencia)',
                r'(?:lento|lenta|demora)',
            ],
            'customer_service': [
                r'(?:mal|mala|pésima?).*(?:atención|servicio)',
                r'(?:no|nadie).*(?:responde|atiende|contesta)',
                r'(?:esperé|esperando|demora).*(?:mucho|horas)',
                r'(?:técnico|soporte).*(?:no|nunca).*(?:vino|llegó)',
            ],
            'billing_issues': [
                r'(?:cobro|cobran|factura).*(?:mal|incorrecta?|más)',
                r'(?:caro|costoso|precio)',
                r'(?:no.*corresponde|error.*factura)',
                r'(?:doble.*cobro|duplicado)',
            ],
            'technical_problems': [
                r'(?:router|modem).*(?:no.*funciona|problema)',
                r'(?:reiniciar|resetear).*(?:siempre|constantemente)',
                r'(?:velocidad|mbps|megas).*(?:baja|lenta|prometida)',
                r'(?:ping|latencia).*(?:alto|alta)',
            ],
            'installation': [
                r'(?:instalación|instalar).*(?:demora|tardó|problema)',
                r'(?:técnico).*(?:no.*vino|canceló|tarde)',
                r'(?:cableado|cables?).*(?:mal|problema)',
                r'(?:configuración).*(?:incorrecta|mal)',
            ]
        }
        
        self.emotion_patterns = {
            'frustration': [
                r'(?:harto|cansado|frustrado)',
                r'(?:siempre|todos los días).*(?:problema|falla)',
                r'(?:no.*más|basta)',
                r'(?:cambiar.*(?:empresa|compañía|proveedor))',
            ],
            'urgency': [
                r'(?:urgente|urgencia|inmediato)',
                r'(?:trabajo|teletrabajo|home.*office).*(?:no.*puedo|imposible)',
                r'(?:clases|estudio).*(?:virtual|online).*(?:no.*puedo)',
                r'(?:necesito|requiero).*(?:ya|ahora|inmediato)',
            ],
            'satisfaction': [
                r'(?:excelente|perfecto|genial)',
                r'(?:rápido|rápida).*(?:solución|respuesta)',
                r'(?:resolvieron|solucionaron).*(?:rápido|bien)',
                r'(?:recomiendo|felicitaciones)',
            ]
        }
        
        self.competitor_patterns = {
            'tigo': [r'tigo', r'cambiar.*tigo', r'mejor.*tigo'],
            'claro': [r'claro', r'cambiar.*claro', r'oferta.*claro'],
            'copaco': [r'copaco', r'volver.*copaco'],
            'vox': [r'vox', r'probar.*vox'],
        }
        
        self.temporal_patterns = {
            'time_of_day': {
                'morning': [r'(?:mañana|am|a\.m\.|madrugada)'],
                'afternoon': [r'(?:tarde|pm|p\.m\.|mediodía)'],
                'night': [r'(?:noche|madrugada|00:|01:|02:|23:)'],
                'business_hours': [r'(?:horario.*(?:trabajo|oficina)|9.*5|laboral)'],
            },
            'frequency': {
                'daily': [r'(?:todos los días|diario|diariamente|cada día)'],
                'weekly': [r'(?:semana|semanal|semanalmente)'],
                'monthly': [r'(?:mes|mensual|mensualmente)'],
                'sporadic': [r'(?:a veces|ocasional|esporádico|random)'],
                'constant': [r'(?:siempre|constantemente|todo el tiempo|sin parar)'],
            }
        }

    def detect_patterns(self, comments: List[str]) -> Dict[str, Any]:
        """
        Detect all patterns in a list of comments
        
        Args:
            comments: List of customer comments
            
        Returns:
            Dictionary containing detected patterns and statistics
        """
        results = {
            'service_patterns': self._detect_service_patterns(comments),
            'emotion_patterns': self._detect_emotion_patterns(comments),
            'competitor_mentions': self._detect_competitor_mentions(comments),
            'temporal_patterns': self._detect_temporal_patterns(comments),
            'recurring_phrases': self._find_recurring_phrases(comments),
            'anomalies': self._detect_anomalies(comments),
            'trends': self._detect_trends(comments),
            'correlations': self._find_correlations(comments),
            'summary': {}
        }
        
        # Generate summary
        results['summary'] = self._generate_pattern_summary(results)
        
        return results
    
    def _detect_service_patterns(self, comments: List[str]) -> Dict[str, Any]:
        """Detect service-related patterns"""
        pattern_counts = defaultdict(int)
        pattern_examples = defaultdict(list)
        
        for comment in comments:
            if not comment:
                continue
                
            comment_lower = str(comment).lower()
            for pattern_type, patterns in self.service_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, comment_lower):
                        pattern_counts[pattern_type] += 1
                        if len(pattern_examples[pattern_type]) < 3:
                            pattern_examples[pattern_type].append(comment[:200])
                        break
        
        return {
            'counts': dict(pattern_counts),
            'examples': dict(pattern_examples),
            'top_issues': sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        }
    
    def _detect_emotion_patterns(self, comments: List[str]) -> Dict[str, Any]:
        """Detect emotional patterns"""
        emotion_counts = defaultdict(int)
        emotion_examples = defaultdict(list)
        
        for comment in comments:
            if not comment:
                continue
                
            comment_lower = str(comment).lower()
            for emotion, patterns in self.emotion_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, comment_lower):
                        emotion_counts[emotion] += 1
                        if len(emotion_examples[emotion]) < 3:
                            emotion_examples[emotion].append(comment[:200])
                        break
        
        total = len(comments)
        emotion_percentages = {
            emotion: (count / total * 100) if total > 0 else 0
            for emotion, count in emotion_counts.items()
        }
        
        return {
            'counts': dict(emotion_counts),
            'percentages': emotion_percentages,
            'examples': dict(emotion_examples),
            'dominant_emotion': max(emotion_counts, key=emotion_counts.get) if emotion_counts else None
        }
    
    def _detect_competitor_mentions(self, comments: List[str]) -> Dict[str, Any]:
        """Detect mentions of competitors"""
        competitor_counts = defaultdict(int)
        competitor_contexts = defaultdict(list)
        
        for comment in comments:
            if not comment:
                continue
                
            comment_lower = str(comment).lower()
            for competitor, patterns in self.competitor_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, comment_lower):
                        competitor_counts[competitor] += 1
                        if len(competitor_contexts[competitor]) < 5:
                            # Extract context around mention
                            match = re.search(pattern, comment_lower)
                            if match:
                                start = max(0, match.start() - 50)
                                end = min(len(comment), match.end() + 50)
                                context = comment[start:end]
                                competitor_contexts[competitor].append(context)
                        break
        
        return {
            'counts': dict(competitor_counts),
            'contexts': dict(competitor_contexts),
            'total_mentions': sum(competitor_counts.values()),
            'most_mentioned': max(competitor_counts, key=competitor_counts.get) if competitor_counts else None
        }
    
    def _detect_temporal_patterns(self, comments: List[str]) -> Dict[str, Any]:
        """Detect temporal patterns"""
        temporal_counts = defaultdict(lambda: defaultdict(int))
        
        for comment in comments:
            if not comment:
                continue
                
            comment_lower = str(comment).lower()
            for category, subcategories in self.temporal_patterns.items():
                for subcat, patterns in subcategories.items():
                    for pattern in patterns:
                        if re.search(pattern, comment_lower):
                            temporal_counts[category][subcat] += 1
                            break
        
        return {
            'time_of_day': dict(temporal_counts['time_of_day']),
            'frequency': dict(temporal_counts['frequency']),
            'peak_complaint_time': max(temporal_counts['time_of_day'], 
                                      key=temporal_counts['time_of_day'].get) 
                                      if temporal_counts['time_of_day'] else None,
            'most_common_frequency': max(temporal_counts['frequency'], 
                                        key=temporal_counts['frequency'].get) 
                                        if temporal_counts['frequency'] else None
        }
    
    def _find_recurring_phrases(self, comments: List[str], min_length: int = 3, min_count: int = 3) -> Dict[str, Any]:
        """Find recurring phrases in comments"""
        phrase_counter = Counter()
        
        for comment in comments:
            if not comment:
                continue
                
            # Extract phrases (sequences of words)
            words = str(comment).lower().split()
            words_len = len(words)
            for i in range(words_len - min_length + 1):
                phrase = ' '.join(words[i:i + min_length])
                # Filter out common words and short phrases
                if len(phrase) > 10 and not phrase.startswith(('el', 'la', 'un', 'una', 'de', 'en')):
                    phrase_counter[phrase] += 1
        
        # Get phrases that appear at least min_count times
        recurring = {phrase: count for phrase, count in phrase_counter.items() if count >= min_count}
        
        return {
            'phrases': recurring,
            'top_phrases': sorted(recurring.items(), key=lambda x: x[1], reverse=True)[:10],
            'total_recurring': len(recurring)
        }
    
    def _detect_anomalies(self, comments: List[str]) -> Dict[str, Any]:
        """Detect anomalous patterns or outliers"""
        anomalies = {
            'very_short': [],
            'very_long': [],
            'all_caps': [],
            'excessive_punctuation': [],
            'potential_spam': []
        }
        
        lengths = [len(str(c)) for c in comments if c]
        if lengths:
            mean_length = np.mean(lengths)
            std_length = np.std(lengths)
            
            for i, comment in enumerate(comments):
                if not comment:
                    continue
                    
                comment_str = str(comment)
                length = len(comment_str)
                
                # Very short comments (outliers)
                if length < mean_length - 2 * std_length and length < 10:
                    anomalies['very_short'].append((i, comment_str[:50]))
                
                # Very long comments (outliers)
                if length > mean_length + 2 * std_length:
                    anomalies['very_long'].append((i, comment_str[:100] + '...'))
                
                # All caps detection
                if comment_str.isupper() and len(comment_str) > 10:
                    anomalies['all_caps'].append((i, comment_str[:50]))
                
                # Excessive punctuation
                punct_ratio = sum(1 for c in comment_str if c in '!?.,;:') / max(length, 1)
                if punct_ratio > 0.2:
                    anomalies['excessive_punctuation'].append((i, comment_str[:50]))
                
                # Potential spam (repetitive content)
                words = comment_str.lower().split()
                if words:
                    unique_ratio = len(set(words)) / len(words)
                    if unique_ratio < 0.3 and len(words) > 5:
                        anomalies['potential_spam'].append((i, comment_str[:50]))
        
        return {
            'anomalies': {k: v[:5] for k, v in anomalies.items()},  # Limit to 5 examples each
            'anomaly_counts': {k: len(v) for k, v in anomalies.items()},
            'total_anomalies': sum(len(v) for v in anomalies.values())
        }
    
    def _detect_trends(self, comments: List[str]) -> Dict[str, Any]:
        """Detect trends in comment patterns"""
        # For demo purposes, we'll simulate trend detection
        # In production, this would analyze temporal data
        
        trends = {
            'improving_areas': [],
            'deteriorating_areas': [],
            'stable_areas': [],
            'emerging_issues': []
        }
        
        # Analyze service patterns for trends
        service_patterns = self._detect_service_patterns(comments)
        
        for issue, count in service_patterns['counts'].items():
            total = len(comments)
            percentage = (count / total * 100) if total > 0 else 0
            
            if percentage > 20:
                trends['deteriorating_areas'].append({
                    'issue': issue,
                    'severity': 'high',
                    'percentage': round(percentage, 1)
                })
            elif percentage > 10:
                trends['emerging_issues'].append({
                    'issue': issue,
                    'severity': 'medium',
                    'percentage': round(percentage, 1)
                })
            elif percentage < 5:
                trends['stable_areas'].append({
                    'issue': issue,
                    'severity': 'low',
                    'percentage': round(percentage, 1)
                })
        
        return trends
    
    def _find_correlations(self, comments: List[str]) -> Dict[str, Any]:
        """Find correlations between different pattern types"""
        correlations = []
        
        # Check correlation between service issues and emotions
        for comment in comments:
            if not comment:
                continue
                
            comment_lower = str(comment).lower()
            detected_services = []
            detected_emotions = []
            
            # Detect service patterns in this comment
            for service, patterns in self.service_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, comment_lower):
                        detected_services.append(service)
                        break
            
            # Detect emotion patterns in this comment
            for emotion, patterns in self.emotion_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, comment_lower):
                        detected_emotions.append(emotion)
                        break
            
            # Record correlations
            if detected_services and detected_emotions:
                for service in detected_services:
                    for emotion in detected_emotions:
                        correlations.append((service, emotion))
        
        # Count correlations
        correlation_counts = Counter(correlations)
        
        return {
            'service_emotion_correlations': dict(correlation_counts.most_common(10)),
            'strongest_correlation': correlation_counts.most_common(1)[0] if correlation_counts else None
        }
    
    def _generate_pattern_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a summary of all detected patterns"""
        summary = {
            'total_service_issues': sum(results['service_patterns']['counts'].values()),
            'dominant_service_issue': results['service_patterns']['top_issues'][0] if results['service_patterns']['top_issues'] else None,
            'emotional_state': results['emotion_patterns']['dominant_emotion'],
            'competitor_threat_level': 'high' if results['competitor_mentions']['total_mentions'] > 10 else 'medium' if results['competitor_mentions']['total_mentions'] > 5 else 'low',
            'peak_issue_time': results['temporal_patterns']['peak_complaint_time'],
            'issue_frequency': results['temporal_patterns']['most_common_frequency'],
            'anomaly_rate': results['anomalies']['total_anomalies'],
            'recurring_complaints': len(results['recurring_phrases']['phrases']),
            'critical_trends': len(results['trends']['deteriorating_areas']),
            'correlation_insights': results['correlations']['strongest_correlation'] if results['correlations']['strongest_correlation'] else None
        }
        
        # Generate actionable insights
        insights = []
        
        if summary['dominant_service_issue']:
            issue_name, issue_count = summary['dominant_service_issue']
            insights.append(f"Primary issue: {issue_name.replace('_', ' ')} ({issue_count} mentions)")
        
        if summary['emotional_state'] == 'frustration':
            insights.append("High customer frustration detected - immediate action required")
        
        if summary['competitor_threat_level'] == 'high':
            insights.append("Significant competitor mentions - retention risk")
        
        if summary['critical_trends'] > 0:
            insights.append(f"{summary['critical_trends']} deteriorating service areas identified")
        
        summary['key_insights'] = insights
        
        return summary
    
    def generate_pattern_report(self, patterns: Dict[str, Any]) -> str:
        """Generate a text report of detected patterns"""
        report = []
        report.append("PATTERN DETECTION REPORT")
        report.append("=" * 50)
        
        # Summary section
        summary = patterns['summary']
        report.append("\nEXECUTIVE SUMMARY")
        report.append("-" * 30)
        for insight in summary.get('key_insights', []):
            report.append(f"• {insight}")
        
        # Service patterns
        report.append("\nSERVICE ISSUE PATTERNS")
        report.append("-" * 30)
        for issue, count in patterns['service_patterns']['top_issues'][:5]:
            report.append(f"• {issue.replace('_', ' ').title()}: {count} occurrences")
        
        # Emotional patterns
        report.append("\nEMOTIONAL PATTERNS")
        report.append("-" * 30)
        for emotion, percentage in patterns['emotion_patterns']['percentages'].items():
            report.append(f"• {emotion.title()}: {percentage:.1f}%")
        
        # Competitor analysis
        report.append("\nCOMPETITOR MENTIONS")
        report.append("-" * 30)
        if patterns['competitor_mentions']['counts']:
            for competitor, count in patterns['competitor_mentions']['counts'].items():
                report.append(f"• {competitor.upper()}: {count} mentions")
        else:
            report.append("• No significant competitor mentions")
        
        # Temporal patterns
        report.append("\nTEMPORAL PATTERNS")
        report.append("-" * 30)
        if patterns['temporal_patterns']['peak_complaint_time']:
            report.append(f"• Peak complaint time: {patterns['temporal_patterns']['peak_complaint_time']}")
        if patterns['temporal_patterns']['most_common_frequency']:
            report.append(f"• Issue frequency: {patterns['temporal_patterns']['most_common_frequency']}")
        
        # Trends
        report.append("\nTRENDS")
        report.append("-" * 30)
        for area in patterns['trends']['deteriorating_areas'][:3]:
            report.append(f"• Deteriorating: {area['issue'].replace('_', ' ')} ({area['percentage']:.1f}%)")
        
        # Anomalies
        report.append("\nANOMALIES DETECTED")
        report.append("-" * 30)
        for anomaly_type, count in patterns['anomalies']['anomaly_counts'].items():
            if count > 0:
                report.append(f"• {anomaly_type.replace('_', ' ').title()}: {count}")
        
        return "\n".join(report)