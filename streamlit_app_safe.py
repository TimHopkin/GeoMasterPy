"""
GeoMasterPy Streamlit App - Safe Version
A simplified version guaranteed to work with basic dependencies
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date

# Configure page
st.set_page_config(
    page_title="GeoMasterPy - Safe Mode",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Check optional dependencies
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

try:
    import folium
    from streamlit_folium import st_folium
    FOLIUM_AVAILABLE = True
except ImportError:
    FOLIUM_AVAILABLE = False

try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

def main():
    """Main application"""
    
    # Header
    st.title("🌍 GeoMasterPy - Safe Mode")
    st.markdown("**Interactive Geospatial Analysis Tool**")
    
    # System status
    st.subheader("🔧 System Status")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.success("✅ Streamlit")
        st.success("✅ Pandas") 
        st.success("✅ NumPy")
    
    with col2:
        if PLOTLY_AVAILABLE:
            st.success("✅ Plotly")
        else:
            st.error("❌ Plotly")
            
        if FOLIUM_AVAILABLE:
            st.success("✅ Folium")
        else:
            st.error("❌ Folium")
    
    with col3:
        if MATPLOTLIB_AVAILABLE:
            st.success("✅ Matplotlib")
        else:
            st.error("❌ Matplotlib")
            
        try:
            import geomasterpy
            st.success("✅ GeoMasterPy")
        except ImportError:
            st.warning("⚠️ GeoMasterPy - Demo Mode")
    
    with col4:
        try:
            import ee
            st.success("✅ Earth Engine")
        except ImportError:
            st.info("ℹ️ Earth Engine - Optional")
    
    # Navigation
    st.sidebar.title("🧭 Navigation")
    page = st.sidebar.selectbox(
        "Choose a feature:",
        [
            "🏠 Home",
            "📊 Sample Analysis",
            "🗺️ Basic Map",
            "📈 Visualization Demo",
            "📚 Getting Started"
        ]
    )
    
    if page == "🏠 Home":
        show_home()
    elif page == "📊 Sample Analysis":
        show_sample_analysis()
    elif page == "🗺️ Basic Map":
        show_basic_map()
    elif page == "📈 Visualization Demo":
        show_visualization_demo()
    elif page == "📚 Getting Started":
        show_getting_started()

def show_home():
    """Home page"""
    st.markdown("## 🚀 Welcome to GeoMasterPy!")
    
    st.markdown("""
    This is the **Safe Mode** version of GeoMasterPy, designed to work with basic dependencies.
    
    ### ✅ What's Working:
    - ✅ Basic Streamlit interface
    - ✅ Data analysis tools
    - ✅ Sample visualizations
    - ✅ Documentation and tutorials
    
    ### 🔧 Full Features (require additional setup):
    - 🗺️ Interactive Earth Engine maps
    - 🛰️ Satellite data analysis
    - 📊 Advanced geospatial analytics
    - 💾 Data export tools
    """)
    
    if st.button("🔄 Switch to Full Version"):
        st.info("To use the full version, ensure all dependencies are installed and run `streamlit_app.py`")

def show_sample_analysis():
    """Sample data analysis"""
    st.markdown("## 📊 Sample Data Analysis")
    
    # Generate sample data
    dates = pd.date_range('2023-01-01', '2023-12-31', freq='D')
    
    # Create sample NDVI data
    ndvi_data = 0.4 + 0.3 * np.sin(2 * np.pi * np.arange(len(dates)) / 365) + np.random.normal(0, 0.05, len(dates))
    
    df = pd.DataFrame({
        'Date': dates,
        'NDVI': ndvi_data,
        'Temperature': 15 + 10 * np.sin(2 * np.pi * np.arange(len(dates)) / 365) + np.random.normal(0, 2, len(dates)),
        'Precipitation': np.random.exponential(2, len(dates))
    })
    
    st.markdown("### 📈 Sample Environmental Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Avg NDVI", f"{df['NDVI'].mean():.3f}", f"{df['NDVI'].std():.3f}")
        st.metric("Avg Temperature", f"{df['Temperature'].mean():.1f}°C", f"{df['Temperature'].std():.1f}")
    
    with col2:
        st.metric("Total Precipitation", f"{df['Precipitation'].sum():.1f}mm", f"{df['Precipitation'].std():.1f}")
        st.metric("Data Points", len(df), "365 days")
    
    # Show data
    st.markdown("### 📊 Data Table")
    st.dataframe(df.head(10))
    
    # Visualization
    if PLOTLY_AVAILABLE:
        st.markdown("### 📈 Time Series Visualization")
        
        fig = px.line(df, x='Date', y=['NDVI', 'Temperature'], 
                     title="Environmental Parameters Over Time")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Install Plotly for advanced visualizations: `pip install plotly`")

def show_basic_map():
    """Basic map functionality"""
    st.markdown("## 🗺️ Basic Map")
    
    if FOLIUM_AVAILABLE:
        st.markdown("### 🌍 Interactive Map")
        
        # Create a basic folium map
        center_lat = 37.7749
        center_lon = -122.4194
        
        m = folium.Map(location=[center_lat, center_lon], zoom_start=10)
        
        # Add a marker
        folium.Marker(
            [center_lat, center_lon],
            popup="San Francisco, CA",
            tooltip="Click for info"
        ).add_to(m)
        
        # Display map
        st_folium(m, width=700, height=500)
        
    else:
        st.warning("Install Folium for maps: `pip install folium streamlit-folium`")
        
        # Show static info instead
        st.info("📍 Map functionality requires Folium installation")
        st.code("pip install folium streamlit-folium")

def show_visualization_demo():
    """Visualization demo"""
    st.markdown("## 📈 Visualization Demo")
    
    # Generate sample data
    data = {
        'Land Cover': ['Forest', 'Agriculture', 'Urban', 'Water', 'Bare Soil'],
        'Area (km²)': [450, 320, 180, 75, 125],
        'Percentage': [38.7, 27.6, 15.5, 6.5, 10.8]
    }
    
    df = pd.DataFrame(data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Land Cover Data")
        st.dataframe(df)
    
    with col2:
        if PLOTLY_AVAILABLE:
            st.markdown("### 🥧 Land Cover Distribution")
            fig = px.pie(df, values='Percentage', names='Land Cover', 
                        title="Land Cover Distribution")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown("### 📊 Land Cover Distribution")
            st.bar_chart(df.set_index('Land Cover')['Percentage'])
    
    # Additional charts
    if PLOTLY_AVAILABLE:
        st.markdown("### 📊 Area Comparison")
        fig = px.bar(df, x='Land Cover', y='Area (km²)', 
                    title="Land Cover Areas")
        st.plotly_chart(fig, use_container_width=True)

def show_getting_started():
    """Getting started guide"""
    st.markdown("## 📚 Getting Started with GeoMasterPy")
    
    tab1, tab2, tab3 = st.tabs(["🚀 Quick Start", "📦 Installation", "💡 Examples"])
    
    with tab1:
        st.markdown("""
        ### 🚀 Quick Start Guide
        
        1. **Check System Status** - Verify all dependencies are working
        2. **Try Sample Analysis** - Explore the data analysis tools
        3. **View Basic Map** - Test the mapping functionality
        4. **Run Visualization Demo** - See the charting capabilities
        
        ### 🔧 For Full Functionality:
        
        ```bash
        # Install all dependencies
        pip install -r requirements_streamlit.txt
        
        # Run full application
        streamlit run streamlit_app.py
        ```
        """)
    
    with tab2:
        st.markdown("""
        ### 📦 Installation Guide
        
        #### Minimum Requirements:
        ```bash
        pip install streamlit pandas numpy
        ```
        
        #### Recommended (for maps):
        ```bash
        pip install folium streamlit-folium
        ```
        
        #### Full Features:
        ```bash
        pip install plotly matplotlib earthengine-api
        ```
        
        #### Complete Installation:
        ```bash
        pip install -r requirements_streamlit.txt
        ```
        """)
    
    with tab3:
        st.markdown("""
        ### 💡 Code Examples
        
        #### Basic Usage:
        ```python
        import geomasterpy as gmp
        import streamlit as st
        
        # Create interactive map
        Map = gmp.Map(center=(37.7749, -122.4194), zoom=10)
        
        # Display in Streamlit
        st.components.v1.html(Map._repr_html_(), height=500)
        ```
        
        #### Data Analysis:
        ```python
        import pandas as pd
        import streamlit as st
        
        # Load and display data
        df = pd.read_csv('your_data.csv')
        st.dataframe(df)
        st.line_chart(df)
        ```
        """)

if __name__ == "__main__":
    main()