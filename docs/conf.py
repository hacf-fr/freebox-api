"""Sphinx configuration."""
from datetime import datetime


project = "aiofreepybox"
author = "HACF"
copyright = f"{datetime.now().year}, {author}"
extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon"]
autodoc_typehints = "description"
