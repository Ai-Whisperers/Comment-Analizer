"""
Clean Streamlit Entry Point - Personal Paraguay Comment Analyzer
Prevents module-level execution issues that cause static HTML rendering
"""

import sys
import os
import logging
from pathlib import Path

# Setup logging for deployment
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add src to path
current_dir = Path(__file__).parent.absolute()
src_dir = current_dir / "src"

if src_dir.exists() and str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

# Import Streamlit
import streamlit as st

# CRITICAL: Only import main when we're actually running the app
logger.info("🚀 Starting Comment Analyzer...")

try:
    # Import the main module (this will execute the UI)
    logger.info("Loading main application...")
    import main
    logger.info("✅ Application loaded successfully")
    
except Exception as e:
    logger.error(f"Failed to load application: {e}")
    st.error("🚨 Error loading application")
    st.error(f"Details: {str(e)}")
    st.error("Please check the deployment logs for more information")