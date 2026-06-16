"""Quality-control helpers: per-subject manifests and simple metric checks."""

from neuro_handbook.qc.manifest import Manifest, StageRecord, write_manifest
from neuro_handbook.qc.metrics import check_connectome_shape

__all__ = [
    "Manifest",
    "StageRecord",
    "check_connectome_shape",
    "write_manifest",
]
