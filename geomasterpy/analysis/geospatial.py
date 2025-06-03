"""
Geospatial Analysis Functions for GeoMasterPy

Provides statistical analysis, classification, and other geospatial operations.
"""

import ee
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Union, Tuple
from ipywidgets import widgets


def image_stats(image: ee.Image, region: ee.Geometry, 
               scale: int = 30, bands: Optional[List[str]] = None) -> Dict[str, Dict[str, float]]:
    """
    Calculate comprehensive statistics for an Earth Engine image.
    
    Args:
        image: Earth Engine Image
        region: Region to calculate statistics over
        scale: Scale in meters for analysis
        bands: List of band names to analyze (if None, uses all bands)
        
    Returns:
        Dictionary with statistics for each band
    """
    try:
        if bands is None:
            bands = image.bandNames().getInfo()
        
        stats = {}
        
        for band in bands:
            band_image = image.select(band)
            
            # Calculate various statistics
            band_stats = band_image.reduceRegion(
                reducer=ee.Reducer.mean()
                    .combine(ee.Reducer.stdDev(), sharedInputs=True)
                    .combine(ee.Reducer.min(), sharedInputs=True)
                    .combine(ee.Reducer.max(), sharedInputs=True)
                    .combine(ee.Reducer.median(), sharedInputs=True)
                    .combine(ee.Reducer.percentile([25, 75]), sharedInputs=True),
                geometry=region,
                scale=scale,
                maxPixels=1e9
            ).getInfo()
            
            # Organize results
            stats[band] = {
                'mean': band_stats.get(f'{band}_mean'),
                'std': band_stats.get(f'{band}_stdDev'),
                'min': band_stats.get(f'{band}_min'),
                'max': band_stats.get(f'{band}_max'),
                'median': band_stats.get(f'{band}_median'),
                'p25': band_stats.get(f'{band}_p25'),
                'p75': band_stats.get(f'{band}_p75')
            }
        
        return stats
        
    except Exception as e:
        print(f"Error calculating image statistics: {str(e)}")
        return {}


