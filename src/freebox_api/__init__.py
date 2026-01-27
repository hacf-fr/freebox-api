"""
Provides authentification and access to Freebox using Freebox OS developer API.
Freebox API documentation : http://dev.freebox.fr/sdk/os/
"""

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version

try:
    __version__: str = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"

from freebox_api.aiofreepybox import Freepybox

__all__ = ["Freepybox"]
