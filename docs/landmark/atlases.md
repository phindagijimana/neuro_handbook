# Atlases and templates

> The standard parcellations and template spaces you'll see in papers and pipelines.

## Cortical parcellations

| Atlas | Granularity | Where it comes from |
| --- | --- | --- |
| **Desikan-Killiany (DK)** | 68 cortical regions | FreeSurfer; widely cited; coarse but robust |
| **Destrieux (`aparc.a2009s`)** | 148 cortical regions | FreeSurfer; finer; gyral-based |
| **HCP-MMP1 (Glasser)** | 360 regions | Multi-modal HCP parcellation; surface only |
| **Schaefer** | 100 / 200 / 400 / 600 / 800 / 1000 regions | Functionally driven; choose granularity |
| **AAL** | 116 regions | Older, widely cited; volumetric |

## Subcortical parcellations

- **FreeSurfer `aseg`** — 16+ subcortical structures. The default.
- **Tian** — fine-grained subcortical, designed to pair with Schaefer cortex.
- **CIT168** — high-resolution subcortical atlas.

## White-matter atlases

- **JHU ICBM-DTI** — white-matter tracts; the volumetric default.
- **HCP1065 tractogram atlas** — major bundles defined on the HCP.
- **TractSeg atlas** — DL-defined bundles; current state-of-the-art for fast bundle segmentation.

## Standard template spaces

| Template | Where it lives | When |
| --- | --- | --- |
| **MNI152NLin2009cAsym** | Volumetric | fMRIPrep / QSIPrep default; modern choice |
| **MNI152NLin6Asym** | Volumetric | FSL's legacy default; still common |
| **MNI152 ICBM 2009c** | Volumetric | The non-asymmetric variant; less common |
| **fsaverage** | Surface | FreeSurfer's default; 163 842 vertices per hemi |
| **fsLR (32k_fs_LR)** | Surface | HCP's default; 32 492 vertices per hemi |
| **Colin27** | Single-subject template | Older; for very high-resolution single-subject work |

Different MNI templates are **not interchangeable**. Always record which one your derivatives are in.

## TemplateFlow

<https://www.templateflow.org> distributes versioned templates as a pip-installable archive. Use it instead of bundling templates in your repo:

```python
from templateflow import api as tflow
img = tflow.get("MNI152NLin2009cAsym", resolution=1, desc="brain", suffix="T1w")
```

Templates have version numbers; pin them in your manifest alongside container digests.

## Naming derivatives accordingly

When you write a derivative into MNI space, the filename should carry the `space-` entity:

```text
sub-001_space-MNI152NLin2009cAsym_desc-preproc_T1w.nii.gz
```

This is what makes BIDS-derivatives self-describing.

## Where to next

That closes the Landmark work section. Loop back to the [Home page](../index.md) for an overview of the rest of the handbook.
