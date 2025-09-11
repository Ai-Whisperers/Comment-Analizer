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

# Initialize New Architecture (Direct DI Container - no aplicacion_principal.py)
if 'contenedor' not in st.session_state:
    try:
        from src.infrastructure.dependency_injection.contenedor_dependencias import ContenedorDependencias
        from src.infrastructure.config.ai_configuration_manager import AIConfiguration
        
        # Create AI configuration
        ai_config = AIConfiguration(
            api_key=config.get('openai_api_key', ''),
            model=config.get('openai_modelo', 'gpt-4o-mini'),
            max_tokens=config.get('openai_max_tokens', 12000),
            temperature=config.get('openai_temperatura', 0.0),
            max_comments_per_batch=config.get('max_comments', 100)
        )
        
        # Initialize dependency container directly with new architecture
        st.session_state.contenedor = ContenedorDependencias(config, ai_config)
        
        # Initialize caso_uso_maestro for session validation (without progress callback)
        try:
            st.session_state.caso_uso_maestro = st.session_state.contenedor.obtener_caso_uso_maestro()
            maestro_status = 'Disponible' if st.session_state.caso_uso_maestro else 'No disponible (modo degradado)'
        except Exception as e:
            st.session_state.caso_uso_maestro = None
            maestro_status = f'Error: {str(e)}'
            
        logger.info("✅ Nueva arquitectura inicializada directamente")
        logger.info(f"✅ Caso de uso maestro: {maestro_status}")
        logger.info(f"📊 Configuración cargada: {len(config)} variables")
    except Exception as e:
        st.error(f"❌ Error inicializando nueva arquitectura: {str(e)}")
        st.stop()

# Simple page configuration
st.set_page_config(
    page_title="Personal Paraguay - Análisis de Comentarios", 
    page_icon="📊",
    layout="wide"
)

# Main page
st.title("Análisis de Comentarios de Personal PY")
st.markdown("Sistema de análisis de comentarios de clientes. Automatizado mediante IA")

# Show environment info
env_info = get_environment_info()
with st.sidebar:
    st.markdown("### Configuración")
    st.json(env_info)

# Navigation
st.markdown("### Páginas Disponibles")

col1, col2 = st.columns(2)
with col1:
    st.page_link("pages/2_Subir.py", label="Subir y Analizar", icon="🚀")
    st.caption("Subir archivo Excel/CSV y ejecutar análisis con IA")

with col2:
    if st.button("Limpiar Cache", help="Limpiar cache y memoria"):
        # Clean up all except core architecture components
        for key in list(st.session_state.keys()):
            if key not in ['contenedor', 'caso_uso_maestro']:
                del st.session_state[key]
        
        # Clean internal caches in dependency container
        if 'contenedor' in st.session_state:
            st.session_state.contenedor.cleanup_singletons()
            
        st.success("✅ Cache limpiado - Arquitectura mantenida")
        st.rerun()

# Instructions
with st.expander("Instrucciones de Uso", expanded=False):
    st.markdown("""
    **Paso 1:** Ve a la página "Subir y Analizar"  
    **Paso 2:** Carga tu archivo Excel o CSV con comentarios  
    **Paso 3:** Ejecuta el análisis con IA  
    **Paso 4:** Descarga los resultados en Excel profesional
    
    **Formatos soportados:** .xlsx, .xls, .csv  
    **Performance:** <30s para archivos típicos (50 comentarios)
    """)

logger.info(f"Main page loaded - Environment: {env_info['environment']}")