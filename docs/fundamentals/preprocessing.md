# Preprocessing overview

Raw MRI volumes are not analysis-ready. A handful of preprocessing steps are nearly universal, and most labs no longer hand-roll them — they delegate to a community BIDS-app.

## The universal steps

| Step | What it does | When |
| --- | --- | --- |
| **Format check** | BIDS validation, header sanity | Once per dataset |
| **Denoising / bias correction** | Remove scanner artifacts, intensity inhomogeneity | All modalities |
| **Motion correction** | Align volumes across time (fMRI, DWI) | 4D modalities |
| **Distortion correction** | Correct susceptibility distortions using field maps | EPI sequences (fMRI, DWI) |
| **Brain extraction** | Skull strip; mask the brain | All modalities |
| **Coregistration** | Align modalities within a subject | Multi-modal sessions |
| **Spatial normalisation** | Warp to a standard template (MNI, fsaverage) | Group analyses |
| **Tissue segmentation** | Grey / white / CSF labels | Most pipelines |
| **Surface reconstruction** | Build cortical surface mesh | Surface-based pipelines |

Each step has many implementations. Each implementation has decades of papers behind it. You do not need to reinvent them.

## Use a BIDS-app

A **BIDS-app** is a containerised, opinionated pipeline that consumes a BIDS dataset and produces a BIDS-derivatives dataset. The dominant ones:

- **fMRIPrep** — functional MRI preprocessing.
- **QSIPrep** — diffusion MRI preprocessing.
- **sMRIPrep** — structural MRI preprocessing.
- **MRIQC** — automated quality control reports.
- **PETPrep** — PET preprocessing.
- **HippUnfold**, **MELD**, **NiBabies**, **NiRodents** — modality / population specific.

They all run with the same CLI shape:

```bash
docker run --rm \
  -v $PWD/bids_dataset:/data:ro \
  -v $PWD/derivatives:/out \
  nipreps/fmriprep:24.0.0 /data /out participant \
  --fs-license-file /opt/fs_license.txt
```

The argument order — input, output, analysis-level — is part of the BIDS-app spec, so the same orchestration script works for all of them.

## Why this matters for data engineering

From a pipeline-engineering perspective, BIDS-apps give you four big things for free:

1. **Containerisation** — pinned, reproducible images.
2. **Idempotency** — most BIDS-apps skip already-completed work.
3. **Provenance** — output `dataset_description.json` records the BIDS-app version, key parameters, and a citation graph.
4. **Schema enforcement** — input validation happens before compute.

That covers four of the five pillars from [Data engineering → The five pillars](../data-engineering/five-pillars.md). The fifth — observability — is what you add on top.

## Pitfalls

- **TemplateFlow downloads.** Many BIDS-apps fetch templates at runtime. On HPC nodes without network access, pre-populate `${TEMPLATEFLOW_HOME}` before the run.
- **FreeSurfer license.** `recon-all` (and anything that wraps it) needs a `license.txt`. Free, but you have to request it from the FreeSurfer site.
- **Long runtimes.** `recon-all` is ~10 h per subject on CPU. FastSurfer is the DL-accelerated drop-in if your throughput matters.
- **Resource sizing.** fMRIPrep peaks at ~16 GB RAM and uses many cores; QSIPrep is heavier still. Look at the docs before sizing Slurm requests.

## Where to next

Once you have preprocessed data, you're in the [Data engineering](../data-engineering/index.md) section's world: how do you turn those derivatives into a reliable, observable, well-tested cohort-level pipeline?
