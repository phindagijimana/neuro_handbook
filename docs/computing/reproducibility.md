# Reproducibility checklist

> A twelve-line audit to run before publishing a result.

Most "I can't reproduce this" failures are not exotic. They cluster around a handful of mistakes. Catch them with this list.

## Before you publish a number

- [ ] **Code is in version control** and a tagged release matches the figure in the paper.
- [ ] **Lockfile or container** records every dependency. The exact commit + lockfile + container digest is enough to recreate the environment.
- [ ] **Random seeds set** for any non-deterministic step (PyTorch, NumPy, splitting, augmentation).
- [ ] **Subject-level splits** documented and enforced (no leakage between train and test).
- [ ] **Data version** is identifiable — DataLad tag, OpenNeuro version, or DOI.
- [ ] **All preprocessing parameters** recorded — fMRIPrep version, TemplateFlow version, atlases used.
- [ ] **Statistical model** fully specified — design matrix, covariates, correction method, threshold.
- [ ] **Software versions** (FSL, FreeSurfer, ANTs, MRtrix3, etc.) recorded per-subject in a manifest.
- [ ] **Exact commands** to reproduce in a script or notebook checked into the repo. "I ran X with default settings" is not enough.
- [ ] **Inputs and outputs identifiable** — sidecar `Sources` fields or a per-output `manifest.json`.
- [ ] **A test cohort** (your `fixtures/sub-tiny/` equivalent) exists and the analysis runs on it end-to-end in CI.
- [ ] **Failure cases reported** — at least one subject the model got wrong, with diagnosis.

If you can tick all twelve, your result is in the top decile of reproducibility for the field.

## A practical pattern

The simplest implementation that satisfies this list:

```text
analysis-repo/
├── README.md                    # how to run end-to-end
├── pyproject.toml + uv.lock     # Python env
├── apptainer.def or Dockerfile  # binary env
├── analysis/                    # scripts, one per figure
├── notebooks/                   # exploratory; restart-and-run-all
├── tests/                       # at least one runs in CI
├── fixtures/                    # tiny dataset
└── outputs/                     # gitignored — derived from inputs + code
```

`make repro` re-runs everything from raw data + code. If `make repro` works two years later, you've achieved backward reproducibility.

## Where to next

That closes the Computing section. The next thing to read is [Landmark work](../landmark/index.md) — the papers, pipelines, and datasets that shaped the field.
