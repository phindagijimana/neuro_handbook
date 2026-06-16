"""DICOM helpers.

This package wraps calls to dcm2niix and provides DICOM-to-BIDS conversion
context. It does not parse DICOM files directly — pydicom is the right tool
when you need that.
"""

from neuro_handbook.dicom.convert import ConversionResult, dicom_to_nifti

__all__ = ["ConversionResult", "dicom_to_nifti"]
