# Your first NIfTI

> Load a brain volume in Python, inspect its shape and orientation, and view one slice. ~15 lines, ~5 minutes.

## 1. Get a real dataset

The `fixtures/sub-tiny/` dataset in this repo uses empty placeholder NIfTIs (for tests). For real data, download one subject from OpenNeuro:

```bash
mkdir -p data/openneuro
pip install osfclient                       # optional convenience
# Or simpler: use any T1w from your own BIDS dataset, or
# wget a single file from an OpenNeuro browser page.
wget -O data/sub-001_T1w.nii.gz \
  https://s3.amazonaws.com/openneuro.org/ds002785/sub-0001/anat/sub-0001_T1w.nii.gz
```

(The exact dataset / URL changes; pick any OpenNeuro T1w. If you can't download, the rest of this page works on any `.nii.gz` you have.)

## 2. Load it

Open a Python REPL or a notebook and:

```python
import nibabel as nib
img = nib.load("data/sub-001_T1w.nii.gz")
print(type(img))
```

`nib.load` returns a lazy image object — it has read the header but not the pixel data yet.

## 3. Inspect

```python
print("shape:", img.shape)               # e.g. (256, 256, 192)
print("voxel size (mm):", img.header.get_zooms())
print("data type:", img.get_data_dtype())
print("orientation:", nib.aff2axcodes(img.affine))   # ('R', 'A', 'S') = RAS
```

Three things to notice:

- **Shape** tells you the array dimensions. Structural T1w is 3D; BOLD is 4D (time as the last axis); DWI is 4D (directions).
- **Voxel size** is in millimetres. A 1×1×1 mm³ MPRAGE is typical structural. EPI is coarser (e.g. 2.4×2.4×2.4).
- **Orientation** tells you which axes go where. RAS is the NIfTI default; LPS is DICOM. See [Fundamentals → Coordinate systems](../fundamentals/coordinate-systems.md).

## 4. Get the actual voxels

```python
data = img.get_fdata()                    # returns a NumPy array
print("array shape:", data.shape, "dtype:", data.dtype)
print("min / max intensity:", data.min(), data.max())
```

## 5. Plot one slice

```python
import matplotlib.pyplot as plt
mid = data.shape[2] // 2                  # middle axial slice
slice_img = data[:, :, mid]

fig, ax = plt.subplots(figsize=(4, 4), dpi=120)
ax.imshow(slice_img.T, cmap="gray", origin="lower")
ax.set_title(f"Axial slice {mid}")
ax.axis("off")
fig.tight_layout()
fig.savefig("figs/first_nifti.png", bbox_inches="tight", dpi=200)
plt.show()
```

You should see a grey brain on a black background. If it's upside-down or mirrored, your image is in a non-canonical orientation — call `nib.as_closest_canonical(img)` before slicing.

## 6. A Nilearn version of the same thing

[Nilearn](https://nilearn.github.io) gives you a one-liner publication-style plot:

```python
from nilearn import plotting
plotting.plot_anat("data/sub-001_T1w.nii.gz",
                   title="My first T1w",
                   output_file="figs/first_nifti_nilearn.png")
```

You've just done what every neuroimaging script starts with.

## What you learned

- How to load and inspect a NIfTI.
- The four things a NIfTI carries: voxel array, affine, header, sometimes a JSON sidecar.
- The visualisation pattern: array → `imshow` → save.

## Where to next

[Your first BIDS app](first-bids-app.md) — run MRIQC on the fixture dataset.
