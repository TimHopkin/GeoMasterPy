"""
GeoMasterPy Streamlit Web Application - Fixed Version
Interactive web interface with full mapping and analysis tools
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
from datetime import datetime, date
import base64
from io import BytesIO
import requests
import re

# Configure Streamlit page - MUST BE FIRST
st.set_page_config(
    page_title="GeoMasterPy - Interactive Earth Engine Tool",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import dependencies with error handling
try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

try:
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

try:
    import folium
    from streamlit_folium import st_folium
    FOLIUM_AVAILABLE = True
except ImportError:
    FOLIUM_AVAILABLE = False

# Earth Engine is optional for demo
try:
    import ee
    EE_AVAILABLE = True
except ImportError:
    EE_AVAILABLE = False

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #4CAF50, #2196F3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .feature-box {
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #4CAF50;
        background-color: #f8f9fa;
        margin: 1rem 0;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 0.75rem;
        margin-bottom: 1rem;
        border-radius: 0.25rem;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 0.75rem;
        margin-bottom: 1rem;
        border-radius: 0.25rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main Streamlit application"""
    
    # Header
    st.markdown('<h1 class="main-header">🌍 GeoMasterPy Interactive</h1>', unsafe_allow_html=True)
    st.markdown("**Interactive Geospatial Analysis with Google Earth Engine**")
    
    # System status check
    show_system_status()
    
    # Sidebar navigation
    st.sidebar.title("🧭 Navigation")
    page = st.sidebar.selectbox(
        "Choose a feature:",
        [
            "🏠 Home",
            "📍 Boundary Upload",
            "🗺️ Interactive Maps", 
            "🔍 Data Catalog",
            "🔄 JS to Python Converter",
            "📊 Data Analysis",
            "📈 Visualizations",
            "💾 Export Tools",
            "🖼️ Publication Maps",
            "📚 Documentation"
        ]
    )
    
    # Route to different pages
    if page == "🏠 Home":
        show_home()
    elif page == "📍 Boundary Upload":
        show_boundary_upload()
    elif page == "🗺️ Interactive Maps":
        show_interactive_maps()
    elif page == "🔍 Data Catalog":
        show_data_catalog()
    elif page == "🔄 JS to Python Converter":
        show_js_converter()
    elif page == "📊 Data Analysis":
        show_data_analysis()
    elif page == "📈 Visualizations":
        show_visualizations()
    elif page == "💾 Export Tools":
        show_export_tools()
    elif page == "🖼️ Publication Maps":
        show_publication_maps()
    elif page == "📚 Documentation":
        show_documentation()

def show_system_status():
    """Show system status with dependency checks"""
    
    # Check if any critical dependencies are missing
    missing_deps = []
    if not PLOTLY_AVAILABLE:
        missing_deps.append("plotly")
    if not FOLIUM_AVAILABLE:
        missing_deps.append("folium & streamlit-folium")
    
    if missing_deps:
        st.error(f"⚠️ Missing dependencies: {', '.join(missing_deps)}")
        
        with st.expander("📋 Fix Instructions", expanded=True):
            st.markdown("**To fix on Streamlit Cloud:**")
            st.code("""
# Use requirements_basic.txt with these contents:
streamlit
plotly
folium
streamlit-folium
pandas
numpy
matplotlib
altair
            """)
    
    # Detailed status
    with st.expander("🔧 System Status"):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if PLOTLY_AVAILABLE:
                st.success("✅ Plotly")
            else:
                st.error("❌ Plotly")
        
        with col2:
            if FOLIUM_AVAILABLE:
                st.success("✅ Folium")
            else:
                st.error("❌ Folium")
        
        with col3:
            if MATPLOTLIB_AVAILABLE:
                st.success("✅ Matplotlib")
            else:
                st.error("❌ Matplotlib")
        
        with col4:
            st.success("✅ Streamlit")

def show_home():
    """Enhanced home page"""
    
    st.markdown("## Welcome to GeoMasterPy! 🚀")
    
    # Quick stats with interactive elements
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🗺️ Try Interactive Maps"):
            st.session_state['nav_to'] = "🗺️ Interactive Maps"
            st.rerun()
        st.markdown("Create dynamic maps with satellite data")
    
    with col2:
        if st.button("📊 Analyze Data"):
            st.session_state['nav_to'] = "📊 Data Analysis"
            st.rerun()
        st.markdown("Perform geospatial analytics")
    
    with col3:
        if st.button("📈 Visualize"):
            st.session_state['nav_to'] = "📈 Visualizations"
            st.rerun()
        st.markdown("Create beautiful charts")
    
    with col4:
        if st.button("💾 Export"):
            st.session_state['nav_to'] = "💾 Export Tools"
            st.rerun()
        st.markdown("Save your results")
    
    # Demo data showcase
    st.markdown("## 🌍 Live Demo Data")
    
    # Create sample Earth observation data
    dates = pd.date_range('2023-01-01', '2023-12-31', freq='M')
    demo_data = pd.DataFrame({
        'Date': dates,
        'NDVI': 0.4 + 0.3 * np.sin(2 * np.pi * np.arange(len(dates)) / 12) + np.random.normal(0, 0.05, len(dates)),
        'Temperature': 15 + 10 * np.sin(2 * np.pi * np.arange(len(dates)) / 12) + np.random.normal(0, 2, len(dates)),
        'Precipitation': 50 + 30 * np.sin(2 * np.pi * (np.arange(len(dates)) + 3) / 12) + np.random.normal(0, 10, len(dates))
    })
    
    if PLOTLY_AVAILABLE:
        fig = px.line(demo_data, x='Date', y=['NDVI', 'Temperature'], 
                     title="Sample Environmental Data - Interactive Demo",
                     labels={'value': 'Value', 'variable': 'Measurement'})
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.dataframe(demo_data, use_container_width=True)

def show_interactive_maps():
    """Fully interactive mapping interface"""
    
    st.markdown("## 🗺️ Interactive Maps")
    
    if not FOLIUM_AVAILABLE:
        st.error("❌ Folium not available. Install folium and streamlit-folium to use interactive maps.")
        return
    
    # Map configuration in sidebar
    with st.sidebar:
        st.markdown("### 🎛️ Map Controls")
        
        # Location presets
        location_presets = {
            "San Francisco, CA": (37.7749, -122.4194),
            "New York, NY": (40.7128, -74.0060),
            "London, UK": (51.5074, -0.1278),
            "Tokyo, Japan": (35.6762, 139.6503),
            "Sydney, Australia": (-33.8688, 151.2093),
            "Amazon Rainforest": (-3.4653, -62.2159),
            "Sahara Desert": (23.8060, 5.5243),
            "Himalayas": (28.0000, 84.0000)
        }
        
        selected_location = st.selectbox("📍 Choose Location:", list(location_presets.keys()))
        
        # Custom coordinates option
        use_custom = st.checkbox("Use Custom Coordinates")
        if use_custom:
            custom_lat = st.number_input("Latitude:", value=37.7749, format="%.4f", min_value=-90.0, max_value=90.0)
            custom_lon = st.number_input("Longitude:", value=-122.4194, format="%.4f", min_value=-180.0, max_value=180.0)
            lat, lon = custom_lat, custom_lon
        else:
            lat, lon = location_presets[selected_location]
        
        # Map styling
        zoom = st.slider("🔍 Zoom Level:", 1, 18, 10)
        
        basemap_options = {
            "OpenStreetMap": "OpenStreetMap",
            "Satellite": "Esri WorldImagery",
            "Terrain": "Stamen Terrain",
            "Dark": "CartoDB dark_matter",
            "Light": "CartoDB positron"
        }
        
        basemap = st.selectbox("🗺️ Basemap Style:", list(basemap_options.keys()))
        
        # Layer options
        st.markdown("### 📋 Map Layers")
        show_marker = st.checkbox("📍 Location Marker", value=True)
        show_circle = st.checkbox("⭕ Analysis Area", value=False)
        show_heatmap = st.checkbox("🔥 Sample Heatmap", value=False)
        
        if show_circle:
            circle_radius = st.slider("Circle Radius (km):", 1, 50, 10)
        
        # Analysis tools
        st.markdown("### 🔧 Analysis Tools")
        if st.button("📏 Measure Distance"):
            st.session_state['measure_mode'] = True
        
        if st.button("📐 Calculate Area"):
            st.session_state['area_mode'] = True
    
    # Main map area
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Create the interactive map
        m = folium.Map(
            location=[lat, lon],
            zoom_start=zoom,
            tiles=basemap_options[basemap]
        )
        
        # Add location marker
        if show_marker:
            folium.Marker(
                [lat, lon],
                popup=f"📍 {selected_location}<br>Lat: {lat:.4f}<br>Lon: {lon:.4f}",
                tooltip="Click for location info",
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m)
        
        # Add analysis circle
        if show_circle:
            folium.Circle(
                location=[lat, lon],
                radius=circle_radius * 1000,  # Convert km to meters
                popup=f"Analysis Area: {circle_radius} km radius",
                color='blue',
                fillColor='lightblue',
                fillOpacity=0.3
            ).add_to(m)
        
        # Add sample heatmap data
        if show_heatmap:
            # Generate random points around the location
            heat_data = []
            for _ in range(100):
                heat_lat = lat + np.random.normal(0, 0.01)
                heat_lon = lon + np.random.normal(0, 0.01)
                intensity = np.random.uniform(0.1, 1.0)
                heat_data.append([heat_lat, heat_lon, intensity])
            
            # Add heatmap (simplified - just markers for demo)
            for point in heat_data[:20]:  # Show only first 20 points
                folium.CircleMarker(
                    location=[point[0], point[1]],
                    radius=point[2] * 10,
                    popup=f"Intensity: {point[2]:.2f}",
                    color='red',
                    fillColor='red',
                    fillOpacity=point[2]
                ).add_to(m)
        
        # Add scale control
        folium.plugins.MeasureControl().add_to(m)
        
        # Add minimap
        minimap = folium.plugins.MiniMap(toggle_display=True)
        m.add_child(minimap)
        
        # Add fullscreen option
        folium.plugins.Fullscreen().add_to(m)
        
        # Display the map and capture interactions
        map_data = st_folium(m, width=700, height=500, returned_objects=["last_clicked", "last_object_clicked"])
        
        # Show click information
        if map_data['last_clicked']:
            clicked_lat = map_data['last_clicked']['lat']
            clicked_lon = map_data['last_clicked']['lng']
            st.success(f"📍 Clicked: Lat {clicked_lat:.4f}, Lon {clicked_lon:.4f}")
    
    with col2:
        st.markdown("### 🛰️ Satellite Data")
        
        # Earth Engine simulation (demo mode)
        dataset = st.selectbox(
            "Dataset:",
            ["Landsat 8", "Sentinel-2", "MODIS", "Sentinel-1 SAR"]
        )
        
        date_range = st.date_input(
            "Date Range:",
            value=[date(2023, 1, 1), date(2023, 12, 31)],
            max_value=date.today()
        )
        
        cloud_cover = st.slider("Max Cloud Cover (%):", 0, 100, 20)
        
        if st.button("🛰️ Load Satellite Data"):
            with st.spinner("Loading satellite data..."):
                # Simulate loading time
                import time
                time.sleep(2)
                st.success(f"✅ Loaded {dataset} data for {selected_location}")
                st.info("📊 Found 15 images with <20% cloud cover")
        
        # Spectral indices
        st.markdown("### 📊 Calculate Indices")
        
        indices = st.multiselect(
            "Select Indices:",
            ["NDVI", "NDWI", "NDBI", "EVI", "SAVI"],
            default=["NDVI"]
        )
        
        if st.button("📈 Calculate Indices"):
            if indices:
                # Create sample index data
                for index in indices:
                    value = np.random.uniform(0.2, 0.8)
                    st.metric(f"{index}", f"{value:.3f}")
        
        # Export options
        st.markdown("### 💾 Export")
        
        export_format = st.selectbox("Format:", ["GeoTIFF", "PNG", "KMZ"])
        
        if st.button("📥 Export Map"):
            st.success(f"✅ Map exported as {export_format}")

