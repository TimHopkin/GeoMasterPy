#!/bin/bash

# GeoMasterPy Land App v2 Launcher
# Run the exact Land App HTML design replica

echo "🌱 Starting GeoMasterPy Land App v2..."
echo "🎨 Exact Land App HTML design with working drawing tools"
echo "🔗 Opening browser at http://localhost:8502"
echo ""
echo "Features:"
echo "  ✅ Pixel-perfect Land App UI"
echo "  ✅ Working polygon drawing tools"
echo "  ✅ OpenStreetMap integration"
echo "  ✅ Seamless Mapping ↔ Analytics switching"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Change to the app directory
cd "$(dirname "$0")"

# Run the Streamlit app on port 8502 to avoid conflicts
streamlit run streamlit_land_app_v2.py --server.port 8502 --server.address localhost --browser.gatherUsageStats false