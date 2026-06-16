# Data engineering

> Building and operating the systems that move, transform, store, and serve neuroimaging data.

This section is a port of an internal "practical course" written against a real diffusion-MRI (DWI) pipeline. The pipeline runs:

```
BIDS sub-XXX ──► QSIPrep ─┬─► QSIRecon (HSVS) ─┐
                          │                    ├─► DK connectome ──► dk_connectome.csv
                          └─► Recon (recon-all)┘
```

Every concept below is grounded in something that pipeline does, or should do.

## How to read it

The chapters build on each other. Read them top-to-bottom once to build a mental map; keep them next to your repo as a reference. Estimated reading time: ~60 minutes for the foundations chapters, plus several focused sessions for the advanced topics.

### Foundations

- **[Foundations](foundations.md)** — what data engineering is, what "production-grade" means, and how that maps onto a neuroimaging pipeline.
- **[The DAG mental model](dag.md)** — directed acyclic graphs as the universal abstraction behind every workflow tool.
- **[The five pillars](five-pillars.md)** — orchestration, idempotency, isolation, observability, configuration.
- **[DWI case study](dwi-case-study.md)** — mapping a real pipeline onto industry concepts (medallion architecture, etc.).
- **[Concepts in depth](concepts.md)** — ETL/ELT, determinism, schemas, lineage, partitioning, retries, cost.

### Industry context

- **[Tooling landscape](tooling.md)** — orchestrators, compute substrates, storage, transformation, streaming, observability.
- **[Reliability & operations](reliability.md)** — SLOs, runbooks, on-call, retries done right.
- **[Performance & scale](performance.md)** — parallelism flavours, profiling, caching, backfills.

### Engineering practice

- **[Testing pipelines](testing.md)** — the testing pyramid, DE-specific test types, fixture subjects.
- **[CI/CD](cicd.md)** — what CI actually means for data pipelines.
- **[HPC → industry](hpc-to-industry.md)** — translating scientific HPC habits into industry data-engineering ones.
- **[Portfolio roadmap](portfolio-roadmap.md)** — a six-milestone path from "working script" to "senior portfolio piece".
- **[Exercises](exercises.md)** — small, concrete tasks against your own repo.

### Advanced

The [Advanced topics](advanced/index.md) sub-section covers data modeling, lakehouse internals, SQL, distributed systems, Spark, streaming (Kafka / Flink), dbt, data contracts, security, IaC, FinOps, real-time analytics, MLOps overlap, disaster recovery, incident management, networking, and org-level data engineering — for when the basics aren't enough.

## Audience

Written for people who already write code (probably Python and shell) and now need to operate pipelines, not just author them. No prior data-engineering background assumed. Some prior neuroimaging exposure helps but isn't required — the [Fundamentals](../fundamentals/index.md) section covers what you need.
