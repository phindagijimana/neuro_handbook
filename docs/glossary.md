# Glossary

A working glossary that mixes data-engineering and neuroimaging vocabulary, because the audience for this handbook lives at that intersection.

## A

**Atomic write** — A write that either completes fully or appears not to have happened. Implemented by writing to a temporary path and renaming. Essential for [idempotency](data-engineering/concepts.md#52-idempotency-deeper).

## B

**Backfill** — Re-processing historical partitions with a new pipeline version. See [Performance & scale](data-engineering/performance.md).

**Backpressure** — Mechanism by which a slow consumer signals an upstream producer to slow down.

**BIDS (Brain Imaging Data Structure)** — A community standard that prescribes folder layout, naming, and JSON sidecars for neuroimaging datasets. See [File formats](fundamentals/file-formats.md).

## D

**DAG (Directed Acyclic Graph)** — The fundamental abstraction of every modern workflow tool. See [The DAG mental model](data-engineering/dag.md).

**DICOM (Digital Imaging and Communications in Medicine)** — The clinical-imaging file and network format. Image arrives as DICOM, gets converted to NIfTI for research.

**DWI (Diffusion-Weighted Imaging)** — An MRI sequence sensitive to water diffusion, used to model white-matter microstructure and to reconstruct fibre pathways via tractography.

## F

**fMRI (functional MRI)** — Time-series MRI that measures the BOLD (blood-oxygen-level-dependent) signal as a proxy for neural activity.

## I

**Idempotency** — Running the operation twice has the same effect as running it once. The cornerstone of safe retries. See [The five pillars](data-engineering/five-pillars.md).

## L

**Lineage** — The directed graph of "table X was produced by job Y consuming tables A, B, C". See [Catalogs & lineage](data-engineering/advanced/catalogs.md).

## M

**Medallion architecture** — Bronze (raw) → Silver (cleaned) → Gold (analysis-ready) layering. See [DWI case study](data-engineering/dwi-case-study.md).

## N

**NIfTI** — The research-imaging file format (`.nii` / `.nii.gz`). Voxel array + affine matrix + minimal header. See [File formats](fundamentals/file-formats.md).

## R

**RAS / LPS** — Two common conventions for naming coordinate axes (Right-Anterior-Superior vs Left-Posterior-Superior). NIfTI uses RAS; DICOM uses LPS. See [Coordinate systems](fundamentals/coordinate-systems.md).

**Runbook** — A short markdown file per common alert/failure: symptoms, causes, diagnostic commands, remediation, escalation. See [Reliability & operations](data-engineering/reliability.md).

## S

**SLI / SLO / SLA** — Service Level Indicator (what you measure) / Objective (your target) / Agreement (contractual). See [Reliability & operations](data-engineering/reliability.md).

## T

**Tractography** — The estimation of white-matter pathways from DWI data, typically as streamlines through a fibre-orientation field.

---

*This glossary will grow as the handbook does. Open a PR to add or improve a term.*
