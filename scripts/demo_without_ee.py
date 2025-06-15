#!/usr/bin/env python3
"""
Demo script showing GeoMasterPy functionality without Earth Engine authentication
"""

import geomasterpy as gmp
from unittest.mock import Mock, patch
import matplotlib.pyplot as plt
import numpy as np

def demo_without_earth_engine():
    """Demonstrate GeoMasterPy features without requiring Earth Engine authentication"""
    
    print("🌍 GeoMasterPy Demo (No Earth Engine Required)")
    print("=" * 50)
    
    # Test 1: Basic Map Creation
    print("\n✓ Testing Map Creation...")
    try:
        with patch('ee.Initialize'):  # Mock Earth Engine
            map_widget = gmp.Map(center=(37.7749, -122.4194), zoom=10)
            print(f"  - Map created successfully: center={map_widget.center}, zoom={map_widget.zoom}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # Test 2: Data Catalog Search
    print("\n✓ Testing Data Catalog...")
    try:
        with patch('ee.Initialize'):
            results = gmp.search_ee_data('landsat', max_results=3)
            print(f"  - Found {len(results)} Landsat datasets:")
            for i, result in enumerate(results[:2], 1):
                print(f"    {i}. {result['title']}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # Test 3: JavaScript to Python Conversion
    print("\n✓ Testing JavaScript Conversion...")
    try:
        js_code = """
        var image = ee.Image('LANDSAT/LC08/C02/T1_L2/LC08_044034_20140318');
        var ndvi = image.normalizedDifference(['B5', 'B4']);
        print(ndvi);
        Map.addLayer(ndvi, {min: -1, max: 1, palette: ['blue', 'white', 'green']}, 'NDVI');
        """
        
        python_code = gmp.js_snippet_to_python(js_code)
        print("  - JavaScript code converted to Python:")
        print("    Original JS:")
        for line in js_code.strip().split('\n'):
            if line.strip():
                print(f"      {line.strip()}")
        print("    Converted Python:")
        for line in python_code.strip().split('\n')[:4]:  # Show first few lines
            if line.strip():
                print(f"      {line.strip()}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # Test 4: Visualization Tools (Static Plot)
    print("\n✓ Testing Visualization Tools...")
    try:
        # Create a sample plot using matplotlib (simulating Earth Engine data)
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Generate sample NDVI data
        x = np.linspace(-122.5, -122.0, 100)
        y = np.linspace(37.5, 38.0, 100)
        X, Y = np.meshgrid(x, y)
        Z = np.sin(10 * X) * np.cos(10 * Y) * 0.5 + 0.2  # Simulate NDVI values
        
        # Create a nice NDVI-style plot
        im = ax.contourf(X, Y, Z, levels=20, cmap='RdYlGn', vmin=-1, vmax=1)
        ax.set_title('Sample NDVI Data (Simulated)', fontsize=14, fontweight='bold')
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('NDVI')
        
        plt.tight_layout()
        
        # Save the plot
        output_file = "/Users/timhopkin/Documents/Software Development/GIS tool GEE/GeoMasterPy/sample_ndvi_plot.png"
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"  - Sample NDVI visualization saved to: sample_ndvi_plot.png")
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # Test 5: Show available basemaps
    print("\n✓ Available Basemaps:")
    basemaps = [
        'OpenStreetMap', 'CartoDB.Positron', 'CartoDB.DarkMatter',
        'Esri.WorldImagery', 'Esri.WorldTopoMap', 'Stamen.Terrain',
        'Google.Satellite', 'Google.Hybrid'
    ]
    for basemap in basemaps:
        print(f"  - {basemap}")
    
    print("\n🎉 Demo completed successfully!")
    print("\n📚 Next Steps:")
    print("1. Authenticate Earth Engine by visiting the URL that was shown earlier")
    print("2. Complete the authentication in your web browser")
    print("3. Run: python3 test_installation.py")
    print("4. Start Jupyter: python3 -m jupyter notebook")
    print("5. Open examples/01_basic_usage.ipynb")
    
    print("\n💡 Quick Start with Jupyter:")
    print("   cd '/Users/timhopkin/Documents/Software Development/GIS tool GEE/GeoMasterPy'")
    print("   python3 -m jupyter notebook")
    
    return True

if __name__ == "__main__":
    demo_without_earth_engine()