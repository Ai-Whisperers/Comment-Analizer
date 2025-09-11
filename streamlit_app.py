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
        logger.info("🔄 Inicializando nueva arquitectura unificada...")
        
        from src.infrastructure.dependency_injection.contenedor_dependencias import ContenedorDependencias
        from src.infrastructure.config.ai_configuration_manager import AIConfiguration
        
        logger.info(f"📊 Configuración disponible: {len(config)} variables")
        
        # Create AI configuration with detailed logging
        try:
            ai_config = AIConfiguration(
                api_key=config.get('openai_api_key', ''),
                model=config.get('openai_modelo', 'gpt-4o-mini'),
                max_tokens=config.get('openai_max_tokens', 12000),
                temperature=config.get('openai_temperatura', 0.0),
                max_comments_per_batch=config.get('max_comments', 100)
            )
            logger.info(f"✅ AI Config creada: {ai_config.model}, {ai_config.max_tokens} tokens")
        except Exception as e:
            logger.error(f"❌ Error creando AI config: {str(e)}")
            raise
        
        # Initialize dependency container directly with new architecture
        try:
            st.session_state.contenedor = ContenedorDependencias(config, ai_config)
            logger.info("✅ ContenedorDependencias creado exitosamente")
        except Exception as e:
            logger.error(f"❌ Error creando contenedor: {str(e)}")
            raise
        
        # Initialize caso_uso_maestro for session validation (without progress callback)
        try:
            st.session_state.caso_uso_maestro = st.session_state.contenedor.obtener_caso_uso_maestro()
            maestro_status = 'Disponible' if st.session_state.caso_uso_maestro else 'No disponible (modo degradado)'
            logger.info(f"✅ Caso de uso maestro: {maestro_status}")
        except Exception as e:
            st.session_state.caso_uso_maestro = None
            maestro_status = f'Error: {str(e)}'
            logger.warning(f"⚠️ Caso de uso maestro error: {str(e)}")
            
        logger.info("✅ Nueva arquitectura inicializada directamente")
        logger.info(f"📊 Session state keys: {list(st.session_state.keys())}")
        
        # FORCE CACHE REFRESH: Verify modern pipeline components
        logger.info("🔍 Verifying modern pipeline version...")
        from src.application.use_cases.analizar_excel_maestro_caso_uso import ComandoAnalisisExcelMaestro
        import inspect
        
        sig = inspect.signature(ComandoAnalisisExcelMaestro.__init__)
        has_progress_callback = 'progress_callback' in str(sig)
        logger.info(f"📋 ComandoAnalisisExcelMaestro signature: {sig}")
        logger.info(f"🎯 Modern pipeline active: {'✅' if has_progress_callback else '❌'} (progress_callback support)")
        
        # Final verification that contenedor is properly initialized
        if 'contenedor' not in st.session_state or st.session_state.contenedor is None:
            raise Exception("Contenedor no se inicializó correctamente en session_state")
        
    except Exception as e:
        error_msg = f"Error inicializando nueva arquitectura: {str(e)}"
        logger.error(f"❌ {error_msg}")
        st.error(f"❌ {error_msg}")
        st.error("🔧 Posibles soluciones:")
        st.error("- Verificar que todas las dependencias estén instaladas")
        st.error("- Verificar configuración en variables de entorno")
        st.error("- Revisar logs para más detalles")
        
        # Show debug info
        with st.expander("🔍 Información de Debug"):
            st.json({
                'config_keys': list(config.keys()) if config else [],
                'config_sample': {k: str(v)[:50] + '...' if len(str(v)) > 50 else str(v) 
                                 for k, v in list(config.items())[:5]} if config else {},
                'session_state_keys': list(st.session_state.keys()),
                'error_type': type(e).__name__,
                'error_message': str(e),
                'environment': 'Streamlit Cloud' if is_streamlit_cloud() else 'Local'
            })
        
        # Force re-initialization button
        if st.button("🔄 Forzar Re-inicialización", type="primary"):
            # Clear all session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
            
        st.stop()

# Additional safety check after initialization
if 'contenedor' not in st.session_state:
    st.error("🚨 Contenedor no disponible después de inicialización")
    st.error("Esto indica un problema serio en el proceso de inicialización")
    st.info("Intenta recargar la página completamente (F5)")
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