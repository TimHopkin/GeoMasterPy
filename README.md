# 🌍 GeoMasterPy - Interactive Geospatial Analysis Library

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Streamlit App](https://img.shields.io/badge/🚀-Streamlit%20App-red.svg)](https://geomasterpy.streamlit.app)

**Interactive Geospatial Analysis Library for Google Earth Engine**

GeoMasterPy is a comprehensive Python library that significantly simplifies and enhances the use of Google Earth Engine (GEE) within Jupyter Notebook environments and web applications. It provides intuitive tools for interactive mapping, data visualization, geospatial analysis, data export, and creation of publication-quality maps.

## 🌟 **New! Interactive Web Application**

**Try GeoMasterPy instantly in your browser - no installation required!**

🚀 **[Launch Web App](https://share.streamlit.io)** *(Deploy this repository)*

## 🚀 Key Features

- **🌐 Web Application**: Complete Streamlit web app for browser-based analysis
- **📍 Interactive Mapping**: Easy-to-use map widgets with Earth Engine integration
- **🗂️ Data Catalog**: Search and discover Earth Engine datasets with built-in metadata
- **🎨 Visualization Tools**: Legends, colorbars, split maps, time series charts, and animations  
- **📊 Geospatial Analysis**: Statistical analysis, classification, spectral indices, and change detection
- **💾 Data Export**: Export images and vectors to local files or Google Drive
- **🖼️ Publication Maps**: High-quality static maps using Cartopy for scientific publications
- **🔧 JavaScript Conversion**: Convert GEE JavaScript code snippets to Python

## 🌐 Quick Start: Web Application

### Deploy on Streamlit Cloud (FREE)

1. **Fork this repository**
2. **Go to [share.streamlit.io](https://share.streamlit.io)**
3. **Connect your GitHub account**
4. **Deploy with:**
   - Repository: `TimHopkin/GeoMasterPy`
   - Main file: `streamlit_app.py`
   - Requirements: `requirements_streamlit.txt`

### Run Locally

```bash
# Clone the repository
git clone https://github.com/TimHopkin/GeoMasterPy.git
cd GeoMasterPy

# Install dependencies
pip install -r requirements_streamlit.txt

# Run the web app
streamlit run streamlit_app.py
```

Open your browser to `http://localhost:8501`

## 💻 Python Library Installation

### Prerequisites

1. **Python 3.8 or higher**
2. **Google Earth Engine account** - Sign up at [earthengine.google.com](https://earthengine.google.com)
3. **Jupyter Notebook or JupyterLab**

### Install Dependencies

```bash
pip install earthengine-api ipyleaflet ipywidgets numpy pandas cartopy matplotlib
```

### Install GeoMasterPy

```bash
# From source
git clone https://github.com/TimHopkin/GeoMasterPy.git
cd GeoMasterPy
pip install -e .
```

### Authenticate Google Earth Engine

```bash
# In Python
import ee
ee.Authenticate()  # Opens browser for authentication
ee.Initialize()
```

## 🏃‍♂️ Quick Start: Python Library

```python
import ee
import geomasterpy as gmp

# Initialize Earth Engine
ee.Initialize()

# Create an interactive map
Map = gmp.Map(center=(37.7749, -122.4194), zoom=10)

# Add a basemap
Map.add_basemap('Google.Satellite')

# Load and display Landsat data
landsat = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2') \
    .filterBounds(ee.Geometry.Point(-122.4194, 37.7749)) \
    .filterDate('2020-01-01', '2020-12-31') \
    .filter(ee.Filter.lt('CLOUD_COVER', 20)) \
    .median()

vis_params = {
    'bands': ['SR_B4', 'SR_B3', 'SR_B2'],
    'min': 0.0,
    'max': 0.3,
    'gamma': 1.4
}

Map.add_ee_layer(landsat, vis_params, 'Landsat 8')

# Display the map
Map
```

## 🎯 Web App Features

### 🌐 **Interactive Web Interface**
- **🏠 Home Dashboard** - Overview and quick navigation
- **🗺️ Interactive Maps** - Create maps with Folium integration
- **🔍 Data Catalog** - Browse Earth Engine datasets
- **🔄 Code Converter** - Convert JavaScript to Python
- **📊 Analysis Tools** - Statistical analysis interfaces
- **📈 Visualizations** - Interactive charts with Plotly
- **💾 Export Tools** - Download results and data
- **🖼️ Map Gallery** - Publication-quality map creation
- **📚 Documentation** - Complete help system

### 📱 **Accessible Anywhere**
- **💻 Desktop** - Full-featured experience
- **📱 Mobile** - Responsive design for phones
- **📟 Tablet** - Optimized for touch interfaces
- **🌐 Browser** - No installation required

## 📚 Python API Documentation

### Core Modules

#### 1. Interactive Mapping (`geomasterpy.Map`)

```python
# Create a map with custom settings
Map = gmp.Map(
    center=(40, -100), 
    zoom=4, 
    height='600px',
    lite_mode=False
)

# Add various basemaps
Map.add_basemap('Google.Satellite')

# Add Earth Engine layers
Map.add_ee_layer(ee_image, vis_params, 'Layer Name')

# Add interactive tools
Map.add_inspector_tool()
```

#### 2. Data Catalog (`geomasterpy.data`)

```python
# Search for datasets
results = gmp.search_ee_data('landsat', max_results=10)

# Convert JavaScript code to Python
js_code = "var image = ee.Image('LANDSAT/LC08/C02/T1_L2/test');"
python_code = gmp.js_snippet_to_python(js_code)

# Get dataset information
info = gmp.data.get_dataset_info('LANDSAT/LC08/C02/T1_L2')
```

#### 3. Geospatial Analysis (`geomasterpy.analysis`)

```python
# Calculate image statistics
stats = gmp.image_stats(image, region, scale=30)

# Perform zonal statistics
zonal_results = gmp.zonal_stats(image, zones, reducer='mean')

# Calculate spectral indices
indices_image = gmp.analysis.calculate_indices(
    image, ['NDVI', 'NDWI', 'NDBI', 'EVI']
)

# Classification
classified = gmp.analysis.unsupervised_classification(
    image, num_classes=5, scale=30
)
```

#### 4. Data Export (`geomasterpy.export`)

```python
# Export to local files
gmp.export_image_to_local(image, 'output_image', region, scale=30)

# Export to Google Drive
task = gmp.export.export_image_to_drive(
    image, 'my_export', folder='EarthEngine', region=region
)

# Extract values at points
df = gmp.extract_values_to_points(image, points, scale=30)
```

#### 5. Visualization (`geomasterpy.viz`)

```python
# Add legends and colorbars
legend_dict = {'Water': 'blue', 'Forest': 'green', 'Urban': 'gray'}
gmp.add_legend(Map, 'Land Cover', legend_dict)

vis_params = {'min': -1, 'max': 1, 'palette': ['blue', 'white', 'green']}
gmp.add_colorbar(Map, vis_params, 'NDVI')

# Create time series charts
chart = gmp.viz.create_time_series_chart(
    image_collection, region, 'NDVI', 'mean', scale=30
)
```

#### 6. Publication Maps (`geomasterpy.plotting`)

```python
# Create publication-quality maps
fig = gmp.plot_ee_image_cartopy(
    image, vis_params, region,
    figsize=(12, 8),
    title='My Study Area',
    projection='PlateCarree',
    add_colorbar=True
)

# Save high-resolution maps
gmp.plotting.save_publication_map(
    fig, 'my_map.png', dpi=300, format='png'
)
```

## 📚 Examples

Explore the example notebooks:

1. **`examples/01_basic_usage.ipynb`** - Introduction to interactive mapping
2. **`examples/02_data_analysis.ipynb`** - Geospatial analysis workflows  
3. **`examples/03_publication_maps.ipynb`** - Creating publication-quality maps
4. **`QUICK_START.ipynb`** - Quick start tutorial

## 📁 Project Structure

```
GeoMasterPy/
├── 🌐 streamlit_app.py          # Web application
├── 📦 geomasterpy/              # Core Python library
│   ├── map/                     # Interactive mapping
│   ├── data/                    # Data catalog & conversion
│   ├── viz/                     # Visualization tools
│   ├── analysis/                # Geospatial analysis
│   ├── export/                  # Data export
│   └── plotting/                # Publication maps
├── 📓 examples/                 # Jupyter notebooks
├── 🧪 tests/                    # Test suite
├── 📚 docs/                     # Documentation
├── 🚀 deploy.sh                 # Deployment script
└── 📋 requirements*.txt         # Dependencies
```

## 🚀 Deployment

### Streamlit Cloud (Recommended)

1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Deploy with `streamlit_app.py` as main file

### Heroku

```bash
git clone https://github.com/TimHopkin/GeoMasterPy.git
cd GeoMasterPy
heroku create your-app-name
git push heroku main
```

### Local Development

```bash
pip install -r requirements_streamlit.txt
streamlit run streamlit_app.py
```

## 🧪 Testing

```bash
# Run tests
pytest tests/

# Test installation
python test_installation.py

# Demo without Earth Engine
python demo_without_ee.py
```

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Earth Engine** team for the amazing platform
- **Streamlit** for the excellent web app framework
- **ipyleaflet** developers for interactive mapping capabilities
- **Cartopy** developers for publication-quality mapping tools
- The open-source geospatial community

## 📞 Support

- 🌐 **Web App**: Try the [interactive version](https://share.streamlit.io)
- 📖 **Documentation**: Complete API reference included
- 🐛 **Issues**: Report bugs via GitHub Issues
- 💬 **Discussions**: Join GitHub Discussions

## 🔗 Related Projects

- [Google Earth Engine Python API](https://github.com/google/earthengine-api)
- [Streamlit](https://github.com/streamlit/streamlit)
- [ipyleaflet](https://github.com/jupyter-widgets/ipyleaflet)
- [Cartopy](https://github.com/SciTools/cartopy)

---

**🌍 Made with ❤️ for the geospatial community**

**🚀 [Try the Web App Now!](https://share.streamlit.io)**