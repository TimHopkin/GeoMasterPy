# 🚀 GeoMasterPy Web App Deployment Guide

Deploy GeoMasterPy as an interactive web application using Streamlit!

## 🌐 Deployment Options

### Option 1: Streamlit Community Cloud (Recommended)

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial GeoMasterPy web app"
   git branch -M main
   git remote add origin https://github.com/yourusername/geomasterpy.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select your repository
   - Set main file: `streamlit_app.py`
   - Set requirements file: `requirements_streamlit.txt`
   - Deploy!

3. **Your app will be live at:**
   `https://yourusername-geomasterpy-streamlit-app-abc123.streamlit.app`

### Option 2: Heroku Deployment

1. **Create Heroku files:**
   ```bash
   # Create Procfile
   echo "web: streamlit run streamlit_app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile
   
   # Create runtime.txt
   echo "python-3.11.0" > runtime.txt
   ```

2. **Deploy to Heroku:**
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### Option 3: Local Development

1. **Install Streamlit dependencies:**
   ```bash
   pip install -r requirements_streamlit.txt
   ```

2. **Run locally:**
   ```bash
   streamlit run streamlit_app.py
   ```

3. **Open in browser:**
   `http://localhost:8501`

## 📁 Required Files for Deployment

- ✅ `streamlit_app.py` - Main web application
- ✅ `requirements_streamlit.txt` - Python dependencies
- ✅ `.streamlit/config.toml` - Streamlit configuration
- ✅ `geomasterpy/` - Core library package

## 🔧 Configuration

### Environment Variables

For production deployment, set these environment variables:

```bash
# Optional: Earth Engine service account (for server-side auth)
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json

# Optional: Custom app settings
STREAMLIT_THEME_PRIMARY_COLOR=#4CAF50
STREAMLIT_SERVER_PORT=8501
```

### Streamlit Secrets

For sensitive data, use Streamlit secrets (`secrets.toml`):

```toml
[gee]
service_account_key = "your-service-account-json-string"

[app]
title = "GeoMasterPy Interactive"
```

## 🌍 Features Available in Web App

### ✅ Working Without Authentication
- 🔍 Data catalog search
- 🔄 JavaScript to Python converter
- 📊 Sample visualizations
- 📚 Documentation
- 🗺️ Basic mapping

### ✅ Full Features (With Earth Engine Auth)
- 🛰️ Real satellite data
- 📈 Time series analysis
- 🏷️ Image classification
- 💾 Data export
- 🖼️ Publication maps

## 🚀 Quick Deploy Script

Save this as `deploy.sh`:

```bash
#!/bin/bash

echo "🚀 Deploying GeoMasterPy Web App"

# Initialize git if needed
if [ ! -d ".git" ]; then
    git init
    git add .
    git commit -m "Initial commit: GeoMasterPy web app"
fi

# Add all changes
git add .
git commit -m "Update GeoMasterPy web app"

# Push to GitHub
echo "📤 Pushing to GitHub..."
git push origin main

echo "✅ Pushed to GitHub!"
echo "🌐 Now deploy on Streamlit Cloud: https://share.streamlit.io"
echo "📱 Or run locally: streamlit run streamlit_app.py"
```

Make it executable and run:
```bash
chmod +x deploy.sh
./deploy.sh
```

## 📱 Mobile Responsiveness

The web app is designed to work on:
- 💻 Desktop computers
- 📱 Mobile phones
- 📟 Tablets

## 🔒 Security Considerations

1. **Never commit API keys** to public repositories
2. **Use environment variables** for sensitive data
3. **Enable HTTPS** in production
4. **Limit Earth Engine quotas** for public apps

## 🎯 Customization

### Change App Theme
Edit `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#YOUR_COLOR"
backgroundColor = "#YOUR_BG_COLOR"
```

### Add Custom Features
Extend `streamlit_app.py` with:
- New analysis tools
- Additional visualizations
- Custom data sources
- User authentication

## 📊 Analytics & Monitoring

Add analytics to track usage:

```python
# Add to streamlit_app.py
import streamlit as st

# Google Analytics (optional)
st.components.v1.html("""
<!-- Google Analytics code -->
""")

# Simple usage tracking
if 'page_views' not in st.session_state:
    st.session_state.page_views = 0
st.session_state.page_views += 1
```

## 🛠️ Troubleshooting

### Common Issues:

1. **"Module not found" errors:**
   - Check `requirements_streamlit.txt`
   - Ensure all dependencies are listed

2. **Memory limits on cloud platforms:**
   - Optimize image processing
   - Use sampling for large datasets

3. **Earth Engine authentication:**
   - Use service account for server deployment
   - Provide clear auth instructions for users

## 🌟 Production Checklist

- [ ] Repository is public on GitHub
- [ ] All secrets removed from code
- [ ] Requirements file is complete
- [ ] App tested locally
- [ ] Mobile responsiveness verified
- [ ] Error handling implemented
- [ ] Usage analytics added (optional)
- [ ] Custom domain configured (optional)

## 🔗 Useful Links

- [Streamlit Documentation](https://docs.streamlit.io)
- [Streamlit Community Cloud](https://share.streamlit.io)
- [Google Earth Engine](https://earthengine.google.com)
- [GeoMasterPy GitHub](https://github.com/yourusername/geomasterpy)

---

**🎉 Your GeoMasterPy web app will be accessible to anyone with an internet connection!**