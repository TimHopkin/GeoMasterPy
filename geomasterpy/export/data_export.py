"""
Data Export Functions for GeoMasterPy

Provides functions for exporting Earth Engine data to local files.
"""

import ee
import os
import time
import requests
import zipfile
import json
from typing import Dict, List, Any, Optional, Union
import geopandas as gpd
import pandas as pd
from shapely.geometry import shape
import rasterio
from rasterio.crs import CRS
import numpy as np


def export_image_to_local(image: ee.Image, filename: str, region: ee.Geometry,
                         scale: int = 30, crs: str = 'EPSG:4326',
                         file_format: str = 'GeoTIFF') -> str:
    """
    Export an Earth Engine image to a local file.
    
    Args:
        image: Earth Engine Image to export
        filename: Output filename (without extension)
        region: Region to export
        scale: Export scale in meters
        crs: Coordinate reference system
        file_format: Export format ('GeoTIFF')
        
    Returns:
        Path to exported file
    """
    try:
        # Clip image to region
        clipped_image = image.clip(region)
        
        # Get download URL
        url = clipped_image.getDownloadURL({
            'scale': scale,
            'crs': crs,
            'region': region.getInfo(),
            'format': file_format
        })
        
        # Download the file
        response = requests.get(url)
        
        if response.status_code == 200:
            # Save as zip file first
            zip_filename = f"{filename}.zip"
            with open(zip_filename, 'wb') as f:
                f.write(response.content)
            
            # Extract the zip file
            with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
                zip_ref.extractall(os.path.dirname(filename) or '.')
            
            # Remove zip file
            os.remove(zip_filename)
            
            # Find the extracted tif file
            directory = os.path.dirname(filename) or '.'
            for file in os.listdir(directory):
                if file.endswith('.tif'):
                    old_path = os.path.join(directory, file)
                    new_path = f"{filename}.tif"
                    os.rename(old_path, new_path)
                    print(f"Image exported to: {new_path}")
                    return new_path
            
            print("Error: No .tif file found in downloaded archive")
            return ""
            
        else:
            print(f"Error downloading image: {response.status_code}")
            return ""
            
    except Exception as e:
        print(f"Error exporting image: {str(e)}")
        return ""


def export_vector_to_local(feature_collection: ee.FeatureCollection, 
                          filename: str, file_format: str = 'SHP') -> str:
    """
    Export an Earth Engine FeatureCollection to a local vector file.
    
    Args:
        feature_collection: Earth Engine FeatureCollection
        filename: Output filename (without extension)
        file_format: Export format ('SHP', 'GeoJSON', 'KML')
        
    Returns:
        Path to exported file
    """
    try:
        # Get download URL
        if file_format.upper() == 'SHP':
            url = feature_collection.getDownloadURL('shp')
            extension = '.zip'  # Shapefile comes as zip
        elif file_format.upper() == 'GEOJSON':
            url = feature_collection.getDownloadURL('json')
            extension = '.geojson'
        elif file_format.upper() == 'KML':
            url = feature_collection.getDownloadURL('kml')
            extension = '.kml'
        else:
            print(f"Unsupported format: {file_format}")
            return ""
        
        # Download the file
        response = requests.get(url)
        
        if response.status_code == 200:
            if file_format.upper() == 'SHP':
                # Handle shapefile (comes as zip)
                zip_filename = f"{filename}.zip"
                with open(zip_filename, 'wb') as f:
                    f.write(response.content)
                
                # Extract the zip file
                with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
                    zip_ref.extractall(os.path.dirname(filename) or '.')
                
                # Remove zip file
                os.remove(zip_filename)
                
                # Find the main shapefile
                directory = os.path.dirname(filename) or '.'
                for file in os.listdir(directory):
                    if file.endswith('.shp'):
                        old_path = os.path.join(directory, file)
                        new_path = f"{filename}.shp"
                        
                        # Also rename associated files
                        base_old = os.path.splitext(old_path)[0]
                        base_new = os.path.splitext(new_path)[0]
                        
                        for ext in ['.shp', '.shx', '.dbf', '.prj']:
                            if os.path.exists(base_old + ext):
                                os.rename(base_old + ext, base_new + ext)
                        
                        print(f"Vector data exported to: {new_path}")
                        return new_path
                
                print("Error: No .shp file found in downloaded archive")
                return ""
            else:
                # Handle other formats
                output_file = f"{filename}{extension}"
                with open(output_file, 'wb') as f:
                    f.write(response.content)
                
                print(f"Vector data exported to: {output_file}")
                return output_file
        else:
            print(f"Error downloading vector data: {response.status_code}")
            return ""
            
    except Exception as e:
        print(f"Error exporting vector data: {str(e)}")
        return ""


