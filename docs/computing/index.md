# Computing environment

> What you actually need on your machine — or your cluster account — to do neuroimaging work.

Neuroimaging code is computationally heavy and dependency-fragile. A "works on my laptop" pipeline that doesn't reproduce on the cluster is a research-integrity problem, not just a logistics one. This section is about getting the environment right from day one.

## Chapters

- **[Python scientific stack](python-stack.md)** — `numpy`, `scipy`, `nibabel`, `nilearn`, `pybids`, `dipy`, `mne`, the choice between `conda` / `mamba` / `uv` / `pip`.
- **[Containers (Docker, Apptainer)](containers.md)** — why every modern pipeline ships as a container, and how to use them on HPC where Docker is forbidden.
- **[HPC and Slurm](hpc-slurm.md)** — the standard scheduler, array jobs, GPU partitions, queue etiquette.
- **[Cloud (AWS / GCP / Azure)](cloud.md)** — when to leave HPC, common patterns, the egress-cost trap.
- **[GPUs and accelerators](gpus.md)** — CUDA / cuDNN / driver dance, multi-GPU training, picking an instance type.
- **[Editor and IDE setup](editor.md)** — VS Code Remote, Jupyter, the small productivity wins that compound.
- **[Dependency management](dependencies.md)** — lockfiles, virtual envs, pinning, the "what's the actual version of FSL on this node" problem.
- **[Reproducibility checklist](reproducibility.md)** — a 12-line pre-publication audit that catches most "I can't rerun this" issues.

## Read this section before...

...you start coding on a new machine. Half of it is one-time setup; the other half is operational discipline that pays off over years.