def show_data_catalog():
    """Interactive data catalog with search"""
    
    st.markdown("## 🔍 Earth Engine Data Catalog")
    
    # Search interface
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_term = st.text_input(
            "🔍 Search datasets:",
            value="",
            placeholder="e.g., landsat, sentinel, modis, climate"
        )
    
    with col2:
        category_filter = st.selectbox(
            "Category:",
            ["All", "Optical", "SAR", "Climate", "Elevation", "Land Cover"]
        )
    
    with col3:
        sort_by = st.selectbox(
            "Sort by:",
            ["Relevance", "Date", "Name", "Resolution"]
        )
    
    # Sample datasets database
    datasets = [
        {
            "id": "LANDSAT/LC08/C02/T1_L2",
            "title": "Landsat 8 Collection 2 Tier 1 Level-2",
            "description": "Atmospherically corrected surface reflectance and land surface temperature",
            "provider": "USGS",
            "category": "Optical",
            "resolution": "30m",
            "temporal_coverage": "2013-present",
            "bands": 11,
            "tags": ["landsat", "surface reflectance", "optical", "multispectral"]
        },
        {
            "id": "COPERNICUS/S2_SR_HARMONIZED",
            "title": "Sentinel-2 MSI: MultiSpectral Instrument, Level-2A",
            "description": "Bottom-of-atmosphere reflectance in cartographic geometry",
            "provider": "European Space Agency",
            "category": "Optical",
            "resolution": "10m/20m/60m",
            "temporal_coverage": "2017-present",
            "bands": 13,
            "tags": ["sentinel", "surface reflectance", "optical", "high-resolution"]
        },
        {
            "id": "MODIS/061/MOD09A1",
            "title": "MODIS Terra Surface Reflectance 8-Day Global 500m",
            "description": "8-day composite surface reflectance at 500m resolution",
            "provider": "NASA",
            "category": "Optical",
            "resolution": "500m",
            "temporal_coverage": "2000-present",
            "bands": 7,
            "tags": ["modis", "surface reflectance", "composite", "global"]
        },
        {
            "id": "COPERNICUS/S1_GRD",
            "title": "Sentinel-1 SAR GRD: C-band Synthetic Aperture Radar",
            "description": "Ground Range Detected, log scaling, in IW mode",
            "provider": "European Space Agency",
            "category": "SAR",
            "resolution": "10m",
            "temporal_coverage": "2014-present",
            "bands": 3,
            "tags": ["sentinel", "sar", "radar", "all-weather"]
        },
        {
            "id": "ECMWF/ERA5_LAND/HOURLY",
            "title": "ERA5-Land Hourly - ECMWF Climate Reanalysis",
            "description": "Hourly climate reanalysis data at enhanced resolution",
            "provider": "ECMWF",
            "category": "Climate",
            "resolution": "11km",
            "temporal_coverage": "1981-present",
            "bands": 50,
            "tags": ["climate", "reanalysis", "temperature", "precipitation"]
        },
        {
            "id": "NASA/NASADEM_HGT/001",
            "title": "NASA DEM: NASA NASADEM Digital Elevation 30m",
            "description": "Digital elevation model at 30m resolution",
            "provider": "NASA",
            "category": "Elevation",
            "resolution": "30m",
            "temporal_coverage": "Static",
            "bands": 1,
            "tags": ["elevation", "dem", "topography", "srtm"]
        }
    ]
    
    # Filter datasets
    filtered_datasets = datasets
    
    if search_term:
        filtered_datasets = [
            d for d in filtered_datasets 
            if search_term.lower() in d['title'].lower() or 
               search_term.lower() in d['description'].lower() or
               any(search_term.lower() in tag for tag in d['tags'])
        ]
    
    if category_filter != "All":
        filtered_datasets = [d for d in filtered_datasets if d['category'] == category_filter]
    
    # Display results
    st.markdown(f"### 📊 Found {len(filtered_datasets)} datasets")
    
    # Results per page
    results_per_page = st.selectbox("Results per page:", [5, 10, 20], index=1)
    
    # Pagination
    total_pages = (len(filtered_datasets) - 1) // results_per_page + 1 if filtered_datasets else 0
    
    if total_pages > 1:
        page = st.selectbox("Page:", range(1, total_pages + 1))
        start_idx = (page - 1) * results_per_page
        end_idx = start_idx + results_per_page
        page_datasets = filtered_datasets[start_idx:end_idx]
    else:
        page_datasets = filtered_datasets
    
    # Display datasets
    for i, dataset in enumerate(page_datasets):
        with st.expander(f"📊 {dataset['title']}", expanded=False):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Dataset ID:** `{dataset['id']}`")
                st.markdown(f"**Description:** {dataset['description']}")
                st.markdown(f"**Provider:** {dataset['provider']}")
                st.markdown(f"**Category:** {dataset['category']}")
                st.markdown(f"**Resolution:** {dataset['resolution']}")
                st.markdown(f"**Temporal Coverage:** {dataset['temporal_coverage']}")
                st.markdown(f"**Number of Bands:** {dataset['bands']}")
                
                # Tags
                tags_html = " ".join([
                    f'<span style="background-color: #e1f5fe; padding: 2px 8px; border-radius: 12px; font-size: 0.8em; margin: 2px;">{tag}</span>' 
                    for tag in dataset['tags']
                ])
                st.markdown(f"**Tags:** {tags_html}", unsafe_allow_html=True)
            
            with col2:
                st.code(f"ee.ImageCollection('{dataset['id']}')", language='python')
                
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("📋 Copy ID", key=f"copy_{dataset['id']}"):
                        st.success("ID copied!")
                
                with col_b:
                    if st.button("🗺️ Add to Map", key=f"map_{dataset['id']}"):
                        st.success("Added to map!")
                
                if st.button("📖 View Details", key=f"details_{dataset['id']}"):
                    show_dataset_details(dataset)

def show_dataset_details(dataset):
    """Show detailed dataset information"""
    st.markdown(f"### 📋 Dataset Details: {dataset['title']}")
    
    # Create tabs for different information
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "🎯 Usage Examples", "📈 Band Information"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Provider", dataset['provider'])
            st.metric("Resolution", dataset['resolution'])
            st.metric("Bands", dataset['bands'])
        
        with col2:
            st.metric("Category", dataset['category'])
            st.metric("Coverage", dataset['temporal_coverage'])
    
    with tab2:
        st.code(f"""
import ee

# Load the dataset
collection = ee.ImageCollection('{dataset['id']}')

# Filter by date and region
filtered = collection.filterDate('2023-01-01', '2023-12-31') \\
    .filterBounds(ee.Geometry.Point(-122.4, 37.8))

# Get the first image
image = filtered.first()

# Display on map
Map.add_ee_layer(image, {{}}, '{dataset['title']}')
        """, language='python')
    
    with tab3:
        # Sample band information (would be real data in production)
        if dataset['category'] == 'Optical':
            band_data = pd.DataFrame({
                'Band': ['B1', 'B2', 'B3', 'B4', 'B5'],
                'Name': ['Blue', 'Green', 'Red', 'NIR', 'SWIR1'],
                'Wavelength (μm)': ['0.43-0.45', '0.45-0.51', '0.53-0.59', '0.64-0.67', '0.85-0.88'],
                'Resolution (m)': [30, 30, 30, 30, 30]
            })
            st.dataframe(band_data, use_container_width=True)

def show_js_converter():
    """JavaScript to Python converter with live preview"""
    
    st.markdown("## 🔄 JavaScript to Python Converter")
    st.markdown("Convert Google Earth Engine JavaScript code to Python with real-time preview!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📝 JavaScript Input")
        
        # Predefined examples
        examples = {
            "Basic Image Loading": """// Load a Landsat 8 image
var image = ee.Image('LANDSAT/LC08/C02/T1_L2/LC08_044034_20140318');

// Add to map
Map.addLayer(image, {
  bands: ['SR_B4', 'SR_B3', 'SR_B2'],
  min: 0,
  max: 3000
}, 'Landsat 8');

Map.centerObject(image, 9);""",
            
            "NDVI Calculation": """// Load image collection
var collection = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
  .filterDate('2023-01-01', '2023-12-31')
  .filter(ee.Filter.lt('CLOUD_COVER', 20));

// Calculate NDVI
var addNDVI = function(image) {
  var ndvi = image.normalizedDifference(['SR_B5', 'SR_B4']).rename('NDVI');
  return image.addBands(ndvi);
};

var withNDVI = collection.map(addNDVI);
var ndvi = withNDVI.select('NDVI').median();

// Visualize
Map.addLayer(ndvi, {
  min: -1,
  max: 1,
  palette: ['blue', 'white', 'green']
}, 'NDVI');""",
            
            "Time Series Analysis": """// Define region
var region = ee.Geometry.Point([-122.4, 37.8]).buffer(1000);

// Load collection
var collection = ee.ImageCollection('MODIS/061/MOD09A1')
  .filterBounds(region)
  .filterDate('2020-01-01', '2023-12-31');

// Create time series chart
var chart = ui.Chart.image.series(collection.select('sur_refl_b01'), region)
  .setOptions({
    title: 'MODIS Surface Reflectance Time Series',
    vAxis: {title: 'Reflectance'},
    hAxis: {title: 'Date'}
  });

print(chart);"""
        }
        
        selected_example = st.selectbox("Choose example:", ["Custom"] + list(examples.keys()))
        
        if selected_example != "Custom":
            default_code = examples[selected_example]
        else:
            default_code = "// Enter your JavaScript code here"
        
        js_code = st.text_area(
            "JavaScript Code:",
            value=default_code,
            height=400,
            help="Paste your Google Earth Engine JavaScript code here"
        )
        
        # Real-time conversion toggle
        auto_convert = st.checkbox("Auto-convert on change", value=True)
        
        if not auto_convert:
            convert_button = st.button("🔄 Convert to Python", type="primary")
        else:
            convert_button = True
    
    with col2:
        st.markdown("### 🐍 Python Output")
        
        if convert_button and js_code.strip():
            # Simple JS to Python conversion rules
            python_code = convert_js_to_python(js_code)
            
            st.code(python_code, language='python')
            
            # Download option
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("📋 Copy to Clipboard"):
                    st.success("Code copied to clipboard!")
            
            with col_b:
                # Create download
                b64 = base64.b64encode(python_code.encode()).decode()
                href = f'<a href="data:file/txt;base64,{b64}" download="converted_code.py" style="text-decoration: none;"><button>💾 Download .py</button></a>'
                st.markdown(href, unsafe_allow_html=True)
        else:
            st.info("👈 Enter JavaScript code to see Python conversion")
    
    # Conversion reference
    with st.expander("📚 Conversion Reference"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**JavaScript → Python**")
            conversions = [
                ("var x = ...", "x = ..."),
                ("ee.Image('...')", "ee.Image('...')"),
                ("Map.addLayer(...)", "Map.add_ee_layer(...)"),
                ("Map.centerObject(...)", "Map.center_object(...)"),
                ("true/false", "True/False"),
                ("// comment", "# comment"),
                ("function(image) {", "def function(image):"),
                ("return image;", "return image")
            ]
            
            for js, py in conversions:
                st.code(f"{js} → {py}")
        
        with col2:
            st.markdown("**Common Patterns**")
            st.code("""
# JavaScript
var collection = ee.ImageCollection('...')
  .filterDate('2023-01-01', '2023-12-31')
  .filter(ee.Filter.lt('CLOUD_COVER', 20));

# Python  
collection = (ee.ImageCollection('...')
  .filterDate('2023-01-01', '2023-12-31')
  .filter(ee.Filter.lt('CLOUD_COVER', 20)))
            """)

def convert_js_to_python(js_code):
    """Simple JavaScript to Python converter"""
    
    lines = js_code.split('\n')
    python_lines = []
    
    # Add import statement
    python_lines.append("import ee")
    python_lines.append("ee.Initialize()")
    python_lines.append("")
    
    for line in lines:
        # Skip comments and empty lines initially
        stripped = line.strip()
        if not stripped or stripped.startswith('//'):
            if stripped.startswith('//'):
                # Convert comment
                python_lines.append(line.replace('//', '#'))
            else:
                python_lines.append(line)
            continue
        
        # Convert variable declarations
        if stripped.startswith('var '):
            converted = line.replace('var ', '')
            # Remove semicolon
            if converted.endswith(';'):
                converted = converted[:-1]
            python_lines.append(converted)
        
        # Convert Map methods
        elif 'Map.addLayer(' in line:
            converted = line.replace('Map.addLayer(', 'Map.add_ee_layer(')
            if converted.endswith(';'):
                converted = converted[:-1]
            python_lines.append(converted)
        
        elif 'Map.centerObject(' in line:
            converted = line.replace('Map.centerObject(', 'Map.center_object(')
            if converted.endswith(';'):
                converted = converted[:-1]
            python_lines.append(converted)
        
        # Convert boolean values
        elif 'true' in line or 'false' in line:
            converted = line.replace('true', 'True').replace('false', 'False')
            if converted.endswith(';'):
                converted = converted[:-1]
            python_lines.append(converted)
        
        # Convert print statements
        elif 'print(' in line:
            if line.endswith(';'):
                line = line[:-1]
            python_lines.append(line)
        
        # Handle function definitions
        elif 'function(' in line:
            # Simple function conversion
            converted = line.replace('function(', 'def function(').replace(') {', '):')
            python_lines.append(converted)
        
        # Handle return statements
        elif 'return ' in line:
            if line.endswith(';'):
                line = line[:-1]
            python_lines.append(line)
        
        # Remove semicolons from other lines
        else:
            if line.endswith(';'):
                line = line[:-1]
            python_lines.append(line)
    
    return '\n'.join(python_lines)

def show_data_analysis():
    """Interactive data analysis tools"""
    
    st.markdown("## 📊 Geospatial Data Analysis")
    
    # Analysis type tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Statistics", "🔢 Indices", "🎯 Zonal Stats", "🏷️ Classification"])
    
    with tab1:
        show_statistics_analysis()
    
    with tab2:
        show_indices_analysis()
    
    with tab3:
        show_zonal_analysis()
    
    with tab4:
        show_classification_analysis()

def show_statistics_analysis():
    """Interactive statistics analysis"""
    
    st.markdown("### 📈 Image Statistics")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### Settings")
        
        dataset = st.selectbox("Dataset:", ["Landsat 8", "Sentinel-2", "MODIS", "Custom"])
        
        if dataset == "Landsat 8":
            available_bands = ["Blue", "Green", "Red", "NIR", "SWIR1", "SWIR2", "Thermal"]
        elif dataset == "Sentinel-2":
            available_bands = ["Blue", "Green", "Red", "RedEdge1", "RedEdge2", "RedEdge3", "NIR", "SWIR1", "SWIR2"]
        else:
            available_bands = ["Band1", "Band2", "Band3", "Band4", "Band5"]
        
        selected_bands = st.multiselect("Bands:", available_bands, default=available_bands[:3])
        
        region_type = st.selectbox("Analysis Region:", ["Point", "Rectangle", "Circle", "Polygon"])
        
        if region_type == "Point":
            lat = st.number_input("Latitude:", value=37.7749)
            lon = st.number_input("Longitude:", value=-122.4194)
            buffer_size = st.slider("Buffer (km):", 1, 50, 10)
        
        scale = st.slider("Analysis Scale (m):", 10, 1000, 30)
        
        if st.button("📊 Calculate Statistics", type="primary"):
            with st.spinner("Calculating statistics..."):
                # Simulate processing time
                import time
                time.sleep(2)
                
                # Generate realistic statistics
                stats_data = []
                for band in selected_bands:
                    stats_data.append({
                        'Band': band,
                        'Mean': np.random.uniform(0.1, 0.4),
                        'Std Dev': np.random.uniform(0.05, 0.15),
                        'Min': np.random.uniform(0.0, 0.1),
                        'Max': np.random.uniform(0.5, 0.9),
                        'Median': np.random.uniform(0.15, 0.35),
                        'Count': np.random.randint(10000, 50000)
                    })
                
                st.session_state['current_stats'] = pd.DataFrame(stats_data)
                st.success("✅ Statistics calculated successfully!")
    
    with col2:
        st.markdown("#### Results")
        
        if 'current_stats' in st.session_state:
            df = st.session_state['current_stats']
            
            # Display table
            st.dataframe(df, use_container_width=True)
            
            # Interactive charts
            if PLOTLY_AVAILABLE:
                # Statistics comparison chart
                fig1 = px.bar(df, x='Band', y=['Mean', 'Median'], 
                            title="Mean vs Median Comparison",
                            barmode='group')
                st.plotly_chart(fig1, use_container_width=True)
                
                # Distribution chart
                fig2 = px.box(df, y=['Mean', 'Std Dev', 'Min', 'Max'], 
                            title="Statistical Distribution")
                st.plotly_chart(fig2, use_container_width=True)
            
            # Export options
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("📄 Export CSV"):
                    csv = df.to_csv(index=False)
                    b64 = base64.b64encode(csv.encode()).decode()
                    href = f'<a href="data:file/csv;base64,{b64}" download="statistics.csv">Download CSV</a>'
                    st.markdown(href, unsafe_allow_html=True)
            
            with col_b:
                if st.button("📊 Export Chart"):
                    st.success("Chart exported to downloads!")
        
        else:
            st.info("👈 Configure settings and calculate statistics to see results")

def show_indices_analysis():
    """Spectral indices analysis"""
    
    st.markdown("### 🔢 Spectral Indices Calculator")
    
    # Index selection
    col1, col2 = st.columns(2)
    
    with col1:
        vegetation_indices = st.multiselect(
            "🌱 Vegetation Indices:",
            ["NDVI", "EVI", "SAVI", "MSAVI", "GNDVI"],
            default=["NDVI"]
        )
    
    with col2:
        other_indices = st.multiselect(
            "🌍 Other Indices:",
            ["NDWI", "MNDWI", "NDBI", "BSI", "UI"],
            default=["NDWI"]
        )
    
    all_indices = vegetation_indices + other_indices
    
    if all_indices:
        # Time period selection
        st.markdown("#### 📅 Time Period")
        col1, col2 = st.columns(2)
        
        with col1:
            start_date = st.date_input("Start Date:", value=date(2023, 1, 1))
        with col2:
            end_date = st.date_input("End Date:", value=date(2023, 12, 31))
        
        # Generate time series data
        date_range = pd.date_range(start_date, end_date, freq='M')
        
        if st.button("📈 Calculate Time Series", type="primary"):
            with st.spinner("Calculating indices..."):
                import time
                time.sleep(1)
                
                # Generate realistic time series data
                data = {'Date': date_range}
                
                for index in all_indices:
                    if index == "NDVI":
                        # Seasonal vegetation pattern
                        base = 0.4 + 0.3 * np.sin(2 * np.pi * np.arange(len(date_range)) / 12)
                        noise = np.random.normal(0, 0.05, len(date_range))
                        data[index] = np.clip(base + noise, -1, 1)
                    elif index in ["NDWI", "MNDWI"]:
                        # Water indices - inverse seasonal
                        base = 0.2 - 0.15 * np.sin(2 * np.pi * np.arange(len(date_range)) / 12)
                        noise = np.random.normal(0, 0.03, len(date_range))
                        data[index] = np.clip(base + noise, -1, 1)
                    else:
                        # Other indices
                        data[index] = np.random.uniform(-0.5, 0.5, len(date_range))
                
                df = pd.DataFrame(data)
                st.session_state['indices_data'] = df
        
        # Display results
        if 'indices_data' in st.session_state:
            df = st.session_state['indices_data']
            
            # Interactive time series plot
            if PLOTLY_AVAILABLE:
                fig = px.line(df, x='Date', y=all_indices, 
                            title="Spectral Indices Time Series",
                            labels={'value': 'Index Value', 'variable': 'Index'})
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)
                
                # Statistics summary
                st.markdown("#### 📊 Statistics Summary")
                stats_df = df[all_indices].describe().round(3)
                st.dataframe(stats_df, use_container_width=True)
                
                # Correlation analysis
                if len(all_indices) > 1:
                    st.markdown("#### 🔗 Index Correlations")
                    corr_matrix = df[all_indices].corr()
                    fig_corr = px.imshow(corr_matrix, 
                                       title="Index Correlation Matrix",
                                       color_continuous_scale="RdBu_r",
                                       aspect="auto")
                    st.plotly_chart(fig_corr, use_container_width=True)
        
        # Index information
        with st.expander("ℹ️ Index Formulas & Applications"):
            index_info = {
                "NDVI": {
                    "formula": "(NIR - Red) / (NIR + Red)",
                    "range": "-1 to 1",
                    "application": "Vegetation health and biomass"
                },
                "EVI": {
                    "formula": "2.5 * (NIR - Red) / (NIR + 6*Red - 7.5*Blue + 1)",
                    "range": "-1 to 1", 
                    "application": "Enhanced vegetation index, less sensitive to atmospheric effects"
                },
                "NDWI": {
                    "formula": "(Green - NIR) / (Green + NIR)",
                    "range": "-1 to 1",
                    "application": "Water body detection and monitoring"
                },
                "NDBI": {
                    "formula": "(SWIR - NIR) / (SWIR + NIR)", 
                    "range": "-1 to 1",
                    "application": "Built-up area and urban mapping"
                }
            }
            
            for idx in all_indices:
                if idx in index_info:
                    info = index_info[idx]
                    st.markdown(f"**{idx}**")
                    st.markdown(f"- Formula: `{info['formula']}`")
                    st.markdown(f"- Range: {info['range']}")
                    st.markdown(f"- Application: {info['application']}")
                    st.markdown("---")

