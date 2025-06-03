"""
GeoMasterPy Simple Streamlit App - Guaranteed to Work
"""

import streamlit as st

# Configure page - MUST be first
st.set_page_config(
    page_title="GeoMasterPy - Simple Version",
    page_icon="🌍",
    layout="wide"
)

# Basic imports
import pandas as pd
import numpy as np

# Check optional imports
try:
    import plotly.express as px
    PLOTLY_OK = True
except ImportError:
    PLOTLY_OK = False

try:
    import folium
    from streamlit_folium import st_folium
    FOLIUM_OK = True
except ImportError:
    FOLIUM_OK = False

# Main app
def main():
    st.title("🌍 GeoMasterPy - Simple Web App")
    st.markdown("**Interactive Geospatial Analysis for Google Earth Engine**")
    
    # Status check
    st.subheader("🔧 System Status")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.success("✅ Streamlit")
    with col2:
        st.success("✅ Pandas") 
    with col3:
        if PLOTLY_OK:
            st.success("✅ Plotly")
        else:
            st.error("❌ Plotly")
    with col4:
        if FOLIUM_OK:
            st.success("✅ Folium")
        else:
            st.error("❌ Folium")
    
    # Features
    st.subheader("🚀 Available Features")
    
    tab1, tab2, tab3 = st.tabs(["📊 Data Demo", "🗺️ Map Demo", "📖 Info"])
    
    with tab1:
        st.markdown("### Sample Data Analysis")
        
        # Create sample data
        data = pd.DataFrame({
            'Date': pd.date_range('2024-01-01', periods=12, freq='M'),
            'NDVI': np.random.uniform(0.2, 0.8, 12),
            'Temperature': np.random.uniform(15, 35, 12),
            'Precipitation': np.random.uniform(0, 100, 12)
        })
        
        st.dataframe(data)
        
        if PLOTLY_OK:
            fig = px.line(data, x='Date', y=['NDVI', 'Temperature'], 
                         title="Sample Time Series Data")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Install plotly to see interactive charts")
    
    with tab2:
        st.markdown("### Interactive Map Demo")
        
        if FOLIUM_OK:
            # Create a simple map
            m = folium.Map(location=[37.7749, -122.4194], zoom_start=10)
            folium.Marker([37.7749, -122.4194], 
                         popup="San Francisco", 
                         tooltip="Click for info").add_to(m)
            
            st_folium(m, width=700, height=500)
        else:
            st.warning("Install folium and streamlit-folium to see interactive maps")
            st.info("Expected: Interactive map of San Francisco would appear here")
    
    with tab3:
        st.markdown("### About GeoMasterPy")
        
        st.markdown("""
        **GeoMasterPy** is a comprehensive library for Google Earth Engine analysis.
        
        **Features:**
        - 🗺️ Interactive mapping
        - 📊 Data analysis tools  
        - 🛰️ Satellite image processing
        - 📈 Visualization capabilities
        - 💾 Data export functions
        
        **GitHub:** https://github.com/TimHopkin/GeoMasterPy
        
        **Requirements to test:**
        ```
        streamlit
        plotly  
        folium
        streamlit-folium
        pandas
        numpy
        ```
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("🌍 **GeoMasterPy** - Making Earth Engine accessible to everyone!")

if __name__ == "__main__":
    main()