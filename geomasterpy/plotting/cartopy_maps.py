"""
Publication Quality Maps using Cartopy

Provides functions for creating static, publication-ready maps from Earth Engine data.
"""

import ee
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import requests
from PIL import Image
import io
from typing import Dict, List, Any, Optional, Tuple, Union
import warnings


def plot_ee_image_cartopy(image: ee.Image, vis_params: Dict[str, Any], 
                         region: ee.Geometry, figsize: Tuple[int, int] = (12, 8),
                         title: str = '', cmap: Optional[str] = None,
                         add_colorbar: bool = True, add_gridlines: bool = True,
                         coastlines: bool = True, borders: bool = True,
                         projection: str = 'PlateCarree', scale: int = 1000) -> plt.Figure:
    """
    Create a publication-quality static map using Cartopy.
    
    Args:
        image: Earth Engine Image
        vis_params: Visualization parameters
        region: Region to plot
        figsize: Figure size (width, height)
        title: Map title
        cmap: Matplotlib colormap name (overrides palette in vis_params)
        add_colorbar: Whether to add a colorbar
        add_gridlines: Whether to add coordinate gridlines
        coastlines: Whether to add coastlines
        borders: Whether to add country borders
        projection: Cartopy projection name
        scale: Scale for image download
        
    Returns:
        Matplotlib Figure object
    """
    try:
        # Get projection
        proj_dict = {
            'PlateCarree': ccrs.PlateCarree(),
            'Mercator': ccrs.Mercator(),
            'Robinson': ccrs.Robinson(),
            'Mollweide': ccrs.Mollweide(),
            'Orthographic': ccrs.Orthographic(),
            'LambertConformal': ccrs.LambertConformal()
        }
        
        proj = proj_dict.get(projection, ccrs.PlateCarree())
        
        # Create figure and axis
        fig = plt.figure(figsize=figsize)
        ax = plt.axes(projection=proj)
        
        # Get region bounds
        bounds = region.bounds().getInfo()['coordinates'][0]
        min_lon = min([coord[0] for coord in bounds])
        max_lon = max([coord[0] for coord in bounds])
        min_lat = min([coord[1] for coord in bounds])
        max_lat = max([coord[1] for coord in bounds])
        
        # Set extent
        ax.set_extent([min_lon, max_lon, min_lat, max_lat], crs=ccrs.PlateCarree())
        
        # Add map features
        if coastlines:
            ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
        if borders:
            ax.add_feature(cfeature.BORDERS, linewidth=0.5)
        
        # Add natural features
        ax.add_feature(cfeature.LAND, alpha=0.3, color='lightgray')
        ax.add_feature(cfeature.OCEAN, alpha=0.3, color='lightblue')
        
        # Download and plot Earth Engine image
        try:
            # Clip image to region
            clipped_image = image.clip(region)
            
            # Get RGB image if multiple bands
            bands = clipped_image.bandNames().getInfo()
            
            if len(bands) >= 3 and 'palette' not in vis_params:
                # RGB visualization
                rgb_image = _get_ee_rgb_image(clipped_image, vis_params, region, scale)
                if rgb_image is not None:
                    ax.imshow(rgb_image, extent=[min_lon, max_lon, min_lat, max_lat],
                             transform=ccrs.PlateCarree(), origin='upper')
            else:
                # Single band or palette visualization
                single_band_data = _get_ee_single_band_data(clipped_image, vis_params, region, scale)
                if single_band_data is not None:
                    data_array, extent = single_band_data
                    
                    # Create colormap
                    if cmap:
                        colormap = plt.get_cmap(cmap)
                    elif 'palette' in vis_params:
                        colors = vis_params['palette']
                        if isinstance(colors, str):
                            colors = colors.split(',')
                        # Normalize colors
                        norm_colors = []
                        for color in colors:
                            if not color.startswith('#') and len(color) == 6:
                                color = '#' + color
                            norm_colors.append(color)
                        colormap = LinearSegmentedColormap.from_list('custom', norm_colors)
                    else:
                        colormap = 'viridis'
                    
                    # Plot data
                    vmin = vis_params.get('min', np.nanmin(data_array))
                    vmax = vis_params.get('max', np.nanmax(data_array))
                    
                    im = ax.imshow(data_array, extent=extent, cmap=colormap, 
                                  vmin=vmin, vmax=vmax, transform=ccrs.PlateCarree(),
                                  origin='upper')
                    
                    # Add colorbar
                    if add_colorbar:
                        cbar = plt.colorbar(im, ax=ax, shrink=0.6, pad=0.1)
                        if 'bands' in vis_params and len(vis_params['bands']) == 1:
                            cbar.set_label(vis_params['bands'][0])
        
        except Exception as e:
            print(f"Warning: Could not load Earth Engine image data: {str(e)}")
            print("Displaying base map only")
        
        # Add gridlines
        if add_gridlines:
            gl = ax.gridlines(draw_labels=True, linewidth=0.5, alpha=0.5)
            gl.xlabel_style = {'size': 10}
            gl.ylabel_style = {'size': 10}
        
        # Add title
        if title:
            plt.title(title, fontsize=14, fontweight='bold', pad=20)
        
        plt.tight_layout()
        return fig
        
    except Exception as e:
        print(f"Error creating cartopy map: {str(e)}")
        # Return empty figure
        fig = plt.figure(figsize=figsize)
        plt.text(0.5, 0.5, f'Error creating map:\n{str(e)}', 
                ha='center', va='center', transform=plt.gca().transAxes)
        return fig


