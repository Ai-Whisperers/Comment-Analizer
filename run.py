#!/usr/bin/env python
"""
Entry point to run the Comment Analyzer application
"""

import sys
from pathlib import Path

# Add src directory to path so imports work
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Import and run the main app directly
from main import *