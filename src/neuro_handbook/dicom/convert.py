"""Thin wrapper around ``dcm2niix`` for DICOM → NIfTI conversion.

The function does not depend on ``dcm2niix`` being installed at import time;
it raises a clear error at call time if the binary is missing. This is the
same pattern most BIDS apps use.
"""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ConversionResult:
    """Outcome of a ``dcm2niix`` invocation."""

    nifti_files: tuple[Path, ...]
    json_sidecars: tuple[Path, ...]
    stdout: str
    stderr: str


def dicom_to_nifti(
    dicom_dir: Path | str,
    output_dir: Path | str,
    *,
    filename_template: str = "%p_%s",
    compress: bool = True,
    bids_sidecar: bool = True,
    dcm2niix_bin: str = "dcm2niix",
) -> ConversionResult:
    """Convert a folder of DICOM files to NIfTI using ``dcm2niix``.

    Parameters
    ----------
    dicom_dir
        Folder containing the DICOM series. Sub-folders are walked recursively.
    output_dir
        Where to place the resulting ``.nii.gz`` and ``.json`` files.
    filename_template
        ``dcm2niix`` filename pattern. See ``dcm2niix -h``.
    compress
        Produce ``.nii.gz`` instead of ``.nii``.
    bids_sidecar
        Emit a BIDS-compatible JSON sidecar next to each NIfTI.
    dcm2niix_bin
        Path or name of the ``dcm2niix`` binary.
    """
    dicom_dir = Path(dicom_dir).resolve()
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    binary = shutil.which(dcm2niix_bin)
    if binary is None:
        raise FileNotFoundError(
            f"Could not find '{dcm2niix_bin}' on PATH. Install it from "
            "https://github.com/rordenlab/dcm2niix or pass dcm2niix_bin=..."
        )

    cmd = [
        binary,
        "-f", filename_template,
        "-z", "y" if compress else "n",
        "-b", "y" if bids_sidecar else "n",
        "-o", str(output_dir),
        str(dicom_dir),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(
            f"dcm2niix failed (exit {proc.returncode}):\n{proc.stderr}"
        )

    nifti = tuple(sorted(output_dir.glob("*.nii*")))
    sidecars = tuple(sorted(output_dir.glob("*.json"))) if bids_sidecar else ()
    return ConversionResult(
        nifti_files=nifti,
        json_sidecars=sidecars,
        stdout=proc.stdout,
        stderr=proc.stderr,
    )
