# 🚀 Running GeoMasterPy Locally

This guide helps you run the GeoMasterPy Streamlit app reliably on your local machine.

## Quick Start

### Option 1: Using the Launch Script (Recommended)

**On macOS/Linux:**
```bash
./run_app.sh
```

**On Windows:**
```bash
python run_app.py
```

### Option 2: Direct Streamlit Command

```bash
streamlit run streamlit_app.py --server.port 8501
```

## 📍 Accessing the App

Once started, open your web browser and go to:
- **Local URL**: http://localhost:8501
- The terminal will also show a network URL if you want to access from other devices

## 🔧 Troubleshooting

### Problem: "localhost refused to connect"

**Solution:**
1. Make sure the Streamlit process is actually running
2. Check the terminal for any error messages
3. Try restarting the app:
   ```bash
   # Kill any existing processes
   pkill -f streamlit
   
   # Wait a moment
   sleep 2
   
   # Restart
   ./run_app.sh
   ```

### Problem: Port 8501 already in use

**Solution:**
```bash
# Find what's using the port
lsof -ti:8501

# Kill the process
kill $(lsof -ti:8501)

# Or use a different port
streamlit run streamlit_app.py --server.port 8502
```

### Problem: Module import errors

**Solution:**
```bash
# Reinstall the package
pip install -e .

# Or install specific requirements
pip install -r requirements_streamlit.txt
```

## 🌟 Features Available

### 📁 Area of Interest (NEW!)
1. Navigate to "📁 Area of Interest" 
2. Load GeoJSON files from Google Drive URLs
3. Use your area for all analysis tools

### 📊 Data Analysis
- **Image Statistics**: Real Earth Engine analysis on your AOI
- **Zonal Statistics**: Multi-zone analysis within your area
- **Spectral Indices**: Time series analysis
- **Interactive Maps**: Visualize your data

### 🔗 Google Drive Integration
Supported URL formats:
- `https://drive.google.com/file/d/FILE_ID/view?usp=sharing`
- `https://drive.google.com/open?id=FILE_ID`
- `https://drive.google.com/uc?id=FILE_ID`

## 💡 Tips for Reliable Usage

1. **Keep the terminal open** - Don't close the terminal window where Streamlit is running
2. **Use the launch scripts** - They handle configuration and cleanup automatically
3. **Check for errors** - If the app stops working, check the terminal for error messages
4. **Restart when needed** - If you encounter issues, restart the app using the scripts

## 🆘 Getting Help

If you continue to have issues:

1. **Check the terminal output** for specific error messages
2. **Verify all dependencies** are installed: `pip install -r requirements_streamlit.txt`
3. **Test the basic import**: `python -c "import geomasterpy; print('OK')"`
4. **Try a different port**: Add `--server.port 8502` to the streamlit command

---

**Happy mapping! 🌍**