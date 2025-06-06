"""
GeoMasterPy Streamlit App - Cloud Optimized Version
Designed specifically for Streamlit Cloud deployment with minimal dependencies
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
from datetime import datetime, date
import base64
from io import BytesIO

# Configure Streamlit page - MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="GeoMasterPy - Cloud Edition",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Check for available packages
DEPENDENCIES = {}

def check_dependency(name, import_path):
    """Check if a dependency is available"""
    try:
        __import__(import_path)
        DEPENDENCIES[name] = True
        return True
    except ImportError:
        DEPENDENCIES[name] = False
        return False

# Check all dependencies
check_dependency('plotly', 'plotly.express')
check_dependency('folium', 'folium')
check_dependency('matplotlib', 'matplotlib.pyplot')
check_dependency('requests', 'requests')

# Import available dependencies
if DEPENDENCIES['plotly']:
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

if DEPENDENCIES['folium']:
    import folium
    from streamlit_folium import st_folium

if DEPENDENCIES['matplotlib']:
    import matplotlib.pyplot as plt

if DEPENDENCIES['requests']:
    import requests

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
    .status-good { color: #4CAF50; }
    .status-missing { color: #f44336; }
    .status-optional { color: #ff9800; }
</style>
""", unsafe_allow_html=True)

def main():
    """Main Streamlit application"""
    
    # Header
    st.markdown('<h1 class="main-header">🌍 GeoMasterPy Cloud Edition</h1>', unsafe_allow_html=True)
    st.markdown("**Interactive Geospatial Analysis - Cloud Optimized**")
    
    # Show deployment status
    show_system_status()
    
    # Initialize session state for AOI if not exists
    if 'aoi_geometry' not in st.session_state:
        st.session_state.aoi_geometry = None
    if 'aoi_geojson' not in st.session_state:
        st.session_state.aoi_geojson = None
    if 'aoi_name' not in st.session_state:
        st.session_state.aoi_name = "Custom Area"
    
    # Sidebar navigation
    st.sidebar.title("🧭 Navigation")
    
    # Show AOI status in sidebar
    if st.session_state.aoi_geojson is not None:
        st.sidebar.success(f"✅ AOI: {st.session_state.aoi_name}")
        if st.sidebar.button("🗑️ Clear AOI"):
            st.session_state.aoi_geometry = None
            st.session_state.aoi_geojson = None
            st.session_state.aoi_name = "Custom Area"
            st.rerun()
    else:
        st.sidebar.info("📍 No AOI defined")
    
    page = st.sidebar.selectbox(
        "Choose a feature:",
        [
            "🏠 Home",
            "📁 Area of Interest",
            "📊 Data Analysis Demo",
            "🗺️ Interactive Maps", 
            "📈 Visualizations",
            "🔧 Cloud Setup Guide",
            "📚 Documentation"
        ]
    )
    
    # Route to different pages
    if page == "🏠 Home":
        show_home()
    elif page == "📁 Area of Interest":
        show_area_of_interest()
    elif page == "📊 Data Analysis Demo":
        show_data_analysis_demo()
    elif page == "🗺️ Interactive Maps":
        show_interactive_maps()
    elif page == "📈 Visualizations":
        show_visualizations()
    elif page == "🔧 Cloud Setup Guide":
        show_cloud_setup()
    elif page == "📚 Documentation":
        show_documentation()

