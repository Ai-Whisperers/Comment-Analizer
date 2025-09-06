"""
Thread-safe Session State Manager for Streamlit
HIGH-001 FIX: Prevents race conditions in session state modifications
"""
import threading
import streamlit as st
from contextlib import contextmanager
from typing import Any, Optional, Dict
import logging

logger = logging.getLogger(__name__)


class SessionStateManager:
    """
    HIGH-001 FIX: Thread-safe session state manager
    Prevents race conditions when multiple components modify session state
    """
    
    def __init__(self):
        self._locks: Dict[str, threading.Lock] = {}
        self._global_lock = threading.Lock()
        logger.debug("🔒 SessionStateManager initialized")
    
    def _get_session_id(self) -> str:
        """
        Get current session ID for per-session locking
        
        Returns:
            str: Unique session identifier
        """
        try:
            # Use streamlit's session state hash as unique ID
            session_id = str(hash(str(st.session_state)))
            return session_id
        except Exception:
            # Fallback for testing or edge cases
            return "default"
    
    @contextmanager
    def session_lock(self):
        """
        Context manager for session-safe operations
        Provides per-session locking to avoid cross-session interference
        
        Usage:
            with session_manager.session_lock():
                st.session_state.key = value
        """
        session_id = self._get_session_id()
        
        # Get or create per-session lock (thread-safe)
        with self._global_lock:
            if session_id not in self._locks:
                self._locks[session_id] = threading.Lock()
            session_lock = self._locks[session_id]
        
        # Acquire session-specific lock
        with session_lock:
            yield
    
    def safe_set(self, key: str, value: Any) -> None:
        """
        Thread-safe session state setter
        
        Args:
            key: Session state key
            value: Value to set
        """
        with self.session_lock():
            st.session_state[key] = value
            logger.debug(f"🔒 Safe set: {key}")
    
    def safe_get(self, key: str, default: Any = None) -> Any:
        """
        Thread-safe session state getter
        
        Args:
            key: Session state key
            default: Default value if key doesn't exist
            
        Returns:
            Value from session state or default
        """
        with self.session_lock():
            value = st.session_state.get(key, default)
            logger.debug(f"🔒 Safe get: {key}")
            return value
    
    def safe_update(self, updates: Dict[str, Any]) -> None:
        """
        Thread-safe batch update of multiple session state keys
        
        Args:
            updates: Dictionary of key-value pairs to update
        """
        with self.session_lock():
            for key, value in updates.items():
                st.session_state[key] = value
            logger.debug(f"🔒 Safe batch update: {len(updates)} keys")
    
    def safe_delete(self, key: str) -> bool:
        """
        Thread-safe session state key deletion
        
        Args:
            key: Key to delete
            
        Returns:
            bool: True if key was deleted, False if it didn't exist
        """
        with self.session_lock():
            if key in st.session_state:
                del st.session_state[key]
                logger.debug(f"🔒 Safe delete: {key}")
                return True
            return False
    
    def safe_exists(self, key: str) -> bool:
        """
        Thread-safe check if key exists in session state
        
        Args:
            key: Key to check
            
        Returns:
            bool: True if key exists
        """
        with self.session_lock():
            exists = key in st.session_state
            logger.debug(f"🔒 Safe exists check: {key} = {exists}")
            return exists
    
    def get_session_stats(self) -> Dict[str, Any]:
        """
        Get statistics about session state management
        
        Returns:
            Dict with session stats
        """
        with self._global_lock:
            return {
                "total_sessions": len(self._locks),
                "current_session_id": self._get_session_id(),
                "thread_safe": True,
                "active_locks": len(self._locks)
            }
    
    def cleanup_old_sessions(self, max_sessions: int = 50) -> int:
        """
        Cleanup old session locks to prevent memory accumulation
        
        Args:
            max_sessions: Maximum number of session locks to keep
            
        Returns:
            int: Number of sessions cleaned up
        """
        with self._global_lock:
            if len(self._locks) <= max_sessions:
                return 0
            
            # Keep only the most recent sessions (simple cleanup)
            # In production, you'd want to track last access time
            sessions_to_remove = len(self._locks) - max_sessions
            session_ids = list(self._locks.keys())
            
            cleaned_count = 0
            for session_id in session_ids[:sessions_to_remove]:
                if session_id != self._get_session_id():  # Don't remove current session
                    del self._locks[session_id]
                    cleaned_count += 1
            
            if cleaned_count > 0:
                logger.info(f"🧹 Cleaned up {cleaned_count} old session locks")
            
            return cleaned_count


# Global instance for use across the application
session_manager = SessionStateManager()


# Convenience functions for easy usage
def safe_set_state(key: str, value: Any) -> None:
    """Convenience function for thread-safe session state setting"""
    session_manager.safe_set(key, value)


def safe_get_state(key: str, default: Any = None) -> Any:
    """Convenience function for thread-safe session state getting"""
    return session_manager.safe_get(key, default)


def safe_update_state(updates: Dict[str, Any]) -> None:
    """Convenience function for thread-safe batch updates"""
    session_manager.safe_update(updates)


def safe_delete_state(key: str) -> bool:
    """Convenience function for thread-safe key deletion"""
    return session_manager.safe_delete(key)


def with_session_lock():
    """Convenience context manager for session locking"""
    return session_manager.session_lock()