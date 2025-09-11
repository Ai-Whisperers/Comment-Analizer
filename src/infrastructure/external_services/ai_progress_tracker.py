"""
Real-time AI Pipeline Progress Tracker
Tracks actual execution steps in AI analysis for accurate user feedback
"""
import time
import threading
from typing import Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class ProgressStep:
    """Represents a single step in AI pipeline execution"""
    name: str
    description: str
    weight: float  # Percentage of total execution time (0-100)
    estimated_duration: float  # Estimated seconds for this step
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    @property
    def is_started(self) -> bool:
        return self.started_at is not None
    
    @property 
    def is_completed(self) -> bool:
        return self.completed_at is not None
    
    @property
    def actual_duration(self) -> float:
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return 0.0


class AIProgressTracker:
    """
    Real-time progress tracker for AI pipeline execution
    Based on actual execution steps from analizador_maestro_ia.py analysis
    """
    
    def __init__(self, comment_count: int):
        """
        Initialize progress tracker with actual pipeline steps
        
        Args:
            comment_count: Number of comments being processed (affects timing)
        """
        self.comment_count = comment_count
        self.total_estimated_time = self._calculate_estimated_time(comment_count)
        self._lock = threading.RLock()
        
        # Define actual pipeline steps based on E2E analysis
        self.steps = {
            'initialization': ProgressStep(
                name='initialization',
                description='Inicializando análisis IA...',
                weight=2.0,  # 2% of total time
                estimated_duration=0.1
            ),
            'cache_check': ProgressStep(
                name='cache_check', 
                description='Verificando cache de análisis previos...',
                weight=3.0,  # 3% of total time
                estimated_duration=0.2
            ),
            'prompt_generation': ProgressStep(
                name='prompt_generation',
                description=f'Construyendo prompt maestro para {comment_count} comentarios...',
                weight=10.0,  # 10% of total time  
                estimated_duration=max(0.5, comment_count * 0.05)
            ),
            'openai_api_call': ProgressStep(
                name='openai_api_call',
                description='Enviando análisis a OpenAI (esto toma más tiempo)...',
                weight=75.0,  # 75% of total time - THE LONGEST STEP
                estimated_duration=max(5.0, comment_count * 0.8)
            ),
            'response_processing': ProgressStep(
                name='response_processing', 
                description='Procesando respuesta IA y extrayendo emociones...',
                weight=8.0,  # 8% of total time
                estimated_duration=max(0.5, comment_count * 0.02)
            ),
            'emotion_extraction': ProgressStep(
                name='emotion_extraction',
                description='Calculando distribución de emociones y sentimientos...',
                weight=2.0,  # 2% of total time
                estimated_duration=0.3
            )
        }
        
        self.current_step: Optional[str] = None
        self.start_time = time.time()
        self.progress_callbacks: Dict[str, Callable] = {}
        
        logger.debug(f"📊 Progress tracker initialized for {comment_count} comments")
    
    def _calculate_estimated_time(self, comment_count: int) -> float:
        """Calculate realistic estimated time based on comment count"""
        # Base time for OpenAI processing
        base_time = 5.0
        
        # Scale with comment count (more comments = longer processing)
        comment_time = comment_count * 0.8
        
        # Add overhead for other operations
        overhead_time = 2.0
        
        total_estimated = base_time + comment_time + overhead_time
        
        # Cap at reasonable maximum (even for large datasets)
        return min(total_estimated, 45.0)  # Max 45 seconds
    
    def start_step(self, step_name: str) -> None:
        """Mark a step as started with accurate timestamp"""
        with self._lock:
            if step_name in self.steps:
                self.steps[step_name].started_at = datetime.now()
                self.current_step = step_name
                
                # Log step start for debugging
                step = self.steps[step_name]
                logger.debug(f"📍 Step started: {step_name} - {step.description}")
                
                # STREAMLIT DEPLOYMENT FIX: Safe session state update with context verification
                if self._has_streamlit_context():
                    try:
                        # Store progress in session state for UI polling
                        st.session_state._ai_progress_data = self.get_current_progress()
                        st.session_state._ai_progress_update_time = datetime.now().isoformat()
                        logger.debug(f"📊 Progress updated in session state: {step_name}")
                    except Exception as e:
                        logger.debug(f"Session state progress update error (non-critical): {e}")
                
                # Trigger progress callback if registered (for non-Streamlit usage)
                if step_name in self.progress_callbacks:
                    try:
                        self.progress_callbacks[step_name](self.get_current_progress())
                    except Exception as e:
                        logger.warning(f"Progress callback error for {step_name}: {e}")
    
    def _has_streamlit_context(self) -> bool:
        """
        Safely check if we're running in a valid Streamlit context
        Prevents warnings and exceptions in development/testing environments
        """
        if not STREAMLIT_AVAILABLE:
            return False
            
        try:
            import streamlit as st
            from streamlit.runtime.scriptrunner import get_script_run_ctx
            
            # Check if we have a valid script run context
            ctx = get_script_run_ctx()
            if ctx is None:
                return False
            
            # Additional check: try to access session state
            _ = st.session_state
            return True
            
        except Exception:
            # Any exception means we don't have valid Streamlit context
            return False
    
    def complete_step(self, step_name: str) -> None:
        """Mark a step as completed with accurate timestamp"""
        with self._lock:
            if step_name in self.steps and self.steps[step_name].is_started:
                self.steps[step_name].completed_at = datetime.now()
                
                step = self.steps[step_name]
                actual_time = step.actual_duration
                logger.debug(f"✅ Step completed: {step_name} in {actual_time:.2f}s (estimated: {step.estimated_duration:.2f}s)")
                
                # STREAMLIT DEPLOYMENT FIX: Safe session state update on completion
                if self._has_streamlit_context():
                    try:
                        st.session_state._ai_progress_data = self.get_current_progress()
                        st.session_state._ai_progress_update_time = datetime.now().isoformat()
                        logger.debug(f"📊 Progress completion updated in session state: {step_name}")
                    except Exception as e:
                        logger.debug(f"Session state progress completion error (non-critical): {e}")
    
    def get_current_progress(self) -> Dict[str, Any]:
        """Get current progress information for UI display"""
        with self._lock:
            completed_weight = 0.0
            current_step_progress = 0.0
            
            # Calculate completed step weights
            for step_name, step in self.steps.items():
                if step.is_completed:
                    completed_weight += step.weight
                elif step.is_started:
                    # Estimate progress within current step based on time
                    elapsed = (datetime.now() - step.started_at).total_seconds()
                    step_progress = min(elapsed / step.estimated_duration, 1.0)
                    current_step_progress = step.weight * step_progress
                    break
            
            total_progress = completed_weight + current_step_progress
            
            # Get current step info
            current_step_info = None
            if self.current_step and self.current_step in self.steps:
                current_step_info = {
                    'name': self.current_step,
                    'description': self.steps[self.current_step].description,
                    'estimated_duration': self.steps[self.current_step].estimated_duration
                }
            
            # Calculate ETA
            elapsed_total = time.time() - self.start_time
            if total_progress > 0:
                eta_seconds = (elapsed_total * 100 / total_progress) - elapsed_total
            else:
                eta_seconds = self.total_estimated_time
            
            return {
                'progress_percentage': min(100.0, max(0.0, total_progress)),
                'current_step': current_step_info,
                'elapsed_time': elapsed_total,
                'estimated_remaining': max(0.0, eta_seconds),
                'total_steps': len(self.steps),
                'completed_steps': len([s for s in self.steps.values() if s.is_completed]),
                'comment_count': self.comment_count,
                'pipeline_stage': self._get_pipeline_stage(total_progress)
            }
    
    def _get_pipeline_stage(self, progress: float) -> str:
        """Get human-readable pipeline stage based on progress"""
        if progress < 5:
            return "Preparando análisis..."
        elif progress < 15:
            return "Generando prompt de análisis..."
        elif progress < 90:
            return "Analizando con Inteligencia Artificial..."
        elif progress < 98:
            return "Procesando resultados y extrayendo emociones..."
        else:
            return "Finalizando análisis..."
    
    def register_progress_callback(self, step_name: str, callback: Callable) -> None:
        """Register callback to be called when step starts"""
        self.progress_callbacks[step_name] = callback
    
    def get_step_details(self) -> Dict[str, Dict[str, Any]]:
        """Get detailed information about all steps"""
        with self._lock:
            return {
                step_name: {
                    'description': step.description,
                    'weight': step.weight,
                    'estimated_duration': step.estimated_duration,
                    'actual_duration': step.actual_duration,
                    'is_started': step.is_started,
                    'is_completed': step.is_completed,
                    'started_at': step.started_at.isoformat() if step.started_at else None,
                    'completed_at': step.completed_at.isoformat() if step.completed_at else None
                }
                for step_name, step in self.steps.items()
            }
    
    def reset(self) -> None:
        """Reset tracker for new analysis"""
        with self._lock:
            for step in self.steps.values():
                step.started_at = None
                step.completed_at = None
            self.current_step = None
            self.start_time = time.time()


