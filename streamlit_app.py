"""
Streamlit Cloud Entry Point - Personal Paraguay Comment Analyzer
This is the main entry point for Streamlit Cloud deployment
"""

import sys
from pathlib import Path

# Add src directory to Python path for Streamlit Cloud compatibility
src_path = Path(__file__).parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Import and run the main application
try:
    from src.main import *
except ImportError:
    # Fallback import for different environments
    from main import *

# Streamlit Cloud will automatically run the imported main.py content