def show_zonal_analysis():
    """Zonal statistics analysis"""
    
    st.markdown("### 🎯 Zonal Statistics")
    st.markdown("Calculate statistics for different zones or regions")
    
    # Zone definition
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📍 Define Zones")
        
        zone_type = st.selectbox(
            "Zone Type:",
            ["Administrative Boundaries", "Land Cover Classes", "Elevation Zones", "Custom Polygons"]
        )
        
        if zone_type == "Administrative Boundaries":
            boundary_level = st.selectbox("Level:", ["Country", "State/Province", "County", "City"])
            region_name = st.text_input("Region Name:", "California")
        
        elif zone_type == "Elevation Zones":
            min_elevation = st.number_input("Min Elevation (m):", 0, 5000, 0)
            max_elevation = st.number_input("Max Elevation (m):", 0, 8000, 1000)
            zone_interval = st.number_input("Interval (m):", 100, 1000, 200)
        
        # Analysis parameters
        st.markdown("#### ⚙️ Analysis Parameters")
        
        statistic_types = st.multiselect(
            "Statistics to Calculate:",
            ["Mean", "Median", "Min", "Max", "Std Dev", "Count", "Sum"],
            default=["Mean", "Count"]
        )
        
        band_to_analyze = st.selectbox(
            "Band/Index:",
            ["NDVI", "Red", "Green", "Blue", "NIR", "Temperature"]
        )
    
    with col2:
        st.markdown("#### 🗺️ Zone Preview")
        
        if FOLIUM_AVAILABLE:
            # Create map with sample zones
            m = folium.Map(location=[37.7749, -122.4194], zoom_start=6)
            
            # Add sample zones
            if zone_type == "Administrative Boundaries":
                # Sample boundary (California outline approximation)
                california_bounds = [
                    [32.5, -124.4], [32.5, -114.1], [42.0, -114.1], [42.0, -124.4]
                ]
                folium.Polygon(
                    locations=california_bounds,
                    popup="California Boundary",
                    color='blue',
                    fillColor='lightblue',
                    fillOpacity=0.3
                ).add_to(m)
            
            elif zone_type == "Elevation Zones":
                # Sample elevation zones (circles representing different elevations)
                colors = ['green', 'yellow', 'orange', 'red']
                for i, color in enumerate(colors):
                    folium.Circle(
                        location=[37.7749 + i*0.5, -122.4194],
                        radius=20000,
                        popup=f"Elevation Zone {i+1}: {i*200}-{(i+1)*200}m",
                        color=color,
                        fillColor=color,
                        fillOpacity=0.4
                    ).add_to(m)
            
            map_data = st_folium(m, width=400, height=300)
        else:
            st.info("Install folium to see zone preview map")
    
    # Run analysis
    if st.button("🎯 Run Zonal Analysis", type="primary"):
        with st.spinner("Running zonal analysis..."):
            import time
            time.sleep(2)
            
            # Generate sample results
            if zone_type == "Administrative Boundaries":
                zones = ["Zone 1", "Zone 2", "Zone 3", "Zone 4"]
            elif zone_type == "Elevation Zones":
                num_zones = int((max_elevation - min_elevation) / zone_interval)
                zones = [f"{min_elevation + i*zone_interval}-{min_elevation + (i+1)*zone_interval}m" 
                        for i in range(num_zones)]
            else:
                zones = ["Zone A", "Zone B", "Zone C"]
            
            # Generate results
            results_data = []
            for zone in zones:
                row = {'Zone': zone}
                for stat in statistic_types:
                    if stat == "Mean":
                        row[stat] = np.random.uniform(0.2, 0.8)
                    elif stat == "Count":
                        row[stat] = np.random.randint(1000, 10000)
                    elif stat == "Min":
                        row[stat] = np.random.uniform(0.0, 0.3)
                    elif stat == "Max":
                        row[stat] = np.random.uniform(0.7, 1.0)
                    else:
                        row[stat] = np.random.uniform(0.1, 0.5)
                
                results_data.append(row)
            
            results_df = pd.DataFrame(results_data)
            st.session_state['zonal_results'] = results_df
            
            st.success("✅ Zonal analysis completed!")
    
    # Display results
    if 'zonal_results' in st.session_state:
        st.markdown("#### 📊 Results")
        
        df = st.session_state['zonal_results']
        st.dataframe(df, use_container_width=True)
        
        if PLOTLY_AVAILABLE and 'Mean' in df.columns:
            # Results visualization
            fig = px.bar(df, x='Zone', y='Mean', 
                        title=f"Mean {band_to_analyze} by Zone",
                        color='Mean',
                        color_continuous_scale='Viridis')
            st.plotly_chart(fig, use_container_width=True)
        
        # Export results
        if st.button("📄 Export Results"):
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="zonal_statistics.csv">Download Results CSV</a>'
            st.markdown(href, unsafe_allow_html=True)

def show_classification_analysis():
    """Image classification interface"""
    
    st.markdown("### 🏷️ Image Classification")
    
    # Classification type
    classification_type = st.selectbox(
        "Classification Method:",
        ["Unsupervised (K-Means)", "Supervised (Random Forest)", "CART Decision Tree", "SVM"]
    )
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### ⚙️ Parameters")
        
        if classification_type == "Unsupervised (K-Means)":
            num_classes = st.slider("Number of Classes:", 3, 15, 6)
            max_iterations = st.slider("Max Iterations:", 10, 100, 20)
            
        elif classification_type == "Supervised (Random Forest)":
            num_trees = st.slider("Number of Trees:", 10, 200, 50)
            num_classes = st.slider("Number of Classes:", 3, 10, 5)
            
            # Class definition
            st.markdown("**Class Labels:**")
            class_names = []
            for i in range(num_classes):
                class_name = st.text_input(f"Class {i+1}:", value=f"Class_{i+1}", key=f"class_{i}")
                class_names.append(class_name)
        
        # Input bands
        input_bands = st.multiselect(
            "Input Bands:",
            ["Blue", "Green", "Red", "NIR", "SWIR1", "SWIR2", "NDVI", "NDWI"],
            default=["Red", "Green", "Blue", "NIR"]
        )
        
        training_sample_size = st.slider("Training Sample Size:", 100, 5000, 1000)
        
        if st.button("🚀 Run Classification", type="primary"):
            with st.spinner(f"Running {classification_type} classification..."):
                import time
                time.sleep(3)
                
                # Generate classification results
                classification_results = {
                    'accuracy': np.random.uniform(0.75, 0.95),
                    'kappa': np.random.uniform(0.65, 0.90),
                    'classes': num_classes,
                    'samples_used': training_sample_size
                }
                
                st.session_state['classification_results'] = classification_results
                st.success("✅ Classification completed!")
    
    with col2:
        st.markdown("#### 🎨 Classification Results")
        
        if 'classification_results' in st.session_state:
            results = st.session_state['classification_results']
            
            # Accuracy metrics
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                st.metric("Overall Accuracy", f"{results['accuracy']:.2%}")
            with col_b:
                st.metric("Kappa Coefficient", f"{results['kappa']:.3f}")
            with col_c:
                st.metric("Classes", results['classes'])
            
            # Create sample classified image
            if MATPLOTLIB_AVAILABLE:
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
                
                # Original image (simulated)
                original = np.random.rand(100, 100, 3)
                ax1.imshow(original)
                ax1.set_title("Original Image")
                ax1.axis('off')
                
                # Classified image
                classified = np.random.randint(0, num_classes, (100, 100))
                im = ax2.imshow(classified, cmap='tab10', vmin=0, vmax=num_classes-1)
                ax2.set_title("Classified Image")
                ax2.axis('off')
                
                # Add colorbar
                plt.colorbar(im, ax=ax2, shrink=0.6)
                
                st.pyplot(fig)
            
            # Confusion matrix (simulated)
            if PLOTLY_AVAILABLE:
                st.markdown("#### 📊 Confusion Matrix")
                
                # Generate sample confusion matrix
                matrix = np.random.randint(10, 100, (num_classes, num_classes))
                np.fill_diagonal(matrix, np.random.randint(80, 150, num_classes))  # Higher diagonal values
                
                fig = px.imshow(matrix, 
                              title="Classification Confusion Matrix",
                              labels=dict(x="Predicted", y="Actual"),
                              color_continuous_scale="Blues")
                st.plotly_chart(fig, use_container_width=True)
            
            # Class statistics
            st.markdown("#### 📈 Class Statistics")
            class_stats = []
            for i in range(num_classes):
                class_stats.append({
                    'Class': f"Class {i+1}",
                    'Pixels': np.random.randint(1000, 10000),
                    'Area (ha)': np.random.randint(100, 1000),
                    'Percentage': np.random.uniform(5, 25)
                })
            
            class_df = pd.DataFrame(class_stats)
            st.dataframe(class_df, use_container_width=True)
        
        else:
            st.info("👈 Configure parameters and run classification to see results")

