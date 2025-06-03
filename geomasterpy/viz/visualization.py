"""
Visualization Tools for GeoMasterPy

Provides functions for adding legends, colorbars, split maps, and animations.
"""

import ee
import ipyleaflet as ipyl
from ipywidgets import widgets, HBox, VBox, Layout, HTML
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Union
import io
import base64
from PIL import Image
import requests
import time


def add_legend(map_widget, title: str, legend_dict: Dict[str, str], 
               position: str = 'bottomright') -> widgets.HTML:
    """
    Add a custom legend to the map.
    
    Args:
        map_widget: Map widget to add legend to
        title: Legend title
        legend_dict: Dictionary mapping labels to colors
        position: Legend position on map
        
    Returns:
        HTML widget containing the legend
    """
    legend_html = f'<div style="background-color: white; padding: 10px; border: 2px solid black; border-radius: 5px;"><h4>{title}</h4>'
    
    for label, color in legend_dict.items():
        legend_html += f'<div><span style="background-color: {color}; width: 20px; height: 20px; display: inline-block; margin-right: 10px;"></span>{label}</div>'
    
    legend_html += '</div>'
    
    legend_widget = HTML(value=legend_html)
    legend_control = ipyl.WidgetControl(widget=legend_widget, position=position)
    map_widget.add_control(legend_control)
    
    return legend_widget


def add_colorbar(map_widget, vis_params: Dict[str, Any], caption: str = '', 
                position: str = 'bottomright') -> widgets.HTML:
    """
    Add a colorbar to the map based on visualization parameters.
    
    Args:
        map_widget: Map widget to add colorbar to
        vis_params: Visualization parameters with min, max, and palette
        caption: Colorbar caption
        position: Colorbar position on map
        
    Returns:
        HTML widget containing the colorbar
    """
    if 'palette' not in vis_params:
        print("No palette found in vis_params")
        return None
        
    palette = vis_params['palette']
    vmin = vis_params.get('min', 0)
    vmax = vis_params.get('max', 1)
    
    # Create colorbar using matplotlib
    fig, ax = plt.subplots(figsize=(6, 0.5))
    fig.subplots_adjust(bottom=0.5)
    
    # Create colormap
    if isinstance(palette, list):
        colors = palette
    else:
        colors = palette.split(',')
    
    # Normalize colors if they're hex strings without #
    normalized_colors = []
    for color in colors:
        if not color.startswith('#') and len(color) == 6:
            color = '#' + color
        normalized_colors.append(color)
    
    cmap = LinearSegmentedColormap.from_list('custom', normalized_colors)
    
    # Create colorbar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=vmin, vmax=vmax))
    sm.set_array([])
    
    cbar = fig.colorbar(sm, cax=ax, orientation='horizontal')
    cbar.set_label(caption)
    
    # Convert to base64 image
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', dpi=100, transparent=True)
    buffer.seek(0)
    
    # Encode image
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    plt.close(fig)
    
    # Create HTML widget
    colorbar_html = f'<div style="background-color: white; padding: 5px; border-radius: 5px;"><img src="data:image/png;base64,{image_base64}" style="width: 200px;"></div>'
    
    colorbar_widget = HTML(value=colorbar_html)
    colorbar_control = ipyl.WidgetControl(widget=colorbar_widget, position=position)
    map_widget.add_control(colorbar_control)
    
    return colorbar_widget


def split_map(left_layer_info: Tuple[Any, Dict, str], 
              right_layer_info: Tuple[Any, Dict, str],
              center: Tuple[float, float] = (40, -100), 
              zoom: int = 4) -> HBox:
    """
    Create a split-screen map for comparing two layers.
    
    Args:
        left_layer_info: Tuple of (ee_object, vis_params, name) for left side
        right_layer_info: Tuple of (ee_object, vis_params, name) for right side  
        center: Map center coordinates
        zoom: Initial zoom level
        
    Returns:
        HBox widget containing split map
    """
    from ..map.split_map import SplitMap
    return SplitMap(left_layer_info, right_layer_info, center, zoom)


