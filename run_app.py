#!/usr/bin/env python3
"""
Reliable launcher for GeoMasterPy Streamlit app
"""
import subprocess
import sys
import os

def main():
    """Launch the Streamlit app with proper configuration"""
    
    # Get the directory where this script is located
    app_dir = os.path.dirname(os.path.abspath(__file__))
    app_file = os.path.join(app_dir, "streamlit_app.py")
    
    # Set environment variables to skip Streamlit setup
    env = os.environ.copy()
    env['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
    
    # Streamlit command with configuration
    cmd = [
        sys.executable, "-m", "streamlit", "run", 
        app_file,
        "--server.port", "8501",
        "--server.address", "0.0.0.0",
        "--server.headless", "false",
        "--browser.gatherUsageStats", "false",
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false"
    ]
    
    print("🚀 Starting GeoMasterPy Streamlit App...")
    print("📍 URL: http://localhost:8501")
    print("⚠️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Run the command with environment variables
        subprocess.run(cmd, cwd=app_dir, env=env, check=True)
    except KeyboardInterrupt:
        print("\n👋 Shutting down GeoMasterPy app...")
    except Exception as e:
        print(f"❌ Error running app: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())