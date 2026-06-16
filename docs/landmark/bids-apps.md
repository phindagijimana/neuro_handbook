# BIDS-app workflows

> The standardised CLI shape every modern pipeline shares — and how to chain them.

## The BIDS-app contract

Every BIDS app accepts three positional arguments in the same order:

```text
<app> <bids_dir> <output_dir> <analysis_level>
```

- **`bids_dir`** — the input BIDS dataset.
- **`output_dir`** — where to write `derivatives/<app>/`.
- **`analysis_level`** — `participant` (per-subject), `group` (cohort-level aggregation).

Plus optional flags:

```bash
--participant-label 001 002 003   # which subjects to run
--session-label baseline followup
--n_cpus 8
--mem-mb 32000
```

This contract is what makes BIDS apps composable. The same orchestration script runs any of them.

## A chained pipeline

```bash
# 1. Validate
npx bids-validator bids/

# 2. Anatomical + functional preprocessing
apptainer run fmriprep.sif \
    bids/ derivatives/ participant --participant-label 001 \
    --fs-license-file fs_license.txt

# 3. Diffusion preprocessing
apptainer run qsiprep.sif \
    bids/ derivatives/ participant --participant-label 001 \
    --output-resolution 1.7

# 4. Diffusion reconstruction
apptainer run qsirecon.sif \
    bids/ derivatives/ participant --participant-label 001 \
    --recon-spec mrtrix_multishell_msmt_ACT-hsvs

# 5. Your custom analysis on derivatives/
python analysis/run.py --bids bids/ --derivatives derivatives/
```

Each step reads BIDS-derivatives from previous steps. Each step writes its own BIDS-derivatives folder. No bespoke globbing.

## On HPC, this becomes one Slurm script per app

```bash
#!/bin/bash
#SBATCH --array=1-100%20
sub=$(sed -n "${SLURM_ARRAY_TASK_ID}p" subjects.txt)
apptainer run fmriprep.sif bids/ derivatives/ participant --participant-label $sub ...
```

…submitted once per app, with dependencies between them:

```bash
JOB1=$(sbatch jobs/fmriprep.sh | awk '{print $4}')
JOB2=$(sbatch --dependency=afterok:$JOB1 jobs/qsiprep.sh | awk '{print $4}')
```

This is the cheapest valid "pipeline orchestrator" — just Slurm dependencies. When it stops scaling, see [Data engineering → Portfolio roadmap](../data-engineering/portfolio-roadmap.md) for migrating to Snakemake.

## Group-level

After every subject finishes participant-level, run group-level to aggregate:

```bash
apptainer run fmriprep.sif bids/ derivatives/ group
```

Group-level may be a no-op (fMRIPrep is per-subject) or it may produce a cohort QC report (MRIQC, fMRIPrep).

## Where to next

[Atlases and templates](atlases.md) — the parcellations and template spaces these pipelines emit into.