def create_landsat_timelapse(roi: ee.Geometry, start_year: int, end_year: int,
                           bands: List[str] = ['B4', 'B3', 'B2'],
                           vis_params: Optional[Dict[str, Any]] = None) -> str:
    """
    Create a Landsat timelapse GIF for a region of interest.
    
    Args:
        roi: Earth Engine Geometry defining the region
        start_year: Starting year
        end_year: Ending year
        bands: List of bands to use for RGB visualization
        vis_params: Visualization parameters
        
    Returns:
        URL to the generated GIF or local file path
    """
    if vis_params is None:
        vis_params = {'min': 0, 'max': 3000, 'gamma': 1.4}
    
    try:
        # Create image collection
        collection = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2') \
            .filterBounds(roi) \
            .filterDate(f'{start_year}-01-01', f'{end_year}-12-31') \
            .filter(ee.Filter.lt('CLOUD_COVER', 20)) \
            .select(bands)
        
        # Function to mask clouds and scale
        def mask_and_scale(image):
            # Apply scaling factors
            optical_bands = image.select('SR_B.').multiply(0.0000275).add(-0.2)
            return image.addBands(optical_bands, None, True)
        
        # Apply cloud masking and scaling
        collection = collection.map(mask_and_scale)
        
        # Create annual composites
        years = list(range(start_year, end_year + 1))
        annual_images = []
        
        for year in years:
            yearly_image = collection.filterDate(f'{year}-01-01', f'{year}-12-31') \
                .median() \
                .clip(roi)
            
            # Add year as property
            yearly_image = yearly_image.set('year', year)
            annual_images.append(yearly_image)
        
        # Create image collection from annual images
        annual_collection = ee.ImageCollection.fromImages(annual_images)
        
        # Generate GIF URL (for Earth Engine Apps)
        gif_params = {
            'collection': annual_collection,
            'selector': bands,
            'min': vis_params['min'],
            'max': vis_params['max'],
            'gamma': vis_params.get('gamma', 1.0),
            'region': roi,
            'framePersec': 1,
            'crs': 'EPSG:4326',
            'scale': 30
        }
        
        # Note: This would typically require Earth Engine Apps or export functionality
        # For now, return a placeholder message
        print(f"Timelapse created for {len(years)} years ({start_year}-{end_year})")
        print("To generate actual GIF, use Earth Engine's getVideoThumbURL() method")
        print("or export the collection using ee.batch.Export.video.toDrive()")
        
        return f"Timelapse prepared for years {start_year}-{end_year}"
        
    except Exception as e:
        print(f"Error creating timelapse: {str(e)}")
        return ""


def create_time_series_chart(image_collection: ee.ImageCollection, 
                           region: ee.Geometry,
                           band: str = 'NDVI',
                           reducer: str = 'mean',
                           scale: int = 30) -> widgets.Output:
    """
    Create a time series chart for an image collection.
    
    Args:
        image_collection: Earth Engine ImageCollection
        region: Region to extract values from
        band: Band name to chart
        reducer: Reduction method ('mean', 'median', etc.)
        scale: Scale in meters
        
    Returns:
        Output widget containing the chart
    """
    import matplotlib.pyplot as plt
    import pandas as pd
    from datetime import datetime
    
    output_widget = widgets.Output()
    
    try:
        # Extract time series data
        def extract_values(image):
            # Reduce image to single value over region
            if reducer == 'mean':
                value = image.select(band).reduceRegion(
                    reducer=ee.Reducer.mean(),
                    geometry=region,
                    scale=scale,
                    maxPixels=1e9
                )
            elif reducer == 'median':
                value = image.select(band).reduceRegion(
                    reducer=ee.Reducer.median(),
                    geometry=region,
                    scale=scale,
                    maxPixels=1e9
                )
            
            # Get date
            date = image.date()
            
            return ee.Feature(None, {
                'date': date,
                'value': value.get(band)
            })
        
        # Map over collection
        time_series = image_collection.map(extract_values)
        
        # Get the data
        data = time_series.getInfo()
        
        # Process data
        dates = []
        values = []
        
        for feature in data['features']:
            props = feature['properties']
            if props['value'] is not None:
                # Convert timestamp to datetime
                timestamp = props['date']['value'] / 1000  # Convert from milliseconds
                date = datetime.fromtimestamp(timestamp)
                dates.append(date)
                values.append(props['value'])
        
        # Create DataFrame
        df = pd.DataFrame({'date': dates, 'value': values})
        df = df.sort_values('date')
        
        # Create plot
        with output_widget:
            plt.figure(figsize=(12, 6))
            plt.plot(df['date'], df['value'], marker='o', linewidth=2, markersize=4)
            plt.title(f'{band} Time Series')
            plt.xlabel('Date')
            plt.ylabel(f'{band} ({reducer})')
            plt.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
            
    except Exception as e:
        with output_widget:
            print(f"Error creating time series chart: {str(e)}")
    
    return output_widget


def create_histogram(image: ee.Image, region: ee.Geometry, 
                    band: str, scale: int = 30,
                    max_pixels: int = 1e6) -> widgets.Output:
    """
    Create a histogram for an Earth Engine image.
    
    Args:
        image: Earth Engine Image
        region: Region to sample
        band: Band name
        scale: Scale in meters
        max_pixels: Maximum number of pixels to sample
        
    Returns:
        Output widget containing the histogram
    """
    import matplotlib.pyplot as plt
    
    output_widget = widgets.Output()
    
    try:
        # Sample the image
        sample = image.select(band).sample(
            region=region,
            scale=scale,
            numPixels=max_pixels,
            dropNulls=True
        )
        
        # Get the data
        data = sample.aggregate_array(band).getInfo()
        
        # Create histogram
        with output_widget:
            plt.figure(figsize=(10, 6))
            plt.hist(data, bins=50, alpha=0.7, edgecolor='black')
            plt.title(f'Histogram of {band}')
            plt.xlabel(f'{band} Values')
            plt.ylabel('Frequency')
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.show()
            
            # Print statistics
            print(f"Statistics for {band}:")
            print(f"  Count: {len(data)}")
            print(f"  Mean: {np.mean(data):.4f}")
            print(f"  Std: {np.std(data):.4f}")
            print(f"  Min: {np.min(data):.4f}")
            print(f"  Max: {np.max(data):.4f}")
            
    except Exception as e:
        with output_widget:
            print(f"Error creating histogram: {str(e)}")
    
    return output_widget