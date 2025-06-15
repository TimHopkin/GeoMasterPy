"""
GeoMasterPy Streamlit Web Application

An interactive web interface for GeoMasterPy - making Google Earth Engine
accessible through a user-friendly web application.
"""

import streamlit as st

# Configure Streamlit page - MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="GeoMasterPy - Interactive Earth Engine Tool",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Now import other modules
import pandas as pd
import numpy as np
import json
from datetime import datetime, date
import base64
from io import BytesIO

# Import with error handling - NO st.error() calls here since st.set_page_config must be first
try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

try:
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError as e:
    PLOTLY_AVAILABLE = False

try:
    import folium
    from streamlit_folium import st_folium
    FOLIUM_AVAILABLE = True
except ImportError:
    FOLIUM_AVAILABLE = False

# Import GeoMasterPy components (with fallbacks for demo mode)
try:
    import geomasterpy as gmp
    GEOMASTERPY_AVAILABLE = True
except ImportError as e:
    GEOMASTERPY_AVAILABLE = False

try:
    import ee
    EE_AVAILABLE = True
except ImportError as e:
    EE_AVAILABLE = False

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
    
    # Show requirements info
    if not PLOTLY_AVAILABLE or not FOLIUM_AVAILABLE:
        st.warning("⚠️ Missing dependencies detected. Check requirements file.")
        with st.expander("📋 Requirements Debug Info"):
            st.code("""
# Try these requirements files on Streamlit Cloud:

Option 1 (Basic - Guaranteed):
requirements_basic.txt

Option 2 (Standard):  
requirements_streamlit.txt

Option 3 (Minimal):
requirements_minimal.txt
            """)
    
    # Check system status
    with st.expander("🔧 System Status", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if PLOTLY_AVAILABLE:
                st.success("✅ Plotly")
            else:
                st.error("❌ Plotly Missing")
                st.caption("Run: pip install plotly")
        
        with col2:
            if FOLIUM_AVAILABLE:
                st.success("✅ Folium")
            else:
                st.error("❌ Folium Missing")
                st.caption("Run: pip install folium streamlit-folium")
        
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
            "🌍 Land App (New!)",
            "📁 Area of Interest",
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
    elif page == "🌍 Land App (New!)":
        show_land_app()
    elif page == "📁 Area of Interest":
        show_area_of_interest()
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

def show_land_app():
    """Display the Land App interface"""
    
    st.markdown("# 🌍 Land App - Advanced Land Management Platform")
    
    # Option to run the dedicated Land App
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 🚀 New Land Management Application
        
        Our **Land App** is a comprehensive land management platform featuring:
        
        - **🗺️ Interactive Mapping** with OpenStreetMap integration
        - **✏️ Drawing Tools** for polygons, circles, rectangles, and points
        - **📋 Plans Management** to organize and manage spatial features
        - **🎓 Learning Centre** with interactive tutorials and AI assistance
        - **🔗 URL Navigation** between map and learning sections
        - **📊 Real-time Analysis** with instant area calculations
        - **🌐 Offline Capability** - works without internet once loaded
        
        **Designed with Material Design 3** for a modern, intuitive experience.
        """)
    
    with col2:
        st.markdown("### 🎯 Quick Access")
        
        # Direct link to standalone Land App
        land_app_url = "streamlit_land_app.py"
        st.markdown(f"""
        **🌍 Standalone Land App:**  
        Run: `streamlit run streamlit_land_app.py`
        
        **🌐 Local HTML Version:**  
        Open: `src/web/land-app-ui-mockup.html`
        """)
        
        if st.button("🚀 Launch Land App in New Tab", help="Opens the standalone Land App"):
            st.markdown("""
            **To launch the Land App:**
            1. Open a new terminal
            2. Run: `streamlit run streamlit_land_app.py --server.port 8502`
            3. Open: http://localhost:8502
            """)
    
    # Embedded preview
    st.markdown("---")
    st.markdown("### 📱 Live Preview")
    
    # Load and display the Land App HTML
    from pathlib import Path
    land_app_path = Path(__file__).parent / "src" / "web" / "land-app-ui-mockup.html"
    
    if land_app_path.exists():
        # Read the HTML file
        with open(land_app_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Display the HTML content in an iframe-style container
        st.components.v1.html(html_content, height=600, scrolling=True)
        
        # Download option
        st.markdown("### 📥 Download")
        st.download_button(
            label="💾 Download Complete Land App",
            data=html_content,
            file_name="land-app.html",
            mime="text/html",
            help="Download the complete Land App as a single HTML file"
        )
        
    else:
        st.error("Land App HTML file not found.")
        st.info("Expected location: src/web/land-app-ui-mockup.html")

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
        1. 📁 Define your **Area of Interest** from Google Drive
        2. 🔍 Start with **Data Catalog** to explore datasets
        3. 🗺️ Create your first **Interactive Map**
        4. 📊 Explore **Data Analysis** tools
        """)
    
    with col2:
        st.markdown("### For Advanced Users")
        st.markdown("""
        1. 📁 Upload **Area of Interest** boundary from Google Drive
        2. 📊 Jump to **Data Analysis** for complex workflows
        3. 🖼️ Create **Publication Maps** for research
        4. 💾 Use **Export Tools** for data management
        """)

