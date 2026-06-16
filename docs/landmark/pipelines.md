# Major pipelines

> One paragraph each on the pipelines you'll encounter, with a clear "what is this for".

## Anatomical / structural

- **FreeSurfer (`recon-all`)** — Cortical surface reconstruction + parcellation + subcortical segmentation. The reference. Slow (~10 h / subject). Outputs every other surface-based tool consumes.
- **FastSurfer** — Deep-learning re-implementation of `recon-all`. Same outputs, ~10 minutes GPU. Use when throughput matters.
- **sMRIPrep** — BIDS-app wrapper around the anatomical preprocessing in fMRIPrep. Minimal cortical pipeline; output is BIDS-derivatives.
- **ANTs (`antsCorticalThickness`)** — Alternative to FreeSurfer. Volumetric thickness; faster; some communities prefer it.

## Functional

- **fMRIPrep** — The standard BIDS-app for functional MRI preprocessing. Reads BIDS, writes BIDS-derivatives, ships a per-subject QC report. If you do fMRI in 2026, this is your starting point.
- **C-PAC** — Configurable Pipeline for the Analysis of Connectomes. Older, more customisable; still has users.
- **AFNI's `afni_proc.py`** — AFNI's official preprocessing script generator. Powerful, dense docs.

## Diffusion

- **QSIPrep** — The fMRIPrep of diffusion. Handles preprocessing across many DWI acquisition flavours.
- **QSIRecon** — Reconstruction layer on top of QSIPrep: SS3T-CSD, MSMT-CSD, NODDI, tractography.
- **MRtrix3** — The reconstruction / tractography workhorse. Tools are CLI; pipelines are scripts you compose.
- **DIPY** — Python-native diffusion library. Best for prototyping new models.

## Specialist

- **HippUnfold** — Unfolds the hippocampus into a 2D surface for sharper analysis of subfields.
- **MELD** — Lesion detection in epilepsy patients. Deep learning on FreeSurfer surfaces.
- **PETPrep** — BIDS-app for PET preprocessing.
- **NiBabies / Infant-FS** — Paediatric variants.
- **Nighres** — High-resolution / 7 T cortical processing.

## Decision quick-reference

| You have | Use |
| --- | --- |
| T1w + want cortical surfaces | FreeSurfer or FastSurfer |
| Task / resting fMRI | fMRIPrep |
| DWI for tractography or microstructure | QSIPrep + QSIRecon (or MRtrix3 directly) |
| Big cohort, slow `recon-all` is the bottleneck | Switch to FastSurfer |
| Hippocampal subfields | HippUnfold |
| PET | PETPrep |
| Lesion detection in epilepsy | MELD |
| Infant data | NiBabies |

## Where to next

[BIDS-app workflows](bids-apps.md) — the CLI shape they all share, and how to chain them.
