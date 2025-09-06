#!/usr/bin/env python3
"""
Quick test to validate CRITICAL-002 thread safety fix
Tests that dependency injection container is thread-safe with concurrent access
"""

import sys
import threading
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add src to path
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

try:
    from src.infrastructure.dependency_injection.contenedor_dependencias import ContenedorDependencias
    print("✅ Successfully imported ContenedorDependencias")
except ImportError as e:
    print(f"❌ Failed to import ContenedorDependencias: {e}")
    sys.exit(1)

def test_concurrent_singleton_creation():
    """Test that singleton creation is thread-safe"""
    print("\n🧪 Testing concurrent singleton creation...")
    
    # Test configuration
    config = {
        'openai_api_key': 'test-key',
        'openai_modelo': 'gpt-4',
        'openai_temperatura': 0.0,
        'openai_max_tokens': 1000,
        'max_comments': 20,
        'cache_ttl': 3600
    }
    
    container = ContenedorDependencias(config)
    
    # Counters for thread safety validation
    creation_counter = {'count': 0}
    creation_lock = threading.Lock()
    results = {}
    
    def create_singleton_worker(worker_id: int) -> str:
        """Worker function that creates singleton instances"""
        try:
            # Try to get repository (should create singleton)
            repo = container.obtener_repositorio_comentarios()
            
            # Track that we got an instance
            with creation_lock:
                creation_counter['count'] += 1
            
            # Store result with instance ID to check if same instance
            instance_id = id(repo)
            results[worker_id] = instance_id
            
            return f"Worker {worker_id}: Got instance {instance_id}"
        except Exception as e:
            return f"Worker {worker_id}: Error - {str(e)}"
    
    # Run multiple threads concurrently
    num_workers = 10
    print(f"🏃 Running {num_workers} concurrent workers...")
    
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(create_singleton_worker, i) for i in range(num_workers)]
        
        worker_results = []
        for future in as_completed(futures):
            try:
                result = future.result()
                worker_results.append(result)
            except Exception as e:
                worker_results.append(f"Future error: {e}")
    
    # Analyze results
    print(f"\nResults:")
    for result in worker_results:
        print(f"  {result}")
    
    print(f"\nSingleton creation stats:")
    print(f"  Total creations attempted: {creation_counter['count']}")
    print(f"  Unique instance IDs: {len(set(results.values()))}")
    
    # Get container stats
    stats = container.get_singleton_stats()
    print(f"  Container singletons: {stats['total_singletons']}")
    print(f"  Container keys: {stats['singleton_keys']}")
    print(f"  Thread safe: {stats['thread_safe']}")
    
    # Validation
    unique_instances = set(results.values())
    if len(unique_instances) == 1:
        print("✅ PASS: All workers got the same singleton instance")
    else:
        print(f"❌ FAIL: Workers got {len(unique_instances)} different instances")
        
    if stats['total_singletons'] >= 1:
        print("✅ PASS: Container correctly maintains singleton instances")
    else:
        print("❌ FAIL: Container doesn't have expected singletons")

def test_cleanup_functionality():
    """Test that cleanup works correctly"""
    print("\n🧪 Testing cleanup functionality...")
    
    config = {
        'openai_api_key': 'test-key',
        'openai_modelo': 'gpt-4',
        'openai_temperatura': 0.0,
        'openai_max_tokens': 1000,
        'max_comments': 20,
        'cache_ttl': 3600
    }
    
    container = ContenedorDependencias(config)
    
    # Create some singletons
    repo = container.obtener_repositorio_comentarios()
    lector = container.obtener_lector_archivos()
    
    stats_before = container.get_singleton_stats()
    print(f"Before cleanup: {stats_before['total_singletons']} singletons")
    
    # Test cleanup
    container.cleanup_singletons()
    
    stats_after = container.get_singleton_stats()
    print(f"After cleanup: {stats_after['total_singletons']} singletons")
    
    if stats_after['total_singletons'] == 0:
        print("✅ PASS: Cleanup successfully cleared all singletons")
    else:
        print("❌ FAIL: Cleanup didn't clear all singletons")

def test_thread_safety_stress():
    """Stress test with rapid concurrent access"""
    print("\n🧪 Stress testing thread safety...")
    
    config = {
        'openai_api_key': 'test-key',
        'openai_modelo': 'gpt-4',
        'openai_temperatura': 0.0,
        'openai_max_tokens': 1000,
        'max_comments': 20,
        'cache_ttl': 3600
    }
    
    container = ContenedorDependencias(config)
    
    def stress_worker(worker_id: int) -> bool:
        """Worker that rapidly accesses different singletons"""
        try:
            for _ in range(50):  # 50 rapid accesses
                repo = container.obtener_repositorio_comentarios()
                lector = container.obtener_lector_archivos()
                # Small delay to increase chance of contention
                time.sleep(0.001)
            return True
        except Exception as e:
            print(f"Stress worker {worker_id} failed: {e}")
            return False
    
    # Run stress test
    num_workers = 20
    success_count = 0
    
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(stress_worker, i) for i in range(num_workers)]
        
        for future in as_completed(futures):
            if future.result():
                success_count += 1
    
    print(f"Stress test results: {success_count}/{num_workers} workers succeeded")
    
    if success_count == num_workers:
        print("✅ PASS: All stress test workers completed successfully")
    else:
        print(f"❌ FAIL: {num_workers - success_count} workers failed")

if __name__ == "__main__":
    print("🔍 CRITICAL-002 Thread Safety Fix Validation Test")
    print("=" * 50)
    
    try:
        test_concurrent_singleton_creation()
        test_cleanup_functionality()
        test_thread_safety_stress()
        print("\n✅ All thread safety tests completed!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()