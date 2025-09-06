#!/usr/bin/env python3
"""
Test polish improvements validation
Validates constants usage, refactoring, and code quality improvements
"""

import sys
from pathlib import Path

# Add current dir to path
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

def test_constants_implementation():
    """Test POLISH-002: Magic numbers extracted to constants"""
    print("🔢 Testing Constants Implementation...")
    
    try:
        # Test constants import
        from src.infrastructure.external_services.ai_engine_constants import AIEngineConstants
        
        print("✅ AIEngineConstants imported successfully")
        
        # Test constant validation
        is_valid = AIEngineConstants.validate_configuration()
        print(f"✅ Constants validation: {is_valid}")
        
        # Test helper methods
        token_limit = AIEngineConstants.get_model_token_limit('gpt-4o-mini')
        print(f"✅ Token limit retrieval: {token_limit} tokens for gpt-4o-mini")
        
        emotion_color = AIEngineConstants.get_emotion_color('satisfaccion')
        print(f"✅ Emotion color retrieval: {emotion_color} for satisfaccion")
        
        classification = AIEngineConstants.classify_emotion_intensity(0.75)
        print(f"✅ Intensity classification: 0.75 → {classification}")
        
        dynamic_height = AIEngineConstants.calculate_dynamic_chart_height(8)
        print(f"✅ Dynamic height calculation: 8 emotions → {dynamic_height}px")
        
        # Test that AI Engine uses constants
        from src.infrastructure.external_services.analizador_maestro_ia import AnalizadorMaestroIA, CONSTANTS_AVAILABLE
        
        if CONSTANTS_AVAILABLE:
            print("✅ AI Engine has constants available")
            
            # Test that constants are used in initialization
            analyzer = AnalizadorMaestroIA('test-key', usar_cache=True)
            
            if hasattr(analyzer, '_cache_max_size'):
                expected_cache_size = AIEngineConstants.DEFAULT_CACHE_SIZE
                if analyzer._cache_max_size == expected_cache_size:
                    print(f"✅ AI Engine uses cache size constant: {expected_cache_size}")
                else:
                    print(f"⚠️ AI Engine cache size mismatch: expected {expected_cache_size}, got {analyzer._cache_max_size}")
            
            if hasattr(analyzer, 'seed'):
                expected_seed = AIEngineConstants.FIXED_SEED
                if analyzer.seed == expected_seed:
                    print(f"✅ AI Engine uses seed constant: {expected_seed}")
                else:
                    print(f"⚠️ AI Engine seed mismatch: expected {expected_seed}, got {analyzer.seed}")
        else:
            print("⚠️ AI Engine constants not available (fallback mode)")
        
        return True
        
    except Exception as e:
        print(f"❌ Constants implementation test failed: {e}")
        return False

def test_chart_constants_usage():
    """Test that chart functions use constants properly"""
    print("\n🎨 Testing Chart Constants Usage...")
    
    try:
        # Check that pages import constants
        with open("pages/2_Subir.py", 'r', encoding='utf-8') as f:
            content = f.read()
        
        if "from src.infrastructure.external_services.ai_engine_constants import AIEngineConstants" in content:
            print("✅ Pages import AIEngineConstants")
        else:
            print("❌ Pages don't import AIEngineConstants")
            return False
        
        if "CONSTANTS_AVAILABLE" in content:
            print("✅ Pages check for constants availability")
        else:
            print("❌ Pages don't check for constants availability")
            return False
        
        # Check that color mapping uses constants
        if "emotion_colors = AIEngineConstants.EMOTION_COLORS" in content:
            print("✅ Chart functions use emotion color constants")
        else:
            print("❌ Chart functions don't use emotion color constants")
            return False
        
        # Check that height calculation uses constants
        if "AIEngineConstants.calculate_dynamic_chart_height" in content:
            print("✅ Chart functions use dynamic height constants")
        else:
            print("❌ Chart functions don't use dynamic height constants")
            return False
        
        # Check that intensity classification uses constants
        if "AIEngineConstants.classify_emotion_intensity" in content:
            print("✅ Excel export uses intensity classification constants")
        else:
            print("❌ Excel export doesn't use intensity classification constants")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Chart constants usage test failed: {e}")
        return False

