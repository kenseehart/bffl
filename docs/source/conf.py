# Configuration file for the Sphinx documentation builder.

# -- Project information -----------------------------------------------------

project = 'bffl'
copyright = '2020-2024, Ken Seehart'
author = 'Ken Seehart'

# The full version, including alpha/beta/rc tags
release = '0.3.2'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
