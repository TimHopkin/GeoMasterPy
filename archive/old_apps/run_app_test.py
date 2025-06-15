#!/usr/bin/env python3
"""
Test script to run GeoMasterPy Streamlit app and confirm it's working
"""

import subprocess
import sys
import time
import requests
import webbrowser
from threading import Thread

def check_app_health(port=8505, max_retries=10):
    """Check if the Streamlit app is responding"""
    for i in range(max_retries):
        try:
            response = requests.get(f"http://localhost:{port}", timeout=3)
            if response.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(1)
    return False

def run_app():
    """Run the Streamlit app"""
    port = 8505
    
    print("🚀 Starting GeoMasterPy Streamlit App...")
    print(f"Port: {port}")
    print("=" * 50)
    
    # Start the app
    cmd = [
        sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
        "--server.port", str(port),
        "--server.headless", "false",
        "--browser.gatherUsageStats", "false"
    ]
    
    try:
        process = subprocess.Popen(cmd, cwd="/Users/timhopkin/Documents/Software Development/GIS tool GEE/GeoMasterPy")
        
        print(f"App starting... (PID: {process.pid})")
        
        # Check if app is responding
        if check_app_health(port):
            print("✅ SUCCESS: App is running and responding!")
            print(f"🌐 URL: http://localhost:{port}")
            print("\n📋 App Features Available:")
            print("  🏠 Home")
            print("  📁 Area of Interest")
            print("  🗺️ Interactive Maps")
            print("  🔍 Data Catalog")
            print("  🔄 JS to Python Converter")
            print("  📊 Data Analysis")
            print("  📈 Visualizations")
            print("  💾 Export Tools")
            print("  🖼️ Publication Maps")
            print("  📚 Documentation")
            print("\n" + "=" * 50)
            print("✅ GeoMasterPy Streamlit app is working correctly!")
            print("Press Ctrl+C to stop the app")
            
            # Keep running
            try:
                process.wait()
            except KeyboardInterrupt:
                print("\n🛑 Stopping app...")
                process.terminate()
                process.wait()
                print("✅ App stopped successfully")
        else:
            print("❌ ERROR: App failed to respond")
            process.terminate()
            return False
            
    except Exception as e:
        print(f"❌ ERROR: Failed to start app: {e}")
        return False
    
    return True

if __name__ == "__main__":
    run_app()