# Cloud (AWS, GCP, Azure)

> When to leave HPC for the cloud, and how to do it without lighting money on fire.

## When to use cloud

- **Your institution doesn't have an HPC** with the resources you need.
- **You need elastic capacity** — a one-off backfill of 5000 subjects in a week.
- **You're collaborating across institutions** — cloud is the lowest-friction common ground.
- **Your data already lives there** (UK Biobank, S3-hosted OpenNeuro).

## When to stay on HPC

- Most academic work; HPC compute-hours are already paid for.
- Long-running interactive analysis (cloud instances cost while idle).
- Data > 10 TB that would cost a fortune to transfer in and out.

## The three substrates

### Batch compute

- **AWS Batch** — managed Slurm-like queue on top of EC2 / Fargate.
- **GCP Batch** — similar, simpler interface.
- **Azure Batch** — similar.

Map your `sbatch` script to a Batch job definition. Same mental model.

### Kubernetes

- **EKS / GKE / AKS** — managed Kubernetes. Argo Workflows, Nextflow's K8s executor, Snakemake's K8s integration.
- More moving parts; pays off when the rest of your stack is K8s anyway.

### Serverless

- **AWS Lambda / GCP Cloud Run** — sub-minute jobs only; useful for lightweight ingestion or reporting steps.

## The egress trap

Cloud providers charge ~$0.09/GB to move data *out*. Transferring 10 TB to your laptop = $900. Common mitigations:

- **Compute in the cloud, don't download.** Keep raw data, derivatives, and analyses all in the same region.
- **Use a cloud-attached workstation** when you do need interactive work (an EC2 instance running JupyterLab).
- **Egress credits** — some providers credit egress for academic / non-profit users; ask.

## Storage tiers

- **S3 Standard / GCS Standard** — read-anytime, costs ~$0.023/GB-month.
- **S3 Intelligent-Tiering** — automatic tiering; usually the best default.
- **S3 Glacier / Coldline** — archive; cheap to store, slow to read. For raw scanner output you might never touch.

Set lifecycle policies on day one. Otherwise the bill grows monotonically.

## Cost monitoring

- **AWS Cost Explorer** / **GCP Cost Report** — daily breakdown by service.
- **Budgets and alerts** — set a monthly limit and email yourself when you cross 80%.
- **Tagging** — tag every resource with project / user. The bill becomes auditable.

## Where to next

[GPUs and accelerators](gpus.md) — the hottest, most expensive cloud resource.
