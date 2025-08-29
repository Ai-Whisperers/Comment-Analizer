"""
Streamlit Cloud Entry Point for Comment Analyzer
This file is required for Streamlit Cloud deployment
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Import and run the main application
try:
    # Try to import from src
    from src.main import *
except ImportError:
    # Fallback for different path structures
    from main import *