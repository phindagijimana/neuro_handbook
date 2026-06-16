"""Minimal BIDS-aware helpers.

For real work use PyBIDS. The helpers here exist so the handbook can show
exactly how the BIDS layout is parsed without hiding it behind a dependency.
"""

from neuro_handbook.bids.walker import BIDSEntity, BIDSImage, walk_bids

__all__ = ["BIDSEntity", "BIDSImage", "walk_bids"]
