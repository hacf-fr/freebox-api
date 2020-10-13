"""Sphinx configuration."""
from datetime import datetime


project = "freebox-api"
author = "HACF"
copyright = f"{datetime.now().year}, {author}"
extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon"]
autodoc_typehints = "description"
