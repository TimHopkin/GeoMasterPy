"""
GeoMasterPy Streamlit Web Application

An interactive web interface for GeoMasterPy - making Google Earth Engine
accessible through a user-friendly web application.
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
from datetime import datetime, date
import base64
from io import BytesIO

# Import with error handling
try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    st.error("Matplotlib not available")

try:
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError as e:
    PLOTLY_AVAILABLE = False
    st.error(f"Plotly not available: {e}")

try:
    import folium
    from streamlit_folium import st_folium
    FOLIUM_AVAILABLE = True
except ImportError:
    FOLIUM_AVAILABLE = False
    st.error("Folium not available")

# Import GeoMasterPy components (with fallbacks for demo mode)
try:
    import geomasterpy as gmp
    GEOMASTERPY_AVAILABLE = True
except ImportError as e:
    GEOMASTERPY_AVAILABLE = False
    print(f"GeoMasterPy not available: {e}")

try:
    import ee
    EE_AVAILABLE = True
except ImportError as e:
    EE_AVAILABLE = False
    print(f"Earth Engine not available: {e}")

# Handle optional heavy dependencies gracefully
try:
    import cartopy
    CARTOPY_AVAILABLE = True
except ImportError:
    CARTOPY_AVAILABLE = False

try:
    import ipyleaflet
    IPYLEAFLET_AVAILABLE = True
except ImportError:
    IPYLEAFLET_AVAILABLE = False

# Configure Streamlit page
st.set_page_config(
    page_title="GeoMasterPy - Interactive Earth Engine Tool",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
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
</style>
""", unsafe_allow_html=True)

