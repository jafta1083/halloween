"""Lightweight shim for `distutils` used by downstream tools when
the stdlib `distutils` package isn't available (Python 3.12+).

This module provides only a tiny subset required by Streamlit: the
`distutils.spawn.find_executable` function. It delegates to
shutil.which so it behaves similarly for finding executables in PATH.

This shim lives in the project root so it will be importable by the
virtualenv Python used to run the app.
"""

__all__ = ["spawn"]

from . import spawn