def extract_values_to_points(image: ee.Image, points: ee.FeatureCollection,
                           scale: int = 30, bands: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Extract image values at point locations and return as DataFrame.
    
    Args:
        image: Earth Engine Image
        points: FeatureCollection of point geometries
        scale: Scale for value extraction
        bands: List of bands to extract (if None, uses all)
        
    Returns:
        Pandas DataFrame with extracted values
    """
    try:
        if bands is not None:
            image = image.select(bands)
        
        # Sample image at points
        sampled = image.sampleRegions(
            collection=points,
            scale=scale,
            tileScale=8,
            geometries=True
        )
        
        # Convert to pandas DataFrame
        data = sampled.getInfo()
        
        rows = []
        for feature in data['features']:
            props = feature['properties'].copy()
            
            # Add coordinates
            geom = feature['geometry']
            if geom['type'] == 'Point':
                coords = geom['coordinates']
                props['longitude'] = coords[0]
                props['latitude'] = coords[1]
            
            rows.append(props)
        
        df = pd.DataFrame(rows)
        return df
        
    except Exception as e:
        print(f"Error extracting values to points: {str(e)}")
        return pd.DataFrame()


def export_image_to_drive(image: ee.Image, description: str, folder: str = 'EarthEngine',
                         region: ee.Geometry = None, scale: int = 30,
                         crs: str = 'EPSG:4326', max_pixels: int = 1e9) -> ee.batch.Task:
    """
    Export an Earth Engine image to Google Drive.
    
    Args:
        image: Earth Engine Image
        description: Export description/filename
        folder: Google Drive folder name
        region: Export region (if None, uses image bounds)
        scale: Export scale in meters
        crs: Coordinate reference system
        max_pixels: Maximum number of pixels
        
    Returns:
        Earth Engine export task
    """
    try:
        if region is None:
            region = image.geometry()
        
        task = ee.batch.Export.image.toDrive(
            image=image,
            description=description,
            folder=folder,
            region=region,
            scale=scale,
            crs=crs,
            maxPixels=max_pixels
        )
        
        task.start()
        print(f"Export task started: {description}")
        print(f"Task ID: {task.id}")
        return task
        
    except Exception as e:
        print(f"Error starting export task: {str(e)}")
        return None


def export_table_to_drive(feature_collection: ee.FeatureCollection, description: str,
                         folder: str = 'EarthEngine', file_format: str = 'CSV') -> ee.batch.Task:
    """
    Export an Earth Engine FeatureCollection to Google Drive.
    
    Args:
        feature_collection: Earth Engine FeatureCollection
        description: Export description/filename
        folder: Google Drive folder name
        file_format: Export format ('CSV', 'SHP', 'GeoJSON', 'KML')
        
    Returns:
        Earth Engine export task
    """
    try:
        task = ee.batch.Export.table.toDrive(
            collection=feature_collection,
            description=description,
            folder=folder,
            fileFormat=file_format
        )
        
        task.start()
        print(f"Export task started: {description}")
        print(f"Task ID: {task.id}")
        return task
        
    except Exception as e:
        print(f"Error starting export task: {str(e)}")
        return None


def check_task_status(task: ee.batch.Task) -> str:
    """
    Check the status of an Earth Engine export task.
    
    Args:
        task: Earth Engine task
        
    Returns:
        Task status string
    """
    try:
        status = task.status()
        state = status['state']
        
        if state == 'COMPLETED':
            print(f"Task {task.id} completed successfully")
        elif state == 'FAILED':
            print(f"Task {task.id} failed: {status.get('error_message', 'Unknown error')}")
        elif state == 'RUNNING':
            print(f"Task {task.id} is running... Progress: {status.get('progress', 0):.1%}")
        else:
            print(f"Task {task.id} status: {state}")
        
        return state
        
    except Exception as e:
        print(f"Error checking task status: {str(e)}")
        return "ERROR"


def wait_for_task(task: ee.batch.Task, timeout: int = 300) -> bool:
    """
    Wait for an Earth Engine task to complete.
    
    Args:
        task: Earth Engine task
        timeout: Maximum wait time in seconds
        
    Returns:
        True if completed successfully, False otherwise
    """
    import time
    
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        status = check_task_status(task)
        
        if status == 'COMPLETED':
            return True
        elif status in ['FAILED', 'CANCELLED']:
            return False
        
        time.sleep(10)  # Wait 10 seconds before checking again
    
    print(f"Task timed out after {timeout} seconds")
    return False


def export_time_series(image_collection: ee.ImageCollection, region: ee.Geometry,
                      description: str, scale: int = 30,
                      reducer: str = 'mean') -> pd.DataFrame:
    """
    Export time series data from an ImageCollection.
    
    Args:
        image_collection: Earth Engine ImageCollection
        region: Region to extract time series from
        description: Description for the export
        scale: Scale for reduction
        reducer: Reduction method
        
    Returns:
        Pandas DataFrame with time series data
    """
    try:
        # Define reducer
        reducer_dict = {
            'mean': ee.Reducer.mean(),
            'median': ee.Reducer.median(),
            'sum': ee.Reducer.sum(),
            'min': ee.Reducer.min(),
            'max': ee.Reducer.max()
        }
        
        ee_reducer = reducer_dict.get(reducer, ee.Reducer.mean())
        
        # Extract time series
        def extract_values(image):
            # Reduce image to single value
            reduced = image.reduceRegion(
                reducer=ee_reducer,
                geometry=region,
                scale=scale,
                maxPixels=1e9
            )
            
            # Get date
            date = image.date().format('YYYY-MM-dd')
            
            # Return feature with date and values
            return ee.Feature(None, reduced.set('date', date))
        
        # Map over collection
        time_series = image_collection.map(extract_values)
        
        # Export to drive as CSV
        task = export_table_to_drive(time_series, f"{description}_timeseries", file_format='CSV')
        
        # Also get data directly for return
        data = time_series.getInfo()
        
        rows = []
        for feature in data['features']:
            rows.append(feature['properties'])
        
        df = pd.DataFrame(rows)
        
        # Convert date column to datetime
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
        
        return df
        
    except Exception as e:
        print(f"Error exporting time series: {str(e)}")
        return pd.DataFrame()