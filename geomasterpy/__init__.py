"""
GeoMasterPy - Interactive Geospatial Analysis Library for Google Earth Engine

A comprehensive Python library that simplifies Google Earth Engine workflows
with interactive mapping, visualization, and analysis tools.
"""

__version__ = "0.1.0"
__author__ = "GeoMasterPy Development Team"

from .map.interactive_map import Map
from .data.catalog import (
    search_ee_data, 
    js_snippet_to_python,
    load_geojson_from_drive_url,
    geojson_to_ee_geometry,
    validate_drive_url,
    convert_drive_sharing_url
)
from .viz.visualization import add_legend, add_colorbar, split_map, create_landsat_timelapse
from .analysis.geospatial import image_stats, zonal_stats
from .export.data_export import export_image_to_local, export_vector_to_local, extract_values_to_points
from .plotting.cartopy_maps import plot_ee_image_cartopy

__all__ = [
    'Map',
    'search_ee_data',
    'js_snippet_to_python',
    'load_geojson_from_drive_url',
    'geojson_to_ee_geometry',
    'validate_drive_url',
    'convert_drive_sharing_url',
    'add_legend',
    'add_colorbar',
    'split_map',
    'create_landsat_timelapse',
    'image_stats',
    'zonal_stats',
    'export_image_to_local',
    'export_vector_to_local',
    'extract_values_to_points',
    'plot_ee_image_cartopy'
]