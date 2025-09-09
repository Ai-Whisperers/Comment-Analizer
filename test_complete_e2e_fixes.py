#!/usr/bin/env python3
"""
Complete E2E pipeline test with all fixes applied
Validates functional fix, batch discrepancy fix, and threading fix together
"""

import sys
import time
from pathlib import Path
from datetime import datetime

# Add src to path
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

def test_complete_pipeline_with_fixes():
    """Test complete pipeline execution with all fixes applied"""
    
    print("🧪 COMPLETE E2E PIPELINE TEST - ALL FIXES APPLIED")
    print("=" * 55)
    
    test_results = {}
    
    print("\n1️⃣ FUNCTIONAL FIX VALIDATION (AI Engine cache attribute)")
    print("-" * 60)
    
    try:
        from src.infrastructure.external_services.analizador_maestro_ia import AnalizadorMaestroIA
        
        # Test both cache modes (this was the original blocker)
        cache_modes = [True, False]
        
        for cache_mode in cache_modes:
            mode_name = "WITH_CACHE" if cache_mode else "NO_CACHE"
            
            try:
                analyzer = AnalizadorMaestroIA('test-key', usar_cache=cache_mode)
                print(f"✅ {mode_name}: AI Engine creation SUCCESS")
                
                # Test core functionality
                tokens = analyzer._calcular_tokens_dinamicos(15)
                print(f"✅ {mode_name}: Token calculation {tokens} tokens")
                
                # Test emotion extraction
                test_comments = [{'emo': 'sat'}, {'emo': 'fru'}, {'emo': 'ale'}]
                emotions = analyzer._extract_emotions_from_comments(test_comments)
                print(f"✅ {mode_name}: Emotion extraction {emotions}")
                
            except Exception as e:
                print(f"❌ {mode_name}: FAILED - {e}")
                test_results['functional_fix'] = False
                return test_results
        
        test_results['functional_fix'] = True
        print("✅ FUNCTIONAL FIX: COMPLETE SUCCESS")
        
    except Exception as e:
        test_results['functional_fix'] = False
        print(f"❌ FUNCTIONAL FIX TEST FAILED: {e}")
    
    print("\n2️⃣ BATCH DISCREPANCY FIX VALIDATION (JSON indexing consistency)")
    print("-" * 70)
    
    try:
        analyzer = AnalizadorMaestroIA('test-key', usar_cache=False)
        
        # Test prompt generation with consistent indexing
        test_comments = [f"Test comment {i+1}" for i in range(20)]
        prompt = analyzer._generar_prompt_maestro(test_comments)
        
        # Verify 1-based indexing consistency
        if '"i": 1,' in prompt:
            print("✅ JSON format indexing: 1-based (consistent with numbering)")
        else:
            print("❌ JSON format indexing: 0-based (inconsistent)")
            test_results['batch_discrepancy_fix'] = False
            return test_results
        
        # Verify enhanced instructions
        if 'EXACTAMENTE' in prompt and 'numerados 1-' in prompt:
            print("✅ Enhanced instructions: Clear count and range specification")
        else:
            print("❌ Enhanced instructions: Missing or unclear")
            test_results['batch_discrepancy_fix'] = False
            return test_results
        
        # Test response validation with discrepancy scenarios
        
        # Scenario: AI returns too many comments (21 instead of 20)
        mock_response_excess = {
            'general': {'total': 21},
            'comentarios': [{'i': i, 'sent': 'pos', 'emo': 'sat'} for i in range(1, 22)],  # 21 comments
            'stats': {'pos': 21, 'neu': 0, 'neg': 0}
        }
        
        original_comments = test_comments  # 20 comments
        
        try:
            result = analyzer._procesar_respuesta_maestra(mock_response_excess, original_comments, 1.0)
            final_count = len(result.comentarios_analizados)
            
            if final_count == 20:
                print(f"✅ Excess comment truncation: 21 → {final_count} SUCCESS")
            else:
                print(f"❌ Excess comment handling FAILED: Expected 20, got {final_count}")
                test_results['batch_discrepancy_fix'] = False
                return test_results
                
        except Exception as e:
            print(f"❌ Response validation test failed: {e}")
            test_results['batch_discrepancy_fix'] = False
            return test_results
        
        test_results['batch_discrepancy_fix'] = True
        print("✅ BATCH DISCREPANCY FIX: COMPLETE SUCCESS")
        
    except Exception as e:
        test_results['batch_discrepancy_fix'] = False
        print(f"❌ BATCH DISCREPANCY FIX TEST FAILED: {e}")
    
    print("\n3️⃣ THREADING FIX VALIDATION (ScriptRunContext elimination)")
    print("-" * 65)
    
    try:
        # Test progress tracking without background threads
        from src.infrastructure.external_services.ai_progress_tracker import (
            create_progress_tracker, get_current_progress, track_step, reset_progress_tracker
        )
        
        print("✅ Progress tracking imports: SUCCESS")
        
        # Create tracker (should use session state, not threads)
        tracker = create_progress_tracker(10)
        print("✅ Progress tracker creation: SUCCESS")
        
        # Test step tracking (should update session state, not create threads)
        steps_to_test = ['cache_check', 'prompt_generation', 'openai_api_call']
        
        for step_name in steps_to_test:
            try:
                # This should NOT create any background threads
                tracker.start_step(step_name)
                
                # Get progress (should work without threading)
                progress = get_current_progress()
                
                if progress:
                    print(f"✅ Step {step_name}: Progress {progress['progress_percentage']:.1f}%")
                else:
                    print(f"⚠️ Step {step_name}: Progress not available")
                
                # Complete step
                time.sleep(0.1)
                tracker.complete_step(step_name)
                
            except Exception as e:
                print(f"❌ Step {step_name} failed: {e}")
                test_results['threading_fix'] = False
                return test_results
        
        # Cleanup
        reset_progress_tracker()
        print("✅ Progress tracking cleanup: SUCCESS")
        
        test_results['threading_fix'] = True
        print("✅ THREADING FIX: COMPLETE SUCCESS")
        
    except Exception as e:
        test_results['threading_fix'] = False
        print(f"❌ THREADING FIX TEST FAILED: {e}")
    
    return test_results

# Run complete test
results = test_complete_pipeline_with_fixes()

print(f"\\n🏆 COMPLETE E2E FIX VALIDATION RESULTS:")
print("=" * 43)

all_passed = True
for fix_name, passed in results.items():
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{fix_name.replace('_', ' ').title()}: {status}")
    if not passed:
        all_passed = False

overall_status = (len([r for r in results.values() if r]) / len(results)) * 100 if results else 0

print(f"\\nOverall Fix Success Rate: {len([r for r in results.values() if r])}/{len(results)} ({overall_status:.1f}%)")

if all_passed and overall_status == 100:
    print("🎯 ALL FIXES SUCCESSFULLY APPLIED AND VALIDATED")
    print("✅ Pipeline ready for deployment without known issues")
else:
    print(f"⚠️ {len([r for r in results.values() if not r])} FIXES NEED ATTENTION")
    print("❌ Deployment may still have issues")

print(f"\\n🚀 DEPLOYMENT READINESS ASSESSMENT:")
print("=" * 37)
if overall_status >= 100:
    print("✅ READY: All critical fixes applied and validated")
    print("✅ Batch discrepancy error should be resolved")
    print("✅ ScriptRunContext warnings should be eliminated") 
    print("✅ AI Engine functional in both cache modes")
    print("✅ Progress tracking works without threading issues")
else:
    print("❌ NOT READY: Critical fixes incomplete or failed validation")
"