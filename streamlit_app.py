"""
Personal Paraguay Comment Analyzer - Clean Architecture
Migrated to use src/ clean architecture with SOLID principles
"""

import sys
import streamlit as st
from pathlib import Path
import logging

# Setup logger
logger = logging.getLogger(__name__)


def _validate_and_log_deployment_config(config):
    """Validate configuration parameters and log deployment info"""
    import os
    import datetime
    
    # Log deployment information for debugging
    deployment_info = {
        'timestamp': datetime.datetime.now().isoformat(),
        'max_comments_config': config.get('max_comments'),
        'max_comments_env': os.getenv('MAX_COMMENTS_PER_BATCH'),
        'max_comments_secrets': st.secrets.get('MAX_COMMENTS_PER_BATCH', 'NOT_SET'),
        'openai_model': config.get('openai_modelo'),
        'openai_max_tokens': config.get('openai_max_tokens'),
        'git_commit': os.getenv('STREAMLIT_COMMIT_SHA', 'unknown')
    }
    
    logger.info(f"🚀 Deployment info: {deployment_info}")
    
    # Configuration validation
    max_comments = config.get('max_comments', 20)
    max_tokens = config.get('openai_max_tokens', 8000)
    
    # Critical validation: batch size too large
    if max_comments > 25:
        st.error(f"❌ CONFIGURACIÓN INCORRECTA: MAX_COMMENTS_PER_BATCH = {max_comments}")
        st.error("🔧 Valor demasiado alto. Máximo permitido: 25")
        st.info("💡 Solución: Actualizar secrets en Streamlit Cloud: MAX_COMMENTS_PER_BATCH = '20'")
        st.info("🔄 Luego reiniciar la aplicación")
        return False
        
    # Warning: token limit high
    if max_tokens > 16000:
        st.warning(f"⚠️ OPENAI_MAX_TOKENS alto: {max_tokens}. Recomendado: 8000")
    
    # Success message
    st.sidebar.success(f"✅ Config: {max_comments} comentarios/lote, {max_tokens} tokens")
    
    # Show deployment info in sidebar for debugging
    with st.sidebar.expander("🔧 Deployment Info", expanded=False):
        st.json(deployment_info)
    
    return True


def _load_enhanced_fallback_css():
    """Enhanced fallback CSS loader when static files are not available"""
    try:
        # Try to load glassmorphism directly from enhanced CSS loader
        if CSS_LOADER_ENHANCED:
            success = load_glassmorphism()
            if success:
                logger.info("✅ Enhanced fallback: Glassmorphism loaded")
                return True
        
        # Fallback to inline enhanced CSS
        enhanced_fallback_css = """
        <style>
        /* Enhanced Fallback CSS - Professional Glassmorphism */
        :root {
            --primary-purple: #8B5CF6;
            --secondary-cyan: #06B6D4;
            --glass-bg: rgba(255, 255, 255, 0.08);
            --glass-border: rgba(255, 255, 255, 0.15);
            --glass-shadow: rgba(139, 92, 246, 0.08);
        }
        
        .glass, .glass-card {
            background: var(--glass-bg) !important;
            backdrop-filter: blur(16px) !important;
            -webkit-backdrop-filter: blur(16px) !important;
            border: 1px solid var(--glass-border) !important;
            border-radius: 16px !important;
            box-shadow: 0 2px 8px var(--glass-shadow) !important;
            transition: all 0.3s ease !important;
        }
        
        .glass-card:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 20px rgba(139, 92, 246, 0.25) !important;
        }
        
        /* Streamlit component enhancements */
        .stButton > button {
            background: linear-gradient(135deg, var(--primary-purple), var(--secondary-cyan)) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            backdrop-filter: blur(10px) !important;
        }
        
        .stSelectbox [data-baseweb="select"] {
            background: var(--glass-bg) !important;
            border: 1px solid var(--glass-border) !important;
            border-radius: 8px !important;
        }
        </style>
        """
        
        st.markdown(enhanced_fallback_css, unsafe_allow_html=True)
        logger.info("✅ Enhanced fallback CSS loaded (inline)")
        return True
        
    except Exception as e:
        logger.error(f"❌ Enhanced fallback CSS failed: {str(e)}")
        return False


# Add current directory to path for imports
current_dir = Path(__file__).parent.absolute()
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

