"""Sphinx configuration."""
from datetime import datetime


project = "Freebox API"
author = "HACF (created by @fstercq, maintained by @Quentame)"
copyright = f"{datetime.now().year}, {author}"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
]
autodoc_typehints = "description"
html_theme = "furo"
