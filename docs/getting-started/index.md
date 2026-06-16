# Getting started

> The 30-minute on-ramp. Start here if you've never touched neuroimaging or shell tooling before.

The rest of the handbook assumes you have a working environment, can read a NIfTI file, and have run at least one BIDS app once. This mini-section gets you there.

## Four pages, in order

1. **[Installing your environment](install.md)** — Python 3.12, Apptainer / Docker, FSL or FreeSurfer license, VS Code remote.
2. **[Your first NIfTI](first-nifti.md)** — load, inspect, plot a brain volume in ~15 lines of Python.
3. **[Your first BIDS app](first-bids-app.md)** — run MRIQC on the bundled `sub-tiny` fixture.
4. **[Your first figure](first-figure.md)** — render a publication-style brain figure with Nilearn.

By the end of these four pages you'll have done a complete mini-pipeline from raw data to a saved PNG. After that, [Reading paths](../paths/index.md) helps you choose where to go next.

## Prerequisites

- A Linux or macOS workstation (or WSL2 on Windows).
- Roughly 10 GB of free disk.
- A modern Python (3.10+).
- ~30 minutes.

You do **not** need an HPC account or a clinical scanner yet. The fixture dataset shipped with this repo is enough to follow every example.
