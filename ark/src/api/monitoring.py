"""
Monitoring and Logging Module
Tracks system usage, performance metrics, and generates usage reports
"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging
from src.config import Config

# Set up logging
logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL))
logger = logging.getLogger(__name__)

class SystemMonitor:
    """Class to handle system monitoring and usage tracking"""
    
    def __init__(self):
        self.monitor_dir = Path("data") / "monitoring"
        self.monitor_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.monitor_dir / "usage_metrics.db"
        self._init_database()
    
    def _init_database(self):
        """Initialize SQLite database for usage tracking"""
        with sqlite3.connect(self.db_path) as conn:
            # Usage sessions table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS usage_sessions (
                    session_id TEXT PRIMARY KEY,
                    start_time TIMESTAMP,
                    end_time TIMESTAMP,
                    user_agent TEXT,
                    total_comments_analyzed INTEGER DEFAULT 0,
                    api_calls_made INTEGER DEFAULT 0,
                    cache_hits INTEGER DEFAULT 0,
                    errors_encountered INTEGER DEFAULT 0,
                    export_count INTEGER DEFAULT 0
                )
            """)
            
            # API calls table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS api_calls (
                    call_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    timestamp TIMESTAMP,
                    api_type TEXT,
                    comments_count INTEGER,
                    success BOOLEAN,
                    response_time_ms INTEGER,
                    error_message TEXT,
                    tokens_used INTEGER,
                    estimated_cost REAL,
                    FOREIGN KEY (session_id) REFERENCES usage_sessions (session_id)
                )
            """)
            
            # Analysis results table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS analysis_results (
                    result_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    timestamp TIMESTAMP,
                    comments_analyzed INTEGER,
                    positive_sentiment_pct REAL,
                    negative_sentiment_pct REAL,
                    neutral_sentiment_pct REAL,
                    guarani_content_pct REAL,
                    avg_confidence REAL,
                    top_themes TEXT,  -- JSON string
                    top_pain_points TEXT,  -- JSON string
                    FOREIGN KEY (session_id) REFERENCES usage_sessions (session_id)
                )
            """)
            
            # System performance table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS system_performance (
                    perf_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP,
                    session_id TEXT,
                    operation_type TEXT,
                    duration_seconds REAL,
                    memory_usage_mb REAL,
                    success BOOLEAN,
                    error_details TEXT
                )
            """)
            
            conn.commit()
    
    def start_session(self, user_agent: str = "Unknown") -> str:
        """Start a new usage session and return session ID"""
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(user_agent) % 10000}"
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO usage_sessions 
                    (session_id, start_time, user_agent)
                    VALUES (?, ?, ?)
                """, (session_id, datetime.now(), user_agent))
                conn.commit()
                
            logger.info(f"Started monitoring session: {session_id}")
            return session_id
            
        except Exception as e:
            logger.error(f"Error starting session: {e}")
            return f"fallback_session_{datetime.now().timestamp()}"
    
    def end_session(self, session_id: str):
        """End a usage session"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    UPDATE usage_sessions 
                    SET end_time = ? 
                    WHERE session_id = ?
                """, (datetime.now(), session_id))
                conn.commit()
                
            logger.info(f"Ended monitoring session: {session_id}")
            
        except Exception as e:
            logger.error(f"Error ending session: {e}")
    
    def log_api_call(self, session_id: str, api_type: str, comments_count: int, 
                     success: bool, response_time_ms: int, error_message: str = None,
                     tokens_used: int = 0, estimated_cost: float = 0.0):
        """Log an API call"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO api_calls 
                    (session_id, timestamp, api_type, comments_count, success, 
                     response_time_ms, error_message, tokens_used, estimated_cost)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (session_id, datetime.now(), api_type, comments_count, success,
                      response_time_ms, error_message, tokens_used, estimated_cost))
                
                # Update session totals
                conn.execute("""
                    UPDATE usage_sessions 
                    SET api_calls_made = api_calls_made + 1,
                        total_comments_analyzed = total_comments_analyzed + ?,
                        errors_encountered = errors_encountered + ?
                    WHERE session_id = ?
                """, (comments_count, 0 if success else 1, session_id))
                
                conn.commit()
                
        except Exception as e:
            logger.error(f"Error logging API call: {e}")
    
    def log_analysis_result(self, session_id: str, insights: Dict):
        """Log analysis results and insights"""
        try:
            sentiment_dist = insights.get('sentiment_percentages', {})
            
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO analysis_results 
                    (session_id, timestamp, comments_analyzed, positive_sentiment_pct,
                     negative_sentiment_pct, neutral_sentiment_pct, guarani_content_pct,
                     avg_confidence, top_themes, top_pain_points)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    session_id,
                    datetime.now(),
                    insights.get('total_comments', 0),
                    sentiment_dist.get('positive', 0),
                    sentiment_dist.get('negative', 0),
                    sentiment_dist.get('neutral', 0),
                    insights.get('guarani_percentage', 0),
                    insights.get('avg_confidence', 0),
                    json.dumps(insights.get('top_themes', {})),
                    json.dumps(insights.get('top_pain_points', {}))
                ))
                conn.commit()
                
        except Exception as e:
            logger.error(f"Error logging analysis result: {e}")
    
    def log_cache_hit(self, session_id: str):
        """Log a cache hit event"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    UPDATE usage_sessions 
                    SET cache_hits = cache_hits + 1
                    WHERE session_id = ?
                """, (session_id,))
                conn.commit()
                
        except Exception as e:
            logger.error(f"Error logging cache hit: {e}")
    
    def log_export_event(self, session_id: str, export_type: str):
        """Log an export event"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    UPDATE usage_sessions 
                    SET export_count = export_count + 1
                    WHERE session_id = ?
                """, (session_id,))
                conn.commit()
                
        except Exception as e:
            logger.error(f"Error logging export event: {e}")
    
    def get_usage_stats(self, days: int = 30) -> Dict[str, Any]:
        """Get usage statistics for the last N days"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            with sqlite3.connect(self.db_path) as conn:
                # Session statistics
                session_stats = conn.execute("""
                    SELECT 
                        COUNT(*) as total_sessions,
                        SUM(total_comments_analyzed) as total_comments,
                        SUM(api_calls_made) as total_api_calls,
                        SUM(cache_hits) as total_cache_hits,
                        SUM(errors_encountered) as total_errors,
                        SUM(export_count) as total_exports,
                        AVG(total_comments_analyzed) as avg_comments_per_session
                    FROM usage_sessions 
                    WHERE start_time >= ?
                """, (cutoff_date,)).fetchone()
                
                # API call statistics
                api_stats = conn.execute("""
                    SELECT 
                        COUNT(*) as total_calls,
                        AVG(response_time_ms) as avg_response_time,
                        SUM(estimated_cost) as total_estimated_cost,
                        COUNT(CASE WHEN success = 1 THEN 1 END) as successful_calls,
                        COUNT(CASE WHEN success = 0 THEN 1 END) as failed_calls
                    FROM api_calls 
                    WHERE timestamp >= ?
                """, (cutoff_date,)).fetchone()
                
                # Recent sentiment trends
                sentiment_trends = conn.execute("""
                    SELECT 
                        AVG(positive_sentiment_pct) as avg_positive,
                        AVG(negative_sentiment_pct) as avg_negative,
                        AVG(neutral_sentiment_pct) as avg_neutral,
                        AVG(guarani_content_pct) as avg_guarani
                    FROM analysis_results 
                    WHERE timestamp >= ?
                """, (cutoff_date,)).fetchone()
                
                return {
                    "period_days": days,
                    "session_stats": {
                        "total_sessions": session_stats[0] or 0,
                        "total_comments_analyzed": session_stats[1] or 0,
                        "total_api_calls": session_stats[2] or 0,
                        "total_cache_hits": session_stats[3] or 0,
                        "total_errors": session_stats[4] or 0,
                        "total_exports": session_stats[5] or 0,
                        "avg_comments_per_session": round(session_stats[6] or 0, 1)
                    },
                    "api_stats": {
                        "total_calls": api_stats[0] or 0,
                        "avg_response_time_ms": round(api_stats[1] or 0, 1),
                        "total_estimated_cost": round(api_stats[2] or 0, 4),
                        "successful_calls": api_stats[3] or 0,
                        "failed_calls": api_stats[4] or 0,
                        "success_rate": round((api_stats[3] or 0) / max(api_stats[0] or 1, 1) * 100, 1)
                    },
                    "sentiment_trends": {
                        "avg_positive_pct": round(sentiment_trends[0] or 0, 1),
                        "avg_negative_pct": round(sentiment_trends[1] or 0, 1),
                        "avg_neutral_pct": round(sentiment_trends[2] or 0, 1),
                        "avg_guarani_pct": round(sentiment_trends[3] or 0, 1)
                    }
                }
                
        except Exception as e:
            logger.error(f"Error getting usage stats: {e}")
            return {"error": str(e)}
    
    def get_recent_sessions(self, limit: int = 10) -> List[Dict]:
        """Get recent session information"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT session_id, start_time, end_time, total_comments_analyzed,
                           api_calls_made, cache_hits, errors_encountered, export_count
                    FROM usage_sessions 
                    ORDER BY start_time DESC 
                    LIMIT ?
                """, (limit,))
                
                sessions = []
                for row in cursor.fetchall():
                    sessions.append({
                        "session_id": row[0],
                        "start_time": row[1],
                        "end_time": row[2],
                        "total_comments_analyzed": row[3],
                        "api_calls_made": row[4],
                        "cache_hits": row[5],
                        "errors_encountered": row[6],
                        "export_count": row[7]
                    })
                
                return sessions
                
        except Exception as e:
            logger.error(f"Error getting recent sessions: {e}")
            return []
    
    def cleanup_old_data(self, days_to_keep: int = 90) -> int:
        """Clean up old monitoring data"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            
            with sqlite3.connect(self.db_path) as conn:
                # Get count of sessions to be deleted
                old_sessions = conn.execute("""
                    SELECT COUNT(*) FROM usage_sessions WHERE start_time < ?
                """, (cutoff_date,)).fetchone()[0]
                
                # Delete old data (cascading deletes)
                conn.execute("DELETE FROM usage_sessions WHERE start_time < ?", (cutoff_date,))
                conn.execute("DELETE FROM api_calls WHERE timestamp < ?", (cutoff_date,))
                conn.execute("DELETE FROM analysis_results WHERE timestamp < ?", (cutoff_date,))
                conn.execute("DELETE FROM system_performance WHERE timestamp < ?", (cutoff_date,))
                
                conn.commit()
                
                logger.info(f"Cleaned up {old_sessions} old sessions")
                return old_sessions
                
        except Exception as e:
            logger.error(f"Error cleaning up old data: {e}")
            return 0

# Global monitor instance
_monitor_instance = None

def get_monitor() -> SystemMonitor:
    """Get global monitor instance"""
    global _monitor_instance
    if _monitor_instance is None:
        _monitor_instance = SystemMonitor()
    return _monitor_instance

# Example usage and testing
if __name__ == "__main__":
    # Test monitoring functionality
    monitor = SystemMonitor()
    
    # Test session
    session_id = monitor.start_session("Test User Agent")
    
    # Simulate some API calls
    monitor.log_api_call(session_id, "openai", 10, True, 1500, None, 500, 0.02)
    monitor.log_api_call(session_id, "openai", 5, True, 800, None, 250, 0.01)
    
    # Simulate cache hit
    monitor.log_cache_hit(session_id)
    
    # Simulate analysis result
    test_insights = {
        "total_comments": 15,
        "sentiment_percentages": {"positive": 60, "negative": 25, "neutral": 15},
        "guarani_percentage": 8.5,
        "avg_confidence": 0.85,
        "top_themes": {"velocidad": 5, "instalacion": 3},
        "top_pain_points": {"demora": 2}
    }
    monitor.log_analysis_result(session_id, test_insights)
    
    # End session
    monitor.end_session(session_id)
    
    # Get stats
    stats = monitor.get_usage_stats(7)
    print("Usage Statistics:")
    print(json.dumps(stats, indent=2, default=str))
    
    # Get recent sessions
    recent = monitor.get_recent_sessions(5)
    print(f"\nRecent Sessions: {len(recent)}")
    for session in recent:
        print(f"  {session['session_id']}: {session['total_comments_analyzed']} comments")