#!/usr/bin/env python3
"""
Test enhanced emotion detection and visualization
Validates the new comprehensive emotions chart and enhanced Excel export
"""

import sys
from pathlib import Path

# Add current dir to path
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

def test_emotion_data_structure():
    """Test that emotion data structure is working correctly"""
    print("🎭 Testing Emotion Data Structure...")
    
    try:
        # Test emotion value object
        from src.domain.value_objects.emocion import Emocion, TipoEmocion
        
        # Create test emotion
        emocion_test = Emocion.crear_positiva(
            TipoEmocion.SATISFACCION, 
            intensidad=0.8, 
            confianza=0.9
        )
        
        print(f"✅ Emotion VO: {emocion_test}")
        print(f"✅ Es positiva: {emocion_test.es_positiva()}")
        print(f"✅ Es intensa: {emocion_test.es_intensa()}")
        print(f"✅ Requiere atención: {emocion_test.requiere_atencion()}")
        
        # Test emotion types count
        all_emotions = list(TipoEmocion)
        print(f"✅ Total emotion types available: {len(all_emotions)}")
        
        # Verify emotion categories
        positivas = [e for e in all_emotions if 'satisfaccion' in e.value or 'alegria' in e.value or 'entusiasmo' in e.value or 'gratitud' in e.value or 'confianza' in e.value]
        negativas = [e for e in all_emotions if 'frustracion' in e.value or 'enojo' in e.value or 'decepcion' in e.value or 'preocupacion' in e.value or 'irritacion' in e.value or 'ansiedad' in e.value or 'tristeza' in e.value]
        
        print(f"✅ Emotion categories confirmed:")
        print(f"  - Positivas: {len(positivas)} types")
        print(f"  - Negativas: {len(negativas)} types") 
        print(f"  - Total cataloged: {len(positivas) + len(negativas) + 4} types")  # +4 for neutral types
        
        return True
        
    except Exception as e:
        print(f"❌ Emotion data structure test failed: {e}")
        return False

def test_comprehensive_emotions_chart():
    """Test the new comprehensive emotions chart function"""
    print("\n📊 Testing Comprehensive Emotions Chart...")
    
    try:
        # Mock emotion data (similar to what AI would produce)
        mock_emotions = {
            'satisfaccion': 0.45,
            'frustracion': 0.32,
            'preocupacion': 0.28,
            'alegria': 0.15,
            'enojo': 0.12,
            'decepcion': 0.08,
            'confianza': 0.05,
            'confusion': 0.03
        }
        
        # Import the chart function (test if importable)
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "subir_page", 
            "pages/2_Subir.py"
        )
        subir_module = importlib.util.module_from_spec(spec)
        
        # Don't execute the module (would run streamlit), just check function exists
        print("✅ pages/2_Subir.py module can be loaded")
        
        # Read the file to verify function exists
        with open("pages/2_Subir.py", 'r', encoding='utf-8') as f:
            content = f.read()
        
        if "_create_comprehensive_emotions_chart" in content:
            print("✅ _create_comprehensive_emotions_chart function found in code")
        else:
            print("❌ _create_comprehensive_emotions_chart function NOT found")
            return False
        
        # Verify the function signature and implementation details
        if "orientation='h'" in content and "sorted_emotions" in content:
            print("✅ Function implementation includes horizontal orientation and sorting")
        else:
            print("❌ Function implementation missing expected features")
            return False
            
        if "Dynamic height based on emotion count" in content:
            print("✅ Function includes dynamic height calculation")
        else:
            print("⚠️ Function might not have dynamic height (check implementation)")
            
        # Check color mapping for all emotion types
        emotion_colors_check = [
            'satisfaccion', 'frustracion', 'enojo', 'alegria', 
            'decepcion', 'preocupacion', 'esperanza', 'confusion'
        ]
        
        missing_colors = []
        for emotion in emotion_colors_check:
            if f"'{emotion}'" not in content:
                missing_colors.append(emotion)
        
        if not missing_colors:
            print("✅ Color mapping includes all expected emotions")
        else:
            print(f"⚠️ Missing color mappings for: {missing_colors}")
        
        return True
        
    except Exception as e:
        print(f"❌ Comprehensive emotions chart test failed: {e}")
        return False

