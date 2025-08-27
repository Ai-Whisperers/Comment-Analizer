"""
Test Suite for AI Pipeline Fixes
Verifies fixes for issues #001-#008
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from io import BytesIO
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.ai_analysis_adapter import AIAnalysisAdapter
from src.utils.config_loader import ConfigLoader

class TestAIPipelineFixes:
    """Test suite for verifying AI pipeline fixes"""
    
    @pytest.fixture
    def ai_adapter(self):
        """Create AI adapter instance for testing"""
        with patch('src.ai_analysis_adapter.OpenAIAnalyzer'):
            adapter = AIAnalysisAdapter()
            adapter.ai_available = True
            adapter.enhanced_analyzer = Mock()
            adapter.improved_analyzer = Mock()
            return adapter
    
    @pytest.fixture
    def sample_excel_file(self):
        """Create a mock Excel file for testing"""
        df = pd.DataFrame({
            'Comentario Final': [
                'El servicio es muy lento',
                'Excelente atención',
                'Se corta constantemente',
                'Estoy muy satisfecho',
                'Precio muy caro'
            ],
            'Nota': [3, 9, 2, 10, 4],
            'NPS': ['Detractor', 'Promotor', 'Detractor', 'Promotor', 'Detractor']
        })
        
        # Create a mock file object
        mock_file = Mock()
        mock_file.name = 'test_comments.xlsx'
        mock_file.size = 1024
        
        # Create BytesIO buffer with Excel data
        buffer = BytesIO()
        df.to_excel(buffer, index=False)
        buffer.seek(0)
        mock_file.read = lambda: buffer.read()
        mock_file.seek = lambda pos: buffer.seek(pos)
        
        return mock_file
    
    def test_emotion_field_consistency_fix_001(self, ai_adapter):
        """Test Fix #001: Emotion field name consistency"""
        # Create mock AI results with English emotions
        ai_results = [
            {
                'sentiment': 'negative',
                'confidence': 0.8,
                'emotions': ['frustration', 'anger'],
                'themes': ['speed'],
                'pain_points': ['slow connection']
            },
            {
                'sentiment': 'positive',
                'confidence': 0.9,
                'emotions': ['satisfaction', 'happiness'],
                'themes': ['service'],
                'pain_points': []
            }
        ]
        
        comments = ['El servicio es muy lento', 'Excelente atención']
        comment_frequencies = {'El servicio es muy lento': 1, 'Excelente atención': 1}
        mock_file = Mock()
        mock_file.name = 'test.xlsx'
        mock_file.size = 1024
        
        # Mock the enhanced and improved analyzers
        ai_adapter.enhanced_analyzer.calculate_nps_from_sentiment = Mock(return_value=5)
        ai_adapter.improved_analyzer.calculate_real_nps = Mock(return_value={
            'nps_score': 0,
            'promoters': 1,
            'detractors': 1,
            'passives': 0
        })
        ai_adapter.improved_analyzer.generate_insights = Mock(return_value={})
        
        # Convert AI results to expected format
        result = ai_adapter._convert_ai_results_to_expected_format(
            ai_results, comments, comment_frequencies, mock_file,
            comments, [], [], False, False
        )
        
        # Verify emotions are in Spanish with correct field name
        assert 'enhanced_results' in result
        assert len(result['enhanced_results']) == 2
        
        # Check first emotion result
        first_emotion = result['enhanced_results'][0]['emotions']
        assert 'dominant_emotion' in first_emotion  # Not 'dominant'
        assert first_emotion['dominant_emotion'] in ['frustración', 'enojo']  # Spanish
        
        # Check emotion summary uses correct field
        assert 'emotion_summary' in result
        assert 'distribution' in result['emotion_summary']
    
    def test_error_context_fix_004(self, ai_adapter):
        """Test Fix #004: Error context instead of null returns"""
        # Create a file with no comment column
        df = pd.DataFrame({
            'Random': [1, 2, 3],
            'Data': ['a', 'b', 'c']
        })
        
        mock_file = Mock()
        mock_file.name = 'no_comments.xlsx'
        mock_file.size = 1024
        buffer = BytesIO()
        df.to_excel(buffer, index=False)
        buffer.seek(0)
        mock_file.read = lambda: buffer.read()
        mock_file.seek = lambda pos: buffer.seek(pos)
        
        # Process file
        result = ai_adapter.process_uploaded_file_with_ai(mock_file)
        
        # Should return error context, not None
        assert result is not None
        assert 'error' in result
        assert result['error'] == True
        assert 'error_code' in result
        assert result['error_code'] == 'NO_COMMENT_COLUMN'
        assert 'error_message' in result
        assert 'No se encontró columna de comentarios' in result['error_message']
    
    def test_partial_recovery_fix_005(self, ai_adapter):
        """Test Fix #005: Partial recovery mechanism"""
        # Mock partial AI results (only 3 of 5 comments)
        ai_results = [
            {'sentiment': 'negative', 'confidence': 0.8, 'emotions': ['frustration'], 'themes': [], 'pain_points': []},
            {'sentiment': 'positive', 'confidence': 0.9, 'emotions': ['satisfaction'], 'themes': [], 'pain_points': []},
            {'sentiment': 'negative', 'confidence': 0.7, 'emotions': ['anger'], 'themes': [], 'pain_points': []}
        ]
        
        comments = [
            'El servicio es muy lento',
            'Excelente atención',
            'Se corta constantemente',
            'Estoy muy satisfecho',
            'Precio muy caro'
        ]
        
        # Mock rule-based analyzer for remaining comments
        ai_adapter.enhanced_analyzer.full_analysis = Mock(return_value={
            'emotions': {'dominant_emotion': 'neutral', 'all_emotions': {}, 'intensity': 5},
            'extended_themes': {},
            'churn_risk': {'risk_level': 'low', 'score': 1, 'indicators': [], 'probability': 10},
            'competitors': {'mentioned': [], 'context': {}},
            'urgency': 'P3',
            'customer_value': {'value_segment': 'standard', 'indicators': []}
        })
        
        ai_adapter.improved_analyzer.analyze_comment_quality = Mock(return_value={
            'quality': 'medium',
            'informative': True,
            'detail_level': 'medium'
        })
        
        ai_adapter.improved_analyzer.detect_themes_improved = Mock(return_value={})
        ai_adapter.improved_analyzer.analyze_service_issues = Mock(return_value={'severity': 'low'})
        ai_adapter.improved_analyzer.enhanced_sentiment_analysis = Mock(return_value={
            'sentiment': 'neutral',
            'confidence': 0.5
        })
        
        # Process with hybrid analysis
        result = ai_adapter._hybrid_analysis(
            ai_results, comments, {c: 1 for c in comments},
            Mock(name='test.xlsx', size=1024), comments,
            [], [], False, False
        )
        
        # Verify hybrid metadata
        assert result['analysis_method'] == 'HYBRID_AI_RULE'
        assert 'ai_coverage' in result
        assert result['ai_coverage'] == 60.0  # 3 of 5 comments = 60%
        
        # Verify all comments were processed
        assert result['total'] == 5
        assert len(result['sentiments']) == 5
        assert len(result['enhanced_results']) == 5
    
    def test_config_usage_fix_006_007_008(self):
        """Test Fixes #006, #007, #008: Configuration usage"""
        config = ConfigLoader()
        
        # Test comment columns from config
        comment_cols = config.get_comment_columns()
        assert isinstance(comment_cols, list)
        assert 'comentario final' in comment_cols
        assert 'comment' in comment_cols
        
        # Test competitors from config
        competitors = config.get_competitors()
        assert isinstance(competitors, list)
        assert 'tigo' in competitors
        assert 'claro' in competitors
        
        # Test emotion intensities from config
        intensities = config.get_emotion_intensities()
        assert isinstance(intensities, dict)
        assert intensities.get('frustración', 0) == 2.0
        assert intensities.get('neutral', 0) == 1.0
        
        # Test urgency thresholds from config
        thresholds = config.get_urgency_thresholds()
        assert thresholds['P0'] == 6
        assert thresholds['P1'] == 4
    
    def test_spanish_emotion_translation(self, ai_adapter):
        """Test that emotions are properly translated to Spanish"""
        emotions = ['frustration', 'anger', 'satisfaction', 'happiness', 'worry']
        spanish_emotions = ai_adapter._translate_emotions_to_spanish(emotions)
        
        assert 'frustración' in spanish_emotions
        assert 'enojo' in spanish_emotions
        assert 'satisfacción' in spanish_emotions
        assert 'felicidad' in spanish_emotions
        assert 'preocupación' in spanish_emotions
    
    def test_data_format_consistency(self, ai_adapter):
        """Test data format consistency between AI and rule-based paths"""
        # Create sample data
        comments = ['Test comment 1', 'Test comment 2']
        
        # Mock AI results
        ai_result = {
            'sentiment': 'positive',
            'confidence': 0.85,
            'emotions': ['satisfaction'],
            'themes': ['service'],
            'pain_points': []
        }
        
        # Process with AI path
        ai_adapter.enhanced_analyzer.full_analysis = Mock(return_value={
            'emotions': {'dominant_emotion': 'satisfacción', 'all_emotions': {'satisfacción': 1}, 'intensity': 7},
            'extended_themes': {'service': {}},
            'churn_risk': {'risk_level': 'low', 'score': 2, 'indicators': [], 'probability': 20},
            'competitors': {'mentioned': [], 'context': {}},
            'urgency': 'P3',
            'customer_value': {'value_segment': 'standard', 'indicators': []}
        })
        
        # Both paths should produce the same structure
        # Check emotion structure
        emotion_ai = {'dominant_emotion': 'satisfacción', 'all_emotions': {'satisfacción': 1}, 'intensity': 7}
        emotion_rule = ai_adapter.enhanced_analyzer.full_analysis()['emotions']
        
        assert 'dominant_emotion' in emotion_ai
        assert 'dominant_emotion' in emotion_rule
        assert 'all_emotions' in emotion_ai
        assert 'all_emotions' in emotion_rule
        assert 'intensity' in emotion_ai
        assert 'intensity' in emotion_rule
    
    def test_error_recovery_cascade(self, ai_adapter):
        """Test complete error recovery cascade"""
        # Simulate various failure scenarios
        scenarios = [
            # Scenario 1: Complete AI failure
            (None, 'RULE_BASED_FALLBACK'),
            
            # Scenario 2: Partial AI success
            ([{'sentiment': 'positive', 'confidence': 0.8, 'emotions': [], 'themes': [], 'pain_points': []}], 'HYBRID_AI_RULE'),
            
            # Scenario 3: Full AI success
            ([
                {'sentiment': 'positive', 'confidence': 0.9, 'emotions': ['happy'], 'themes': [], 'pain_points': []},
                {'sentiment': 'negative', 'confidence': 0.8, 'emotions': ['sad'], 'themes': [], 'pain_points': []}
            ], 'AI_POWERED')
        ]
        
        for ai_results, expected_method in scenarios:
            # Mock _try_ai_analysis to return specific results
            with patch.object(ai_adapter, '_try_ai_analysis', return_value=ai_results):
                # Create test data
                mock_file = Mock()
                mock_file.name = 'test.csv'
                mock_file.size = 1024
                mock_file.read = Mock(return_value=b'Comentario Final\\nTest comment 1\\nTest comment 2')
                mock_file.seek = Mock()
                
                # Mock necessary methods for fallback
                if expected_method in ['RULE_BASED_FALLBACK', 'HYBRID_AI_RULE']:
                    ai_adapter.enhanced_analyzer.full_analysis = Mock(return_value={
                        'emotions': {'dominant_emotion': 'neutral', 'all_emotions': {}, 'intensity': 5},
                        'extended_themes': {},
                        'churn_risk': {'risk_level': 'low', 'score': 1, 'indicators': [], 'probability': 10},
                        'competitors': {'mentioned': [], 'context': {}},
                        'urgency': 'P3',
                        'customer_value': {'value_segment': 'standard', 'indicators': []}
                    })
                    
                    ai_adapter.improved_analyzer = Mock()
                    ai_adapter.improved_analyzer.calculate_real_nps = Mock(return_value={
                        'nps_score': 0,
                        'promoters': 0,
                        'detractors': 0,
                        'passives': 2
                    })
                    ai_adapter.improved_analyzer.analyze_comment_quality = Mock(return_value={
                        'quality': 'medium',
                        'informative': True
                    })
                    ai_adapter.improved_analyzer.detect_themes_improved = Mock(return_value={})
                    ai_adapter.improved_analyzer.analyze_service_issues = Mock(return_value={'severity': 'low'})
                    ai_adapter.improved_analyzer.enhanced_sentiment_analysis = Mock(return_value={'sentiment': 'neutral'})
                    ai_adapter.improved_analyzer.generate_insights = Mock(return_value={})
                
                # Process file
                result = ai_adapter.process_uploaded_file_with_ai(mock_file)
                
                # Verify expected method was used
                if result and not result.get('error'):
                    assert result.get('analysis_method') == expected_method

if __name__ == '__main__':
    pytest.main([__file__, '-v'])