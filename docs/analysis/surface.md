# Surface-based analysis

> Why analysing BOLD or thickness on the cortical surface often beats analysing it in a volume.

## Why surface at all (beginner orientation)

The cortex is a crumpled 2D sheet ~3 mm thick. Two voxels 5 mm apart in 3D can sit on opposite banks of a sulcus — geodesically far along the cortical sheet, but Euclidean-close. Volumetric smoothing happily blends signal across that sulcus, and across the grey/white boundary, and calls it neighbourhood. Surface analysis instead reconstructs the cortical sheet as a triangulated mesh, then defines distance, smoothing, and group statistics *along the cortex*. Neighbours on the mesh are neighbours in cytoarchitecture, not just in millimetres. The price: surface reconstruction is slow ([FreeSurfer `recon-all`](https://surfer.nmr.mgh.harvard.edu/fswiki/recon-all) ~8 h CPU; [FastSurfer](https://deep-mi.org/research/fastsurfer/) ~1 h GPU), brittle in pathology, and locks you into a template — fsaverage, [fsLR](https://www.humanconnectome.org/study/hcp-young-adult/document/extensively-processed-fmri-data-documentation), or a ciftify hybrid. Commit to one early and don't drift.

## The motivation

In a volumetric analysis, voxels on opposite banks of a sulcus are spatially close — millimetres apart — but functionally distant (different cytoarchitecture, different connectivity). A 6 mm smoothing kernel pools signal across the sulcus and blurs everything.

**Surface-based analysis** projects the data onto a triangulated mesh of the cortical surface. Smoothing along the mesh respects gyral / sulcal topology. The same anatomical neighbours stay neighbours.

## When it helps

- **Cortical thickness, surface area** — volumetric pipelines do this badly; FreeSurfer's surface output is the default for a reason.
- **Task fMRI in association cortex** — the buried tissue of the inferior frontal gyrus, the cingulate, the insula. Volumetric smoothing destroys their signal.
- **High-resolution 7 T data** — the cortical ribbon is < 4 mm; volumetric analysis is wasteful.
- **HCP-style multi-modal parcellations** — these live on the surface by design.

## When it doesn't help

- **Subcortical structures.** No surfaces. Analyse them volumetrically.
- **Low-resolution fMRI on small cortical samples.** The signal isn't there to find.
- **Lesion / tumour studies.** Pathology breaks surface reconstruction.

## fsLR vs fsaverage

Two standard surface spaces:

- **fsaverage** — FreeSurfer's template. Spherical registration. The de facto default for FreeSurfer-based work.
- **fsLR** — HCP's template. Better alignment, smaller mesh (32 k vertices per hemisphere). Default for HCP-pipeline outputs.

For a new study, start with whichever template your preprocessing pipeline emits, and pin it.

## Workflow

```python
import nibabel as nib
from nilearn import surface, plotting

# Load a thickness map on fsaverage.
lh_thickness = surface.load_surf_data("derivatives/freesurfer/sub-001/surf/lh.thickness")
fsavg = surface.load_surf_data("fsaverage/surf/lh.pial")

# Smooth along the mesh
from nilearn.surface import smooth_surface
smoothed = smooth_surface(fsavg, lh_thickness, fwhm=6.0)

# Plot
plotting.plot_surf_stat_map(fsavg, smoothed, hemi="left", view="lateral").show()
```

For BOLD timecourses, project the volumetric BOLD onto the surface with `vol_to_surf` (Nilearn) or `mri_vol2surf` (FreeSurfer).

## Statistics on the surface

The same statistical machinery — GLM, multiple-comparison correction — applies. Replace voxels with vertices. The cluster-correction logic uses the mesh's adjacency, not Euclidean adjacency, so a "cluster" is a connected patch on the surface.

**FreeSurfer's `mri_glmfit-sim`** is the venerable tool. **PALM** (FSL) handles arbitrary designs on the surface or in the volume. Nilearn's surface plotting is good; its surface statistics are still maturing.

## Where to next

[Group-level statistics](group-stats.md) — the cross-subject statistical machinery.
