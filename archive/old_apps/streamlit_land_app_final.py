"""
GeoMasterPy Land App - Final Version

Fixed sidebar rendering and full-screen map display
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
from datetime import datetime, date

# Configure Streamlit page
st.set_page_config(
    page_title="GeoMasterPy Land App",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
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

# Land App CSS with proper layout
st.markdown("""
<style>
    /* Remove Streamlit branding */
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    
    /* Remove default padding */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: none;
    }
    
    /* Body styling */
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
        margin: -1rem -1rem 1rem -1rem;
        position: relative;
        z-index: 1000;
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
        font-size: 12px;
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
    }
    
    .header-btn:hover {
        color: #333;
    }
    
    /* Sidebar styling */
    .sidebar {
        width: 250px;
        background: white;
        border-right: 1px solid #e0e0e0;
        overflow-y: auto;
        height: 100%;
        flex-shrink: 0;
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
        color: #333;
    }
    
    .sidebar-item {
        padding: 12px 15px;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 10px;
        transition: background 0.2s;
        border-left: 3px solid transparent;
        margin: 0;
    }
    
    .sidebar-item:hover {
        background: #f5f5f5;
    }
    
    .sidebar-item.active {
        background: #e8f5e9;
        border-left-color: #4CAF50;
    }
    
    .sidebar-item-icon {
        width: 20px;
        text-align: center;
        color: #666;
        font-size: 16px;
    }
    
    .sidebar-item.active .sidebar-item-icon {
        color: #4CAF50;
    }
    
    .sidebar-item-text {
        flex: 1;
        font-size: 14px;
        margin: 0;
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
    
    /* Main container */
    .main-container {
        display: flex;
        height: calc(100vh - 60px);
        width: 100%;
        overflow: hidden;
    }
    
    /* Main content area */
    .main-content {
        flex: 1;
        position: relative;
        background: #e0e0e0;
        height: 100%;
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
        border: 1px solid #e0e0e0;
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
        min-width: 140px;
        text-align: center;
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
        left: 20px;
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
    
    /* Analytics styling */
    .analytics-header {
        background: white;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .metric-card {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        margin-bottom: 15px;
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
    
    /* Hide Streamlit specific elements */
    .stButton > button {
        display: none;
    }
</style>

<!-- FontAwesome for icons -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />
""", unsafe_allow_html=True)

def main():
    """Main application"""
    
    # Initialize session state
    if 'current_view' not in st.session_state:
        st.session_state.current_view = 'mapping'
    if 'show_info_panel' not in st.session_state:
        st.session_state.show_info_panel = False
    
    # Render header
    render_header()
    
    # Create layout with sidebar and main content
    if st.session_state.current_view == 'mapping':
        render_mapping_interface()
    else:
        render_analytics_interface()

def render_header():
    """Render the Land App header"""
    
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

def render_mapping_interface():
    """Render the mapping interface with proper layout"""
    
    # Use the working approach from streamlit_land_app_fixed.py
    # This renders the complete interface in one go
    render_complete_mapping_layout()
    
    # Tab Navigation
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        tab_col1, tab_col2 = st.columns(2)
        with tab_col1:
            if st.button("🗺️ Mapping View", key="mapping_btn", use_container_width=True):
                st.session_state.current_view = 'mapping'
                st.rerun()
        with tab_col2:
            if st.button("📊 Analytics View", key="analytics_btn", use_container_width=True):
                st.session_state.current_view = 'analytics'
                st.rerun()
    
    # Drawing Tools (overlay)
    st.markdown('''
    <div class="drawing-tools">
        <button class="drawing-tool" title="Select">
            <i class="fas fa-mouse-pointer"></i>
        </button>
        <button class="drawing-tool active" title="Draw Polygon">
            <i class="fas fa-draw-polygon"></i>
        </button>
        <button class="drawing-tool" title="Draw Rectangle">
            <i class="fas fa-vector-square"></i>
        </button>
        <button class="drawing-tool" title="Draw Circle">
            <i class="fas fa-circle"></i>
        </button>
        <button class="drawing-tool" title="Measure">
            <i class="fas fa-ruler"></i>
        </button>
    </div>
    ''', unsafe_allow_html=True)
    
    # Map Controls (overlay)
    st.markdown('''
    <div class="map-controls">
        <button class="map-control-button" title="Zoom In">
            <i class="fas fa-plus"></i>
        </button>
        <button class="map-control-button" title="Zoom Out">
            <i class="fas fa-minus"></i>
        </button>
        <button class="map-control-button" title="Locate">
            <i class="fas fa-crosshairs"></i>
        </button>
        <button class="map-control-button" title="Fullscreen">
            <i class="fas fa-expand"></i>
        </button>
    </div>
    ''', unsafe_allow_html=True)
    
    # Render the main map
    render_full_screen_map()
    
    # Info Panel (conditional)
    if st.session_state.show_info_panel:
        render_info_panel()
    
    st.markdown('</div></div>', unsafe_allow_html=True)

def render_complete_mapping_layout():
    """Render the complete mapping layout that actually works"""
    
    # Use a container approach that bypasses Streamlit's sidebar limitations
    st.markdown('''
    <div style="display: flex; width: 100%; height: calc(100vh - 60px); overflow: hidden;">
        <!-- Left Sidebar -->
        <div style="width: 250px; background: white; border-right: 1px solid #e0e0e0; overflow-y: auto; flex-shrink: 0;">
            <div style="padding: 15px; border-bottom: 1px solid #e0e0e0; display: flex; justify-content: space-between; align-items: center;">
                <h3 style="font-weight: 600; font-size: 16px; margin: 0; color: #333;">Plans</h3>
                <button style="background: none; border: none; cursor: pointer; color: #666;">
                    <i class="fas fa-plus"></i>
                </button>
            </div>
            
            <div class="sidebar-item">
                <i class="fas fa-border-all" style="width: 20px; text-align: center; color: #666; font-size: 16px;"></i>
                <span style="flex: 1; font-size: 14px; margin: 0 10px;">Boundary</span>
                <span style="background: #e0e0e0; color: #666; font-size: 12px; padding: 2px 8px; border-radius: 10px; min-width: 20px; text-align: center;">1</span>
            </div>
            
            <div class="sidebar-item">
                <i class="fas fa-map" style="width: 20px; text-align: center; color: #666; font-size: 16px;"></i>
                <span style="flex: 1; font-size: 14px; margin: 0 10px;">OSMM</span>
                <span style="background: #e0e0e0; color: #666; font-size: 12px; padding: 2px 8px; border-radius: 10px; min-width: 20px; text-align: center;">1</span>
            </div>
            
            <div class="sidebar-item">
                <i class="fas fa-database" style="width: 20px; text-align: center; color: #666; font-size: 16px;"></i>
                <span style="flex: 1; font-size: 14px; margin: 0 10px;">HPA Data</span>
                <span style="background: #e0e0e0; color: #666; font-size: 12px; padding: 2px 8px; border-radius: 10px; min-width: 20px; text-align: center;">1</span>
            </div>
            
            <div class="sidebar-item active">
                <i class="fas fa-tree" style="width: 20px; text-align: center; color: #4CAF50; font-size: 16px;"></i>
                <span style="flex: 1; font-size: 14px; margin: 0 10px;">BLE1</span>
                <span style="background: #e0e0e0; color: #666; font-size: 12px; padding: 2px 8px; border-radius: 10px; min-width: 20px; text-align: center;">1</span>
            </div>
            
            <div class="sidebar-item">
                <i class="fas fa-water" style="width: 20px; text-align: center; color: #666; font-size: 16px;"></i>
                <span style="flex: 1; font-size: 14px; margin: 0 10px;">EWCO</span>
                <span style="background: #e0e0e0; color: #666; font-size: 12px; padding: 2px 8px; border-radius: 10px; min-width: 20px; text-align: center;">1</span>
            </div>
            
            <div class="sidebar-item">
                <i class="fas fa-chart-line" style="width: 20px; text-align: center; color: #666; font-size: 16px;"></i>
                <span style="flex: 1; font-size: 14px; margin: 0 10px;">e-planner</span>
                <span style="background: #e0e0e0; color: #666; font-size: 12px; padding: 2px 8px; border-radius: 10px; min-width: 20px; text-align: center;">1</span>
            </div>
            
            <div class="sidebar-item">
                <i class="fas fa-shield-alt" style="width: 20px; text-align: center; color: #666; font-size: 16px;"></i>
                <span style="flex: 1; font-size: 14px; margin: 0 10px;">Hedge survey</span>
                <span style="background: #e0e0e0; color: #666; font-size: 12px; padding: 2px 8px; border-radius: 10px; min-width: 20px; text-align: center;">1</span>
            </div>
            
            <div class="sidebar-item">
                <i class="fas fa-project-diagram" style="width: 20px; text-align: center; color: #666; font-size: 16px;"></i>
                <span style="flex: 1; font-size: 14px; margin: 0 10px;">SFI Designs</span>
                <span style="background: #e0e0e0; color: #666; font-size: 12px; padding: 2px 8px; border-radius: 10px; min-width: 20px; text-align: center;">7</span>
            </div>
            
            <div style="padding: 15px; border-bottom: 1px solid #e0e0e0; margin-top: 20px; border-top: 1px solid #e0e0e0;">
                <h3 style="font-weight: 600; font-size: 16px; margin: 0; color: #333;">Other information</h3>
            </div>
            
            <div class="sidebar-item">
                <i class="fas fa-file-alt" style="width: 20px; text-align: center; color: #666; font-size: 16px;"></i>
                <span style="flex: 1; font-size: 14px; margin: 0 10px;">Lucerne</span>
                <span style="background: #e0e0e0; color: #666; font-size: 12px; padding: 2px 8px; border-radius: 10px; min-width: 20px; text-align: center;">1</span>
            </div>
        </div>
        
        <!-- Right Map Area -->
        <div style="flex: 1; position: relative; background: #e0e0e0; height: 100%;">
            <!-- Tab Navigation -->
            <div style="position: absolute; top: 20px; left: 50%; transform: translateX(-50%); background: white; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); display: flex; overflow: hidden; z-index: 1001; border: 1px solid #e0e0e0;">
                <div style="padding: 12px 24px; background: #4CAF50; color: white; font-size: 14px; font-weight: 500; min-width: 140px; text-align: center;">
                    🗺️ Mapping View
                </div>
                <div style="padding: 12px 24px; background: white; color: #666; font-size: 14px; font-weight: 500; border-left: 1px solid #e0e0e0; min-width: 140px; text-align: center; cursor: pointer;">
                    📊 Analytics View
                </div>
            </div>
            
            <!-- Drawing Tools -->
            <div style="position: absolute; top: 20px; left: 20px; background: white; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); display: flex; gap: 5px; padding: 5px; z-index: 1000;">
                <button style="width: 36px; height: 36px; border: none; background: none; cursor: pointer; border-radius: 4px; display: flex; align-items: center; justify-content: center; color: #666; font-size: 16px;" title="Select">
                    <i class="fas fa-mouse-pointer"></i>
                </button>
                <button style="width: 36px; height: 36px; border: none; background: #4CAF50; color: white; cursor: pointer; border-radius: 4px; display: flex; align-items: center; justify-content: center; font-size: 16px;" title="Draw Polygon">
                    <i class="fas fa-draw-polygon"></i>
                </button>
                <button style="width: 36px; height: 36px; border: none; background: none; cursor: pointer; border-radius: 4px; display: flex; align-items: center; justify-content: center; color: #666; font-size: 16px;" title="Draw Rectangle">
                    <i class="fas fa-vector-square"></i>
                </button>
                <button style="width: 36px; height: 36px; border: none; background: none; cursor: pointer; border-radius: 4px; display: flex; align-items: center; justify-content: center; color: #666; font-size: 16px;" title="Draw Circle">
                    <i class="fas fa-circle"></i>
                </button>
                <button style="width: 36px; height: 36px; border: none; background: none; cursor: pointer; border-radius: 4px; display: flex; align-items: center; justify-content: center; color: #666; font-size: 16px;" title="Measure">
                    <i class="fas fa-ruler"></i>
                </button>
            </div>
            
            <!-- Map Controls -->
            <div style="position: absolute; top: 20px; right: 20px; display: flex; flex-direction: column; gap: 10px; z-index: 1000;">
                <button style="background: white; border: 1px solid #ddd; width: 40px; height: 40px; border-radius: 4px; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 18px; color: #666;" title="Zoom In">
                    <i class="fas fa-plus"></i>
                </button>
                <button style="background: white; border: 1px solid #ddd; width: 40px; height: 40px; border-radius: 4px; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 18px; color: #666;" title="Zoom Out">
                    <i class="fas fa-minus"></i>
                </button>
                <button style="background: white; border: 1px solid #ddd; width: 40px; height: 40px; border-radius: 4px; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 18px; color: #666;" title="Locate">
                    <i class="fas fa-crosshairs"></i>
                </button>
                <button style="background: white; border: 1px solid #ddd; width: 40px; height: 40px; border-radius: 4px; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 18px; color: #666;" title="Fullscreen">
                    <i class="fas fa-expand"></i>
                </button>
            </div>
            
            <!-- Map will be rendered here by Streamlit -->
            <div id="map-container" style="position: absolute; top: 80px; left: 0; right: 0; bottom: 0;">
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Render the map
    render_map_in_container()

def render_map_in_container():
    """Render the map to fill the container"""
    
    if not FOLIUM_AVAILABLE:
        st.error("❌ Folium not available. Please install: pip install folium streamlit-folium")
        return
    
    # Create map centered on Norney Farm
    m = folium.Map(
        location=[51.1867, -0.5749],
        zoom_start=15,
        tiles="OpenStreetMap"
    )
    
    # Add sample farm areas
    # Woodland area (green)
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
        popup=folium.Popup("Woodland Area<br>19.94 hectares", parse_html=True),
        tooltip="Woodland - Click for details"
    ).add_to(m)
    
    # Grassland area (blue)
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
        popup=folium.Popup("Grassland Area<br>30.62 hectares", parse_html=True),
        tooltip="Grassland - Click for details"
    ).add_to(m)
    
    # Buffer zone (cross-hatched pattern effect)
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
        popup=folium.Popup("Buffer Strip<br>0.48 hectares", parse_html=True),
        tooltip="Buffer Strip - Click for details"
    ).add_to(m)
    
    # Add drawing tools
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
            'circle': False,
            'marker': False,
            'circlemarker': False,
            'polyline': False
        }
    )
    draw.add_to(m)
    
    # Display map filling the available space
    map_data = st_folium(
        m, 
        width="100%", 
        height=600, 
        returned_objects=["all_drawings", "last_object_clicked"],
        key="main_mapping_interface"
    )
    
    # Handle interactions
    if map_data['all_drawings'] or map_data['last_object_clicked']:
        if not st.session_state.show_info_panel:
            st.session_state.show_info_panel = True
            st.rerun()

def render_info_panel():
    """Render the information panel"""
    
    st.markdown('''
    <div class="info-panel">
        <div class="info-panel-header">
            <h3 class="info-panel-title">Selected Parcel Information</h3>
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
    
    # Close button
    if st.button("✕ Close", key="close_info", help="Close information panel"):
        st.session_state.show_info_panel = False
        st.rerun()

def render_analytics_interface():
    """Render analytics interface"""
    
    # Tab Navigation
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        tab_col1, tab_col2 = st.columns(2)
        with tab_col1:
            if st.button("🗺️ Mapping View", key="mapping_btn_analytics", use_container_width=True):
                st.session_state.current_view = 'mapping'
                st.rerun()
        with tab_col2:
            if st.button("📊 Analytics View", key="analytics_btn_analytics", use_container_width=True):
                st.session_state.current_view = 'analytics'
                st.rerun()
    
    # Analytics Header
    st.markdown('''
    <div class="analytics-header">
        <h2 style="margin: 0; color: #333;">Nature Reporting: Norney Farm</h2>
        <p style="margin: 5px 0 0 0; color: #666;">Surrey - 68.00 ha</p>
        <p style="margin: 10px 0 0 0; color: #4CAF50; font-weight: 600;">Produce Type: Mixed Farming</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('''
        <div class="metric-card">
            <div class="metric-value">100.00%</div>
            <p class="metric-label">Habitat Cover</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown('''
        <div class="metric-card">
            <div class="metric-value">30.91%</div>
            <p class="metric-label">Connectedness</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown('''
        <div class="metric-card">
            <div class="metric-value">0.65</div>
            <p class="metric-label">NDVI Index</p>
        </div>
        ''', unsafe_allow_html=True)
    
    # Charts
    if PLOTLY_AVAILABLE:
        col4, col5 = st.columns(2)
        
        with col4:
            st.subheader("🛰️ NDVI Trend")
            dates = pd.date_range('2023-01-01', '2023-12-31', freq='M')
            ndvi_values = 0.4 + 0.3 * np.sin(2 * np.pi * np.arange(len(dates)) / 12) + np.random.normal(0, 0.05, len(dates))
            
            fig = px.line(x=dates, y=ndvi_values, title="Vegetation Health")
            fig.update_layout(height=300, showlegend=False)
            fig.update_traces(line_color='#4CAF50')
            st.plotly_chart(fig, use_container_width=True)
        
        with col5:
            st.subheader("🌾 Land Use")
            land_use = ['Woodland', 'Grassland', 'Crops', 'Buffer']
            areas = [19.94, 30.62, 17.0, 0.48]
            
            fig = px.pie(values=areas, names=land_use, title="Area Distribution")
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()