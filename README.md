# NeuroStack

> *The open neuroimaging handbook.*

**NeuroStack** is an open reference for working with neuroimaging data — fundamentals, BIDS, analysis, data engineering, AI / ML, computing — written for people who are getting started in neuroimaging research, neuroscience research, and the development that supports them.

The site lives at **https://phindagijimana.github.io/neuro_handbook/** (the GitHub repo slug stays `neuro_handbook` so existing URLs and the `neuro_handbook` Python package keep working).

This repo is **both** a documentation site and a small Python package of reusable utilities. The site is hosted on GitHub Pages; the package ships the code that appears in the worked examples.

## What's inside

- `docs/` — the handbook content, rendered with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/).
  - **Fundamentals** — how MRI / DWI / fMRI / PET / EEG data is acquired, stored, and organised (DICOM, NIfTI, BIDS).
  - **Data engineering** — DAGs, pipelines, idempotency, observability, testing, scale. Anchored in a real diffusion MRI pipeline.
  - **AI / ML** — classical ML on volumetrics, CNNs / U-Nets, foundation models, evaluation pitfalls specific to neuroimaging.
  - **Tools** — opinionated landscape of the workflow, storage, and analytics tools you'll meet in this space.
- `src/neuro_handbook/` — the companion Python package: BIDS walking, DICOM conversion helpers, QC metrics, manifest emission, tiny DAG primitives.
- `examples/` — short scripts that exercise the package on a tiny fixture dataset.
- `tests/` — pytest suite for the package.

## Quick start

```bash
# clone and install
git clone https://github.com/<you>/neuro-handbook.git
cd neuro-handbook
pip install -e ".[docs,dev]"

# preview the site locally
mkdocs serve

# run the examples
python examples/01_walk_bids.py fixtures/sub-tiny
```

## Reading the handbook online

Visit the rendered site at **`https://<you>.github.io/neuro-handbook/`** once GitHub Pages is enabled (see `.github/workflows/docs.yml`).

## Status

Early. Content is being ported and expanded chapter-by-chapter. The data-engineering section is the most complete; fundamentals and AI/ML sections are stubs that will grow over time. Contributions and corrections are welcome — open an issue or a PR.

## License

[MIT](LICENSE).