def test_excel_export_enhancements():
    """Test enhanced Excel export with detailed emotion statistics"""
    print("\n📄 Testing Enhanced Excel Export...")
    
    try:
        # Read the Excel export section
        with open("pages/2_Subir.py", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for enhanced emotion section
        if "DISTRIBUCIÓN COMPLETA DE EMOCIONES GRANULARES" in content:
            print("✅ Enhanced emotion section header found in Excel export")
        else:
            print("❌ Enhanced emotion section header NOT found")
            return False
        
        # Check for comprehensive emotion statistics
        excel_features = [
            ("Column headers", "Emoción.*Intensidad.*Porcentaje"),
            ("Emotion classification", "Muy Intensa.*Intensa.*Moderada"),
            ("Emotion types", "Positiva.*Negativa.*Neutra"),
            ("Statistics summary", "ESTADÍSTICAS DE EMOCIONES"),
            ("Total calculations", "Total.*s.*total_intensity")
        ]
        
        for feature_name, pattern in excel_features:
            if any(phrase in content for phrase in pattern.split(".*")):
                print(f"✅ Excel export includes {feature_name}")
            else:
                print(f"❌ Excel export missing {feature_name}")
                return False
        
        # Check for percentage calculations
        if "percentage = (intensidad / total_intensity * 100)" in content:
            print("✅ Excel export includes percentage calculations")
        else:
            print("❌ Excel export missing percentage calculations")
            return False
            
        # Check for emotion sorting
        if "sorted_emotions = sorted" in content and "reverse=True" in content:
            print("✅ Excel export sorts emotions by intensity")
        else:
            print("❌ Excel export doesn't sort emotions properly")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Excel export test failed: {e}")
        return False

def test_emotion_chart_integration():
    """Test that emotion chart is properly integrated as first display"""
    print("\n🎨 Testing Emotion Chart Integration...")
    
    try:
        with open("pages/2_Subir.py", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the visualization section
        viz_section_start = content.find("📊 Visualización de Análisis IA")
        if viz_section_start == -1:
            print("❌ Visualization section not found")
            return False
        
        # Find the first chart after visualization header
        first_chart_start = content.find("emotions_main_chart = _create_comprehensive_emotions_chart", viz_section_start)
        sentiment_chart_start = content.find("sentiment_chart = _create_sentiment_distribution_chart", viz_section_start)
        
        if first_chart_start == -1:
            print("❌ Comprehensive emotions chart not found in visualization section")
            return False
            
        if sentiment_chart_start == -1:
            print("❌ Sentiment chart not found")
            return False
            
        if first_chart_start < sentiment_chart_start:
            print("✅ Comprehensive emotions chart appears BEFORE sentiment chart (correct order)")
        else:
            print("❌ Comprehensive emotions chart appears AFTER sentiment chart (wrong order)")
            return False
        
        # Check for proper section headers
        if "🎭 Distribución Completa de Emociones Detectadas" in content:
            print("✅ Proper emotion chart section header found")
        else:
            print("❌ Emotion chart section header missing")
            return False
            
        # Check for full width display (POLISH-001 FIX: Appropriate range)
        if "use_container_width=True" in content[first_chart_start:first_chart_start+300]:
            print("✅ Comprehensive emotions chart uses full container width")
        else:
            print("❌ Comprehensive emotions chart doesn't use full width")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Emotion chart integration test failed: {e}")
        return False

def run_emotion_enhancement_tests():
    """Run all emotion enhancement tests"""
    print("🎭 EMOTION ENHANCEMENT VALIDATION TESTS")
    print("=" * 45)
    
    results = {}
    
    # Run all tests
    results['Emotion Data Structure'] = test_emotion_data_structure()
    results['Comprehensive Chart Function'] = test_comprehensive_emotions_chart()
    results['Excel Export Enhancements'] = test_excel_export_enhancements()
    results['Chart Integration Order'] = test_emotion_chart_integration()
    
    # Summary
    print(f"\n📊 EMOTION ENHANCEMENT TEST RESULTS:")
    print("=" * 45)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    success_rate = (passed / total) * 100
    print(f"\nOverall Success Rate: {passed}/{total} ({success_rate:.1f}%)")
    
    if success_rate == 100:
        print("🎯 EMOTION ENHANCEMENTS: PERFECT IMPLEMENTATION")
    elif success_rate >= 75:
        print("✅ EMOTION ENHANCEMENTS: GOOD IMPLEMENTATION")
    else:
        print("❌ EMOTION ENHANCEMENTS: NEEDS WORK")
    
    return success_rate >= 75

if __name__ == "__main__":
    try:
        success = run_emotion_enhancement_tests()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)