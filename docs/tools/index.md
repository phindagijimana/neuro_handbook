# Tools landscape

> Opinionated map of the tools you'll meet — what they do and when to reach for each.

This page is a quick index, organised by what the tool *does* rather than where it sits in the stack. Each row links to a deeper treatment elsewhere in the handbook when one exists.

## Neuroimaging-specific

| Tool | What it does | Notes |
| --- | --- | --- |
| **dcm2niix** | DICOM → NIfTI conversion | The de-facto standard; embeds BIDS-friendly sidecars. |
| **HeuDiConv / Dcm2Bids** | Build a BIDS dataset from DICOM | Heuristic-driven; pick HeuDiConv for institutional repeatability, Dcm2Bids for one-off conversions. |
| **BIDS Validator** | Check a dataset against the BIDS spec | Run before *any* pipeline. |
| **FreeSurfer** (`recon-all`) | Cortical surface reconstruction, parcellations | Slow (≈10 h / subject); FastSurfer is the DL-accelerated drop-in. |
| **fMRIPrep / QSIPrep / sMRIPrep** | BIDS-app preprocessing | Standardised, container-shipped; outputs are reusable across downstream analyses. |
| **MRtrix3** | Diffusion modeling, tractography | Workhorse for DWI streamlines and FOD-based methods. |
| **ANTs / FSL / AFNI** | Registration, segmentation, fMRI stats | Mature, well-cited, slower-moving. |
| **Nilearn** | Python analytics on NIfTI / Niimg | Best Python entry point if you're coming from scikit-learn. |
| **PyBIDS** | Programmatic BIDS access | Use it instead of writing glob patterns. |
| **TemplateFlow** | Versioned standard templates | Pin versions in your pipeline. |

## Workflow orchestrators

| Tool | Strength | When to pick |
| --- | --- | --- |
| **Snakemake** | File-target rules; native HPC integration | Best fit for neuroimaging on Slurm. |
| **Nextflow** | Containerised, channel-based; massive bioinformatics adoption | When your team already uses it. |
| **Airflow** | Time-based scheduling; huge ecosystem | Tabular / warehouse-centric pipelines. |
| **Dagster** | Asset-based mental model; strong typing | Modern data platforms, software-defined assets. |
| **Prefect** | Pythonic; flexible deployment | Lighter weight than Airflow. |
| **Argo Workflows** | Kubernetes-native | When the rest of the stack is on K8s. |

## Storage layers

| Tool | What | Notes |
| --- | --- | --- |
| **POSIX filesystem** | Plain files | What HPC clusters give you. Fast within a node, painful across. |
| **S3 / GCS / Azure Blob** | Object storage | Cloud default; cheap at rest, network-egress costs bite. |
| **Parquet** | Columnar file format | The lingua franca of analytical data. |
| **Iceberg / Delta / Hudi** | Table formats on top of Parquet | ACID transactions, time-travel, schema evolution. See [Lakehouse internals](../data-engineering/advanced/lakehouse.md). |
| **DataLad** | Git-annex for datasets | The neuroimaging-native versioning answer. |
| **DICOM PACS** | Clinical image archives | Where data starts; rarely where it lives during research. |

## Analytics & transformation

| Tool | When |
| --- | --- |
| **DuckDB** | In-process SQL on Parquet / CSV. Excellent for cohort summaries. |
| **Polars** | Fast single-node DataFrames. |
| **Pandas** | Familiar, ubiquitous, slower at scale. |
| **Spark / PySpark** | When the data doesn't fit on one machine. See [Spark](../data-engineering/advanced/spark.md). |
| **dbt** | SQL transformations with version control, tests, lineage. See [dbt](../data-engineering/advanced/dbt.md). |

## Observability

| Layer | Tool |
| --- | --- |
| Logs | Loki, ELK, Datadog Logs |
| Metrics | Prometheus + Grafana, Datadog |
| Traces | OpenTelemetry, Jaeger, Tempo |
| Lineage | OpenLineage + Marquez, DataHub, Atlan |
| Data quality | Great Expectations, Pandera, Soda |

---

This is a starting map, not an exhaustive catalogue. Tools change; the *categories* don't.
