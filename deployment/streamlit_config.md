# 🚀 Streamlit Deployment Configuration

## 📁 Available Streamlit Apps

### 1. 🌍 Land App (Recommended for Land Management)
**File:** `streamlit_land_app.py`  
**Purpose:** Dedicated land management application  
**Features:**
- Interactive mapping with drawing tools
- Plans management system
- Learning centre with tutorials
- Material Design 3 interface
- Offline-capable HTML interface

**Deployment:**
```bash
# Local development
streamlit run streamlit_land_app.py

# Production (Streamlit Cloud)
# Main file: streamlit_land_app.py
```

### 2. 🔬 GeoMasterPy Main App (Full Python Interface)
**File:** `streamlit_app.py`  
**Purpose:** Complete GeoMasterPy toolkit interface  
**Features:**
- Earth Engine integration
- Data analysis tools
- JavaScript to Python converter
- Publication-quality mapping
- Complete Python API access

**Deployment:**
```bash
# Local development
streamlit run streamlit_app.py

# Production (Streamlit Cloud)
# Main file: streamlit_app.py
```

## 🌐 For Streamlit Cloud Deployment

### Option 1: Land App (Most Users)
1. **Main file:** `streamlit_land_app.py`
2. **URL:** Your app will load the Land App interface
3. **Use case:** Land management, mapping, educational purposes

### Option 2: Full GeoMasterPy Suite (Advanced Users)
1. **Main file:** `streamlit_app.py` 
2. **URL:** Your app will load the complete GeoMasterPy interface
3. **Use case:** Research, advanced analysis, full Python development

## 🔧 Configuration Notes

- Both apps can run simultaneously on different ports
- The Land App includes access to the full HTML interface
- The main app includes access to the Land App via navigation
- Choose based on your primary use case

## 📋 Recommended Setup

**For most users:** Use `streamlit_land_app.py` as your main file on Streamlit Cloud for the best land management experience.