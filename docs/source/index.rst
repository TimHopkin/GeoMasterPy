GeoMasterPy Documentation
========================

GeoMasterPy is an interactive geospatial analysis library for Google Earth Engine that simplifies remote sensing workflows with intuitive tools for interactive mapping, data visualization, and analysis.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   api_reference
   examples
   tutorials

Features
--------

* **Interactive Mapping**: Easy-to-use map widgets with Earth Engine integration
* **Data Catalog**: Search and discover Earth Engine datasets
* **Visualization Tools**: Legends, colorbars, split maps, and animations
* **Geospatial Analysis**: Statistical analysis, classification, and spectral indices
* **Data Export**: Export images and vectors to local files or Google Drive
* **Publication Maps**: High-quality static maps using Cartopy

Quick Example
------------

.. code-block:: python

   import ee
   import geomasterpy as gmp

   # Initialize Earth Engine
   ee.Initialize()

   # Create an interactive map
   Map = gmp.Map(center=(40, -100), zoom=4)

   # Load Landsat data
   landsat = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2').first()

   # Add to map
   vis_params = {'bands': ['SR_B4', 'SR_B3', 'SR_B2'], 'min': 0, 'max': 3000}
   Map.add_ee_layer(landsat, vis_params, 'Landsat 8')

   # Display the map
   Map

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`