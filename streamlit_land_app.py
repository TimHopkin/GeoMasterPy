"""
Land App - Streamlit Web Interface
A specialized land management application with interactive mapping and drawing tools.
"""

import streamlit as st
import os
from pathlib import Path

# Configure Streamlit page
st.set_page_config(
    page_title="Land App - Advanced Land Management Platform",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def main():
    """Main Streamlit application for Land App"""
    
    # Hide Streamlit components for full-screen experience
    hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display:none;}
        .stDecoration {display:none;}
        </style>
        """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    
    # Load and display the Land App HTML
    land_app_path = Path(__file__).parent / "src" / "web" / "land-app-ui-mockup.html"
    
    if land_app_path.exists():
        # Read the HTML file
        with open(land_app_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Display the HTML content
        st.components.v1.html(html_content, height=800, scrolling=True)
        
        # Add download link for the HTML file
        with st.expander("📥 Download Land App", expanded=False):
            st.markdown("### Download the standalone Land App")
            st.markdown("You can download and run this application locally or host it on any web server.")
            
            st.download_button(
                label="💾 Download HTML File",
                data=html_content,
                file_name="land-app.html",
                mime="text/html",
                help="Download the complete Land App as a single HTML file"
            )
            
            st.markdown("""
            **Usage Instructions:**
            1. Download the HTML file
            2. Open it in any modern web browser
            3. All features work offline including:
               - Interactive mapping with OpenStreetMap
               - Drawing tools (polygons, circles, rectangles, points)
               - Plans management system
               - Learning Centre with educational content
               - URL-based navigation (#map, #learning-centre)
            """)
    
    else:
        st.error("Land App HTML file not found. Please ensure the file exists at: src/web/land-app-ui-mockup.html")
        
        # Provide alternative access
        st.markdown("### Alternative Access")
        st.markdown("""
        If you're running this locally, you can access the Land App directly by opening:
        `src/web/land-app-ui-mockup.html` in your browser.
        """)

if __name__ == "__main__":
    main()