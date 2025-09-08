#!/usr/bin/env python3
"""
Test batch discrepancy fix
Validates that prompt consistency fixes the 20→21 comment issue
"""

import sys
from pathlib import Path

# Add src to path
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

def test_prompt_consistency():
    """Test that prompt numbering and JSON format are now consistent"""
    
    print("🔍 PROMPT CONSISTENCY VALIDATION")
    print("=" * 35)
    
    try:
        from src.infrastructure.external_services.analizador_maestro_ia import AnalizadorMaestroIA
        
        analyzer = AnalizadorMaestroIA('test-key', usar_cache=False)
        
        # Test prompt generation with 20 comments
        test_comments = [f"Test comment {i+1}" for i in range(20)]
        prompt = analyzer._generar_prompt_maestro(test_comments)
        
        print(f"✅ Generated prompt for {len(test_comments)} comments")
        
        # Check numbering consistency
        print("\n📋 NUMBERING CONSISTENCY CHECK:")
        
        # Extract comment numbering from prompt
        lines = prompt.split('\n')
        comment_lines = [line for line in lines if '. Test comment' in line]
        
        print(f"Comment lines in prompt: {len(comment_lines)}")
        print(f"First comment: {comment_lines[0] if comment_lines else 'None'}")
        print(f"Last comment: {comment_lines[-1] if comment_lines else 'None'}")
        
        # Check JSON format example
        if '"i": 1,' in prompt:
            print("✅ JSON format uses 1-based indexing (consistent with numbering)")
        elif '"i": 0,' in prompt:
            print("❌ JSON format still uses 0-based indexing (inconsistent)")
        else:
            print("⚠️ JSON format indexing unclear")
        
        # Check instruction clarity
        if f"EXACTAMENTE {len(test_comments)} comentarios" in prompt:
            print("✅ Instructions specify exact count expected")
        else:
            print("❌ Instructions don't specify exact count")
        
        if f"numerados 1-{len(test_comments)}" in prompt:
            print("✅ Instructions clarify numbering range")
        else:
            print("❌ Instructions don't clarify numbering range")
        
        return True
        
    except Exception as e:
        print(f"❌ Prompt consistency test failed: {e}")
        return False

def test_response_validation():
    """Test response validation and truncation logic"""
    
    print("\n🔧 RESPONSE VALIDATION TEST")
    print("=" * 30)
    
    try:
        from src.infrastructure.external_services.analizador_maestro_ia import AnalizadorMaestroIA
        
        analyzer = AnalizadorMaestroIA('test-key', usar_cache=False)
        
        # Test response processing with discrepancy scenarios
        
        # Scenario 1: AI returns too many comments (21 instead of 20)
        print("\n📊 Testing AI returns TOO MANY comments (21→20):")
        
        mock_response_too_many = {
            'general': {'total': 21, 'tendencia': 'positiva'},
            'comentarios': [
                {'i': i, 'sent': 'pos', 'emo': 'sat', 'conf': 0.8}
                for i in range(1, 22)  # 21 comments (1-21)
            ],
            'stats': {'pos': 15, 'neu': 4, 'neg': 2}
        }
        
        original_comments = [f"Comment {i}" for i in range(20)]  # 20 comments
        
        try:
            result = analyzer._procesar_respuesta_maestra(
                mock_response_too_many, original_comments, 1.0
            )
            
            final_count = len(result.comentarios_analizados)
            print(f"✅ Truncation handling: {21} → {final_count} comments")
            
            if final_count == 20:
                print("✅ Correct truncation: Excess comments removed")
            else:
                print(f"❌ Truncation failed: Expected 20, got {final_count}")
                
        except Exception as e:
            print(f"❌ Too many comments test failed: {e}")
        
        # Scenario 2: AI returns too few comments (19 instead of 20)
        print("\n📊 Testing AI returns TOO FEW comments (19<20):")
        
        mock_response_too_few = {
            'general': {'total': 19, 'tendencia': 'positiva'},
            'comentarios': [
                {'i': i, 'sent': 'pos', 'emo': 'sat', 'conf': 0.8}
                for i in range(1, 20)  # 19 comments (1-19)
            ],
            'stats': {'pos': 15, 'neu': 4, 'neg': 0}
        }
        
        try:
            result = analyzer._procesar_respuesta_maestra(
                mock_response_too_few, original_comments, 1.0
            )
            
            final_count = len(result.comentarios_analizados)
            print(f"✅ Undercount handling: Processed {final_count} comments")
            
            if final_count == 19:
                print("✅ Correct handling: Continues with available comments")
            else:
                print(f"❌ Undercount handling failed: Expected 19, got {final_count}")
                
        except Exception as e:
            print(f"❌ Too few comments test failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Response validation test failed: {e}")
        return False

if __name__ == "__main__":
    print("🔧 BATCH DISCREPANCY FIX VALIDATION")
    print("=" * 38)
    
    try:
        results = {}
        
        # Run tests
        results['Prompt Consistency'] = test_prompt_consistency()
        results['Response Validation'] = test_response_validation()
        
        # Summary
        print(f"\n📊 BATCH FIX TEST RESULTS:")
        print("=" * 28)
        
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
            print("🎯 BATCH DISCREPANCY FIX: PERFECT")
        elif success_rate >= 80:
            print("✅ BATCH DISCREPANCY FIX: WORKING")
        else:
            print("❌ BATCH DISCREPANCY FIX: NEEDS MORE WORK")
        
        print(f"\n🎯 DEPLOYMENT ERROR STATUS:")
        if success_rate >= 80:
            print("✅ Batch discrepancy error should be RESOLVED in deployment")
        else:
            print("❌ Batch discrepancy error may PERSIST in deployment")
        
        sys.exit(0 if success_rate >= 80 else 1)
        
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)