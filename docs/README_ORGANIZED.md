# 🌍 GeoMasterPy - Advanced Land Management Platform

A comprehensive geospatial application combining modern web technologies with powerful Earth observation data analysis capabilities.

## 🚀 Quick Start

### 🎯 Main Application
```bash
# Run the Streamlit interface
python streamlit_app.py

# Or run the main application
python run_app.py
```

### 🌐 Web Interface
Open `src/web/land-app-ui-mockup.html` in your browser for the standalone web application.

## 📂 Project Structure

```
GeoMasterPy/
├── 🎯 src/web/                    # Main web application
├── 📦 geomasterpy/               # Python package
├── 📚 docs/                      # Documentation
├── 🚀 deployment/               # Deployment configs
├── 📖 examples/                  # Usage examples
├── 🧪 tests/                     # Test suites
├── 📦 archive/                   # Archived/legacy code
└── ⚙️ scripts/                   # Utility scripts
```

## 🌟 Key Features

### 🗺️ **Interactive Mapping**
- **Drawing Tools**: Create polygons, circles, rectangles, and points
- **Plans Management**: Organize and manage spatial features
- **Multi-layer Support**: Toggle between different map layers
- **Real-time Analysis**: Instant area calculations and measurements

### 📊 **Earth Engine Integration**
- **Satellite Data**: Access to Google Earth Engine datasets
- **Time Series Analysis**: Historical data visualization
- **Custom Algorithms**: Advanced geospatial processing
- **Cloud Computing**: Scalable analysis on Google's infrastructure

### 🎓 **Learning Center**
- **Interactive Tutorials**: Step-by-step learning modules
- **AI Assistant**: Contextual help and guidance
- **Progress Tracking**: Achievement system with certificates
- **Course Library**: Structured learning paths

### 🔧 **OpenStreetMap Integration**
- **Real-time Data**: Live OSM feature loading
- **Context Menus**: Right-click interactions
- **Feature Inspection**: Detailed property viewing
- **Copy to Plans**: Seamless workflow integration

## 🛠️ Technology Stack

### Frontend
- **HTML5/CSS3**: Modern web standards with Material Design 3
- **JavaScript**: ES6+ with modular architecture
- **Leaflet.js**: Interactive mapping library
- **URL Routing**: Hash-based navigation system

### Backend
- **Python 3.8+**: Core application language
- **Streamlit**: Web application framework
- **Google Earth Engine**: Satellite data processing
- **GeoPandas**: Geospatial data manipulation

### Visualization
- **Cartopy**: Publication-quality static maps
- **Matplotlib**: Scientific plotting
- **Plotly**: Interactive visualizations
- **Custom Styling**: Material Design 3 components

## 📋 Installation

### Prerequisites
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Streamlit dependencies
pip install -r requirements_streamlit.txt
```

### Earth Engine Setup
```bash
# Authenticate with Google Earth Engine
python scripts/auth_earth_engine.py

# Test installation
python scripts/test_installation.py
```

## 🚀 Deployment

### Local Development
```bash
# Run Streamlit app
streamlit run streamlit_app.py

# Run standalone Python app
python run_app.py
```

### Streamlit Cloud
See `deployment/README_DEPLOYMENT.md` for cloud deployment instructions.

### GitHub Integration
```bash
# Deploy script
bash deployment/deploy.sh
```

## 📖 Documentation

- **🏗️ Architecture**: `docs/architecture/project-architecture.mmd`
- **👥 User Guide**: `docs/user_guide/`
- **🔧 API Reference**: `docs/api/`
- **📚 Examples**: `examples/`

## 🧪 Testing

```bash
# Run test suite
python -m pytest tests/

# Run specific tests
python -m pytest tests/test_data.py
```

## 📝 Development History

### Major Milestones
- ✅ **v1.0**: Core mapping functionality
- ✅ **v1.1**: Earth Engine integration
- ✅ **v1.2**: Learning Center implementation
- ✅ **v1.3**: URL routing system
- ✅ **v1.4**: Project organization and cleanup

### Archived Components
Legacy code and experimental features are preserved in:
- `archive/old_apps/`: Previous application versions
- `archive/old_scripts/`: Legacy utility scripts
- `archive/vendor/`: Third-party dependencies

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch
3. **Commit** your changes
4. **Push** to the branch
5. **Create** a Pull Request

## 📄 License

See `LICENSE` file for details.

## 🔗 Links

- **Documentation**: [Project Wiki](./docs/)
- **Examples**: [Usage Examples](./examples/)
- **Issues**: [GitHub Issues](../../issues)
- **Discussions**: [GitHub Discussions](../../discussions)

---

**📅 Last Updated**: 2025-06-15  
**🏷️ Version**: 1.4.0  
**👨‍💻 Status**: Production Ready