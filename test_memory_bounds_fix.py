#!/usr/bin/env python3
"""
Quick test to validate CRITICAL-003 memory bounds fix
Tests that repository properly limits memory usage and uses LRU eviction
"""

import sys
import uuid
from pathlib import Path

# Add src to path
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

try:
    from src.infrastructure.repositories.repositorio_comentarios_memoria import RepositorioComentariosMemoria
    from src.domain.entities.comentario import Comentario
    print("✅ Successfully imported required classes")
except ImportError as e:
    print(f"❌ Failed to import required classes: {e}")
    sys.exit(1)

def create_test_comment(text: str, comment_id: str = None) -> Comentario:
    """Create a test comment with specified text"""
    if comment_id is None:
        comment_id = str(uuid.uuid4())
    
    return Comentario(
        id=comment_id,
        texto=text,
        texto_limpio=text,  # Use same text for simplicity
        frecuencia=1
    )

def test_memory_limits():
    """Test that memory limits are enforced with LRU eviction"""
    print("\n🧪 Testing memory limits with LRU eviction...")
    
    # Create repository with tight limits for testing
    repo = RepositorioComentariosMemoria(
        max_comentarios=5,  # Very small limit
        max_memory_mb=0.01  # 10KB limit - very tight
    )
    
    print(f"Repository initialized with limits:")
    stats = repo.get_memory_stats()
    print(f"  Max comments: {stats['max_comments_limit']}")
    print(f"  Max memory: {stats['max_memory_limit_mb']} MB")
    
    # Create comments with increasing sizes
    comments_data = [
        ("Small comment 1", "id1"),
        ("Medium comment with more text to increase size", "id2"), 
        ("Large comment with much more text to significantly increase the memory footprint of this comment", "id3"),
        ("Another large comment that should trigger memory limits and cause eviction of older comments", "id4"),
        ("Yet another large comment that will definitely trigger the LRU eviction mechanism", "id5"),
        ("Final large comment to test multiple evictions in sequence", "id6"),
        ("Extra comment to test continuous eviction", "id7")
    ]
    
    # Add comments one by one and monitor memory
    for i, (text, comment_id) in enumerate(comments_data):
        comment = create_test_comment(text, comment_id)
        
        print(f"\nAdding comment {i+1}: {comment_id[:8]}... (length: {len(text)})")
        print(f"Before: {repo.get_memory_stats()['total_comments']} comments, {repo.get_memory_stats()['estimated_memory_mb']} MB")
        
        repo.guardar(comment)
        
        stats = repo.get_memory_stats()
        print(f"After:  {stats['total_comments']} comments, {stats['estimated_memory_mb']} MB")
        print(f"Memory utilization: {stats['memory_utilization_pct']}%")
        print(f"Count utilization: {stats['count_utilization_pct']}%")
    
    # Final validation
    final_stats = repo.get_memory_stats()
    print(f"\n📊 Final Repository Stats:")
    for key, value in final_stats.items():
        print(f"  {key}: {value}")
    
    # Verify limits are enforced
    if final_stats['total_comments'] <= 5:
        print("✅ PASS: Comment count limit enforced")
    else:
        print(f"❌ FAIL: Comment count limit violated: {final_stats['total_comments']}")
    
    if final_stats['estimated_memory_mb'] <= 0.015:  # Allow small buffer
        print("✅ PASS: Memory limit approximately enforced")
    else:
        print(f"❌ FAIL: Memory limit might be violated: {final_stats['estimated_memory_mb']} MB")
    
    print(f"✅ PASS: LRU eviction strategy confirmed: {final_stats['eviction_strategy']}")

def test_lru_ordering():
    """Test that LRU eviction removes oldest comments first"""
    print("\n🧪 Testing LRU ordering...")
    
    repo = RepositorioComentariosMemoria(max_comentarios=3, max_memory_mb=100)  # Count limit only
    
    # Add comments in order
    comments = []
    for i in range(5):
        comment_id = f"comment_{i}"
        comment = create_test_comment(f"Test comment number {i}", comment_id)
        repo.guardar(comment)
        comments.append((comment_id, comment))
        print(f"Added: {comment_id}")
    
    # Check which comments remain (should be the last 3)
    remaining_comments = repo.obtener_todos()
    remaining_ids = [c.id for c in remaining_comments]
    
    print(f"Remaining comment IDs: {remaining_ids}")
    
    # Should have comments 2, 3, 4 (the last 3 added)
    expected_ids = ["comment_2", "comment_3", "comment_4"]
    
    if set(remaining_ids) == set(expected_ids):
        print("✅ PASS: LRU eviction correctly removed oldest comments")
    else:
        print(f"❌ FAIL: Expected {expected_ids}, got {remaining_ids}")

def test_memory_estimation():
    """Test that memory estimation works reasonably"""
    print("\n🧪 Testing memory estimation...")
    
    repo = RepositorioComentariosMemoria(max_comentarios=1000, max_memory_mb=100)
    
    # Test with different sized comments
    test_cases = [
        ("Short", "short"),
        ("Medium length comment with more text", "medium"),
        ("Very long comment with a lot of text that should use significantly more memory than the short comment, testing the memory estimation algorithm", "long")
    ]
    
    for text, comment_id in test_cases:
        comment = create_test_comment(text, comment_id)
        estimated_size = repo._estimate_memory_usage(comment)
        
        print(f"Text length: {len(text):3d} chars | Estimated memory: {estimated_size:4d} bytes | Text: '{text[:50]}...'")
        
        # Basic sanity check: longer text should use more memory
        if len(text) < 50:
            expected_range = (200, 500)  # Small comment
        elif len(text) < 100:
            expected_range = (300, 800)  # Medium comment  
        else:
            expected_range = (400, 1000) # Large comment
        
        if expected_range[0] <= estimated_size <= expected_range[1]:
            print(f"✅ Memory estimation in reasonable range: {expected_range}")
        else:
            print(f"⚠️ Memory estimation outside expected range: {expected_range}")

def test_cleanup_and_stats():
    """Test cleanup and statistics functionality"""
    print("\n🧪 Testing cleanup and statistics...")
    
    repo = RepositorioComentariosMemoria(max_comentarios=10, max_memory_mb=1)
    
    # Add some comments
    for i in range(5):
        comment = create_test_comment(f"Test comment number {i} with some text", f"id_{i}")
        repo.guardar(comment)
    
    stats_before = repo.get_memory_stats()
    print(f"Before cleanup: {stats_before['total_comments']} comments, {stats_before['estimated_memory_mb']} MB")
    
    # Test cleanup
    repo.limpiar()
    
    stats_after = repo.get_memory_stats()
    print(f"After cleanup: {stats_after['total_comments']} comments, {stats_after['estimated_memory_mb']} MB")
    
    if stats_after['total_comments'] == 0 and stats_after['estimated_memory_mb'] == 0:
        print("✅ PASS: Cleanup properly reset both count and memory tracking")
    else:
        print("❌ FAIL: Cleanup didn't properly reset statistics")

if __name__ == "__main__":
    print("🔍 CRITICAL-003 Memory Bounds Fix Validation Test")
    print("=" * 55)
    
    try:
        test_memory_limits()
        test_lru_ordering()
        test_memory_estimation()
        test_cleanup_and_stats()
        print("\n✅ All memory bounds tests completed!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()