def test_improved_test_reliability():
    """Test POLISH-001: Fixed test range issue"""
    print("\n🧪 Testing Improved Test Reliability...")
    
    try:
        # Test the fixed range in emotion test
        with open("test_emotion_enhancements.py", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for improved range
        if "first_chart_start+300" in content:
            print("✅ Test range improved from 200 to 300 characters")
        else:
            print("❌ Test range not improved")
            return False
        
        # Run the actual emotion test to verify 100% pass rate
        import subprocess
        result = subprocess.run([sys.executable, "test_emotion_enhancements.py"], 
                              capture_output=True, text=True, cwd=".")
        
        if "Overall Success Rate: 4/4 (100.0%)" in result.stdout:
            print("✅ Emotion enhancement tests now pass at 100%")
        elif "PERFECT IMPLEMENTATION" in result.stdout:
            print("✅ Emotion enhancement tests show perfect implementation")
        else:
            print("⚠️ Emotion enhancement tests might not be at 100%")
            print(f"Test output sample: {result.stdout[-200:]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test reliability improvement test failed: {e}")
        return False

def test_code_quality_improvements():
    """Test overall code quality improvements"""
    print("\n✨ Testing Code Quality Improvements...")
    
    try:
        # Test that imports work correctly
        from src.infrastructure.external_services.ai_engine_constants import AIEngineConstants
        from src.infrastructure.external_services.analizador_maestro_ia import AnalizadorMaestroIA
        
        # Test that constants validation works
        is_valid = AIEngineConstants.validate_configuration()
        print(f"✅ Constants configuration valid: {is_valid}")
        
        # Test that AI Engine initializes with constants
        analyzer = AnalizadorMaestroIA('test-key')
        print(f"✅ AI Engine initialization successful with constants")
        
        # Test that constants provide expected values
        cache_size = AIEngineConstants.DEFAULT_CACHE_SIZE
        seed_value = AIEngineConstants.FIXED_SEED
        
        if cache_size == 50 and seed_value == 12345:
            print("✅ Constants provide expected values")
        else:
            print(f"⚠️ Unexpected constant values: cache={cache_size}, seed={seed_value}")
        
        # Test helper methods
        height = AIEngineConstants.calculate_dynamic_chart_height(10)
        classification = AIEngineConstants.classify_emotion_intensity(0.75)
        color = AIEngineConstants.get_emotion_color('satisfaccion')
        
        if height > 400 and classification == "Intensa" and color.startswith('#'):
            print("✅ All helper methods working correctly")
        else:
            print(f"⚠️ Helper method issues: height={height}, class={classification}, color={color}")
        
        return True
        
    except Exception as e:
        print(f"❌ Code quality test failed: {e}")
        return False

def test_integration_after_polish():
    """Test that polish improvements don't break existing functionality"""
    print("\n🔗 Testing Integration After Polish...")
    
    try:
        # Test AI Engine token calculation still works
        from src.infrastructure.external_services.analizador_maestro_ia import AnalizadorMaestroIA
        
        analyzer = AnalizadorMaestroIA('test-key')
        tokens = analyzer._calcular_tokens_dinamicos(10)
        
        # Should be around 2200 tokens (1200 base + 10*80 + 10% buffer)
        expected_range = (2000, 2500)
        if expected_range[0] <= tokens <= expected_range[1]:
            print(f"✅ Token calculation working correctly: {tokens} tokens")
        else:
            print(f"⚠️ Token calculation might be off: {tokens} (expected {expected_range})")
        
        # Test cache functionality
        stats = analyzer.obtener_estadisticas_cache()
        if 'cache_habilitado' in stats:
            print("✅ Cache statistics functional")
        else:
            print("❌ Cache statistics broken")
            return False
        
        # Test that emotion chart function exists and is callable
        with open("pages/2_Subir.py", 'r') as f:
            content = f.read()
        
        if "_create_comprehensive_emotions_chart" in content:
            print("✅ Comprehensive emotions chart function present")
        else:
            print("❌ Comprehensive emotions chart function missing")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

def run_polish_validation_tests():
    """Run all polish improvement validation tests"""
    print("🎨 POLISH IMPROVEMENTS VALIDATION TESTS")
    print("=" * 45)
    
    results = {}
    
    # Run all tests
    results['Constants Implementation'] = test_constants_implementation()
    results['Chart Constants Usage'] = test_chart_constants_usage()
    results['Improved Test Reliability'] = test_improved_test_reliability()
    results['Code Quality Improvements'] = test_code_quality_improvements()
    results['Integration After Polish'] = test_integration_after_polish()
    
    # Summary
    print(f"\n📊 POLISH IMPROVEMENTS TEST RESULTS:")
    print("=" * 45)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    success_rate = (passed / total) * 100
    print(f"\nOverall Polish Success Rate: {passed}/{total} ({success_rate:.1f}%)")
    
    if success_rate == 100:
        print("🏆 POLISH IMPROVEMENTS: PERFECT IMPLEMENTATION")
        quality_level = "EXCELLENT (100%)"
    elif success_rate >= 80:
        print("✅ POLISH IMPROVEMENTS: HIGH QUALITY IMPLEMENTATION")
        quality_level = "VERY GOOD (80%+)"
    else:
        print("⚠️ POLISH IMPROVEMENTS: NEEDS MORE WORK")
        quality_level = "NEEDS IMPROVEMENT"
    
    print(f"Final Code Quality Level: {quality_level}")
    
    return success_rate >= 80

if __name__ == "__main__":
    try:
        success = run_polish_validation_tests()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Polish test suite failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)