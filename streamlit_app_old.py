"""
Streamlit Cloud Entry Point - Personal Paraguay Comment Analyzer
Production-ready entry point with error boundaries and health checks
"""

import sys
import os
import traceback
from pathlib import Path
import logging

# Configure logging for deployment debugging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Production debugging info (reduced verbosity)
logger.info(f"Starting Streamlit app from: {__file__}")
logger.info(f"Working directory: {os.getcwd()}")

# Robust path setup for Streamlit Cloud
current_dir = Path(__file__).parent.absolute()
src_dir = current_dir / "src"

# Ensure src directory exists
if not src_dir.exists():
    logger.error(f"Source directory not found: {src_dir}")
    sys.exit(1)

# Add to Python path
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

logger.info(f"Added to Python path: {src_dir}")

# Prevent infinite import loops with session-based guard
import streamlit as st

# Initialize session state early to prevent re-imports
if 'app_initialized' not in st.session_state:
    st.session_state.app_initialized = False

if not st.session_state.app_initialized:
    logger.info("First-time app initialization...")
    
    # Error boundary for main application import
    import_success = False
    
    try:
        logger.info("Attempting main application import...")
        # CRITICAL FIX: Import main as module instead of wildcard to prevent execution
        import src.main as main_module
        import_success = True
        st.session_state.app_initialized = True
        logger.info("✅ Main application imported successfully")
        
    except ImportError as e:
        logger.error(f"Import failed: {e}")
        st.error("🚨 Application failed to load due to missing dependencies")
        st.error(f"Details: {str(e)}")
        
    except SyntaxError as syntax_error:
        logger.error(f"Syntax error in main application: {syntax_error}")
        st.error("🚨 CRITICAL: Application code has syntax errors")
        st.error(f"Error: {syntax_error}")
        st.error("Please contact support - this is a deployment issue")
        
    except Exception as e:
        logger.error(f"Unexpected error during initialization: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        st.error("🚨 Application initialization failed")
        st.error("This appears to be a deployment or configuration issue")
        with st.expander("Technical Details"):
            st.code(str(e))
            st.code(traceback.format_exc())
else:
    import_success = True
    logger.info("App already initialized")

# Strategy 2: Try without src prefix (only if first strategy failed)
if not import_success and not st.session_state.app_initialized:
    try:
        print("Attempting: from main import *")
        from main import *
        import_success = True
        st.session_state.app_initialized = True
        print("✅ SUCCESS: main import worked")
    except ImportError as e:
        print(f"❌ main import failed: {e}")
    except SyntaxError as syntax_error:
        print(f"🚨 SYNTAX ERROR in main.py: {syntax_error}")
        print("🔧 Check main.py for syntax issues (missing try/except blocks, indentation)")
    except Exception as e:
        print(f"🚨 UNEXPECTED ERROR during fallback import: {e}")
        import traceback
        print(f"🔍 Fallback traceback: {traceback.format_exc()}")

# Strategy 3: Try explicit path import (only if previous strategies failed)
if not import_success and not st.session_state.app_initialized:
    try:
        print("Attempting: explicit path import")
        main_path = src_dir / "main.py"
        spec = __import__('importlib.util').util.spec_from_file_location("main", main_path)
        main_module = __import__('importlib.util').util.module_from_spec(spec)
        spec.loader.exec_module(main_module)
        import_success = True
        st.session_state.app_initialized = True
        print("✅ SUCCESS: explicit import worked")
    except Exception as e:
        print(f"❌ explicit import failed: {e}")

if not import_success:
    import streamlit as st
    st.error("🚨 CRITICAL: Could not import main application")
    st.error("This is a deployment configuration issue.")
    st.info("Check the Streamlit Cloud logs for import error details.")
    st.stop()

print("🚀 Entry point completed successfully")