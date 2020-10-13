"""
Provides authentification and access to Freebox using Freebox OS developer API.
Freebox API documentation : http://dev.freebox.fr/sdk/os/
"""
# __version__ need to be declare before import to avoid circular import
# importlib.metadata available from Python 3.8 use importlib_metadata for
# earlier versions.
try:
    from importlib.metadata import version, PackageNotFoundError  # type: ignore
except ImportError:  # pragma: no cover
    from importlib_metadata import version, PackageNotFoundError  # type: ignore


try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"

from freebox_api.aiofreepybox import Freepybox

__all__ = ["Freepybox"]
