"""
Interactive Map Module for GeoMasterPy

Provides the core Map class for interactive mapping with Google Earth Engine
integration using ipyleaflet.
"""

import ee
import ipyleaflet as ipyl
from ipywidgets import widgets, HBox, VBox, Layout
import json
from typing import Dict, Any, Optional, Tuple, Union


class Map(ipyl.Map):
    """
    Interactive map widget based on ipyleaflet with Google Earth Engine integration.
    
    This class extends ipyleaflet.Map to provide simplified methods for adding
    Earth Engine layers, basemaps, and interactive tools.
    """
    
    def __init__(self, center: Tuple[float, float] = (40, -100), zoom: int = 4, 
                 height: str = '600px', width: str = '100%', lite_mode: bool = False, **kwargs):
        """
        Initialize the interactive map.
        
        Args:
            center: Initial map center as (latitude, longitude)
            zoom: Initial zoom level
            height: Map height in CSS units
            width: Map width in CSS units  
            lite_mode: If True, shows minimal toolbar
            **kwargs: Additional arguments passed to ipyleaflet.Map
        """
        # Set default layout
        layout = Layout(height=height, width=width)
        
        # Initialize the base ipyleaflet Map
        super().__init__(center=center, zoom=zoom, layout=layout, **kwargs)
        
        # Initialize Earth Engine if not already done
        try:
            ee.Initialize()
        except Exception:
            print("Warning: Earth Engine not initialized. Please run 'ee.Authenticate()' and 'ee.Initialize()'")
        
        # Store configuration
        self.lite_mode = lite_mode
        self._ee_layers = {}
        self._layer_count = 0
        
        # Add default basemap controls
        if not lite_mode:
            self._setup_controls()
    
    def _setup_controls(self):
        """Set up map controls and tools."""
        # Add layer control
        self.add_control(ipyl.LayersControl(position='topright'))
        
        # Add scale control
        self.add_control(ipyl.ScaleControl(position='bottomleft'))
        
        # Add fullscreen control
        self.add_control(ipyl.FullScreenControl())
        
        # Add drawing control
        draw_control = ipyl.DrawControl()
        draw_control.polyline = {}
        draw_control.polygon = {"shapeOptions": {"color": "#6bc2e5", "weight": 4, "opacity": 1.0}}
        draw_control.circle = {}
        draw_control.rectangle = {"shapeOptions": {"color": "#6bc2e5", "weight": 4, "opacity": 1.0}}
        draw_control.marker = {}
        self.add_control(draw_control)
        
        # Store reference to draw control
        self.draw_control = draw_control
    
    def add_basemap(self, name: str = 'OpenStreetMap'):
        """
        Add a predefined basemap.
        
        Args:
            name: Name of the basemap. Options include:
                  'OpenStreetMap', 'CartoDB.Positron', 'CartoDB.DarkMatter',
                  'Esri.WorldImagery', 'Esri.WorldTopoMap', 'Stamen.Terrain'
        """
        basemap_dict = {
            'OpenStreetMap': ipyl.basemaps.OpenStreetMap.Mapnik,
            'CartoDB.Positron': ipyl.basemaps.CartoDB.Positron,
            'CartoDB.DarkMatter': ipyl.basemaps.CartoDB.DarkMatter,
            'Esri.WorldImagery': ipyl.basemaps.Esri.WorldImagery,
            'Esri.WorldTopoMap': ipyl.basemaps.Esri.WorldTopoMap,
            'Stamen.Terrain': ipyl.basemaps.Stamen.Terrain,
            'Google.Satellite': {
                'url': 'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
                'attribution': 'Google',
                'name': 'Google Satellite',
                'max_zoom': 20
            },
            'Google.Hybrid': {
                'url': 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
                'attribution': 'Google',
                'name': 'Google Hybrid',
                'max_zoom': 20
            }
        }
        
        if name in basemap_dict:
            basemap = basemap_dict[name]
            if isinstance(basemap, dict):
                # Custom basemap
                layer = ipyl.TileLayer(
                    url=basemap['url'],
                    attribution=basemap['attribution'],
                    name=basemap['name'],
                    max_zoom=basemap.get('max_zoom', 18)
                )
            else:
                # Predefined basemap
                layer = ipyl.basemap_to_tiles(basemap)
            
            self.add_layer(layer)
        else:
            print(f"Basemap '{name}' not found. Available options: {list(basemap_dict.keys())}")
    
    def add_ee_layer(self, ee_object: Union[ee.Image, ee.ImageCollection, ee.FeatureCollection], 
                     vis_params: Optional[Dict[str, Any]] = None, name: str = 'EE Layer',
                     opacity: float = 1.0):
        """
        Add an Earth Engine object to the map.
        
        Args:
            ee_object: Earth Engine Image, ImageCollection, or FeatureCollection
            vis_params: Visualization parameters dictionary
            name: Layer name
            opacity: Layer opacity (0-1)
        """
        if vis_params is None:
            vis_params = {}
        
        try:
            # Handle different EE object types
            if isinstance(ee_object, ee.Image):
                tile_layer = self._ee_image_to_tile_layer(ee_object, vis_params, name, opacity)
            elif isinstance(ee_object, ee.ImageCollection):
                # Convert to Image (mosaic)
                image = ee_object.mosaic()
                tile_layer = self._ee_image_to_tile_layer(image, vis_params, name, opacity)
            elif isinstance(ee_object, ee.FeatureCollection):
                tile_layer = self._ee_vector_to_tile_layer(ee_object, vis_params, name, opacity)
            else:
                print(f"Unsupported Earth Engine object type: {type(ee_object)}")
                return
            
            # Add layer to map
            self.add_layer(tile_layer)
            
            # Store reference
            self._ee_layers[name] = {
                'layer': tile_layer,
                'ee_object': ee_object,
                'vis_params': vis_params
            }
            
        except Exception as e:
            print(f"Error adding Earth Engine layer: {str(e)}")
    
    def _ee_image_to_tile_layer(self, image: ee.Image, vis_params: Dict[str, Any], 
                               name: str, opacity: float) -> ipyl.TileLayer:
        """Convert EE Image to ipyleaflet TileLayer."""
        # Get the map tile URL
        map_id_dict = ee.Image(image).getMapId(vis_params)
        
        # Create tile layer
        tile_layer = ipyl.TileLayer(
            url=map_id_dict['tile_fetcher'].url_format,
            attribution='Google Earth Engine',
            name=name,
            opacity=opacity
        )
        
        return tile_layer
    
    def _ee_vector_to_tile_layer(self, feature_collection: ee.FeatureCollection, 
                                vis_params: Dict[str, Any], name: str, opacity: float) -> ipyl.TileLayer:
        """Convert EE FeatureCollection to ipyleaflet TileLayer."""
        # Default style for vectors
        default_style = {
            'color': 'blue',
            'width': 2,
            'fillColor': 'blue',
            'fillOpacity': 0.3
        }
        
        # Merge with user params
        style = {**default_style, **vis_params}
        
        # Create styled image from vector
        styled_vector = feature_collection.style(**style)
        
        # Get map tiles
        map_id_dict = styled_vector.getMapId()
        
        # Create tile layer
        tile_layer = ipyl.TileLayer(
            url=map_id_dict['tile_fetcher'].url_format,
            attribution='Google Earth Engine',
            name=name,
            opacity=opacity
        )
        
        return tile_layer
    
    def remove_ee_layer(self, name: str):
        """
        Remove an Earth Engine layer by name.
        
        Args:
            name: Name of the layer to remove
        """
        if name in self._ee_layers:
            layer_info = self._ee_layers[name]
            self.remove_layer(layer_info['layer'])
            del self._ee_layers[name]
        else:
            print(f"Layer '{name}' not found")
    
    def clear_ee_layers(self):
        """Remove all Earth Engine layers."""
        for name in list(self._ee_layers.keys()):
            self.remove_ee_layer(name)
    
    def set_center(self, lat: float, lon: float, zoom: Optional[int] = None):
        """
        Set map center and optionally zoom level.
        
        Args:
            lat: Latitude
            lon: Longitude  
            zoom: Zoom level (optional)
        """
        self.center = (lat, lon)
        if zoom is not None:
            self.zoom = zoom
    
    def zoom_to_bounds(self, bounds: Tuple[float, float, float, float]):
        """
        Zoom map to specified bounds.
        
        Args:
            bounds: Bounding box as (west, south, east, north)
        """
        west, south, east, north = bounds
        self.fit_bounds([[south, west], [north, east]])
    
    def add_inspector_tool(self):
        """Add a tool for inspecting pixel values."""
        def handle_interaction(**kwargs):
            if kwargs.get('type') == 'click':
                lat, lon = kwargs.get('coordinates')
                point = ee.Geometry.Point([lon, lat])
                
                # Create info widget
                info_widget = widgets.HTML(
                    value=f"<b>Clicked at:</b> {lat:.4f}, {lon:.4f}<br>Inspecting layers..."
                )
                
                # Display basic info
                print(f"Clicked coordinates: {lat:.4f}, {lon:.4f}")
                
                # Sample EE layers at this point
                for layer_name, layer_info in self._ee_layers.items():
                    try:
                        ee_object = layer_info['ee_object']
                        if isinstance(ee_object, ee.Image):
                            # Sample the image
                            sample = ee_object.sample(point, 30).first()
                            properties = sample.getInfo()['properties']
                            print(f"{layer_name}: {properties}")
                    except Exception as e:
                        print(f"Error sampling {layer_name}: {str(e)}")
        
        # Add click handler
        self.on_interaction(handle_interaction)
    
    def get_drawing_data(self) -> Dict[str, Any]:
        """
        Get data from drawing control.
        
        Returns:
            Dictionary containing drawn features
        """
        if hasattr(self, 'draw_control'):
            return {
                'last_draw': self.draw_control.last_draw,
                'data': self.draw_control.data
            }
        return {}
    
    def create_split_map(self, left_layer_info: Tuple[Any, Dict, str], 
                        right_layer_info: Tuple[Any, Dict, str]) -> 'SplitMap':
        """
        Create a split-screen map for comparison.
        
        Args:
            left_layer_info: Tuple of (ee_object, vis_params, name) for left side
            right_layer_info: Tuple of (ee_object, vis_params, name) for right side
            
        Returns:
            SplitMap widget
        """
        from .split_map import SplitMap
        return SplitMap(
            left_layer_info=left_layer_info,
            right_layer_info=right_layer_info,
            center=self.center,
            zoom=self.zoom
        )