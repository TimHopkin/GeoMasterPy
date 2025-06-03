"""
Split Map widget for side-by-side comparison of Earth Engine layers.
"""

import ee
import ipyleaflet as ipyl
from ipywidgets import widgets, HBox
from typing import Dict, Any, Tuple, Union


class SplitMap(HBox):
    """
    Split-screen map widget for comparing two layers side by side.
    """
    
    def __init__(self, left_layer_info: Tuple[Any, Dict, str], 
                 right_layer_info: Tuple[Any, Dict, str],
                 center: Tuple[float, float] = (40, -100), zoom: int = 4):
        """
        Initialize split map.
        
        Args:
            left_layer_info: Tuple of (ee_object, vis_params, name) for left map
            right_layer_info: Tuple of (ee_object, vis_params, name) for right map
            center: Map center coordinates
            zoom: Initial zoom level
        """
        # Create two map instances
        self.left_map = ipyl.Map(center=center, zoom=zoom, layout={'width': '50%'})
        self.right_map = ipyl.Map(center=center, zoom=zoom, layout={'width': '50%'})
        
        # Add controls
        self.left_map.add_control(ipyl.ScaleControl(position='bottomleft'))
        self.right_map.add_control(ipyl.ScaleControl(position='bottomleft'))
        
        # Add layers
        self._add_ee_layer_to_map(self.left_map, *left_layer_info)
        self._add_ee_layer_to_map(self.right_map, *right_layer_info)
        
        # Synchronize map views
        self._link_maps()
        
        # Initialize HBox with both maps
        super().__init__([self.left_map, self.right_map])
    
    def _add_ee_layer_to_map(self, map_widget: ipyl.Map, ee_object: Any, 
                            vis_params: Dict[str, Any], name: str):
        """Add Earth Engine layer to a specific map."""
        try:
            if isinstance(ee_object, ee.Image):
                map_id_dict = ee.Image(ee_object).getMapId(vis_params)
            elif isinstance(ee_object, ee.ImageCollection):
                image = ee_object.mosaic()
                map_id_dict = ee.Image(image).getMapId(vis_params)
            elif isinstance(ee_object, ee.FeatureCollection):
                # Style vector data
                default_style = {'color': 'blue', 'width': 2}
                style = {**default_style, **vis_params}
                styled_vector = ee_object.style(**style)
                map_id_dict = styled_vector.getMapId()
            else:
                print(f"Unsupported Earth Engine object type: {type(ee_object)}")
                return
            
            # Create and add tile layer
            tile_layer = ipyl.TileLayer(
                url=map_id_dict['tile_fetcher'].url_format,
                attribution='Google Earth Engine',
                name=name
            )
            map_widget.add_layer(tile_layer)
            
        except Exception as e:
            print(f"Error adding layer {name}: {str(e)}")
    
    def _link_maps(self):
        """Synchronize the view of both maps."""
        # Link zoom and center
        widgets.jslink((self.left_map, 'zoom'), (self.right_map, 'zoom'))
        widgets.jslink((self.left_map, 'center'), (self.right_map, 'center'))