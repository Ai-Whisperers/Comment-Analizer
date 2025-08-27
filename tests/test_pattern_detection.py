"""
Test suite for pattern detection functionality
"""

import pytest
from pathlib import Path

# Import from installed package
# Install with: pip install -e .
from src.pattern_detection.pattern_detector import PatternDetector


class TestPatternDetector:
    """Test suite for PatternDetector class"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test fixtures"""
        self.detector = PatternDetector()
    
    def test_detect_service_patterns(self, pattern_detection_comments):
        """Test detection of service-related patterns"""
        patterns = self.detector.detect_patterns(pattern_detection_comments)
        
        assert 'service_patterns' in patterns
        assert 'counts' in patterns['service_patterns']
        assert 'examples' in patterns['service_patterns']
        assert 'top_issues' in patterns['service_patterns']
        
        # Should detect connection issues
        assert any('connection' in str(issue).lower() or 'technical' in str(issue).lower() 
                  for issue in patterns['service_patterns']['counts'].keys())
    
    def test_detect_emotion_patterns(self):
        """Test detection of emotional patterns"""
        emotional_comments = [
            "Estoy muy frustrado con el servicio",
            "Urgente necesito que lo arreglen",
            "Excelente, estoy muy satisfecho",
            "Harto de los problemas constantes"
        ]
        
        patterns = self.detector.detect_patterns(emotional_comments)
        
        assert 'emotion_patterns' in patterns
        assert 'counts' in patterns['emotion_patterns']
        assert 'percentages' in patterns['emotion_patterns']
        assert 'dominant_emotion' in patterns['emotion_patterns']
        
        # Should detect frustration
        assert patterns['emotion_patterns']['counts'].get('frustration', 0) > 0
    
    def test_detect_competitor_mentions(self):
        """Test detection of competitor mentions"""
        competitor_comments = [
            "Voy a cambiar a Tigo",
            "Claro tiene mejor servicio",
            "Pensando en volver a Copaco",
            "He escuchado que Vox es bueno"
        ]
        
        patterns = self.detector.detect_patterns(competitor_comments)
        
        assert 'competitor_mentions' in patterns
        assert 'counts' in patterns['competitor_mentions']
        assert 'total_mentions' in patterns['competitor_mentions']
        assert patterns['competitor_mentions']['total_mentions'] >= 4
    
    def test_detect_temporal_patterns(self):
        """Test detection of temporal patterns"""
        temporal_comments = [
            "Falla todas las mañanas",
            "Por la noche no funciona",
            "Todos los días el mismo problema",
            "Ocasionalmente se corta"
        ]
        
        patterns = self.detector.detect_patterns(temporal_comments)
        
        assert 'temporal_patterns' in patterns
        assert 'time_of_day' in patterns['temporal_patterns']
        assert 'frequency' in patterns['temporal_patterns']
        
        # Should detect daily frequency
        assert patterns['temporal_patterns']['frequency'].get('daily', 0) > 0
    
    def test_find_recurring_phrases(self):
        """Test finding recurring phrases"""
        comments_with_recurring = [
            "no funciona el internet",
            "no funciona el internet",
            "no funciona el internet",
            "el servicio es malo",
            "el servicio es malo"
        ]
        
        patterns = self.detector.detect_patterns(comments_with_recurring)
        
        assert 'recurring_phrases' in patterns
        assert 'phrases' in patterns['recurring_phrases']
        assert 'top_phrases' in patterns['recurring_phrases']
        assert len(patterns['recurring_phrases']['phrases']) > 0
    
    def test_detect_anomalies(self):
        """Test detection of anomalous comments"""
        anomalous_comments = [
            "ok",  # Very short
            "a" * 1000,  # Very long
            "TERRIBLE SERVICIO!!!",  # All caps
            "!!!???...",  # Excessive punctuation
            "spam spam spam spam spam"  # Repetitive
        ]
        
        patterns = self.detector.detect_patterns(anomalous_comments)
        
        assert 'anomalies' in patterns
        assert 'anomaly_counts' in patterns['anomalies']
        assert 'total_anomalies' in patterns['anomalies']
        assert patterns['anomalies']['total_anomalies'] > 0
    
    def test_detect_trends(self):
        """Test trend detection"""
        trending_comments = [
            "Internet lento" for _ in range(30)
        ] + ["Buen servicio" for _ in range(5)]
        
        patterns = self.detector.detect_patterns(trending_comments)
        
        assert 'trends' in patterns
        assert any(key in patterns['trends'] for key in 
                  ['improving_areas', 'deteriorating_areas', 'stable_areas', 'emerging_issues'])
    
    def test_find_correlations(self):
        """Test finding correlations between patterns"""
        correlated_comments = [
            "Internet lento y estoy frustrado",
            "Se corta mucho, muy molesto",
            "No funciona, necesito cancelar",
            "Precio alto y mal servicio"
        ]
        
        patterns = self.detector.detect_patterns(correlated_comments)
        
        assert 'correlations' in patterns
        assert 'service_emotion_correlations' in patterns['correlations']
    
    def test_generate_summary(self):
        """Test pattern summary generation"""
        test_comments = [
            "Servicio pésimo",
            "Internet lento",
            "Cambiar a Tigo",
            "Urgente arreglar"
        ]
        
        patterns = self.detector.detect_patterns(test_comments)
        
        assert 'summary' in patterns
        assert 'total_service_issues' in patterns['summary']
        assert 'emotional_state' in patterns['summary']
        assert 'competitor_threat_level' in patterns['summary']
        assert 'key_insights' in patterns['summary']
    
    def test_generate_report(self, pattern_detection_comments):
        """Test report generation"""
        patterns = self.detector.detect_patterns(pattern_detection_comments)
        report = self.detector.generate_pattern_report(patterns)
        
        assert isinstance(report, str)
        assert "PATTERN DETECTION REPORT" in report
        assert "EXECUTIVE SUMMARY" in report
        assert "SERVICE ISSUE PATTERNS" in report
    
    def test_empty_comments_handling(self):
        """Test handling of empty comment list"""
        patterns = self.detector.detect_patterns([])
        
        assert patterns is not None
        assert 'summary' in patterns
        assert patterns['summary']['total_service_issues'] == 0
    
    def test_none_comments_handling(self):
        """Test handling of None values in comments"""
        comments_with_none = ["Good service", None, "", "Bad service", None]
        patterns = self.detector.detect_patterns(comments_with_none)
        
        assert patterns is not None
        assert 'summary' in patterns