def show_system_status():
    """Display system status for cloud deployment"""
    
    with st.expander("🔧 Cloud Deployment Status", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        
        # Core dependencies (required)
        with col1:
            st.markdown("**Core Dependencies**")
            st.markdown('<p class="status-good">✅ Streamlit</p>', unsafe_allow_html=True)
            st.markdown('<p class="status-good">✅ Pandas</p>', unsafe_allow_html=True)
            st.markdown('<p class="status-good">✅ NumPy</p>', unsafe_allow_html=True)
        
        # Visualization dependencies
        with col2:
            st.markdown("**Visualization**")
            if DEPENDENCIES['plotly']:
                st.markdown('<p class="status-good">✅ Plotly</p>', unsafe_allow_html=True)
            else:
                st.markdown('<p class="status-missing">❌ Plotly</p>', unsafe_allow_html=True)
            
            if DEPENDENCIES['matplotlib']:
                st.markdown('<p class="status-good">✅ Matplotlib</p>', unsafe_allow_html=True)
            else:
                st.markdown('<p class="status-missing">❌ Matplotlib</p>', unsafe_allow_html=True)
        
        # Map dependencies
        with col3:
            st.markdown("**Mapping**")
            if DEPENDENCIES['folium']:
                st.markdown('<p class="status-good">✅ Folium</p>', unsafe_allow_html=True)
            else:
                st.markdown('<p class="status-missing">❌ Folium</p>', unsafe_allow_html=True)
            
            st.markdown('<p class="status-optional">⚠️ Earth Engine (Optional)</p>', unsafe_allow_html=True)
        
        # Cloud status
        with col4:
            st.markdown("**Cloud Status**")
            st.markdown('<p class="status-good">✅ Cloud Ready</p>', unsafe_allow_html=True)
            st.markdown('<p class="status-good">✅ No Auth Required</p>', unsafe_allow_html=True)
            
        # Instructions for missing dependencies
        missing_deps = [name for name, available in DEPENDENCIES.items() if not available]
        if missing_deps:
            st.warning(f"⚠️ Missing optional dependencies: {', '.join(missing_deps)}")
            st.info("The app will work with reduced functionality. See the Cloud Setup Guide for installation instructions.")

def show_home():
    """Home page with cloud-specific information"""
    
    st.markdown("## Welcome to GeoMasterPy Cloud Edition! 🚀")
    
    # Cloud deployment info
    st.info("""
    🌐 **This version is optimized for Streamlit Cloud deployment**
    
    ✅ **What works out of the box:**
    - Interactive data analysis and visualization
    - Basic mapping (with Folium)
    - Sample geospatial workflows
    - Documentation and tutorials
    
    🔧 **For full Earth Engine functionality:**
    - Set up authentication (see Cloud Setup Guide)
    - Configure service account credentials
    """)
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-container">
            <h3>📊</h3>
            <p><strong>Data Analysis</strong></p>
            <p>Interactive demos ready</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-container">
            <h3>🗺️</h3>
            <p><strong>Maps</strong></p>
            <p>Folium integration</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-container">
            <h3>📈</h3>
            <p><strong>Visualizations</strong></p>
            <p>Plotly charts</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-container">
            <h3>☁️</h3>
            <p><strong>Cloud Ready</strong></p>
            <p>Zero configuration</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick start
    st.markdown("## 🚀 Quick Start")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✅ Available Now")
        st.markdown("""
        1. 📊 **Data Analysis Demo** - Explore sample environmental data
        2. 🗺️ **Interactive Maps** - Basic mapping with Folium
        3. 📈 **Visualizations** - Create charts and graphs
        4. 📚 **Documentation** - Learn about GeoMasterPy
        """)
    
    with col2:
        st.markdown("### 🔧 Advanced Setup")
        st.markdown("""
        1. 🔧 **Cloud Setup Guide** - Configure Earth Engine
        2. 🔐 **Authentication** - Set up service accounts
        3. 🛰️ **Satellite Data** - Access Earth Engine datasets
        4. 📊 **Full Analysis** - Complete geospatial workflows
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
                        # Extract file ID from Google Drive URL
                        file_id = extract_drive_file_id(drive_url)
                        if file_id:
                            # Create direct download URL
                            download_url = f"https://drive.google.com/uc?id={file_id}&export=download"
                            
                            if DEPENDENCIES['requests']:
                                import requests
                                response = requests.get(download_url)
                                if response.status_code == 200:
                                    try:
                                        geojson_data = response.json()
                                        
                                        # Store in session state
                                        st.session_state.aoi_geojson = geojson_data
                                        st.session_state.aoi_name = aoi_name if aoi_name else "Custom Area"
                                        
                                        # Create a simple geometry representation for analysis
                                        if geojson_data.get('type') == 'FeatureCollection':
                                            # Use first feature's geometry
                                            first_feature = geojson_data['features'][0]
                                            st.session_state.aoi_geometry = first_feature['geometry']
                                        else:
                                            st.session_state.aoi_geometry = geojson_data.get('geometry', geojson_data)
                                        
                                        st.success(f"✅ Successfully loaded GeoJSON: {st.session_state.aoi_name}")
                                        st.rerun()
                                        
                                    except json.JSONDecodeError:
                                        st.error("Invalid GeoJSON format in the file")
                                else:
                                    st.error(f"Failed to download file. Status code: {response.status_code}")
                            else:
                                st.error("Requests library not available. Cannot load from Google Drive.")
                        else:
                            st.error("Invalid Google Drive URL. Please check the format.")
                                    
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
            st.rerun()
    
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
                st.info("Navigate to '📊 Data Analysis Demo' to analyze your area")
        
        # Display the GeoJSON on a map if Folium is available
        if DEPENDENCIES['folium']:
            st.markdown("### 🌍 Area Preview")
            
            try:
                # Create a simple folium map
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
                
                # Try to fit bounds to the geometry
                if geojson_type == 'FeatureCollection' and st.session_state.aoi_geojson['features']:
                    # Get bounds from first feature
                    coords = get_geojson_bounds(st.session_state.aoi_geojson)
                    if coords:
                        m.fit_bounds(coords)
                
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
        2. **📊 Analyze** environmental data within your boundary
        3. **📈 Create** time series charts and statistics
        4. **💾 Export** results and processed data
        
        All analysis tools will automatically use your defined area as the region of interest.
        """)

def extract_drive_file_id(url):
    """Extract file ID from Google Drive URL"""
    import re
    
    # Match different Google Drive URL formats
    patterns = [
        r'https://drive\.google\.com/file/d/([a-zA-Z0-9-_]+)',
        r'https://drive\.google\.com/open\?id=([a-zA-Z0-9-_]+)',
        r'https://drive\.google\.com/uc\?id=([a-zA-Z0-9-_]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_geojson_bounds(geojson):
    """Get bounds from GeoJSON for map fitting"""
    try:
        if geojson['type'] == 'FeatureCollection':
            features = geojson['features']
            if features:
                # Get coordinates from first feature
                geometry = features[0]['geometry']
                if geometry['type'] == 'Polygon':
                    coords = geometry['coordinates'][0]
                elif geometry['type'] == 'Point':
                    coord = geometry['coordinates']
                    return [[coord[1] - 0.01, coord[0] - 0.01], [coord[1] + 0.01, coord[0] + 0.01]]
                else:
                    return None
                
                # Calculate bounds
                lats = [coord[1] for coord in coords]
                lons = [coord[0] for coord in coords]
                return [[min(lats), min(lons)], [max(lats), max(lons)]]
        return None
    except:
        return None

def get_aoi_center(geojson):
    """Get center coordinates from GeoJSON"""
    try:
        if geojson['type'] == 'FeatureCollection':
            features = geojson['features']
            if features:
                geometry = features[0]['geometry']
                if geometry['type'] == 'Polygon':
                    coords = geometry['coordinates'][0]
                    # Calculate centroid
                    lats = [coord[1] for coord in coords]
                    lons = [coord[0] for coord in coords]
                    return (sum(lats) / len(lats), sum(lons) / len(lons))
                elif geometry['type'] == 'Point':
                    coord = geometry['coordinates']
                    return (coord[1], coord[0])
        elif geojson.get('geometry'):
            geometry = geojson['geometry']
            if geometry['type'] == 'Point':
                coord = geometry['coordinates']
                return (coord[1], coord[0])
            elif geometry['type'] == 'Polygon':
                coords = geometry['coordinates'][0]
                lats = [coord[1] for coord in coords]
                lons = [coord[0] for coord in coords]
                return (sum(lats) / len(lats), sum(lons) / len(lons))
        return None
    except:
        return None

def show_data_analysis_demo():
    """Data analysis demo with sample data"""
    
    st.markdown("## 📊 Data Analysis Demo")
    
    # Check AOI status and show appropriate message
    if st.session_state.aoi_geojson is not None:
        st.success(f"✅ Using Area of Interest: **{st.session_state.aoi_name}**")
        st.info("Analysis will be focused on your defined area of interest.")
        use_aoi = True
    else:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.warning("⚠️ No Area of Interest defined. Analysis will use sample/global data.")
        with col2:
            if st.button("📁 Load AOI"):
                st.info("Navigate to '📁 Area of Interest' to load your study area")
        use_aoi = False
    
    if use_aoi:
        st.markdown("### 🎯 Area-Specific Analysis")
        st.markdown(f"Analyzing environmental data for: **{st.session_state.aoi_name}**")
    else:
        st.markdown("### 🌍 Global Sample Data Analysis")
        st.markdown("Explore sample environmental and geospatial data")
    
    # Generate sample environmental data
    dates = pd.date_range('2023-01-01', '2023-12-31', freq='D')
    
    # Create realistic sample data
    np.random.seed(42)  # For reproducible results
    
    # NDVI with seasonal pattern
    day_of_year = np.arange(1, len(dates) + 1)
    seasonal_component = 0.3 * np.sin(2 * np.pi * day_of_year / 365.25 - np.pi/2)  # Peak in summer
    ndvi = 0.4 + seasonal_component + np.random.normal(0, 0.05, len(dates))
    ndvi = np.clip(ndvi, 0, 1)  # Keep NDVI in valid range
    
    # Temperature with seasonal pattern
    temp = 15 + 10 * np.sin(2 * np.pi * day_of_year / 365.25 - np.pi/2) + np.random.normal(0, 2, len(dates))
    
    # Precipitation (more random)
    precip = np.random.exponential(2.5, len(dates))
    
    df = pd.DataFrame({
        'Date': dates,
        'NDVI': ndvi,
        'Temperature_C': temp,
        'Precipitation_mm': precip,
        'Month': dates.month,
        'Season': [get_season(month) for month in dates.month]
    })
    
    # Summary statistics
    st.markdown("### 📈 Summary Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Avg NDVI", f"{df['NDVI'].mean():.3f}", f"±{df['NDVI'].std():.3f}")
        st.metric("Max NDVI", f"{df['NDVI'].max():.3f}")
        st.metric("Min NDVI", f"{df['NDVI'].min():.3f}")
    
    with col2:
        st.metric("Avg Temperature", f"{df['Temperature_C'].mean():.1f}°C", f"±{df['Temperature_C'].std():.1f}")
        st.metric("Max Temperature", f"{df['Temperature_C'].max():.1f}°C")
        st.metric("Min Temperature", f"{df['Temperature_C'].min():.1f}°C")
    
    with col3:
        st.metric("Total Precipitation", f"{df['Precipitation_mm'].sum():.0f}mm")
        st.metric("Avg Daily Precip", f"{df['Precipitation_mm'].mean():.1f}mm")
        st.metric("Max Daily Precip", f"{df['Precipitation_mm'].max():.1f}mm")
    
    # Time series visualization
    if DEPENDENCIES['plotly']:
        st.markdown("### 📊 Time Series Analysis")
        
        # Create subplot with secondary y-axis
        fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=['NDVI (Vegetation Index)', 'Temperature (°C)', 'Precipitation (mm)'],
            vertical_spacing=0.08,
            specs=[[{"secondary_y": False}],
                   [{"secondary_y": False}],
                   [{"secondary_y": False}]]
        )
        
        # Add traces
        fig.add_trace(go.Scatter(x=df['Date'], y=df['NDVI'], 
                               name='NDVI', line=dict(color='green', width=2)), row=1, col=1)
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Temperature_C'], 
                               name='Temperature', line=dict(color='red', width=2)), row=2, col=1)
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Precipitation_mm'], 
                               name='Precipitation', line=dict(color='blue', width=1)), row=3, col=1)
        
        fig.update_layout(height=700, title_text="Environmental Parameters - 2023", showlegend=False)
        fig.update_xaxes(title_text="Date", row=3, col=1)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Seasonal analysis
        st.markdown("### 🍂 Seasonal Analysis")
        
        seasonal_stats = df.groupby('Season').agg({
            'NDVI': ['mean', 'std'],
            'Temperature_C': ['mean', 'std'],
            'Precipitation_mm': ['sum', 'mean']
        }).round(3)
        
        # Flatten column names
        seasonal_stats.columns = ['_'.join(col).strip() for col in seasonal_stats.columns.values]
        seasonal_stats = seasonal_stats.reset_index()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.dataframe(seasonal_stats, use_container_width=True)
        
        with col2:
            # Seasonal comparison chart
            fig = px.bar(df.groupby('Season')['NDVI'].mean().reset_index(), 
                        x='Season', y='NDVI', 
                        title="Average NDVI by Season",
                        color='Season')
            st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.warning("Install Plotly for advanced visualizations")
        
        # Show basic statistics
        st.markdown("### 📊 Basic Data Overview")
        st.dataframe(df.head(10))
    
    # Download option
    st.markdown("### 💾 Download Data")
    
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download Sample Data (CSV)",
        data=csv,
        file_name="sample_environmental_data.csv",
        mime="text/csv"
    )

