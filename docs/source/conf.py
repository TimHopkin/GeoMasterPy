# Configuration file for the Sphinx documentation builder.

# Project information
project = 'GeoMasterPy'
copyright = '2024, GeoMasterPy Development Team'
author = 'GeoMasterPy Development Team'
release = '0.1.0'

# General configuration
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax',
    'myst_nb',
    'sphinx_rtd_theme'
]

templates_path = ['_templates']
exclude_patterns = []

# Options for HTML output
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Napoleon settings for Google/NumPy style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False

# MyST-NB settings
nb_execution_mode = "off"
nb_execution_timeout = 300

# Intersphinx mapping
intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'pandas': ('https://pandas.pydata.org/docs/', None),
    'matplotlib': ('https://matplotlib.org/stable/', None),
}