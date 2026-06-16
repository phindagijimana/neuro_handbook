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

## Where to next

[Performance & scale](performance.md) — when "it works" needs to become "it works *fast*".
