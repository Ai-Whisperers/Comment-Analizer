"""
CSS Loader para componentes Streamlit
Utilidad para cargar CSS modular en aplicaciones Streamlit
"""
import streamlit as st
import os
from pathlib import Path
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


class CSSLoader:
    """
    Cargador de CSS modular para aplicaciones Streamlit
    
    Permite cargar CSS completo o módulos específicos de manera eficiente
    con cache y manejo de errores.
    """
    
    def __init__(self, css_base_path: str = "static"):
        """
        Inicializa el cargador CSS
        
        Args:
            css_base_path: Ruta base donde están los archivos CSS
        """
        self.css_base_path = Path(css_base_path)
        self._loaded_modules = set()
        
    def load_main_css(self, force_reload: bool = False) -> bool:
        """
        Carga el CSS principal (main.css) que incluye todos los módulos
        
        Args:
            force_reload: Si True, fuerza la recarga aunque ya esté cargado
            
        Returns:
            bool: True si se cargó exitosamente
        """
        css_file = self.css_base_path / "main.css"
        
        if not force_reload and "main.css" in self._loaded_modules:
            return True
            
        if self._load_css_file(css_file):
            self._loaded_modules.add("main.css")
            logger.info("✅ CSS principal cargado exitosamente")
            return True
        return False
    
    def load_specific_modules(self, modules: List[str], force_reload: bool = False) -> bool:
        """
        Carga módulos CSS específicos
        
        Args:
            modules: Lista de módulos a cargar (ej: ['components/forms.css', 'utils/utilities.css'])
            force_reload: Si True, fuerza la recarga
            
        Returns:
            bool: True si todos los módulos se cargaron exitosamente
        """
        success_count = 0
        
        for module in modules:
            css_file = self.css_base_path / "css" / module
            
            if not force_reload and module in self._loaded_modules:
                success_count += 1
                continue
                
            if self._load_css_file(css_file):
                self._loaded_modules.add(module)
                success_count += 1
                logger.debug(f"✅ Módulo CSS cargado: {module}")
            else:
                logger.error(f"❌ Error cargando módulo CSS: {module}")
        
        all_loaded = success_count == len(modules)
        if all_loaded:
            logger.info(f"✅ Todos los módulos CSS cargados: {modules}")
        return all_loaded
    
    def load_component_styles(self, component_type: str) -> bool:
        """
        Carga estilos específicos para un tipo de componente
        
        Args:
            component_type: Tipo de componente ('forms', 'charts', 'layout', 'core')
            
        Returns:
            bool: True si se cargó exitosamente
        """
        component_modules = {
            'forms': ['base/variables.css', 'components/forms.css'],
            'charts': ['base/variables.css', 'components/charts.css', 'animations/keyframes.css'],
            'layout': ['base/variables.css', 'components/layout.css'],
            'core': ['base/variables.css', 'base/reset.css', 'components/streamlit-core.css'],
            'complete': ['base/variables.css', 'base/reset.css', 'components/streamlit-core.css', 
                        'components/forms.css', 'components/charts.css', 'components/layout.css',
                        'animations/keyframes.css', 'utils/utilities.css']
        }
        
        if component_type not in component_modules:
            logger.error(f"❌ Tipo de componente desconocido: {component_type}")
            return False
            
        modules = component_modules[component_type]
        return self.load_specific_modules(modules)
    
    def inject_custom_css(self, css_string: str, identifier: Optional[str] = None) -> bool:
        """
        Inyecta CSS personalizado directamente
        
        Args:
            css_string: Código CSS a inyectar
            identifier: Identificador único para el CSS (opcional)
            
        Returns:
            bool: True si se inyectó exitosamente
        """
        try:
            st.markdown(f'<style>{css_string}</style>', unsafe_allow_html=True)
            
            if identifier:
                self._loaded_modules.add(f"custom_{identifier}")
            
            logger.debug("✅ CSS personalizado inyectado")
            return True
        except Exception as e:
            logger.error(f"❌ Error inyectando CSS personalizado: {str(e)}")
            return False
    
    def get_loaded_modules(self) -> List[str]:
        """
        Obtiene la lista de módulos cargados
        
        Returns:
            List[str]: Lista de módulos cargados
        """
        return list(self._loaded_modules)
    
    def clear_cache(self) -> None:
        """
        Limpia el cache de módulos cargados
        """
        self._loaded_modules.clear()
        logger.info("🧹 Cache de CSS limpiado")
    
    def _load_css_file(self, css_file_path: Path) -> bool:
        """
        Carga un archivo CSS específico
        
        Args:
            css_file_path: Ruta al archivo CSS
            
        Returns:
            bool: True si se cargó exitosamente
        """
        try:
            if not css_file_path.exists():
                logger.error(f"❌ Archivo CSS no encontrado: {css_file_path}")
                return False
            
            with open(css_file_path, 'r', encoding='utf-8') as f:
                css_content = f.read()
                
            st.markdown(f'<style>{css_content}</style>', unsafe_allow_html=True)
            return True
            
        except Exception as e:
            logger.error(f"❌ Error cargando archivo CSS {css_file_path}: {str(e)}")
            return False
    
    @staticmethod
    def create_glass_card(content: str, css_class: str = "glass-card") -> str:
        """
        Crea HTML para una tarjeta con efecto glass morphism
        
        Args:
            content: Contenido HTML interno
            css_class: Clase CSS adicional
            
        Returns:
            str: HTML de la tarjeta
        """
        return f"""
        <div class="{css_class} animate-fade-in">
            {content}
        </div>
        """
    
    @staticmethod
    def create_metric_card(title: str, value: str, change: Optional[float] = None, 
                          icon: Optional[str] = None) -> str:
        """
        Crea HTML para una tarjeta de métrica
        
        Args:
            title: Título de la métrica
            value: Valor principal
            change: Cambio porcentual (opcional)
            icon: Icono opcional
            
        Returns:
            str: HTML de la métrica
        """
        change_html = ""
        if change is not None:
            change_class = "text-success" if change > 0 else "text-error" if change < 0 else "text-tertiary"
            change_symbol = "+" if change > 0 else ""
            change_html = f'<div class="{change_class} text-sm font-medium mt-1">{change_symbol}{change:.1f}%</div>'
        
        icon_html = f'<div class="text-2xl mb-2">{icon}</div>' if icon else ""
        
        return f"""
        <div class="stat-card glass-card animate-fade-in">
            {icon_html}
            <div class="stat-value text-gradient">{value}</div>
            <div class="stat-label">{title}</div>
            {change_html}
        </div>
        """
    
    @staticmethod
    def create_section_header(title: str, subtitle: Optional[str] = None) -> str:
        """
        Crea HTML para un header de sección
        
        Args:
            title: Título principal
            subtitle: Subtítulo opcional
            
        Returns:
            str: HTML del header
        """
        subtitle_html = f'<p class="text-secondary">{subtitle}</p>' if subtitle else ''
        
        return f"""
        <div class="section-header animate-fade-in-up">
            <h2 class="text-gradient">{title}</h2>
            {subtitle_html}
        </div>
        """


