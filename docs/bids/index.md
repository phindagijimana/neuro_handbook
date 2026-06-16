# BIDS toolkit

> Practical recipes for organising, validating, querying, and versioning BIDS datasets.

The [Fundamentals → File formats](../fundamentals/file-formats.md) page explains what BIDS *is*. This section is about what you actually *do* with it day-to-day:

- **[Validating a dataset](validation.md)** — running the BIDS validator (CLI, web, Python) and reading its output without panic.
- **[DICOM to BIDS](dicom-to-bids.md)** — HeuDiConv, Dcm2Bids, and the heuristics file that does 80% of the work.
- **[Querying with PyBIDS](pybids.md)** — `BIDSLayout`, filters, and writing pipeline code that doesn't break on the next dataset.
- **[Derivatives layout](derivatives.md)** — how to lay out your own outputs so the next BIDS app can read them.
- **[Versioning with DataLad](datalad.md)** — git + git-annex for datasets that don't fit in git.
- **[Common pitfalls](pitfalls.md)** — the things that break in production: special characters in IDs, IntendedFor mistakes, sidecar inheritance bugs.

## How to use this section

If you're starting a new project, read [DICOM to BIDS](dicom-to-bids.md), then [Validation](validation.md), then [PyBIDS](pybids.md). If you're picking up an existing dataset, start with [Validation](validation.md) and [Common pitfalls](pitfalls.md). If your dataset is going to outlive a single project, read [DataLad](datalad.md) early.

All examples in this section can run against `fixtures/sub-tiny/` in the repo.
