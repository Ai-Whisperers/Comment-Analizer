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

# Import memory monitoring functions
try:
    from shared.utils.memory_monitor import get_memory_status, optimize_memory, format_memory_display
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
            memory_status = get_memory_status()
            
            if memory_status['available']:
                label, value, delta = format_memory_display(memory_status)
                
                st.metric(label, value, delta)
                
                # Show recommendation for high memory usage
                if memory_status['status'] != 'Normal':
                    st.warning(memory_status['recommendation'])
                    
                    # Memory cleanup button for high usage
                    if memory_status['status'] == 'Alto':
                        if st.button("Limpiar Memoria", key="memory_cleanup_upload", type="secondary"):
                            if optimize_memory():
                                st.success("Memoria optimizada")
                                st.rerun()
                            else:
                                st.error("Error en optimización")
                
                # Environment info
                st.caption(f"Entorno: {memory_status['environment']}")
            else:
                st.info(memory_status['error'])
        else:
            st.info("Monitoreo de memoria no disponible")
    except Exception as e:
        st.info(f"Error en monitoreo: {str(e)}")
    
    # Navigation
    st.markdown("---")
    st.markdown("### Navegación")
    if st.button("Ver Resultados", disabled=('analysis_results' not in st.session_state)):
        st.switch_page("pages/results.py")