# Initialize Clean Architecture App
try:
    from src.aplicacion_principal import crear_aplicacion
    from src.shared.exceptions.archivo_exception import ArchivoException
    from src.shared.exceptions.ia_exception import IAException
    
    # Import enhanced CSS loader for glassmorphism and chart integration  
    try:
        from src.presentation.streamlit.enhanced_css_loader import ensure_css_loaded, load_glassmorphism
        CSS_LOADER_ENHANCED = True
    except ImportError:
        # Fallback to basic CSS loader
        from src.presentation.streamlit.css_loader import load_css, load_component_css
        CSS_LOADER_ENHANCED = False
    
    # Initialize app in session state
    if 'analizador_app' not in st.session_state:
        # PHASE 2: Use centralized AI configuration system
        import os
        from dotenv import load_dotenv
        load_dotenv()
        
        try:
            from src.infrastructure.config import get_ai_configuration_manager, get_ai_configuration
            from src.infrastructure.dependency_injection.contenedor_dependencias import ContenedorDependencias
            
            # Initialize centralized AI configuration
            ai_config_manager = get_ai_configuration_manager(st.secrets)
            ai_config = ai_config_manager.get_configuration()
            
            # Validate configuration
            if not ai_config_manager.validate_configuration():
                st.error("❌ Invalid AI configuration detected")
                st.stop()
            
            # Create legacy config format for backwards compatibility
            config = {
                'openai_api_key': ai_config.api_key,
                'openai_modelo': ai_config.model,
                'openai_temperatura': ai_config.temperature,
                'openai_max_tokens': ai_config.max_tokens,
                'max_comments': ai_config.max_comments_per_batch,
                'cache_ttl': ai_config.cache_ttl_seconds
            }
            
            # CONFIGURATION VALIDATION AND DEPLOYMENT INFO
            if not _validate_and_log_deployment_config(config):
                st.stop()
            
            contenedor = ContenedorDependencias(config, ai_config)
            st.session_state.contenedor = contenedor
            st.session_state.caso_uso_maestro = contenedor.obtener_caso_uso_maestro()
            
            # Store AI configuration manager for access throughout the app
            st.session_state.ai_config_manager = ai_config_manager
            st.session_state.ai_configuration = ai_config
            
            if not st.session_state.caso_uso_maestro:
                raise ValueError("No se pudo inicializar sistema IA maestro")
            
        except Exception as e:
            st.error(f"Error inicializando sistema IA: {str(e)}")
            st.error("Esta aplicación requiere sistema IA funcional.")
            st.stop()
        
        # Log IA system initialization 
        st.session_state.app_info = {
            'version': '3.0.0-ia-pure',
            'arquitectura': 'Clean Architecture + Pure IA',
            'configuracion_actual': {
                'openai_configurado': True,
                'sistema': 'maestro_ia'
            }
        }
    
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

# Initialize session state for theme and load CSS
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True

# Load enhanced CSS system with improved static/ integration
if CLEAN_ARCHITECTURE_AVAILABLE:
    try:
        # Enhanced CSS loader with better static/ folder integration
        from src.presentation.streamlit.enhanced_css_loader import ensure_css_loaded
        
        # Load complete CSS cascade from static/ folder
        css_loaded = ensure_css_loaded()
        logger.info(f"🎨 CSS system loaded: {css_loaded}")
        
        if not css_loaded:
            # Enhanced fallback with core glassmorphism
            logger.warning("⚠️ CSS files not found, loading enhanced fallback")
            _load_enhanced_fallback_css()
        
        if not css_loaded:
            # Final fallback - load critical CSS files directly
            try:
                critical_files = [
                    'static/css/glassmorphism.css',
                    'static/main.css',
                    'static/styles.css'
                ]
                
                for css_file in critical_files:
                    try:
                        with open(css_file, 'r', encoding='utf-8') as f:
                            css_content = f.read()
                            st.markdown(f'<style>{css_content}</style>', unsafe_allow_html=True)
                            css_loaded = True
                            break
                    except:
                        continue
                        
            except Exception:
                # Ultimate fallback - inline essential CSS with glassmorphism
                essential_css = """
                <style>
                :root {
                    --primary-purple: #8B5CF6;
                    --secondary-cyan: #06B6D4;
                }
                
                /* Essential Glassmorphism */
                .glass, .glass-card {
                    background: rgba(255, 255, 255, 0.08) !important;
                    backdrop-filter: blur(16px) !important;
                    -webkit-backdrop-filter: blur(16px) !important;
                    border: 1px solid rgba(255, 255, 255, 0.15) !important;
                    border-radius: 16px !important;
                    box-shadow: 0 2px 8px rgba(139, 92, 246, 0.08) !important;
                }
                
                .stButton > button {
                    background: linear-gradient(135deg, var(--primary-purple), var(--secondary-cyan));
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    border-radius: 12px;
                    color: white;
                    transition: all 0.3s ease;
                }
                
                .stButton > button:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 8px 20px rgba(139, 92, 246, 0.25);
                }
                </style>
                """
                st.markdown(essential_css, unsafe_allow_html=True)
                css_loaded = True
        
        st.session_state.css_loaded = css_loaded
        
    except Exception as e:
        st.session_state.css_loaded = False
        logger.error(f"❌ CSS loading failed: {str(e)}")
        # Try basic fallback
        _load_basic_fallback_css()


def _load_enhanced_fallback_css():
    """Enhanced fallback CSS when static/ files not accessible"""
    enhanced_fallback = """
    <style>
    :root {
        --primary-purple: #8B5CF6;
        --secondary-cyan: #06B6D4;
        --glass-bg: rgba(255, 255, 255, 0.08);
        --glass-border: rgba(255, 255, 255, 0.15);
    }
    
    /* Enhanced glassmorphism for all components */
    .glass, .glass-card {
        background: var(--glass-bg) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 16px !important;
        box-shadow: 0 2px 8px rgba(139, 92, 246, 0.08) !important;
    }
    
    /* Streamlit button enhancement */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-purple), var(--secondary-cyan)) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: white !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(139, 92, 246, 0.25) !important;
    }
    
    /* Chart containers with glass effects */
    .plotly-graph-div {
        background: rgba(255, 255, 255, 0.03) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(8px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        padding: 0.5rem !important;
    }
    
    /* Metrics with glassmorphism */
    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.06) !important;
        border-radius: 8px !important;
        backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
    }
    </style>
    """
    st.markdown(enhanced_fallback, unsafe_allow_html=True)
    logger.info("✅ Enhanced fallback CSS loaded")


def _load_basic_fallback_css():
    """Basic fallback CSS for emergency situations"""
    basic_css = """
    <style>
    .stButton > button {
        background: linear-gradient(135deg, #8B5CF6, #06B6D4);
        color: white;
        border: none;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    </style>
    """
    st.markdown(basic_css, unsafe_allow_html=True)

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