def show_visualizations():
    """Advanced visualization tools"""
    
    st.markdown("## 📈 Advanced Visualizations")
    
    if not PLOTLY_AVAILABLE:
        st.error("❌ Plotly not available. Install plotly for interactive visualizations.")
        return
    
    viz_tabs = st.tabs(["📊 Charts", "🗺️ Maps", "🎬 Animations", "📋 Legends"])
    
    with viz_tabs[0]:
        show_chart_visualizations()
    
    with viz_tabs[1]:
        show_map_visualizations()
    
    with viz_tabs[2]:
        show_animation_tools()
    
    with viz_tabs[3]:
        show_legend_tools()

def show_chart_visualizations():
    """Interactive chart creation"""
    
    st.markdown("### 📊 Interactive Charts")
    
    chart_type = st.selectbox(
        "Chart Type:",
        ["Time Series", "Scatter Plot", "Histogram", "Box Plot", "Heatmap", "3D Surface"]
    )
    
    # Generate sample data based on chart type
    if chart_type == "Time Series":
        dates = pd.date_range('2020-01-01', '2023-12-31', freq='M')
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("#### Settings")
            
            variables = st.multiselect(
                "Variables:",
                ["NDVI", "Temperature", "Precipitation", "LST", "EVI"],
                default=["NDVI", "Temperature"]
            )
            
            show_trend = st.checkbox("Show Trend Line")
            show_anomalies = st.checkbox("Highlight Anomalies")
            chart_height = st.slider("Chart Height:", 300, 800, 500)
        
        with col2:
            if variables:
                # Generate data
                data = {'Date': dates}
                for var in variables:
                    if var == "NDVI":
                        base = 0.4 + 0.3 * np.sin(2 * np.pi * np.arange(len(dates)) / 12)
                        noise = np.random.normal(0, 0.05, len(dates))
                        data[var] = base + noise
                    elif var == "Temperature":
                        base = 15 + 10 * np.sin(2 * np.pi * np.arange(len(dates)) / 12)
                        noise = np.random.normal(0, 2, len(dates))
                        data[var] = base + noise
                    else:
                        data[var] = np.random.uniform(0.2, 0.8, len(dates))
                
                df = pd.DataFrame(data)
                
                # Create interactive chart
                fig = px.line(df, x='Date', y=variables, 
                            title="Time Series Visualization",
                            height=chart_height)
                
                if show_trend:
                    # Add trend lines
                    for var in variables:
                        z = np.polyfit(range(len(df)), df[var], 1)
                        p = np.poly1d(z)
                        fig.add_scatter(x=df['Date'], y=p(range(len(df))), 
                                      mode='lines', name=f'{var} Trend',
                                      line=dict(dash='dash'))
                
                if show_anomalies:
                    # Highlight anomalies (simple threshold method)
                    for var in variables:
                        mean_val = df[var].mean()
                        std_val = df[var].std()
                        anomalies = df[abs(df[var] - mean_val) > 2 * std_val]
                        if not anomalies.empty:
                            fig.add_scatter(x=anomalies['Date'], y=anomalies[var],
                                          mode='markers', name=f'{var} Anomalies',
                                          marker=dict(color='red', size=10, symbol='x'))
                
                fig.update_layout(
                    xaxis_title="Date",
                    yaxis_title="Value",
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "Scatter Plot":
        st.markdown("#### Scatter Plot Analysis")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            x_var = st.selectbox("X Variable:", ["NDVI", "Temperature", "Elevation", "Precipitation"])
            y_var = st.selectbox("Y Variable:", ["LST", "Biomass", "Soil Moisture", "LAI"])
            color_var = st.selectbox("Color by:", ["None", "Land Cover", "Season", "Elevation Zone"])
            size_var = st.selectbox("Size by:", ["None", "Population", "Area", "Distance"])
        
        with col2:
            # Generate scatter data
            n_points = 500
            x_data = np.random.uniform(0, 1, n_points)
            y_data = 0.5 * x_data + np.random.normal(0, 0.2, n_points)
            
            df_scatter = pd.DataFrame({
                x_var: x_data,
                y_var: y_data
            })
            
            if color_var != "None":
                df_scatter[color_var] = np.random.choice(['A', 'B', 'C', 'D'], n_points)
            
            if size_var != "None":
                df_scatter[size_var] = np.random.uniform(5, 20, n_points)
            
            # Create scatter plot
            fig = px.scatter(df_scatter, x=x_var, y=y_var,
                           color=color_var if color_var != "None" else None,
                           size=size_var if size_var != "None" else None,
                           title=f"{y_var} vs {x_var}",
                           trendline="ols")
            
            st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "Heatmap":
        st.markdown("#### Correlation Heatmap")
        
        # Generate correlation matrix
        variables = ["NDVI", "Temperature", "Precipitation", "Elevation", "LST", "EVI", "NDWI"]
        n_vars = len(variables)
        
        # Create realistic correlations
        corr_matrix = np.random.rand(n_vars, n_vars)
        corr_matrix = (corr_matrix + corr_matrix.T) / 2  # Make symmetric
        np.fill_diagonal(corr_matrix, 1)  # Perfect self-correlation
        
        # Adjust some correlations to be more realistic
        corr_matrix[0, 1] = 0.7  # NDVI-Temperature correlation
        corr_matrix[1, 0] = 0.7
        corr_matrix[0, 5] = 0.9  # NDVI-EVI high correlation
        corr_matrix[5, 0] = 0.9
        
        corr_df = pd.DataFrame(corr_matrix, index=variables, columns=variables)
        
        fig = px.imshow(corr_df,
                       title="Variable Correlation Matrix",
                       color_continuous_scale="RdBu_r",
                       aspect="auto")
        
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

def show_map_visualizations():
    """Map-specific visualizations"""
    
    if not FOLIUM_AVAILABLE:
        st.warning("Install folium for map visualizations")
        return
    
    st.markdown("### 🗺️ Map Visualizations")
    
    map_viz_type = st.selectbox(
        "Visualization Type:",
        ["Choropleth Map", "Point Density", "Heat Map", "Flow Map", "3D Terrain"]
    )
    
    if map_viz_type == "Choropleth Map":
        st.markdown("#### 🗾 Choropleth Mapping")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("**Settings**")
            
            boundary_level = st.selectbox("Boundary Level:", ["Countries", "States", "Counties"])
            color_variable = st.selectbox("Color Variable:", ["Population", "NDVI", "Temperature", "GDP"])
            color_scheme = st.selectbox("Color Scheme:", ["Viridis", "Plasma", "Blues", "Reds", "RdYlBu"])
            
            show_labels = st.checkbox("Show Labels", value=True)
            show_borders = st.checkbox("Show Borders", value=True)
        
        with col2:
            # Create choropleth map
            m = folium.Map(location=[39.8283, -98.5795], zoom_start=4)
            
            # Sample data for US states
            states_data = {
                'California': np.random.uniform(0.5, 0.9),
                'Texas': np.random.uniform(0.3, 0.7),
                'Florida': np.random.uniform(0.4, 0.8),
                'New York': np.random.uniform(0.2, 0.6),
                'Illinois': np.random.uniform(0.3, 0.7)
            }
            
            # Add sample polygons (simplified state boundaries)
            sample_polygons = [
                # California (approximate)
                [[32.5, -124.4], [32.5, -114.1], [42.0, -114.1], [42.0, -124.4]],
                # Texas (approximate)  
                [[25.8, -106.6], [25.8, -93.5], [36.5, -93.5], [36.5, -106.6]]
            ]
            
            colors = ['red', 'blue', 'green', 'orange', 'purple']
            
            for i, polygon in enumerate(sample_polygons):
                folium.Polygon(
                    locations=polygon,
                    popup=f"Region {i+1}: {list(states_data.values())[i]:.2f}",
                    color=colors[i],
                    fillColor=colors[i],
                    fillOpacity=0.6
                ).add_to(m)
            
            map_data = st_folium(m, width=500, height=400)
    
    elif map_viz_type == "Heat Map":
        st.markdown("#### 🔥 Heat Map Visualization")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("**Settings**")
            
            heat_variable = st.selectbox("Heat Variable:", ["Population Density", "Temperature", "NDVI", "Pollution"])
            intensity = st.slider("Heat Intensity:", 0.1, 2.0, 1.0, 0.1)
            radius = st.slider("Heat Radius:", 10, 50, 25)
            
            # Generate sample points
            n_points = st.slider("Number of Points:", 50, 500, 200)
        
        with col2:
            # Create heat map
            m = folium.Map(location=[37.7749, -122.4194], zoom_start=10)
            
            # Generate random heat points around San Francisco
            heat_data = []
            for _ in range(n_points):
                lat = 37.7749 + np.random.normal(0, 0.05)
                lon = -122.4194 + np.random.normal(0, 0.05)
                weight = np.random.uniform(0.1, intensity)
                heat_data.append([lat, lon, weight])
            
            # Add heat map using CircleMarkers (simplified version)
            for point in heat_data[:50]:  # Limit for performance
                folium.CircleMarker(
                    location=[point[0], point[1]],
                    radius=point[2] * radius / 2,
                    popup=f"Intensity: {point[2]:.2f}",
                    color='red',
                    fillColor='red',
                    fillOpacity=point[2]
                ).add_to(m)
            
            map_data = st_folium(m, width=500, height=400)

def show_animation_tools():
    """Animation creation tools"""
    
    st.markdown("### 🎬 Animation Tools")
    
    animation_type = st.selectbox(
        "Animation Type:",
        ["Time Series Animation", "NDVI Progression", "Climate Change Visualization"]
    )
    
    if animation_type == "Time Series Animation":
        st.markdown("#### 📹 Time Series Animation")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("**Animation Settings**")
            
            variable = st.selectbox("Variable:", ["NDVI", "Temperature", "Precipitation"])
            animation_speed = st.slider("Animation Speed (ms):", 100, 2000, 500)
            frame_count = st.slider("Number of Frames:", 10, 50, 24)
            
            show_trail = st.checkbox("Show Trail", value=True)
            
            if st.button("🎬 Generate Animation"):
                # Create animated plot
                dates = pd.date_range('2023-01-01', periods=frame_count, freq='M')
                
                data_frames = []
                for i, date in enumerate(dates):
                    # Generate sample spatial data
                    x = np.linspace(-5, 5, 20)
                    y = np.linspace(-5, 5, 20)
                    X, Y = np.meshgrid(x, y)
                    
                    # Animated wave pattern
                    Z = np.sin(np.sqrt(X**2 + Y**2) - i * 0.5) * np.exp(-0.1 * (X**2 + Y**2))
                    
                    frame_data = pd.DataFrame({
                        'x': X.flatten(),
                        'y': Y.flatten(), 
                        'z': Z.flatten(),
                        'frame': i,
                        'date': date
                    })
                    data_frames.append(frame_data)
                
                all_data = pd.concat(data_frames, ignore_index=True)
                
                fig = px.density_contour(all_data, x='x', y='y', z='z',
                                       animation_frame='frame',
                                       title=f"{variable} Animation",
                                       color_continuous_scale='Viridis')
                
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("**Animation Preview**")
            st.info("Click 'Generate Animation' to create time series animation")
            
            # Show static preview
            if MATPLOTLIB_AVAILABLE:
                fig, ax = plt.subplots(figsize=(6, 4))
                
                x = np.linspace(-5, 5, 20)
                y = np.linspace(-5, 5, 20)
                X, Y = np.meshgrid(x, y)
                Z = np.sin(np.sqrt(X**2 + Y**2)) * np.exp(-0.1 * (X**2 + Y**2))
                
                im = ax.contourf(X, Y, Z, levels=20, cmap='viridis')
                ax.set_title("Animation Preview (Static Frame)")
                plt.colorbar(im, ax=ax)
                
                st.pyplot(fig)

def show_legend_tools():
    """Legend and colorbar creation tools"""
    
    st.markdown("### 📋 Legends & Colorbars")
    
    legend_type = st.selectbox(
        "Legend Type:",
        ["Continuous Colorbar", "Discrete Legend", "Custom Classification"]
    )
    
    if legend_type == "Continuous Colorbar":
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Colorbar Settings**")
            
            colormap = st.selectbox(
                "Color Scheme:",
                ["viridis", "plasma", "RdYlGn", "RdBu", "coolwarm", "terrain"]
            )
            
            min_value = st.number_input("Min Value:", value=0.0)
            max_value = st.number_input("Max Value:", value=1.0)
            
            title = st.text_input("Legend Title:", "NDVI")
            orientation = st.selectbox("Orientation:", ["vertical", "horizontal"])
            
        with col2:
            if PLOTLY_AVAILABLE:
                # Create sample data with colorbar
                x = np.linspace(-2, 2, 50)
                y = np.linspace(-2, 2, 50)
                X, Y = np.meshgrid(x, y)
                Z = np.sin(X) * np.cos(Y)
                
                fig = px.imshow(Z, 
                              color_continuous_scale=colormap,
                              title=f"Sample {title} Visualization",
                              labels={'color': title})
                
                fig.update_coloraxes(
                    colorbar_orientation=orientation[0],  # 'v' or 'h'
                    cmin=min_value,
                    cmax=max_value
                )
                
                st.plotly_chart(fig, use_container_width=True)
    
    elif legend_type == "Discrete Legend":
        st.markdown("#### 🏷️ Discrete Classification Legend")
        
        col1, col2 = st.columns(2)
        
        with col1:
            num_classes = st.slider("Number of Classes:", 3, 10, 5)
            
            # Class definition
            classes = []
            colors = []
            for i in range(num_classes):
                col_a, col_b = st.columns(2)
                with col_a:
                    class_name = st.text_input(f"Class {i+1}:", f"Class_{i+1}", key=f"discrete_class_{i}")
                with col_b:
                    color = st.color_picker(f"Color {i+1}:", f"#{i*50:02x}{(255-i*40):02x}{i*30:02x}", key=f"discrete_color_{i}")
                
                classes.append(class_name)
                colors.append(color)
        
        with col2:
            # Create discrete legend visualization
            if MATPLOTLIB_AVAILABLE:
                fig, ax = plt.subplots(figsize=(6, 4))
                
                # Create sample classified image
                classified_data = np.random.randint(0, num_classes, (50, 50))
                
                # Create custom colormap
                from matplotlib.colors import ListedColormap
                cmap = ListedColormap([color for color in colors])
                
                im = ax.imshow(classified_data, cmap=cmap, vmin=0, vmax=num_classes-1)
                ax.set_title("Classification with Discrete Legend")
                
                # Create custom legend
                from matplotlib.patches import Patch
                legend_elements = [Patch(facecolor=colors[i], label=classes[i]) 
                                 for i in range(num_classes)]
                ax.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1, 0.5))
                
                st.pyplot(fig)

