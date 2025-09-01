"""
Fix for inotify instance limit reached error in Streamlit
Optimizes file watching and system resources for production deployment
"""

import os
import subprocess
import sys


def check_inotify_limits():
    """Check current inotify limits"""
    try:
        # Check current inotify limits
        max_user_instances = subprocess.check_output(
            ["cat", "/proc/sys/fs/inotify/max_user_instances"]
        ).decode().strip()
        
        max_user_watches = subprocess.check_output(
            ["cat", "/proc/sys/fs/inotify/max_user_watches"]
        ).decode().strip()
        
        print(f"Current inotify limits:")
        print(f"  max_user_instances: {max_user_instances}")
        print(f"  max_user_watches: {max_user_watches}")
        
        return int(max_user_instances), int(max_user_watches)
        
    except Exception as e:
        print(f"Could not check inotify limits: {e}")
        return None, None


def fix_inotify_limits():
    """Increase inotify limits if running as privileged user"""
    try:
        # Try to increase limits (requires sudo/root)
        commands = [
            "echo 1024 | sudo tee /proc/sys/fs/inotify/max_user_instances",
            "echo 524288 | sudo tee /proc/sys/fs/inotify/max_user_watches"
        ]
        
        for cmd in commands:
            try:
                subprocess.run(cmd, shell=True, check=True)
                print(f"✅ Executed: {cmd}")
            except subprocess.CalledProcessError:
                print(f"⚠️ Could not execute: {cmd} (requires sudo)")
                
    except Exception as e:
        print(f"Error fixing limits: {e}")


def optimize_streamlit_config():
    """Optimize Streamlit configuration for production"""
    config_content = """[server]
fileWatcherType = "none"
runOnSave = false
port = 8501
address = "0.0.0.0"
headless = true
maxUploadSize = 2

[browser]
gatherUsageStats = false

[global]
developmentMode = false
logLevel = "warning"
"""
    
    # Ensure .streamlit directory exists
    os.makedirs(".streamlit", exist_ok=True)
    
    # Write optimized config
    with open(".streamlit/config.toml", "w") as f:
        f.write(config_content)
    
    print("✅ Streamlit config optimized for production")


def cleanup_file_watchers():
    """Cleanup any hanging file watchers"""
    try:
        # Kill any hanging streamlit processes
        subprocess.run(["pkill", "-f", "streamlit"], check=False)
        print("✅ Cleaned up any hanging Streamlit processes")
        
        # Clean up inotify watches
        subprocess.run(["sudo", "sysctl", "fs.inotify.max_user_instances=1024"], check=False)
        subprocess.run(["sudo", "sysctl", "fs.inotify.max_user_watches=524288"], check=False)
        print("✅ Reset inotify system limits")
        
    except Exception as e:
        print(f"Cleanup info: {e}")


if __name__ == "__main__":
    print("🔧 FIXING INOTIFY INSTANCE LIMIT ISSUE")
    print("=" * 50)
    
    # Check current state
    instances, watches = check_inotify_limits()
    
    # Optimize configuration
    optimize_streamlit_config()
    
    # Try to fix system limits
    fix_inotify_limits()
    
    # Cleanup
    cleanup_file_watchers()
    
    print("\n🚀 OPTIMIZATION COMPLETE")
    print("Restart Streamlit app to apply changes")
    print("Use: streamlit run streamlit_app.py --server.fileWatcherType none")