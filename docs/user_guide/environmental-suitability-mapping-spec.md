# Claude Code Specification: Environmental Suitability Mapping Tool

## Project Overview
Build a Python command-line tool that generates 5-meter resolution suitability heat maps for environmental land management (starting with woodland creation). The tool processes geospatial datasets and outputs interactive visualizations to help farmers identify optimal locations for environmental interventions.

## Core Requirements

### Input Data Support
- **OSMasterMap** (shapefiles) - land cover and features
- **Soil data** (raster/vector) - drainage, texture, type
- **LiDAR DEM** (GeoTIFF) - elevation data for slope/aspect calculation
- **Farm boundary** (shapefile) - user-defined area of interest

### Processing Requirements
- Reproject all data to British National Grid (EPSG:27700)
- Resample to 5-meter resolution
- Clip analysis to farm boundary
- Implement Multi-Criteria Decision Analysis (MCDA) for woodland suitability

### Output Requirements
- **GeoTIFF** suitability raster
- **Static visualization** (PNG with heat map)
- **Interactive map** (HTML with Folium)
- **Summary statistics** (CSV)

## Technical Implementation

### Required Python Libraries
```python
# Core geospatial libraries
import geopandas as gpd
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
from rasterio.features import rasterize, geometry_mask
import numpy as np
import pandas as pd

# Analysis and visualization
from scipy.ndimage import sobel
import matplotlib.pyplot as plt
import folium
import json
import argparse
import os
from pathlib import Path
```

### Project Structure
```
environmental-suitability-tool/
├── src/
│   ├── __init__.py
│   ├── data_ingestion.py
│   ├── suitability_analysis.py
│   ├── output_generation.py
│   └── main.py
├── config/
│   └── woodland_creation.json
├── tests/
│   ├── test_data_ingestion.py
│   ├── test_suitability_analysis.py
│   └── test_output_generation.py
├── sample_data/
├── output/
├── requirements.txt
└── README.md
```

## Module Specifications

### 1. Data Ingestion Module (`data_ingestion.py`)

**Functions to implement:**
- `load_and_validate_inputs(osmm_path, soil_path, lidar_path, boundary_path=None)`
- `reproject_to_bng(dataset, target_resolution=5)`
- `clip_to_boundary(dataset, boundary_geom)`
- `resample_raster(raster, target_transform, target_shape)`

**Key functionality:**
- Validate file formats and coordinate systems
- Handle missing data through interpolation or masking
- Ensure all datasets align to 5m grid in EPSG:27700
- Provide clear error messages for invalid inputs

### 2. Suitability Analysis Module (`suitability_analysis.py`)

**Functions to implement:**
- `calculate_slope_from_dem(dem_array, pixel_size=5)`
- `extract_woodland_proximity(osmm_gdf, transform, shape, buffer_distance=100)`
- `score_soil_drainage(soil_array, drainage_mapping)`
- `apply_mcda(criteria_scores, weights_config)`

**MCDA Logic for Woodland Creation:**
- **Slope scoring**: <15° (score=1.0), 15-30° (score=0.5), >30° (score=0.0)
- **Soil drainage**: Well-drained (1.0), Moderate (0.5), Poor (0.0)
- **Proximity to woodland**: Within 100m (1.0), Beyond 100m (0.5)
- **Default weights**: Slope 40%, Soil 30%, Proximity 30%

### 3. Output Generation Module (`output_generation.py`)

**Functions to implement:**
- `save_geotiff(array, profile, output_path)`
- `create_static_visualization(suitability_array, output_path)`
- `create_interactive_map(suitability_array, bounds, output_path)`
- `export_summary_stats(suitability_array, output_path)`

### 4. Main CLI Interface (`main.py`)

**Command-line arguments:**
```bash
python main.py \
  --osmm path/to/osmastermap.shp \
  --soil path/to/soil_data.tif \
  --lidar path/to/dem.tif \
  --boundary path/to/farm_boundary.shp \
  --output output_directory \
  --config config/woodland_creation.json
```

## Configuration File Format

