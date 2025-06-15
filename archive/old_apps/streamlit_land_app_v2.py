"""
GeoMasterPy Land App v2 - Exact Land App HTML Design

A pixel-perfect recreation of the Land App interface with working drawing tools
and seamless transition to analytics view.
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
import requests
from datetime import datetime, date
import base64
from io import BytesIO

# Configure Streamlit page
st.set_page_config(
    page_title="GeoMasterPy Land App",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
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

# Complete Land App CSS - Exact replica
st.markdown("""
<style>
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    .stApp > header {visibility: hidden;}
    
    /* Remove default Streamlit padding */
    .main .block-container {
        padding-top: 0;
        padding-bottom: 0;
        padding-left: 0;
        padding-right: 0;
        max-width: none;
    }
    
    /* Body styling to match Land App */
    .stApp {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
        background-color: #f5f5f5;
    }
    
    /* Land App Header */
    .land-app-header {
        background: white;
        border-bottom: 1px solid #e0e0e0;
        height: 60px;
        display: flex;
        align-items: center;
        padding: 0 20px;
        position: relative;
        z-index: 1000;
        width: 100%;
        margin: 0;
    }
    
    .logo {
        display: flex;
        align-items: center;
        gap: 10px;
        font-weight: 600;
        font-size: 16px;
    }
    
    .logo-icon {
        width: 24px;
        height: 24px;
        background: #4CAF50;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 14px;
    }
    
    .header-title {
        flex: 1;
        text-align: center;
        font-size: 14px;
        color: #666;
    }
    
    .header-actions {
        display: flex;
        gap: 15px;
        align-items: center;
    }
    
    .header-btn {
        background: none;
        border: none;
        cursor: pointer;
        font-size: 18px;
        color: #666;
        padding: 5px;
        transition: color 0.2s;
    }
    
    .header-btn:hover {
        color: #333;
    }
    
    /* Main Container */
    .main-container {
        display: flex;
        height: calc(100vh - 60px);
        width: 100%;
    }
    
    /* Sidebar */
    .sidebar {
        width: 250px;
        background: white;
        border-right: 1px solid #e0e0e0;
        overflow-y: auto;
        transition: width 0.3s ease;
        height: 100%;
    }
    
    .sidebar.collapsed {
        width: 60px;
    }
    
    .sidebar-header {
        padding: 15px;
        border-bottom: 1px solid #e0e0e0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .sidebar-title {
        font-weight: 600;
        font-size: 16px;
        margin: 0;
    }
    
    .sidebar.collapsed .sidebar-title {
        display: none;
    }
    
    .sidebar-item {
        padding: 12px 15px;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 10px;
        transition: background 0.2s;
        border-left: 3px solid transparent;
    }
    
    .sidebar-item:hover {
        background: #f5f5f5;
    }
    
    .sidebar-item.active {
        background: #e8f5e9;
        border-left-color: #4CAF50;
    }
    
    .sidebar-item i {
        width: 20px;
        text-align: center;
        color: #666;
        font-size: 16px;
    }
    
    .sidebar-item.active i {
        color: #4CAF50;
    }
    
    .sidebar-item-text {
        flex: 1;
        font-size: 14px;
        margin: 0;
    }
    
    .sidebar.collapsed .sidebar-item-text {
        display: none;
    }
    
    .sidebar-item-count {
        background: #e0e0e0;
        color: #666;
        font-size: 12px;
        padding: 2px 8px;
        border-radius: 10px;
        min-width: 20px;
        text-align: center;
    }
    
    .sidebar.collapsed .sidebar-item-count {
        display: none;
    }
    
    /* Map Container */
    .map-container {
        flex: 1;
        position: relative;
        background: #e0e0e0;
    }
    
    /* Drawing Tools */
    .drawing-tools {
        position: absolute;
        top: 20px;
        left: 20px;
        background: white;
        border-radius: 4px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        display: flex;
        gap: 5px;
        padding: 5px;
        z-index: 1000;
    }
    
    .drawing-tool {
        width: 36px;
        height: 36px;
        border: none;
        background: none;
        cursor: pointer;
        border-radius: 4px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #666;
        transition: all 0.2s;
        font-size: 16px;
    }
    
    .drawing-tool:hover {
        background: #f5f5f5;
        color: #333;
    }
    
    .drawing-tool.active {
        background: #4CAF50;
        color: white;
    }
    
    /* Map Controls */
    .map-controls {
        position: absolute;
        top: 20px;
        right: 20px;
        display: flex;
        flex-direction: column;
        gap: 10px;
        z-index: 1000;
    }
    
    .map-control-button {
        background: white;
        border: 1px solid #ddd;
        width: 40px;
        height: 40px;
        border-radius: 4px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        color: #666;
        transition: all 0.2s;
    }
    
    .map-control-button:hover {
        background: #f5f5f5;
        color: #333;
    }
    
    /* Info Panel */
    .info-panel {
        position: absolute;
        bottom: 20px;
        left: 270px;
        right: 20px;
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        padding: 20px;
        z-index: 1000;
        max-height: 200px;
        overflow-y: auto;
    }
    
    .info-panel-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
    }
    
    .info-panel-title {
        font-size: 18px;
        font-weight: 600;
        margin: 0;
    }
    
    .info-panel-close {
        background: none;
        border: none;
        font-size: 20px;
        cursor: pointer;
        color: #666;
    }
    
    .info-panel-content {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
    }
    
    .info-item {
        display: flex;
        flex-direction: column;
        gap: 5px;
    }
    
    .info-label {
        font-size: 12px;
        color: #666;
        text-transform: uppercase;
        margin: 0;
    }
    
    .info-value {
        font-size: 24px;
        font-weight: 600;
        color: #333;
        margin: 0;
    }
    
    .info-unit {
        font-size: 14px;
        font-weight: 400;
        color: #666;
    }
    
    /* Tab Navigation */
    .tab-navigation {
        position: absolute;
        top: 20px;
        left: 50%;
        transform: translateX(-50%);
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        display: flex;
        overflow: hidden;
        z-index: 1001;
    }
    
    .tab-button {
        padding: 12px 24px;
        border: none;
        background: white;
        cursor: pointer;
        font-size: 14px;
        font-weight: 500;
        color: #666;
        transition: all 0.2s;
        border-right: 1px solid #e0e0e0;
    }
    
    .tab-button:last-child {
        border-right: none;
    }
    
    .tab-button:hover {
        background: #f5f5f5;
        color: #333;
    }
    
    .tab-button.active {
        background: #4CAF50;
        color: white;
    }
    
    /* Analytics View */
    .analytics-container {
        padding: 20px;
        background: #f5f5f5;
        height: 100%;
        overflow-y: auto;
    }
    
    .analytics-header {
        background: white;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .analytics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 20px;
        margin-bottom: 20px;
    }
    
    .analytics-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 4px solid #4CAF50;
    }
    
    .metric-row {
        display: flex;
        gap: 20px;
        margin-bottom: 20px;
    }
    
    .metric-card {
        flex: 1;
        background: #f8f9fa;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 600;
        color: #4CAF50;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        color: #666;
        font-size: 0.9rem;
        margin: 0;
    }
    
    /* Hide Streamlit elements in map view */
    .main-container .stApp > div {
        padding: 0 !important;
    }
    
    /* Custom scrollbar */
    .sidebar::-webkit-scrollbar {
        width: 6px;
    }
    
    .sidebar::-webkit-scrollbar-track {
        background: #f1f1f1;
    }
    
    .sidebar::-webkit-scrollbar-thumb {
        background: #c1c1c1;
        border-radius: 3px;
    }
    
    .sidebar::-webkit-scrollbar-thumb:hover {
        background: #a8a8a8;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application with exact Land App design"""
    
    # Initialize session state
    if 'current_view' not in st.session_state:
        st.session_state.current_view = 'mapping'
    if 'sidebar_collapsed' not in st.session_state:
        st.session_state.sidebar_collapsed = False
    if 'selected_area' not in st.session_state:
        st.session_state.selected_area = None
    if 'area_geojson' not in st.session_state:
        st.session_state.area_geojson = None
    if 'area_name' not in st.session_state:
        st.session_state.area_name = "Norney Farm"
    if 'area_center' not in st.session_state:
        st.session_state.area_center = [51.1867, -0.5749]  # Norney Farm coordinates
    if 'show_info_panel' not in st.session_state:
        st.session_state.show_info_panel = False
    
    # Create the exact Land App layout
    render_land_app_interface()

def render_land_app_interface():
    """Render the complete Land App interface"""
    
    # Land App Header
    st.markdown("""
    <div class="land-app-header">
        <div class="logo">
            <div class="logo-icon">🌱</div>
            <span>Land App</span>
        </div>
        <div class="header-title">
            Map: Official - Norney Farm (106257846) SFI design 2024 with Ben Habgood
        </div>
        <div class="header-actions">
            <button class="header-btn" title="Search">
                <i class="fas fa-search"></i>
            </button>
            <button class="header-btn" title="Layers">
                <i class="fas fa-layer-group"></i>
            </button>
            <button class="header-btn" title="Download">
                <i class="fas fa-download"></i>
            </button>
            <button class="header-btn" title="Share">
                <i class="fas fa-share-alt"></i>
            </button>
            <button class="header-btn" title="Settings">
                <i class="fas fa-cog"></i>
            </button>
            <button class="header-btn" title="User">
                <i class="fas fa-user-circle"></i>
            </button>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Main Container
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Determine current view and render accordingly
    if st.session_state.current_view == 'mapping':
        render_mapping_interface()
    else:
        render_analytics_interface()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_mapping_interface():
    """Render the mapping interface with exact Land App layout"""
    
    # Sidebar
    sidebar_class = "sidebar collapsed" if st.session_state.sidebar_collapsed else "sidebar"
    
    st.markdown(f'''
    <div class="{sidebar_class}">
        <div class="sidebar-header">
            <h3 class="sidebar-title">Plans</h3>
            <button style="background: none; border: none; cursor: pointer;">
                <i class="fas fa-plus"></i>
            </button>
        </div>
        
        <div class="sidebar-item">
            <i class="fas fa-border-all"></i>
            <span class="sidebar-item-text">Boundary</span>
            <span class="sidebar-item-count">1</span>
        </div>
        
        <div class="sidebar-item">
            <i class="fas fa-map"></i>
            <span class="sidebar-item-text">OSMM</span>
            <span class="sidebar-item-count">1</span>
        </div>
        
        <div class="sidebar-item">
            <i class="fas fa-database"></i>
            <span class="sidebar-item-text">HPA Data</span>
            <span class="sidebar-item-count">1</span>
        </div>
        
        <div class="sidebar-item active">
            <i class="fas fa-tree"></i>
            <span class="sidebar-item-text">BLE1</span>
            <span class="sidebar-item-count">1</span>
        </div>
        
        <div class="sidebar-item">
            <i class="fas fa-water"></i>
            <span class="sidebar-item-text">EWCO</span>
            <span class="sidebar-item-count">1</span>
        </div>
        
        <div class="sidebar-item">
            <i class="fas fa-chart-line"></i>
            <span class="sidebar-item-text">e-planner</span>
            <span class="sidebar-item-count">1</span>
        </div>
        
        <div class="sidebar-item">
            <i class="fas fa-shield-alt"></i>
            <span class="sidebar-item-text">Hedge survey</span>
            <span class="sidebar-item-count">1</span>
        </div>
        
        <div class="sidebar-item">
            <i class="fas fa-project-diagram"></i>
            <span class="sidebar-item-text">SFI Designs</span>
            <span class="sidebar-item-count">7</span>
        </div>
        
        <div class="sidebar-header" style="margin-top: 20px;">
            <h3 class="sidebar-title">Other information</h3>
        </div>
        
        <div class="sidebar-item">
            <i class="fas fa-file-alt"></i>
            <span class="sidebar-item-text">Lucerne</span>
            <span class="sidebar-item-count">1</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Map Container with overlays
    st.markdown('<div class="map-container">', unsafe_allow_html=True)
    
    # Tab Navigation
    st.markdown(f'''
    <div class="tab-navigation">
        <button class="tab-button {'active' if st.session_state.current_view == 'mapping' else ''}" 
                onclick="switchToMapping()">
            🗺️ Mapping View
        </button>
        <button class="tab-button {'active' if st.session_state.current_view == 'analytics' else ''}" 
                onclick="switchToAnalytics()">
            📊 Analytics View
        </button>
    </div>
    ''', unsafe_allow_html=True)
    
    # Drawing Tools
    st.markdown('''
    <div class="drawing-tools">
        <button class="drawing-tool" title="Select" onclick="selectTool('select')">
            <i class="fas fa-mouse-pointer"></i>
        </button>
        <button class="drawing-tool active" title="Draw Polygon" onclick="selectTool('polygon')">
            <i class="fas fa-draw-polygon"></i>
        </button>
        <button class="drawing-tool" title="Draw Rectangle" onclick="selectTool('rectangle')">
            <i class="fas fa-vector-square"></i>
        </button>
        <button class="drawing-tool" title="Draw Circle" onclick="selectTool('circle')">
            <i class="fas fa-circle"></i>
        </button>
        <button class="drawing-tool" title="Measure" onclick="selectTool('measure')">
            <i class="fas fa-ruler"></i>
        </button>
    </div>
    ''', unsafe_allow_html=True)
    
    # Map Controls
    st.markdown('''
    <div class="map-controls">
        <button class="map-control-button" title="Zoom In" onclick="zoomIn()">
            <i class="fas fa-plus"></i>
        </button>
        <button class="map-control-button" title="Zoom Out" onclick="zoomOut()">
            <i class="fas fa-minus"></i>
        </button>
        <button class="map-control-button" title="Locate" onclick="locate()">
            <i class="fas fa-crosshairs"></i>
        </button>
        <button class="map-control-button" title="Fullscreen" onclick="toggleFullscreen()">
            <i class="fas fa-expand"></i>
        </button>
    </div>
    ''', unsafe_allow_html=True)
    
    # Render the actual map
    render_folium_map()
    
    # Info Panel (conditionally shown)
    if st.session_state.show_info_panel:
        render_info_panel()
    
    # View switching buttons (hidden but functional)
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🗺️ Mapping", key="mapping_tab", help="Switch to mapping view"):
            st.session_state.current_view = 'mapping'
            st.rerun()
    
    with col2:
        if st.button("📊 Analytics", key="analytics_tab", help="Switch to analytics view"):
            st.session_state.current_view = 'analytics'
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_folium_map():
    """Render the interactive Folium map with drawing capabilities"""
    
    if not FOLIUM_AVAILABLE:
        st.error("❌ Folium not available. Please install: pip install folium streamlit-folium")
        return
    
    # Create the map centered on Norney Farm
    m = folium.Map(
        location=st.session_state.area_center,
        zoom_start=15,
        tiles="OpenStreetMap"
    )
    
    # Add sample farm parcels (woodland and grassland)
    # Woodland parcel
    woodland_coords = [
        [51.1875, -0.5765],
        [51.1880, -0.5745],
        [51.1870, -0.5740],
        [51.1865, -0.5755]
    ]
    
    folium.Polygon(
        locations=woodland_coords,
        color='#4CAF50',
        fillColor='#4CAF50',
        fillOpacity=0.6,
        weight=2,
        popup="Woodland Area - 19.94 ha",
        tooltip="Woodland"
    ).add_to(m)
    
    # Grassland parcel
    grassland_coords = [
        [51.1860, -0.5760],
        [51.1865, -0.5735],
        [51.1855, -0.5730],
        [51.1850, -0.5750]
    ]
    
    folium.Polygon(
        locations=grassland_coords,
        color='#2196F3',
        fillColor='#2196F3',
        fillOpacity=0.5,
        weight=2,
        popup="Grassland Area - 30.62 ha",
        tooltip="Grassland"
    ).add_to(m)
    
    # Buffer zone with cross-hatch pattern
    buffer_coords = [
        [51.1870, -0.5755],
        [51.1872, -0.5748],
        [51.1868, -0.5745],
        [51.1866, -0.5752]
    ]
    
    folium.Polygon(
        locations=buffer_coords,
        color='#4CAF50',
        fillColor='#4CAF50',
        fillOpacity=0.3,
        weight=2,
        dashArray='5, 5',
        popup="Buffer Strip - 0.48 ha",
        tooltip="Buffer Strip"
    ).add_to(m)
    
    # Add drawing capability
    draw = folium.plugins.Draw(
        export=True,
        draw_options={
            'polygon': {
                'allowIntersection': False,
                'shapeOptions': {
                    'color': '#4CAF50',
                    'fillOpacity': 0.5
                }
            },
            'rectangle': {
                'shapeOptions': {
                    'color': '#2196F3',
                    'fillOpacity': 0.5
                }
            },
            'circle': True,
            'marker': False,
            'circlemarker': False,
            'polyline': False
        }
    )
    draw.add_to(m)
    
    # Display the map
    map_data = st_folium(
        m, 
        width=None, 
        height=500, 
        returned_objects=["all_drawings", "last_object_clicked"],
        key="land_app_map"
    )
    
    # Handle drawn features
    if map_data['all_drawings']:
        if not st.session_state.show_info_panel:
            st.session_state.show_info_panel = True
            st.rerun()
    
    # Handle clicks on existing features
    if map_data['last_object_clicked']:
        if not st.session_state.show_info_panel:
            st.session_state.show_info_panel = True
            st.rerun()

def render_info_panel():
    """Render the information panel at the bottom"""
    
    st.markdown('''
    <div class="info-panel">
        <div class="info-panel-header">
            <h3 class="info-panel-title">Selected Parcel Information</h3>
            <button class="info-panel-close" onclick="closeInfoPanel()">
                <i class="fas fa-times"></i>
            </button>
        </div>
        <div class="info-panel-content">
            <div class="info-item">
                <p class="info-label">Total Area</p>
                <p class="info-value">68.00 <span class="info-unit">ha</span></p>
            </div>
            <div class="info-item">
                <p class="info-label">Woodland</p>
                <p class="info-value">19.94 <span class="info-unit">ha</span></p>
            </div>
            <div class="info-item">
                <p class="info-label">Grassland</p>
                <p class="info-value">30.62 <span class="info-unit">ha</span></p>
            </div>
            <div class="info-item">
                <p class="info-label">Buffer Strips</p>
                <p class="info-value">0.48 <span class="info-unit">ha</span></p>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Hidden close button that actually works
    if st.button("✕", key="close_info_panel", help="Close info panel"):
        st.session_state.show_info_panel = False
        st.rerun()

def render_analytics_interface():
    """Render the analytics dashboard"""
    
    st.markdown('<div class="analytics-container">', unsafe_allow_html=True)
    
    # Tab Navigation
    st.markdown(f'''
    <div class="tab-navigation">
        <button class="tab-button {'active' if st.session_state.current_view == 'mapping' else ''}" 
                onclick="switchToMapping()">
            🗺️ Mapping View
        </button>
        <button class="tab-button {'active' if st.session_state.current_view == 'analytics' else ''}" 
                onclick="switchToAnalytics()">
            📊 Analytics View
        </button>
    </div>
    ''', unsafe_allow_html=True)
    
    # Analytics Header
    st.markdown(f'''
    <div class="analytics-header">
        <h2 style="margin: 0; color: #333;">Nature Reporting: {st.session_state.area_name}</h2>
        <p style="margin: 5px 0 0 0; color: #666;">Surrey - 68.00 ha</p>
        <p style="margin: 10px 0 0 0; color: #4CAF50; font-weight: 600;">Produce Type: Mixed Farming</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Metrics Grid
    render_analytics_metrics()
    
    # Charts and visualizations
    render_analytics_charts()
    
    # View switching buttons (hidden but functional)
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🗺️ Mapping", key="mapping_tab_analytics", help="Switch to mapping view"):
            st.session_state.current_view = 'mapping'
            st.rerun()
    
    with col2:
        if st.button("📊 Analytics", key="analytics_tab_analytics", help="Stay in analytics view"):
            pass  # Already in analytics
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_analytics_metrics():
    """Render the metrics cards"""
    
    # Top metrics row
    st.markdown('''
    <div class="metric-row">
        <div class="metric-card">
            <div class="metric-value">100.00%</div>
            <p class="metric-label">Habitat Cover</p>
            <div style="margin-top: 10px; font-size: 12px; color: #666;">
                83.75% (-16.35%) - Land management plan
            </div>
        </div>
        <div class="metric-card">
            <div class="metric-value">30.91%</div>
            <p class="metric-label">Connectedness</p>
            <div style="margin-top: 10px; font-size: 12px; color: #666;">
                27.08% (-3.91%) - Land management plan
            </div>
        </div>
        <div class="metric-card">
            <div class="metric-value">0.65</div>
            <p class="metric-label">NDVI Index</p>
            <div style="margin-top: 10px; font-size: 12px; color: #666;">
                Vegetation health indicator
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

def render_analytics_charts():
    """Render charts and visualizations"""
    
    if not PLOTLY_AVAILABLE:
        st.warning("Plotly not available for charts")
        return
    
    # Create two columns for charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
        st.markdown("### 🛰️ NDVI Trend Analysis")
        
        # Generate NDVI time series
        dates = pd.date_range('2023-01-01', '2023-12-31', freq='M')
        ndvi_values = 0.4 + 0.3 * np.sin(2 * np.pi * np.arange(len(dates)) / 12) + np.random.normal(0, 0.05, len(dates))
        
        fig = px.line(
            x=dates, 
            y=ndvi_values,
            title="Vegetation Health Over Time",
            labels={'x': 'Date', 'y': 'NDVI Value'}
        )
        fig.update_layout(height=300, showlegend=False)
        fig.update_traces(line_color='#4CAF50')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
        st.markdown("### 🌾 Land Use Distribution")
        
        # Land use pie chart
        land_use = ['Woodland', 'Grassland', 'Crops', 'Buffer Strips']
        areas = [19.94, 30.62, 17.0, 0.48]
        
        fig = px.pie(
            values=areas,
            names=land_use,
            title="Area Distribution (hectares)",
            color_discrete_sequence=['#4CAF50', '#2196F3', '#FF9800', '#9C27B0']
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Weather and soil analysis
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
        st.markdown("### 🌤️ Weather Conditions")
        
        # Current weather metrics
        st.metric("Temperature", "18.5°C", "↑ 2.1°C")
        st.metric("Humidity", "68%", "↓ 5%")
        st.metric("Wind Speed", "12 km/h", "↑ 3 km/h")
        st.metric("Precipitation", "2.3 mm", "↑ 1.1 mm")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
        st.markdown("### 🌱 Soil Health Indicators")
        
        # Soil health metrics
        st.metric("Soil pH", "6.8", "↑ 0.2")
        st.metric("Organic Matter", "4.2%", "↑ 0.3%")
        st.metric("Nitrogen", "42 ppm", "↓ 3 ppm")
        st.metric("Phosphorus", "28 ppm", "↑ 5 ppm")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Add JavaScript for interactive functionality
st.markdown("""
<script>
function switchToMapping() {
    // This would normally trigger the view switch
    console.log('Switching to mapping view');
}

function switchToAnalytics() {
    // This would normally trigger the view switch
    console.log('Switching to analytics view');
}

function selectTool(tool) {
    // Remove active class from all tools
    document.querySelectorAll('.drawing-tool').forEach(t => t.classList.remove('active'));
    // Add active class to clicked tool
    event.target.closest('.drawing-tool').classList.add('active');
    console.log('Selected tool:', tool);
}

function closeInfoPanel() {
    document.querySelector('.info-panel').style.display = 'none';
}

function zoomIn() {
    console.log('Zoom in');
}

function zoomOut() {
    console.log('Zoom out');
}

function locate() {
    console.log('Locate');
}

function toggleFullscreen() {
    console.log('Toggle fullscreen');
}
</script>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()