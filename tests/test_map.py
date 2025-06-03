"""
Tests for the Map module
"""

import pytest
import ee
from unittest.mock import Mock, patch
from geomasterpy.map.interactive_map import Map


class TestMap:
    """Test cases for the Map class"""
    
    def test_map_initialization(self):
        """Test basic map initialization"""
        with patch('ee.Initialize'):
            map_widget = Map(center=(40, -100), zoom=4)
            assert map_widget.center == (40, -100)
            assert map_widget.zoom == 4
    
    def test_map_with_lite_mode(self):
        """Test map initialization in lite mode"""
        with patch('ee.Initialize'):
            map_widget = Map(lite_mode=True)
            assert map_widget.lite_mode == True
    
    def test_add_basemap(self):
        """Test adding basemaps"""
        with patch('ee.Initialize'):
            map_widget = Map()
            
            # Test valid basemap
            map_widget.add_basemap('OpenStreetMap')
            # Should not raise an error
            
            # Test invalid basemap
            with patch('builtins.print') as mock_print:
                map_widget.add_basemap('InvalidBasemap')
                mock_print.assert_called()
    
    @patch('ee.Image')
    def test_add_ee_layer_image(self, mock_image):
        """Test adding Earth Engine Image layers"""
        with patch('ee.Initialize'):
            map_widget = Map()
            
            # Mock Earth Engine Image
            mock_ee_image = Mock()
            mock_ee_image.getMapId.return_value = {
                'tile_fetcher': Mock(url_format='http://test.com/{z}/{x}/{y}')
            }
            
            vis_params = {'min': 0, 'max': 100}
            
            with patch('ee.Image', return_value=mock_ee_image):
                map_widget.add_ee_layer(mock_ee_image, vis_params, 'Test Layer')
                
                assert 'Test Layer' in map_widget._ee_layers
    
    def test_set_center(self):
        """Test setting map center"""
        with patch('ee.Initialize'):
            map_widget = Map()
            map_widget.set_center(37.7749, -122.4194, 10)
            
            assert map_widget.center == (37.7749, -122.4194)
            assert map_widget.zoom == 10
    
    def test_zoom_to_bounds(self):
        """Test zooming to bounds"""
        with patch('ee.Initialize'):
            map_widget = Map()
            bounds = (-122.5, 37.7, -122.3, 37.8)
            
            with patch.object(map_widget, 'fit_bounds') as mock_fit_bounds:
                map_widget.zoom_to_bounds(bounds)
                mock_fit_bounds.assert_called_once()
    
    def test_remove_ee_layer(self):
        """Test removing Earth Engine layers"""
        with patch('ee.Initialize'):
            map_widget = Map()
            
            # Add a mock layer first
            mock_layer = Mock()
            map_widget._ee_layers['test'] = {
                'layer': mock_layer,
                'ee_object': Mock(),
                'vis_params': {}
            }
            
            with patch.object(map_widget, 'remove_layer') as mock_remove:
                map_widget.remove_ee_layer('test')
                mock_remove.assert_called_once_with(mock_layer)
                assert 'test' not in map_widget._ee_layers
    
    def test_clear_ee_layers(self):
        """Test clearing all Earth Engine layers"""
        with patch('ee.Initialize'):
            map_widget = Map()
            
            # Add some mock layers
            map_widget._ee_layers = {
                'layer1': {'layer': Mock(), 'ee_object': Mock(), 'vis_params': {}},
                'layer2': {'layer': Mock(), 'ee_object': Mock(), 'vis_params': {}}
            }
            
            with patch.object(map_widget, 'remove_ee_layer') as mock_remove:
                map_widget.clear_ee_layers()
                assert len(map_widget._ee_layers) == 0
    
    def test_get_drawing_data(self):
        """Test getting drawing data"""
        with patch('ee.Initialize'):
            map_widget = Map()
            
            # Mock draw control
            mock_draw_control = Mock()
            mock_draw_control.last_draw = {'type': 'Feature'}
            mock_draw_control.data = [{'type': 'Feature'}]
            map_widget.draw_control = mock_draw_control
            
            data = map_widget.get_drawing_data()
            assert 'last_draw' in data
            assert 'data' in data