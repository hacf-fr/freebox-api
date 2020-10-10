# -*- coding:utf-8 -*-
"""
Provides authentification and row access to Freebox using Freebox OS developer API.
Freebox API documentation : http://dev.freebox.fr/sdk/os/
"""
# __version__ need to be declare before import to avoid circular import
__version__ = "0.0.8"

from aiofreepybox.aiofreepybox import Freepybox

__all__ = ["Freepybox"]
