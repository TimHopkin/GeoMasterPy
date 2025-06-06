# Streamlit Cloud Deployment Guide

## 🚀 Quick Deploy

Your app is now ready for Streamlit Cloud! Here's how to deploy:

### Option 1: Use Cloud-Optimized Version (Recommended)

**File:** `streamlit_app_cloud.py`
**Requirements:** `requirements_cloud.txt`

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub repository
3. Set main file to: `streamlit_app_cloud.py`
4. Set requirements file to: `requirements_cloud.txt`
5. Deploy!

### Option 2: Use Safe Version (Minimal)

**File:** `streamlit_app_safe.py`
**Requirements:** Basic dependencies only

## 🔧 What Was Fixed

### 1. Dependencies Issues
- **Problem**: Heavy dependencies (cartopy, rasterio, geopandas) causing build timeouts
- **Solution**: Created `requirements_cloud.txt` with minimal, guaranteed-working dependencies

### 2. Earth Engine Authentication
- **Problem**: EE auth doesn't work on cloud without setup
- **Solution**: Added fallback demo mode and authentication guide

### 3. GeoMasterPy Import Issues
- **Problem**: Circular dependencies and installation issues
- **Solution**: Graceful fallbacks when geomasterpy isn't available

### 4. Configuration
- **Problem**: Missing Streamlit configuration
- **Solution**: Added `.streamlit/config.toml` with optimal settings

## 📋 File Structure for Deployment

```
your-repo/
├── streamlit_app_cloud.py          # 👈 Main app file (use this)
├── requirements_cloud.txt          # 👈 Dependencies (use this)
├── streamlit_app_safe.py           # Alternative minimal version
├── streamlit_app.py                # Original (for local dev)
├── requirements_streamlit.txt       # Original (heavy dependencies)
├── .streamlit/
│   ├── config.toml                 # Streamlit configuration
│   └── secrets.toml                # Earth Engine credentials (add manually)
└── README_DEPLOYMENT.md            # This file
```

## 🌐 Deployment Steps

### Step 1: Prepare Repository
1. Ensure `streamlit_app_cloud.py` is in your repo root
2. Ensure `requirements_cloud.txt` is in your repo root
3. Push to GitHub

### Step 2: Deploy to Streamlit Cloud
1. Visit [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. **Important**: Set main file to `streamlit_app_cloud.py`
6. Click "Deploy"

### Step 3: Configure (Optional)
For Earth Engine functionality:
1. Add secrets in Streamlit Cloud dashboard
2. Follow the authentication guide in the app

## ✅ What Works Out of the Box

- ✅ Interactive data analysis with sample data
- ✅ Basic mapping with Folium
- ✅ Advanced visualizations with Plotly
- ✅ Data export functionality
- ✅ Cloud-optimized performance

## 🔧 Optional: Earth Engine Setup

To enable satellite data analysis:

1. Create Google Cloud Project
2. Enable Earth Engine API
3. Create service account
4. Add credentials to Streamlit secrets
5. Follow in-app setup guide

## 🐛 Troubleshooting

### Build Fails
- Use `requirements_cloud.txt` instead of `requirements_streamlit.txt`
- Remove heavy dependencies

### App Loads but Features Missing
- Check dependency status in app
- Install missing packages via requirements

### Authentication Issues
- Earth Engine requires manual setup
- Use demo mode for testing
- Follow cloud setup guide

## 📞 Support

If you encounter issues:
1. Check the Cloud Setup Guide in the app
2. Verify your requirements file
3. Test locally first with `streamlit_app_safe.py`

## 🔗 Useful Links

- [Streamlit Cloud](https://share.streamlit.io)
- [Streamlit Documentation](https://docs.streamlit.io)
- [Earth Engine Setup](https://developers.google.com/earth-engine/guides/auth)