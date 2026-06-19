# Reliability and operations

A pipeline that runs once is a demo. A pipeline that runs every day for two years is infrastructure. The difference is operational discipline.

## 7.1 SLAs, SLOs, SLIs

- **SLI (Service Level Indicator)** — what you *measure*. Examples: "p95 pipeline runtime", "% subjects with valid DK matrix".
- **SLO (Service Level Objective)** — your *internal target*. Example: "99% of subjects finish in <12 h".
- **SLA (Service Level Agreement)** — a *contractual target* with consequences. Mostly external.

A DE team owns SLOs on its pipelines. Below SLO triggers an investigation; trending toward the boundary triggers prevention.

## 7.2 The failure modes you actually see

| Class | Examples | Mitigation |
| --- | --- | --- |
| **Input** | Bad DICOM, missing field maps, malformed BIDS | Validation gate at ingest |
| **Resource** | OOM, walltime exceeded, disk full | Right-size + monitoring |
| **Dependency** | Container missing, TemplateFlow down | Pin + cache + retry |
| **Transient infra** | Slurm hiccup, node crash | Retries with backoff |
| **Logic bugs** | Wrong b-vector flip, off-by-one ROI | Tests + manual QC |

Each one becomes a runbook the first time it happens.

## 7.3 Runbooks

A **runbook** is a short markdown file per common alert or failure: "If alert X fires, the cause is usually Y; check Z; remediate with command W; escalate to person P." Cheap, high-leverage, and a great signal of operational maturity in a team.

A new teammate should be able to resolve a Sev-3 alert from a runbook without paging anyone.

## 7.4 On-call

Production pipelines that other teams depend on need on-call coverage. The DE rotation typically handles:

- Failed pipeline runs (page within minutes if SLO-critical).
- Data quality alerts (page slower).
- Capacity issues (proactive).

In a typical neuroimaging lab, *you are the entire on-call rotation* for your pipeline. That's fine — but it's why discipline matters: every fix should leave the system more resilient than you found it.

## 7.5 Retries — the right way

The naive `for i in 1..3; do something || continue; done` is rarely the right answer. Real retry policy:

- **Only retry transient errors** (network, 5xx). Never retry on validation errors.
- **Exponential backoff with jitter** to avoid thundering herds.
- **Idempotency is a precondition** — never retry a non-idempotent operation without deduplication.
- **Bounded** — give up eventually and surface the error.

Workflow engines do most of this for you (`retries=3, retry_delay=...`).

## 7.6 SLO and runbook templates for neuroimaging pipelines

Concept is easy; templates are scarce. Copy these into your repo on day one and edit, don't write from scratch under pressure.

### A practical SLO menu for a DWI cohort pipeline

| Class | SLI (what you measure) | SLO (target) | Where the number lives |
| --- | --- | --- | --- |
| **Freshness** | Time from DICOM landing in `incoming/` to `dk_connectome.csv` published | 95% of subjects within 72 h | `runs` table, `dicom_arrival_ts` and `published_ts` columns |
| **Completeness** | Per-subject derivative count vs the expected manifest (FA, MD, AD, RD, tensor, DK matrix) | 99% of expected derivatives produced | Manifest checker job, nightly |
| **Correctness** | % subjects flagged by automated QC (eddy outlier %, SNR floor, motion threshold) | <2% flagged; trend, not single-point | QSIPrep + eddy QC JSON, aggregated |
| **Cost** | $ per subject (cloud) or CPU-hours per subject (HPC) | <$8 per subject *or* <12 CPU-h per subject | Slurm `sacct` or cloud billing export, joined on `subject_id` |

A subject that misses any one of these is not a failure of the SLO — the SLO is a *cohort-level* target. Single-subject misses go in the QC queue; sustained drift triggers an incident.

