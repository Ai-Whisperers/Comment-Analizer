"""
Streamlit Cloud Entry Point - Personal Paraguay Comment Analyzer
Robust entry point with multiple fallback strategies
"""

import sys
import os
from pathlib import Path

# Debug: Print current working directory and Python path
print(f"Current working directory: {os.getcwd()}")
print(f"Python path: {sys.path[:3]}...")  # First 3 entries
print(f"__file__ location: {__file__}")

# Multiple path setup strategies for maximum compatibility
current_dir = Path(__file__).parent.absolute()
src_dir = current_dir / "src"

print(f"Attempting to add to path: {src_dir}")

# Add both possible path locations
paths_to_add = [
    str(src_dir),
    str(current_dir / "src"),
    str(current_dir),
    os.path.join(os.path.dirname(__file__), "src")
]

for path in paths_to_add:
    if path not in sys.path:
        sys.path.insert(0, path)

print(f"Updated Python path (first 5): {sys.path[:5]}")

# Prevent infinite import loops with session-based guard
import streamlit as st

# Initialize session state early to prevent re-imports
if 'app_initialized' not in st.session_state:
    st.session_state.app_initialized = False

if not st.session_state.app_initialized:
    print("🚀 First-time app initialization...")
    
    # Import main application with comprehensive fallback
    import_success = False

    # Strategy 1: Try direct src import
    try:
        print("Attempting: from src.main import *")
        from src.main import *
        import_success = True
        print("✅ SUCCESS: src.main import worked")
        print("🎯 Main module imported - setting initialization flag")
        st.session_state.app_initialized = True
    except ImportError as e:
        print(f"❌ src.main import failed: {e}")
    except SyntaxError as syntax_error:
        print(f"🚨 SYNTAX ERROR in src/main.py: {syntax_error}")
        print("🔧 Critical: main.py has syntax errors preventing import")
        print(f"🔍 Error details: {syntax_error}")
    except Exception as e:
        print(f"🚨 UNEXPECTED ERROR during main execution: {e}")
        import traceback
        print(f"🔍 Full traceback: {traceback.format_exc()}")
else:
    print("✅ App already initialized - skipping re-import")
    import_success = True

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