Create `config/woodland_creation.json`:
```json
{
  "option_name": "woodland_creation",
  "description": "Suitability analysis for woodland creation",
  "criteria": {
    "slope": {
      "weight": 0.4,
      "thresholds": [
        {"max_degrees": 15, "score": 1.0},
        {"max_degrees": 30, "score": 0.5},
        {"max_degrees": 999, "score": 0.0}
      ]
    },
    "soil_drainage": {
      "weight": 0.3,
      "mapping": {
        "well_drained": 1.0,
        "moderately_drained": 0.5,
        "poorly_drained": 0.0
      }
    },
    "proximity_to_woodland": {
      "weight": 0.3,
      "buffer_distance_m": 100,
      "inside_score": 1.0,
      "outside_score": 0.5
    }
  }
}
```

## Sample Implementation Templates

### Data Loading Template
```python
def load_and_validate_inputs(osmm_path, soil_path, lidar_path, boundary_path=None):
    """Load and validate all input datasets."""
    try:
        # Load vector data
        osmm = gpd.read_file(osmm_path)
        if boundary_path:
            boundary = gpd.read_file(boundary_path)
        else:
            boundary = None
            
        # Load raster data
        with rasterio.open(soil_path) as src:
            soil_data = src.read(1)
            soil_profile = src.profile
            
        with rasterio.open(lidar_path) as src:
            dem_data = src.read(1)
            dem_profile = src.profile
            
        return {
            'osmm': osmm,
            'boundary': boundary,
            'soil_data': soil_data,
            'soil_profile': soil_profile,
            'dem_data': dem_data,
            'dem_profile': dem_profile
        }
    except Exception as e:
        raise ValueError(f"Error loading input data: {str(e)}")
```

### Slope Calculation Template
```python
def calculate_slope_from_dem(dem_array, pixel_size=5):
    """Calculate slope in degrees from DEM array."""
    # Calculate gradients
    dy, dx = np.gradient(dem_array, pixel_size)
    
    # Calculate slope in degrees
    slope_radians = np.arctan(np.sqrt(dx**2 + dy**2))
    slope_degrees = np.degrees(slope_radians)
    
    return slope_degrees
```

### Visualization Template
```python
def create_static_visualization(suitability_array, output_path):
    """Create static heat map visualization."""
    plt.figure(figsize=(12, 8))
    plt.imshow(suitability_array, cmap='RdYlGn', vmin=0, vmax=1)
    plt.colorbar(label='Suitability Score (0-1)', shrink=0.8)
    plt.title('Woodland Creation Suitability Map')
    plt.xlabel('Easting (5m grid)')
    plt.ylabel('Northing (5m grid)')
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
```

## Testing Requirements

### Unit Tests
- Test data loading with various file formats
- Test coordinate reprojection accuracy
- Test MCDA calculations with known inputs
- Test output file generation

### Integration Tests
- Process a small sample dataset end-to-end
- Verify output file formats and content
- Test error handling with invalid inputs

### Sample Test Data
Create minimal test datasets:
- Small OSMasterMap shapefile (1km²)
- Simple soil raster with drainage values
- Basic DEM with elevation variations
- Test farm boundary polygon

## Performance Requirements
- Process 10 km² area in under 5 minutes
- Handle datasets up to 100 km² (with appropriate memory management)
- Provide progress indicators for long-running operations

## Error Handling
- Clear error messages for missing files
- Validation of coordinate systems before processing
- Graceful handling of missing data values
- Memory usage warnings for large datasets

## Documentation Requirements

### README.md should include:
- Installation instructions
- Usage examples
- Sample command-line calls
- Description of input data requirements
- Explanation of output files

### Code Documentation:
- Docstrings for all functions
- Type hints where appropriate
- Inline comments for complex calculations

## Extensibility Design
- Config-driven approach for adding new environmental options
- Modular criteria functions for easy customization
- Plugin architecture for additional data sources

## Success Criteria
1. Tool successfully processes sample data and produces all required outputs
2. Generated suitability maps show logical patterns (high scores near existing woodland, low scores on steep slopes)
3. All tests pass
4. Tool runs within performance requirements
5. Documentation is complete and clear

## Development Priority
1. **Phase 1**: Core data processing and MCDA implementation
2. **Phase 2**: Output generation and visualization
3. **Phase 3**: CLI interface and configuration system
4. **Phase 4**: Testing, optimization, and documentation

## Notes for Implementation
- Start with hardcoded criteria before implementing config file system
- Use small test datasets during development
- Implement logging for debugging large dataset processing
- Consider memory-mapped arrays for very large rasters
- Validate against known good results if available