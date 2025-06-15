#!/usr/bin/env python3
"""
Simple Earth Engine Authentication Setup
Run this script to authenticate with Google Earth Engine
"""

import sys

def setup_earth_engine():
    """Simple Earth Engine setup with clear instructions"""
    
    print("🌍 Google Earth Engine Authentication Setup")
    print("=" * 50)
    
    try:
        import ee
        print("✅ Earth Engine API is installed")
    except ImportError:
        print("❌ Earth Engine API not found. Installing...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "earthengine-api"])
        import ee
        print("✅ Earth Engine API installed successfully")
    
    print("\n🔐 Starting authentication process...")
    print("This will open your web browser.")
    print("Follow these steps:")
    print("1. Sign in to your Google account")
    print("2. Grant Earth Engine permissions")
    print("3. Copy the verification code")
    print("4. Paste it back here when prompted")
    
    input("\nPress ENTER to continue...")
    
    try:
        # Start authentication
        ee.Authenticate()
        
        # Test initialization
        ee.Initialize()
        
        print("\n✅ SUCCESS! Earth Engine is now authenticated")
        print("✅ Your Streamlit app will now show 'Earth Engine' as ready")
        
        # Test with a simple query
        print("\n🧪 Testing Earth Engine access...")
        image = ee.Image('LANDSAT/LC08/C02/T1_L2').first()
        info = image.getInfo()
        print("✅ Earth Engine data access confirmed!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Authentication failed: {e}")
        print("\n💡 Troubleshooting tips:")
        print("1. Make sure you have Earth Engine access at: https://earthengine.google.com/")
        print("2. Try running this script again")
        print("3. Make sure you're signed in to the correct Google account")
        
        return False

if __name__ == "__main__":
    success = setup_earth_engine()
    
    if success:
        print("\n🎉 All done! Your Streamlit app is ready to use Earth Engine!")
        print("Run your Streamlit app and you should see ✅ Earth Engine")
    else:
        print("\n🤔 Need help? The app will still work in demo mode.")
        
    input("\nPress ENTER to close...")