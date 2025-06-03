# 🚀 Streamlit Cloud Deployment Instructions

## Quick Deploy Settings

When deploying on [share.streamlit.io](https://share.streamlit.io):

### Required Settings:
- **Repository**: `TimHopkin/GeoMasterPy`
- **Branch**: `main`
- **Main file path**: `streamlit_app.py`
- **Python version**: `3.9` or `3.10`

### Requirements File Options:

#### Option 1: Full Features (Recommended)
**Requirements file**: `requirements_streamlit.txt`
- Includes Earth Engine support
- Full geospatial capabilities
- May take 3-5 minutes to build

#### Option 2: Minimal/Fast Deploy  
**Requirements file**: `requirements_minimal.txt`
- Core web app features only
- Faster deployment (~1-2 minutes)
- Good for testing

## 🎯 Expected Build Time
- **Minimal**: 1-2 minutes
- **Full**: 3-5 minutes (includes heavy geospatial libraries)

## 🌟 Features Available

### ✅ Always Available (Demo Mode)
- Interactive web interface
- Data catalog search
- JavaScript to Python converter
- Sample visualizations
- Documentation

### 🚀 With Earth Engine Authentication
- Real satellite data
- Live analysis tools
- Data export capabilities
- Publication maps

## 🔧 Troubleshooting

If deployment fails:

1. **Try minimal requirements first**: Use `requirements_minimal.txt`
2. **Check build logs** for specific error messages
3. **Restart deployment** if it times out

## 📱 Access Your App

Once deployed, your app will be available at:
`https://[random-url].streamlit.app`

Share this URL with anyone to let them use GeoMasterPy!