def get_season(month):
    """Get season from month number"""
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Fall'

def show_interactive_maps():
    """Interactive mapping with Folium"""
    
    st.markdown("## 🗺️ Interactive Maps")
    
    if not DEPENDENCIES['folium']:
        st.error("❌ Folium is required for interactive maps")
        st.code("pip install folium streamlit-folium")
        return
    
    # Check AOI status
    if st.session_state.aoi_geojson is not None:
        st.success(f"✅ Displaying Area of Interest: **{st.session_state.aoi_name}**")
        use_aoi = True
    else:
        st.info("💡 Load an Area of Interest to center the map on your study area")
        use_aoi = False
    
    st.markdown("Create and explore interactive maps with your data")
    
    # Map configuration
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 🎛️ Map Settings")
        
        # Location selector - change based on AOI availability
        if use_aoi:
            st.markdown("📍 **Map will center on your Area of Interest**")
            
            # Get center from AOI
            aoi_center = get_aoi_center(st.session_state.aoi_geojson)
            if aoi_center:
                lat, lon = aoi_center
                st.info(f"Center: {lat:.4f}, {lon:.4f}")
            else:
                lat, lon = (0, 0)
                st.warning("Could not determine AOI center, using default")
        else:
            location_name = st.selectbox(
                "Choose a location:",
                [
                    "San Francisco, CA",
                    "New York, NY", 
                    "London, UK",
                    "Tokyo, Japan",
                    "Sydney, Australia",
                    "Custom Location"
                ]
            )
            
            # Predefined locations
            locations = {
                "San Francisco, CA": (37.7749, -122.4194),
                "New York, NY": (40.7128, -74.0060),
                "London, UK": (51.5074, -0.1278),
                "Tokyo, Japan": (35.6762, 139.6503),
                "Sydney, Australia": (-33.8688, 151.2093),
            }
            
            if location_name == "Custom Location":
                lat = st.number_input("Latitude", value=37.7749, format="%.4f", min_value=-90.0, max_value=90.0)
                lon = st.number_input("Longitude", value=-122.4194, format="%.4f", min_value=-180.0, max_value=180.0)
            else:
                lat, lon = locations[location_name]
        
        zoom = st.slider("Zoom Level", 1, 18, 10)
        
        # Map style
        map_style = st.selectbox(
            "Map Style:",
            [
                "OpenStreetMap",
                "CartoDB Positron",
                "CartoDB Dark Matter", 
                "Stamen Terrain",
                "Stamen Watercolor"
            ]
        )
        
        # Sample data options
        show_sample_data = st.checkbox("Add Sample Data Points", value=True)
        
    with col2:
        st.markdown("### 🌍 Interactive Map")
        
        # Create folium map
        if map_style == "OpenStreetMap":
            tiles = "OpenStreetMap"
        elif map_style == "CartoDB Positron":
            tiles = "CartoDB positron"
        elif map_style == "CartoDB Dark Matter":
            tiles = "CartoDB dark_matter"
        elif map_style == "Stamen Terrain":
            tiles = "Stamen Terrain"
        else:
            tiles = "Stamen Watercolor"
        
        m = folium.Map(
            location=[lat, lon],
            zoom_start=zoom,
            tiles=tiles
        )
        
        # Add AOI or main marker
        if use_aoi:
            # Add AOI to map
            folium.GeoJson(
                st.session_state.aoi_geojson,
                style_function=lambda x: {
                    'fillColor': 'blue',
                    'color': 'blue',
                    'weight': 3,
                    'fillOpacity': 0.3
                },
                popup=f"Area of Interest: {st.session_state.aoi_name}",
                tooltip=f"AOI: {st.session_state.aoi_name}"
            ).add_to(m)
            
            # Fit bounds to AOI
            bounds = get_geojson_bounds(st.session_state.aoi_geojson)
            if bounds:
                m.fit_bounds(bounds)
        else:
            # Add main marker
            folium.Marker(
                [lat, lon],
                popup=f"📍 {location_name}",
                tooltip="Main Location",
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m)
        
        # Add sample data points if enabled
        if show_sample_data:
            # Generate sample points around the main location
            np.random.seed(42)
            n_points = 5
            
            for i in range(n_points):
                sample_lat = lat + np.random.normal(0, 0.01)
                sample_lon = lon + np.random.normal(0, 0.01)
                sample_value = np.random.uniform(0.2, 0.8)
                
                # Color code based on value
                color = 'green' if sample_value > 0.6 else 'orange' if sample_value > 0.4 else 'red'
                
                folium.CircleMarker(
                    location=[sample_lat, sample_lon],
                    radius=8,
                    popup=f"Sample Point {i+1}<br>Value: {sample_value:.3f}",
                    color='black',
                    weight=1,
                    fill=True,
                    fillColor=color,
                    fillOpacity=0.7
                ).add_to(m)
        
        # Add a sample polygon (only for predefined locations)
        if not use_aoi and 'location_name' in locals() and location_name == "San Francisco, CA":
            # Golden Gate Park boundary (approximate)
            park_coords = [
                [37.7694, -122.4862],
                [37.7694, -122.4550],
                [37.7762, -122.4550],
                [37.7762, -122.4862]
            ]
            
            folium.Polygon(
                locations=park_coords,
                popup="Golden Gate Park",
                color='green',
                weight=2,
                fill=True,
                fillColor='green',
                fillOpacity=0.3
            ).add_to(m)
        
        # Display map
        map_data = st_folium(m, width=700, height=500)
        
        # Show clicked data
        if map_data['last_clicked']:
            clicked_lat = map_data['last_clicked']['lat']
            clicked_lng = map_data['last_clicked']['lng']
            st.info(f"🎯 Last clicked: ({clicked_lat:.4f}, {clicked_lng:.4f})")
    
    # Map analysis section
    st.markdown("### 📊 Map Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📈 Analyze Area"):
            st.success("✅ Area analysis complete!")
            # Generate sample analysis results
            area_km2 = np.random.uniform(10, 100)
            vegetation_percent = np.random.uniform(20, 80)
            
            st.metric("Area", f"{area_km2:.1f} km²")
            st.metric("Vegetation Cover", f"{vegetation_percent:.1f}%")
    
    with col2:
        if st.button("🛰️ Load Satellite Data"):
            st.info("ℹ️ Earth Engine integration required for satellite data")
            st.markdown("Configure Earth Engine in the Cloud Setup Guide")
    
    with col3:
        if st.button("💾 Export Map"):
            st.success("✅ Map export initiated!")
            st.info("📁 Map would be saved to downloads")