def _get_ee_rgb_image(image: ee.Image, vis_params: Dict[str, Any], 
                     region: ee.Geometry, scale: int) -> Optional[np.ndarray]:
    """
    Download RGB image data from Earth Engine.
    
    Args:
        image: Earth Engine Image
        vis_params: Visualization parameters
        region: Download region
        scale: Download scale
        
    Returns:
        RGB numpy array or None if failed
    """
    try:
        # Select RGB bands
        bands = vis_params.get('bands', image.bandNames().getInfo()[:3])
        rgb_image = image.select(bands[:3])
        
        # Get download URL
        url = rgb_image.getThumbURL({
            'region': region.getInfo(),
            'dimensions': 512,
            'format': 'png'
        })
        
        # Download image
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            # Load image
            pil_image = Image.open(io.BytesIO(response.content))
            rgb_array = np.array(pil_image)
            
            # Convert to 0-1 range if needed
            if rgb_array.max() > 1:
                rgb_array = rgb_array / 255.0
            
            return rgb_array
        else:
            print(f"Failed to download RGB image: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error getting RGB image: {str(e)}")
        return None


def _get_ee_single_band_data(image: ee.Image, vis_params: Dict[str, Any],
                           region: ee.Geometry, scale: int) -> Optional[Tuple[np.ndarray, List[float]]]:
    """
    Download single band image data from Earth Engine.
    
    Args:
        image: Earth Engine Image
        vis_params: Visualization parameters  
        region: Download region
        scale: Download scale
        
    Returns:
        Tuple of (data_array, extent) or None if failed
    """
    try:
        # Select first band or specified band
        bands = image.bandNames().getInfo()
        if 'bands' in vis_params:
            band_name = vis_params['bands'][0] if isinstance(vis_params['bands'], list) else vis_params['bands']
        else:
            band_name = bands[0]
        
        single_band = image.select(band_name)
        
        # Get array from Earth Engine
        # Note: This is a simplified approach - for larger areas, you'd need to use sampling
        bounds = region.bounds().getInfo()['coordinates'][0]
        min_lon = min([coord[0] for coord in bounds])
        max_lon = max([coord[0] for coord in bounds])
        min_lat = min([coord[1] for coord in bounds])
        max_lat = max([coord[1] for coord in bounds])
        
        # Sample the image to get data array
        # This is a basic implementation - for production use, consider ee.Image.getDownloadURL
        try:
            # Create a grid of points for sampling
            lon_step = (max_lon - min_lon) / 100
            lat_step = (max_lat - min_lat) / 100
            
            points = []
            for i in range(100):
                for j in range(100):
                    lon = min_lon + i * lon_step
                    lat = min_lat + j * lat_step
                    points.append(ee.Geometry.Point([lon, lat]))
            
            # Sample at these points
            point_collection = ee.FeatureCollection(points)
            sampled = single_band.sampleRegions(
                collection=point_collection,
                scale=scale,
                geometries=True
            )
            
            # Get the results
            sample_data = sampled.getInfo()
            
            # Convert to array
            data_array = np.full((100, 100), np.nan)
            for idx, feature in enumerate(sample_data['features']):
                i = idx // 100
                j = idx % 100
                value = feature['properties'].get(band_name)
                if value is not None:
                    data_array[i, j] = value
            
            extent = [min_lon, max_lon, min_lat, max_lat]
            return data_array, extent
            
        except Exception as e:
            print(f"Could not sample Earth Engine data: {str(e)}")
            return None
            
    except Exception as e:
        print(f"Error getting single band data: {str(e)}")
        return None


