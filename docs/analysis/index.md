# Analysis

> What you can compute from preprocessed neuroimaging data, organised by modality.

This section assumes the data has already been through a BIDS app (see [Fundamentals → Preprocessing](../fundamentals/preprocessing.md)). The pages below show what comes next.

- **[Structural morphometry](structural.md)** — cortical thickness, surface area, subcortical volumes; FreeSurfer + ENIGMA pipelines.
- **[Diffusion & tractography](diffusion.md)** — tensor metrics (FA / MD), HARDI reconstruction, fibre tracking, connectomes.
- **[Functional connectivity](functional.md)** — seed-based, ROI-to-ROI, ICA; Nilearn's role in the modern stack.
- **[Surface-based analysis](surface.md)** — when volumetric analysis loses the signal and surfaces don't.
- **[Group-level statistics](group-stats.md)** — voxel-wise, vertex-wise, network-level; GLM, mixed models, permutation.
- **[Multiple comparisons](multiple-comparisons.md)** — FDR, FWE, TFCE, cluster correction, and how to choose.

## How to read it

Each page is self-contained and modality-focused. If you only do fMRI, you don't have to read the diffusion page. The two statistics pages, though, apply to everything — read them.

## Engineering vs analysis

Analysis is the *what*; engineering is the *how*. A well-engineered pipeline that computes the wrong statistic is no better than a brittle script that computes the right one. This section focuses on the statistics and methods; the [Data engineering](../data-engineering/index.md) section handles the pipeline mechanics.
