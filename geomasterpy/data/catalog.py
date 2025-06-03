"""
Earth Engine Data Catalog and Conversion Utilities
"""

import ee
import re
import requests
from typing import List, Dict, Any, Optional
import json


def search_ee_data(keywords: str, max_results: int = 20) -> List[Dict[str, Any]]:
    """
    Search the Google Earth Engine data catalog.
    
    Args:
        keywords: Search terms
        max_results: Maximum number of results to return
        
    Returns:
        List of dictionaries containing dataset information
    """
    try:
        # Initialize EE if needed
        try:
            ee.Initialize()
        except:
            print("Warning: Earth Engine not initialized")
            return []
        
        # Common Earth Engine datasets with metadata
        common_datasets = {
            'landsat': [
                {
                    'id': 'LANDSAT/LC08/C02/T1_L2',
                    'title': 'Landsat 8 Collection 2 Tier 1 Level-2',
                    'description': 'Atmospherically corrected surface reflectance',
                    'provider': 'USGS',
                    'tags': ['landsat', 'surface reflectance', 'optical']
                },
                {
                    'id': 'LANDSAT/LE07/C02/T1_L2', 
                    'title': 'Landsat 7 Collection 2 Tier 1 Level-2',
                    'description': 'Atmospherically corrected surface reflectance',
                    'provider': 'USGS',
                    'tags': ['landsat', 'surface reflectance', 'optical']
                }
            ],
            'sentinel': [
                {
                    'id': 'COPERNICUS/S2_SR_HARMONIZED',
                    'title': 'Sentinel-2 MSI: MultiSpectral Instrument, Level-2A',
                    'description': 'Bottom-of-atmosphere reflectance',
                    'provider': 'European Space Agency',
                    'tags': ['sentinel', 'surface reflectance', 'optical']
                },
                {
                    'id': 'COPERNICUS/S1_GRD',
                    'title': 'Sentinel-1 SAR GRD: C-band Synthetic Aperture Radar',
                    'description': 'Ground Range Detected SAR imagery',
                    'provider': 'European Space Agency', 
                    'tags': ['sentinel', 'radar', 'sar']
                }
            ],
            'modis': [
                {
                    'id': 'MODIS/061/MOD13Q1',
                    'title': 'MOD13Q1.061 Terra Vegetation Indices 16-Day Global 250m',
                    'description': 'NDVI and EVI vegetation indices',
                    'provider': 'NASA',
                    'tags': ['modis', 'vegetation', 'ndvi', 'evi']
                },
                {
                    'id': 'MODIS/061/MCD12Q1',
                    'title': 'MCD12Q1.061 MODIS Land Cover Type Yearly Global 500m',
                    'description': 'Annual land cover classification',
                    'provider': 'NASA',
                    'tags': ['modis', 'land cover', 'classification']
                }
            ],
            'climate': [
                {
                    'id': 'ECMWF/ERA5_LAND/HOURLY',
                    'title': 'ERA5-Land Hourly - ECMWF climate reanalysis',
                    'description': 'Land surface reanalysis data',
                    'provider': 'ECMWF',
                    'tags': ['climate', 'temperature', 'precipitation', 'era5']
                },
                {
                    'id': 'UCSB-CHG/CHIRPS/DAILY',
                    'title': 'CHIRPS Daily: Climate Hazards Group InfraRed Precipitation',
                    'description': 'Daily precipitation estimates',
                    'provider': 'UCSB',
                    'tags': ['precipitation', 'climate', 'chirps']
                }
            ],
            'elevation': [
                {
                    'id': 'USGS/SRTMGL1_003',
                    'title': 'NASA SRTM Digital Elevation 30m',
                    'description': '30-meter resolution digital elevation model',
                    'provider': 'NASA/USGS',
                    'tags': ['elevation', 'dem', 'srtm', 'topography']
                },
                {
                    'id': 'NASA/NASADEM_HGT/001',
                    'title': 'NASADEM: NASA NASADEM Digital Elevation 30m',
                    'description': 'Improved SRTM-based digital elevation model',
                    'provider': 'NASA',
                    'tags': ['elevation', 'dem', 'nasadem', 'topography']
                }
            ],
            'population': [
                {
                    'id': 'WorldPop/GP/100m/pop',
                    'title': 'WorldPop Global Project Population Data',
                    'description': 'Population counts and densities',
                    'provider': 'WorldPop',
                    'tags': ['population', 'demographics', 'worldpop']
                }
            ]
        }
        
        # Search through common datasets
        results = []
        keywords_lower = keywords.lower()
        
        for category, datasets in common_datasets.items():
            if keywords_lower in category or any(keyword in keywords_lower.split() for keyword in [category]):
                results.extend(datasets)
            else:
                # Search within dataset metadata
                for dataset in datasets:
                    if (keywords_lower in dataset['title'].lower() or 
                        keywords_lower in dataset['description'].lower() or
                        any(keyword in dataset['tags'] for keyword in keywords_lower.split())):
                        results.append(dataset)
        
        # Remove duplicates and limit results
        seen_ids = set()
        unique_results = []
        for result in results:
            if result['id'] not in seen_ids:
                seen_ids.add(result['id'])
                unique_results.append(result)
                if len(unique_results) >= max_results:
                    break
        
        return unique_results
        
    except Exception as e:
        print(f"Error searching Earth Engine catalog: {str(e)}")
        return []


