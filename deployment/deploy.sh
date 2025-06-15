#!/bin/bash

echo "🚀 GeoMasterPy Deployment Script"
echo "=================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit: GeoMasterPy interactive web app"
    echo "✅ Git repository initialized"
else
    echo "📝 Adding changes to Git..."
    git add .
    git commit -m "Update: GeoMasterPy web app - $(date)"
    echo "✅ Changes committed"
fi

echo ""
echo "🌐 Deployment Options:"
echo "======================"
echo ""
echo "1️⃣  STREAMLIT COMMUNITY CLOUD (Recommended)"
echo "   • Push to GitHub (if you haven't already):"
echo "     git remote add origin https://github.com/yourusername/geomasterpy.git"
echo "     git branch -M main"
echo "     git push -u origin main"
echo ""
echo "   • Then go to: https://share.streamlit.io"
echo "   • Connect your GitHub account"
echo "   • Deploy this repository"
echo "   • Main file: streamlit_app.py"
echo "   • Requirements: requirements_streamlit.txt"
echo ""
echo "2️⃣  LOCAL TESTING"
echo "   • Run: streamlit run streamlit_app.py"
echo "   • Open: http://localhost:8501"
echo ""
echo "3️⃣  HEROKU DEPLOYMENT"
echo "   • Install Heroku CLI"
echo "   • Run: heroku create your-app-name"
echo "   • Run: git push heroku main"
echo ""

# Test if we can run streamlit locally
if command -v streamlit &> /dev/null; then
    echo "✅ Streamlit is installed"
    echo ""
    echo "🚀 Want to test locally? Run:"
    echo "   streamlit run streamlit_app.py"
else
    echo "⚠️  Streamlit not found. Install with:"
    echo "   pip install streamlit"
fi

echo ""
echo "📱 Your web app includes:"
echo "========================"
echo "✅ Interactive maps with Folium"
echo "✅ Data catalog search (demo mode)"
echo "✅ JavaScript to Python converter"
echo "✅ Sample visualizations with Plotly"
echo "✅ Publication-quality map previews"
echo "✅ Complete documentation"
echo "✅ Mobile-responsive design"
echo ""
echo "🎉 GeoMasterPy is ready for the web!"