# Instancia global del cargador
css_loader = CSSLoader()


# Funciones de conveniencia para usar directamente
def load_css(force_reload: bool = False) -> bool:
    """Carga el CSS principal"""
    return css_loader.load_main_css(force_reload)


def load_component_css(component_type: str) -> bool:
    """Carga CSS para un componente específico"""
    return css_loader.load_component_styles(component_type)


def inject_css(css_string: str, identifier: str = None) -> bool:
    """Inyecta CSS personalizado"""
    return css_loader.inject_custom_css(css_string, identifier)


def glass_card(content: str, css_class: str = "glass-card") -> None:
    """Renderiza una tarjeta glass en Streamlit"""
    html = css_loader.create_glass_card(content, css_class)
    st.markdown(html, unsafe_allow_html=True)


def metric_card(title: str, value: str, change: float = None, icon: str = None) -> None:
    """Renderiza una tarjeta de métrica en Streamlit"""
    html = css_loader.create_metric_card(title, value, change, icon)
    st.markdown(html, unsafe_allow_html=True)


def section_header(title: str, subtitle: str = None) -> None:
    """Renderiza un header de sección en Streamlit"""
    html = css_loader.create_section_header(title, subtitle)
    st.markdown(html, unsafe_allow_html=True)


# Decorador para cargar CSS automáticamente
def with_css(component_type: str = "complete"):
    """
    Decorador que carga CSS automáticamente antes de ejecutar una función
    
    Args:
        component_type: Tipo de componente CSS a cargar
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            load_component_css(component_type)
            return func(*args, **kwargs)
        return wrapper
    return decorator