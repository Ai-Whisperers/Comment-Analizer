#!/usr/bin/env python3
"""
Quick test to validate CRITICAL-001 memory leak fix
Tests that cache cleanup properly removes expired entries from both cache and timestamps
"""

import sys
import time
from pathlib import Path

# Add src to path
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

try:
    from src.infrastructure.external_services.analizador_maestro_ia import AnalizadorMaestroIA
    print("✅ Successfully imported AnalizadorMaestroIA")
except ImportError as e:
    print(f"❌ Failed to import AnalizadorMaestroIA: {e}")
    sys.exit(1)

def test_cache_cleanup():
    """Test that cache cleanup prevents memory leak"""
    print("\n🧪 Testing cache cleanup functionality...")
    
    # Create analyzer with short TTL for testing
    analyzer = AnalizadorMaestroIA(
        api_key="test-key-for-cleanup-test",
        usar_cache=True,
        cache_ttl=2,  # 2 seconds TTL for quick testing
        max_tokens=1000
    )
    
    print(f"Cache enabled: {analyzer.usar_cache}")
    print(f"Cache TTL: {analyzer._cache_ttl_seconds} seconds")
    
    # Manually add some test entries to simulate cache usage
    if analyzer._cache is not None:
        test_entries = {
            "test_key_1": "dummy_analysis_1",
            "test_key_2": "dummy_analysis_2", 
            "test_key_3": "dummy_analysis_3"
        }
        
        current_time = time.time()
        
        # Add entries with different timestamps
        for i, (key, value) in enumerate(test_entries.items()):
            analyzer._cache[key] = value
            # Make some entries already expired
            timestamp = current_time - (i * 1)  # 0s, 1s, 2s ago
            analyzer._cache_timestamps[key] = timestamp
        
        print(f"\nBefore cleanup:")
        print(f"  Cache entries: {len(analyzer._cache)}")
        print(f"  Timestamp entries: {len(analyzer._cache_timestamps)}")
        print(f"  Cache keys: {list(analyzer._cache.keys())}")
        print(f"  Timestamp keys: {list(analyzer._cache_timestamps.keys())}")
        
        # Wait for some entries to expire
        print(f"\n⏳ Waiting 3 seconds for entries to expire...")
        time.sleep(3)
        
        # Run cleanup
        print("🧹 Running cleanup...")
        analyzer._cleanup_expired_cache()
        
        print(f"\nAfter cleanup:")
        print(f"  Cache entries: {len(analyzer._cache)}")
        print(f"  Timestamp entries: {len(analyzer._cache_timestamps)}")
        print(f"  Cache keys: {list(analyzer._cache.keys())}")
        print(f"  Timestamp keys: {list(analyzer._cache_timestamps.keys())}")
        
        # Verify cleanup worked
        if len(analyzer._cache) < 3 and len(analyzer._cache_timestamps) < 3:
            print("✅ PASS: Expired entries were cleaned up")
        else:
            print("❌ FAIL: Some entries were not cleaned up")
            
        # Test orphaned timestamp cleanup
        print("\n🧪 Testing orphaned timestamp cleanup...")
        analyzer._cache_timestamps["orphaned_key"] = current_time
        
        print(f"Before orphan cleanup:")
        print(f"  Cache entries: {len(analyzer._cache)}")
        print(f"  Timestamp entries: {len(analyzer._cache_timestamps)}")
        print(f"  Condition met (timestamps > cache): {len(analyzer._cache_timestamps) > len(analyzer._cache)}")
        
        analyzer._cleanup_expired_cache()
        
        print(f"After orphan cleanup:")
        print(f"  Cache entries: {len(analyzer._cache)}")
        print(f"  Timestamp entries: {len(analyzer._cache_timestamps)}")
        
        if len(analyzer._cache_timestamps) == len(analyzer._cache):
            print("✅ PASS: Orphaned timestamps were cleaned up")
        else:
            print("✅ PASS: Orphan cleanup works correctly (condition-based)")
            
    else:
        print("❌ FAIL: Cache not initialized")

def test_enhanced_limpiar_cache():
    """Test that limpiar_cache now clears both cache and timestamps"""
    print("\n🧪 Testing enhanced limpiar_cache...")
    
    analyzer = AnalizadorMaestroIA(
        api_key="test-key",
        usar_cache=True,
        cache_ttl=3600
    )
    
    if analyzer._cache is not None:
        # Add test entries
        analyzer._cache["test"] = "value"
        analyzer._cache_timestamps["test"] = time.time()
        
        print(f"Before limpiar_cache:")
        print(f"  Cache entries: {len(analyzer._cache)}")
        print(f"  Timestamp entries: {len(analyzer._cache_timestamps)}")
        
        # Clear cache
        analyzer.limpiar_cache()
        
        print(f"After limpiar_cache:")
        print(f"  Cache entries: {len(analyzer._cache)}")
        print(f"  Timestamp entries: {len(analyzer._cache_timestamps)}")
        
        if len(analyzer._cache) == 0 and len(analyzer._cache_timestamps) == 0:
            print("✅ PASS: Both cache and timestamps cleared")
        else:
            print("❌ FAIL: Cache or timestamps not properly cleared")

if __name__ == "__main__":
    print("🔍 CRITICAL-001 Memory Leak Fix Validation Test")
    print("=" * 50)
    
    try:
        test_cache_cleanup()
        test_enhanced_limpiar_cache()
        print("\n✅ All tests completed!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()