"""
Analyze Page - File processing with modern UI preserved
Simple architecture with sophisticated styling maintained
"""

import sys
import streamlit as st
from pathlib import Path

# Add shared modules to path
current_dir = Path(__file__).parent.parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from shared.styling.theme_manager_full import ThemeManager, UIComponents
from shared.business.file_processor import FileProcessor

# Initialize styling (PRESERVE MODERN UX)
if 'theme_manager' not in st.session_state:
    st.session_state.theme_manager = ThemeManager()
    st.session_state.ui = UIComponents()

theme = st.session_state.theme_manager
ui = st.session_state.ui

# Apply complete glassmorphism Web3 styling
st.markdown(theme.get_complete_css(st.session_state.get('dark_mode', True)), unsafe_allow_html=True)

# Modern header (PRESERVED)
st.markdown(
    ui.animated_header(
        title="Procesando Comentarios",
        subtitle="Análisis Avanzado en Progreso"
    ),
    unsafe_allow_html=True
)

# Check if file was uploaded
if 'uploaded_file' not in st.session_state:
    st.error("No se cargó ningún archivo. Por favor regresa a cargar un archivo.")
    if st.button("Volver a Cargar", key="back_to_upload"):
        st.switch_page("pages/upload.py")
    st.stop()

uploaded_file = st.session_state.uploaded_file
processor = FileProcessor()

# SIMPLE PROCESSING WITH MODERN UI
st.markdown("### Opciones de Análisis")

# Analysis method selection with simple button structure
col1, col2 = st.columns(2)

with col1:
    # SIMPLE BUTTON - NO DEEP NESTING
    if st.button("Análisis Rápido", type="primary", use_container_width=True, key="quick_analysis"):
        with st.spinner("Procesando comentarios..."):
            try:
                # Process file using business logic
                results = processor.process_uploaded_file(uploaded_file)
                
                if results:
                    st.session_state.analysis_results = results
                    st.success("Análisis completado!")
                    
                    # Navigate to results
                    if st.button("Ver Resultados", key="view_results_quick"):
                        st.switch_page("pages/results.py")
                else:
                    st.error("Error procesando archivo")
                    
            except Exception as e:
                st.error(f"Error durante análisis: {str(e)}")

with col2:
    # SIMPLE AI BUTTON - NO DEEP NESTING  
    if st.button("Análisis con IA", type="secondary", use_container_width=True, key="ai_analysis"):
        with st.spinner("Procesando con inteligencia artificial..."):
            try:
                # Process file using AI-enhanced business logic
                results = processor.process_uploaded_file(uploaded_file, use_ai_insights=True)
                
                if results:
                    st.session_state.analysis_results = results
                    st.success("Análisis IA completado!")
                    
                    # Navigate to results
                    if st.button("Ver Resultados IA", key="view_results_ai"):
                        st.switch_page("pages/results.py")
                else:
                    st.error("Error procesando archivo con IA")
                    
            except Exception as e:
                st.error(f"Error durante análisis IA: {str(e)}")

# Modern section divider (PRESERVED)
st.markdown(ui.section_divider(), unsafe_allow_html=True)

# Processing status with modern styling
if 'analysis_results' in st.session_state:
    results = st.session_state.analysis_results
    
    # Modern status display (PRESERVED SOPHISTICATION)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            ui.status_badge(
                icon="📊",
                text=f"Total: {results.get('total', 0)} comentarios",
                badge_type="neutral"
            ),
            unsafe_allow_html=True
        )
    
    with col2:
        dominant_sentiment = results.get('insights', {}).get('dominant_sentiment', 'neutral')
        badge_type = "positive" if dominant_sentiment == "positivo" else "negative" if dominant_sentiment == "negativo" else "neutral"
        
        st.markdown(
            ui.status_badge(
                icon="💭",
                text=f"Sentimiento: {dominant_sentiment}",
                badge_type=badge_type
            ),
            unsafe_allow_html=True
        )
    
    with col3:
        quality = results.get('insights', {}).get('analysis_quality', 'basic')
        st.markdown(
            ui.status_badge(
                icon="⭐",
                text=f"Calidad: {quality}",
                badge_type="positive" if quality == "high" else "neutral"
            ),
            unsafe_allow_html=True
        )

# Navigation with modern styling
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    if st.button("Nueva Carga", key="new_upload"):
        # Clear session and go back
        if 'uploaded_file' in st.session_state:
            del st.session_state.uploaded_file
        st.switch_page("pages/upload.py")

with col2:
    if st.button("Ver Resultados", key="goto_results", disabled=('analysis_results' not in st.session_state)):
        st.switch_page("pages/results.py")

# Modern footer (PRESERVED)
st.markdown(
    ui.gradient_footer(
        primary_text="Motor de Análisis | Analizador de Comentarios", 
        secondary_text="Procesamiento Inteligente"
    ),
    unsafe_allow_html=True
)