def create_comparison_map(image1: ee.Image, image2: ee.Image, 
                         vis_params1: Dict[str, Any], vis_params2: Dict[str, Any],
                         region: ee.Geometry, titles: List[str] = ['Image 1', 'Image 2'],
                         figsize: Tuple[int, int] = (16, 6)) -> plt.Figure:
    """
    Create a side-by-side comparison map.
    
    Args:
        image1: First Earth Engine Image
        image2: Second Earth Engine Image
        vis_params1: Visualization parameters for first image
        vis_params2: Visualization parameters for second image
        region: Region to plot
        titles: List of titles for each subplot
        figsize: Figure size
        
    Returns:
        Matplotlib Figure object
    """
    try:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize, 
                                      subplot_kw={'projection': ccrs.PlateCarree()})
        
        # Plot first image
        _plot_single_image(ax1, image1, vis_params1, region, titles[0])
        
        # Plot second image  
        _plot_single_image(ax2, image2, vis_params2, region, titles[1])
        
        plt.tight_layout()
        return fig
        
    except Exception as e:
        print(f"Error creating comparison map: {str(e)}")
        fig = plt.figure(figsize=figsize)
        plt.text(0.5, 0.5, f'Error creating comparison map:\n{str(e)}', 
                ha='center', va='center', transform=plt.gca().transAxes)
        return fig


def _plot_single_image(ax, image: ee.Image, vis_params: Dict[str, Any], 
                      region: ee.Geometry, title: str):
    """Helper function to plot a single image on an axis."""
    try:
        # Get region bounds
        bounds = region.bounds().getInfo()['coordinates'][0]
        min_lon = min([coord[0] for coord in bounds])
        max_lon = max([coord[0] for coord in bounds])
        min_lat = min([coord[1] for coord in bounds])
        max_lat = max([coord[1] for coord in bounds])
        
        # Set extent
        ax.set_extent([min_lon, max_lon, min_lat, max_lat], crs=ccrs.PlateCarree())
        
        # Add features
        ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
        ax.add_feature(cfeature.BORDERS, linewidth=0.5)
        ax.add_feature(cfeature.LAND, alpha=0.3, color='lightgray')
        
        # Try to plot Earth Engine image
        try:
            clipped_image = image.clip(region)
            rgb_image = _get_ee_rgb_image(clipped_image, vis_params, region, 1000)
            if rgb_image is not None:
                ax.imshow(rgb_image, extent=[min_lon, max_lon, min_lat, max_lat],
                         transform=ccrs.PlateCarree(), origin='upper')
        except Exception as e:
            print(f"Warning: Could not load image data for {title}: {str(e)}")
        
        # Add gridlines
        gl = ax.gridlines(draw_labels=True, linewidth=0.5, alpha=0.5)
        gl.xlabel_style = {'size': 8}
        gl.ylabel_style = {'size': 8}
        
        # Add title
        ax.set_title(title, fontsize=12, fontweight='bold')
        
    except Exception as e:
        print(f"Error plotting image {title}: {str(e)}")


def save_publication_map(fig: plt.Figure, filename: str, dpi: int = 300, 
                        format: str = 'png', bbox_inches: str = 'tight'):
    """
    Save a publication-quality map to file.
    
    Args:
        fig: Matplotlib Figure object
        filename: Output filename
        dpi: Resolution in dots per inch
        format: Output format ('png', 'pdf', 'eps', 'svg')
        bbox_inches: Bounding box setting
    """
    try:
        fig.savefig(filename, dpi=dpi, format=format, bbox_inches=bbox_inches)
        print(f"Map saved to: {filename}")
    except Exception as e:
        print(f"Error saving map: {str(e)}")