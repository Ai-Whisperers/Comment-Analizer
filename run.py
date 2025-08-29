#!/usr/bin/env python
"""
Entry point to run the Comment Analyzer application
Cross-platform support for Windows, Linux, and macOS
"""

import sys
import os
import subprocess
from pathlib import Path

def setup_paths():
    """Setup Python path for imports"""
    src_path = Path(__file__).parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

def check_requirements():
    """Check if required packages are installed"""
    try:
        import streamlit
        return True
    except ImportError:
        print("Error: Streamlit not found. Please install requirements:")
        print("pip install -r requirements.txt")
        return False

def run_streamlit():
    """Run the Streamlit application with proper configuration"""
    # Setup environment
    os.environ.setdefault('STREAMLIT_PORT', '8501')
    os.environ.setdefault('STREAMLIT_SERVER_ADDRESS', '0.0.0.0')
    
    # Get the main.py path
    main_path = Path(__file__).parent / "src" / "main.py"
    
    # Build streamlit command
    cmd = [
        sys.executable, "-m", "streamlit", "run", str(main_path),
        "--server.port", os.environ.get('STREAMLIT_PORT', '8501'),
        "--server.address", os.environ.get('STREAMLIT_SERVER_ADDRESS', '0.0.0.0'),
        "--server.headless", "true",
        "--browser.gatherUsageStats", "false",
        "--theme.base", "dark",
        "--theme.primaryColor", "#4ea4ff",
        "--theme.backgroundColor", "#0f1419",
        "--theme.secondaryBackgroundColor", "#18202a",
        "--theme.textColor", "#e6edf3"
    ]
    
    try:
        print("Starting Comment Analyzer...")
        print(f"Access at: http://localhost:{os.environ.get('STREAMLIT_PORT', '8501')}")
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\nShutting down Comment Analyzer...")
    except Exception as e:
        print(f"Error starting application: {e}")

def main():
    """Main entry point"""
    setup_paths()
    
    if not check_requirements():
        sys.exit(1)
    
    run_streamlit()

if __name__ == "__main__":
    main()