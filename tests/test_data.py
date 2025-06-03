"""
Tests for the Data module
"""

import pytest
from unittest.mock import Mock, patch
from geomasterpy.data.catalog import search_ee_data, js_snippet_to_python, get_dataset_info


class TestDataCatalog:
    """Test cases for data catalog functions"""
    
    def test_search_ee_data_landsat(self):
        """Test searching for Landsat data"""
        with patch('ee.Initialize'):
            results = search_ee_data('landsat', max_results=5)
            
            assert len(results) > 0
            assert any('landsat' in result['id'].lower() for result in results)
    
    def test_search_ee_data_sentinel(self):
        """Test searching for Sentinel data"""
        with patch('ee.Initialize'):
            results = search_ee_data('sentinel')
            
            assert len(results) > 0
            assert any('sentinel' in result['title'].lower() for result in results)
    
    def test_search_ee_data_no_results(self):
        """Test search with no results"""
        with patch('ee.Initialize'):
            results = search_ee_data('nonexistentdataset')
            
            # Should return empty list for non-existent datasets
            assert len(results) == 0
    
    def test_js_snippet_to_python_basic(self):
        """Test basic JavaScript to Python conversion"""
        js_code = """
        var image = ee.Image('LANDSAT/LC08/C02/T1_L2/LC08_044034_20140318');
        print(image);
        Map.addLayer(image, {bands: ['SR_B4', 'SR_B3', 'SR_B2']}, 'True Color');
        """
        
        python_code = js_snippet_to_python(js_code)
        
        assert 'var ' not in python_code
        assert 'print(' in python_code
        assert 'import ee' in python_code
        assert 'Map.add_ee_layer(' in python_code
    
    def test_js_snippet_to_python_variables(self):
        """Test JavaScript variable conversion"""
        js_code = "var x = 5; let y = 10; const z = 15;"
        python_code = js_snippet_to_python(js_code)
        
        assert 'var ' not in python_code
        assert 'let ' not in python_code
        assert 'const ' not in python_code
    
    def test_js_snippet_to_python_boolean_values(self):
        """Test JavaScript boolean value conversion"""
        js_code = "var isTrue = true; var isFalse = false; var nothing = null;"
        python_code = js_snippet_to_python(js_code)
        
        assert 'True' in python_code
        assert 'False' in python_code
        assert 'None' in python_code
        assert 'true' not in python_code.split('True')[0]  # Check original 'true' was replaced
    
    def test_js_snippet_to_python_comments(self):
        """Test JavaScript comment conversion"""
        js_code = "// This is a comment\nvar x = 5; // Another comment"
        python_code = js_snippet_to_python(js_code)
        
        assert '# This is a comment' in python_code
        assert '# Another comment' in python_code
        assert '//' not in python_code
    
    @patch('ee.Image')
    @patch('ee.Initialize')
    def test_get_dataset_info_image(self, mock_init, mock_image):
        """Test getting dataset info for an Image"""
        # Mock Earth Engine Image
        mock_ee_image = Mock()
        mock_ee_image.bandNames.return_value.getInfo.return_value = ['B1', 'B2', 'B3']
        mock_ee_image.propertyNames.return_value.getInfo.return_value = ['system:time_start']
        mock_image.return_value = mock_ee_image
        
        info = get_dataset_info('TEST/IMAGE')
        
        assert info is not None
        assert info['type'] == 'Image'
        assert 'bands' in info
        assert info['bands'] == ['B1', 'B2', 'B3']
    
    @patch('ee.ImageCollection')
    @patch('ee.Image')
    @patch('ee.Initialize')
    def test_get_dataset_info_collection(self, mock_init, mock_image, mock_collection):
        """Test getting dataset info for an ImageCollection"""
        # Mock Earth Engine ImageCollection and first Image
        mock_first_image = Mock()
        mock_first_image.bandNames.return_value.getInfo.return_value = ['B1', 'B2']
        mock_first_image.propertyNames.return_value.getInfo.return_value = ['system:time_start']
        
        mock_ee_collection = Mock()
        mock_ee_collection.first.return_value = mock_first_image
        mock_collection.return_value = mock_ee_collection
        mock_image.return_value = mock_first_image
        
        info = get_dataset_info('LANDSAT/LC08/C02/T1_L2')
        
        assert info is not None
        assert info['type'] == 'ImageCollection'
    
    def test_get_dataset_info_invalid(self):
        """Test getting info for invalid dataset"""
        with patch('ee.Initialize'):
            with patch('builtins.print'):  # Suppress error print
                info = get_dataset_info('INVALID/DATASET')
                assert info is None