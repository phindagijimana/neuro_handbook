# Structural morphometry

> Measuring brain anatomy: cortical thickness, surface area, subcortical volume.

## The standard pipeline

1. **Acquire** a T1-weighted MPRAGE or MP2RAGE.
2. **Preprocess** with sMRIPrep or fMRIPrep (handles bias correction, brain extraction, normalisation).
3. **Reconstruct surfaces** with FreeSurfer's `recon-all` or its DL-accelerated equivalent **FastSurfer**.
4. **Parcellate** using the Desikan-Killiany (DK), Destrieux, or HCP-MMP atlas.
5. **Extract metrics** per region: thickness, surface area, volume, curvature, sulcal depth.

The output is a per-subject table: rows = regions, columns = metrics.

## FreeSurfer's standard outputs

After `recon-all`, every subject has:

```text
$SUBJECTS_DIR/sub-001/
├── mri/aparc+aseg.mgz          # cortical + subcortical parcellation
├── surf/lh.thickness            # per-vertex thickness, left hemi
├── surf/rh.thickness            # right hemi
├── label/lh.aparc.annot         # DK atlas labels on the left surface
└── stats/
    ├── aseg.stats               # subcortical volumes
    ├── lh.aparc.stats           # left cortical metrics per DK region
    └── rh.aparc.stats           # right
```

The `*.stats` files are tab-delimited text — read them with pandas.

## FastSurfer

`recon-all` takes ~10 hours per subject. FastSurfer replaces the slow parts (brain extraction, segmentation) with deep nets; runtime drops to ~1 hour CPU or ~10 minutes GPU. Outputs are FreeSurfer-compatible; downstream tools don't notice the difference.

If your cohort is > 50 subjects, switching to FastSurfer pays for itself in one rerun.

## ENIGMA harmonisation

The ENIGMA consortium publishes scripts that summarise FreeSurfer outputs into a single per-subject CSV with consistent column naming. Use them when:

- You're contributing to or pulling from a meta-analysis.
- You want to make site comparisons easier later.

## A quick worked example

```python
import pandas as pd
from pathlib import Path

# Pull every subject's DK thickness into one wide DataFrame.
rows = []
for stats in Path("derivatives/freesurfer").glob("sub-*/stats/lh.aparc.stats"):
    sub = stats.parents[1].name
    df = pd.read_csv(
        stats, comment="#", sep=r"\s+", header=None,
        names=["StructName", "NumVert", "SurfArea", "GrayVol",
               "ThickAvg", "ThickStd", "MeanCurv", "GausCurv",
               "FoldInd", "CurvInd"],
    )
    df = df[["StructName", "ThickAvg"]].set_index("StructName").T
    df.index = [sub]
    rows.append(df)

cohort = pd.concat(rows)
print(cohort.shape)  # (n_subjects, ~35 regions)
```

That's a cohort-level feature table. Feed it to the classical ML in [AI / ML → Classical ML](../ai/classical-ml.md).

## Pitfalls

- **Pial-surface failures.** A bad skull strip puts the pial surface inside the bone. Visual QC is non-optional.
- **Motion.** A subject who moved during the MPRAGE has noisy surfaces. Higher thickness variance than expected = check the raw scan.
- **Cross-sectional vs longitudinal.** FreeSurfer's longitudinal stream is *not* the same as running `recon-all` twice and subtracting. Use the longitudinal stream if you have timepoints.

## Where to next

[Diffusion & tractography](diffusion.md) — what the white-matter side of the same brain tells you.
