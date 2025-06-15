#!/usr/bin/env python3
"""Debug script to test GeoMasterPy Streamlit app"""

import sys
import subprocess
import time
import threading
import signal
import os

def run_streamlit():
    """Run streamlit and capture output"""
    try:
        # Change to the correct directory
        os.chdir("/Users/timhopkin/Documents/Software Development/GIS tool GEE/GeoMasterPy")
        
        # Run streamlit
        cmd = [sys.executable, "-m", "streamlit", "run", "streamlit_app.py", "--server.port", "8503"]
        
        print("Starting Streamlit app...")
        print(f"Command: {' '.join(cmd)}")
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Monitor output for errors
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(f"STDOUT: {output.strip()}")
                
            # Check for errors
            error = process.stderr.readline()
            if error:
                print(f"STDERR: {error.strip()}")
                
            # Check if app started successfully
            if "You can now view your Streamlit app in your browser" in output:
                print("\n✅ SUCCESS: App started successfully!")
                print("App should be available at: http://localhost:8503")
                break
                
            # Check for specific error patterns
            if "Error" in output or "Exception" in output:
                print(f"\n❌ ERROR DETECTED: {output.strip()}")
                
        # Let it run for a few seconds then terminate
        time.sleep(3)
        process.terminate()
        
        return_code = process.wait()
        print(f"\nProcess finished with return code: {return_code}")
        
    except Exception as e:
        print(f"Error running streamlit: {e}")

if __name__ == "__main__":
    run_streamlit()