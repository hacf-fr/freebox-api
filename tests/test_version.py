"""Test the single source version in pyproject.toml"""
from packaging.version import Version

import aiofreepybox


def test_single_source_version() -> None:
    """
    It is compliant with the standard version scheme for Python packages
    """
    Version(aiofreepybox.__version__)
