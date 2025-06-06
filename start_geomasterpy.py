#!/usr/bin/env python3
"""
GeoMasterPy Streamlit App Launcher
Ensures all dependencies are available and starts the app safely
"""

import sys
import subprocess
import importlib.util
import time

def check_dependency(name, package=None):
    """Check if a Python package is installed"""
    if package is None:
        package = name
    
    spec = importlib.util.find_spec(package)
    return spec is not None

def install_missing_dependencies():
    """Install any missing dependencies"""
    required_deps = [
        ('streamlit', 'streamlit'),
        ('plotly', 'plotly'),
        ('folium', 'folium'),
        ('streamlit-folium', 'streamlit_folium'),
        ('pandas', 'pandas'),
        ('numpy', 'numpy'),
        ('matplotlib', 'matplotlib'),
        ('requests', 'requests'),
        ('pillow', 'PIL')
    ]
    
    missing_deps = []
    
    print("🔍 Checking dependencies...")
    for pip_name, import_name in required_deps:
        if check_dependency(import_name):
            print(f"  ✅ {pip_name}")
        else:
            print(f"  ❌ {pip_name} - MISSING")
            missing_deps.append(pip_name)
    
    if missing_deps:
        print(f"\n📦 Installing missing dependencies: {', '.join(missing_deps)}")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "--user", *missing_deps
            ])
            print("✅ Dependencies installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies. Please install manually:")
            for dep in missing_deps:
                print(f"  pip install {dep}")
            return False
    else:
        print("✅ All dependencies are installed!")
    
    return True

def start_streamlit_app():
    """Start the Streamlit application"""
    print("\n🚀 Starting GeoMasterPy Streamlit App...")
    
    # Command to run streamlit
    cmd = [
        sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
        "--server.port", "8501",
        "--browser.gatherUsageStats", "false"
    ]
    
    try:
        print("Command:", " ".join(cmd))
        print("Working directory:", "/Users/timhopkin/Documents/Software Development/GIS tool GEE/GeoMasterPy")
        print("\n" + "=" * 60)
        print("🌍 GeoMasterPy - Interactive Earth Engine Tool")
        print("=" * 60)
        print("✅ Starting application...")
        print("📍 URL: http://localhost:8501")
        print("🛑 Press Ctrl+C to stop")
        print("=" * 60)
        
        # Start the app
        subprocess.run(cmd, cwd="/Users/timhopkin/Documents/Software Development/GIS tool GEE/GeoMasterPy")
        
    except KeyboardInterrupt:
        print("\n🛑 Stopping application...")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        print("\n🔧 Troubleshooting tips:")
        print("1. Ensure all dependencies are installed")
        print("2. Check that you're in the correct directory")
        print("3. Try running: pip install streamlit plotly folium streamlit-folium")
        return False
    
    return True

def main():
    """Main function"""
    print("🌍 GeoMasterPy Streamlit Launcher")
    print("=" * 40)
    
    # Check and install dependencies
    if not install_missing_dependencies():
        print("\n❌ Cannot proceed without required dependencies")
        return
    
    # Start the app
    start_streamlit_app()

if __name__ == "__main__":
    main()