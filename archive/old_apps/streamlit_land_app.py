"""
GeoMasterPy Land App - Modern Land Management Interface

A beautiful, Land App-inspired interface for geospatial analysis with a streamlined
workflow: Upload/Draw → Analyze.
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
import requests
from datetime import datetime, date
import base64
from io import BytesIO
import tempfile
import os

# Configure Streamlit page - MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="GeoMasterPy Land App",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"  # Start with collapsed sidebar for clean look
)

# Import dependencies with error handling
try:
    import folium
    from streamlit_folium import st_folium
    FOLIUM_AVAILABLE = True
except ImportError:
    FOLIUM_AVAILABLE = False

try:
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

try:
    import geopandas as gpd
    import shapely.geometry as geom
    GEOPANDAS_AVAILABLE = True
except ImportError:
    GEOPANDAS_AVAILABLE = False

# Import GeoMasterPy and geemap
try:
    import geomasterpy as gmp
    GEOMASTERPY_AVAILABLE = True
except ImportError:
    GEOMASTERPY_AVAILABLE = False

try:
    import ee
    EE_AVAILABLE = True
except ImportError:
    EE_AVAILABLE = False

# Custom CSS for Land App styling
st.markdown("""
<style>
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    
    /* Land App Header Styling */
    .land-app-header {
        background: white;
        border-bottom: 1px solid #e0e0e0;
        padding: 1rem 2rem;
        margin: -1rem -1rem 1rem -1rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .logo-section {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .logo-icon {
        width: 32px;
        height: 32px;
        background: #4CAF50;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 18px;
        font-weight: bold;
    }
    
    .app-title {
        font-size: 18px;
        font-weight: 600;
        color: #333;
    }
    
    .header-subtitle {
        flex: 1;
        text-align: center;
        color: #666;
        font-size: 14px;
    }
    
    .header-actions {
        display: flex;
        gap: 15px;
        align-items: center;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background: white;
        border-bottom: 1px solid #e0e0e0;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background: none;
        border: none;
        color: #666;
        font-size: 16px;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        color: #4CAF50;
        border-bottom: 2px solid #4CAF50;
    }
    
    /* Mapping view styling */
    .map-controls {
        background: white;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    /* Analytics cards */
    .analytics-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #4CAF50;
    }
    
    .metric-card {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        margin: 0.5rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 600;
        color: #4CAF50;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        color: #666;
        font-size: 0.9rem;
    }
    
    /* Status indicators */
    .status-success {
        background: #e8f5e9;
        color: #4CAF50;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    .status-warning {
        background: #fff3e0;
        color: #ff9800;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    /* Drawing tools */
    .drawing-tools {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
        margin: 1rem 0;
    }
    
    .tool-button {
        background: white;
        border: 1px solid #ddd;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .tool-button:hover {
        background: #f5f5f5;
        border-color: #4CAF50;
    }
    
    .tool-button.active {
        background: #4CAF50;
        color: white;
        border-color: #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application with Land App-style interface"""
    
    # Initialize session state
    if 'selected_area' not in st.session_state:
        st.session_state.selected_area = None
    if 'area_geojson' not in st.session_state:
        st.session_state.area_geojson = None
    if 'area_name' not in st.session_state:
        st.session_state.area_name = "My Farm"
    if 'area_center' not in st.session_state:
        st.session_state.area_center = [51.5074, -0.1278]  # Default to London
    
    # Land App Header
    render_header()
    
    # Main content with tabs
    tab1, tab2 = st.tabs(["🗺️ Mapping View", "📊 Analytics View"])
    
    with tab1:
        render_mapping_view()
    
    with tab2:
        render_analytics_view()

def render_header():
    """Render the Land App-style header"""
    
    st.markdown("""
    <div class="land-app-header">
        <div class="logo-section">
            <div class="logo-icon">🌱</div>
            <div class="app-title">GeoMasterPy Land App</div>
        </div>
        <div class="header-subtitle">
            Interactive Land Management & Environmental Analysis Platform
        </div>
        <div class="header-actions">
            <span style="color: #666;">🌍 Global Analysis Ready</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_mapping_view():
    """Render the mapping interface for uploading/drawing areas"""
    
    st.markdown("## 🗺️ Define Your Land Area")
    st.markdown("Upload a GeoJSON file or draw your farm boundary to get started with analysis.")
    
    # Create two columns for controls and map
    col1, col2 = st.columns([1, 2])
    
    with col1:
        render_mapping_controls()
    
    with col2:
        render_interactive_map()

def render_mapping_controls():
    """Render the mapping controls panel"""
    
    st.markdown("""
    <div class="map-controls">
        <h4 style="margin-top: 0;">📁 Upload Area</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Area name input
    area_name = st.text_input(
        "Area name:",
        value=st.session_state.area_name,
        placeholder="e.g., Smith Farm, North Field, etc."
    )
    st.session_state.area_name = area_name
    
    # File upload method
    upload_method = st.radio(
        "How would you like to define your area?",
        ["📤 Upload GeoJSON file", "🔗 Load from Google Drive URL", "✏️ Draw on map"],
        horizontal=True
    )
    
    if upload_method == "📤 Upload GeoJSON file":
        handle_file_upload()
    elif upload_method == "🔗 Load from Google Drive URL":
        handle_drive_url()
    else:
        handle_map_drawing()
    
    # Show current area status
    render_area_status()

def handle_file_upload():
    """Handle direct file upload"""
    
    uploaded_file = st.file_uploader(
        "Choose a GeoJSON file",
        type=['geojson', 'json'],
        help="Upload a GeoJSON file containing your land boundary"
    )
    
    if uploaded_file is not None:
        try:
            # Read the uploaded file
            geojson_data = json.load(uploaded_file)
            
            # Validate GeoJSON
            if validate_geojson(geojson_data):
                st.session_state.area_geojson = geojson_data
                st.session_state.area_center = get_geojson_center(geojson_data)
                st.success(f"✅ Successfully loaded: {st.session_state.area_name}")
            else:
                st.error("❌ Invalid GeoJSON format")
                
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")

def handle_drive_url():
    """Handle Google Drive URL loading"""
    
    drive_url = st.text_input(
        "Google Drive sharing URL:",
        placeholder="https://drive.google.com/file/d/YOUR_FILE_ID/view?usp=sharing",
        help="Paste the sharing URL of your GeoJSON file from Google Drive"
    )
    
    if st.button("🔄 Load from Drive"):
        if drive_url:
            with st.spinner("Loading GeoJSON from Google Drive..."):
                try:
                    if GEOMASTERPY_AVAILABLE:
                        from geomasterpy.data.catalog import (
                            validate_drive_url, 
                            load_geojson_from_drive_url
                        )
                        
                        if validate_drive_url(drive_url):
                            geojson_data = load_geojson_from_drive_url(drive_url)
                            if geojson_data:
                                st.session_state.area_geojson = geojson_data
                                st.session_state.area_center = get_geojson_center(geojson_data)
                                st.success(f"✅ Successfully loaded: {st.session_state.area_name}")
                            else:
                                st.error("Failed to load GeoJSON from Drive")
                        else:
                            st.error("Invalid Google Drive URL format")
                    else:
                        st.error("GeoMasterPy not available for Drive integration")
                        
                except Exception as e:
                    st.error(f"Error loading from Drive: {str(e)}")
        else:
            st.warning("Please enter a Google Drive URL")

def handle_map_drawing():
    """Handle drawing on map"""
    
    st.markdown("""
    <div class="drawing-tools">
        <div class="tool-button">✏️ Draw Polygon</div>
        <div class="tool-button">⬜ Draw Rectangle</div>
        <div class="tool-button">📏 Measure</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 Use the drawing tools on the map to define your area")
    st.markdown("**Instructions:**")
    st.markdown("""
    1. Click the drawing tools in the map
    2. Draw your farm boundary
    3. The area will be automatically calculated
    4. Switch to Analytics View to analyze your land
    """)

def render_area_status():
    """Show current area status"""
    
    st.markdown("---")
    st.markdown("**📍 Current Area Status**")
    
    if st.session_state.area_geojson:
        area_ha = calculate_area_hectares(st.session_state.area_geojson)
        
        st.markdown(f"""
        <div class="status-success">
            ✅ {st.session_state.area_name} loaded ({area_ha:.1f} hectares)
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🗑️ Clear Area"):
            st.session_state.area_geojson = None
            st.rerun()
    else:
        st.markdown("""
        <div class="status-warning">
            ⚠️ No area defined yet
        </div>
        """, unsafe_allow_html=True)

def render_interactive_map():
    """Render the interactive map"""
    
    if not FOLIUM_AVAILABLE:
        st.error("❌ Folium not available. Please install with: pip install folium streamlit-folium")
        return
    
    # Create the folium map
    center = st.session_state.area_center
    m = folium.Map(
        location=center,
        zoom_start=10,
        tiles="OpenStreetMap"
    )
    
    # Add the area if it exists
    if st.session_state.area_geojson:
        folium.GeoJson(
            st.session_state.area_geojson,
            style_function=lambda x: {
                'fillColor': '#4CAF50',
                'color': '#2E7D32',
                'weight': 3,
                'fillOpacity': 0.3
            },
            popup=folium.Popup(f"📍 {st.session_state.area_name}", parse_html=True),
            tooltip=f"{st.session_state.area_name}"
        ).add_to(m)
        
        # Fit bounds to the area
        if st.session_state.area_geojson['type'] == 'FeatureCollection':
            bounds = get_geojson_bounds(st.session_state.area_geojson)
            m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])
    
    # Add drawing capabilities
    draw = folium.plugins.Draw(
        export=True,
        draw_options={
            'polygon': {'allowIntersection': False},
            'rectangle': True,
            'circle': False,
            'marker': False,
            'circlemarker': False,
            'polyline': False
        }
    )
    draw.add_to(m)
    
    # Display the map
    map_data = st_folium(m, width=700, height=500, returned_objects=["all_drawings"])
    
    # Handle drawn features
    if map_data['all_drawings']:
        if st.button("💾 Save Drawn Area"):
            try:
                # Convert drawn features to GeoJSON
                geojson_data = {
                    "type": "FeatureCollection",
                    "features": map_data['all_drawings']
                }
                
                st.session_state.area_geojson = geojson_data
                st.session_state.area_center = get_geojson_center(geojson_data)
                st.success(f"✅ Saved drawn area: {st.session_state.area_name}")
                st.rerun()
                
            except Exception as e:
                st.error(f"Error saving drawn area: {str(e)}")

def render_analytics_view():
    """Render the analytics dashboard"""
    
    if not st.session_state.area_geojson:
        render_no_area_analytics()
        return
    
    st.markdown(f"## 📊 Analytics Dashboard - {st.session_state.area_name}")
    
    # Create analytics layout
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        render_weather_widget()
    
    with col2:
        render_area_metrics()
    
    with col3:
        render_land_health()
    
    # Full-width analytics
    st.markdown("---")
    
    col4, col5 = st.columns([1, 1])
    
    with col4:
        render_satellite_analysis()
    
    with col5:
        render_soil_analysis()
    
    # Time series analysis
    st.markdown("---")
    render_time_series_analysis()

def render_no_area_analytics():
    """Show analytics placeholder when no area is defined"""
    
    st.markdown("## 📊 Analytics Dashboard")
    
    st.info("🗺️ **Please define an area first**")
    st.markdown("""
    To see analytics for your land:
    
    1. **Switch to the Mapping View tab**
    2. **Upload a GeoJSON file or draw your area**
    3. **Return here to see detailed analytics**
    
    Once you define an area, you'll see:
    - 🌤️ Current weather conditions
    - 📏 Area measurements and boundaries  
    - 🛰️ Satellite imagery analysis
    - 🌱 Vegetation health metrics
    - 📈 Historical trends and patterns
    """)
    
    # Show demo analytics
    with st.expander("👁️ Preview Analytics (Demo Data)"):
        render_demo_analytics()

def render_weather_widget():
    """Render current weather for the area"""
    
    st.markdown("""
    <div class="analytics-card">
        <h4 style="margin-top: 0;">🌤️ Current Weather</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Get weather data (demo for now)
    center = st.session_state.area_center
    weather_data = get_weather_data(center[0], center[1])
    
    if weather_data:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{weather_data['temperature']}°C</div>
                <div class="metric-label">Temperature</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{weather_data['humidity']}%</div>
                <div class="metric-label">Humidity</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.metric("💨 Wind Speed", f"{weather_data['wind_speed']} km/h")
        st.metric("🌧️ Precipitation", f"{weather_data['precipitation']} mm")
    else:
        st.warning("Weather data unavailable")

def render_area_metrics():
    """Render basic area metrics"""
    
    st.markdown("""
    <div class="analytics-card">
        <h4 style="margin-top: 0;">📏 Area Information</h4>
    </div>
    """, unsafe_allow_html=True)
    
    area_ha = calculate_area_hectares(st.session_state.area_geojson)
    area_acres = area_ha * 2.47105  # Convert to acres
    
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{area_ha:.1f}</div>
        <div class="metric-label">Hectares</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{area_acres:.1f}</div>
        <div class="metric-label">Acres</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Boundary analysis
    perimeter = calculate_perimeter_km(st.session_state.area_geojson)
    st.metric("📐 Perimeter", f"{perimeter:.2f} km")

def render_land_health():
    """Render land health indicators"""
    
    st.markdown("""
    <div class="analytics-card">
        <h4 style="margin-top: 0;">🌱 Land Health</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Generate sample health metrics
    ndvi = np.random.uniform(0.3, 0.8)
    soil_health = np.random.uniform(60, 90)
    biodiversity = np.random.uniform(70, 95)
    
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{ndvi:.2f}</div>
        <div class="metric-label">NDVI Index</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.metric("🌾 Soil Health", f"{soil_health:.0f}%")
    st.metric("🦋 Biodiversity", f"{biodiversity:.0f}%")

def render_satellite_analysis():
    """Render satellite imagery analysis"""
    
    st.markdown("### 🛰️ Satellite Analysis")
    
    if not PLOTLY_AVAILABLE:
        st.warning("Plotly not available for visualizations")
        return
    
    # Generate sample NDVI time series
    dates = pd.date_range('2023-01-01', '2023-12-31', freq='M')
    ndvi_values = 0.4 + 0.3 * np.sin(2 * np.pi * np.arange(len(dates)) / 12) + np.random.normal(0, 0.05, len(dates))
    
    fig = px.line(
        x=dates, 
        y=ndvi_values,
        title="NDVI Trend (Vegetation Health)",
        labels={'x': 'Date', 'y': 'NDVI Value'}
    )
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)

def render_soil_analysis():
    """Render soil analysis"""
    
    st.markdown("### 🌾 Soil Analysis")
    
    if not PLOTLY_AVAILABLE:
        st.warning("Plotly not available for visualizations")
        return
    
    # Generate sample soil data
    soil_types = ['Clay', 'Loam', 'Sand', 'Silt']
    percentages = np.random.dirichlet(np.ones(4)) * 100
    
    fig = px.pie(
        values=percentages,
        names=soil_types,
        title="Soil Composition"
    )
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)

def render_time_series_analysis():
    """Render comprehensive time series analysis"""
    
    st.markdown("### 📈 Historical Analysis")
    
    if not PLOTLY_AVAILABLE:
        st.warning("Plotly not available for visualizations")
        return
    
    # Generate sample multi-metric time series
    dates = pd.date_range('2020-01-01', '2023-12-31', freq='M')
    
    # NDVI
    ndvi = 0.4 + 0.3 * np.sin(2 * np.pi * np.arange(len(dates)) / 12) + np.random.normal(0, 0.05, len(dates))
    
    # Temperature
    temp = 15 + 10 * np.sin(2 * np.pi * np.arange(len(dates)) / 12) + np.random.normal(0, 2, len(dates))
    
    # Precipitation
    precip = 50 + 30 * np.sin(2 * np.pi * (np.arange(len(dates)) + 3) / 12) + np.random.normal(0, 10, len(dates))
    
    # Create subplot
    fig = make_subplots(
        rows=3, cols=1,
        subplot_titles=['Vegetation Health (NDVI)', 'Temperature (°C)', 'Precipitation (mm)'],
        vertical_spacing=0.08
    )
    
    fig.add_trace(go.Scatter(x=dates, y=ndvi, name='NDVI', line=dict(color='green')), row=1, col=1)
    fig.add_trace(go.Scatter(x=dates, y=temp, name='Temperature', line=dict(color='red')), row=2, col=1)
    fig.add_trace(go.Scatter(x=dates, y=precip, name='Precipitation', line=dict(color='blue')), row=3, col=1)
    
    fig.update_layout(height=500, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

def render_demo_analytics():
    """Show demo analytics"""
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🌤️ Temperature", "18.5°C", "↑ 2.1°C")
    
    with col2:
        st.metric("🌱 NDVI", "0.65", "↑ 0.05")
    
    with col3:
        st.metric("🌾 Soil Health", "78%", "↑ 3%")

# Utility functions
def validate_geojson(geojson_data):
    """Validate GeoJSON format"""
    try:
        required_keys = ['type']
        if not all(key in geojson_data for key in required_keys):
            return False
        
        if geojson_data['type'] not in ['Feature', 'FeatureCollection', 'Polygon', 'MultiPolygon']:
            return False
        
        return True
    except:
        return False

def get_geojson_center(geojson_data):
    """Get the center point of a GeoJSON"""
    try:
        if GEOPANDAS_AVAILABLE:
            gdf = gpd.GeoDataFrame.from_features(geojson_data)
            centroid = gdf.geometry.centroid.iloc[0]
            return [centroid.y, centroid.x]
        else:
            # Fallback calculation
            return [51.5074, -0.1278]  # Default to London
    except:
        return [51.5074, -0.1278]

def get_geojson_bounds(geojson_data):
    """Get bounds of GeoJSON"""
    try:
        if GEOPANDAS_AVAILABLE:
            gdf = gpd.GeoDataFrame.from_features(geojson_data)
            bounds = gdf.total_bounds
            return bounds  # [minx, miny, maxx, maxy]
        else:
            return [-1, 51, 1, 52]  # Default bounds
    except:
        return [-1, 51, 1, 52]

def calculate_area_hectares(geojson_data):
    """Calculate area in hectares"""
    try:
        if GEOPANDAS_AVAILABLE:
            gdf = gpd.GeoDataFrame.from_features(geojson_data)
            # Convert to appropriate CRS for area calculation
            gdf_projected = gdf.to_crs('EPSG:3857')  # Web Mercator
            area_m2 = gdf_projected.geometry.area.sum()
            return area_m2 / 10000  # Convert to hectares
        else:
            return np.random.uniform(10, 200)  # Demo value
    except:
        return np.random.uniform(10, 200)

def calculate_perimeter_km(geojson_data):
    """Calculate perimeter in kilometers"""
    try:
        if GEOPANDAS_AVAILABLE:
            gdf = gpd.GeoDataFrame.from_features(geojson_data)
            gdf_projected = gdf.to_crs('EPSG:3857')
            perimeter_m = gdf_projected.geometry.length.sum()
            return perimeter_m / 1000  # Convert to km
        else:
            return np.random.uniform(2, 20)  # Demo value
    except:
        return np.random.uniform(2, 20)

def get_weather_data(lat, lon):
    """Get weather data for coordinates (demo implementation)"""
    # In a real implementation, this would call a weather API
    return {
        'temperature': np.random.uniform(10, 25),
        'humidity': np.random.uniform(40, 80),
        'wind_speed': np.random.uniform(5, 20),
        'precipitation': np.random.uniform(0, 15)
    }

if __name__ == "__main__":
    main()