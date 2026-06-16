# The DAG mental model

A **DAG — Directed Acyclic Graph** — is the fundamental abstraction of every modern workflow tool. Internalising it is the single highest-leverage move you can make.

## 2.1 Definitions

- **Graph** — a set of nodes connected by edges.
- **Directed** — each edge has an arrow (`A → B` is *not* the same as `B → A`).
- **Acyclic** — no path that starts at a node returns to it. Cycles would mean a task depends on itself, directly or transitively.

## 2.2 The DWI pipeline as a DAG

```text
                                  ┌─► QSIRecon (HSVS) ──┐
BIDS sub-001 ──► QSIPrep ─────────┤                     ├──► DK connectome ──► dk_connectome.csv
                                  └─► Recon (recon-all)─┘
```

Each box is a task; each arrow declares "this task needs the previous task's output". The graph tells a scheduler four things for free:

- **Order** — DK cannot start until both Recon and QSIRecon finish.
- **Parallelism** — QSIPrep and Recon are independent of each other and can run concurrently. Likewise, `sub-001` and `sub-007` are entirely independent — they're separate DAG instances.
- **What's safe to skip** — if `dk_connectome.csv` exists and is newer than its inputs, do nothing.
- **Blast radius** — deleting `aparc+aseg.mgz` invalidates only Recon and DK; QSIPrep is unaffected.

## 2.3 Why DAGs win

Before DAG-thinking, people wrote sequential bash scripts ("step 1 then step 2 then step 3"). Sequential scripts conflate *what depends on what* with *when to run it*. DAGs separate these concerns: you declare the dependencies, the scheduler figures out the schedule.

Once a scheduler owns the schedule it can:

- Re-run only failed branches.
- Parallelise independent branches.
- Visualise the workflow.
- Optimise placement (run heavy nodes on big machines, light nodes on cheap ones).

Every workflow framework you'll encounter — Snakemake, Nextflow, Airflow, Dagster, Prefect, Argo, Kubeflow, Luigi, Make, Bazel — is a DAG engine under the hood. **Master the abstraction once and the tools become syntax differences.**

!!! tip "Exercise"
    Draw the DAG of your own pipeline by hand, including any subtle dependencies (e.g., a `.lta` registration file consumed by a later step). Save it as `docs/dag.png` — every future explanation will start from this drawing.

## Where to next

The [five pillars](five-pillars.md) — the structural properties that distinguish a working script from production infrastructure.
