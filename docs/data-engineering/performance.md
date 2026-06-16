# Performance and scale

## 8.1 Parallelism — three flavours

- **Data parallelism** — same operation over different shards (your across-subject parallelism).
- **Pipeline parallelism** — different stages on different workers (QSIPrep on node A while Recon on node B for the next subject).
- **Task parallelism** — independent tasks share a worker (multi-threading inside QSIPrep).

Knowing which you're using clarifies bottlenecks. Adding more workers helps data-parallel work but does nothing for sequential-bound work.

## 8.2 Profiling and resource estimation

A senior DE knows, roughly, for each stage:

- CPU time per unit of work.
- Peak RSS (memory).
- Disk I/O pattern.
- External calls per unit.

You get this with `seff <jobid>` on Slurm, with `time -v`, with cgroups accounting, or with explicit Python timing. Write down a sentence per stage. Then size the cluster request honestly — overprovisioning costs money *and* slows queueing, underprovisioning causes OOM kills.

## 8.3 Caching and memoization

If a sub-result is expensive and rarely changes, **cache it**. Patterns:

- **Filesystem cache** keyed by input hash.
- **Memcached / Redis** for sub-second values.
- **HTTP caching with ETags** for external APIs (TemplateFlow, BIDS validators).

Caching is power-and-responsibility: a wrong cache key is the worst bug class in DE because it silently returns stale data. **Always include the content version in cache keys.**

## 8.4 Backfills

When you change a stage, you usually need to re-process all historical data. This is a **backfill**. Industry-grade orchestrators have first-class support (`airflow backfill`, `dagster backfill`, Snakemake `--forceall`). Plan backfills like deploys: dry-run, partial run, full run, with checkpoints.

## Where to next

[Testing pipelines](testing.md) — the discipline that lets you change anything without fear.
