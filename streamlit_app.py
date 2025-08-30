"""
Clean Streamlit Cloud Entry Point - Comment Analyzer
Fixes static HTML rendering by ensuring proper Streamlit context
"""

import sys
import os
from pathlib import Path

# Add src to Python path
current_dir = Path(__file__).parent.absolute()
src_dir = current_dir / "src"

if src_dir.exists() and str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

# CRITICAL FIX: Import main directly without wildcard
# This prevents namespace pollution and module-level execution issues
import main