def zonal_stats(image: ee.Image, zones: ee.FeatureCollection, 
               reducer: str = 'mean', scale: int = 30,
               bands: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Calculate zonal statistics for an image over vector zones.
    
    Args:
        image: Earth Engine Image
        zones: FeatureCollection defining zones
        reducer: Reduction method ('mean', 'sum', 'median', 'std', etc.)
        scale: Scale in meters
        bands: List of bands to analyze
        
    Returns:
        Pandas DataFrame with zonal statistics
    """
    try:
        if bands is None:
            bands = image.bandNames().getInfo()
        
        # Select bands
        image = image.select(bands)
        
        # Choose reducer
        reducer_dict = {
            'mean': ee.Reducer.mean(),
            'median': ee.Reducer.median(),
            'sum': ee.Reducer.sum(),
            'std': ee.Reducer.stdDev(),
            'min': ee.Reducer.min(),
            'max': ee.Reducer.max(),
            'count': ee.Reducer.count()
        }
        
        if reducer not in reducer_dict:
            print(f"Unknown reducer: {reducer}. Using 'mean'.")
            reducer = 'mean'
        
        ee_reducer = reducer_dict[reducer]
        
        # Reduce image over zones
        zonal_results = image.reduceRegions(
            collection=zones,
            reducer=ee_reducer,
            scale=scale,
            crs='EPSG:4326'
        )
        
        # Convert to pandas DataFrame
        results_info = zonal_results.getInfo()
        
        rows = []
        for feature in results_info['features']:
            row = feature['properties']
            rows.append(row)
        
        df = pd.DataFrame(rows)
        return df
        
    except Exception as e:
        print(f"Error calculating zonal statistics: {str(e)}")
        return pd.DataFrame()


def supervised_classification(image: ee.Image, training_data: ee.FeatureCollection,
                            class_property: str = 'class',
                            classifier_type: str = 'randomForest',
                            bands: Optional[List[str]] = None) -> ee.Image:
    """
    Perform supervised classification on an Earth Engine image.
    
    Args:
        image: Earth Engine Image to classify
        training_data: FeatureCollection with training samples
        class_property: Property name containing class labels
        classifier_type: Type of classifier ('randomForest', 'svm', 'cart')
        bands: List of bands to use for classification
        
    Returns:
        Classified Earth Engine Image
    """
    try:
        if bands is None:
            bands = image.bandNames().getInfo()
        
        # Select bands for classification
        image = image.select(bands)
        
        # Sample training data
        training = image.sampleRegions(
            collection=training_data,
            properties=[class_property],
            scale=30
        )
        
        # Choose classifier
        if classifier_type == 'randomForest':
            classifier = ee.Classifier.smileRandomForest(numberOfTrees=100)
        elif classifier_type == 'svm':
            classifier = ee.Classifier.libsvm()
        elif classifier_type == 'cart':
            classifier = ee.Classifier.smileCart()
        else:
            print(f"Unknown classifier: {classifier_type}. Using randomForest.")
            classifier = ee.Classifier.smileRandomForest(numberOfTrees=100)
        
        # Train classifier
        trained_classifier = classifier.train(
            features=training,
            classProperty=class_property,
            inputProperties=bands
        )
        
        # Classify image
        classified = image.classify(trained_classifier)
        
        return classified
        
    except Exception as e:
        print(f"Error in supervised classification: {str(e)}")
        return None


def unsupervised_classification(image: ee.Image, num_classes: int = 10,
                              scale: int = 30, region: Optional[ee.Geometry] = None,
                              bands: Optional[List[str]] = None) -> ee.Image:
    """
    Perform unsupervised classification (k-means clustering).
    
    Args:
        image: Earth Engine Image to classify
        num_classes: Number of classes/clusters
        scale: Scale for sampling
        region: Region to sample (if None, uses image extent)
        bands: List of bands to use
        
    Returns:
        Classified Earth Engine Image
    """
    try:
        if bands is None:
            bands = image.bandNames().getInfo()
        
        # Select bands
        image = image.select(bands)
        
        # Use image bounds if no region specified
        if region is None:
            region = image.geometry()
        
        # Sample training data for clustering
        training = image.sample(
            region=region,
            scale=scale,
            numPixels=5000
        )
        
        # Create k-means clusterer
        clusterer = ee.Clusterer.wekaKMeans(num_classes)
        
        # Train clusterer
        cluster = clusterer.train(training)
        
        # Classify image
        classified = image.cluster(cluster)
        
        return classified
        
    except Exception as e:
        print(f"Error in unsupervised classification: {str(e)}")
        return None


def calculate_indices(image: ee.Image, indices: List[str] = ['NDVI']) -> ee.Image:
    """
    Calculate common spectral indices.
    
    Args:
        image: Earth Engine Image (Landsat or Sentinel-2)
        indices: List of indices to calculate
        
    Returns:
        Image with added index bands
    """
    try:
        result_image = image
        
        for index in indices:
            if index == 'NDVI':
                # Normalized Difference Vegetation Index
                if 'B5' in image.bandNames().getInfo():  # Landsat
                    ndvi = image.normalizedDifference(['B5', 'B4']).rename('NDVI')
                elif 'B8' in image.bandNames().getInfo():  # Sentinel-2
                    ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
                else:
                    print("Cannot calculate NDVI: NIR or Red bands not found")
                    continue
                result_image = result_image.addBands(ndvi)
                
            elif index == 'NDWI':
                # Normalized Difference Water Index
                if 'B3' in image.bandNames().getInfo() and 'B5' in image.bandNames().getInfo():  # Landsat
                    ndwi = image.normalizedDifference(['B3', 'B5']).rename('NDWI')
                elif 'B3' in image.bandNames().getInfo() and 'B8' in image.bandNames().getInfo():  # Sentinel-2
                    ndwi = image.normalizedDifference(['B3', 'B8']).rename('NDWI')
                else:
                    print("Cannot calculate NDWI: required bands not found")
                    continue
                result_image = result_image.addBands(ndwi)
                
            elif index == 'NDBI':
                # Normalized Difference Built-up Index
                if 'B6' in image.bandNames().getInfo() and 'B5' in image.bandNames().getInfo():  # Landsat
                    ndbi = image.normalizedDifference(['B6', 'B5']).rename('NDBI')
                elif 'B11' in image.bandNames().getInfo() and 'B8' in image.bandNames().getInfo():  # Sentinel-2
                    ndbi = image.normalizedDifference(['B11', 'B8']).rename('NDBI')
                else:
                    print("Cannot calculate NDBI: SWIR or NIR bands not found")
                    continue
                result_image = result_image.addBands(ndbi)
                
            elif index == 'EVI':
                # Enhanced Vegetation Index
                if all(band in image.bandNames().getInfo() for band in ['B5', 'B4', 'B2']):  # Landsat
                    evi = image.expression(
                        '2.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1))',
                        {
                            'NIR': image.select('B5'),
                            'RED': image.select('B4'),
                            'BLUE': image.select('B2')
                        }
                    ).rename('EVI')
                elif all(band in image.bandNames().getInfo() for band in ['B8', 'B4', 'B2']):  # Sentinel-2
                    evi = image.expression(
                        '2.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1))',
                        {
                            'NIR': image.select('B8'),
                            'RED': image.select('B4'),
                            'BLUE': image.select('B2')
                        }
                    ).rename('EVI')
                else:
                    print("Cannot calculate EVI: required bands not found")
                    continue
                result_image = result_image.addBands(evi)
                
            else:
                print(f"Unknown index: {index}")
        
        return result_image
        
    except Exception as e:
        print(f"Error calculating indices: {str(e)}")
        return image


def accuracy_assessment(reference: ee.FeatureCollection, classified: ee.Image,
                       class_property: str = 'class') -> Dict[str, Any]:
    """
    Perform accuracy assessment for a classified image.
    
    Args:
        reference: Reference/validation FeatureCollection
        classified: Classified image
        class_property: Property name with reference class values
        
    Returns:
        Dictionary with accuracy metrics
    """
    try:
        # Sample classified image at reference points
        validation = classified.sampleRegions(
            collection=reference,
            properties=[class_property],
            scale=30,
            tileScale=8
        )
        
        # Create confusion matrix
        confusion_matrix = validation.errorMatrix(class_property, 'classification')
        
        # Calculate accuracy metrics
        overall_accuracy = confusion_matrix.accuracy()
        kappa = confusion_matrix.kappa()
        
        # Get matrix as array
        matrix_array = confusion_matrix.getInfo()
        
        results = {
            'overall_accuracy': overall_accuracy.getInfo(),
            'kappa': kappa.getInfo(),
            'confusion_matrix': matrix_array,
            'producer_accuracy': confusion_matrix.producersAccuracy().getInfo(),
            'consumer_accuracy': confusion_matrix.consumersAccuracy().getInfo()
        }
        
        return results
        
    except Exception as e:
        print(f"Error in accuracy assessment: {str(e)}")
        return {}


def change_detection(image1: ee.Image, image2: ee.Image, 
                    band: str = 'NDVI', threshold: float = 0.1) -> ee.Image:
    """
    Perform simple change detection between two images.
    
    Args:
        image1: First image (earlier date)
        image2: Second image (later date)
        band: Band to use for change detection
        threshold: Change threshold
        
    Returns:
        Change detection image (0 = no change, 1 = change)
    """
    try:
        # Calculate difference
        difference = image2.select(band).subtract(image1.select(band))
        
        # Apply threshold
        change = difference.abs().gt(threshold)
        
        return change.rename('change')
        
    except Exception as e:
        print(f"Error in change detection: {str(e)}")
        return None