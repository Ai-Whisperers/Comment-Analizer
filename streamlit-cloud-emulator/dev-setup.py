#!/usr/bin/env python3
"""
Development Environment Setup Script
Unifies local and Streamlit Cloud environments
"""

import os
import sys
import subprocess
import json
from pathlib import Path

class DevEnvironmentSetup:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.requirements_file = self.project_root / "requirements.txt"
        self.env_file = self.project_root / ".env"
        self.secrets_file = self.project_root / ".streamlit" / "secrets.toml"
    
    def check_python_version(self):
        """Ensure Python 3.12 is being used"""
        version = sys.version_info
        if version.major != 3 or version.minor != 12:
            print(f"⚠️ Warning: Using Python {version.major}.{version.minor}, but Streamlit Cloud uses Python 3.12")
            print("Consider using Python 3.12 for better compatibility")
        else:
            print("✅ Python 3.12 detected - matches Streamlit Cloud")
    
    def install_requirements(self):
        """Install requirements matching Streamlit Cloud"""
        print("📦 Installing requirements...")
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", str(self.requirements_file)
            ], check=True, capture_output=True, text=True)
            print("✅ Requirements installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error installing requirements: {e}")
            return False
        return True
    
    def validate_environment_files(self):
        """Validate that environment files are properly configured"""
        issues = []
        
        # Check .env file
        if not self.env_file.exists():
            issues.append("❌ .env file not found")
        else:
            with open(self.env_file, 'r') as f:
                env_content = f.read()
                if 'OPENAI_API_KEY=' not in env_content or 'sk-' not in env_content:
                    issues.append("⚠️ OPENAI_API_KEY not properly set in .env")
        
        # Check secrets.toml file
        if not self.secrets_file.exists():
            issues.append("❌ .streamlit/secrets.toml file not found")
        else:
            with open(self.secrets_file, 'r') as f:
                secrets_content = f.read()
                if 'OPENAI_API_KEY' not in secrets_content:
                    issues.append("⚠️ OPENAI_API_KEY not set in secrets.toml")
        
        if issues:
            print("🚨 Environment Configuration Issues:")
            for issue in issues:
                print(f"  {issue}")
            return False
        else:
            print("✅ Environment files properly configured")
            return True
    
    def test_resource_limits(self):
        """Test if app respects Streamlit Cloud resource limits"""
        print("🧪 Testing resource limit compatibility...")
        
        try:
            # Import the unified config
            sys.path.insert(0, str(self.project_root))
            from config import config, is_streamlit_cloud
            
            print(f"Environment detected: {'Streamlit Cloud' if is_streamlit_cloud() else 'Local'}")
            print(f"Max batch size: {config.get('MAX_COMMENTS_PER_BATCH')}")
            print(f"Cache TTL: {config.get('CACHE_TTL_SECONDS')}s")
            print(f"Memory optimization: {config.get('ENABLE_MEMORY_OPTIMIZATION')}")
            
            return True
        except Exception as e:
            print(f"❌ Error testing configuration: {e}")
            return False
    
    def run_docker_mode(self):
        """Run in Docker mode to simulate Streamlit Cloud"""
        print("🐳 Starting Docker environment (simulates Streamlit Cloud)...")
        
        if not Path("docker-compose.yml").exists():
            print("❌ docker-compose.yml not found")
            return False
        
        try:
            subprocess.run(["docker-compose", "up", "--build", "-d"], check=True)
            print("✅ Docker environment started successfully")
            print("🌐 App available at: http://localhost:8501")
            print("📊 Resource limits: 1GB RAM, 1 CPU (matches Streamlit Cloud)")
            return True
        except subprocess.CalledProcessError:
            print("❌ Error starting Docker environment")
            print("Make sure Docker is installed and running")
            return False
    
    def run_local_mode(self):
        """Run in local mode with development settings"""
        print("💻 Starting local development environment...")
        
        try:
            subprocess.run([
                sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
                "--server.address", "localhost",
                "--server.port", "8501"
            ], check=True)
        except KeyboardInterrupt:
            print("\n👋 Shutting down development server...")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error running local server: {e}")
            return False
        return True
    
    def setup_environment(self):
        """Complete environment setup"""
        print("🚀 Setting up unified development environment...")
        print("=" * 50)
        
        steps = [
            ("Checking Python version", self.check_python_version),
            ("Installing requirements", self.install_requirements),
            ("Validating environment files", self.validate_environment_files),
            ("Testing resource limits", self.test_resource_limits),
        ]
        
        for step_name, step_func in steps:
            print(f"\n{step_name}...")
            if not step_func():
                print(f"❌ Failed at: {step_name}")
                return False
        
        print("\n✅ Environment setup complete!")
        print("\nAvailable modes:")
        print("  1. Local mode: python dev-setup.py --local")
        print("  2. Docker mode (simulates cloud): python dev-setup.py --docker")
        return True

def main():
    setup = DevEnvironmentSetup()
    
    if len(sys.argv) > 1:
        if "--local" in sys.argv:
            setup.run_local_mode()
        elif "--docker" in sys.argv:
            setup.run_docker_mode()
        elif "--setup" in sys.argv:
            setup.setup_environment()
        else:
            print("Usage: python dev-setup.py [--setup|--local|--docker]")
    else:
        setup.setup_environment()

if __name__ == "__main__":
    main()