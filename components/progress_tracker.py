"""
Progress Tracking Component - Streamlit Fragment-Based
Non-blocking progress updates using Streamlit's fragment system
"""

import streamlit as st
import time
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


@st.fragment
def show_batch_progress(total_batches: int, current_batch: int, 
                       elapsed_time: float) -> None:
    """
    Non-blocking progress display using Streamlit fragments
    
    Fragment Benefits:
    - Updates independently without triggering full app reruns  
    - Responsive UI during long operations
    - Real-time progress without blocking other components
    """
    if total_batches <= 0:
        return
        
    progress_pct = (current_batch / total_batches) * 100
    remaining_batches = total_batches - current_batch
    avg_time_per_batch = elapsed_time / max(current_batch, 1)
    eta = avg_time_per_batch * remaining_batches
    
    # Progress bar with real-time updates
    st.progress(
        progress_pct / 100, 
        text=f"Progreso: {progress_pct:.1f}% completado"
    )
    
    # Detailed status that updates without full app rerun
    st.info(f"""
📊 **Progreso:** {progress_pct:.1f}% completado  
⏱️ **Tiempo transcurrido:** {elapsed_time:.1f}s  
🔮 **Tiempo estimado restante:** {eta:.1f}s  
📈 **Etapa actual:** Procesando lote {current_batch}/{total_batches}  
📦 **Lotes optimizados:** {total_batches} (vs {current_batch * 20//50} with old system)
""")


@st.fragment(run_every=1)
def auto_update_analysis_progress() -> None:
    """
    Auto-updating progress display that refreshes every second
    Uses Streamlit's auto-refresh fragment capability
    """
    if 'analysis_progress' in st.session_state:
        progress_data = st.session_state.analysis_progress
        show_batch_progress(
            progress_data.get('total_batches', 0),
            progress_data.get('current_batch', 0), 
            progress_data.get('elapsed_time', 0)
        )


def start_progress_tracking(total_batches: int) -> None:
    """
    Initialize progress tracking in session state
    Simple session state usage following Streamlit best practices
    """
    st.session_state.analysis_progress = {
        'total_batches': total_batches,
        'current_batch': 0,
        'start_time': time.time(),
        'elapsed_time': 0,
        'status': 'iniciando'
    }
    logger.info(f"📊 Progress tracking initialized for {total_batches} batches")


def update_progress(current_batch: int, status: str = 'procesando') -> None:
    """
    Update progress in session state for fragment display
    Lightweight update that triggers fragment refresh only
    """
    if 'analysis_progress' in st.session_state:
        start_time = st.session_state.analysis_progress['start_time']
        st.session_state.analysis_progress.update({
            'current_batch': current_batch,
            'elapsed_time': time.time() - start_time,
            'status': status
        })


def finish_progress_tracking() -> Dict[str, Any]:
    """
    Complete progress tracking and return final metrics
    """
    if 'analysis_progress' not in st.session_state:
        return {}
    
    progress_data = st.session_state.analysis_progress
    total_time = time.time() - progress_data['start_time']
    
    final_metrics = {
        'total_time': total_time,
        'total_batches': progress_data['total_batches'],
        'avg_time_per_batch': total_time / progress_data['total_batches'] if progress_data['total_batches'] > 0 else 0,
        'completed_at': time.time()
    }
    
    # Clear progress data
    if 'analysis_progress' in st.session_state:
        del st.session_state.analysis_progress
    
    logger.info(f"✅ Progress tracking completed: {total_time:.2f}s total")
    return final_metrics


@st.fragment(run_every=1)
def show_ai_analysis_progress() -> None:
    """
    Show detailed AI analysis progress with real-time updates
    Displays progress from AI pipeline tracker (not batch tracker)
    """
    try:
        # Get AI progress data from session state (set by ai_progress_tracker)
        if hasattr(st.session_state, '_ai_progress_data'):
            progress_data = st.session_state._ai_progress_data
            
            # Show detailed AI progress
            progress_pct = progress_data.get('progress_percentage', 0)
            current_step = progress_data.get('current_step', {})
            elapsed = progress_data.get('elapsed_time', 0)
            eta = progress_data.get('estimated_remaining', 0)
            
            # Progress bar
            st.progress(
                progress_pct / 100, 
                text=f"Análisis IA: {progress_pct:.1f}% - {current_step.get('description', 'Procesando...')}"
            )
            
            # Detailed info
            stage = progress_data.get('pipeline_stage', 'Iniciando...')
            completed_steps = progress_data.get('completed_steps', 0)
            total_steps = progress_data.get('total_steps', 6)
            
            st.info(f"""
🤖 **{stage}**  
📊 **Progreso:** {progress_pct:.1f}% ({completed_steps}/{total_steps} pasos)  
⏱️ **Tiempo:** {elapsed:.1f}s transcurridos, ~{eta:.1f}s restantes  
🎯 **Paso actual:** {current_step.get('description', 'Preparando...')}
""")
            
        # Also check for AI progress tracker directly
        elif hasattr(st.session_state, '_ai_progress_tracker'):
            tracker = st.session_state._ai_progress_tracker
            if tracker:
                progress_data = tracker.get_current_progress()
                if progress_data:
                    # Same display logic as above
                    progress_pct = progress_data.get('progress_percentage', 0)
                    stage = progress_data.get('pipeline_stage', 'Iniciando...')
                    
                    st.progress(progress_pct / 100, text=f"Análisis IA: {progress_pct:.1f}%")
                    st.info(f"🤖 **{stage}**")
                    
    except Exception as e:
        logger.warning(f"Error showing AI progress: {e}")


@st.fragment  
def show_performance_comparison(current_time: float, estimated_old_time: float) -> None:
    """
    Show performance improvement comparison using fragments
    Non-blocking display of optimization benefits
    """
    improvement_pct = ((estimated_old_time - current_time) / estimated_old_time) * 100
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Tiempo Actual", f"{current_time:.1f}s", 
                 delta=f"-{estimated_old_time - current_time:.1f}s")
    
    with col2:
        st.metric("Tiempo Anterior", f"{estimated_old_time:.1f}s")
        
    with col3:
        st.metric("Mejora", f"{improvement_pct:.1f}%",
                 delta=f"{improvement_pct:.1f}% más rápido")
    
    if improvement_pct > 50:
        st.success(f"🚀 Optimización exitosa: {improvement_pct:.1f}% más rápido!")
    elif improvement_pct > 25:
        st.info(f"📈 Buena mejora: {improvement_pct:.1f}% más rápido")
    else:
        st.warning(f"⚠️ Mejora mínima: {improvement_pct:.1f}%")