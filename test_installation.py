#!/usr/bin/env python3
"""
Quick test script to verify GeoMasterPy installation
"""

def test_installation():
    """Test basic GeoMasterPy functionality"""
    print("Testing GeoMasterPy installation...")
    
    try:
        # Test imports
        print("✓ Testing imports...")
        import geomasterpy as gmp
        print("  - geomasterpy imported successfully")
        
        import ee
        print("  - earthengine-api imported successfully")
        
        # Test Earth Engine initialization
        print("✓ Testing Earth Engine...")
        try:
            ee.Initialize()
            print("  - Earth Engine initialized successfully")
        except Exception as e:
            print(f"  ⚠️  Earth Engine initialization failed: {e}")
            print("  Please run: earthengine authenticate")
            return False
        
        # Test basic functionality
        print("✓ Testing basic functionality...")
        
        # Test map creation
        map_widget = gmp.Map(center=(40, -100), zoom=4)
        print("  - Map widget created successfully")
        
        # Test data search
        results = gmp.search_ee_data('landsat', max_results=3)
        print(f"  - Data catalog search returned {len(results)} results")
        
        # Test JavaScript conversion
        js_code = "var x = ee.Image('test'); print(x);"
        python_code = gmp.js_snippet_to_python(js_code)
        print("  - JavaScript to Python conversion working")
        
        print("\n🎉 GeoMasterPy installation test PASSED!")
        print("\nYou can now:")
        print("1. Start Jupyter: jupyter notebook")
        print("2. Open examples/01_basic_usage.ipynb")
        print("3. Or create your own notebook and import geomasterpy")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("\nTry installing missing dependencies:")
        print("pip install -r requirements.txt")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


if __name__ == "__main__":
    test_installation()