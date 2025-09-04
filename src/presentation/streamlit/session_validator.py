"""
Validador de estado de sesión para Streamlit
Asegura que los componentes críticos estén inicializados
"""
import streamlit as st
from typing import Optional, Any, List
import logging

logger = logging.getLogger(__name__)


def ensure_session_initialized(required_keys: Optional[List[str]] = None) -> bool:
    """
    Asegura que el session state esté correctamente inicializado
    
    Args:
        required_keys: Lista opcional de claves requeridas. 
                      Por defecto usa las claves críticas del sistema
    
    Returns:
        bool: True si está inicializado, False si no
    """
    if required_keys is None:
        required_keys = ['caso_uso_maestro', 'contenedor']
    
    missing_keys = []
    for key in required_keys:
        if key not in st.session_state or st.session_state[key] is None:
            missing_keys.append(key)
            logger.error(f"Session state missing required key: {key}")
    
    if missing_keys:
        st.error(f"⚠️ Sistema no inicializado correctamente")
        st.error(f"Componentes faltantes: {', '.join(missing_keys)}")
        st.info("🔄 Por favor, recarga la aplicación desde la página principal")
        
        # Mostrar botón de recarga
        if st.button("Recargar aplicación", type="primary"):
            st.rerun()
        
        st.stop()
        return False
    
    return True


def get_caso_uso_maestro(validate: bool = True):
    """
    Obtiene el caso de uso maestro con validación opcional
    
    Args:
        validate: Si True, valida que exista antes de retornarlo
    
    Returns:
        El caso de uso maestro o None si no existe
    """
    if validate:
        ensure_session_initialized(['caso_uso_maestro'])
    
    return st.session_state.get('caso_uso_maestro')


def get_contenedor(validate: bool = True):
    """
    Obtiene el contenedor de dependencias con validación opcional
    
    Args:
        validate: Si True, valida que exista antes de retornarlo
    
    Returns:
        El contenedor de dependencias o None si no existe
    """
    if validate:
        ensure_session_initialized(['contenedor'])
    
    return st.session_state.get('contenedor')


def get_analysis_results():
    """
    Obtiene los resultados del análisis si existen
    
    Returns:
        Los resultados del análisis o None si no existen
    """
    return st.session_state.get('analysis_results')


def clear_analysis_results():
    """
    Limpia los resultados del análisis de la sesión
    """
    keys_to_clear = ['analysis_results', 'analysis_type']
    
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
            logger.info(f"Cleared session state key: {key}")


def is_ia_system_ready() -> bool:
    """
    Verifica si el sistema IA está listo para usar
    
    Returns:
        bool: True si el sistema IA está listo
    """
    try:
        caso_uso = get_caso_uso_maestro(validate=False)
        
        if caso_uso is None:
            logger.warning("IA system not ready: caso_uso_maestro is None")
            return False
        
        # Verificar si el caso de uso tiene los métodos necesarios
        if not hasattr(caso_uso, 'ejecutar'):
            logger.error("IA system not ready: caso_uso_maestro lacks 'ejecutar' method")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"Error checking IA system readiness: {str(e)}")
        return False


def initialize_session_defaults():
    """
    Inicializa valores por defecto en el session state
    Útil para evitar KeyError en accesos posteriores
    """
    defaults = {
        'css_loaded': False,
        'dark_mode': True,
        'analysis_type': None,
        'app_info': {
            'version': '3.0.0-ia-pure',
            'arquitectura': 'Clean Architecture + Pure IA'
        }
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
            logger.debug(f"Initialized session state key: {key}")


def get_session_info() -> dict:
    """
    Obtiene información sobre el estado actual de la sesión
    
    Returns:
        dict: Información del estado de la sesión
    """
    info = {
        'keys': list(st.session_state.keys()),
        'ia_ready': is_ia_system_ready(),
        'has_results': get_analysis_results() is not None,
        'css_loaded': st.session_state.get('css_loaded', False),
        'app_version': st.session_state.get('app_info', {}).get('version', 'unknown')
    }
    
    return info


# Funciones de conveniencia para validación rápida

def require_ia_system():
    """
    Decorator que requiere que el sistema IA esté inicializado
    
    Usage:
        @require_ia_system()
        def my_function():
            # Esta función solo se ejecuta si IA está lista
            pass
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not is_ia_system_ready():
                st.error("❌ Sistema IA no disponible")
                st.info("Asegúrate de que la API key de OpenAI esté configurada")
                st.stop()
                return None
            return func(*args, **kwargs)
        return wrapper
    return decorator