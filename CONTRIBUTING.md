# Contributing to NeuroStack

Thanks for being interested. **NeuroStack** grows by accretion — small additions, corrections, and worked examples are exactly what makes it useful.

## Quick start

```bash
make install        # creates .venv and installs dev + docs extras
make test           # run the test suite
make serve          # preview the docs locally
```

## What good contributions look like

- **Pages stay focused.** A page does one thing. If it grows past ~800 lines it probably wants to split.
- **Concepts are anchored in something concrete.** When you introduce a term, give an example from a real pipeline. The DWI pipeline is the running example; if you contribute a section that uses fMRI or PET, please do the same with that modality.
- **Code that appears in the docs lives in the repo.** If you show a snippet, it should be importable from `neuro_handbook` (or under `examples/`) and tested.
- **Stubs are fine.** A page with a clean scope statement and links to good external references is better than an empty file. Just keep the `!!! info "In development"` admonition until the page is done.

## Style

- Markdown is rendered with **MkDocs Material**. Use admonitions (`!!! note`, `!!! tip`, `!!! warning`) liberally.
- Headings: `H1` is the page title; sub-sections use `H2` and below.
- Code blocks use language fences (` ```python `, ` ```bash `, ` ```sql `, etc.).
- Tables for any landscape comparison; bullet lists for short enumerations.

## Tests

- Anything in `src/neuro_handbook/` needs at least one happy-path test in `tests/`.
- Use `fixtures/sub-tiny/` for BIDS-shaped fixtures. Empty placeholder files are fine.

## Filing issues

Use GitHub Issues. Helpful issue contents:

- Page link or section heading you're asking about.
- What's confusing, missing, or wrong.
- A suggestion (even a rough one) if you have it.