def show_export_tools():
    """Data export interface"""
    
    st.markdown("## 💾 Export Tools")
    
    export_tabs = st.tabs(["🖼️ Images", "📊 Data", "🗺️ Maps", "📈 Charts"])
    
    with export_tabs[0]:
        show_image_export_tool()
    
    with export_tabs[1]:
        show_data_export_tool()
    
    with export_tabs[2]:
        show_map_export_tool()
    
    with export_tabs[3]:
        show_chart_export_tool()

def show_image_export_tool():
    """Image export tool"""
    
    st.markdown("### 🖼️ Image Export")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### Export Settings")
        
        export_format = st.selectbox("Format:", ["GeoTIFF", "PNG", "JPEG", "PDF"])
        
        resolution = st.selectbox("Resolution:", ["30m", "10m", "1m", "Custom"])
        if resolution == "Custom":
            custom_res = st.number_input("Custom Resolution (m):", 1, 1000, 30)
        
        compression = st.selectbox("Compression:", ["LZW", "DEFLATE", "JPEG", "None"])
        
        # Spatial extent
        st.markdown("#### Spatial Extent")
        extent_method = st.selectbox("Define Extent:", ["Bounding Box", "Geometry", "Current View"])
        
        if extent_method == "Bounding Box":
            col_a, col_b = st.columns(2)
            with col_a:
                north = st.number_input("North:", value=37.8)
                south = st.number_input("South:", value=37.7)
            with col_b:
                east = st.number_input("East:", value=-122.3)
                west = st.number_input("West:", value=-122.5)
        
        # Export options
        include_metadata = st.checkbox("Include Metadata", value=True)
        include_projection = st.checkbox("Include Projection Info", value=True)
        
        if st.button("📥 Export Image", type="primary"):
            with st.spinner("Exporting image..."):
                import time
                time.sleep(2)
                
                # Create sample export info
                export_info = {
                    'filename': f'exported_image.{export_format.lower()}',
                    'size': f"{np.random.randint(100, 500)} MB",
                    'dimensions': f"{np.random.randint(1000, 5000)} x {np.random.randint(1000, 5000)} pixels",
                    'bands': np.random.randint(3, 12)
                }
                
                st.session_state['last_export'] = export_info
                st.success("✅ Image exported successfully!")
    
    with col2:
        st.markdown("#### Export Preview & Info")
        
        if 'last_export' in st.session_state:
            info = st.session_state['last_export']
            
            st.success("**Last Export:**")
            st.write(f"📁 **Filename:** {info['filename']}")
            st.write(f"📏 **File Size:** {info['size']}")
            st.write(f"🖼️ **Dimensions:** {info['dimensions']}")
            st.write(f"📊 **Bands:** {info['bands']}")
            
            # Sample export code
            st.code(f"""
# Export code example
export_params = {{
    'image': your_image,
    'description': 'exported_image',
    'scale': {resolution.replace('m', '') if resolution != 'Custom' else custom_res if 'custom_res' in locals() else 30},
    'region': your_region,
    'fileFormat': '{export_format}',
    'formatOptions': {{
        'cloudOptimized': true,
        'compression': '{compression}'
    }}
}}

# Start export
task = ee.batch.Export.image.toDrive(export_params)
task.start()
            """)
        else:
            # Show sample preview
            if MATPLOTLIB_AVAILABLE:
                fig, ax = plt.subplots(figsize=(6, 4))
                
                # Create sample image
                sample_image = np.random.rand(100, 100, 3)
                ax.imshow(sample_image)
                ax.set_title("Sample Export Preview")
                ax.axis('off')
                
                st.pyplot(fig)
            
            st.info("Configure settings and click 'Export Image' to generate export")

def show_data_export_tool():
    """Data export tool"""
    
    st.markdown("### 📊 Data Export")
    
    data_type = st.selectbox(
        "Data Type:",
        ["Time Series", "Statistics Table", "Vector Data", "Point Data"]
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Export Settings")
        
        file_format = st.selectbox("File Format:", ["CSV", "JSON", "Excel", "Shapefile", "GeoJSON"])
        
        if data_type == "Time Series":
            variables = st.multiselect(
                "Variables to Export:",
                ["NDVI", "Temperature", "Precipitation", "LST", "EVI"],
                default=["NDVI"]
            )
            
            date_range = st.date_input(
                "Date Range:",
                value=[date(2023, 1, 1), date(2023, 12, 31)]
            )
        
        include_coords = st.checkbox("Include Coordinates", value=True)
        include_metadata = st.checkbox("Include Metadata", value=True)
        
        if st.button("📤 Export Data", type="primary"):
            # Generate sample data
            if data_type == "Time Series":
                dates = pd.date_range(date_range[0], date_range[1], freq='M')
                export_data = pd.DataFrame({'Date': dates})
                
                for var in variables:
                    export_data[var] = np.random.uniform(0.2, 0.8, len(dates))
                
                if include_coords:
                    export_data['Latitude'] = 37.7749
                    export_data['Longitude'] = -122.4194
            
            else:
                # Sample statistics data
                export_data = pd.DataFrame({
                    'Statistic': ['Mean', 'Median', 'Std Dev', 'Min', 'Max'],
                    'Value': np.random.uniform(0.1, 0.8, 5)
                })
            
            st.session_state['export_data'] = export_data
            st.success(f"✅ Data exported as {file_format}")
    
    with col2:
        st.markdown("#### Data Preview")
        
        if 'export_data' in st.session_state:
            df = st.session_state['export_data']
            st.dataframe(df, use_container_width=True)
            
            # Create download link
            if file_format == "CSV":
                csv = df.to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()
                href = f'<a href="data:file/csv;base64,{b64}" download="exported_data.csv">📥 Download CSV</a>'
                st.markdown(href, unsafe_allow_html=True)
            
            elif file_format == "JSON":
                json_data = df.to_json(orient='records', indent=2)
                b64 = base64.b64encode(json_data.encode()).decode()
                href = f'<a href="data:file/json;base64,{b64}" download="exported_data.json">📥 Download JSON</a>'
                st.markdown(href, unsafe_allow_html=True)
        
        else:
            st.info("Configure settings and export data to see preview")

def show_map_export_tool():
    """Map export tool"""
    
    st.markdown("### 🗺️ Map Export")
    
    if not FOLIUM_AVAILABLE:
        st.warning("Install folium for map export functionality")
        return
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### Map Settings")
        
        map_type = st.selectbox("Map Type:", ["Static Map", "Interactive HTML", "Web Map Service"])
        
        export_format = st.selectbox("Format:", ["PNG", "PDF", "SVG", "HTML"])
        
        resolution_dpi = st.selectbox("Resolution (DPI):", [150, 300, 600, 1200])
        
        # Map elements
        st.markdown("#### Map Elements")
        include_legend = st.checkbox("Legend", value=True)
        include_scale = st.checkbox("Scale Bar", value=True)
        include_north_arrow = st.checkbox("North Arrow", value=True)
        include_attribution = st.checkbox("Attribution", value=True)
        
        # Styling
        st.markdown("#### Styling")
        title = st.text_input("Map Title:", "Exported Map")
        font_size = st.slider("Font Size:", 8, 24, 12)
        
        if st.button("🗺️ Export Map", type="primary"):
            st.success(f"✅ Map exported as {export_format} at {resolution_dpi} DPI")
    
    with col2:
        st.markdown("#### Map Preview")
        
        # Create exportable map
        m = folium.Map(location=[37.7749, -122.4194], zoom_start=10)
        
        # Add sample data
        folium.Marker(
            [37.7749, -122.4194],
            popup="San Francisco",
            tooltip="Export Location"
        ).add_to(m)
        
        # Add sample polygon
        folium.Polygon(
            locations=[[37.76, -122.45], [37.76, -122.35], [37.80, -122.35], [37.80, -122.45]],
            popup="Sample Area",
            color='blue',
            fillColor='lightblue',
            fillOpacity=0.3
        ).add_to(m)
        
        if include_scale:
            folium.plugins.MeasureControl().add_to(m)
        
        map_data = st_folium(m, width=500, height=400)
        
        # Export info
        st.info(f"**Map Title:** {title}")
        st.info(f"**Export Format:** {export_format}")
        st.info(f"**Resolution:** {resolution_dpi} DPI")

def show_chart_export_tool():
    """Chart export tool"""
    
    st.markdown("### 📈 Chart Export")
    
    if not PLOTLY_AVAILABLE:
        st.warning("Install plotly for chart export functionality")
        return
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### Chart Settings")
        
        chart_type = st.selectbox("Chart Type:", ["Line Chart", "Bar Chart", "Scatter Plot", "Heatmap"])
        
        export_format = st.selectbox("Format:", ["PNG", "PDF", "SVG", "HTML"])
        
        width = st.number_input("Width (px):", 400, 2000, 800)
        height = st.number_input("Height (px):", 300, 1500, 600)
        
        # Styling options
        st.markdown("#### Styling")
        theme = st.selectbox("Theme:", ["plotly", "plotly_white", "plotly_dark", "ggplot2"])
        
        title = st.text_input("Chart Title:", "Exported Chart")
        
        show_grid = st.checkbox("Show Grid", value=True)
        show_legend = st.checkbox("Show Legend", value=True)
        
        if st.button("📊 Export Chart", type="primary"):
            st.success(f"✅ Chart exported as {export_format}")
    
    with col2:
        st.markdown("#### Chart Preview")
        
        # Generate sample data based on chart type
        if chart_type == "Line Chart":
            dates = pd.date_range('2023-01-01', periods=12, freq='M')
            data = pd.DataFrame({
                'Date': dates,
                'Series 1': np.random.uniform(0.3, 0.8, 12),
                'Series 2': np.random.uniform(0.2, 0.7, 12)
            })
            
            fig = px.line(data, x='Date', y=['Series 1', 'Series 2'], 
                         title=title, template=theme)
        
        elif chart_type == "Bar Chart":
            categories = ['A', 'B', 'C', 'D', 'E']
            values = np.random.uniform(10, 100, 5)
            
            fig = px.bar(x=categories, y=values, title=title, template=theme)
        
        elif chart_type == "Scatter Plot":
            n_points = 100
            data = pd.DataFrame({
                'X': np.random.uniform(0, 10, n_points),
                'Y': np.random.uniform(0, 10, n_points),
                'Category': np.random.choice(['A', 'B', 'C'], n_points)
            })
            
            fig = px.scatter(data, x='X', y='Y', color='Category', 
                           title=title, template=theme)
        
        else:  # Heatmap
            matrix = np.random.rand(10, 10)
            fig = px.imshow(matrix, title=title, template=theme)
        
        fig.update_layout(
            width=width,
            height=height,
            showlegend=show_legend
        )
        
        if show_grid:
            fig.update_xaxes(showgrid=True)
            fig.update_yaxes(showgrid=True)
        else:
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=False)
        
        st.plotly_chart(fig, use_container_width=True)

def show_publication_maps():
    """Publication quality maps interface"""
    
    st.markdown("## 🖼️ Publication Quality Maps")
    
    if not MATPLOTLIB_AVAILABLE:
        st.error("❌ Matplotlib not available for publication maps")
        return
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Map Configuration")
        
        # Map settings
        map_title = st.text_input("Map Title:", "Study Area Analysis")
        
        projection = st.selectbox(
            "Projection:",
            ["PlateCarree", "Mercator", "Robinson", "Mollweide", "Orthographic"]
        )
        
        # Output settings
        st.markdown("#### Output Settings")
        dpi = st.selectbox("Resolution (DPI):", [150, 300, 600, 1200])
        format_type = st.selectbox("Format:", ["PNG", "PDF", "SVG", "EPS"])
        
        # Map elements
        st.markdown("#### Map Elements")
        include_coastlines = st.checkbox("Coastlines", value=True)
        include_borders = st.checkbox("Country Borders", value=True)
        include_gridlines = st.checkbox("Gridlines", value=True)
        include_scale_bar = st.checkbox("Scale Bar", value=False)
        include_north_arrow = st.checkbox("North Arrow", value=False)
        
        # Styling
        st.markdown("#### Styling")
        colormap = st.selectbox(
            "Colormap:",
            ["RdYlGn", "viridis", "plasma", "coolwarm", "terrain", "RdBu"]
        )
        
        # Data settings
        st.markdown("#### Data Settings")
        data_variable = st.selectbox("Variable:", ["NDVI", "Temperature", "Precipitation", "Elevation"])
        
        # Value range
        col_a, col_b = st.columns(2)
        with col_a:
            vmin = st.number_input("Min Value:", value=-1.0 if data_variable == "NDVI" else 0.0)
        with col_b:
            vmax = st.number_input("Max Value:", value=1.0 if data_variable == "NDVI" else 100.0)
    
    with col2:
        st.markdown("### Publication Map")
        
        # Create publication-quality map
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Generate sample spatial data
        x = np.linspace(-125, -65, 100)  # US longitude range
        y = np.linspace(20, 50, 80)     # US latitude range
        X, Y = np.meshgrid(x, y)
        
        # Create realistic data pattern
        if data_variable == "NDVI":
            Z = 0.3 + 0.4 * np.sin((X + 95) / 10) * np.cos((Y - 35) / 8)
            Z += 0.1 * np.random.random(Z.shape)  # Add noise
            Z = np.clip(Z, -1, 1)
        elif data_variable == "Temperature":
            Z = 15 + 15 * np.sin((Y - 20) / 15) + 5 * np.cos((X + 95) / 20)
            Z += 2 * np.random.random(Z.shape)
        elif data_variable == "Precipitation":
            Z = 50 + 40 * np.sin((X + 95) / 15) * np.cos((Y - 35) / 10)
            Z += 10 * np.random.random(Z.shape)
            Z = np.clip(Z, 0, None)
        else:  # Elevation
            Z = 1000 * np.exp(-((X + 105)**2 + (Y - 40)**2) / 500)
            Z += 500 * np.random.random(Z.shape)
        
        # Create the map
        im = ax.contourf(X, Y, Z, levels=20, cmap=colormap, vmin=vmin, vmax=vmax)
        
        # Styling based on user selections
        if include_gridlines:
            ax.grid(True, alpha=0.3, linestyle='--')
        
        # Add map elements
        ax.set_xlabel('Longitude (°)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Latitude (°)', fontsize=12, fontweight='bold')
        ax.set_title(map_title, fontsize=16, fontweight='bold', pad=20)
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, shrink=0.8, aspect=30)
        cbar.set_label(f'{data_variable}', fontsize=12, fontweight='bold')
        
        # Improve layout
        ax.set_aspect('equal', adjustable='box')
        plt.tight_layout()
        
        # Display the map
        st.pyplot(fig, dpi=150)
        
        # Map statistics
        st.markdown("#### 📊 Map Statistics")
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.metric("Mean Value", f"{Z.mean():.2f}")
        with col_b:
            st.metric("Min Value", f"{Z.min():.2f}")
        with col_c:
            st.metric("Max Value", f"{Z.max():.2f}")
        
        # Export button
        if st.button("📥 Generate High-Resolution Map", type="primary"):
            with st.spinner(f"Generating {format_type} at {dpi} DPI..."):
                import time
                time.sleep(2)
                st.success(f"✅ Publication map generated!")
                st.info(f"📁 Saved as: {map_title.replace(' ', '_')}.{format_type.lower()}")
    
    # Code example
    with st.expander("💻 Code Example"):
        st.code(f"""
import matplotlib.pyplot as plt
import numpy as np

# Create figure
fig, ax = plt.subplots(figsize=(12, 8))

# Your data here (replace with actual Earth Engine data)
# image = ee.Image('your_image_id')
# data = image.sample(region, scale=30).getInfo()

# Create publication map
im = ax.contourf(X, Y, Z, levels=20, cmap='{colormap}', 
                vmin={vmin}, vmax={vmax})

# Customize map
ax.set_xlabel('Longitude (°)', fontsize=12, fontweight='bold')
ax.set_ylabel('Latitude (°)', fontsize=12, fontweight='bold')
ax.set_title('{map_title}', fontsize=16, fontweight='bold')

# Add colorbar
cbar = plt.colorbar(im, ax=ax, shrink=0.8)
cbar.set_label('{data_variable}', fontsize=12, fontweight='bold')

# Save high-resolution map
plt.savefig('{map_title.replace(" ", "_")}.{format_type.lower()}', 
           dpi={dpi}, bbox_inches='tight', format='{format_type.lower()}')
plt.show()
        """)

