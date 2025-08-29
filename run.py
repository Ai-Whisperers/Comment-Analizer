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
    """Check if required packages are installed with user-friendly messages"""
    missing_packages = []
    
    try:
        import streamlit
    except ImportError:
        missing_packages.append("streamlit")
    
    try:
        import pandas
    except ImportError:
        missing_packages.append("pandas")
    
    try:
        import openai
    except ImportError:
        missing_packages.append("openai")
    
    if missing_packages:
        print("=" * 60)
        print("MISSING REQUIRED PACKAGES")
        print("=" * 60)
        print("")
        print("The following packages need to be installed:")
        for pkg in missing_packages:
            print(f"  - {pkg}")
        print("")
        print("To fix this:")
        print("1. Run the setup script: bootstrap.ps1 (PowerShell) or bootstrap.bat")
        print("2. Or manually install: pip install -r requirements.txt")
        print("")
        print("=" * 60)
        return False
    
    return True

def run_streamlit():
    """Run the Streamlit application with simple direct configuration"""
    # Check if main.py exists
    main_path = Path(__file__).parent / "src" / "main.py"
    if not main_path.exists():
        print("=" * 60)
        print("APPLICATION FILE NOT FOUND")
        print("=" * 60)
        print("")
        print(f"Could not find: {main_path}")
        print("")
        print("Make sure you're running this from the correct directory.")
        print("The Comment Analyzer application files should be in ./src/")
        print("=" * 60)
        return
    
    # Simple port configuration without environment variables
    port = "8501"  # Fixed default port for reliable deployment
    
    # Simplified streamlit command for better compatibility
    cmd = [
        sys.executable, "-m", "streamlit", "run", str(main_path),
        "--server.port", port,
        "--server.headless", "true",
        "--browser.gatherUsageStats", "false"
    ]
    
    try:
        print("=" * 60)
        print("🚀 STARTING COMMENT ANALYZER")
        print("=" * 60)
        print("")
        print("🌐 Application will be available at:")
        print(f"   http://localhost:{port}")
        print(f"   http://127.0.0.1:{port}")
        if port != "8501":
            print(f"   (Custom port: {port})")
        print("")
        print("✋ To stop the application: Press Ctrl+C")
        print("📁 Upload your Excel/CSV files using the web interface")
        print("")
        print("=" * 60)
        print("Starting server...")
        print("")
        
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n" + "=" * 60)
        print("🛑 SHUTTING DOWN COMMENT ANALYZER")
        print("=" * 60)
        print("\nThank you for using Comment Analyzer!")
        
    except FileNotFoundError:
        print("=" * 60)
        print("STREAMLIT NOT FOUND")
        print("=" * 60)
        print("")
        print("Streamlit is not installed or not accessible.")
        print("")
        print("To fix this:")
        print("1. Run the setup script: bootstrap.ps1 or bootstrap.bat")
        print("2. Or manually install: pip install streamlit")
        print("")
        print("=" * 60)
        
    except Exception as e:
        print("=" * 60)
        print("APPLICATION ERROR")
        print("=" * 60)
        print("")
        print(f"Error: {e}")
        print("")
        print("Troubleshooting:")
        print("1. Check that all dependencies are installed")
        print("2. Verify your OpenAI API key is set")
        print("3. Try running the bootstrap script again")
        print("")
        print("=" * 60)

def main():
    """Main entry point"""
    setup_paths()
    
    if not check_requirements():
        sys.exit(1)
    
    run_streamlit()

if __name__ == "__main__":
    main()