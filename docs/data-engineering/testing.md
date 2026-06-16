# Testing pipelines

## 9.1 The pyramid

```text
                 ╱╲
                ╱  ╲   E2E (1 tiny subject end-to-end)
               ╱────╲
              ╱      ╲  Integration (rule by rule, mocked containers)
             ╱────────╲
            ╱          ╲ Unit (helpers, config, parsers)
           ╱────────────╲
```

Many fast unit tests at the bottom, a few slow end-to-end tests at the top.

## 9.2 Test types specific to DE

- **Schema tests** — row count > 0, no nulls in primary key, foreign keys resolve, value ranges sane.
- **Volume tests** — today's row count is within ±20% of yesterday's.
- **Freshness tests** — most recent partition's `max(updated_at)` is within N hours.
- **Distribution tests** — mean / stddev of numeric column hasn't drifted.

For neuroimaging analogues:

- **Schema** — every subject has 1 DK matrix; matrix shape is 84×84.
- **Volume** — total streamlines per subject in `[N₁, N₂]`.
- **Distribution** — cohort-mean FA hasn't drifted between releases.
- **Provenance** — every output `.csv` has a sibling `_log.json` recording the container hash.

## 9.3 Test data

Curate one or two **fixture subjects** with very small dimensions (cropped DWI, small T1w) that can run the full pipeline in under 5 minutes on a single node. This is the basis for your integration test and the most valuable test asset you own.

The repo includes a `fixtures/sub-tiny/` placeholder; populate it with a stripped-down dataset and your tests will become both fast and meaningful.

## Where to next

[CI/CD](cicd.md) — running these tests on every change.