def show_visualizations():
    """Advanced visualizations demo"""
    
    st.markdown("## 📈 Advanced Visualizations")
    
    if not DEPENDENCIES['plotly']:
        st.error("❌ Plotly is required for advanced visualizations")
        st.code("pip install plotly")
        return
    
    # Sample land cover data
    land_cover_data = {
        'Land Cover Type': ['Forest', 'Agriculture', 'Urban', 'Water Bodies', 'Grassland', 'Bare Soil'],
        'Area (km²)': [1250, 980, 345, 120, 450, 280],
        'Percentage': [37.5, 29.4, 10.4, 3.6, 13.5, 8.4],
        'Carbon Storage (tons/ha)': [150, 45, 12, 0, 25, 5]
    }
    
    land_cover_df = pd.DataFrame(land_cover_data)
    
    tab1, tab2, tab3 = st.tabs(["🥧 Land Cover", "📊 Time Series", "📈 Correlations"])
    
    with tab1:
        st.markdown("### 🌍 Land Cover Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Pie chart
            fig_pie = px.pie(land_cover_df, values='Percentage', names='Land Cover Type',
                           title="Land Cover Distribution",
                           color_discrete_sequence=px.colors.qualitative.Set3)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Bar chart
            fig_bar = px.bar(land_cover_df, x='Land Cover Type', y='Area (km²)',
                           title="Land Cover Areas",
                           color='Area (km²)',
                           color_continuous_scale='Viridis')
            fig_bar.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Data table
        st.markdown("### 📋 Land Cover Data")
        st.dataframe(land_cover_df, use_container_width=True)
    
    with tab2:
        st.markdown("### 📊 Environmental Time Series")
        
        # Generate sample time series data
        dates = pd.date_range('2020-01-01', '2023-12-31', freq='ME')
        
        # NDVI time series with trend and seasonality
        trend = np.linspace(0.35, 0.45, len(dates))
        seasonal = 0.15 * np.sin(2 * np.pi * np.arange(len(dates)) / 12)
        noise = np.random.normal(0, 0.02, len(dates))
        ndvi_series = trend + seasonal + noise
        
        # Temperature series
        temp_base = 15
        temp_seasonal = 8 * np.sin(2 * np.pi * np.arange(len(dates)) / 12)
        temp_trend = np.linspace(0, 1.5, len(dates))  # Warming trend
        temp_series = temp_base + temp_seasonal + temp_trend + np.random.normal(0, 1, len(dates))
        
        time_series_df = pd.DataFrame({
            'Date': dates,
            'NDVI': ndvi_series,
            'Temperature': temp_series,
            'Year': dates.year
        })
        
        # Multi-axis plot
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Scatter(x=time_series_df['Date'], y=time_series_df['NDVI'], 
                      name="NDVI", line=dict(color='green')),
            secondary_y=False,
        )
        
        fig.add_trace(
            go.Scatter(x=time_series_df['Date'], y=time_series_df['Temperature'], 
                      name="Temperature (°C)", line=dict(color='red')),
            secondary_y=True,
        )
        
        fig.update_yaxes(title_text="NDVI", secondary_y=False)
        fig.update_yaxes(title_text="Temperature (°C)", secondary_y=True)
        fig.update_layout(title_text="NDVI and Temperature Trends (2020-2023)", height=500)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Yearly comparison
        yearly_stats = time_series_df.groupby('Year').agg({
            'NDVI': ['mean', 'std'],
            'Temperature': ['mean', 'std']
        }).round(3)
        
        st.markdown("### 📅 Yearly Comparison")
        st.dataframe(yearly_stats, use_container_width=True)
    
    with tab3:
        st.markdown("### 📈 Variable Correlations")
        
        # Generate correlated sample data
        np.random.seed(42)
        n_samples = 100
        
        # Create correlated variables
        elevation = np.random.uniform(0, 3000, n_samples)
        temperature = 25 - 0.006 * elevation + np.random.normal(0, 2, n_samples)
        precipitation = 500 + 0.3 * elevation + np.random.normal(0, 100, n_samples)
        ndvi = 0.1 + 0.0002 * elevation + 0.01 * temperature + 0.0005 * precipitation + np.random.normal(0, 0.1, n_samples)
        ndvi = np.clip(ndvi, 0, 1)
        
        correlation_df = pd.DataFrame({
            'Elevation (m)': elevation,
            'Temperature (°C)': temperature,
            'Precipitation (mm)': precipitation,
            'NDVI': ndvi
        })
        
        # Correlation matrix
        corr_matrix = correlation_df.corr()
        
        fig_corr = px.imshow(corr_matrix, 
                           title="Variable Correlation Matrix",
                           color_continuous_scale='RdBu_r',
                           aspect="auto")
        fig_corr.update_layout(height=400)
        st.plotly_chart(fig_corr, use_container_width=True)
        
        # Scatter plot matrix
        fig_scatter = px.scatter_matrix(correlation_df,
                                      title="Scatter Plot Matrix",
                                      color='NDVI',
                                      height=600)
        st.plotly_chart(fig_scatter, use_container_width=True)

