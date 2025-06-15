import streamlit as st
import pandas as pd
import numpy as np

# Simple working Streamlit app
st.set_page_config(
    page_title="GeoMasterPy - Simple Test",
    page_icon="🌍", 
    layout="wide"
)

st.title("🌍 GeoMasterPy - Simple Test")
st.write("Testing basic Streamlit functionality...")

# Test basic components
col1, col2 = st.columns(2)

with col1:
    st.subheader("Basic Test")
    st.write("✅ Streamlit is working!")
    
    # Test input
    name = st.text_input("Enter your name:", "World")
    st.write(f"Hello, {name}!")

with col2:
    st.subheader("Data Test")
    
    # Test data display
    data = pd.DataFrame({
        'x': np.random.randn(10),
        'y': np.random.randn(10)
    })
    
    st.dataframe(data)
    st.line_chart(data)

# Test dependencies
st.subheader("Dependency Check")
deps = {
    'Streamlit': '✅ Working',
    'Pandas': '✅ Working', 
    'NumPy': '✅ Working'
}

for dep, status in deps.items():
    st.write(f"{dep}: {status}")

if st.button("Test Complete!"):
    st.success("🎉 All basic tests passed!")
    st.balloons()