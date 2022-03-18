"""Skeleton init file."""
import sys

if sys.version_info[:2] >= (3, 8):
    from importlib.metadata import PackageNotFoundError  # pragma: no cover
    from importlib.metadata import version  # pragma: no cover
else:
    from importlib_metadata import PackageNotFoundError  # pragma: no cover
    from importlib_metadata import version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "friendly-parakeet"
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError
