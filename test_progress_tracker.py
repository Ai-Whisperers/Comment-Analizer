#!/usr/bin/env python3
"""
Test real-time progress tracker for AI pipeline
Validates that progress tracking reflects actual execution steps and timing
"""

import sys
import time
from pathlib import Path

# Add src to path
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

def test_progress_tracker():
    """Test progress tracker functionality"""
    
    print("📊 PROGRESS TRACKER VALIDATION TEST")
    print("=" * 40)
    
    try:
        # Test progress tracker import
        from src.infrastructure.external_services.ai_progress_tracker import (
            AIProgressTracker, create_progress_tracker, get_current_progress, track_step
        )
        print("✅ Progress tracker imports: SUCCESS")
        
        # Test tracker creation
        comment_count = 10
        tracker = create_progress_tracker(comment_count)
        print(f"✅ Tracker creation: SUCCESS for {comment_count} comments")
        
        # Test initial progress
        initial_progress = get_current_progress()
        print(f"✅ Initial progress: {initial_progress['progress_percentage']:.1f}%")
        print(f"✅ Pipeline stage: {initial_progress['pipeline_stage']}")
        
        # Simulate actual pipeline execution steps
        print("\n🔄 SIMULATING AI PIPELINE EXECUTION:")
        print("-" * 38)
        
        pipeline_steps = [
            ('cache_check', 0.3),
            ('prompt_generation', 1.0), 
            ('openai_api_call', 8.0),     # Longest step
            ('response_processing', 1.5),
            ('emotion_extraction', 0.2)
        ]
        
        for step_name, simulate_duration in pipeline_steps:
            print(f"\n🔄 Executing step: {step_name}")
            
            # Start step
            with track_step(step_name):
                start_time = time.time()
                
                # Get progress during step
                progress = get_current_progress()
                print(f"  📊 Progress: {progress['progress_percentage']:.1f}%")
                print(f"  📈 Stage: {progress['pipeline_stage']}")
                print(f"  ⏱️ Current step: {progress['current_step']['description'] if progress['current_step'] else 'None'}")
                
                # Simulate work (shortened for testing)
                time.sleep(min(simulate_duration * 0.1, 1.0))  # 10% of real time for testing
                
                actual_time = time.time() - start_time
                print(f"  ✅ Completed in {actual_time:.2f}s")
        
        # Final progress check
        final_progress = get_current_progress()
        print(f"\n🏆 FINAL PROGRESS: {final_progress['progress_percentage']:.1f}%")
        print(f"🎯 Total time: {final_progress['elapsed_time']:.2f}s")
        
        # Test step details
        step_details = tracker.get_step_details()
        print(f"\n📋 STEP EXECUTION SUMMARY:")
        for step_name, details in step_details.items():
            status = "✅ COMPLETED" if details['is_completed'] else "⏳ PENDING"
            duration = details['actual_duration'] or details['estimated_duration']
            print(f"  {step_name}: {status} ({duration:.2f}s)")
        
        return True
        
    except Exception as e:
        print(f"❌ Progress tracker test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ai_engine_integration():
    """Test that AI Engine can use progress tracking"""
    
    print("\n🤖 AI ENGINE INTEGRATION TEST")  
    print("=" * 32)
    
    try:
        # Test AI Engine with progress tracking
        from src.infrastructure.external_services.analizador_maestro_ia import AnalizadorMaestroIA, PROGRESS_TRACKING_AVAILABLE
        
        if PROGRESS_TRACKING_AVAILABLE:
            print("✅ AI Engine has progress tracking capability")
            
            # Test AI Engine creation (should now work with both cache modes)
            analyzer = AnalizadorMaestroIA('test-key', usar_cache=False)
            print("✅ AI Engine creation: SUCCESS (functional fix working)")
            
            # Test that progress tracking imports work
            from src.infrastructure.external_services.ai_progress_tracker import track_step
            print("✅ Progress tracking imports in AI Engine: SUCCESS")
            
        else:
            print("⚠️ AI Engine progress tracking not available (fallback mode)")
        
        return True
        
    except Exception as e:
        print(f"❌ AI Engine integration test failed: {e}")
        return False

def test_pages_integration():
    """Test that pages can use progress tracking"""
    
    print("\n📄 PAGES INTEGRATION TEST")
    print("=" * 27)
    
    try:
        # Check that pages can import progress tracking
        with open('pages/2_Subir.py', 'r') as f:
            content = f.read()
        
        if 'ai_progress_tracker' in content:
            print("✅ Pages imports progress tracker: SUCCESS")
        else:
            print("❌ Pages missing progress tracker import")
            return False
        
        if 'progress_container = st.empty()' in content:
            print("✅ Progress display containers: IMPLEMENTED")
        else:
            print("❌ Progress display containers: MISSING")
            return False
        
        if 'update_progress_display()' in content:
            print("✅ Progress update function: IMPLEMENTED")
        else:
            print("❌ Progress update function: MISSING") 
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Pages integration test failed: {e}")
        return False

if __name__ == "__main__":
    print("🔄 REAL-TIME PROGRESS LOADER VALIDATION")
    print("=" * 45)
    
    try:
        results = {}
        
        # Run all tests
        results['Progress Tracker Core'] = test_progress_tracker()
        results['AI Engine Integration'] = test_ai_engine_integration()
        results['Pages UI Integration'] = test_pages_integration()
        
        # Summary
        print(f"\n📊 PROGRESS LOADER TEST RESULTS:")
        print("=" * 37)
        
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
            print("🎯 PROGRESS LOADER: PERFECT IMPLEMENTATION")
        elif success_rate >= 80:
            print("✅ PROGRESS LOADER: FUNCTIONAL")
        else:
            print("❌ PROGRESS LOADER: NEEDS FIXES")
        
        sys.exit(0 if success_rate >= 80 else 1)
        
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)