# Tutorials

> End-to-end walkthroughs that exercise everything else in the handbook. Each is written so you can paste blocks into a Jupyter notebook or a script and run them.

## The four tutorials

<div class="grid cards" markdown>

-   :material-vector-line: **[DWI cohort tractography](dwi-cohort.md)**

    ---

    Take an OpenNeuro DWI cohort through QSIPrep + QSIRecon, build connectomes, run a group-level edge-wise test. Covers BIDS, container orchestration, MRtrix3, statistical correction.

-   :material-chart-line: **[fMRI first/second-level GLM](fmri-glm.md)**

    ---

    Task-fMRI from preprocessed BIDS-Derivatives through Nilearn's first-level GLM, contrast estimation, and group-level inference. Covers HRF, design matrices, confound regression, permutation FWE.

-   :material-brain: **[Cortical thickness ML](cortical-thickness-ml.md)**

    ---

    Train a classical ML model to predict age from FreeSurfer-derived cortical thickness, with proper site-stratified cross-validation, ComBat harmonisation, and honest reporting.

-   :material-puzzle: **[Lesion segmentation with nnU-Net](lesion-segmentation.md)**

    ---

    Train and evaluate a 3D lesion-segmentation model on a small public dataset (e.g. ATLAS or WMH), with patch sampling, class-imbalanced loss, and cross-site evaluation.

-   :material-flag-checkered: **[Capstone — DICOM to published figure](capstone.md)**

    ---

    The integrated tutorial: take one subject from raw DICOM through BIDS, fMRIPrep, first-level GLM, registration, and a publication-style multi-panel figure. The whole pipeline on one screen.

</div>

## How to read them

Each tutorial:

- States its **prerequisites** (links to earlier handbook chapters and required tools).
- Walks through the **conceptual pipeline** before the code.
- Provides **runnable code blocks** you paste into a notebook or `.py` file.
- Ends with a **what went wrong / what could go wrong** section.
- Cites the **primary methods papers** for everything it uses.

Tutorials assume you've completed [Getting Started](../getting-started/index.md). They are *not* a replacement for the foundations chapters — the goal is synthesis, not first-time exposure.

## Data sources

Tutorials download small example data from public sources:

- **OpenNeuro** ([https://openneuro.org](https://openneuro.org)) — open BIDS datasets.
- **NiBabel test data** — bundled small NIfTI files.
- **Nilearn datasets** — `datasets.fetch_*` helpers.
- **MONAI tutorial data** — for the segmentation tutorial.

If your institution is air-gapped, mirror the data once and edit the paths.