For the conceptual ground floor, the [Google SRE book](https://sre.google/sre-book/service-level-objectives/) chapter on SLO/SLI/SLA is the canonical free reference, and the [SRE Workbook](https://sre.google/workbook/implementing-slos/) chapter on implementing SLOs is the practical follow-on. The runbook-template tradition itself is documented in the [Site Reliability Workbook chapter on on-call](https://sre.google/workbook/on-call/).

### Runbook template — fMRIPrep job exceeded 24 h on >30% of subjects

```markdown
## Symptom
A nightly run of fMRIPrep on the current cohort shows >30% of
subjects exceeding the 24 h walltime budget. The `runs` table
shows status = TIMEOUT for the affected jobs.

## What to check first
- **Peak RSS > 16 GB?** `sacct -j <jobid> --format=MaxRSS,ReqMem`
  — if yes, the memory ceiling was hit and the process thrashed.
  Bump `--mem` and resubmit.
- **Slurm partition correct?** `squeue -j <jobid> -o "%P"` — a
  partition swap (preemption, maintenance) may have parked you
  on a slower queue.
- **Topup or eddy stage hung?** Tail the log: are timestamps
  flat for >2 h on a single stage? Eddy GPU stage hanging is
  the classic CUDA-driver-mismatch symptom.
- **Cluster filesystem under load?** `lfs check servers` (Lustre)
  or `df -h /scratch`; latency >100 ms on `/scratch` will tank
  any I/O-heavy stage.

## Escalation
- Sev-3 (cohort delayed but no SLO miss yet) — assignee + Slack.
- Sev-2 (freshness SLO at risk this week) — page DE on-call.
- Sev-1 (cluster-wide; multiple pipelines) — page HPC ops.

## Resolution patterns
- Memory ceiling: raise `--mem` in the submit script, document
  the new floor in the pipeline README.
- Slow queue: resubmit to the intended partition; file a ticket
  with HPC ops if preemption is repeating.
- Eddy hang: pin CUDA driver / container digest; fall back to
  CPU eddy on the affected node.
- Filesystem: move scratch to a node-local SSD for the
  preprocessing stage; revisit when ops confirms /scratch is healthy.

## Postmortem template
- Timeline (UTC).
- Subjects affected and re-run status.
- Root cause (technical + organisational).
- What we changed (config, monitoring, alert).
- What's still latent.
```

### Runbook template — QC failure rate spiked from 5% to 30% overnight

```markdown
## Symptom
The nightly QC report shows the flagged-subject rate jumped from
~5% (rolling 30-day baseline) to 30% in a single batch.

## What to check first
- **Did anyone update the QC threshold?** `git log -p qc/thresholds.yaml`
  — a threshold change is the single most common cause of
  apparent overnight drift.
- **Did the scanner get serviced?** Check the site maintenance
  log; a coil swap or gradient calibration shifts SNR and motion
  distributions immediately.
- **Site-harmonisation drift?** Group the flagged subjects by
  site / scanner / coil; if 90% come from one site, it's not the
  pipeline, it's the acquisition.
- **Pipeline version change?** `git log --since="48 hours ago"`
  on the pipeline repo; an unannounced QSIPrep bump can change
  the eddy outlier statistic.
- **Input format change?** New DICOM vendor field, new b-table
  layout — `dcm2niix` warnings surface this.

## Escalation
- If site / scanner cause confirmed: notify the site PI and pause
  ingestion from that scanner until acquisition is validated.
- If pipeline cause confirmed: roll back the container digest;
  open a bug against the offending version.

## Resolution patterns
- Threshold change: revert or socialise; never change QC
  thresholds without a baseline-shift PR.
- Scanner drift: add a per-scanner QC baseline; flag against
  scanner-specific norms, not cohort-wide norms.
- Pipeline drift: pin container digest in `pipeline.lock`;
  add a smoke-test cohort of 3 known-good subjects that must
  pass before promoting a new version.

## Postmortem template
(same as above)
```

### A minimal monitoring stack

You do not need Datadog to run a defensible cohort pipeline. The minimum useful stack is three things:

| Layer | Tool | What it answers |
| --- | --- | --- |
| **Raw logs** | Slurm `sacct` + per-job stderr in object storage | "What did this one job do?" |
| **Runs table** | Postgres / SQLite, one row per `(subject, pipeline_version, run_id)` | "What's the cohort state right now?" |
| **Dashboard** | [Streamlit](https://streamlit.io/) or [Grafana](https://grafana.com/) reading the runs table | "Are we hitting freshness / completeness this week?" |

Wire the SLOs from the table above directly onto the dashboard — freshness as a time-to-publish histogram, completeness as a stacked bar by subject status, correctness as a QC-pass-rate trend line, cost as $/subject over time. The [DWI case study observability section](dwi-case-study.md#46-observability-what-you-wire-up-on-day-one) walks through the same wiring with concrete schema.

The rule: if a number appears in your SLO, it must appear on the dashboard, and the dashboard URL must be in every runbook.

## References

1. **Beyer B, Jones C, Petoff J, Murphy NR (eds.).** *Site Reliability Engineering: How Google Runs Production Systems.* O'Reilly, 2016. Free online: [https://sre.google/sre-book/table-of-contents/](https://sre.google/sre-book/table-of-contents/) — see especially the chapter on [Service Level Objectives](https://sre.google/sre-book/service-level-objectives/).
2. **Beyer B, Murphy NR, Rensin DK, Kawahara K, Thorne S (eds.).** *The Site Reliability Workbook: Practical Ways to Implement SRE.* O'Reilly, 2018. Free online: [https://sre.google/workbook/table-of-contents/](https://sre.google/workbook/table-of-contents/) — see [Implementing SLOs](https://sre.google/workbook/implementing-slos/) and [On-Call](https://sre.google/workbook/on-call/) for the runbook tradition.

## Where to next

[Performance & scale](performance.md) — when "it works" needs to become "it works *fast*".
