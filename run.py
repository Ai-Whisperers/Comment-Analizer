#!/usr/bin/env python
"""
Entry point to run the Comment Analyzer application
"""

import sys
import subprocess
from pathlib import Path

def main():
    """Run the Streamlit application"""
    # Get the path to main.py
    main_file = Path(__file__).parent / "src" / "main.py"
    
    # Run streamlit
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", str(main_file)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running application: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nApplication stopped.")
        sys.exit(0)

if __name__ == "__main__":
    main()