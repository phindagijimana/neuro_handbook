# The five pillars of any pipeline

These are the structural properties that distinguish "a working script" from "a piece of infrastructure". Score every pipeline you meet against these.

## 3.1 Orchestration

Something has to decide *what* runs, *where*, in *what order*, with *what resources*, *after what*. That something is the **orchestrator**. Options range from the trivial (a cron + a bash script) to the heavyweight (Airflow with Celery workers on a Kubernetes cluster). The right answer depends on the workload, not on fashion.

For a neuroimaging pipeline on a Slurm cluster, `submit.sh` + `array.sh` + `subject.sh` *is* the orchestrator: it translates "process these subjects" into Slurm array tasks. Snakemake / Nextflow replace those shell scripts with a declarative DAG that the orchestrator interprets.

## 3.2 Idempotency

**Idempotent** = running the operation twice has the same effect as running it once. In data pipelines, this means: if a step has already produced its output, re-running the pipeline does not recompute it, does not duplicate the output, and does not corrupt state.

A hand-written idempotency guard looks like this:

```bash
if [[ -f "${aparc}" ]]; then
  echo "Recon: ${aparc} already exists — skipping"
  return 0
fi
```

Industry tools handle this declaratively — Snakemake says "this rule produces `aparc+aseg.mgz`; if it exists and is newer than its inputs, skip" — and you never write the guard.

Idempotency is what makes pipelines safe to re-run. Without it, every retry risks duplicating data or corrupting state. See [Concepts in depth](concepts.md#52-idempotency-deeper) for the deeper treatment.

## 3.3 Isolation (containerisation)

Each task should run in an environment that is reproducible and independent of the others. **Containers** provide this: a frozen filesystem + binaries + libraries that runs identically everywhere. Apptainer (formerly Singularity) on HPC, Docker / Podman elsewhere.

Isolation buys you:

- **Reproducibility** — `qsiprep:0.23.1` produces the same output today and in five years.
- **Dependency-hell avoidance** — QSIPrep needs Python 3.10, your other tools need 3.11; both live happily side by side in different containers.
- **Portability** — the same image runs on Slurm, on EC2, on your laptop.

Always pin container tags. Never `:latest`.

## 3.4 Observability

You cannot fix what you cannot see. A pipeline is **observable** when, for any failure or oddity, you can quickly answer:

- **What** happened? (the error message, the stack trace)
- **Where**? (which task, which subject, which input)
- **When**? (timestamp, what else was running)
- **Why**? (the contributing cause)

The three observability primitives are:

- **Logs** — what each task printed; usually a file or a stream in a log aggregator.
- **Metrics** — numbers over time (CPU, memory, queue depth, success rate, latency).
- **Traces** — the path of a single request / task across distributed components.

Most scientific pipelines have logs but no metrics or traces. That's the most common gap; the [Reliability & operations](reliability.md) chapter shows how to close it cheaply.

## 3.5 Configuration

A pipeline that hard-codes paths and parameters is not a pipeline; it's a script. Real pipelines accept configuration through:

- **Environment variables** — fine for a few knobs (`RESULTS_ROOT`, `RECON_TOOL`).
- **Config files** — YAML / TOML / JSON loaded at startup.
- **Schemas with validation** — Pydantic, JSON Schema, Avro, Protobuf. Reject bad config *before* the cluster spends 10 hours computing on it.

Configuration discipline is what lets the same code base run dev, staging, and production with different inputs.

!!! tip "Exercise"
    Introduce a Pydantic config object that mirrors today's env vars. Replace `${RESULTS_ROOT:-…}` with `cfg.results_root`. Run with both a valid and an invalid config; observe how much earlier the bad-config error surfaces.

## Where to next

The [DWI case study](dwi-case-study.md) — concrete mapping of a real pipeline onto these pillars and onto industry concepts like the medallion architecture.
