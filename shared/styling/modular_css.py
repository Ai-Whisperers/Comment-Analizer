"""
Modular CSS Manager for Comment Analyzer
Provides proper separation of concerns with external CSS files
"""

import streamlit as st
from pathlib import Path
from typing import List, Optional, Dict
from functools import lru_cache
import logging

logger = logging.getLogger(__name__)

class ModularStyleManager:
    """
    Manages modular CSS loading with proper separation of concerns
    Replaces the monolithic CSS-in-JS approach with external files
    """
    
    def __init__(self):
        self.static_dir = Path("static/css")
        self.css_files = [
            "core.css",           # Variables, typography, base styles
            "glassmorphism.css",  # All glassmorphism and Web3 effects
        ]
        self.theme_overrides = {
            'dark': [],  # Dark theme is default in core.css
            'light': []  # Light theme overrides (if needed)
        }
    
    def initialize_styles(self, dark_mode: bool = True) -> bool:
        """
        Initialize all application styles with proper modularity
        
        Args:
            dark_mode: Whether to use dark theme (light theme not fully implemented)
            
        Returns:
            bool: True if all styles loaded successfully
        """
        success_count = 0
        total_files = len(self.css_files)
        
        st.markdown("<!-- Modular CSS Loading Start -->", unsafe_allow_html=True)
        
        # Load core CSS modules
        for css_file in self.css_files:
            if self._load_css_file(css_file):
                success_count += 1
            else:
                logger.warning(f"Failed to load CSS file: {css_file}")
        
        # Load theme-specific overrides if needed
        theme = 'dark' if dark_mode else 'light'
        for override_file in self.theme_overrides.get(theme, []):
            if self._load_css_file(override_file):
                success_count += 1
            total_files += 1
        
        # Only inject minimal theme variables if needed
        if dark_mode:
            self._inject_minimal_theme_vars()
        
        st.markdown("<!-- Modular CSS Loading Complete -->", unsafe_allow_html=True)
        
        success_rate = success_count / total_files if total_files > 0 else 0
        if success_rate < 1.0:
            st.warning(f"Some CSS files failed to load ({success_count}/{total_files} loaded)")
        
        return success_rate == 1.0
    
    def _load_css_file(self, filename: str) -> bool:
        """
        Load individual CSS file with Streamlit-compatible approach
        Uses cached file reading with minimal inline injection
        
        Args:
            filename: Name of CSS file in static/css directory
            
        Returns:
            bool: True if file loaded successfully
        """
        css_path = self.static_dir / filename
        
        # Check if file exists
        if not css_path.exists():
            logger.error(f"CSS file not found: {css_path}")
            return False
        
        try:
            # Read CSS file and inject as cached content
            css_content = self._get_cached_css_content(str(css_path))
            if css_content:
                st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
                logger.debug(f"Successfully loaded CSS: {filename}")
                return True
            else:
                logger.error(f"CSS file is empty: {filename}")
                return False
            
        except Exception as e:
            logger.error(f"Failed to load CSS file {filename}: {e}")
            return False
    
    @lru_cache(maxsize=16)
    def _get_cached_css_content(self, css_path: str) -> Optional[str]:
        """
        Get CSS file content with caching for performance
        
        Args:
            css_path: Full path to CSS file
            
        Returns:
            str: CSS content or None if failed
        """
        try:
            with open(css_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Minify CSS (remove comments and extra whitespace)
                return self._minify_css(content)
        except Exception as e:
            logger.error(f"Failed to read CSS file {css_path}: {e}")
            return None
    
    def _minify_css(self, css_content: str) -> str:
        """
        Basic CSS minification to reduce payload
        
        Args:
            css_content: Raw CSS content
            
        Returns:
            str: Minified CSS
        """
        import re
        
        # Remove comments
        css_content = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)
        
        # Remove extra whitespace
        css_content = re.sub(r'\s+', ' ', css_content)
        css_content = re.sub(r'\s*{\s*', '{', css_content)
        css_content = re.sub(r'\s*}\s*', '}', css_content)
        css_content = re.sub(r'\s*;\s*', ';', css_content)
        css_content = re.sub(r'\s*:\s*', ':', css_content)
        
        return css_content.strip()
    
    def _inject_minimal_theme_vars(self) -> None:
        """
        Inject only minimal theme variables (not full CSS)
        This maintains modularity while allowing dynamic theme switching
        """
        # Only inject truly dynamic variables (< 500 chars)
        minimal_vars = """
        <style>
        :root {
            --theme-mode: 'dark';
            --dynamic-opacity: 1.0;
        }
        </style>
        """
        st.markdown(minimal_vars, unsafe_allow_html=True)
    
    @lru_cache(maxsize=32)
    def get_css_file_info(self, filename: str) -> Dict[str, str]:
        """
        Get information about a CSS file (cached for performance)
        
        Args:
            filename: Name of CSS file
            
        Returns:
            dict: File information (size, modified time, etc.)
        """
        css_path = self.static_dir / filename
        
        if not css_path.exists():
            return {"status": "missing", "size": 0}
        
        try:
            stat = css_path.stat()
            return {
                "status": "exists",
                "size": stat.st_size,
                "modified": stat.st_mtime
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def get_diagnostics(self) -> Dict[str, any]:
        """
        Get diagnostic information about CSS loading status
        Useful for debugging styling issues
        
        Returns:
            dict: Diagnostic information
        """
        diagnostics = {
            "static_dir_exists": self.static_dir.exists(),
            "css_files": {},
            "total_css_size": 0
        }
        
        for css_file in self.css_files:
            info = self.get_css_file_info(css_file)
            diagnostics["css_files"][css_file] = info
            if info.get("size"):
                diagnostics["total_css_size"] += info["size"]
        
        return diagnostics

class LegacyFallbackManager:
    """
    Fallback to CSS-in-JS if external CSS loading fails
    Provides graceful degradation while maintaining functionality
    """
    
    @staticmethod
    @lru_cache(maxsize=4)
    def get_minimal_css(dark_mode: bool = True) -> str:
        """
        Get minimal CSS for fallback scenarios
        Much smaller than the previous monolithic approach
        
        Returns:
            str: Minimal CSS (< 5KB)
        """
        return """
        <style>
        /* Minimal Fallback CSS */
        .stApp { 
            background: linear-gradient(135deg, #0D0B14, #1A1825); 
            color: #F8FAFC;
        }
        .stButton > button {
            background: linear-gradient(135deg, #8B5CF6, #7C3AED);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0.5rem 1rem;
        }
        /* Add other critical styles as needed */
        </style>
        """
    
    @staticmethod
    def apply_fallback_styles(dark_mode: bool = True) -> None:
        """Apply fallback styles if external CSS fails"""
        st.markdown(LegacyFallbackManager.get_minimal_css(dark_mode), unsafe_allow_html=True)
        st.info("⚠️ Using fallback styling - some visual effects may be limited")

# Convenience function for easy integration
def initialize_modular_styles(dark_mode: bool = True, use_fallback: bool = True) -> bool:
    """
    Initialize modular styles with optional fallback
    
    Args:
        dark_mode: Use dark theme
        use_fallback: Apply fallback styles if external CSS fails
        
    Returns:
        bool: True if styles loaded successfully
    """
    style_manager = ModularStyleManager()
    success = style_manager.initialize_styles(dark_mode)
    
    if not success and use_fallback:
        logger.warning("External CSS failed, applying fallback styles")
        LegacyFallbackManager.apply_fallback_styles(dark_mode)
    
    return success

# For debugging and development
def show_css_diagnostics() -> None:
    """Show CSS loading diagnostics in sidebar"""
    style_manager = ModularStyleManager()
    diagnostics = style_manager.get_diagnostics()
    
    with st.sidebar:
        st.markdown("### CSS Diagnostics")
        st.json(diagnostics)