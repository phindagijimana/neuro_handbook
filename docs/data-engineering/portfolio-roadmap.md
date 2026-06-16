# A portfolio progression roadmap

Concrete, ordered steps that turn a working bash + Slurm pipeline into a strong data-engineering portfolio piece. Each item is sized at *"a weekend"*.

## Milestone 0 — Current state

Bash + Slurm + Apptainer + 4 stages, no tests, manual runbook.

## Milestone 1 — Snakemake port (1 weekend)

- Replace `submit.sh` / `array.sh` / `subject.sh` glue with a `Snakefile`.
- One rule per stage; declare `input:`, `output:`, `container:`, `threads:`, `resources:`.
- `snakemake --executor slurm --jobs 50` runs the same workload.
- `snakemake -n` is your dry-run / dependency diff.
- `snakemake --report report.html` is your provenance artifact.
- Keep the bash scripts in `legacy/` so reviewers can compare.

## Milestone 2 — Tests and CI (1 weekend)

- Pick one cropped subject as fixture (`tests/fixtures/sub-tiny/`).
- Add `pytest` with a single integration test that runs the pipeline locally on the fixture (no Slurm) and asserts the DK CSV exists with shape 84×84.
- Add `tests/test_config.py` with unit tests for any Python helpers (Pydantic config validator if you introduce one).
- Add `.github/workflows/ci.yml`: shellcheck + ruff + `snakemake -n` + `pytest`.
- Add a `Makefile` with `make lint test integration`.

## Milestone 3 — Observability (1 weekend)

- Emit a per-subject `manifest.json` (subject ID, container hashes, git SHA, timings, success/failure).
- Aggregate manifests into a single `cohort_report.parquet`.
- A tiny Grafana dashboard or a static HTML report ("69/76 subjects complete, p95 runtime 8.2 h, failures by stage"). Even a hand-written HTML works.

## Milestone 4 — SQL / warehouse layer (1 weekend)

- DuckDB locally (zero ops) or a small Postgres on-cluster.
- Load every subject's QC metrics, manifest, and a flattened connectome (`subject_id, source_node, target_node, weight`) into three tables.
- Wrap a tiny dbt project around them with two models (`cohort_qc_summary`, `connectome_long_to_wide`) and a few dbt tests.
- This is the **missing tabular surface area** that converts a "scientific pipeline" into "DE portfolio".

## Milestone 5 — Cloud port (stretch, 2 weekends)

- Run the same Snakemake workflow on AWS Batch with S3 as the storage layer.
- Push the Apptainer images to a container registry (or convert to Docker).
- The pipeline now demonstrates HPC-and-cloud literacy in one repo.

## Milestone 6 — Airflow / Dagster comparison (stretch)

- Wrap the existing pipeline as a single Airflow or Dagster DAG (each stage = one operator / op).
- Write a short `docs/why-snakemake-vs-airflow.md` documenting the trade-offs you observed. This is exactly the kind of artifact senior engineers and tech leads write — and is gold in interviews.

---

By Milestone 4 you have a strong portfolio piece. Milestones 5–6 turn it into a senior-level one.

## Where to next

[Exercises](exercises.md) — bite-sized tasks to practise the ideas in this chapter without committing to a full milestone.
