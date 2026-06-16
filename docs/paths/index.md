# Reading paths

> With 100+ pages the question "where do I start?" matters. Four named paths through the handbook based on your background.

After [Getting Started](../getting-started/index.md), pick the path that matches you.

## Path A — Brand-new researcher (e.g. first-year graduate student)

You've taken some biology and statistics; you've written *some* Python; you've never run a neuroimaging pipeline.

1. [Fundamentals → Modalities](../fundamentals/modalities.md)
2. [Fundamentals → File formats](../fundamentals/file-formats.md)
3. [Fundamentals → Coordinate systems](../fundamentals/coordinate-systems.md)
4. [Fundamentals → Foundations → Neuroscience](../fundamentals/foundations/neuroscience.md)
5. [Fundamentals → Preprocessing overview](../fundamentals/preprocessing.md)
6. [BIDS toolkit → DICOM to BIDS](../bids/dicom-to-bids.md)
7. [BIDS toolkit → Validating a dataset](../bids/validation.md)
8. [Tutorials → fMRI first/second-level GLM](../tutorials/fmri-glm.md)
9. [Analysis → Group-level statistics](../analysis/group-stats.md)
10. [Analysis → Multiple comparisons](../analysis/multiple-comparisons.md)
11. [Fundamentals → Foundations → Statistics](../fundamentals/foundations/statistics.md)
12. [Landmark → Foundational papers](../landmark/papers.md)

**Goal at the end**: you can read a neuroimaging methods section critically and design a small study yourself.

## Path B — Software / data engineer pivoting in

You're senior in Python and infra; you've never seen a brain image.

1. [Fundamentals → Foundations → Neuroscience](../fundamentals/foundations/neuroscience.md)
2. [Fundamentals → Modalities](../fundamentals/modalities.md)
3. [Fundamentals → File formats](../fundamentals/file-formats.md)
4. [Fundamentals → Foundations → Medical imaging physics](../fundamentals/foundations/physics.md)
5. [BIDS toolkit → index](../bids/index.md) (skim all chapters)
6. [Fundamentals → Medical imaging → Acquisition + Reconstruction + Registration + Segmentation](../fundamentals/medical-imaging/index.md)
7. [Data engineering → Foundations](../data-engineering/foundations.md) → [The DAG mental model](../data-engineering/dag.md) → [Portfolio roadmap](../data-engineering/portfolio-roadmap.md)
8. [Computing → Containers + HPC + Cloud](../computing/index.md)
9. [Tutorials → DWI cohort + Capstone](../tutorials/index.md)
10. [Landmark → Major pipelines + BIDS-app workflows](../landmark/pipelines.md)

**Goal**: you can ship a production cohort pipeline and have an opinion on every tool choice.

## Path C — Clinician learning the engineering

You read radiology reports daily; you've never written a Bash script or a Python data-frame.

1. [Getting Started → all four pages](../getting-started/index.md)
2. [Fundamentals → Foundations → Python](../fundamentals/foundations/python.md)
3. [Fundamentals → Foundations → CLI commands](../fundamentals/foundations/cli.md)
4. [Fundamentals → Foundations → Data analysis](../fundamentals/foundations/data-analysis.md)
5. [Fundamentals → File formats](../fundamentals/file-formats.md)
6. [BIDS toolkit → DICOM to BIDS](../bids/dicom-to-bids.md)
7. [BIDS toolkit → Common pitfalls](../bids/pitfalls.md)
8. [Fundamentals → Medical imaging → Segmentation](../fundamentals/medical-imaging/segmentation.md)
9. [AI/ML → Evaluation pitfalls](../ai/evaluation.md)
10. [Analysis → Multiple comparisons](../analysis/multiple-comparisons.md)
11. [Landmark → Datasets + Pipelines](../landmark/datasets.md)

**Goal**: you can review a neuro-AI paper, replicate its pipeline, and spot the methodological problems.

## Path D — ML engineer building neuro-AI products

You've trained vision transformers; you've never thought about subject leakage or site harmonisation.

1. [Fundamentals → Modalities + File formats + Coordinate systems](../fundamentals/modalities.md)
2. [Fundamentals → Foundations → Neuroscience](../fundamentals/foundations/neuroscience.md)
3. [Fundamentals → Foundations → Medical imaging physics](../fundamentals/foundations/physics.md)
4. [Fundamentals → Medical imaging → Segmentation + Registration + Enhancement](../fundamentals/medical-imaging/index.md)
5. [Fundamentals → Foundations → Mathematics (AI section) + Statistics](../fundamentals/foundations/mathematics.md)
6. [AI/ML → Classical ML + Deep learning + Foundation models + Evaluation](../ai/index.md)
7. [AI/ML → Training mechanics](../ai/training-mechanics.md)
8. [Tutorials → Lesion segmentation](../tutorials/lesion-segmentation.md)
9. [Data engineering → Advanced → MLOps overlap](../data-engineering/advanced/mlops.md)
10. [Landmark → Foundational papers](../landmark/papers.md)

**Goal**: you can build a medical-imaging model that survives a held-out site and an FDA-style audit.

## Re-using and remixing

These four paths cover the most common entry points. If you don't fit cleanly, mix them:

- **Postdoc switching fields** → Path A + Path D for ML side.
- **Industry SWE doing rotations in a lab** → Path B then Path A's analysis chapters.
- **MD/PhD** → Path C then Path A.

When you finish a path, do the [end-to-end capstone tutorial](../tutorials/capstone.md). It's the synthesis exercise that turns reading into competence.
