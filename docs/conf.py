import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'RockyDB'
copyright = '2022, Ahmed'
author = 'Ahmed'
release = '0.2.9'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']


add_module_names = False


pygments_style = "monokai"