class ProgressContext:
    """
    Context manager for automatic step tracking
    """
    
    def __init__(self, tracker: AIProgressTracker, step_name: str):
        self.tracker = tracker
        self.step_name = step_name
    
    def __enter__(self):
        self.tracker.start_step(self.step_name)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.tracker.complete_step(self.step_name)
        
        # Log any exceptions that occurred during the step
        if exc_type:
            logger.error(f"❌ Step {self.step_name} failed with {exc_type.__name__}: {exc_val}")


# STREAMLIT DEPLOYMENT FIX: Session state based tracking (no background threads)
try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False

# Global tracker instance (will be set when analysis starts)
_current_tracker: Optional[AIProgressTracker] = None
_tracker_lock = threading.RLock()

def _has_streamlit_context_global() -> bool:
    """
    Global function to safely check Streamlit context
    (Same logic as AIProgressTracker._has_streamlit_context but accessible globally)
    """
    if not STREAMLIT_AVAILABLE:
        return False
        
    try:
        import streamlit as st
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        
        # Check if we have a valid script run context
        ctx = get_script_run_ctx()
        if ctx is None:
            return False
        
        # Additional check: try to access session state
        _ = st.session_state
        return True
        
    except Exception:
        # Any exception means we don't have valid Streamlit context
        return False

