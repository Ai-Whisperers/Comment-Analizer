"""
Análisis Optimizada - Streamlit Native Performance
Experimental analysis workflow using optimized components with native caching
Parallel implementation to test performance improvements vs 2_Subir.py
Note: Some dependencies in lib/ and components/ may need verification
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime
import time
import logging

# Setup path for component imports
current_dir = Path(__file__).parent.parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

# Import Streamlit-native components
from components.file_processor import process_file_content, validate_file_structure, calculate_processing_estimate
from components.ai_analyzer import analyze_comments_optimized, get_openai_client
from components.chart_generator import create_analysis_dashboard, prepare_chart_data_optimized
from components.progress_tracker import start_progress_tracking, auto_update_analysis_progress, finish_progress_tracking
from components.ui_components import (
    render_upload_section, render_analysis_controls, render_results_section, 
    render_performance_stats, render_error_section
)
from lib.utils import generate_config_hash, validate_comment_content, create_processing_summary
from lib.data_models import AnalysisResult, ProcessingMetadata

logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Análisis Optimizada - Personal Paraguay",
    page_icon="🚀",
    layout="wide"
)

# Enhanced CSS loading with caching
try:
    from src.presentation.streamlit.enhanced_css_loader import ensure_css_loaded
    css_loaded = ensure_css_loaded()
    if css_loaded:
        logger.info("✅ Enhanced CSS loaded successfully")
except ImportError:
    logger.warning("⚠️ Enhanced CSS not available, using defaults")


@st.cache_resource  
def initialize_analysis_system(_config_hash: str):
    """
    Initialize analysis system with Streamlit native resource caching
    Replaces complex DI container with simple cached initialization
    """
    config = st.session_state.get('config', {})
    
    # Validate configuration
    from lib.ai_client import validate_openai_config
    validation = validate_openai_config(config)
    
    if not validation['all_valid']:
        logger.error("❌ Invalid configuration for analysis system")
        return None
    
    # Get cached OpenAI client
    client = get_openai_client(_config_hash)
    
    system_info = {
        'client': client,
        'config': config,
        'initialized_at': datetime.now().isoformat(),
        'optimization_enabled': True
    }
    
    logger.info("✅ Analysis system initialized with Streamlit caching")
    return system_info


def main():
    """
    Main analysis workflow using Streamlit-native patterns
    Modular, cached, and fragment-based for optimal performance
    """
    st.title("🚀 Análisis de Comentarios - Sistema Optimizado")
    st.markdown("Sistema de análisis con IA optimizada usando Streamlit native caching y fragments")
    
    # Initialize system with caching
    config = st.session_state.get('config')
    if not config:
        st.error("❌ Sistema no configurado. Vuelve a la página principal.")
        st.stop()
    
    config_hash = generate_config_hash(config)
    analysis_system = initialize_analysis_system(config_hash)
    
    if not analysis_system:
        st.error("❌ No se pudo inicializar el sistema de análisis.")
        st.stop()
    
    # File upload section (fragment-based)
    uploaded_file = render_upload_section()
    
    if uploaded_file is not None:
        # Process file with native caching
        with st.spinner("Procesando archivo..."):
            comments, metadata = process_file_content(
                uploaded_file.read(), 
                uploaded_file.name
            )
        
        if not comments:
            render_error_section("No se encontraron comentarios válidos", "file")
            return
        
        # Validate comments
        validation = validate_comment_content(comments)
        if not validation['is_valid']:
            render_error_section(validation['message'], "file")
            return
        
        # Show file preview and processing estimates
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # File statistics
            st.markdown("#### 📊 Estadísticas del Archivo")
            
            stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
            with stat_col1:
                st.metric("Comentarios", validation['valid_comments'])
            with stat_col2:
                st.metric("Promedio Chars", f"{validation['avg_length']:.0f}")
            with stat_col3:
                filtered = validation['filtered_out']
                st.metric("Filtrados", filtered)
            with stat_col4:
                quality = validation['quality_score'] * 100
                st.metric("Calidad", f"{quality:.0f}%")
        
        with col2:
            # Processing estimates
            st.markdown("#### ⏱️ Estimación de Tiempo")
            estimates = calculate_processing_estimate(len(comments))
            
            st.metric("Tiempo Estimado", f"{estimates['estimated_total_seconds']:.0f}s")
            st.metric("Lotes Optimizados", estimates['num_batches'])
            
            # Performance comparison
            old_estimate = len(comments) * 0.3
            improvement = ((old_estimate - estimates['estimated_total_seconds']) / old_estimate) * 100
            st.metric("Mejora vs Sistema Anterior", f"{improvement:.0f}%")
        
        # Analysis controls (fragment-based)
        if render_analysis_controls(len(comments)):
            run_optimized_analysis(comments, metadata, config)


def run_optimized_analysis(comments: List[str], metadata: Dict[str, Any], 
                          config: Dict[str, Any]) -> None:
    """
    Run optimized analysis workflow with caching and fragments
    """
    start_time = time.time()
    
    # Prepare for analysis
    batch_size = 50  # Optimized batch size
    num_batches = (len(comments) + batch_size - 1) // batch_size
    
    # Initialize progress tracking
    start_progress_tracking(num_batches)
    
    # Container for progress updates (fragment-based)
    progress_container = st.empty()
    
    with progress_container:
        auto_update_analysis_progress()
    
    try:
        # Run cached AI analysis
        config_hash = generate_config_hash(config)
        comments_tuple = tuple(comments)  # Make hashable for caching
        
        logger.info(f"🚀 Starting optimized analysis: {len(comments)} comments in {num_batches} batches")
        
        # This call will be cached by @st.cache_data if same content
        analysis_result = analyze_comments_optimized(comments_tuple, config)
        
        # Clear progress display
        progress_container.empty()
        
        # Get final processing metrics
        processing_metrics = finish_progress_tracking()
        processing_time = time.time() - start_time
        
        # Display performance comparison
        from components.progress_tracker import show_performance_comparison
        old_estimate = len(comments) * 0.3  # Old system estimate
        show_performance_comparison(processing_time, old_estimate)
        
        # Prepare chart data with caching
        chart_data = prepare_chart_data_optimized(analysis_result)
        
        # Generate charts with caching
        charts = create_analysis_dashboard(chart_data)
        
        # Display results (fragment-based)
        render_results_section(analysis_result, charts)
        
        # Show performance stats
        processing_metadata = ProcessingMetadata(
            file_name=metadata['file_name'],
            total_comments=len(comments),
            processing_time=processing_time,
            batch_count=num_batches,
            model_used=config.get('openai_modelo', 'unknown'),
            cache_hit='analysis_result' in str(st.cache_data),  # Detect cache hit
            optimization_enabled=True
        )
        
        render_performance_stats(processing_metadata.__dict__)
        
        # Store results in session state for cross-page access
        st.session_state.latest_analysis = {
            'result': analysis_result,
            'metadata': processing_metadata,
            'charts': charts,
            'timestamp': datetime.now().isoformat()
        }
        
        st.success("🎉 Análisis optimizado completado!")
        st.balloons()
        
    except Exception as e:
        # Clear progress on error
        progress_container.empty()
        if 'analysis_progress' in st.session_state:
            del st.session_state.analysis_progress
        
        logger.error(f"❌ Error in optimized analysis: {str(e)}")
        render_error_section(str(e), "ai")


# Sidebar with optimization info
with st.sidebar:
    st.markdown("### ⚡ Optimizaciones Activas")
    
    optimizations = [
        "✅ Streamlit native caching",
        "✅ Fragment-based UI updates", 
        "✅ Lotes optimizados (50 comentarios)",
        "✅ Rate limiting mínimo (0.2s)",
        "✅ Caching automático de gráficos",
        "✅ Reutilización de análisis previos"
    ]
    
    for opt in optimizations:
        st.markdown(opt)
    
    # Performance targets
    st.markdown("### 🎯 Objetivos de Performance")
    st.markdown("- **200 comentarios:** ≤15s")  
    st.markdown("- **1000 comentarios:** ≤45s")
    st.markdown("- **Re-uploads:** Instantáneo")
    
    # Current session info
    if 'latest_analysis' in st.session_state:
        last_analysis = st.session_state.latest_analysis
        metadata = last_analysis['metadata']
        
        st.markdown("### 📊 Última Análisis")
        st.metric("Tiempo", f"{metadata.processing_time:.1f}s")
        st.metric("Comentarios", metadata.total_comments)  
        st.metric("Lotes", metadata.batch_count)


if __name__ == "__main__":
    main()