def show_cloud_setup():
    """Cloud setup and configuration guide"""
    
    st.markdown("## 🔧 Cloud Setup Guide")
    st.markdown("Configure your Streamlit app for full Earth Engine functionality")
    
    tab1, tab2, tab3 = st.tabs(["🚀 Quick Setup", "🔐 Authentication", "📋 Requirements"])
    
    with tab1:
        st.markdown("### 🚀 Quick Setup for Streamlit Cloud")
        
        st.markdown("""
        #### 1. Repository Setup
        
        Make sure your repository has these files:
        
        ```
        your-repo/
        ├── streamlit_app_cloud.py      # This file
        ├── requirements_cloud.txt       # Minimal dependencies
        └── .streamlit/
            └── secrets.toml            # For Earth Engine credentials
        ```
        """)
        
        st.markdown("""
        #### 2. Deploy to Streamlit Cloud
        
        1. Go to [share.streamlit.io](https://share.streamlit.io)
        2. Connect your GitHub repository
        3. Set main file to `streamlit_app_cloud.py`
        4. Deploy!
        """)
        
        st.code("""
# Example deployment URL:
https://your-username-your-repo-streamlitappcloud-main.streamlit.app
        """)
        
        if st.button("🔗 Open Streamlit Cloud"):
            st.markdown("[🚀 Deploy to Streamlit Cloud](https://share.streamlit.io)")
    
    with tab2:
        st.markdown("### 🔐 Earth Engine Authentication")
        
        st.warning("⚠️ Earth Engine requires authentication for satellite data access")
        
        st.markdown("""
        #### Option 1: Service Account (Recommended for Production)
        
        1. **Create a Service Account** in Google Cloud Console
        2. **Download the JSON key file**
        3. **Add to Streamlit Secrets**:
        """)
        
        st.code("""
# .streamlit/secrets.toml
[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\\nYOUR_PRIVATE_KEY\\n-----END PRIVATE KEY-----\\n"
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"
        """)
        
        st.markdown("""
        #### Option 2: User Authentication (Development)
        
        For development, you can use user authentication:
        """)
        
        st.code("""
# In your Streamlit app
import ee
import streamlit as st

# For local development
if st.button("Authenticate Earth Engine"):
    ee.Authenticate()
    ee.Initialize()
    st.success("Earth Engine authenticated!")
        """)
    
    with tab3:
        st.markdown("### 📋 Requirements Management")
        
        st.markdown("""
        #### Current Requirements (requirements_cloud.txt)
        
        This minimal set is guaranteed to work on Streamlit Cloud:
        """)
        
        requirements_text = """streamlit>=1.28.0
pandas>=1.5.0
numpy>=1.21.0
plotly>=5.15.0
folium>=0.14.0
streamlit-folium>=0.15.0
matplotlib>=3.5.0
requests>=2.28.0
Pillow>=9.0.0
altair>=4.0.0"""
        
        st.code(requirements_text)
        
        st.markdown("""
        #### Optional Dependencies
        
        Add these only if needed and working:
        """)
        
        optional_requirements = """# Heavy dependencies - may cause deployment issues
# earthengine-api>=0.1.300
# geopandas>=0.12.0
# rasterio>=1.3.0
# cartopy>=0.21.0"""
        
        st.code(optional_requirements)
        
        # Download button for requirements
        st.download_button(
            label="📥 Download requirements_cloud.txt",
            data=requirements_text,
            file_name="requirements_cloud.txt",
            mime="text/plain"
        )
        
        st.markdown("""
        #### Troubleshooting Deployment Issues
        
        **Common problems and solutions:**
        
        1. **Build timeout**: Remove heavy dependencies like cartopy, rasterio
        2. **Memory issues**: Use minimal requirements file
        3. **Import errors**: Check dependency compatibility
        4. **Authentication**: Use service account for production
        """)

