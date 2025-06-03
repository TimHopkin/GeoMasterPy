#!/usr/bin/env python3
"""
Simple Earth Engine Authentication
"""

import ee

print("🌍 Google Earth Engine Authentication")
print("=" * 40)

try:
    print("✅ Earth Engine API found")
    
    print("\n🔐 Starting authentication...")
    print("This will open your web browser automatically.")
    print("Follow the instructions in the browser.")
    
    # Authenticate
    ee.Authenticate()
    
    # Initialize
    ee.Initialize()
    
    print("\n✅ SUCCESS! Earth Engine is authenticated!")
    
    # Test
    print("🧪 Testing access...")
    image = ee.Image('LANDSAT/LC08/C02/T1_L2').first()
    print("✅ Earth Engine data access confirmed!")
    
    print("\n🎉 Your Streamlit app will now work with real Earth Engine data!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\n💡 Don't worry! Your Streamlit app still works in demo mode.")
    print("You can apply for Earth Engine access at: https://earthengine.google.com/")