def create_progress_tracker(comment_count: int) -> AIProgressTracker:
    """Create and set progress tracker (session state compatible)"""
    global _current_tracker
    with _tracker_lock:
        _current_tracker = AIProgressTracker(comment_count)
        
        # STREAMLIT DEPLOYMENT FIX: Safe session state storage with context verification
        if _has_streamlit_context_global():
            try:
                st.session_state._ai_progress_tracker = _current_tracker
                logger.debug("📊 Progress tracker stored in session state")
            except Exception:
                logger.debug("Progress tracker session state storage failed - using global fallback")
        
        return _current_tracker

def get_current_progress() -> Optional[Dict[str, Any]]:
    """Get current progress information (Streamlit deployment compatible)"""
    tracker = None
    
    # STREAMLIT DEPLOYMENT FIX: Safe session state access with context verification
    if _has_streamlit_context_global():
        try:
            tracker = getattr(st.session_state, '_ai_progress_tracker', None)
        except Exception:
            pass
    
    # Fallback to global tracker
    if not tracker:
        global _current_tracker
        with _tracker_lock:
            tracker = _current_tracker
    
    if tracker:
        return tracker.get_current_progress()
    return None


def track_step(step_name: str) -> ProgressContext:
    """Context manager for tracking a specific step"""
    global _current_tracker
    if _current_tracker:
        return ProgressContext(_current_tracker, step_name)
    else:
        # Return no-op context manager if no tracker
        class NoOpContext:
            def __enter__(self): return self
            def __exit__(self, *args): pass
        return NoOpContext()


def reset_progress_tracker() -> None:
    """Reset current tracker"""
    global _current_tracker
    with _tracker_lock:
        if _current_tracker:
            _current_tracker.reset()
        _current_tracker = None