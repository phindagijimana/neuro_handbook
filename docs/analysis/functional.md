# Functional connectivity

> Estimating which brain regions co-fluctuate in their BOLD signal — the most common rs-fMRI analysis.

## The standard pipeline

1. **Acquire** resting-state or task BOLD.
2. **Preprocess** with fMRIPrep (motion correction, distortion correction, registration, optional ICA-AROMA).
3. **Confound regression** — remove motion, physiological noise, and global signal effects.
4. **Parcellate** — extract one timecourse per atlas region.
5. **Compute connectivity** — typically Pearson correlation, partial correlation, or tangent-space embedding.
6. **Threshold or weight** the resulting matrix; analyse.

## Nilearn — the Python workhorse

Nilearn (<https://nilearn.github.io>) wraps the preprocessing-to-connectivity pipeline for fMRI in a scikit-learn-style API:

```python
from nilearn.maskers import NiftiLabelsMasker
from nilearn.connectome import ConnectivityMeasure
import nibabel as nib

masker = NiftiLabelsMasker(
    labels_img="Schaefer400.nii.gz",
    standardize=True,
    detrend=True,
    high_pass=0.01,
    low_pass=0.1,
    t_r=2.0,
)
timecourses = masker.fit_transform(
    "sub-001_desc-preproc_bold.nii.gz",
    confounds="sub-001_desc-confounds_timeseries.tsv",
)
conn = ConnectivityMeasure(kind="correlation").fit_transform([timecourses])[0]
```

A 400×400 connectivity matrix in ~30 lines.

## Confound regression — the part most people get wrong

fMRIPrep emits a `*_desc-confounds_timeseries.tsv` with dozens of columns. You don't use all of them. Common reasonable strategies:

| Strategy | Columns |
| --- | --- |
| **6 motion + global signal** | `trans_x..z`, `rot_x..z`, `global_signal` |
| **24 motion** | The 6 motion params, their squares, derivatives, derivatives squared |
| **ACompCor** | Top-5 PCA components from white matter + CSF masks |
| **ICA-AROMA + 24 motion** | Use AROMA-cleaned BOLD plus motion |

Pick one strategy, document it, apply it consistently across your cohort. The reproducibility crisis in resting-state fMRI is partly a "everyone picks a different confound set" crisis.

## Connectivity measures

- **Pearson correlation** — the workhorse. Symmetric, interpretable.
- **Partial correlation** — controls for the rest of the network. Cleaner for graph-theory analyses.
- **Tangent-space embedding** — Nilearn's `kind="tangent"`. Better for ML on cohorts of connectomes (Pearson matrices live on a curved manifold; tangent projections live on a flat one).
- **Mutual information / sparse covariance** — for non-linear or sparse connectivity assumptions.

For most papers, Pearson + Fisher z-transform is fine.

## Group analyses

A common pattern: stack each subject's connectivity matrix into a 3D array `(n_subjects, n_regions, n_regions)`, then:

- **Edge-wise tests** — `n_regions * (n_regions - 1) / 2` mass-univariate tests. Multiple-comparison correction is essential.
- **Network-level summaries** — within-network connectivity, modularity, degree.
- **NBS (Network-Based Statistics)** — clusters of connected significant edges; usually more powerful than edge-wise FDR.

See [Multiple comparisons](multiple-comparisons.md) before believing any p-value.

## Pitfalls

- **Motion is the dominant confound.** A "group difference" between movers and non-movers is what you'll find if you don't censor or regress motion properly.
- **Global signal regression is contentious.** Removes some real signal along with the noise. Document whether you did or didn't.
- **Atlas choice matters.** Schaefer-400 is not equivalent to Power-264 is not equivalent to Yeo-7. Stick with one per study.

## Where to next

[Surface-based analysis](surface.md) — when volumetric BOLD averaging blurs across sulci.
