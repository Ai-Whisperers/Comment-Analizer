#!/usr/bin/env python3
"""
Health Check Endpoint for Streamlit Cloud Deployment
Provides basic health check functionality for monitoring and load balancers
"""

import sys
import os
import json
from datetime import datetime
from pathlib import Path

def check_system_health():
    """Perform basic system health checks"""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "checks": {}
    }
    
    try:
        # Check if main modules can be imported
        sys.path.insert(0, str(Path(__file__).parent / "src"))
        
        # Test critical imports
        try:
            import streamlit as st
            health_status["checks"]["streamlit"] = "ok"
        except Exception as e:
            health_status["checks"]["streamlit"] = f"error: {str(e)}"
            health_status["status"] = "unhealthy"
        
        try:
            import pandas as pd
            health_status["checks"]["pandas"] = "ok"
        except Exception as e:
            health_status["checks"]["pandas"] = f"error: {str(e)}"
            health_status["status"] = "unhealthy"
        
        try:
            from src.config import Config
            health_status["checks"]["config"] = "ok"
        except Exception as e:
            health_status["checks"]["config"] = f"error: {str(e)}"
            health_status["status"] = "degraded"
        
        # Check file system access
        try:
            test_path = Path(__file__).parent / "src"
            if test_path.exists():
                health_status["checks"]["filesystem"] = "ok"
            else:
                health_status["checks"]["filesystem"] = "src directory not found"
                health_status["status"] = "unhealthy"
        except Exception as e:
            health_status["checks"]["filesystem"] = f"error: {str(e)}"
            health_status["status"] = "unhealthy"
        
        # Check memory usage
        try:
            import psutil
            memory = psutil.virtual_memory()
            if memory.percent < 90:
                health_status["checks"]["memory"] = f"ok ({memory.percent:.1f}% used)"
            else:
                health_status["checks"]["memory"] = f"high ({memory.percent:.1f}% used)"
                health_status["status"] = "degraded"
        except Exception as e:
            health_status["checks"]["memory"] = f"unavailable: {str(e)}"
        
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["error"] = str(e)
    
    return health_status

def main():
    """Main health check function"""
    health = check_system_health()
    
    # Print JSON for programmatic access
    if len(sys.argv) > 1 and sys.argv[1] == "--json":
        print(json.dumps(health, indent=2))
    else:
        # Human-readable output
        print(f"Health Status: {health['status'].upper()}")
        print(f"Timestamp: {health['timestamp']}")
        print("\nChecks:")
        for check, result in health.get('checks', {}).items():
            status_emoji = "✅" if result == "ok" or result.startswith("ok") else "❌"
            print(f"  {status_emoji} {check}: {result}")
        
        if 'error' in health:
            print(f"\nError: {health['error']}")
    
    # Exit with appropriate code
    if health['status'] == 'healthy':
        sys.exit(0)
    elif health['status'] == 'degraded':
        sys.exit(1)
    else:  # unhealthy
        sys.exit(2)

if __name__ == "__main__":
    main()