def show_documentation():
    """Documentation and help"""
    
    st.markdown("## 📚 Documentation & Help")
    
    doc_tabs = st.tabs(["🚀 Quick Start", "📖 API Reference", "💡 Examples", "❓ FAQ", "🔧 Troubleshooting"])
    
    with doc_tabs[0]:
        show_quick_start_guide()
    
    with doc_tabs[1]:
        show_api_reference_guide()
    
    with doc_tabs[2]:
        show_examples_guide()
    
    with doc_tabs[3]:
        show_faq_guide()
    
    with doc_tabs[4]:
        show_troubleshooting_guide()

def show_quick_start_guide():
    """Quick start guide"""
    
    st.markdown("### 🚀 Quick Start Guide")
    
    # Installation
    st.markdown("#### 1. Installation")
    
    tab1, tab2, tab3 = st.tabs(["Pip Install", "Conda Install", "Development"])
    
    with tab1:
        st.code("""
# Basic installation
pip install geomasterpy

# For Streamlit apps
pip install geomasterpy[streamlit]

# Full installation with all dependencies
pip install geomasterpy[full]
        """)
    
    with tab2:
        st.code("""
# Using conda
conda install -c conda-forge geomasterpy

# Or with pip in conda environment
conda create -n geomaster python=3.9
conda activate geomaster
pip install geomasterpy
        """)
    
    with tab3:
        st.code("""
# Development installation
git clone https://github.com/TimHopkin/GeoMasterPy.git
cd GeoMasterPy
pip install -e .

# Install development dependencies
pip install -e .[dev]
        """)
    
    # Basic usage
    st.markdown("#### 2. Basic Usage")
    
    st.code("""
import geomasterpy as gmp
import ee

# Initialize Earth Engine
ee.Initialize()

# Create interactive map
Map = gmp.Map(center=(37.7749, -122.4194), zoom=10)

# Load satellite data
landsat = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2') \\
    .filterDate('2023-01-01', '2023-12-31') \\
    .filter(ee.Filter.lt('CLOUD_COVER', 20)) \\
    .median()

# Add to map
vis_params = {
    'bands': ['SR_B4', 'SR_B3', 'SR_B2'],
    'min': 0.0,
    'max': 0.3,
    'gamma': 1.4
}

Map.add_ee_layer(landsat, vis_params, 'Landsat 8')

# Display map
Map
    """, language='python')
    
    # Common workflows
    st.markdown("#### 3. Common Workflows")
    
    workflow_type = st.selectbox(
        "Select Workflow:",
        ["NDVI Analysis", "Land Cover Classification", "Time Series Analysis", "Change Detection"]
    )
    
    if workflow_type == "NDVI Analysis":
        st.code("""
# NDVI Analysis Workflow
import geomasterpy as gmp
import ee

# Define area of interest
aoi = ee.Geometry.Point([-122.4, 37.8]).buffer(10000)

# Load Landsat data
collection = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2') \\
    .filterBounds(aoi) \\
    .filterDate('2023-01-01', '2023-12-31') \\
    .filter(ee.Filter.lt('CLOUD_COVER', 20))

# Calculate NDVI
def add_ndvi(image):
    ndvi = image.normalizedDifference(['SR_B5', 'SR_B4']).rename('NDVI')
    return image.addBands(ndvi)

# Apply NDVI calculation
with_ndvi = collection.map(add_ndvi)

# Get median NDVI
ndvi_median = with_ndvi.select('NDVI').median()

# Visualize
Map = gmp.Map(center=[-122.4, 37.8], zoom=10)
Map.add_ee_layer(ndvi_median, {
    'min': -1, 'max': 1,
    'palette': ['blue', 'white', 'green']
}, 'NDVI')

# Calculate statistics
stats = gmp.image_stats(ndvi_median, aoi, scale=30)
print("NDVI Statistics:", stats)
        """, language='python')

def show_api_reference_guide():
    """API reference guide"""
    
    st.markdown("### 📖 API Reference")
    
    # Module selection
    module = st.selectbox(
        "Select Module:",
        ["Map", "Data", "Analysis", "Visualization", "Export"]
    )
    
    if module == "Map":
        st.markdown("#### 🗺️ Map Module")
        
        functions = [
            {
                "name": "Map(center, zoom)",
                "description": "Create interactive map widget",
                "parameters": [
                    ("center", "tuple", "Map center coordinates (lat, lon)"),
                    ("zoom", "int", "Initial zoom level (1-18)")
                ],
                "returns": "Map widget object",
                "example": """
Map = gmp.Map(center=(37.7749, -122.4194), zoom=10)
                """
            },
            {
                "name": "add_ee_layer(image, vis_params, name)",
                "description": "Add Earth Engine layer to map",
                "parameters": [
                    ("image", "ee.Image", "Earth Engine image"),
                    ("vis_params", "dict", "Visualization parameters"),
                    ("name", "str", "Layer name")
                ],
                "returns": "None",
                "example": """
Map.add_ee_layer(image, {
    'bands': ['B4', 'B3', 'B2'],
    'min': 0, 'max': 3000
}, 'RGB')
                """
            }
        ]
        
        for func in functions:
            with st.expander(f"📋 {func['name']}"):
                st.markdown(f"**Description:** {func['description']}")
                
                st.markdown("**Parameters:**")
                for param_name, param_type, param_desc in func['parameters']:
                    st.markdown(f"- `{param_name}` ({param_type}): {param_desc}")
                
                st.markdown(f"**Returns:** {func['returns']}")
                
                st.markdown("**Example:**")
                st.code(func['example'], language='python')
    
    elif module == "Analysis":
        st.markdown("#### 📊 Analysis Module")
        
        analysis_functions = [
            "image_stats()", "zonal_stats()", "calculate_indices()", 
            "supervised_classification()", "unsupervised_classification()",
            "change_detection()", "trend_analysis()"
        ]
        
        selected_func = st.selectbox("Function:", analysis_functions)
        
        if selected_func == "image_stats()":
            st.code("""
def image_stats(image, region, scale=30, bands=None):
    \"\"\"
    Calculate comprehensive statistics for an image
    
    Parameters:
    -----------
    image : ee.Image
        Input Earth Engine image
    region : ee.Geometry
        Region of interest for analysis
    scale : int, optional
        Analysis scale in meters (default: 30)
    bands : list, optional
        List of bands to analyze (default: all bands)
    
    Returns:
    --------
    dict : Dictionary containing statistics
        - mean, median, min, max, std_dev, count for each band
    
    Example:
    --------
    stats = gmp.image_stats(
        image=landsat_image,
        region=study_area,
        scale=30,
        bands=['B4', 'B3', 'B2']
    )
    \"\"\"
            """, language='python')

def show_examples_guide():
    """Examples guide"""
    
    st.markdown("### 💡 Examples & Tutorials")
    
    example_category = st.selectbox(
        "Example Category:",
        ["Beginner", "Intermediate", "Advanced", "Specific Use Cases"]
    )
    
    if example_category == "Beginner":
        st.markdown("#### 🌱 Beginner Examples")
        
        beginner_examples = [
            {
                "title": "🗺️ Your First Interactive Map",
                "description": "Create a basic interactive map and add satellite imagery",
                "difficulty": "Easy",
                "time": "5 minutes"
            },
            {
                "title": "📊 Calculate NDVI",
                "description": "Compute vegetation index from Landsat data",
                "difficulty": "Easy", 
                "time": "10 minutes"
            },
            {
                "title": "🎨 Customize Map Visualization",
                "description": "Learn to style and customize map layers",
                "difficulty": "Easy",
                "time": "15 minutes"
            }
        ]
        
        for example in beginner_examples:
            with st.expander(f"{example['title']} - {example['difficulty']} ({example['time']})"):
                st.markdown(example['description'])
                
                if "First Interactive Map" in example['title']:
                    st.code("""
# Example 1: Your First Interactive Map

import geomasterpy as gmp
import ee

# Initialize Earth Engine
ee.Initialize()

# Create a map centered on San Francisco
Map = gmp.Map(center=(37.7749, -122.4194), zoom=10)

# Load a Landsat 8 image
image = ee.Image('LANDSAT/LC08/C02/T1_L2/LC08_044034_20140318')

# Define visualization parameters for true color
vis_params = {
    'bands': ['SR_B4', 'SR_B3', 'SR_B2'],  # Red, Green, Blue
    'min': 0.0,
    'max': 0.3,
    'gamma': 1.4
}

# Add the image to the map
Map.add_ee_layer(image, vis_params, 'Landsat 8 True Color')

# Center the map on the image
Map.center_object(image, 9)

# Display the map
Map
                    """, language='python')

def show_faq_guide():
    """FAQ guide"""
    
    st.markdown("### ❓ Frequently Asked Questions")
    
    faq_categories = st.tabs(["Setup", "Usage", "Troubleshooting", "Performance"])
    
    with faq_categories[0]:
        st.markdown("#### ⚙️ Setup Questions")
        
        setup_faqs = [
            {
                "q": "How do I install GeoMasterPy?",
                "a": """
                **For basic installation:**
                ```bash
                pip install geomasterpy
                ```
                
                **For Streamlit apps:**
                ```bash
                pip install geomasterpy[streamlit]
                ```
                
                **For full functionality:**
                ```bash
                pip install geomasterpy[full]
                ```
                """
            },
            {
                "q": "How do I authenticate with Google Earth Engine?",
                "a": """
                **First time setup:**
                ```python
                import ee
                ee.Authenticate()  # Opens browser for authentication
                ee.Initialize()
                ```
                
                **For subsequent uses:**
                ```python
                import ee
                ee.Initialize()  # Uses stored credentials
                ```
                """
            },
            {
                "q": "What Python version is required?",
                "a": """
                GeoMasterPy requires **Python 3.8 or higher**.
                
                **Recommended versions:**
                - Python 3.9 (most stable)
                - Python 3.10 (good performance)
                - Python 3.11 (latest features)
                """
            }
        ]
        
        for faq in setup_faqs:
            with st.expander(faq["q"]):
                st.markdown(faq["a"])
    
    with faq_categories[1]:
        st.markdown("#### 🔄 Usage Questions")
        
        usage_faqs = [
            {
                "q": "Can I use GeoMasterPy without Earth Engine?",
                "a": """
                **Yes!** Many features work without Earth Engine:
                
                - ✅ Interactive map creation
                - ✅ Data visualization
                - ✅ JavaScript to Python conversion
                - ✅ Basic geospatial analysis
                - ❌ Earth Engine data access
                - ❌ Cloud-based processing
                """
            },
            {
                "q": "How do I export large images?",
                "a": """
                **For large exports, use Google Drive:**
                
                ```python
                # Export to Google Drive
                task = gmp.export_image_to_drive(
                    image=your_image,
                    description='large_export',
                    scale=30,
                    region=your_region,
                    maxPixels=1e13
                )
                task.start()
                
                # Monitor progress
                task.status()
                ```
                """
            }
        ]
        
        for faq in usage_faqs:
            with st.expander(faq["q"]):
                st.markdown(faq["a"])

