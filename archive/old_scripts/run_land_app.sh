#!/bin/bash

# GeoMasterPy Land App Launcher
# Run the new Land App-style interface

echo "🌱 Starting GeoMasterPy Land App..."
echo "🔗 Opening browser at http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Change to the app directory
cd "$(dirname "$0")"

# Run the Streamlit app
streamlit run streamlit_land_app.py --server.port 8501 --server.address localhost --browser.gatherUsageStats false