#!/usr/bin/env python
"""
Setup Verification Script for Comment Analyzer
Run this to verify your environment is properly configured
"""

import sys
import os
from pathlib import Path

def check_environment():
    """Check if environment is properly configured"""
    print("=" * 60)
    print("COMMENT ANALYZER - SETUP VERIFICATION")
    print("=" * 60)
    
    # Check Python version
    print(f"\n✓ Python Version: {sys.version}")
    
    # Check if .env exists
    env_file = Path(".env")
    if env_file.exists():
        print("✓ .env file found")
    else:
        print("✗ .env file NOT found - copy .env.template to .env")
        return False
    
    # Check OpenAI key
    try:
        from src.config import Config
        
        if Config.OPENAI_API_KEY:
            # Show partial key for verification (first 10 chars only)
            key_preview = Config.OPENAI_API_KEY[:10] + "..." if len(Config.OPENAI_API_KEY) > 10 else "KEY_TOO_SHORT"
            print(f"✓ OpenAI API Key configured (starts with: {key_preview})")
            print(f"✓ Model: {Config.OPENAI_MODEL}")
            print(f"✓ Max Tokens: {Config.OPENAI_MAX_TOKENS}")
        else:
            print("✗ OpenAI API Key NOT configured - add to .env file")
            return False
    except ImportError as e:
        print(f"✗ Error importing config: {e}")
        return False
    
    # Check required packages
    required_packages = [
        'streamlit',
        'pandas',
        'numpy',
        'openai',
        'plotly',
        'dotenv'
    ]
    
    print("\nChecking required packages:")
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'dotenv':
                __import__('dotenv')
            else:
                __import__(package)
            print(f"  ✓ {package}")
        except ImportError:
            install_name = 'python-dotenv' if package == 'dotenv' else package
            print(f"  ✗ {package} - install with: pip install {install_name}")
            missing_packages.append(install_name)
    
    # Check directories
    print("\nChecking project directories:")
    dirs_to_check = ['src', 'tests', 'data', 'outputs']
    
    for dir_name in dirs_to_check:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"  ✓ {dir_name}/")
        else:
            print(f"  ✗ {dir_name}/ - directory missing")
    
    # Summary
    print("\n" + "=" * 60)
    if missing_packages:
        print("⚠️  SETUP INCOMPLETE")
        print(f"   Install missing packages: pip install {' '.join(missing_packages)}")
    else:
        print("✅ SETUP COMPLETE - Ready to run the application!")
        print("\nTo start the application, run:")
        print("  streamlit run src/main.py")
    print("=" * 60)
    
    return len(missing_packages) == 0

if __name__ == "__main__":
    success = check_environment()
    sys.exit(0 if success else 1)