"""Minimal replacement for distutils.spawn.find_executable.

Provides find_executable(name) -> path or None using shutil.which.
This is intentionally tiny and only intended to satisfy packages that
import this single function (Streamlit in our case).
"""
import shutil
import typing

def find_executable(cmd: str) -> typing.Optional[str]:
    """Return the path to *cmd* if it exists on PATH, else None.

    Mirrors the behaviour of distutils.spawn.find_executable sufficiently
    for our use-case.
    """
    return shutil.which(cmd)
