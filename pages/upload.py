"""
Upload Page - Simplified architecture with modern styling preserved
Clean button implementation without deep nesting
"""

import sys
from pathlib import Path

# Add shared modules to path
current_dir = Path(__file__).parent.parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

import streamlit as st
from shared.styling.theme_manager_full import ThemeManager, UIComponents
from shared.business.file_processor import FileProcessor

# Initialize styling and components (PRESERVE MODERN UX)
if 'theme_manager' not in st.session_state:
    st.session_state.theme_manager = ThemeManager()
    st.session_state.ui = UIComponents()

theme = st.session_state.theme_manager
ui = st.session_state.ui

# Apply sophisticated styling (EXACT SAME AS ORIGINAL)
dark_theme = theme.get_theme(st.session_state.get('dark_mode', True))
st.markdown(f"<style>{theme.generate_css_variables(dark_theme)}</style>", unsafe_allow_html=True)
st.markdown(f"<style>{theme.generate_base_styles(dark_theme)}</style>", unsafe_allow_html=True)
st.markdown(f"<style>{theme.generate_animations()}</style>", unsafe_allow_html=True)

# Modern animated header (PRESERVED SOPHISTICATION)
st.markdown(
    ui.animated_header(
        title="Análisis de Comentarios",
        subtitle="Personal Paraguay | File Upload"
    ),
    unsafe_allow_html=True
)

# Floating particles effect (PRESERVED)
st.markdown(ui.floating_particles(), unsafe_allow_html=True)

# SIMPLE BUTTON ARCHITECTURE (FIX FOR RELIABILITY)
st.markdown("### Upload Your File")

# File upload with modern styling
uploaded_file = st.file_uploader(
    "Cargar archivo Excel o CSV",
    type=['xlsx', 'xls', 'csv'],
    help="Sube un archivo Excel (.xlsx, .xls) o CSV con comentarios de clientes"
)

# SIMPLE, TOP-LEVEL BUTTON IMPLEMENTATION (NO DEEP NESTING)
if uploaded_file:
    # File validation display
    processor = FileProcessor()
    validation = processor.validate_file(uploaded_file)
    
    if validation['valid']:
        st.success(f"✅ Archivo válido: {uploaded_file.name} ({validation['file_size_mb']:.1f}MB)")
        
        # SIMPLE BUTTON - NO COMPLEX NESTING
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Procesar Archivo", type="primary", use_container_width=True, key="process_file_btn"):
                # Store file for processing
                st.session_state.uploaded_file = uploaded_file
                st.session_state.validation_results = validation
                
                # Navigate to analyze page
                st.switch_page("pages/analyze.py")
    else:
        st.error(f"❌ {validation['error_message']}")

# Modern section divider (PRESERVED)
st.markdown(ui.section_divider(), unsafe_allow_html=True)

# File requirements with modern styling
st.markdown("### 📋 Requisitos del Archivo")

with st.expander("ℹ️ Información de formato", expanded=False):
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
        primary_text="File Upload | Comment Analyzer",
        secondary_text="Powered by Advanced Analytics"
    ),
    unsafe_allow_html=True
)

# Memory monitoring in sidebar (PRESERVED FUNCTIONALITY)
with st.sidebar:
    st.markdown("### 💾 System Status")
    
    try:
        # Import memory functions
        sys.path.insert(0, str(current_dir / "src"))
        from main import get_memory_usage, is_streamlit_cloud
        
        memory_mb = get_memory_usage()
        if memory_mb > 0:
            memory_limit = 690 if is_streamlit_cloud() else 2048
            memory_pct = (memory_mb / memory_limit) * 100
            color = "🔴" if memory_pct > 80 else ("🟡" if memory_pct > 60 else "🟢")
            
            st.metric(
                f"{color} Memory",
                f"{memory_mb:.0f}MB", 
                f"{memory_pct:.1f}% used"
            )
    except:
        st.info("Memory monitoring unavailable")
    
    # Navigation
    st.markdown("---")
    st.markdown("### 🧭 Navigation")
    if st.button("📊 View Results", disabled=('analysis_results' not in st.session_state)):
        st.switch_page("pages/results.py")