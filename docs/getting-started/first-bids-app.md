# Your first BIDS app

> Run [MRIQC](https://mriqc.readthedocs.io) on a tiny BIDS dataset. ~15 minutes the first time (most of it is the container pull).

[MRIQC](https://doi.org/10.1371/journal.pone.0184661) is the canonical "first BIDS app" because it doesn't need a FreeSurfer license and produces a human-readable HTML report. Once you've run one BIDS app you can run any of them — they share the same CLI shape.

## 1. The BIDS-app contract

Every modern BIDS app takes three positional arguments:

```text
<app> <bids_dir> <output_dir> <analysis_level>
```

with `analysis_level` being `participant` (per-subject) or `group` (cohort-level). Optional flags include `--participant-label`, `--n_cpus`, `--mem-mb`. That contract is what makes BIDS apps composable.

## 2. Prepare a real fixture

The `fixtures/sub-tiny/` in this repo is *valid BIDS* but the `.nii.gz` files are empty placeholders — fine for testing the walker, but MRIQC needs real bytes. Quickest path: download a small subject from OpenNeuro.

```bash
mkdir -p data/bids
cd data/bids

# Download one subject's T1w from a small OpenNeuro dataset
wget -O dataset_description.json \
  https://raw.githubusercontent.com/bids-standard/bids-examples/master/ds003/dataset_description.json
mkdir -p sub-01/anat
wget -O sub-01/anat/sub-01_T1w.nii.gz \
  https://s3.amazonaws.com/openneuro.org/ds000003/sub-01/anat/sub-01_T1w.nii.gz
wget -O sub-01/anat/sub-01_T1w.json \
  https://s3.amazonaws.com/openneuro.org/ds000003/sub-01/anat/sub-01_T1w.json
```

(URLs change on OpenNeuro; use whatever T1w you can grab.)

## 3. Validate the dataset

Always validate before running an app:

```bash
npx bids-validator data/bids
```

If it reports errors, fix them before the app sees them. See [BIDS toolkit → Validating a dataset](../bids/validation.md).

## 4. Run MRIQC — Docker version

```bash
docker run --rm -it \
  -v $(pwd)/data/bids:/data:ro \
  -v $(pwd)/data/derivatives:/out \
  nipreps/mriqc:24.0.2 \
  /data /out participant \
  --participant-label 01 \
  --nprocs 2
```

The first run pulls the image (~2 GB) — be patient. Subsequent runs reuse the cached layers.

## 5. Run MRIQC — Apptainer version (HPC)

```bash
apptainer build mriqc.sif docker://nipreps/mriqc:24.0.2

apptainer run --cleanenv \
  -B $(pwd)/data/bids:/data:ro \
  -B $(pwd)/data/derivatives:/out \
  mriqc.sif \
  /data /out participant \
  --participant-label 01 \
  --nprocs 2
```

## 6. Inspect the output

```bash
ls data/derivatives/
```

You should see:

```text
data/derivatives/
└── mriqc/
    ├── dataset_description.json
    ├── sub-01_T1w.html              ← open this in a browser
    ├── sub-01/
    │   └── anat/
    │       └── sub-01_T1w.json      ← all the QC metrics
    └── logs/
```

Open `sub-01_T1w.html` — it's a per-subject report with image-quality metrics (CNR, SNR, EFC, etc.) and a slice-by-slice background+foreground overlay. The metrics are also in the sibling JSON for programmatic use.

## 7. Run group-level (after several subjects)

```bash
docker run --rm \
  -v $(pwd)/data/bids:/data:ro \
  -v $(pwd)/data/derivatives:/out \
  nipreps/mriqc:24.0.2 \
  /data /out group
```

That produces a `group_T1w.tsv` + a group HTML — your cohort dashboard.

## What you learned

- The BIDS-app CLI contract (`bids_dir output_dir analysis_level`).
- The container invocation pattern (`-v` / `-B` bind mounts; `--cleanenv` for Apptainer).
- That BIDS-derivatives lands under `derivatives/<app-name>/` with its own `dataset_description.json`.
- Where to find both the human-readable report and the machine-readable JSON.

## Where to next

[Your first figure](first-figure.md) — load the QC results into Python and render a cohort plot.
