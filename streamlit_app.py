"""
Personal Paraguay Comment Analyzer - Controlled Navigation
Using st.navigation for complete control over navbar buttons
"""

import sys
import streamlit as st
from pathlib import Path

# Add current directory to path for imports
current_dir = Path(__file__).parent.absolute()
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

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

# Import memory monitoring
try:
    from shared.utils.memory_monitor import get_memory_status, optimize_memory, format_memory_display
    MEMORY_MONITORING_AVAILABLE = True
except ImportError:
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
    
    # Theme toggle (PRESERVE MODERN FEATURE)
    if st.button("Cambiar Tema", key="theme_toggle"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()
    
    # Enhanced memory monitoring with glassmorphism styling
    st.markdown("---")
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
                        if st.button("Limpiar Memoria", key="memory_cleanup_main", type="secondary"):
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
    
    st.markdown("---")
    st.markdown("### Información de la App")
    st.markdown("""
    **Arquitectura**: Multipágina
    **Estilo**: Moderno preservado
    **Rendimiento**: Optimizado
    """)

# Run the selected page
pg.run()

# Global footer (PRESERVE SOPHISTICATED STYLING)
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; padding: 2rem; color: #666;'>
        <p><strong>Personal Paraguay</strong> | Plataforma Avanzada de Análisis de Comentarios</p>
        <p>Arquitectura multipágina con estilo moderno preservado</p>
    </div>
    """,
    unsafe_allow_html=True
)