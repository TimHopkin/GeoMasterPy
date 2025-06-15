#!/usr/bin/env python3
"""
Local development runner for GeoMasterPy Streamlit app
This script helps launch the app properly for development
"""

import subprocess
import sys
import os
import time

def main():
    """Launch Streamlit app for local development"""
    
    # Change to the app directory
    app_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(app_dir)
    
    print("🚀 Starting GeoMasterPy Streamlit App...")
    print(f"📁 Working directory: {app_dir}")
    print("🌐 App will be available at: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the app")
    print("-" * 50)
    
    try:
        # Launch Streamlit
        cmd = [sys.executable, "-m", "streamlit", "run", "streamlit_app_cloud.py"]
        subprocess.run(cmd, check=True)
        
    except KeyboardInterrupt:
        print("\n⏹️  App stopped by user")
    except FileNotFoundError:
        print("❌ Streamlit not found. Install with: pip install streamlit")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting app: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()