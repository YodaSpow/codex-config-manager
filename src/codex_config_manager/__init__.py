"""Codex Config Manager."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("codex-config-manager")
except PackageNotFoundError:
    __version__ = "0.1.0"

CONTRACT_VERSION = 1
