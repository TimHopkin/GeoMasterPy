#!/usr/bin/env python3
"""
Simple and reliable GeoMasterPy app launcher
"""
import os
import sys

def main():
    """Start the GeoMasterPy Streamlit app"""
    
    print("🌍 GeoMasterPy - Starting App...")
    print("📍 URL: http://localhost:8501")
    print("⚠️  Press Ctrl+C to stop")
    print("-" * 40)
    
    # Change to app directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Use python -m streamlit to ensure it finds the module
    os.system("python3 -m streamlit run streamlit_app.py")

if __name__ == "__main__":
    main()