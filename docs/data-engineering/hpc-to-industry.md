# From scientific HPC to industry DE — bridging the gap

## 11.1 What you already have

The mental model is identical. You've built a multi-stage idempotent pipeline orchestrated by a scheduler, with containerised tasks, configurable via env vars, with structured logs. That's the same shape as the pipelines that move billions of rows a day at large companies — only the data type and tooling differ.

## 11.2 What's different

| Scientific HPC | Industry DE |
| --- | --- |
| Single shared cluster (Slurm) | Heterogeneous compute (K8s, cloud batch, serverless) |
| Outputs on POSIX disk | Outputs in object storage + warehouse |
| Logs in `.out` files | Logs in centralised aggregator (Loki, Datadog) |
| Pipelines run when researcher hits enter | Pipelines run on schedule, on event, on demand |
| "Done when it's done" | SLOs and on-call |
| Final artifact is an analysis | Final artifact is a contract another team depends on |

## 11.3 The translation table

| HPC concept | Industry analogue |
| --- | --- |
| Slurm job | Airflow task / K8s Job |
| `sbatch` array | DAG with mapped tasks |
| Apptainer SIF | Docker image in ECR/GCR |
| `seff` / `sacct` | Datadog / Grafana |
| Lab disk quota | S3 lifecycle policy + cost report |
| `module load X` | `pip install -e .[X]` + container |
| Author-as-operator | Designated on-call rotation |

You don't need to leave HPC to learn these — most can be added inside an existing scientific repo and they're exactly what makes a portfolio piece read as "production-grade".

## Where to next

[Portfolio roadmap](portfolio-roadmap.md) — concrete, weekend-sized milestones that turn a working bash pipeline into a strong DE portfolio piece.
