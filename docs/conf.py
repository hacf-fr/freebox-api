"""Sphinx configuration."""
from datetime import datetime


project = "aiofreepybox"
author = "stilllman"
copyright = f"{datetime.now().year}, {author}"
extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon"]
autodoc_typehints = "description"
