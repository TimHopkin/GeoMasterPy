#!/bin/bash

# GeoMasterPy Land App - Fixed Version
# Single-screen mapping view with no scrolling issues

echo "🌱 Starting GeoMasterPy Land App - FIXED VERSION"
echo "✅ Single-screen mapping view (no scrolling)"
echo "✅ Exact Land App HTML specification"
echo "✅ Tab navigation at top"
echo "✅ Working polygon drawing tools"
echo ""
echo "🔗 Opening browser at http://localhost:8503"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Change to the app directory
cd "$(dirname "$0")"

# Run the fixed Streamlit app on port 8503
streamlit run streamlit_land_app_fixed.py --server.port 8503 --server.address localhost --browser.gatherUsageStats false