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


# Add current directory to path for imports
current_dir = Path(__file__).parent.absolute()
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

# Initialize Clean Architecture App
try:
    from src.aplicacion_principal import crear_aplicacion
    from src.shared.exceptions.archivo_exception import ArchivoException
    from src.shared.exceptions.ia_exception import IAException
    from src.presentation.streamlit.css_loader import load_css, load_component_css
    
    # Initialize app in session state
    if 'analizador_app' not in st.session_state:
        # Load OpenAI key from environment/secrets
        import os
        from dotenv import load_dotenv
        load_dotenv()
        
        openai_key = os.getenv('OPENAI_API_KEY') or st.secrets.get('OPENAI_API_KEY', None)
        
        # Pure IA maestro system initialization
        if not openai_key:
            st.error("OpenAI API key es requerida para esta aplicación IA.")
            st.info("Configura OPENAI_API_KEY en las variables de entorno o Streamlit secrets.")
            st.stop()
            
        try:
            from src.infrastructure.dependency_injection.contenedor_dependencias import ContenedorDependencias
            
            # Create IA-pure system with environment variables
            config = {
                'openai_api_key': openai_key,
                'openai_modelo': os.getenv('OPENAI_MODEL') or st.secrets.get('OPENAI_MODEL', 'gpt-4'),
                'openai_temperatura': float(os.getenv('OPENAI_TEMPERATURE', '0.0') or st.secrets.get('OPENAI_TEMPERATURE', '0.0')),
                'openai_max_tokens': int(os.getenv('OPENAI_MAX_TOKENS', '8000') or st.secrets.get('OPENAI_MAX_TOKENS', '8000')),
                'max_comments': int(os.getenv('MAX_COMMENTS_PER_BATCH', '20') or st.secrets.get('MAX_COMMENTS_PER_BATCH', '20')),
                'cache_ttl': int(os.getenv('CACHE_TTL_SECONDS', '3600') or st.secrets.get('CACHE_TTL_SECONDS', '3600'))
            }
            
            # CONFIGURATION VALIDATION AND DEPLOYMENT INFO
            if not _validate_and_log_deployment_config(config):
                st.stop()
            
            contenedor = ContenedorDependencias(config)
            st.session_state.contenedor = contenedor
            st.session_state.caso_uso_maestro = contenedor.obtener_caso_uso_maestro()
            
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

# Load enhanced CSS system with glassmorphism support
if CLEAN_ARCHITECTURE_AVAILABLE:
    try:
        # Try enhanced CSS loader first
        from src.presentation.streamlit.enhanced_css_loader import ensure_css_loaded, load_glassmorphism
        
        # Ensure all CSS including glassmorphism is loaded
        css_loaded = ensure_css_loaded()
        
        if not css_loaded:
            # Fallback to original CSS loader
            try:
                from src.presentation.streamlit.css_loader import CSSLoader
                css_loader = CSSLoader()
                css_loaded = css_loader.load_main_css()
            except:
                pass
        
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
        logger.warning(f"CSS loading failed: {str(e)}")

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