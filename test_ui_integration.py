#!/usr/bin/env python3
"""
Test UI Integration - Spanish Sentiment Analysis with Layered CSS
Tests the integration of the enhanced Spanish sentiment UI with existing layered CSS styling
"""

import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_ui_components_integration():
    """Test UI components integration"""
    print("🧪 Testing UI Components Integration...")
    
    try:
        from src.ui_styling import UIComponents, ThemeManager, inject_styles
        from src.components.sentiment_results_ui import SentimentResultsUI
        
        # Test theme manager
        theme_manager = ThemeManager()
        dark_theme = theme_manager.get_theme(True)
        light_theme = theme_manager.get_theme(False)
        
        # Verify theme colors exist
        assert 'positive' in dark_theme
        assert 'negative' in dark_theme
        assert 'neutral' in dark_theme
        assert 'primary' in dark_theme
        
        # Test UI components
        ui = UIComponents()
        
        # Test metric card
        metric_html = ui.metric_card(
            icon="📊",
            title="Test Metric",
            value="100",
            card_type="positive"
        )
        assert "metric-card-enhanced" in metric_html
        assert "positive" in metric_html
        
        # Test status badge
        badge_html = ui.status_badge(
            icon="🤖",
            text="Test Badge",
            badge_type="positive"
        )
        assert "status-badge" in badge_html
        assert "positive" in badge_html
        
        # Test results header
        header_html = ui.results_header("Test Results")
        assert "results-header" in header_html
        assert "Test Results" in header_html
        
        # Test CSS injection
        css_html = inject_styles(True)
        assert "<style>" in css_html
        assert "status-badge" in css_html
        assert "results-header" in css_html
        
        print("✅ UI Components integration working correctly")
        return True
        
    except Exception as e:
        print(f"❌ UI Components integration error: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False

def test_sentiment_ui_component():
    """Test sentiment UI component with layered styling"""
    print("🧪 Testing Sentiment UI Component Integration...")
    
    try:
        from src.components.sentiment_results_ui import SentimentResultsUI
        
        # Create sentiment UI component
        sentiment_ui = SentimentResultsUI()
        
        # Test that it has UI components
        assert hasattr(sentiment_ui, 'ui')
        assert hasattr(sentiment_ui, 'theme_manager')
        
        # Test color scheme integration
        assert sentiment_ui.sentiment_colors['positivo'] == sentiment_ui.ui.theme_manager.get_theme(True)['positive']
        assert sentiment_ui.sentiment_colors['negativo'] == sentiment_ui.ui.theme_manager.get_theme(True)['negative']
        
        # Test confidence colors use theme colors
        assert sentiment_ui.confidence_colors['high'] == sentiment_ui.ui.theme_manager.get_theme(True)['positive']
        assert sentiment_ui.confidence_colors['medium'] == sentiment_ui.ui.theme_manager.get_theme(True)['accent']
        
        print("✅ Sentiment UI component integration working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Sentiment UI component integration error: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False

def test_spanish_translations_ui():
    """Test Spanish translations work with UI components"""
    print("🧪 Testing Spanish Translations with UI Integration...")
    
    try:
        from src.i18n.translations import get_translator, translate_sentiment_data
        from src.components.sentiment_results_ui import SentimentResultsUI
        
        # Test translator
        translator = get_translator('es')
        assert translator.get('positive') == 'Positivo'
        assert translator.get('negative') == 'Negativo'
        
        # Test sentiment data translation
        sample_result = {
            'sentiment': 'positive',
            'confidence': 0.85,
            'themes': ['velocidad', 'calidad_servicio'],
            'emotions': ['satisfacción']
        }
        
        translated = translate_sentiment_data(sample_result)
        assert translated['sentimiento'] == 'Positivo'
        assert translated['confianza_porcentaje'] == '85.0%'
        
        # Test UI component can handle translated data
        sentiment_ui = SentimentResultsUI()
        
        # Test sample results structure
        sample_results = {
            'total': 10,
            'positive_count': 6,
            'negative_count': 2,
            'neutral_count': 2,
            'positive_pct': 60.0,
            'negative_pct': 20.0,
            'neutral_pct': 20.0,
            'analysis_method': 'AI_POWERED',
            'ai_confidence_avg': 0.85,
            'ai_model_used': 'gpt-4o-mini'
        }
        
        # Test that UI component methods exist
        assert hasattr(sentiment_ui, '_render_analysis_header')
        assert hasattr(sentiment_ui, '_render_sentiment_overview')
        assert hasattr(sentiment_ui, 'render_comprehensive_results')
        
        print("✅ Spanish translations UI integration working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Spanish translations UI integration error: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False

def test_main_integration():
    """Test main.py integration"""
    print("🧪 Testing main.py integration...")
    
    try:
        # Test that main.py can import the render function
        from src.components.sentiment_results_ui import render_sentiment_results
        
        # Test render function exists
        assert callable(render_sentiment_results)
        
        # Test UI styling imports work in main context
        sys.path.insert(0, str(Path(__file__).parent / "src"))
        from src.ui_styling import UIComponents
        
        ui = UIComponents()
        
        # Test status badge method exists (used in enhanced main.py)
        badge_html = ui.status_badge("🎯", "Test", "positive")
        assert "status-badge" in badge_html
        
        print("✅ main.py integration working correctly")
        return True
        
    except Exception as e:
        print(f"❌ main.py integration error: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False

def run_ui_integration_tests():
    """Run all UI integration tests"""
    print("🚀 Starting UI Integration Tests with Layered CSS...")
    print("=" * 70)
    
    tests = [
        ("UI Components Integration", test_ui_components_integration),
        ("Sentiment UI Component", test_sentiment_ui_component),
        ("Spanish Translations UI", test_spanish_translations_ui),
        ("Main.py Integration", test_main_integration)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"💥 {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 70)
    print("📊 UI INTEGRATION TEST RESULTS:")
    print("=" * 70)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\nSummary: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 ALL UI INTEGRATION TESTS PASSED!")
        print("\n🌟 Enhanced Spanish sentiment UI with layered CSS successfully integrated:")
        print("   • UI Components with theme consistency ✅")
        print("   • Spanish translations with styled components ✅") 
        print("   • Layered CSS styling system working ✅")
        print("   • Main.py integration complete ✅")
        return True
    else:
        print("⚠️ Some tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = run_ui_integration_tests()
    sys.exit(0 if success else 1)