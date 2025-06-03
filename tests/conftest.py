"""
Pytest configuration and fixtures for GeoMasterPy tests
"""

import pytest
from unittest.mock import Mock, patch
import ee


@pytest.fixture(autouse=True)
def mock_ee_initialize():
    """Automatically mock Earth Engine initialization for all tests"""
    with patch('ee.Initialize'):
        yield


@pytest.fixture
def mock_ee_image():
    """Mock Earth Engine Image"""
    mock_image = Mock()
    mock_image.bandNames.return_value.getInfo.return_value = ['B1', 'B2', 'B3', 'B4']
    mock_image.propertyNames.return_value.getInfo.return_value = ['system:time_start', 'CLOUD_COVER']
    mock_image.getMapId.return_value = {
        'tile_fetcher': Mock(url_format='http://test.com/{z}/{x}/{y}')
    }
    mock_image.clip.return_value = mock_image
    mock_image.select.return_value = mock_image
    mock_image.normalizedDifference.return_value = mock_image
    mock_image.rename.return_value = mock_image
    return mock_image


@pytest.fixture  
def mock_ee_collection():
    """Mock Earth Engine ImageCollection"""
    mock_collection = Mock()
    mock_collection.filterBounds.return_value = mock_collection
    mock_collection.filterDate.return_value = mock_collection
    mock_collection.filter.return_value = mock_collection
    mock_collection.median.return_value = Mock()  # Returns an Image
    mock_collection.first.return_value = Mock()   # Returns an Image
    mock_collection.map.return_value = mock_collection
    return mock_collection


@pytest.fixture
def mock_ee_geometry():
    """Mock Earth Engine Geometry"""
    mock_geometry = Mock()
    mock_geometry.bounds.return_value.getInfo.return_value = {
        'coordinates': [[[-122.5, 37.7], [-122.3, 37.7], [-122.3, 37.8], [-122.5, 37.8], [-122.5, 37.7]]]
    }
    mock_geometry.getInfo.return_value = {
        'type': 'Polygon',
        'coordinates': [[[-122.5, 37.7], [-122.3, 37.7], [-122.3, 37.8], [-122.5, 37.8], [-122.5, 37.7]]]
    }
    return mock_geometry


@pytest.fixture
def sample_vis_params():
    """Sample visualization parameters"""
    return {
        'bands': ['B4', 'B3', 'B2'],
        'min': 0,
        'max': 3000,
        'gamma': 1.4
    }