def main():
    """Main Streamlit application"""
    
    # Header
    st.markdown('<h1 class="main-header">🌍 GeoMasterPy Interactive</h1>', unsafe_allow_html=True)
    st.markdown("**Interactive Geospatial Analysis with Google Earth Engine**")
    
    # Check system status
    with st.expander("🔧 System Status", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if PLOTLY_AVAILABLE:
                st.success("✅ Plotly")
            else:
                st.error("❌ Plotly Missing")
        
        with col2:
            if FOLIUM_AVAILABLE:
                st.success("✅ Folium")
            else:
                st.error("❌ Folium Missing")
        
        with col3:
            if MATPLOTLIB_AVAILABLE:
                st.success("✅ Matplotlib")
            else:
                st.error("❌ Matplotlib Missing")
        
        with col4:
            if GEOMASTERPY_AVAILABLE:
                st.success("✅ GeoMasterPy")
            else:
                st.warning("⚠️ Demo Mode")
        
        # Second row for additional status
        col5, col6, col7, col8 = st.columns(4)
        
        with col5:
            if EE_AVAILABLE:
                try:
                    ee.Initialize()
                    st.success("✅ Earth Engine")
                    ee_status = True
                except:
                    st.warning("⚠️ EE Auth Needed")
                    ee_status = False
            else:
                st.info("ℹ️ EE Optional")
                ee_status = False
        
        with col6:
            st.success("✅ Streamlit")
        
        with col7:
            st.success("✅ Pandas")
        
        with col8:
            st.success("✅ NumPy")
    
    # Sidebar navigation
    st.sidebar.title("🧭 Navigation")
    page = st.sidebar.selectbox(
        "Choose a feature:",
        [
            "🏠 Home",
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

def show_home():
    """Home page with overview and quick start"""
    
    st.markdown("## Welcome to GeoMasterPy! 🚀")
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-container">
            <h3>🗺️</h3>
            <p><strong>Interactive Maps</strong></p>
            <p>Create dynamic maps with Earth Engine</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-container">
            <h3>📊</h3>
            <p><strong>Data Analysis</strong></p>
            <p>Powerful geospatial analytics</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-container">
            <h3>🎨</h3>
            <p><strong>Visualizations</strong></p>
            <p>Beautiful charts and maps</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-container">
            <h3>💾</h3>
            <p><strong>Export Tools</strong></p>
            <p>Save your results anywhere</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Features overview
    st.markdown("## 🌟 Key Features")
    
    features = [
        ("🗺️ Interactive Mapping", "Create dynamic maps with Google Earth Engine integration"),
        ("🔍 Data Catalog Search", "Discover and explore Earth Engine datasets"),
        ("🔄 JavaScript Converter", "Convert GEE JavaScript code to Python"),
        ("📊 Geospatial Analysis", "Perform statistical analysis and classification"),
        ("📈 Advanced Visualizations", "Create charts, legends, and animations"),
        ("💾 Data Export", "Export images and data to multiple formats"),
        ("🖼️ Publication Maps", "Generate high-quality static maps"),
        ("📚 Comprehensive Docs", "Complete documentation and examples")
    ]
    
    for title, description in features:
        st.markdown(f"""
        <div class="feature-box">
            <h4>{title}</h4>
            <p>{description}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick start
    st.markdown("## 🚀 Quick Start")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### For Beginners")
        st.markdown("""
        1. 🔍 Start with **Data Catalog** to explore datasets
        2. 🔄 Try the **JS Converter** to migrate existing code
        3. 🗺️ Create your first **Interactive Map**
        4. 📊 Explore **Data Analysis** tools
        """)
    
    with col2:
        st.markdown("### For Advanced Users")
        st.markdown("""
        1. 📊 Jump to **Data Analysis** for complex workflows
        2. 🖼️ Create **Publication Maps** for research
        3. 💾 Use **Export Tools** for data management
        4. 📚 Check **Documentation** for API details
        """)

def show_interactive_maps():
    """Interactive mapping interface"""
    
    st.markdown("## 🗺️ Interactive Maps")
    
    # Map configuration
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Map Settings")
        
        # Location selector
        location = st.selectbox(
            "Choose a location:",
            [
                "San Francisco, CA",
                "New York, NY", 
                "Yellowstone National Park",
                "Amazon Rainforest",
                "Custom Location"
            ]
        )
        
        # Location coordinates
        locations = {
            "San Francisco, CA": (37.7749, -122.4194),
            "New York, NY": (40.7128, -74.0060),
            "Yellowstone National Park": (44.4280, -110.5885),
            "Amazon Rainforest": (-3.4653, -62.2159),
        }
        
        if location == "Custom Location":
            lat = st.number_input("Latitude", value=37.7749, format="%.4f")
            lon = st.number_input("Longitude", value=-122.4194, format="%.4f")
        else:
            lat, lon = locations[location]
        
        zoom = st.slider("Zoom Level", 1, 18, 10)
        
        # Basemap selection
        basemap = st.selectbox(
            "Basemap:",
            [
                "OpenStreetMap",
                "CartoDB Positron",
                "CartoDB Dark Matter", 
                "Stamen Terrain",
                "Stamen Toner"
            ]
        )
    
    with col2:
        st.markdown("### Interactive Map")
        
        # Create folium map
        if basemap == "OpenStreetMap":
            tiles = "OpenStreetMap"
        elif basemap == "CartoDB Positron":
            tiles = "CartoDB positron"
        elif basemap == "CartoDB Dark Matter":
            tiles = "CartoDB dark_matter"
        elif basemap == "Stamen Terrain":
            tiles = "Stamen Terrain"
        else:
            tiles = "Stamen Toner"
        
        m = folium.Map(
            location=[lat, lon],
            zoom_start=zoom,
            tiles=tiles
        )
        
        # Add marker
        folium.Marker(
            [lat, lon],
            popup=f"📍 {location}",
            tooltip="Click for info"
        ).add_to(m)
        
        # Display map
        map_data = st_folium(m, width=700, height=500)
    
    # Earth Engine data options (demo mode)
    st.markdown("### 🛰️ Satellite Data Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🛰️ Add Landsat 8"):
            st.info("Landsat 8 data would be loaded here with Earth Engine authentication")
    
    with col2:
        if st.button("🛰️ Add Sentinel-2"):
            st.info("Sentinel-2 data would be loaded here with Earth Engine authentication")
    
    with col3:
        if st.button("📊 Calculate NDVI"):
            st.info("NDVI calculation would be performed here with Earth Engine authentication")
    
    # Code example
    with st.expander("💻 Code Example"):
        st.code("""
import geomasterpy as gmp
import ee

# Initialize Earth Engine
ee.Initialize()

# Create interactive map
Map = gmp.Map(center=({lat}, {lon}), zoom={zoom})

# Add basemap
Map.add_basemap('{basemap}')

# Load satellite data
landsat = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2') \\
    .filterBounds(ee.Geometry.Point({lon}, {lat})) \\
    .filterDate('2023-01-01', '2023-12-31') \\
    .filter(ee.Filter.lt('CLOUD_COVER', 20)) \\
    .median()

# Add to map
vis_params = {{
    'bands': ['SR_B4', 'SR_B3', 'SR_B2'],
    'min': 0.0,
    'max': 0.3,
    'gamma': 1.4
}}

Map.add_ee_layer(landsat, vis_params, 'Landsat 8')

# Display map
Map
        """.format(lat=lat, lon=lon, zoom=zoom, basemap=basemap))

def show_data_catalog():
    """Data catalog and search interface"""
    
    st.markdown("## 🔍 Earth Engine Data Catalog")
    
    # Search interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_term = st.text_input(
            "🔍 Search for datasets:",
            value="landsat",
            help="Enter keywords like 'landsat', 'sentinel', 'modis', 'climate', etc."
        )
    
    with col2:
        max_results = st.number_input("Max results:", 1, 50, 10)
    
    if st.button("🔍 Search Datasets"):
        if GEOMASTERPY_AVAILABLE:
            with st.spinner("Searching Earth Engine catalog..."):
                try:
                    results = gmp.search_ee_data(search_term, max_results)
                    
                    if results:
                        st.success(f"Found {len(results)} datasets matching '{search_term}'")
                        
                        # Display results in a nice format
                        for i, result in enumerate(results, 1):
                            with st.expander(f"📊 {i}. {result['title']}"):
                                col1, col2 = st.columns([2, 1])
                                
                                with col1:
                                    st.markdown(f"**Dataset ID:** `{result['id']}`")
                                    st.markdown(f"**Description:** {result['description']}")
                                    st.markdown(f"**Provider:** {result['provider']}")
                                    
                                    # Tags
                                    if 'tags' in result:
                                        tags_html = " ".join([f'<span style="background-color: #e1f5fe; padding: 2px 8px; border-radius: 12px; font-size: 0.8em;">{tag}</span>' for tag in result['tags']])
                                        st.markdown(f"**Tags:** {tags_html}", unsafe_allow_html=True)
                                
                                with col2:
                                    st.code(f"ee.ImageCollection('{result['id']}')")
                                    if st.button(f"📋 Copy ID", key=f"copy_{i}"):
                                        st.info(f"Copy this: {result['id']}")
                    else:
                        st.warning(f"No datasets found for '{search_term}'. Try terms like 'landsat', 'sentinel', 'modis'.")
                        
                except Exception as e:
                    st.error(f"Error searching catalog: {str(e)}")
        else:
            # Demo mode - show sample results
            st.info("Demo mode: Showing sample search results")
            
            sample_results = [
                {
                    'id': 'LANDSAT/LC08/C02/T1_L2',
                    'title': 'Landsat 8 Collection 2 Tier 1 Level-2',
                    'description': 'Atmospherically corrected surface reflectance',
                    'provider': 'USGS',
                    'tags': ['landsat', 'surface reflectance', 'optical']
                },
                {
                    'id': 'COPERNICUS/S2_SR_HARMONIZED',
                    'title': 'Sentinel-2 MSI: MultiSpectral Instrument, Level-2A',
                    'description': 'Bottom-of-atmosphere reflectance',
                    'provider': 'European Space Agency',
                    'tags': ['sentinel', 'surface reflectance', 'optical']
                }
            ]
            
            for i, result in enumerate(sample_results, 1):
                with st.expander(f"📊 {i}. {result['title']}"):
                    st.markdown(f"**Dataset ID:** `{result['id']}`")
                    st.markdown(f"**Description:** {result['description']}")
                    st.markdown(f"**Provider:** {result['provider']}")
    
    # Popular datasets
    st.markdown("## 🌟 Popular Datasets")
    
    popular_datasets = {
        "🛰️ Optical Imagery": [
            ("Landsat 8 Level-2", "LANDSAT/LC08/C02/T1_L2"),
            ("Sentinel-2 Level-2A", "COPERNICUS/S2_SR_HARMONIZED"),
            ("MODIS Terra Surface Reflectance", "MODIS/061/MOD09A1")
        ],
        "🌡️ Climate Data": [
            ("ERA5-Land Hourly", "ECMWF/ERA5_LAND/HOURLY"),
            ("CHIRPS Daily Precipitation", "UCSB-CHG/CHIRPS/DAILY"),
            ("MODIS Land Surface Temperature", "MODIS/061/MOD11A1")
        ],
        "🏔️ Elevation & Terrain": [
            ("NASA SRTM DEM", "USGS/SRTMGL1_003"),
            ("NASA DEM", "NASA/NASADEM_HGT/001"),
            ("ALOS World 3D", "JAXA/ALOS/AW3D30/V3_2")
        ]
    }
    
    for category, datasets in popular_datasets.items():
        with st.expander(category):
            for name, dataset_id in datasets:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{name}**")
                    st.code(dataset_id)
                with col2:
                    if st.button("📋", key=f"copy_{dataset_id}"):
                        st.info("Copied!")

def show_js_converter():
    """JavaScript to Python converter"""
    
    st.markdown("## 🔄 JavaScript to Python Converter")
    st.markdown("Convert your Google Earth Engine JavaScript code to Python instantly!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📝 JavaScript Code")
        
        # Sample JavaScript code
        sample_js = """// Load a Landsat 8 image
var image = ee.Image('LANDSAT/LC08/C02/T1_L2/LC08_044034_20140318');

// Calculate NDVI
var ndvi = image.normalizedDifference(['SR_B5', 'SR_B4']);

// Add to map
Map.addLayer(ndvi, {
  min: -1,
  max: 1,
  palette: ['blue', 'white', 'green']
}, 'NDVI');

// Print image info
print('Image info:', image);
Map.centerObject(image, 9);"""
        
        js_code = st.text_area(
            "Paste your JavaScript code here:",
            value=sample_js,
            height=400,
            help="Enter Google Earth Engine JavaScript code"
        )
    
    with col2:
        st.markdown("### 🐍 Python Code")
        
        if st.button("🔄 Convert to Python"):
            if GEOMASTERPY_AVAILABLE:
                try:
                    python_code = gmp.js_snippet_to_python(js_code)
                    st.code(python_code, language='python')
                    
                    # Download button
                    b64 = base64.b64encode(python_code.encode()).decode()
                    href = f'<a href="data:file/txt;base64,{b64}" download="converted_code.py">💾 Download Python Code</a>'
                    st.markdown(href, unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"Conversion error: {str(e)}")
            else:
                # Demo conversion
                demo_python = """import ee
ee.Initialize()

# Load a Landsat 8 image
image = ee.Image('LANDSAT/LC08/C02/T1_L2/LC08_044034_20140318')

# Calculate NDVI
ndvi = image.normalizedDifference(['SR_B5', 'SR_B4'])

# Add to map
Map.add_ee_layer(ndvi, {
    'min': -1,
    'max': 1,
    'palette': ['blue', 'white', 'green']
}, 'NDVI')

# Print image info
print('Image info:', image)
Map.center_object(image, 9)"""
                st.code(demo_python, language='python')
        else:
            st.info("👆 Click 'Convert to Python' to see the converted code")
    
    # Conversion tips
    st.markdown("## 💡 Conversion Tips")
    
    tips = [
        ("Variables", "`var x = ...` → `x = ...`"),
        ("Print statements", "`print(...)` → `print(...)`"),
        ("Map methods", "`Map.addLayer(...)` → `Map.add_ee_layer(...)`"),
        ("Boolean values", "`true/false` → `True/False`"),
        ("Comments", "`// comment` → `# comment`"),
        ("Earth Engine", "`ee.Image(...)` → `ee.Image(...)`")
    ]
    
    col1, col2 = st.columns(2)
    for i, (concept, conversion) in enumerate(tips):
        with col1 if i % 2 == 0 else col2:
            st.markdown(f"**{concept}:** `{conversion}`")

def show_data_analysis():
    """Data analysis and statistics interface"""
    
    st.markdown("## 📊 Geospatial Data Analysis")
    
    # Analysis type selector
    analysis_type = st.selectbox(
        "Choose analysis type:",
        [
            "📈 Image Statistics",
            "🎯 Zonal Statistics", 
            "🔢 Spectral Indices",
            "🏷️ Image Classification",
            "🔍 Change Detection"
        ]
    )
    
    if analysis_type == "📈 Image Statistics":
        show_image_statistics()
    elif analysis_type == "🎯 Zonal Statistics":
        show_zonal_statistics()
    elif analysis_type == "🔢 Spectral Indices":
        show_spectral_indices()
    elif analysis_type == "🏷️ Image Classification":
        show_classification()
    elif analysis_type == "🔍 Change Detection":
        show_change_detection()

def show_image_statistics():
    """Image statistics interface"""
    
    st.markdown("### 📈 Image Statistics")
    st.markdown("Calculate comprehensive statistics for satellite imagery")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### Settings")
        
        dataset = st.selectbox(
            "Dataset:",
            ["Landsat 8", "Sentinel-2", "MODIS"]
        )
        
        bands = st.multiselect(
            "Bands to analyze:",
            ["Blue", "Green", "Red", "NIR", "SWIR1", "SWIR2"],
            default=["Red", "NIR"]
        )
        
        scale = st.number_input("Analysis scale (meters):", 10, 1000, 30)
        
        if st.button("📊 Calculate Statistics"):
            # Demo statistics
            demo_stats = pd.DataFrame({
                'Band': bands,
                'Mean': np.random.uniform(0.1, 0.3, len(bands)),
                'Std': np.random.uniform(0.05, 0.15, len(bands)),
                'Min': np.random.uniform(0.0, 0.1, len(bands)),
                'Max': np.random.uniform(0.4, 0.8, len(bands)),
                'Median': np.random.uniform(0.15, 0.25, len(bands))
            })
            
            st.session_state['stats'] = demo_stats
    
    with col2:
        st.markdown("#### Results")
        
        if 'stats' in st.session_state:
            df = st.session_state['stats']
            st.dataframe(df, use_container_width=True)
            
            # Visualization
            if PLOTLY_AVAILABLE:
                fig = px.bar(df, x='Band', y=['Mean', 'Median'], 
                            title="Band Statistics Comparison",
                            barmode='group')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("⚠️ Plotly not available - visualization disabled")
        else:
            st.info("👈 Configure settings and click 'Calculate Statistics'")

def show_spectral_indices():
    """Spectral indices calculation interface"""
    
    st.markdown("### 🔢 Spectral Indices")
    st.markdown("Calculate vegetation, water, and urban indices")
    
    # Index selector
    indices = st.multiselect(
        "Select indices to calculate:",
        ["NDVI", "NDWI", "NDBI", "EVI", "SAVI", "MNDWI"],
        default=["NDVI", "NDWI"]
    )
    
    if indices:
        # Create sample time series data
        dates = pd.date_range('2023-01-01', '2023-12-31', freq='M')
        
        # Generate demo data for each index
        data = {}
        for index in indices:
            if index == "NDVI":
                # Seasonal vegetation pattern
                base = 0.4 + 0.3 * np.sin(2 * np.pi * np.arange(len(dates)) / 12)
                noise = np.random.normal(0, 0.05, len(dates))
                data[index] = base + noise
            elif index == "NDWI":
                # Water index - inverse seasonal pattern
                base = 0.2 - 0.15 * np.sin(2 * np.pi * np.arange(len(dates)) / 12)
                noise = np.random.normal(0, 0.03, len(dates))
                data[index] = base + noise
            else:
                # Random pattern for other indices
                data[index] = np.random.uniform(-0.2, 0.6, len(dates))
        
        df = pd.DataFrame(data, index=dates)
        
        # Display time series
        fig = px.line(df, title="Spectral Indices Time Series", 
                     labels={'index': 'Date', 'value': 'Index Value'})
        st.plotly_chart(fig, use_container_width=True)
        
        # Statistics table
        st.markdown("#### Index Statistics")
        stats_df = df.describe()
        st.dataframe(stats_df, use_container_width=True)
        
        # Index information
        with st.expander("ℹ️ Index Information"):
            index_info = {
                "NDVI": "Normalized Difference Vegetation Index - measures vegetation health",
                "NDWI": "Normalized Difference Water Index - detects water bodies",
                "NDBI": "Normalized Difference Built-up Index - identifies urban areas",
                "EVI": "Enhanced Vegetation Index - improved vegetation measure",
                "SAVI": "Soil Adjusted Vegetation Index - accounts for soil background",
                "MNDWI": "Modified NDWI - better water detection in urban areas"
            }
            
            for idx in indices:
                if idx in index_info:
                    st.markdown(f"**{idx}:** {index_info[idx]}")

def show_visualizations():
    """Advanced visualizations interface"""
    
    st.markdown("## 📈 Advanced Visualizations")
    
    viz_type = st.selectbox(
        "Choose visualization type:",
        [
            "📊 Time Series Charts",
            "📈 Histograms", 
            "🗺️ Interactive Plots",
            "🎬 Animations",
            "📋 Legends & Colorbars"
        ]
    )
    
    if viz_type == "📊 Time Series Charts":
        show_time_series_viz()
    elif viz_type == "📈 Histograms":
        show_histogram_viz()
    elif viz_type == "🗺️ Interactive Plots":
        show_interactive_plots()
    elif viz_type == "🎬 Animations":
        show_animations()
    elif viz_type == "📋 Legends & Colorbars":
        show_legends_colorbars()

def show_time_series_viz():
    """Time series visualization"""
    
    st.markdown("### 📊 Time Series Visualization")
    
    # Generate sample time series data
    dates = pd.date_range('2020-01-01', '2023-12-31', freq='M')
    
    # NDVI time series with seasonal pattern
    ndvi = 0.4 + 0.3 * np.sin(2 * np.pi * np.arange(len(dates)) / 12) + np.random.normal(0, 0.05, len(dates))
    
    # Temperature data
    temp = 15 + 10 * np.sin(2 * np.pi * np.arange(len(dates)) / 12) + np.random.normal(0, 2, len(dates))
    
    # Precipitation data
    precip = 50 + 30 * np.sin(2 * np.pi * (np.arange(len(dates)) + 3) / 12) + np.random.normal(0, 10, len(dates))
    
    df = pd.DataFrame({
        'NDVI': ndvi,
        'Temperature': temp,
        'Precipitation': precip
    }, index=dates)
    
    # Create subplot
    fig = make_subplots(
        rows=3, cols=1,
        subplot_titles=['NDVI', 'Temperature (°C)', 'Precipitation (mm)'],
        vertical_spacing=0.1
    )
    
    # Add traces
    fig.add_trace(go.Scatter(x=df.index, y=df['NDVI'], name='NDVI', line=dict(color='green')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['Temperature'], name='Temperature', line=dict(color='red')), row=2, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['Precipitation'], name='Precipitation', line=dict(color='blue')), row=3, col=1)
    
    fig.update_layout(height=600, title_text="Environmental Time Series")
    fig.update_xaxes(title_text="Date", row=3, col=1)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Avg NDVI", f"{df['NDVI'].mean():.3f}", f"{df['NDVI'].std():.3f}")
    
    with col2:
        st.metric("Avg Temperature", f"{df['Temperature'].mean():.1f}°C", f"{df['Temperature'].std():.1f}")
    
    with col3:
        st.metric("Avg Precipitation", f"{df['Precipitation'].mean():.1f}mm", f"{df['Precipitation'].std():.1f}")

def show_publication_maps():
    """Publication quality maps interface"""
    
    st.markdown("## 🖼️ Publication Quality Maps")
    st.markdown("Create high-resolution maps for scientific publications")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Map Settings")
        
        map_title = st.text_input("Map Title:", "Study Area - NDVI Analysis")
        
        projection = st.selectbox(
            "Projection:",
            ["PlateCarree", "Mercator", "Robinson", "Mollweide"]
        )
        
        resolution = st.selectbox(
            "Resolution (DPI):",
            [150, 300, 600]
        )
        
        format_type = st.selectbox(
            "Output Format:",
            ["PNG", "PDF", "SVG"]
        )
        
        include_features = st.multiselect(
            "Map Features:",
            ["Coastlines", "Borders", "Gridlines", "Scale Bar", "North Arrow"],
            default=["Coastlines", "Borders", "Gridlines"]
        )
        
        colormap = st.selectbox(
            "Color Scheme:",
            ["RdYlGn", "viridis", "plasma", "coolwarm", "terrain"]
        )
    
    with col2:
        st.markdown("### Map Preview")
        
        # Create sample publication map
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Generate sample spatial data
        x = np.linspace(-125, -65, 100)
        y = np.linspace(20, 50, 80)
        X, Y = np.meshgrid(x, y)
        Z = np.sin((X + 95) / 10) * np.cos((Y - 35) / 8) * 0.5 + 0.3
        
        # Create the map
        im = ax.contourf(X, Y, Z, levels=20, cmap=colormap, vmin=-1, vmax=1)
        
        # Customize based on settings
        if "Gridlines" in include_features:
            ax.grid(True, alpha=0.3)
        
        ax.set_xlabel('Longitude (°)')
        ax.set_ylabel('Latitude (°)')
        ax.set_title(map_title, fontsize=14, fontweight='bold', pad=20)
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, shrink=0.8)
        cbar.set_label('NDVI')
        
        # Style improvements
        ax.set_aspect('equal')
        plt.tight_layout()
        
        st.pyplot(fig)
        
        # Generate download
        if st.button("📥 Generate High-Resolution Map"):
            # In a real implementation, this would create the actual map
            st.success(f"Map generated at {resolution} DPI in {format_type} format!")
            st.info("📁 Map saved to downloads folder")
    
    # Code example
    with st.expander("💻 Code Example"):
        st.code(f"""
import geomasterpy as gmp
import ee

# Load Earth Engine data
image = ee.Image('your_image_id')
region = ee.Geometry.Rectangle([-125, 20, -65, 50])

# Create publication map
fig = gmp.plot_ee_image_cartopy(
    image=image,
    vis_params={{'min': -1, 'max': 1, 'palette': ['{colormap}']}},
    region=region,
    figsize=(12, 8),
    title='{map_title}',
    projection='{projection}',
    add_colorbar=True,
    add_gridlines={'Gridlines' in include_features}
)

# Save high-resolution map
gmp.plotting.save_publication_map(
    fig, 
    'publication_map.{format_type.lower()}', 
    dpi={resolution}, 
    format='{format_type.lower()}'
)
        """)

def show_export_tools():
    """Data export interface"""
    
    st.markdown("## 💾 Export Tools")
    st.markdown("Export your analysis results and data")
    
    export_type = st.selectbox(
        "Export Type:",
        [
            "🖼️ Export Images",
            "📊 Export Vector Data", 
            "📈 Export Statistics",
            "⏱️ Export Time Series",
            "☁️ Export to Google Drive"
        ]
    )
    
    if export_type == "🖼️ Export Images":
        show_image_export()
    elif export_type == "📊 Export Vector Data":
        show_vector_export()
    elif export_type == "📈 Export Statistics":
        show_stats_export()
    elif export_type == "⏱️ Export Time Series":
        show_timeseries_export()
    elif export_type == "☁️ Export to Google Drive":
        show_drive_export()

def show_image_export():
    """Image export interface"""
    
    st.markdown("### 🖼️ Image Export")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Export Settings")
        
        file_format = st.selectbox("Format:", ["GeoTIFF", "PNG", "JPEG"])
        scale = st.number_input("Scale (meters):", 10, 1000, 30)
        compression = st.selectbox("Compression:", ["LZW", "DEFLATE", "None"])
        
        # Demo export
        if st.button("📥 Export Image"):
            st.success("✅ Image export started!")
            st.info("📁 File will be saved to your downloads folder")
            
            # Show export code
            st.code(f"""
# Export with GeoMasterPy
gmp.export_image_to_local(
    image=your_image,
    filename='exported_image',
    region=your_region,
    scale={scale},
    file_format='{file_format}'
)
            """)
    
    with col2:
        st.markdown("#### Export Preview")
        
        # Create a sample export preview
        fig, ax = plt.subplots(figsize=(6, 4))
        
        # Generate sample data
        data = np.random.rand(50, 50)
        im = ax.imshow(data, cmap='RdYlGn')
        ax.set_title('Export Preview')
        ax.set_xlabel('X (pixels)')
        ax.set_ylabel('Y (pixels)')
        
        plt.colorbar(im, ax=ax, label='Values')
        st.pyplot(fig)

def show_documentation():
    """Documentation and help"""
    
    st.markdown("## 📚 Documentation & Help")
    
    doc_section = st.selectbox(
        "Documentation Section:",
        [
            "🚀 Getting Started",
            "📖 API Reference",
            "💡 Examples & Tutorials", 
            "❓ FAQ",
            "🔧 Troubleshooting"
        ]
    )
    
    if doc_section == "🚀 Getting Started":
        show_getting_started()
    elif doc_section == "📖 API Reference":
        show_api_reference()
    elif doc_section == "💡 Examples & Tutorials":
        show_examples()
    elif doc_section == "❓ FAQ":
        show_faq()
    elif doc_section == "🔧 Troubleshooting":
        show_troubleshooting()

def show_getting_started():
    """Getting started documentation"""
    
    st.markdown("### 🚀 Getting Started with GeoMasterPy")
    
    st.markdown("""
    #### Installation
    
    ```bash
    pip install geomasterpy
    ```
    
    #### Basic Usage
    
    ```python
    import geomasterpy as gmp
    import ee
    
    # Initialize Earth Engine
    ee.Initialize()
    
    # Create a map
    Map = gmp.Map(center=(37.7749, -122.4194), zoom=10)
    
    # Load satellite data
    image = ee.Image('LANDSAT/LC08/C02/T1_L2').first()
    
    # Add to map
    Map.add_ee_layer(image, {
        'bands': ['SR_B4', 'SR_B3', 'SR_B2'],
        'min': 0, 'max': 3000
    }, 'Landsat 8')
    
    # Display map
    Map
    ```
    
    #### Key Concepts
    
    - **Interactive Maps**: Create dynamic maps with `gmp.Map()`
    - **Data Loading**: Use Earth Engine collections and images
    - **Visualization**: Add layers with custom styling
    - **Analysis**: Perform statistical analysis and classification
    - **Export**: Save results to files or cloud storage
    """)

def show_api_reference():
    """API reference documentation"""
    
    st.markdown("### 📖 API Reference")
    
    api_modules = {
        "Map": [
            ("Map()", "Create interactive map widget"),
            ("add_ee_layer()", "Add Earth Engine layer to map"),
            ("add_basemap()", "Add basemap layer"),
            ("set_center()", "Set map center and zoom")
        ],
        "Data": [
            ("search_ee_data()", "Search Earth Engine catalog"),
            ("js_snippet_to_python()", "Convert JavaScript to Python"),
            ("get_dataset_info()", "Get dataset metadata")
        ],
        "Analysis": [
            ("image_stats()", "Calculate image statistics"),
            ("zonal_stats()", "Perform zonal statistics"),
            ("calculate_indices()", "Compute spectral indices"),
            ("supervised_classification()", "Classify images")
        ],
        "Export": [
            ("export_image_to_local()", "Export images locally"),
            ("export_vector_to_local()", "Export vector data"),
            ("export_to_drive()", "Export to Google Drive")
        ],
        "Visualization": [
            ("add_legend()", "Add custom legend"),
            ("add_colorbar()", "Add colorbar"),
            ("create_time_series_chart()", "Create time series"),
            ("plot_ee_image_cartopy()", "Publication maps")
        ]
    }
    
    for module, functions in api_modules.items():
        with st.expander(f"📦 {module} Module"):
            for func_name, description in functions:
                st.markdown(f"**`{func_name}`** - {description}")

def show_examples():
    """Examples and tutorials"""
    
    st.markdown("### 💡 Examples & Tutorials")
    
    examples = [
        {
            "title": "🗺️ Basic Interactive Mapping",
            "description": "Create your first interactive map with satellite imagery",
            "code": """
import geomasterpy as gmp
import ee

ee.Initialize()

# Create map
Map = gmp.Map(center=(37.7749, -122.4194), zoom=10)

# Add Landsat 8
landsat = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2').first()
Map.add_ee_layer(landsat, {
    'bands': ['SR_B4', 'SR_B3', 'SR_B2'],
    'min': 0, 'max': 3000
}, 'Landsat 8')

Map
            """
        },
        {
            "title": "📊 NDVI Time Series Analysis",
            "description": "Analyze vegetation changes over time",
            "code": """
import geomasterpy as gmp
import ee

# Load Landsat collection
collection = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2') \\
    .filterDate('2020-01-01', '2023-12-31') \\
    .filter(ee.Filter.lt('CLOUD_COVER', 20))

# Calculate NDVI for each image
def add_ndvi(image):
    ndvi = image.normalizedDifference(['SR_B5', 'SR_B4']).rename('NDVI')
    return image.addBands(ndvi)

ndvi_collection = collection.map(add_ndvi)

# Create time series chart
region = ee.Geometry.Point([-122.4194, 37.7749]).buffer(1000)
chart = gmp.viz.create_time_series_chart(
    ndvi_collection, region, 'NDVI'
)
chart
            """
        },
        {
            "title": "🏷️ Land Cover Classification",
            "description": "Classify land cover using machine learning",
            "code": """
import geomasterpy as gmp
import ee

# Load and prepare image
image = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2').median()

# Add spectral indices
image_with_indices = gmp.analysis.calculate_indices(
    image, ['NDVI', 'NDWI', 'NDBI']
)

# Perform unsupervised classification
classified = gmp.analysis.unsupervised_classification(
    image_with_indices,
    num_classes=5,
    scale=30
)

# Visualize results
Map = gmp.Map()
Map.add_ee_layer(classified, {
    'min': 0, 'max': 4,
    'palette': ['red', 'blue', 'green', 'yellow', 'purple']
}, 'Land Cover')

Map
            """
        }
    ]
    
    for example in examples:
        with st.expander(example["title"]):
            st.markdown(example["description"])
            st.code(example["code"], language='python')

def show_faq():
    """FAQ section"""
    
    st.markdown("### ❓ Frequently Asked Questions")
    
    faqs = [
        {
            "question": "How do I authenticate Google Earth Engine?",
            "answer": """
            Run the following in Python:
            ```python
            import ee
            ee.Authenticate()  # Opens browser for authentication
            ee.Initialize()
            ```
            """
        },
        {
            "question": "Can I use GeoMasterPy without Earth Engine?",
            "answer": """
            Yes! Many features work without Earth Engine:
            - Data catalog search
            - JavaScript to Python conversion
            - Basic map creation
            - Static visualizations
            """
        },
        {
            "question": "How do I export large images?",
            "answer": """
            For large exports, use Google Drive export:
            ```python
            task = gmp.export.export_image_to_drive(
                image, 'my_export', scale=30
            )
            ```
            """
        },
        {
            "question": "What file formats are supported for export?",
            "answer": """
            **Images**: GeoTIFF, PNG, JPEG
            **Vectors**: Shapefile, GeoJSON, KML
            **Data**: CSV, JSON
            """
        }
    ]
    
    for faq in faqs:
        with st.expander(faq["question"]):
            st.markdown(faq["answer"])

def show_troubleshooting():
    """Troubleshooting guide"""
    
    st.markdown("### 🔧 Troubleshooting")
    
    issues = [
        {
            "issue": "Earth Engine authentication errors",
            "solution": """
            1. Run `ee.Authenticate()` in Python
            2. Follow browser authentication prompts
            3. Ensure you have Earth Engine access
            4. Try `ee.Initialize()` after authentication
            """
        },
        {
            "issue": "Maps not displaying in Jupyter",
            "solution": """
            1. Enable ipyleaflet extension:
               ```bash
               jupyter nbextension enable --py --sys-prefix ipyleaflet
               ```
            2. Restart Jupyter
            3. Try refreshing the page
            """
        },
        {
            "issue": "Memory errors with large datasets",
            "solution": """
            1. Reduce analysis scale
            2. Filter data by date/region
            3. Use server-side operations when possible
            4. Export large results to Drive instead of local
            """
        }
    ]
    
    for item in issues:
        with st.expander(f"❗ {item['issue']}"):
            st.markdown(item['solution'])

# Helper functions for missing components
def show_zonal_statistics():
    st.info("Zonal statistics interface would be implemented here")

def show_classification():
    st.info("Classification interface would be implemented here")

def show_change_detection():
    st.info("Change detection interface would be implemented here")

def show_histogram_viz():
    st.info("Histogram visualization would be implemented here")

def show_interactive_plots():
    st.info("Interactive plots interface would be implemented here")

def show_animations():
    st.info("Animation tools would be implemented here")

def show_legends_colorbars():
    st.info("Legends and colorbars interface would be implemented here")

def show_vector_export():
    st.info("Vector export interface would be implemented here")

def show_stats_export():
    st.info("Statistics export interface would be implemented here")

def show_timeseries_export():
    st.info("Time series export interface would be implemented here")

def show_drive_export():
    st.info("Google Drive export interface would be implemented here")

if __name__ == "__main__":
    main()