#!/bin/bash

# GeoMasterPy Streamlit App Launcher
# This script provides a reliable way to run the app locally

echo "🌍 GeoMasterPy - Interactive Geospatial Analysis Tool"
echo "=================================================="
echo ""

# Check if we're in the right directory
if [ ! -f "streamlit_app.py" ]; then
    echo "❌ Error: streamlit_app.py not found in current directory"
    echo "Please run this script from the GeoMasterPy project directory"
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 not found"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check if streamlit is installed
if ! python3 -c "import streamlit" &> /dev/null; then
    echo "❌ Error: Streamlit not installed"
    echo "Installing Streamlit..."
    pip install streamlit
fi

# Kill any existing streamlit processes
echo "🔄 Stopping any existing Streamlit processes..."
pkill -f streamlit 2>/dev/null || true

# Wait a moment for processes to stop
sleep 2

echo "🚀 Starting GeoMasterPy Streamlit App..."
echo ""
echo "📍 The app will be available at: http://localhost:8501"
echo "🌐 Network URL will be shown below if available"
echo ""
echo "⚠️  Press Ctrl+C to stop the server"
echo "=================================================="
echo ""

# Start the streamlit app with proper configuration
python3 -m streamlit run streamlit_app.py \
    --server.port 8501 \
    --server.address 0.0.0.0 \
    --server.headless false \
    --browser.gatherUsageStats false \
    --server.enableCORS false \
    --server.enableXsrfProtection false