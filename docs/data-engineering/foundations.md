# Foundations

## 1.1 What data engineering actually is

A **data engineer** builds and operates the systems that move, transform, store, and serve data so that downstream consumers — analysts, scientists, ML systems, products — can rely on it. The output of a data engineer is not an analysis or a model; it's *infrastructure* that other people use.

Three roles, frequently confused:

- **Data analyst / scientist** — asks questions of data; produces dashboards, reports, models.
- **ML engineer** — productionises models; lives at the boundary of research and serving.
- **Data engineer** — owns the pipelines that produce the data the other two consume. If their pipeline is down, nobody else works.

If you write code that takes diffusion-weighted images from a scanner, preprocesses them, computes a connectome matrix, and lands the result on disk for someone else to analyse — congratulations, you're doing data engineering for neuroimaging. The "data" is DWI volumes, FreeSurfer surfaces, and connectome matrices; the "consumers" are eventually statistical analyses and downstream ML.

## 1.2 What "production-grade" means

A pipeline is **production-grade** when it satisfies, roughly, these six properties:

- **Correct** — outputs match the contract you advertised.
- **Idempotent** — running it twice with the same inputs gives the same outputs and no side effects.
- **Observable** — when something goes wrong you can find out *what*, *where*, *when*, and ideally *why* without re-running the pipeline.
- **Recoverable** — a failed run can be resumed from the point of failure without redoing finished work.
- **Documented** — a new teammate can run it without paging you.
- **Tested** — changes are validated automatically before they hit the cluster or cloud.

Most scientific pipelines satisfy *some* of these. A bash pipeline that already skips already-completed `recon-all` runs and emits structured logs has idempotency and partial observability. The rest of this section is mostly about closing the remaining gaps.

!!! tip "Self-check"
    Pick your current pipeline. Score it 0–5 on each of the six properties. Pillars scoring 0 or 1 are where the next milestone of work should go.

## Where to next

Next, the [DAG mental model](dag.md) — the abstraction that every workflow tool you'll meet uses under the hood.