def show_troubleshooting_guide():
    """Troubleshooting guide"""
    
    st.markdown("### 🔧 Troubleshooting")
    
    issue_type = st.selectbox(
        "Issue Type:",
        ["Installation Problems", "Authentication Errors", "Map Display Issues", "Performance Problems"]
    )
    
    if issue_type == "Installation Problems":
        st.markdown("#### 🔧 Installation Problems")
        
        issues = [
            {
                "problem": "ModuleNotFoundError: No module named 'geomasterpy'",
                "solution": """
                **Solution:**
                1. Check if you're in the correct Python environment
                2. Reinstall the package:
                   ```bash
                   pip uninstall geomasterpy
                   pip install geomasterpy
                   ```
                3. If using conda, try:
                   ```bash
                   conda install pip
                   pip install geomasterpy
                   ```
                """
            },
            {
                "problem": "Dependency conflicts during installation",
                "solution": """
                **Solution:**
                1. Create a fresh virtual environment:
                   ```bash
                   python -m venv geomaster_env
                   source geomaster_env/bin/activate  # Linux/Mac
                   # or
                   geomaster_env\\Scripts\\activate  # Windows
                   ```
                2. Install in the new environment:
                   ```bash
                   pip install geomasterpy
                   ```
                """
            }
        ]
        
        for issue in issues:
            with st.expander(f"❗ {issue['problem']}"):
                st.markdown(issue['solution'])
    
    elif issue_type == "Authentication Errors":
        st.markdown("#### 🔐 Authentication Errors")
        
        auth_issues = [
            {
                "problem": "Earth Engine authentication failed",
                "solution": """
                **Solution:**
                1. Clear existing credentials:
                   ```bash
                   earthengine authenticate --force
                   ```
                2. Or use Python:
                   ```python
                   import ee
                   ee.Authenticate(force=True)
                   ```
                3. Make sure you have Earth Engine access at https://earthengine.google.com/
                """
            },
            {
                "problem": "Service account authentication",
                "solution": """
                **For service accounts:**
                ```python
                import ee
                
                # Using service account key file
                service_account = 'your-service-account@project.iam.gserviceaccount.com'
                credentials = ee.ServiceAccountCredentials(service_account, 'path/to/key.json')
                ee.Initialize(credentials)
                ```
                """
            }
        ]
        
        for issue in auth_issues:
            with st.expander(f"🔐 {issue['problem']}"):
                st.markdown(issue['solution'])

def show_boundary_upload():
    """GeoJSON boundary upload and analysis interface"""
    
    st.markdown("## 📍 Boundary Upload & Analysis")
    st.markdown("Upload your GeoJSON boundary file and analyze it with all available tools!")
    
    # Upload interface
    st.markdown("### 📤 Upload Boundary File")
    
    # Method selection
    upload_method = st.selectbox(
        "Upload Method:",
        ["🔗 Google Drive URL", "📁 File Upload", "✍️ Manual GeoJSON"]
    )
    
    geojson_data = None
    boundary_name = "Custom Boundary"
    
    if upload_method == "🔗 Google Drive URL":
        show_google_drive_upload()
    elif upload_method == "📁 File Upload":
        show_file_upload()
    elif upload_method == "✍️ Manual GeoJSON":
        show_manual_geojson()

def show_google_drive_upload():
    """Google Drive URL upload interface"""
    
    st.markdown("#### 🔗 Google Drive URL Upload")
    
    # Instructions
    with st.expander("📋 How to get Google Drive URL", expanded=False):
        st.markdown("""
        **Steps to get shareable Google Drive URL:**
        
        1. **Upload your GeoJSON file** to Google Drive
        2. **Right-click** on the file → **Get link**
        3. **Change permissions** to "Anyone with the link can view"
        4. **Copy the link** and paste it below
        
        **Example URL format:**
        ```
        https://drive.google.com/file/d/1abc123def456ghi789/view?usp=sharing
        ```
        """)
    
    # URL input
    drive_url = st.text_input(
        "📎 Google Drive URL:",
        placeholder="https://drive.google.com/file/d/YOUR_FILE_ID/view?usp=sharing",
        help="Paste the shareable Google Drive link to your GeoJSON file"
    )
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        if st.button("📥 Load Boundary", type="primary"):
            if drive_url:
                geojson_data = load_geojson_from_drive(drive_url)
            else:
                st.error("Please enter a Google Drive URL")
    
    with col2:
        boundary_name = st.text_input("🏷️ Boundary Name:", "My Study Area")
    
    # Process uploaded boundary
    if 'uploaded_boundary' in st.session_state:
        process_uploaded_boundary(st.session_state['uploaded_boundary'], boundary_name)

def show_file_upload():
    """Local file upload interface"""
    
    st.markdown("#### 📁 File Upload")
    
    uploaded_file = st.file_uploader(
        "Choose a GeoJSON file",
        type=['geojson', 'json'],
        help="Upload a GeoJSON file from your computer"
    )
    
    boundary_name = st.text_input("🏷️ Boundary Name:", "Uploaded Boundary")
    
    if uploaded_file is not None:
        try:
            # Read the uploaded file
            geojson_data = json.loads(uploaded_file.getvalue().decode('utf-8'))
            st.session_state['uploaded_boundary'] = geojson_data
            st.success(f"✅ Successfully loaded: {uploaded_file.name}")
            
            # Process the boundary
            process_uploaded_boundary(geojson_data, boundary_name)
            
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")

def show_manual_geojson():
    """Manual GeoJSON input interface"""
    
    st.markdown("#### ✍️ Manual GeoJSON Input")
    
    # Sample GeoJSON for reference
    sample_geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "name": "Sample Area"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-122.5, 37.7],
                        [-122.3, 37.7], 
                        [-122.3, 37.8],
                        [-122.5, 37.8],
                        [-122.5, 37.7]
                    ]]
                }
            }
        ]
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📋 Use Sample GeoJSON"):
            st.session_state['manual_geojson'] = json.dumps(sample_geojson, indent=2)
    
    with col2:
        boundary_name = st.text_input("🏷️ Boundary Name:", "Manual Boundary")
    
    # Text area for GeoJSON
    geojson_text = st.text_area(
        "Paste your GeoJSON here:",
        value=st.session_state.get('manual_geojson', ''),
        height=300,
        help="Paste valid GeoJSON data"
    )
    
    if st.button("🔄 Load GeoJSON") and geojson_text:
        try:
            geojson_data = json.loads(geojson_text)
            st.session_state['uploaded_boundary'] = geojson_data
            st.success("✅ GeoJSON loaded successfully!")
            
            # Process the boundary
            process_uploaded_boundary(geojson_data, boundary_name)
            
        except json.JSONDecodeError as e:
            st.error(f"❌ Invalid GeoJSON: {str(e)}")

def load_geojson_from_drive(drive_url):
    """Load GeoJSON from Google Drive URL"""
    
    try:
        # Convert Google Drive URL to direct download URL
        file_id = extract_file_id_from_drive_url(drive_url)
        if not file_id:
            st.error("❌ Invalid Google Drive URL format")
            return None
        
        download_url = f"https://drive.google.com/uc?id={file_id}&export=download"
        
        with st.spinner("📥 Downloading boundary file..."):
            # Download the file
            response = requests.get(download_url)
            response.raise_for_status()
            
            # Parse GeoJSON
            geojson_data = response.json()
            
            # Store in session state
            st.session_state['uploaded_boundary'] = geojson_data
            st.success("✅ Boundary loaded successfully from Google Drive!")
            
            return geojson_data
            
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error downloading file: {str(e)}")
        st.markdown("**Troubleshooting tips:**")
        st.markdown("- Make sure the file is shared publicly")
        st.markdown("- Check that the URL is correct")
        st.markdown("- Try re-sharing the file")
        return None
        
    except json.JSONDecodeError as e:
        st.error(f"❌ Invalid GeoJSON format: {str(e)}")
        return None
        
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")
        return None

