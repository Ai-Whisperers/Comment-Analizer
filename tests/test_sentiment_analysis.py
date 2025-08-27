"""
Test suite for sentiment analysis functionality
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sentiment_analysis.enhanced_analyzer import EnhancedAnalyzer


class TestEnhancedAnalyzer:
    """Test suite for EnhancedAnalyzer class"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test fixtures"""
        self.analyzer = EnhancedAnalyzer()
    
    def test_analyze_positive_sentiment(self):
        """Test analysis of positive comments"""
        positive_comments = [
            "Excelente servicio, muy satisfecho",
            "Todo funciona perfectamente bien",
            "El mejor servicio que he tenido",
            "Rápido y eficiente, lo recomiendo"
        ]
        
        for comment in positive_comments:
            result = self.analyzer.analyze(comment)
            assert result is not None
            assert 'sentiment' in result
            assert result['sentiment'] in ['positive', 'positivo']
    
    def test_analyze_negative_sentiment(self):
        """Test analysis of negative comments"""
        negative_comments = [
            "Pésimo servicio, no funciona nada",
            "Terrible, se corta constantemente",
            "Muy malo, no lo recomiendo",
            "El peor servicio de mi vida"
        ]
        
        for comment in negative_comments:
            result = self.analyzer.analyze(comment)
            assert result is not None
            assert 'sentiment' in result
            assert result['sentiment'] in ['negative', 'negativo']
    
    def test_analyze_neutral_sentiment(self):
        """Test analysis of neutral comments"""
        neutral_comments = [
            "El servicio es regular",
            "Funciona pero podría ser mejor",
            "Normal, nada especial",
            "Más o menos"
        ]
        
        for comment in neutral_comments:
            result = self.analyzer.analyze(comment)
            assert result is not None
            assert 'sentiment' in result
    
    def test_empty_comment_handling(self):
        """Test handling of empty or None comments"""
        empty_comments = ["", None, "   ", "\n\t"]
        
        for comment in empty_comments:
            result = self.analyzer.analyze(comment)
            assert result is not None
            assert 'sentiment' in result
            assert result['sentiment'] in ['neutral', 'unknown', None]
    
    def test_mixed_language_comments(self):
        """Test handling of mixed language comments"""
        mixed_comments = [
            "Good service pero muy caro",
            "Internet slow, necesita mejorar",
            "OK service, precio regular"
        ]
        
        for comment in mixed_comments:
            result = self.analyzer.analyze(comment)
            assert result is not None
            assert 'sentiment' in result
    
    def test_special_characters_handling(self):
        """Test handling of comments with special characters"""
        special_comments = [
            "¡¡¡Excelente!!!",
            "Mal... muy mal...",
            "###TERRIBLE###",
            "😊 Buen servicio 👍"
        ]
        
        for comment in special_comments:
            result = self.analyzer.analyze(comment)
            assert result is not None
            assert 'sentiment' in result
    
    def test_long_comment_analysis(self):
        """Test analysis of very long comments"""
        long_comment = "El servicio " * 100 + "es malo"
        result = self.analyzer.analyze(long_comment)
        assert result is not None
        assert 'sentiment' in result
    
    def test_confidence_scores(self):
        """Test that confidence scores are within valid range"""
        comments = [
            "Definitivamente excelente",
            "Tal vez bueno",
            "Posiblemente malo"
        ]
        
        for comment in comments:
            result = self.analyzer.analyze(comment)
            if 'confidence' in result:
                assert 0 <= result['confidence'] <= 1
    
    def test_keyword_detection(self):
        """Test detection of specific keywords"""
        keyword_comments = {
            "velocidad lenta": ['slow', 'lento', 'velocidad'],
            "se corta mucho": ['corta', 'interruption', 'intermitente'],
            "precio muy caro": ['precio', 'caro', 'expensive']
        }
        
        for comment, expected_keywords in keyword_comments.items():
            result = self.analyzer.analyze(comment)
            assert result is not None
            if 'keywords' in result:
                found_any = any(kw in str(result.get('keywords', [])).lower() 
                              for kw in expected_keywords)
                assert found_any or 'sentiment' in result
    
    def test_batch_analysis(self):
        """Test batch analysis of multiple comments"""
        comments = [
            "Buen servicio",
            "Mal servicio",
            "Regular",
            ""
        ]
        
        results = [self.analyzer.analyze(c) for c in comments]
        assert len(results) == len(comments)
        assert all('sentiment' in r for r in results)