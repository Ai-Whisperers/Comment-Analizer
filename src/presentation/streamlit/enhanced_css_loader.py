"""
Enhanced CSS Loader with Glassmorphism Support
Ensures all CSS files from static folder are properly loaded
"""
import streamlit as st
from pathlib import Path
from typing import List, Optional, Dict
import logging

logger = logging.getLogger(__name__)


class EnhancedCSSLoader:
    """
    Enhanced CSS loader that ensures glassmorphism and all styles are loaded
    """
    
    # CSS loading priority order
    CSS_LOAD_ORDER = [
        'css/base/variables.css',
        'css/base/reset.css', 
        'css/glassmorphism.css',  # Load glassmorphism early
        'css/core.css',
        'css/components/streamlit-core.css',
        'css/components/forms.css',
        'css/components/charts.css',
        'css/components/layout.css',
        'css/animations/keyframes.css',
        'css/utils/utilities.css',
        'main.css',  # Main CSS that imports everything
        'styles.css'  # Legacy styles for backward compatibility
    ]
    
    def __init__(self, static_path: str = "static"):
        """Initialize the enhanced CSS loader"""
        self.static_path = Path(static_path)
        self._loaded_styles: Dict[str, bool] = {}
        self._css_cache: Dict[str, str] = {}
        
    def load_all_styles(self, force_reload: bool = False) -> bool:
        """
        Load all CSS files in the correct order
        
        Args:
            force_reload: Force reload even if already loaded
            
        Returns:
            bool: True if all styles loaded successfully
        """
        if not force_reload and self._loaded_styles.get('all_styles'):
            return True
            
        success = True
        loaded_files = []
        
        # Load CSS files in priority order
        for css_file in self.CSS_LOAD_ORDER:
            file_path = self.static_path / css_file
            
            if file_path.exists():
                if self._load_css_file(file_path):
                    loaded_files.append(css_file)
                else:
                    logger.warning(f"Failed to load {css_file}")
                    success = False
            else:
                # Try without css/ prefix for root files
                root_path = self.static_path / css_file.replace('css/', '')
                if root_path.exists() and self._load_css_file(root_path):
                    loaded_files.append(css_file)
        
        if loaded_files:
            logger.info(f"✅ Loaded {len(loaded_files)} CSS files")
            self._loaded_styles['all_styles'] = True
        else:
            logger.error("❌ No CSS files loaded")
            success = False
            
        return success
    
    def load_glassmorphism(self, force_reload: bool = False) -> bool:
        """
        Load glassmorphism CSS specifically
        
        Args:
            force_reload: Force reload even if already loaded
            
        Returns:
            bool: True if loaded successfully
        """
        if not force_reload and self._loaded_styles.get('glassmorphism'):
            return True
            
        # Load dependencies first
        deps_loaded = True
        dependencies = [
            self.static_path / 'css' / 'base' / 'variables.css',
            self.static_path / 'css' / 'glassmorphism.css'
        ]
        
        for dep in dependencies:
            if dep.exists():
                if not self._load_css_file(dep):
                    deps_loaded = False
                    
        if deps_loaded:
            self._loaded_styles['glassmorphism'] = True
            logger.info("✅ Glassmorphism styles loaded")
            
            # Also inject inline glassmorphism for immediate availability
            self._inject_inline_glassmorphism()
            
        return deps_loaded
    
    def _load_css_file(self, file_path: Path) -> bool:
        """
        Load a single CSS file
        
        Args:
            file_path: Path to CSS file
            
        Returns:
            bool: True if loaded successfully
        """
        try:
            # Check cache first
            cache_key = str(file_path)
            
            if cache_key not in self._css_cache:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self._css_cache[cache_key] = f.read()
            
            css_content = self._css_cache[cache_key]
            
            # Process @import statements to inline them
            css_content = self._process_imports(css_content, file_path.parent)
            
            # Inject CSS
            st.markdown(f'<style>{css_content}</style>', unsafe_allow_html=True)
            return True
            
        except Exception as e:
            logger.error(f"Error loading {file_path}: {str(e)}")
            return False
    
    def _process_imports(self, css_content: str, base_path: Path) -> str:
        """
        Process @import statements and inline them
        
        Args:
            css_content: CSS content with potential @import statements
            base_path: Base path for relative imports
            
        Returns:
            str: CSS with imports inlined
        """
        import re
        
        # Find all @import statements
        import_pattern = r'@import\s+url\([\'"]?([^\'"\)]+)[\'"]?\);?'
        
        def replace_import(match):
            import_path = match.group(1)
            
            # Handle relative paths
            if import_path.startswith('./'):
                import_path = import_path[2:]
            
            import_file = base_path / import_path
            
            if import_file.exists():
                try:
                    with open(import_file, 'r', encoding='utf-8') as f:
                        return f.read()
                except Exception:
                    return match.group(0)  # Keep original if can't load
            
            return match.group(0)  # Keep original if file doesn't exist
        
        return re.sub(import_pattern, replace_import, css_content)
    
    def _inject_inline_glassmorphism(self):
        """Inject inline glassmorphism CSS for immediate availability"""
        inline_glass = """
        <style>
        /* Inline Glassmorphism - Immediate load */
        .glass, .glass-card {
            background: rgba(255, 255, 255, 0.08) !important;
            backdrop-filter: blur(16px) !important;
            -webkit-backdrop-filter: blur(16px) !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            border-radius: 16px !important;
            box-shadow: 0 2px 8px rgba(139, 92, 246, 0.08) !important;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        }
        
        .glass:hover, .glass-card:hover {
            background: rgba(255, 255, 255, 0.12) !important;
            border-color: rgba(255, 255, 255, 0.25) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 24px rgba(139, 92, 246, 0.12) !important;
        }
        
        /* Glass elevated for special components */
        .glass-elevated {
            background: linear-gradient(135deg, 
                rgba(255, 255, 255, 0.1), 
                rgba(255, 255, 255, 0.05)) !important;
            backdrop-filter: blur(20px) !important;
            -webkit-backdrop-filter: blur(20px) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 24px !important;
            box-shadow: 
                0 8px 32px rgba(139, 92, 246, 0.2),
                inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
        }
        
        /* Ensure Streamlit components get glass effect */
        .stButton > button {
            background: linear-gradient(135deg, #8B5CF6, #06B6D4) !important;
            backdrop-filter: blur(10px) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
            color: white !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 20px rgba(139, 92, 246, 0.25) !important;
        }
        
        /* Glass metrics */
        [data-testid="metric-container"] {
            background: rgba(255, 255, 255, 0.05) !important;
            backdrop-filter: blur(10px) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
            padding: 1rem !important;
        }
        
        /* Glass expandable */
        .streamlit-expanderHeader {
            background: rgba(255, 255, 255, 0.05) !important;
            backdrop-filter: blur(8px) !important;
            border-radius: 8px !important;
        }
        </style>
        """
        st.markdown(inline_glass, unsafe_allow_html=True)
    
    def ensure_styles_loaded(self) -> bool:
        """
        Ensure all necessary styles are loaded
        Called at the start of each page
        
        Returns:
            bool: True if styles are ready
        """
        # Check if already loaded in session
        if 'css_loaded' in st.session_state and st.session_state.css_loaded:
            return True
            
        # Load everything
        success = self.load_all_styles()
        
        if success:
            st.session_state.css_loaded = True
            
        return success
    
    def inject_page_specific_css(self, page_name: str):
        """
        Inject page-specific CSS if needed
        
        Args:
            page_name: Name of the page (e.g., 'upload', 'main')
        """
        page_css = {
            'upload': """
                /* Upload page specific styles */
                [data-testid="stFileUploader"] {
                    background: rgba(255, 255, 255, 0.05) !important;
                    backdrop-filter: blur(10px) !important;
                    border: 2px dashed rgba(139, 92, 246, 0.3) !important;
                    border-radius: 16px !important;
                    padding: 2rem !important;
                    transition: all 0.3s ease !important;
                }
                
                [data-testid="stFileUploader"]:hover {
                    border-color: rgba(139, 92, 246, 0.6) !important;
                    background: rgba(255, 255, 255, 0.08) !important;
                }
            """,
            'main': """
                /* Main page specific styles */
                .main-header {
                    background: linear-gradient(135deg, 
                        rgba(139, 92, 246, 0.1),
                        rgba(6, 182, 212, 0.1)) !important;
                    backdrop-filter: blur(20px) !important;
                    padding: 2rem !important;
                    border-radius: 20px !important;
                    margin-bottom: 2rem !important;
                }
            """
        }
        
        if page_name in page_css:
            st.markdown(f'<style>{page_css[page_name]}</style>', unsafe_allow_html=True)


# Global instance
enhanced_css_loader = EnhancedCSSLoader()


# Convenience functions
def ensure_css_loaded() -> bool:
    """Ensure all CSS is loaded"""
    return enhanced_css_loader.ensure_styles_loaded()


def load_glassmorphism() -> bool:
    """Load glassmorphism styles specifically"""
    return enhanced_css_loader.load_glassmorphism()


def inject_page_css(page_name: str):
    """Inject page-specific CSS"""
    enhanced_css_loader.inject_page_specific_css(page_name)