"""
Personal Paraguay Comment Analyzer - SIMPLIFIED
Clean Architecture with ZERO duplication and minimal overhead
"""

import sys
import streamlit as st
from pathlib import Path
import logging

# Import unified configuration
from config import config, is_streamlit_cloud, get_environment_info

# Setup logger
logging.basicConfig(
    level=getattr(logging, config.get('log_level', 'INFO')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add current directory to path for imports
current_dir = Path(__file__).parent.absolute()
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

# Load CSS (single implementation)
try:
    from src.presentation.streamlit.enhanced_css_loader import ensure_css_loaded
    ensure_css_loaded()
except ImportError:
    # Minimal fallback only
    st.markdown('<style>.stButton > button { border-radius: 8px; }</style>', unsafe_allow_html=True)

# Initialize Clean Architecture App (simplified)
if 'app' not in st.session_state:
    try:
        from src.aplicacion_principal import crear_aplicacion
        st.session_state.app = crear_aplicacion(config)
        st.session_state.contenedor = st.session_state.app.contenedor
        logger.info("✅ Aplicación inicializada")
    except Exception as e:
        st.error(f"❌ Error inicializando aplicación: {str(e)}")
        st.stop()

# Simple page configuration
st.set_page_config(
    page_title="Personal Paraguay - Análisis de Comentarios", 
    page_icon="📊",
    layout="wide"
)

# Main page
st.title("📊 Personal Paraguay - Análisis de Comentarios")
st.markdown("Sistema de análisis automatizado de comentarios de clientes usando IA")

# Show environment info
env_info = get_environment_info()
with st.sidebar:
    st.markdown("### 🔧 Configuración")
    st.json(env_info)

# Navigation
st.markdown("### 📄 Páginas Disponibles")

col1, col2 = st.columns(2)
with col1:
    st.page_link("pages/2_Subir.py", label="📁 Subir y Analizar", icon="🚀")
    st.caption("Subir archivo Excel/CSV y ejecutar análisis con IA")

with col2:
    if st.button("🧹 Limpiar Cache", help="Limpiar cache y memoria"):
        # Simple cleanup
        for key in list(st.session_state.keys()):
            if key not in ['app', 'contenedor']:
                del st.session_state[key]
        st.success("✅ Cache limpiado")
        st.rerun()

# Instructions
with st.expander("📖 Instrucciones de Uso", expanded=False):
    st.markdown("""
    **Paso 1:** Ve a la página "Subir y Analizar"  
    **Paso 2:** Carga tu archivo Excel o CSV con comentarios  
    **Paso 3:** Ejecuta el análisis con IA  
    **Paso 4:** Descarga los resultados en Excel profesional
    
    **Formatos soportados:** .xlsx, .xls, .csv  
    **Performance:** <30s para archivos típicos (50 comentarios)
    """)

logger.info(f"Main page loaded - Environment: {env_info['environment']}")