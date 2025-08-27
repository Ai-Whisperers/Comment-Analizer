"""
Cache Manager Module
Handles caching of API responses to reduce costs and improve performance
"""

import json
import hashlib
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import logging
from src.config import Config

# Set up logging
logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL))
logger = logging.getLogger(__name__)

class CacheManager:
    """Class to handle caching of API responses"""
    
    def __init__(self, cache_duration_hours: int = 24):
        self.cache_duration = timedelta(hours=cache_duration_hours)
        self.cache_dir = Path("data") / "cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.cache_dir / "api_cache.db"
        self._init_database()
    
    def _init_database(self):
        """Initialize SQLite database for cache storage"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS api_cache (
                    cache_key TEXT PRIMARY KEY,
                    request_hash TEXT,
                    response_data TEXT,
                    created_at TIMESTAMP,
                    expires_at TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_expires_at ON api_cache(expires_at)
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_request_hash ON api_cache(request_hash)
            """)
            
            conn.commit()
    
    def _generate_cache_key(self, comments: List[str], analysis_type: str = "sentiment") -> str:
        """Generate a unique cache key for a set of comments"""
        # Create a deterministic hash of the comments
        comments_text = "|".join(sorted(comments))  # Sort for consistency
        hash_input = f"{analysis_type}:{comments_text}"
        
        # Generate SHA-256 hash
        cache_key = hashlib.sha256(hash_input.encode('utf-8')).hexdigest()
        return f"{analysis_type}_{cache_key[:16]}"  # Use first 16 chars for readability
    
    def _generate_request_hash(self, comments: List[str]) -> str:
        """Generate hash for the exact request (order matters)"""
        comments_text = "|".join(comments)  # Preserve order
        return hashlib.md5(comments_text.encode('utf-8')).hexdigest()
    
    def get_cached_analysis(self, comments: List[str], analysis_type: str = "sentiment") -> Optional[List[Dict]]:
        """Retrieve cached analysis results if available and not expired"""
        
        if not comments:
            return None
            
        cache_key = self._generate_cache_key(comments, analysis_type)
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT response_data, expires_at FROM api_cache 
                    WHERE cache_key = ? AND expires_at > ?
                """, (cache_key, datetime.now()))
                
                result = cursor.fetchone()
                
                if result:
                    response_data, expires_at = result
                    logger.info(f"Cache hit for key: {cache_key}")
                    return json.loads(response_data)
                else:
                    logger.info(f"Cache miss for key: {cache_key}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error retrieving from cache: {e}")
            return None
    
    def cache_analysis_result(self, comments: List[str], results: List[Dict], analysis_type: str = "sentiment"):
        """Store analysis results in cache"""
        
        if not comments or not results:
            return
        
        cache_key = self._generate_cache_key(comments, analysis_type)
        request_hash = self._generate_request_hash(comments)
        
        expires_at = datetime.now() + self.cache_duration
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO api_cache 
                    (cache_key, request_hash, response_data, created_at, expires_at)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    cache_key,
                    request_hash,
                    json.dumps(results, ensure_ascii=False),
                    datetime.now(),
                    expires_at
                ))
                
                conn.commit()
                logger.info(f"Cached analysis result for key: {cache_key}")
                
        except Exception as e:
            logger.error(f"Error storing in cache: {e}")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Total cached items
                total_count = conn.execute("SELECT COUNT(*) FROM api_cache").fetchone()[0]
                
                # Valid (non-expired) items
                valid_count = conn.execute("""
                    SELECT COUNT(*) FROM api_cache WHERE expires_at > ?
                """, (datetime.now(),)).fetchone()[0]
                
                # Expired items
                expired_count = total_count - valid_count
                
                # Cache size (approximate)
                cache_size = self.db_path.stat().st_size if self.db_path.exists() else 0
                
                # Oldest and newest entries
                oldest = conn.execute("""
                    SELECT MIN(created_at) FROM api_cache WHERE expires_at > ?
                """, (datetime.now(),)).fetchone()[0]
                
                newest = conn.execute("""
                    SELECT MAX(created_at) FROM api_cache WHERE expires_at > ?
                """, (datetime.now(),)).fetchone()[0]
                
                return {
                    "total_entries": total_count,
                    "valid_entries": valid_count,
                    "expired_entries": expired_count,
                    "cache_size_bytes": cache_size,
                    "cache_size_mb": round(cache_size / (1024 * 1024), 2),
                    "oldest_entry": oldest,
                    "newest_entry": newest,
                    "hit_rate_potential": f"{(valid_count / max(total_count, 1)) * 100:.1f}%"
                }
                
        except Exception as e:
            logger.error(f"Error getting cache stats: {e}")
            return {"error": str(e)}
    
    def cleanup_expired_cache(self) -> int:
        """Remove expired cache entries and return count of removed items"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Count expired entries
                expired_count = conn.execute("""
                    SELECT COUNT(*) FROM api_cache WHERE expires_at <= ?
                """, (datetime.now(),)).fetchone()[0]
                
                # Delete expired entries
                conn.execute("""
                    DELETE FROM api_cache WHERE expires_at <= ?
                """, (datetime.now(),))
                
                conn.commit()
                
                if expired_count > 0:
                    logger.info(f"Cleaned up {expired_count} expired cache entries")
                
                return expired_count
                
        except Exception as e:
            logger.error(f"Error cleaning up cache: {e}")
            return 0
    
    def clear_cache(self) -> bool:
        """Clear all cache entries"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("DELETE FROM api_cache")
                conn.commit()
                logger.info("Cache cleared successfully")
                return True
                
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
            return False
    
    def get_similar_cached_results(self, comments: List[str], similarity_threshold: float = 0.8) -> Optional[List[Dict]]:
        """Find similar cached results based on comment similarity"""
        
        # This is a simple implementation - could be enhanced with more sophisticated similarity
        if len(comments) < 3:  # Only works well for larger comment sets
            return None
        
        request_hash = self._generate_request_hash(comments)
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Look for exact hash match first
                cursor = conn.execute("""
                    SELECT response_data FROM api_cache 
                    WHERE request_hash = ? AND expires_at > ?
                """, (request_hash, datetime.now()))
                
                result = cursor.fetchone()
                
                if result:
                    logger.info(f"Found similar cached result via hash match")
                    return json.loads(result[0])
                
                return None
                
        except Exception as e:
            logger.error(f"Error finding similar cache results: {e}")
            return None

# Example usage and testing
if __name__ == "__main__":
    # Test cache functionality
    cache = CacheManager()
    
    # Test data
    test_comments = [
        "El servicio es excelente",
        "Tengo problemas con la conexión",
        "El precio está bien"
    ]
    
    test_results = [
        {"sentiment": "positive", "confidence": 0.9},
        {"sentiment": "negative", "confidence": 0.8},
        {"sentiment": "neutral", "confidence": 0.7}
    ]
    
    # Test caching
    print("Testing cache functionality...")
    
    # Cache results
    cache.cache_analysis_result(test_comments, test_results)
    
    # Retrieve from cache
    cached_results = cache.get_cached_analysis(test_comments)
    
    if cached_results:
        print("Cache test passed - results retrieved successfully")
        print(f"Cached results: {len(cached_results)} items")
    else:
        print("Cache test failed - no results retrieved")
    
    # Get stats
    stats = cache.get_cache_stats()
    print(f"\nCache Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Cleanup test
    cleaned = cache.cleanup_expired_cache()
    print(f"\nCleaned up {cleaned} expired entries")