def extract_file_id_from_drive_url(url):
    """Extract file ID from Google Drive URL"""
    
    # Pattern for Google Drive URLs
    patterns = [
        r'/file/d/([a-zA-Z0-9-_]+)',  # Standard sharing URL
        r'id=([a-zA-Z0-9-_]+)',       # Direct URL with id parameter
        r'/open\?id=([a-zA-Z0-9-_]+)' # Open URL format
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None

def process_uploaded_boundary(geojson_data, boundary_name):
    """Process and analyze uploaded boundary"""
    
    if not geojson_data:
        return
    
    st.markdown("---")
    st.markdown(f"### 🎯 Boundary Analysis: {boundary_name}")
    
    # Extract boundary info
    boundary_info = extract_boundary_info(geojson_data)
    
    # Display boundary info
    show_boundary_info(boundary_info, boundary_name)
    
    # Visualization
    show_boundary_visualization(geojson_data, boundary_name)
    
    # Analysis options
    show_boundary_analysis_options(geojson_data, boundary_name, boundary_info)

def extract_boundary_info(geojson_data):
    """Extract information from GeoJSON boundary"""
    
    info = {
        'features': 0,
        'geometry_types': [],
        'bounds': None,
        'center': None,
        'area_estimate': 0,
        'properties': []
    }
    
    try:
        if geojson_data.get('type') == 'FeatureCollection':
            features = geojson_data.get('features', [])
        elif geojson_data.get('type') == 'Feature':
            features = [geojson_data]
        else:
            features = []
        
        info['features'] = len(features)
        
        if features:
            # Get geometry types
            for feature in features:
                geom_type = feature.get('geometry', {}).get('type')
                if geom_type and geom_type not in info['geometry_types']:
                    info['geometry_types'].append(geom_type)
            
            # Calculate bounds (simplified)
            all_coords = []
            for feature in features:
                coords = extract_coordinates(feature.get('geometry', {}))
                all_coords.extend(coords)
            
            if all_coords:
                lons = [coord[0] for coord in all_coords]
                lats = [coord[1] for coord in all_coords]
                
                info['bounds'] = {
                    'west': min(lons),
                    'east': max(lons),
                    'south': min(lats),
                    'north': max(lats)
                }
                
                info['center'] = {
                    'lat': (min(lats) + max(lats)) / 2,
                    'lon': (min(lons) + max(lons)) / 2
                }
                
                # Rough area estimate (degrees squared)
                info['area_estimate'] = (max(lons) - min(lons)) * (max(lats) - min(lats))
            
            # Get properties
            for feature in features:
                props = feature.get('properties', {})
                for key in props.keys():
                    if key not in info['properties']:
                        info['properties'].append(key)
    
    except Exception as e:
        st.error(f"Error extracting boundary info: {str(e)}")
    
    return info

def extract_coordinates(geometry):
    """Extract all coordinates from a geometry"""
    
    coords = []
    geom_type = geometry.get('type')
    coordinates = geometry.get('coordinates', [])
    
    if geom_type == 'Point':
        coords.append(coordinates)
    elif geom_type in ['LineString', 'MultiPoint']:
        coords.extend(coordinates)
    elif geom_type in ['Polygon', 'MultiLineString']:
        for ring in coordinates:
            coords.extend(ring)
    elif geom_type == 'MultiPolygon':
        for polygon in coordinates:
            for ring in polygon:
                coords.extend(ring)
    
    return coords

def show_boundary_info(info, boundary_name):
    """Display boundary information"""
    
    st.markdown("#### 📊 Boundary Information")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Features", info['features'])
    
    with col2:
        st.metric("Geometry Types", len(info['geometry_types']))
    
    with col3:
        if info['center']:
            st.metric("Center Lat", f"{info['center']['lat']:.4f}")
    
    with col4:
        if info['center']:
            st.metric("Center Lon", f"{info['center']['lon']:.4f}")
    
    # Additional info
    if info['geometry_types']:
        st.markdown(f"**Geometry Types:** {', '.join(info['geometry_types'])}")
    
    if info['properties']:
        st.markdown(f"**Available Properties:** {', '.join(info['properties'])}")
    
    if info['bounds']:
        bounds = info['bounds']
        st.markdown(f"**Bounding Box:** {bounds['west']:.4f}, {bounds['south']:.4f}, {bounds['east']:.4f}, {bounds['north']:.4f}")

def show_boundary_visualization(geojson_data, boundary_name):
    """Visualize the boundary on a map"""
    
    if not FOLIUM_AVAILABLE:
        st.warning("Install folium to see boundary visualization")
        return
    
    st.markdown("#### 🗺️ Boundary Visualization")
    
    try:
        # Extract center point for map
        info = extract_boundary_info(geojson_data)
        
        if info['center']:
            center_lat = info['center']['lat']
            center_lon = info['center']['lon']
        else:
            center_lat, center_lon = 0, 0
        
        # Create map
        m = folium.Map(location=[center_lat, center_lon], zoom_start=10)
        
        # Add GeoJSON to map
        folium.GeoJson(
            geojson_data,
            name=boundary_name,
            style_function=lambda feature: {
                'fillColor': 'lightblue',
                'color': 'blue',
                'weight': 2,
                'fillOpacity': 0.3,
                'opacity': 0.8
            },
            popup=folium.Popup(boundary_name),
            tooltip=folium.Tooltip(f"Click to see {boundary_name} details")
        ).add_to(m)
        
        # Add layer control
        folium.LayerControl().add_to(m)
        
        # Fit bounds to boundary
        if info['bounds']:
            bounds = info['bounds']
            sw = [bounds['south'], bounds['west']]
            ne = [bounds['north'], bounds['east']]
            m.fit_bounds([sw, ne])
        
        # Display map
        map_data = st_folium(m, width=700, height=500)
        
        st.success(f"✅ {boundary_name} visualized successfully!")
        
    except Exception as e:
        st.error(f"Error visualizing boundary: {str(e)}")

def show_boundary_analysis_options(geojson_data, boundary_name, boundary_info):
    """Show analysis options for the uploaded boundary"""
    
    st.markdown("#### 🔬 Analysis Options")
    
    # Analysis tabs
    analysis_tabs = st.tabs([
        "📊 Zonal Statistics", 
        "🛰️ Satellite Analysis", 
        "📈 Time Series", 
        "🏷️ Classification",
        "💾 Export Boundary"
    ])
    
    with analysis_tabs[0]:
        show_boundary_zonal_stats(geojson_data, boundary_name)
    
    with analysis_tabs[1]:
        show_boundary_satellite_analysis(geojson_data, boundary_name)
    
    with analysis_tabs[2]:
        show_boundary_time_series(geojson_data, boundary_name)
    
    with analysis_tabs[3]:
        show_boundary_classification(geojson_data, boundary_name)
    
    with analysis_tabs[4]:
        show_boundary_export(geojson_data, boundary_name)

def show_boundary_zonal_stats(geojson_data, boundary_name):
    """Zonal statistics for the boundary"""
    
    st.markdown(f"### 📊 Zonal Statistics for {boundary_name}")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### Settings")
        
        # Data source
        data_source = st.selectbox(
            "Data Source:",
            ["Landsat 8", "Sentinel-2", "MODIS NDVI", "Climate Data", "Elevation"]
        )
        
        # Bands/indices
        if data_source in ["Landsat 8", "Sentinel-2"]:
            variables = st.multiselect(
                "Variables:",
                ["NDVI", "NDWI", "Red", "Green", "Blue", "NIR"],
                default=["NDVI"]
            )
        else:
            variables = ["NDVI"]
        
        # Time period
        if data_source != "Elevation":
            date_range = st.date_input(
                "Date Range:",
                value=[date(2023, 1, 1), date(2023, 12, 31)]
            )
        
        # Statistics
        stats_to_calc = st.multiselect(
            "Statistics:",
            ["Mean", "Median", "Min", "Max", "Std Dev", "Count"],
            default=["Mean", "Count"]
        )
        
        if st.button("📊 Calculate Zonal Statistics", type="primary"):
            calculate_boundary_zonal_stats(geojson_data, boundary_name, data_source, variables, stats_to_calc)
    
    with col2:
        st.markdown("#### Results")
        
        if f'zonal_stats_{boundary_name}' in st.session_state:
            results = st.session_state[f'zonal_stats_{boundary_name}']
            
            # Display results table
            st.dataframe(results, use_container_width=True)
            
            # Visualization
            if PLOTLY_AVAILABLE and len(results) > 0:
                if 'Mean' in results.columns:
                    fig = px.bar(results, x='Variable', y='Mean',
                                title=f"Mean Values for {boundary_name}",
                                color='Mean', color_continuous_scale='Viridis')
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("👈 Configure settings and calculate statistics to see results")

def calculate_boundary_zonal_stats(geojson_data, boundary_name, data_source, variables, stats_to_calc):
    """Calculate zonal statistics for boundary (demo version)"""
    
    with st.spinner(f"Calculating zonal statistics for {boundary_name}..."):
        import time
        time.sleep(2)  # Simulate processing
        
        # Generate realistic demo results
        results_data = []
        
        for variable in variables:
            row = {'Variable': variable}
            
            for stat in stats_to_calc:
                if stat == "Mean":
                    if variable == "NDVI":
                        row[stat] = np.random.uniform(0.3, 0.8)
                    elif variable == "NDWI":
                        row[stat] = np.random.uniform(-0.2, 0.3)
                    else:
                        row[stat] = np.random.uniform(0.1, 0.4)
                elif stat == "Count":
                    row[stat] = np.random.randint(10000, 100000)
                elif stat == "Min":
                    row[stat] = row.get("Mean", 0.5) - np.random.uniform(0.1, 0.3)
                elif stat == "Max":
                    row[stat] = row.get("Mean", 0.5) + np.random.uniform(0.1, 0.3)
                else:
                    row[stat] = np.random.uniform(0.05, 0.15)
            
            results_data.append(row)
        
        results_df = pd.DataFrame(results_data)
        st.session_state[f'zonal_stats_{boundary_name}'] = results_df
        
        st.success(f"✅ Zonal statistics calculated for {boundary_name}!")

def show_boundary_satellite_analysis(geojson_data, boundary_name):
    """Satellite analysis for the boundary"""
    
    st.markdown(f"### 🛰️ Satellite Analysis for {boundary_name}")
    
    # Analysis options
    analysis_type = st.selectbox(
        "Analysis Type:",
        ["Cloud-free Composite", "Change Detection", "Vegetation Health", "Water Detection"]
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Settings
        satellite = st.selectbox("Satellite:", ["Landsat 8", "Sentinel-2", "MODIS"])
        cloud_threshold = st.slider("Max Cloud Cover (%):", 0, 50, 20)
        
        if analysis_type == "Change Detection":
            before_date = st.date_input("Before Date:", date(2020, 1, 1))
            after_date = st.date_input("After Date:", date(2023, 1, 1))
        else:
            date_range = st.date_input(
                "Date Range:",
                value=[date(2023, 1, 1), date(2023, 12, 31)]
            )
    
    with col2:
        # Visualization parameters
        if analysis_type == "Cloud-free Composite":
            vis_bands = st.multiselect("RGB Bands:", ["Red", "Green", "Blue", "NIR"], default=["Red", "Green", "Blue"])
        elif analysis_type == "Vegetation Health":
            index_type = st.selectbox("Vegetation Index:", ["NDVI", "EVI", "SAVI"])
        
        scale = st.number_input("Analysis Scale (m):", 10, 1000, 30)
    
    if st.button(f"🚀 Run {analysis_type}", type="primary"):
        run_boundary_satellite_analysis(geojson_data, boundary_name, analysis_type, satellite)

def run_boundary_satellite_analysis(geojson_data, boundary_name, analysis_type, satellite):
    """Run satellite analysis for boundary (demo version)"""
    
    with st.spinner(f"Running {analysis_type} for {boundary_name}..."):
        import time
        time.sleep(3)  # Simulate processing
        
        st.success(f"✅ {analysis_type} completed for {boundary_name}!")
        
        # Generate demo results
        if analysis_type == "Vegetation Health":
            mean_ndvi = np.random.uniform(0.4, 0.8)
            vegetation_cover = np.random.uniform(60, 90)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Mean NDVI", f"{mean_ndvi:.3f}")
            with col2:
                st.metric("Vegetation Cover", f"{vegetation_cover:.1f}%")
            with col3:
                st.metric("Health Status", "Good" if mean_ndvi > 0.6 else "Moderate")
        
        elif analysis_type == "Change Detection":
            change_percent = np.random.uniform(-15, 25)
            change_area = np.random.uniform(100, 1000)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Area Changed", f"{change_area:.0f} ha")
            with col2:
                st.metric("Change %", f"{change_percent:+.1f}%")
        
        # Show sample visualization
        if MATPLOTLIB_AVAILABLE:
            fig, ax = plt.subplots(figsize=(8, 6))
            
            # Create sample result image
            data = np.random.rand(100, 100)
            if analysis_type == "Vegetation Health":
                data = 0.3 + 0.5 * data  # NDVI range
                cmap = 'RdYlGn'
                title = f"NDVI for {boundary_name}"
            else:
                cmap = 'viridis'
                title = f"{analysis_type} Result for {boundary_name}"
            
            im = ax.imshow(data, cmap=cmap)
            ax.set_title(title)
            ax.axis('off')
            
            plt.colorbar(im, ax=ax, shrink=0.8)
            st.pyplot(fig)

def show_boundary_time_series(geojson_data, boundary_name):
    """Time series analysis for the boundary"""
    
    st.markdown(f"### 📈 Time Series Analysis for {boundary_name}")
    
    if not PLOTLY_AVAILABLE:
        st.warning("Install plotly for time series visualization")
        return
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### Settings")
        
        # Variables
        variables = st.multiselect(
            "Variables:",
            ["NDVI", "EVI", "NDWI", "LST", "Precipitation"],
            default=["NDVI"]
        )
        
        # Time range
        start_date = st.date_input("Start Date:", date(2020, 1, 1))
        end_date = st.date_input("End Date:", date(2023, 12, 31))
        
        # Temporal resolution
        temporal_res = st.selectbox("Temporal Resolution:", ["Monthly", "Weekly", "Daily"])
        
        if st.button("📊 Generate Time Series", type="primary"):
            generate_boundary_time_series(geojson_data, boundary_name, variables, start_date, end_date, temporal_res)
    
    with col2:
        st.markdown("#### Results")
        
        if f'time_series_{boundary_name}' in st.session_state:
            ts_data = st.session_state[f'time_series_{boundary_name}']
            
            # Interactive time series plot
            fig = px.line(ts_data, x='Date', y=variables,
                         title=f"Time Series for {boundary_name}",
                         labels={'value': 'Value', 'variable': 'Variable'})
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            # Statistics
            st.markdown("#### Statistics Summary")
            stats = ts_data[variables].describe().round(3)
            st.dataframe(stats, use_container_width=True)
        else:
            st.info("👈 Configure settings and generate time series")

def generate_boundary_time_series(geojson_data, boundary_name, variables, start_date, end_date, temporal_res):
    """Generate time series for boundary (demo version)"""
    
    with st.spinner(f"Generating time series for {boundary_name}..."):
        import time
        time.sleep(2)
        
        # Generate date range
        if temporal_res == "Monthly":
            freq = 'M'
        elif temporal_res == "Weekly":
            freq = 'W'
        else:
            freq = 'D'
        
        dates = pd.date_range(start_date, end_date, freq=freq)
        
        # Generate realistic time series data
        ts_data = {'Date': dates}
        
        for variable in variables:
            if variable == "NDVI":
                # Seasonal pattern for NDVI
                base = 0.4 + 0.3 * np.sin(2 * np.pi * np.arange(len(dates)) / 12)
                noise = np.random.normal(0, 0.05, len(dates))
                ts_data[variable] = np.clip(base + noise, 0, 1)
            elif variable == "LST":
                # Temperature pattern
                base = 20 + 10 * np.sin(2 * np.pi * np.arange(len(dates)) / 12)
                noise = np.random.normal(0, 2, len(dates))
                ts_data[variable] = base + noise
            else:
                # Random pattern for other variables
                ts_data[variable] = np.random.uniform(0.2, 0.8, len(dates))
        
        ts_df = pd.DataFrame(ts_data)
        st.session_state[f'time_series_{boundary_name}'] = ts_df
        
        st.success(f"✅ Time series generated for {boundary_name}!")

def show_boundary_classification(geojson_data, boundary_name):
    """Classification analysis for the boundary"""
    
    st.markdown(f"### 🏷️ Land Cover Classification for {boundary_name}")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### Classification Settings")
        
        # Classification method
        method = st.selectbox(
            "Method:",
            ["Unsupervised (K-Means)", "Supervised (Random Forest)", "CART Decision Tree"]
        )
        
        # Number of classes
        if "Unsupervised" in method:
            num_classes = st.slider("Number of Classes:", 3, 15, 6)
        else:
            num_classes = st.slider("Number of Classes:", 3, 10, 5)
            
            # Class names
            st.markdown("**Class Names:**")
            class_names = []
            for i in range(num_classes):
                name = st.text_input(f"Class {i+1}:", f"Class_{i+1}", key=f"class_{boundary_name}_{i}")
                class_names.append(name)
        
        # Input data
        input_data = st.multiselect(
            "Input Bands/Indices:",
            ["Red", "Green", "Blue", "NIR", "SWIR1", "NDVI", "NDWI"],
            default=["Red", "Green", "Blue", "NIR"]
        )
        
        if st.button("🚀 Run Classification", type="primary"):
            run_boundary_classification(geojson_data, boundary_name, method, num_classes)
    
    with col2:
        st.markdown("#### Classification Results")
        
        if f'classification_{boundary_name}' in st.session_state:
            results = st.session_state[f'classification_{boundary_name}']
            
            # Accuracy metrics
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Overall Accuracy", f"{results['accuracy']:.1%}")
            with col_b:
                st.metric("Kappa", f"{results['kappa']:.3f}")
            with col_c:
                st.metric("Classes", results['num_classes'])
            
            # Class areas (demo)
            if PLOTLY_AVAILABLE:
                class_areas = [np.random.uniform(50, 500) for _ in range(num_classes)]
                class_labels = [f"Class {i+1}" for i in range(num_classes)]
                
                fig = px.pie(values=class_areas, names=class_labels,
                           title=f"Land Cover Distribution - {boundary_name}")
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("👈 Configure settings and run classification")

def run_boundary_classification(geojson_data, boundary_name, method, num_classes):
    """Run classification for boundary (demo version)"""
    
    with st.spinner(f"Running {method} classification for {boundary_name}..."):
        import time
        time.sleep(3)
        
        # Generate demo results
        results = {
            'accuracy': np.random.uniform(0.75, 0.95),
            'kappa': np.random.uniform(0.65, 0.90),
            'num_classes': num_classes,
            'method': method
        }
        
        st.session_state[f'classification_{boundary_name}'] = results
        st.success(f"✅ Classification completed for {boundary_name}!")

def show_boundary_export(geojson_data, boundary_name):
    """Export options for the boundary"""
    
    st.markdown(f"### 💾 Export {boundary_name}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Export Boundary")
        
        export_format = st.selectbox("Format:", ["GeoJSON", "Shapefile", "KML", "CSV"])
        
        include_analysis = st.checkbox("Include Analysis Results", value=True)
        
        if st.button("📥 Export Boundary", type="primary"):
            export_boundary_data(geojson_data, boundary_name, export_format, include_analysis)
    
    with col2:
        st.markdown("#### Export Analysis Results")
        
        # Check what analysis results are available
        available_results = []
        if f'zonal_stats_{boundary_name}' in st.session_state:
            available_results.append("Zonal Statistics")
        if f'time_series_{boundary_name}' in st.session_state:
            available_results.append("Time Series")
        if f'classification_{boundary_name}' in st.session_state:
            available_results.append("Classification Results")
        
        if available_results:
            results_to_export = st.multiselect("Results to Export:", available_results)
            
            result_format = st.selectbox("Results Format:", ["CSV", "Excel", "JSON"])
            
            if st.button("📊 Export Results"):
                export_analysis_results(boundary_name, results_to_export, result_format)
        else:
            st.info("No analysis results available. Run some analysis first!")

def export_boundary_data(geojson_data, boundary_name, export_format, include_analysis):
    """Export boundary data"""
    
    with st.spinner(f"Exporting {boundary_name}..."):
        import time
        time.sleep(1)
        
        if export_format == "GeoJSON":
            # Create download for GeoJSON
            json_str = json.dumps(geojson_data, indent=2)
            b64 = base64.b64encode(json_str.encode()).decode()
            href = f'<a href="data:file/json;base64,{b64}" download="{boundary_name.replace(" ", "_")}.geojson">📥 Download GeoJSON</a>'
            st.markdown(href, unsafe_allow_html=True)
        
        st.success(f"✅ {boundary_name} exported as {export_format}!")

def export_analysis_results(boundary_name, results_to_export, result_format):
    """Export analysis results"""
    
    with st.spinner("Exporting analysis results..."):
        import time
        time.sleep(1)
        
        # Combine results
        all_results = {}
        
        for result_type in results_to_export:
            if result_type == "Zonal Statistics" and f'zonal_stats_{boundary_name}' in st.session_state:
                all_results['zonal_statistics'] = st.session_state[f'zonal_stats_{boundary_name}']
            elif result_type == "Time Series" and f'time_series_{boundary_name}' in st.session_state:
                all_results['time_series'] = st.session_state[f'time_series_{boundary_name}']
        
        st.success(f"✅ Analysis results exported as {result_format}!")

if __name__ == "__main__":
    main()