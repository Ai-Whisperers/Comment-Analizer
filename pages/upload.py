"""
Upload Page - Simplified architecture with modern styling preserved
Clean button implementation without deep nesting
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

# Try to import memory monitoring functions
try:
    sys.path.insert(0, str(current_dir / "src"))
    from main import get_memory_usage, is_streamlit_cloud
    MEMORY_MONITORING_AVAILABLE = True
except ImportError:
    MEMORY_MONITORING_AVAILABLE = False

# Initialize styling and components (PRESERVE MODERN UX)
if 'theme_manager' not in st.session_state:
    st.session_state.theme_manager = ThemeManager()
    st.session_state.ui = UIComponents()

theme = st.session_state.theme_manager
ui = st.session_state.ui

# Apply modular glassmorphism Web3 styling (proper separation of concerns)
from shared.styling.modular_css import initialize_modular_styles
initialize_modular_styles(dark_mode=st.session_state.get('dark_mode', True))

# Modern animated header (PRESERVED SOPHISTICATION)
st.markdown(
    ui.animated_header(
        title="Análisis de Comentarios",
        subtitle="Personal Paraguay | Cargar Archivo"
    ),
    unsafe_allow_html=True
)

# Floating particles effect (PRESERVED)
st.markdown(ui.floating_particles(), unsafe_allow_html=True)

# SIMPLE BUTTON ARCHITECTURE (FIX FOR RELIABILITY)
st.markdown("### Cargar Archivo")

# File upload with modern styling
uploaded_file = st.file_uploader(
    "Cargar archivo Excel o CSV",
    type=['xlsx', 'xls', 'csv'],
    help="Sube un archivo Excel (.xlsx, .xls) o CSV con comentarios de clientes"
)

# ENHANCED FILE UPLOAD WITH PREVIEW
if uploaded_file:
    # File validation display
    processor = FileProcessor()
    validation = processor.validate_file(uploaded_file)
    
    if validation['valid']:
        st.success(f"Archivo válido: {uploaded_file.name} ({validation['file_size_mb']:.1f}MB)")
        
        # Enhanced file preview with statistics
        try:
            import pandas as pd
            import io
            
            # Read file for preview
            if uploaded_file.name.endswith('.csv'):
                df_preview = pd.read_csv(uploaded_file, nrows=5)
                df_full = pd.read_csv(uploaded_file)
            else:
                df_preview = pd.read_excel(uploaded_file, nrows=5)
                df_full = pd.read_excel(uploaded_file)
            
            # Display file preview header with stats
            st.markdown(
                ui.file_preview_header(
                    filename=uploaded_file.name,
                    filesize=f"{validation['file_size_mb']:.1f}MB",
                    rows=len(df_full),
                    columns=len(df_full.columns)
                ),
                unsafe_allow_html=True
            )
            
            # Show data preview
            with st.expander("Vista previa de datos (primeras 5 filas)", expanded=True):
                st.dataframe(df_preview, use_container_width=True)
                
                # Column analysis
                col_info = []
                for col in df_full.columns:
                    col_type = "Comentarios" if any(keyword in col.lower() for keyword in ['comment', 'comentario', 'feedback']) else "Numérica" if df_full[col].dtype in ['int64', 'float64'] else "Texto"
                    col_info.append(f"**{col}**: {col_type}")
                
                st.info("**Columnas detectadas:** " + " | ".join(col_info))
            
        except Exception as e:
            st.warning(f"No se pudo generar vista previa: {str(e)}")
        
        # SIMPLE BUTTON - NO COMPLEX NESTING
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Procesar Archivo", type="primary", use_container_width=True, key="process_file_btn"):
                # Store file for processing
                st.session_state.uploaded_file = uploaded_file
                st.session_state.validation_results = validation
                
                # Navigate to analyze page
                st.switch_page("pages/analyze.py")
    else:
        st.error(f"Error: {validation['error_message']}")

# Modern section divider (PRESERVED)
st.markdown(ui.section_divider(), unsafe_allow_html=True)

# File requirements with modern styling
st.markdown("### Requisitos del Archivo")

with st.expander("Información de formato", expanded=False):
    st.markdown("""
    **Formatos soportados:**
    - Excel (.xlsx, .xls)
    - CSV (.csv)
    
    **Límites para Streamlit Cloud:**
    - Tamaño máximo: 1.5MB
    - Comentarios máximos: 200
    
    **Columnas requeridas:**
    - Una columna con comentarios (puede llamarse: comentario, comment, feedback, etc.)
    - Columnas opcionales: NPS, Nota
    """)

# Modern gradient footer (PRESERVED)
st.markdown(
    ui.gradient_footer(
        primary_text="Cargar Archivo | Analizador de Comentarios",
        secondary_text="Impulsado por Análisis Avanzados"
    ),
    unsafe_allow_html=True
)

# Memory monitoring in sidebar (PRESERVED FUNCTIONALITY)
with st.sidebar:
    st.markdown("### Estado del Sistema")
    
    try:
        if MEMORY_MONITORING_AVAILABLE:
            memory_mb = get_memory_usage()
            if memory_mb > 0:
                memory_limit = 690 if is_streamlit_cloud() else 2048
                memory_pct = (memory_mb / memory_limit) * 100
                status = "Alto" if memory_pct > 80 else ("Medio" if memory_pct > 60 else "Normal")
                color = "red" if memory_pct > 80 else ("orange" if memory_pct > 60 else "green")
                
                st.metric(
                    f"Memoria ({status})",
                    f"{memory_mb:.0f}MB", 
                    f"{memory_pct:.1f}% usado"
                )
            else:
                st.info("Datos de memoria no disponibles")
        else:
            st.info("Monitoreo de memoria no disponible")
    except Exception as e:
        st.info("Monitoreo de memoria no disponible")
    
    # Navigation
    st.markdown("---")
    st.markdown("### Navegación")
    if st.button("Ver Resultados", disabled=('analysis_results' not in st.session_state)):
        st.switch_page("pages/results.py")