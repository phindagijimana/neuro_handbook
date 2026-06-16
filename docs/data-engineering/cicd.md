# CI/CD for data pipelines

CI/CD does not mean "auto-deploy production data jobs on every commit". For data, it means:

- **Lint** — `shellcheck` on `*.sh`, `ruff` on `*.py`, `snakemake -n` (dry-run) on every PR.
- **Unit tests** — `pytest` on PR.
- **Integration tests** — run the pipeline on the tiny fixture subject on PR (a few minutes).
- **Schema diff** — if the pipeline outputs a known schema, diff against the previous release.
- **Container build & scan** — build the SIF / Docker image, scan for vulnerabilities (Trivy, Grype).
- **Promotion gates** — merging to `main` builds production images; deploying to prod still requires a manual click for high-blast-radius pipelines.

GitHub Actions or GitLab CI handles this for free. A `Makefile` with `make lint test integration` targets keeps the same commands runnable locally.

## A minimal pipeline-of-pipelines

```yaml
# .github/workflows/ci.yml (abbreviated)
on: [pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps: [..., ruff check ., shellcheck *.sh]
  test:
    runs-on: ubuntu-latest
    steps: [..., pytest]
  integration:
    runs-on: ubuntu-latest
    steps: [..., snakemake --use-conda -j 1 -- all  # fixtures/sub-tiny]
```

This repo ships a similar workflow under `.github/workflows/ci.yml`.

## Where to next

[HPC → industry](hpc-to-industry.md) — translating scientific habits into industry DE ones.