def js_snippet_to_python(js_code: str) -> str:
    """
    Convert Google Earth Engine JavaScript code snippets to Python.
    
    Args:
        js_code: JavaScript code string
        
    Returns:
        Converted Python code string
    """
    python_code = js_code
    
    # Basic conversions
    conversions = [
        # Variable declarations
        (r'\bvar\s+', ''),
        (r'\blet\s+', ''),
        (r'\bconst\s+', ''),
        
        # Comments
        (r'//', '#'),
        
        # Print statements
        (r'\bprint\s*\(', 'print('),
        
        # Map operations
        (r'Map\.addLayer\s*\(', 'Map.add_ee_layer('),
        (r'Map\.centerObject\s*\(', 'Map.center_object('),
        (r'Map\.setCenter\s*\(', 'Map.set_center('),
        
        # Earth Engine objects
        (r'\bee\.', 'ee.'),
        
        # Method chaining (keep as is, but note the difference)
        # JavaScript uses camelCase, Python uses snake_case for some methods
        
        # String methods
        (r'\.length\b', '.size()'),  # For EE objects
        
        # Boolean values
        (r'\btrue\b', 'True'),
        (r'\bfalse\b', 'False'),
        (r'\bnull\b', 'None'),
        
        # Semicolons (remove)
        (r';$', ''),
        (r';\s*\n', '\n'),
    ]
    
    # Apply conversions
    for pattern, replacement in conversions:
        python_code = re.sub(pattern, replacement, python_code, flags=re.MULTILINE)
    
    # Handle common EE method name conversions
    ee_method_conversions = [
        ('addBands', 'addBands'),  # Same in both
        ('select', 'select'),      # Same in both
        ('filter', 'filter'),      # Same in both
        ('map', 'map'),            # Same in both
        ('reduce', 'reduce'),      # Same in both
        ('first', 'first'),        # Same in both
        ('getInfo', 'getInfo'),    # Same in both
    ]
    
    # Add import statement if not present
    if 'import ee' not in python_code and 'ee.' in python_code:
        python_code = 'import ee\n\n' + python_code
    
    # Add Earth Engine initialization if not present
    if 'ee.Initialize' not in python_code and 'ee.' in python_code:
        python_code = python_code.replace('import ee\n', 'import ee\nee.Initialize()\n')
    
    # Clean up extra whitespace
    python_code = re.sub(r'\n\s*\n', '\n\n', python_code)
    python_code = python_code.strip()
    
    return python_code


def get_dataset_info(dataset_id: str) -> Optional[Dict[str, Any]]:
    """
    Get detailed information about a specific Earth Engine dataset.
    
    Args:
        dataset_id: Earth Engine dataset ID
        
    Returns:
        Dictionary containing dataset metadata
    """
    try:
        # Get the dataset
        if 'ImageCollection' in dataset_id or any(x in dataset_id for x in ['LANDSAT', 'MODIS', 'COPERNICUS']):
            dataset = ee.ImageCollection(dataset_id)
            dataset_type = 'ImageCollection'
        elif 'FeatureCollection' in dataset_id:
            dataset = ee.FeatureCollection(dataset_id)  
            dataset_type = 'FeatureCollection'
        else:
            # Try as Image first
            try:
                dataset = ee.Image(dataset_id)
                dataset_type = 'Image'
            except:
                dataset = ee.ImageCollection(dataset_id)
                dataset_type = 'ImageCollection'
        
        # Get basic info
        info = {
            'id': dataset_id,
            'type': dataset_type
        }
        
        # Try to get additional metadata
        try:
            if dataset_type in ['Image', 'ImageCollection']:
                # Get band names for images
                if dataset_type == 'ImageCollection':
                    first_image = ee.Image(dataset.first())
                    band_names = first_image.bandNames().getInfo()
                else:
                    band_names = dataset.bandNames().getInfo()
                info['bands'] = band_names
                
                # Get image properties (for first image if collection)
                if dataset_type == 'ImageCollection':
                    props = first_image.propertyNames().getInfo()
                else:
                    props = dataset.propertyNames().getInfo()
                info['properties'] = props
                
        except Exception as e:
            print(f"Could not retrieve detailed metadata: {str(e)}")
        
        return info
        
    except Exception as e:
        print(f"Error getting dataset info for {dataset_id}: {str(e)}")
        return None


def list_available_datasets(category: Optional[str] = None) -> List[str]:
    """
    List commonly used Earth Engine datasets by category.
    
    Args:
        category: Optional category filter ('imagery', 'climate', 'elevation', etc.)
        
    Returns:
        List of dataset IDs
    """
    datasets = {
        'imagery': [
            'LANDSAT/LC08/C02/T1_L2',
            'LANDSAT/LE07/C02/T1_L2',
            'COPERNICUS/S2_SR_HARMONIZED',
            'COPERNICUS/S1_GRD',
            'MODIS/061/MOD09A1',
            'MODIS/061/MYD09A1'
        ],
        'climate': [
            'ECMWF/ERA5_LAND/HOURLY',
            'UCSB-CHG/CHIRPS/DAILY',
            'NASA/GLDAS/V021/NOAH/G025/T3H',
            'MODIS/061/MOD11A1'
        ],
        'elevation': [
            'USGS/SRTMGL1_003',
            'NASA/NASADEM_HGT/001',
            'JAXA/ALOS/AW3D30/V3_2'
        ],
        'vegetation': [
            'MODIS/061/MOD13Q1',
            'MODIS/061/MYD13Q1',
            'COPERNICUS/S2_SR_HARMONIZED'
        ],
        'land_cover': [
            'MODIS/061/MCD12Q1',
            'ESA/WorldCover/v100',
            'COPERNICUS/Landcover/100m/Proba-V-C3/Global'
        ]
    }
    
    if category:
        return datasets.get(category, [])
    else:
        # Return all datasets
        all_datasets = []
        for cat_datasets in datasets.values():
            all_datasets.extend(cat_datasets)
        return list(set(all_datasets))  # Remove duplicates