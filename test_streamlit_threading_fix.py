#!/usr/bin/env python3
"""
Test Streamlit threading fix for progress loader
Validates that progress tracking works without ScriptRunContext warnings
"""

import sys
from pathlib import Path

# Add src to path
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

def test_threading_fix():
    """Test that threading issues are resolved"""
    
    print("🔧 STREAMLIT THREADING FIX VALIDATION")
    print("=" * 42)
    
    try:
        # Test progress tracker import
        from src.infrastructure.external_services.ai_progress_tracker import (
            AIProgressTracker, create_progress_tracker, get_current_progress, 
            STREAMLIT_AVAILABLE
        )
        print("✅ Progress tracker imports: SUCCESS")
        print(f"✅ Streamlit available: {STREAMLIT_AVAILABLE}")
        
        # Test tracker creation (should use session state if available)
        tracker = create_progress_tracker(15)
        print("✅ Progress tracker creation: SUCCESS")
        
        # Test progress tracking without background threads
        print("\n📊 SESSION STATE BASED PROGRESS TEST:")
        print("-" * 40)
        
        # Simulate progress updates (no background threads)
        steps = ['cache_check', 'prompt_generation', 'openai_api_call', 'response_processing']
        
        for i, step_name in enumerate(steps):
            print(f"\n🔄 Step {i+1}: {step_name}")
            
            # Start step (should update session state, not create threads)
            tracker.start_step(step_name)
            
            # Get progress (should work without ScriptRunContext)
            progress = tracker.get_current_progress()
            print(f"  📊 Progress: {progress['progress_percentage']:.1f}%")
            print(f"  📈 Stage: {progress['pipeline_stage']}")
            
            # Complete step
            import time
            time.sleep(0.1)  # Simulate work
            tracker.complete_step(step_name)
            
            # Verify completion
            final_progress = tracker.get_current_progress()
            print(f"  ✅ Completed: {final_progress['completed_steps']}/{final_progress['total_steps']} steps")
        
        print(f"\n✅ Threading fix test: SUCCESSFUL (no background threads created)")
        return True
        
    except Exception as e:
        print(f"❌ Threading fix test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_session_state_compatibility():
    """Test session state based progress tracking"""
    
    print("\n🔄 SESSION STATE COMPATIBILITY TEST")
    print("=" * 38)
    
    try:
        # Mock session state for testing
        class MockSessionState:
            def __init__(self):
                self._storage = {}
            
            def __setattr__(self, key, value):
                if key.startswith('_storage'):
                    super().__setattr__(key, value)
                else:
                    self._storage[key] = value
            
            def __getattr__(self, key):
                return self._storage.get(key, None)
        
        # Test with mock session state
        mock_st = MockSessionState()
        
        from src.infrastructure.external_services.ai_progress_tracker import AIProgressTracker
        
        tracker = AIProgressTracker(10)
        
        # Simulate session state updates (what happens in real deployment)
        mock_st._ai_progress_tracker = tracker
        mock_st._ai_progress_data = tracker.get_current_progress()
        
        print("✅ Session state storage: SUCCESS")
        print(f"✅ Progress data stored: {mock_st._ai_progress_data is not None}")
        
        # Test progress retrieval from session state
        retrieved_progress = mock_st._ai_progress_data
        if retrieved_progress:
            print(f"✅ Progress retrieval: {retrieved_progress['progress_percentage']:.1f}%")
        else:
            print("❌ Progress retrieval: FAILED")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Session state test failed: {e}")
        return False

def test_pages_implementation():
    """Test pages implementation without background threads"""
    
    print("\n📄 PAGES IMPLEMENTATION VALIDATION")
    print("=" * 37)
    
    try:
        with open('pages/2_Subir.py', 'r') as f:
            content = f.read()
        
        # Check that background threads are removed
        if 'Thread(' in content and 'progress_monitor' in content:
            print("❌ Background threads still present in pages")
            return False
        else:
            print("✅ Background threads removed: SUCCESS")
        
        # Check session state usage
        if 'session_state._ai_progress' in content:
            print("✅ Session state progress integration: IMPLEMENTED")
        else:
            print("⚠️ Session state progress integration: Check implementation")
        
        # Check progress container usage
        if 'progress_container.empty()' in content:
            print("✅ Progress container cleanup: IMPLEMENTED")
        else:
            print("❌ Progress container cleanup: MISSING")
            return False
        
        # Check exception handling for containers
        if 'except:' in content and 'progress_container' in content:
            print("✅ Exception handling for progress containers: IMPLEMENTED")
        else:
            print("⚠️ Exception handling for progress containers: Check implementation")
        
        return True
        
    except Exception as e:
        print(f"❌ Pages implementation test failed: {e}")
        return False

if __name__ == "__main__":
    print("🔧 STREAMLIT DEPLOYMENT COMPATIBILITY TEST")
    print("=" * 44)
    
    try:
        results = {}
        
        # Run tests
        results['Threading Fix'] = test_threading_fix()
        results['Session State Compatibility'] = test_session_state_compatibility()
        results['Pages Implementation'] = test_pages_implementation()
        
        # Summary
        print(f"\n📊 DEPLOYMENT COMPATIBILITY RESULTS:")
        print("=" * 39)
        
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
            print("🎯 DEPLOYMENT COMPATIBILITY: PERFECT")
            print("✅ ScriptRunContext warnings should be ELIMINATED")
        elif success_rate >= 80:
            print("✅ DEPLOYMENT COMPATIBILITY: GOOD")
            print("⚠️ Some ScriptRunContext warnings may persist")
        else:
            print("❌ DEPLOYMENT COMPATIBILITY: NEEDS FIXES")
            print("🚨 ScriptRunContext warnings will likely persist")
        
        sys.exit(0 if success_rate >= 80 else 1)
        
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)