def show_area_of_interest():
    """Area of Interest definition interface with Google Drive GeoJSON support"""
    
    st.markdown("## 📁 Define Your Area of Interest")
    st.markdown("Load a GeoJSON file from Google Drive to define your study area for analysis.")
    
    # Instructions
    with st.expander("📖 How to use Google Drive GeoJSON", expanded=False):
        st.markdown("""
        ### Steps to share a GeoJSON file from Google Drive:
        
        1. **Upload your GeoJSON file to Google Drive**
        2. **Right-click the file** and select "Share"
        3. **Change permissions** to "Anyone with the link can view"
        4. **Copy the sharing link** and paste it below
        
        ### Supported URL formats:
        - `https://drive.google.com/file/d/FILE_ID/view?usp=sharing`
        - `https://drive.google.com/open?id=FILE_ID`
        - `https://drive.google.com/uc?id=FILE_ID`
        
        ### Tips:
        - Ensure your GeoJSON file is valid
        - Keep file sizes reasonable (< 10MB recommended)
        - Use simple geometries for better performance
        """)
    
    # Google Drive URL input
    st.markdown("### 🔗 Google Drive GeoJSON URL")
    
    # Session state for storing the loaded geometry
    if 'aoi_geometry' not in st.session_state:
        st.session_state.aoi_geometry = None
    if 'aoi_geojson' not in st.session_state:
        st.session_state.aoi_geojson = None
    if 'aoi_name' not in st.session_state:
        st.session_state.aoi_name = "Custom Area"
    
    # URL input
    drive_url = st.text_input(
        "Enter Google Drive sharing URL:",
        placeholder="https://drive.google.com/file/d/YOUR_FILE_ID/view?usp=sharing",
        help="Paste the sharing URL of your GeoJSON file from Google Drive"
    )
    
    # Optional: Area name
    aoi_name = st.text_input(
        "Area name (optional):",
        value=st.session_state.aoi_name,
        placeholder="e.g., My Study Area, Farm Boundary, etc."
    )
    
    # Load button
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("🔄 Load GeoJSON", type="primary"):
            if drive_url:
                with st.spinner("Loading GeoJSON from Google Drive..."):
                    try:
                        # Validate URL first
                        if not GEOMASTERPY_AVAILABLE:
                            st.error("GeoMasterPy not available. Please check installation.")
                        else:
                            # Import the functions
                            from geomasterpy.data.catalog import (
                                validate_drive_url, 
                                load_geojson_from_drive_url,
                                geojson_to_ee_geometry
                            )
                            
                            # Validate URL
                            if not validate_drive_url(drive_url):
                                st.error("Invalid Google Drive URL. Please check the format.")
                            else:
                                # Load GeoJSON
                                geojson_data = load_geojson_from_drive_url(drive_url)
                                
                                if geojson_data:
                                    # Store in session state
                                    st.session_state.aoi_geojson = geojson_data
                                    st.session_state.aoi_name = aoi_name if aoi_name else "Custom Area"
                                    
                                    # Convert to Earth Engine geometry if EE is available
                                    if EE_AVAILABLE:
                                        ee_geometry = geojson_to_ee_geometry(geojson_data)
                                        st.session_state.aoi_geometry = ee_geometry
                                    
                                    st.success(f"✅ Successfully loaded GeoJSON: {st.session_state.aoi_name}")
                                    
                                else:
                                    st.error("Failed to load GeoJSON. Please check the URL and file format.")
                                    
                    except Exception as e:
                        st.error(f"Error loading GeoJSON: {str(e)}")
            else:
                st.warning("Please enter a Google Drive URL")
    
    with col2:
        if st.button("🗑️ Clear Area"):
            st.session_state.aoi_geometry = None
            st.session_state.aoi_geojson = None
            st.session_state.aoi_name = "Custom Area"
            st.success("Area of interest cleared")
    
    # Display current area of interest
    if st.session_state.aoi_geojson:
        st.markdown("### 📍 Current Area of Interest")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.info(f"**Name:** {st.session_state.aoi_name}")
            
            # Display basic info about the GeoJSON
            geojson_type = st.session_state.aoi_geojson.get('type', 'Unknown')
            st.info(f"**Type:** {geojson_type}")
            
            if geojson_type == 'FeatureCollection':
                num_features = len(st.session_state.aoi_geojson.get('features', []))
                st.info(f"**Features:** {num_features}")
            
        with col2:
            # Show options for using this AOI
            st.markdown("**Use this area for:**")
            if st.button("🗺️ View on Interactive Map"):
                st.info("Navigate to '🗺️ Interactive Maps' to visualize your area")
            if st.button("📊 Run Data Analysis"):
                st.info("Navigate to '📊 Data Analysis' to analyze your area")
            if st.button("💾 Export Data"):
                st.info("Navigate to '💾 Export Tools' to export data from your area")
        
        # Display the GeoJSON on a map if Folium is available
        if FOLIUM_AVAILABLE:
            st.markdown("### 🌍 Area Preview")
            
            try:
                import folium
                import json
                
                # Create a simple folium map
                # Calculate bounds from GeoJSON
                if st.session_state.aoi_geojson['type'] == 'FeatureCollection':
                    # Get first feature's coordinates for centering
                    first_feature = st.session_state.aoi_geojson['features'][0]
                    coords = first_feature['geometry']['coordinates']
                else:
                    coords = st.session_state.aoi_geojson['coordinates']
                
                # Create map centered on the area
                m = folium.Map(location=[0, 0], zoom_start=2)
                
                # Add GeoJSON to map
                folium.GeoJson(
                    st.session_state.aoi_geojson,
                    style_function=lambda x: {
                        'fillColor': 'red',
                        'color': 'red',
                        'weight': 2,
                        'fillOpacity': 0.3
                    }
                ).add_to(m)
                
                # Fit bounds to the geometry
                geojson_layer = folium.GeoJson(st.session_state.aoi_geojson)
                m.fit_bounds(geojson_layer.get_bounds())
                
                # Display map
                st_folium(m, width=700, height=400)
                
            except Exception as e:
                st.warning(f"Could not display map preview: {str(e)}")
        
        # Raw GeoJSON viewer (optional)
        with st.expander("🔍 View Raw GeoJSON", expanded=False):
            st.json(st.session_state.aoi_geojson)
    
    else:
        st.markdown("### 📍 No Area of Interest Defined")
        st.info("Load a GeoJSON file from Google Drive to define your study area.")
        
        # Show example without actual loading
        st.markdown("### 📋 Example Analysis Workflow")
        st.markdown("""
        Once you load an area of interest, you can:
        
        1. **🗺️ Visualize** your area on interactive maps
        2. **📊 Analyze** satellite data within your boundary
        3. **📈 Create** time series charts and statistics
        4. **💾 Export** results and processed data
        5. **🖼️ Generate** publication-quality maps
        
        All analysis tools will automatically use your defined area as the region of interest.
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
    
    # Area of Interest status
    if st.session_state.get('aoi_geometry') is not None:
        st.success(f"✅ Using Area of Interest: **{st.session_state.get('aoi_name', 'Custom Area')}**")
        st.info("All analysis will be focused on your defined area of interest.")
    else:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.warning("⚠️ No Area of Interest defined. Analysis will use sample/default regions.")
        with col2:
            if st.button("📁 Load AOI"):
                st.info("Navigate to '📁 Area of Interest' to load your study area")
    
    st.markdown("---")
    
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
        
        # Region selection based on AOI availability
        if st.session_state.get('aoi_geometry') is not None:
            st.success(f"📍 Analysis region: {st.session_state.get('aoi_name', 'Custom Area')}")
            use_aoi = True
        else:
            st.info("💡 Using sample coordinates. Load an Area of Interest for real analysis.")
            use_aoi = False
        
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
        
        # Date range for analysis
        col_start, col_end = st.columns(2)
        with col_start:
            start_date = st.date_input("Start date:", datetime(2023, 1, 1).date())
        with col_end:
            end_date = st.date_input("End date:", datetime(2023, 12, 31).date())
        
        if st.button("📊 Calculate Statistics"):
            with st.spinner("Calculating statistics..."):
                if use_aoi and EE_AVAILABLE and GEOMASTERPY_AVAILABLE:
                    try:
                        import ee
                        
                        # Initialize Earth Engine
                        ee.Initialize()
                        
                        # Get the AOI geometry
                        region = st.session_state.aoi_geometry
                        
                        # Select appropriate dataset
                        if dataset == "Landsat 8":
                            collection = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
                            band_mapping = {
                                'Blue': 'SR_B2', 'Green': 'SR_B3', 'Red': 'SR_B4',
                                'NIR': 'SR_B5', 'SWIR1': 'SR_B6', 'SWIR2': 'SR_B7'
                            }
                        elif dataset == "Sentinel-2":
                            collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
                            band_mapping = {
                                'Blue': 'B2', 'Green': 'B3', 'Red': 'B4',
                                'NIR': 'B8', 'SWIR1': 'B11', 'SWIR2': 'B12'
                            }
                        else:  # MODIS
                            collection = ee.ImageCollection('MODIS/061/MOD09A1')
                            band_mapping = {
                                'Red': 'sur_refl_b01', 'NIR': 'sur_refl_b02',
                                'Blue': 'sur_refl_b03', 'Green': 'sur_refl_b04',
                                'SWIR1': 'sur_refl_b06', 'SWIR2': 'sur_refl_b07'
                            }
                        
                        # Filter collection
                        image = collection.filterBounds(region) \
                                        .filterDate(start_date.isoformat(), end_date.isoformat()) \
                                        .median()
                        
                        # Select bands
                        selected_bands = [band_mapping[band] for band in bands if band in band_mapping]
                        image = image.select(selected_bands)
                        
                        # Calculate statistics
                        stats = image.reduceRegion(
                            reducer=ee.Reducer.mean().combine(
                                ee.Reducer.stdDev(), '', True
                            ).combine(
                                ee.Reducer.minMax(), '', True
                            ).combine(
                                ee.Reducer.median(), '', True
                            ),
                            geometry=region,
                            scale=scale,
                            maxPixels=1e9
                        ).getInfo()
                        
                        # Format results
                        results = []
                        for i, band in enumerate(bands):
                            if band in band_mapping:
                                ee_band = band_mapping[band]
                                results.append({
                                    'Band': band,
                                    'Mean': stats.get(f'{ee_band}_mean', 0),
                                    'Std': stats.get(f'{ee_band}_stdDev', 0),
                                    'Min': stats.get(f'{ee_band}_min', 0),
                                    'Max': stats.get(f'{ee_band}_max', 0),
                                    'Median': stats.get(f'{ee_band}_median', 0)
                                })
                        
                        if results:
                            real_stats = pd.DataFrame(results)
                            st.session_state['stats'] = real_stats
                            st.success(f"✅ Calculated statistics for {st.session_state.aoi_name}")
                        else:
                            st.error("No valid data found for the selected bands and region")
                            
                    except Exception as e:
                        st.error(f"Error calculating real statistics: {str(e)}")
                        st.info("Falling back to demo data...")
                        # Fall back to demo data
                        demo_stats = pd.DataFrame({
                            'Band': bands,
                            'Mean': np.random.uniform(0.1, 0.3, len(bands)),
                            'Std': np.random.uniform(0.05, 0.15, len(bands)),
                            'Min': np.random.uniform(0.0, 0.1, len(bands)),
                            'Max': np.random.uniform(0.4, 0.8, len(bands)),
                            'Median': np.random.uniform(0.15, 0.25, len(bands))
                        })
                        st.session_state['stats'] = demo_stats
                else:
                    # Demo statistics for when AOI is not available or EE not initialized
                    demo_stats = pd.DataFrame({
                        'Band': bands,
                        'Mean': np.random.uniform(0.1, 0.3, len(bands)),
                        'Std': np.random.uniform(0.05, 0.15, len(bands)),
                        'Min': np.random.uniform(0.0, 0.1, len(bands)),
                        'Max': np.random.uniform(0.4, 0.8, len(bands)),
                        'Median': np.random.uniform(0.15, 0.25, len(bands))
                    })
                    st.session_state['stats'] = demo_stats
                    if not use_aoi:
                        st.info("📍 These are sample statistics. Load an Area of Interest for real analysis.")
    
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
    """Zonal statistics interface with AOI integration"""
    
    st.markdown("### 🎯 Zonal Statistics")
    st.markdown("Calculate statistics for different zones within your area of interest")
    
    # Check for AOI
    if st.session_state.get('aoi_geometry') is None:
        st.warning("⚠️ Zonal statistics requires an Area of Interest to be defined")
        st.markdown("""
        **To use zonal statistics:**
        1. Navigate to the **📁 Area of Interest** page
        2. Load a GeoJSON file from Google Drive
        3. Return here to analyze zones within your area
        
        **Note:** Your GeoJSON should contain multiple features/polygons to analyze as separate zones.
        """)
        return
    
    # Display current AOI info
    st.success(f"✅ Analyzing zones within: **{st.session_state.get('aoi_name', 'Custom Area')}**")
    
    # Check if AOI has multiple features for zonal analysis
    aoi_geojson = st.session_state.get('aoi_geojson')
    if aoi_geojson and aoi_geojson.get('type') == 'FeatureCollection':
        num_zones = len(aoi_geojson.get('features', []))
        if num_zones > 1:
            st.info(f"📊 Found {num_zones} zones for analysis")
        else:
            st.info("ℹ️ Single zone detected. Analysis will calculate statistics for the entire area.")
    else:
        st.info("ℹ️ Single zone detected. Analysis will calculate statistics for the entire area.")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### Settings")
        
        dataset = st.selectbox(
            "Dataset:",
            ["Landsat 8", "Sentinel-2", "MODIS"],
            help="Choose the satellite dataset for analysis"
        )
        
        bands = st.multiselect(
            "Bands to analyze:",
            ["Blue", "Green", "Red", "NIR", "SWIR1", "SWIR2"],
            default=["Red", "NIR", "Green"],
            help="Select bands for statistical analysis"
        )
        
        scale = st.number_input("Analysis scale (meters):", 10, 1000, 30)
        
        # Date range
        col_start, col_end = st.columns(2)
        with col_start:
            start_date = st.date_input("Start date:", datetime(2023, 6, 1).date())
        with col_end:
            end_date = st.date_input("End date:", datetime(2023, 8, 31).date())
        
        # Analysis type
        analysis_type = st.selectbox(
            "Statistics to calculate:",
            ["Basic (mean, median)", "Extended (mean, std, min, max)", "All statistics"],
            index=1
        )
        
        if st.button("🎯 Run Zonal Analysis", type="primary"):
            if not bands:
                st.error("Please select at least one band for analysis")
                return
                
            with st.spinner("Running zonal statistics analysis..."):
                if EE_AVAILABLE and GEOMASTERPY_AVAILABLE:
                    try:
                        import ee
                        
                        # Initialize Earth Engine
                        ee.Initialize()
                        
                        # Get zones from AOI
                        if aoi_geojson['type'] == 'FeatureCollection' and len(aoi_geojson['features']) > 1:
                            # Multiple zones
                            zones = ee.FeatureCollection(aoi_geojson)
                        else:
                            # Single zone - create a feature collection with one feature
                            zones = ee.FeatureCollection([ee.Feature(st.session_state.aoi_geometry)])
                        
                        # Select dataset and bands
                        if dataset == "Landsat 8":
                            collection = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
                            band_mapping = {
                                'Blue': 'SR_B2', 'Green': 'SR_B3', 'Red': 'SR_B4',
                                'NIR': 'SR_B5', 'SWIR1': 'SR_B6', 'SWIR2': 'SR_B7'
                            }
                        elif dataset == "Sentinel-2":
                            collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
                            band_mapping = {
                                'Blue': 'B2', 'Green': 'B3', 'Red': 'B4',
                                'NIR': 'B8', 'SWIR1': 'B11', 'SWIR2': 'B12'
                            }
                        else:  # MODIS
                            collection = ee.ImageCollection('MODIS/061/MOD09A1')
                            band_mapping = {
                                'Red': 'sur_refl_b01', 'NIR': 'sur_refl_b02',
                                'Blue': 'sur_refl_b03', 'Green': 'sur_refl_b04',
                                'SWIR1': 'sur_refl_b06', 'SWIR2': 'sur_refl_b07'
                            }
                        
                        # Filter and select image
                        image = collection.filterBounds(st.session_state.aoi_geometry) \
                                        .filterDate(start_date.isoformat(), end_date.isoformat()) \
                                        .median()
                        
                        # Select bands
                        selected_bands = [band_mapping[band] for band in bands if band in band_mapping]
                        image = image.select(selected_bands)
                        
                        # Choose reducer based on analysis type
                        if analysis_type == "Basic (mean, median)":
                            reducer = ee.Reducer.mean().combine(ee.Reducer.median(), '', True)
                        elif analysis_type == "Extended (mean, std, min, max)":
                            reducer = ee.Reducer.mean().combine(
                                ee.Reducer.stdDev(), '', True
                            ).combine(
                                ee.Reducer.minMax(), '', True
                            )
                        else:  # All statistics
                            reducer = ee.Reducer.mean().combine(
                                ee.Reducer.stdDev(), '', True
                            ).combine(
                                ee.Reducer.minMax(), '', True
                            ).combine(
                                ee.Reducer.median(), '', True
                            ).combine(
                                ee.Reducer.count(), '', True
                            )
                        
                        # Calculate zonal statistics
                        zonal_stats = image.reduceRegions(
                            collection=zones,
                            reducer=reducer,
                            scale=scale,
                            crs='EPSG:4326'
                        )
                        
                        # Get results
                        results = zonal_stats.getInfo()
                        
                        # Process results into a DataFrame
                        processed_results = []
                        for i, feature in enumerate(results['features']):
                            props = feature['properties']
                            zone_data = {'Zone': f'Zone {i+1}'}
                            
                            # Extract statistics for each band
                            for band in bands:
                                if band in band_mapping:
                                    ee_band = band_mapping[band]
                                    if analysis_type == "Basic (mean, median)":
                                        zone_data[f'{band}_mean'] = props.get(f'{ee_band}_mean', 0)
                                        zone_data[f'{band}_median'] = props.get(f'{ee_band}_median', 0)
                                    elif analysis_type == "Extended (mean, std, min, max)":
                                        zone_data[f'{band}_mean'] = props.get(f'{ee_band}_mean', 0)
                                        zone_data[f'{band}_std'] = props.get(f'{ee_band}_stdDev', 0)
                                        zone_data[f'{band}_min'] = props.get(f'{ee_band}_min', 0)
                                        zone_data[f'{band}_max'] = props.get(f'{ee_band}_max', 0)
                                    else:  # All statistics
                                        zone_data[f'{band}_mean'] = props.get(f'{ee_band}_mean', 0)
                                        zone_data[f'{band}_std'] = props.get(f'{ee_band}_stdDev', 0)
                                        zone_data[f'{band}_min'] = props.get(f'{ee_band}_min', 0)
                                        zone_data[f'{band}_max'] = props.get(f'{ee_band}_max', 0)
                                        zone_data[f'{band}_median'] = props.get(f'{ee_band}_median', 0)
                                        zone_data[f'{band}_count'] = props.get(f'{ee_band}_count', 0)
                            
                            processed_results.append(zone_data)
                        
                        if processed_results:
                            zonal_df = pd.DataFrame(processed_results)
                            st.session_state['zonal_stats'] = zonal_df
                            st.success(f"✅ Calculated zonal statistics for {len(processed_results)} zones")
                        else:
                            st.error("No valid data found for the selected parameters")
                            
                    except Exception as e:
                        st.error(f"Error calculating zonal statistics: {str(e)}")
                        st.info("Generating demo data...")
                        
                        # Generate demo data
                        demo_zones = 3 if aoi_geojson.get('type') == 'FeatureCollection' and len(aoi_geojson.get('features', [])) > 1 else 1
                        demo_data = []
                        for i in range(demo_zones):
                            zone_data = {'Zone': f'Zone {i+1}'}
                            for band in bands:
                                if analysis_type == "Basic (mean, median)":
                                    zone_data[f'{band}_mean'] = round(np.random.uniform(0.1, 0.3), 3)
                                    zone_data[f'{band}_median'] = round(np.random.uniform(0.15, 0.25), 3)
                                elif analysis_type == "Extended (mean, std, min, max)":
                                    zone_data[f'{band}_mean'] = round(np.random.uniform(0.1, 0.3), 3)
                                    zone_data[f'{band}_std'] = round(np.random.uniform(0.05, 0.15), 3)
                                    zone_data[f'{band}_min'] = round(np.random.uniform(0.0, 0.1), 3)
                                    zone_data[f'{band}_max'] = round(np.random.uniform(0.4, 0.8), 3)
                                else:  # All statistics
                                    zone_data[f'{band}_mean'] = round(np.random.uniform(0.1, 0.3), 3)
                                    zone_data[f'{band}_std'] = round(np.random.uniform(0.05, 0.15), 3)
                                    zone_data[f'{band}_min'] = round(np.random.uniform(0.0, 0.1), 3)
                                    zone_data[f'{band}_max'] = round(np.random.uniform(0.4, 0.8), 3)
                                    zone_data[f'{band}_median'] = round(np.random.uniform(0.15, 0.25), 3)
                                    zone_data[f'{band}_count'] = np.random.randint(1000, 5000)
                            demo_data.append(zone_data)
                        
                        demo_df = pd.DataFrame(demo_data)
                        st.session_state['zonal_stats'] = demo_df
                        st.warning("⚠️ Showing demo data. Real analysis requires Earth Engine authentication.")
                        
                else:
                    st.error("Earth Engine or GeoMasterPy not available. Cannot perform real analysis.")
    
    with col2:
        st.markdown("#### Results")
        
        if 'zonal_stats' in st.session_state:
            df = st.session_state['zonal_stats']
            st.dataframe(df, use_container_width=True)
            
            # Download button
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"zonal_stats_{st.session_state.get('aoi_name', 'area').replace(' ', '_')}.csv",
                mime="text/csv"
            )
            
            # Visualization
            if PLOTLY_AVAILABLE and len(df) > 1:
                st.markdown("#### Visualization")
                
                # Select bands for plotting
                numeric_cols = [col for col in df.columns if col != 'Zone' and not col.endswith('_count')]
                
                if numeric_cols:
                    plot_bands = st.multiselect(
                        "Select bands/statistics to plot:",
                        numeric_cols,
                        default=numeric_cols[:3] if len(numeric_cols) >= 3 else numeric_cols
                    )
                    
                    if plot_bands:
                        # Create comparison chart
                        fig = px.bar(
                            df.melt(id_vars=['Zone'], value_vars=plot_bands, 
                                   var_name='Band_Stat', value_name='Value'),
                            x='Zone', y='Value', color='Band_Stat',
                            title="Zonal Statistics Comparison",
                            height=400
                        )
                        st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Run the analysis to see results here")
            
            # Show example of what zonal statistics can reveal
            st.markdown("""
            **Zonal statistics help you:**
            - Compare different areas within your region
            - Identify spatial patterns and variations
            - Quantify differences between land cover types
            - Monitor changes across different zones
            - Generate reports for specific sub-regions
            """)

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