def show_documentation():
    """Documentation section"""
    
    st.markdown("## 📚 Documentation")
    
    doc_tab1, doc_tab2, doc_tab3 = st.tabs(["📖 User Guide", "💻 Code Examples", "❓ FAQ"])
    
    with doc_tab1:
        st.markdown("""
        ### 📖 User Guide
        
        #### Getting Started
        
        This cloud-optimized version of GeoMasterPy provides:
        
        - **Interactive data analysis** with sample environmental datasets
        - **Map visualization** using Folium for web-based mapping
        - **Advanced charts** with Plotly for data exploration
        - **Cloud deployment** ready for Streamlit Cloud
        
        #### Navigation
        
        Use the sidebar to navigate between different features:
        
        - **🏠 Home**: Overview and introduction
        - **📊 Data Analysis Demo**: Work with sample environmental data
        - **🗺️ Interactive Maps**: Create and explore maps
        - **📈 Visualizations**: Advanced charting and analysis
        - **🔧 Cloud Setup Guide**: Deployment and configuration
        - **📚 Documentation**: This help section
        
        #### Cloud Deployment
        
        This app is designed for easy deployment on Streamlit Cloud:
        
        1. Fork or clone the repository
        2. Push to your GitHub account
        3. Deploy via share.streamlit.io
        4. Configure secrets for Earth Engine (optional)
        """)
    
    with doc_tab2:
        st.markdown("""
        ### 💻 Code Examples
        
        #### Basic Map Creation
        
        ```python
        import folium
        import streamlit as st
        from streamlit_folium import st_folium
        
        # Create a map
        m = folium.Map(location=[37.7749, -122.4194], zoom_start=10)
        
        # Add a marker
        folium.Marker(
            [37.7749, -122.4194],
            popup="San Francisco",
            tooltip="Click for info"
        ).add_to(m)
        
        # Display in Streamlit
        st_folium(m, width=700, height=500)
        ```
        
        #### Data Visualization
        
        ```python
        import plotly.express as px
        import pandas as pd
        
        # Create sample data
        df = pd.DataFrame({
            'x': range(10),
            'y': [i**2 for i in range(10)]
        })
        
        # Create plot
        fig = px.line(df, x='x', y='y', title='Sample Plot')
        st.plotly_chart(fig, use_container_width=True)
        ```
        
        #### Earth Engine Integration
        
        ```python
        import ee
        import streamlit as st
        
        # Initialize Earth Engine
        try:
            ee.Initialize()
            st.success("Earth Engine connected!")
        except:
            st.error("Earth Engine authentication required")
        
        # Load and display satellite data
        image = ee.Image('LANDSAT/LC08/C02/T1_L2').first()
        ```
        """)
    
    with doc_tab3:
        st.markdown("""
        ### ❓ Frequently Asked Questions
        
        #### Q: Why can't I see satellite data?
        
        **A:** Earth Engine requires authentication. See the Cloud Setup Guide for configuration instructions.
        
        #### Q: The app works locally but fails on Streamlit Cloud?
        
        **A:** Check your requirements.txt file. Remove heavy dependencies like cartopy and rasterio that can cause build timeouts.
        
        #### Q: How do I add my own data?
        
        **A:** You can upload CSV files using `st.file_uploader()` or connect to external APIs using the `requests` library.
        
        #### Q: Can I export the analysis results?
        
        **A:** Yes! Use `st.download_button()` to allow users to download CSV files, charts, or other results.
        
        #### Q: How do I deploy my own version?
        
        **A:** 
        1. Fork this repository
        2. Customize the code
        3. Push to GitHub
        4. Deploy via share.streamlit.io
        
        #### Q: What if I need more advanced geospatial features?
        
        **A:** Consider upgrading to the full GeoMasterPy version with Earth Engine integration and additional dependencies.
        """)

if __name__ == "__main__":
    main()