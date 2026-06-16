# The industry tooling landscape

You don't need to learn all of these. You do need to **recognise** them so job posts make sense and you can pick the right tool for the next project.

## 6.1 Workflow orchestrators

| Tool | Strength | When |
| --- | --- | --- |
| **Snakemake** | File-target rules; native HPC | Best fit for scientific pipelines on Slurm. |
| **Nextflow** | Channel-based; bioinformatics adoption | If your group already uses it. |
| **Airflow** | Time-based scheduling; huge ecosystem | Tabular / warehouse pipelines. |
| **Dagster** | Asset-based; strong typing | Modern data platforms. |
| **Prefect** | Pythonic, lightweight | Lightweight alternative to Airflow. |
| **Argo Workflows** | Kubernetes-native | All-in on K8s. |
| **Luigi / Make / Bazel** | DAG engines in different costumes | Niche but conceptually similar. |

## 6.2 Compute substrates

- **HPC schedulers** — Slurm, PBS, SGE, LSF. Cluster sharing, queues, fair scheduling.
- **Kubernetes** — the cloud-native answer. Pods, deployments, jobs.
- **Cloud batch** — AWS Batch, GCP Batch. Managed schedulers on top of cloud compute.
- **Serverless** — Lambda, Cloud Run. Sub-minute jobs, no infrastructure.

## 6.3 Storage layers

- **POSIX filesystems** — Lustre, GPFS on HPC; NFS in labs.
- **Object stores** — S3, GCS, Azure Blob. Cheap, durable, slow per-request.
- **Warehouses** — Snowflake, BigQuery, Redshift, Databricks SQL. Columnar, SQL-native.
- **Lakehouses** — Iceberg / Delta / Hudi tables on top of object storage. See [Lakehouse internals](advanced/lakehouse.md).
- **Time-series** — InfluxDB, TimescaleDB, Prometheus.
- **OLTP** — Postgres, MySQL. The transactional workhorses.

## 6.4 Transformation tools

- **SQL on a warehouse** — the workhorse.
- **dbt** — SQL with Jinja templating, versioning, tests, lineage. Modern ELT default. See [dbt deeply](advanced/dbt.md).
- **Spark / PySpark** — distributed transformations on huge datasets. See [Spark](advanced/spark.md).
- **Pandas / Polars / DuckDB** — single-node Python analytics.

## 6.5 Streaming

- **Apache Kafka** — distributed log; the de-facto event bus.
- **AWS Kinesis / Google Pub-Sub** — managed alternatives.
- **Apache Flink / Spark Structured Streaming / Apache Beam** — stream processors on top.

See [Streaming systems](advanced/streaming.md) for the deeper treatment.

## 6.6 Observability

- **Logs** — ELK (Elasticsearch + Logstash + Kibana), Splunk, Loki, Datadog Logs.
- **Metrics** — Prometheus + Grafana, Datadog, CloudWatch.
- **Traces** — OpenTelemetry, Jaeger, Tempo.
- **Data-specific** — OpenLineage, Marquez, Monte Carlo, Bigeye.

## 6.7 Data quality

- **Great Expectations** — Python framework for declarative data tests ("expect rows >= 1000", "expect age between 0 and 120").
- **dbt tests** — built-in SQL-based assertions in dbt projects.
- **Soda** — YAML-based data quality DSL.
- **Pandera** — Pydantic for pandas / Polars DataFrames.

## Where to next

[Reliability & operations](reliability.md) — the day-2 work that keeps the pipeline alive once it's running.
