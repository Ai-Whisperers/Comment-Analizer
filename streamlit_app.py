"""
Personal Paraguay Comment Analyzer - Clean Architecture
Migrated to use src/ clean architecture with SOLID principles
"""

import sys
import streamlit as st
from pathlib import Path

# Add current directory to path for imports
current_dir = Path(__file__).parent.absolute()
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

# Initialize Clean Architecture App
try:
    from src.aplicacion_principal import crear_aplicacion
    from src.shared.exceptions.archivo_exception import ArchivoException
    from src.shared.exceptions.ia_exception import IAException
    
    # Initialize app in session state
    if 'analizador_app' not in st.session_state:
        # Load OpenAI key from environment/secrets
        import os
        from dotenv import load_dotenv
        load_dotenv()
        
        openai_key = os.getenv('OPENAI_API_KEY') or st.secrets.get('OPENAI_API_KEY', None)
        
        st.session_state.analizador_app = crear_aplicacion(
            openai_api_key=openai_key,
            max_comments=2000,
            debug_mode=False
        )
        
        # Log initialization
        if hasattr(st.session_state.analizador_app, 'obtener_info_sistema'):
            info = st.session_state.analizador_app.obtener_info_sistema()
            st.session_state.app_info = info
    
    CLEAN_ARCHITECTURE_AVAILABLE = True
except ImportError as e:
    st.error(f"❌ Error cargando nueva arquitectura: {str(e)}")
    CLEAN_ARCHITECTURE_AVAILABLE = False
except Exception as e:
    st.warning(f"⚠️ Advertencia en inicialización: {str(e)}")
    CLEAN_ARCHITECTURE_AVAILABLE = False

# Page configuration (PRESERVE PROFESSIONAL SETUP)
st.set_page_config(
    page_title="Personal Paraguay — Análisis de Comentarios",
    page_icon=None, 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for theme (PRESERVE THEME SYSTEM)
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True

# Memory monitoring not available after cleanup
MEMORY_MONITORING_AVAILABLE = False

# Define pages with controlled navigation (Subir first, no streamlit app button)
pages = [
    st.Page("pages/2_Subir.py", title="Subir"),
    st.Page("pages/1_Página_Principal.py", title="Página Principal")
]

# Create navigation with sidebar position (prevents streamlit app button)
pg = st.navigation(pages, position="sidebar")

# Sidebar additional functionality below navigation
with st.sidebar:
    st.markdown("---")
    st.markdown("### Herramientas")
    
    
    # System status section
    st.markdown("---")
    st.markdown("### Estado del Sistema")
    
    if CLEAN_ARCHITECTURE_AVAILABLE and 'app_info' in st.session_state:
        info = st.session_state.app_info
        st.success(f"{info.get('version', '2.0.0')} activo")
        
        config = info.get('configuracion_actual', {})
        openai_status = "OpenAI Configurado" if config.get('openai_configurado') else "Solo Reglas"
        st.info(openai_status)
    else:
        st.warning("Sistema inicializando...")
    
    st.markdown("---")
    st.markdown("### Información de la App")
    
    if CLEAN_ARCHITECTURE_AVAILABLE and 'app_info' in st.session_state:
        info = st.session_state.app_info
        st.markdown(f"""
        **Arquitectura**: {info.get('arquitectura', 'Clean Architecture')}
        **Versión**: {info.get('version', '2.0.0')}
        **OpenAI**: {'Configurado' if info.get('configuracion_actual', {}).get('openai_configurado') else 'Sin configurar'}
        **Rendimiento**: Optimizado
        """)
    else:
        st.markdown("""
        **Arquitectura**: Clean Architecture (Cargando...)
        **Estado**: Inicializando
        **Rendimiento**: Optimizado
        """)

# Run the selected page
pg.run()

# Global footer (PRESERVE SOPHISTICATED STYLING)
st.markdown("---")
st.markdown(
    f"""
    <div style='text-align: center; padding: 2rem; color: #666;'>
        <p><strong>Personal Paraguay</strong> | Plataforma Avanzada de Análisis de Comentarios</p>
        <p>Clean Architecture + SOLID + DDD | {'Sistema Activo' if CLEAN_ARCHITECTURE_AVAILABLE else 'Modo Compatibilidad'}</p>
    </div>
    """,
    unsafe_allow_html=True
)