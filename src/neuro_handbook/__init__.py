"""neuro_handbook — companion utilities for the neuro-handbook reference site.

The submodules are intentionally small and readable. Each one ships the code
that appears in the handbook's worked examples; they are not meant to compete
with PyBIDS, nibabel, dcm2niix, or any other mature tool. Use them to learn,
then graduate to the real thing.
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("neuro-handbook")
except PackageNotFoundError:
    __version__ = "0.0.0+unknown"

__all__ = ["__version__"]
