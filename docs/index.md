# neuro-handbook

> An open reference for working with neuroimaging data — fundamentals, data engineering, and AI/ML.

This handbook is written for **people getting started** in neuroimaging research, neuroscience research, and the engineering that supports them: graduate students, postdocs, research software engineers, data engineers from outside the medical-imaging world, and developers building neuro-AI products.

It tries to be the document we wish we had when we first walked into the field.

---

## What's covered

<div class="grid cards" markdown>

-   :material-school: **[Fundamentals](fundamentals/index.md)**

    ---

    What a "neuroimaging dataset" actually is. Acquisition basics for MRI, DWI, fMRI, PET, and EEG. Coordinate systems (RAS / LPS / MNI), file formats (DICOM, NIfTI, GIFTI/CIFTI), and the BIDS standard.

-   :material-pipe: **[Data engineering](data-engineering/index.md)**

    ---

    DAGs, pipelines, idempotency, observability, testing, and scale — taught against a real diffusion-MRI pipeline (QSIPrep → Recon → QSIRecon → connectome). Goes from "first script" all the way to lakehouses, streaming, and FinOps.

-   :material-brain: **[AI / ML](ai/index.md)**

    ---

    Classical ML on volumetric features, CNNs and U-Nets for segmentation, transformer and diffusion models, foundation models for medical imaging, and the evaluation pitfalls that bite neuroimaging projects specifically.

-   :material-tools: **[Tools landscape](tools/index.md)**

    ---

    Opinionated map of the workflow orchestrators, storage layers, transformation engines, and observability stacks you'll bump into. Pointers, not exhaustive lists.

</div>

---

## How to read it

- **Linear**: read top-to-bottom once to build a mental map. Each chapter assumes you've read the previous one in its section but not across sections.
- **As reference**: jump to a topic. Every page is self-contained enough to be useful on its own, and links liberally to neighbours.
- **As exercises**: most chapters end with "try this" tasks against a tiny sample dataset shipped under `fixtures/sub-tiny/`. Pair them with the code in `examples/`.

If you're brand new to neuroimaging, start with [Fundamentals → Modalities](fundamentals/modalities.md). If you're a data engineer or software engineer coming in from outside, start with [Fundamentals → File formats](fundamentals/file-formats.md) and then go straight to [Data engineering → Foundations](data-engineering/foundations.md).

## Companion code

This site is generated from a repository that also ships a small Python package, `neuro_handbook`, plus runnable examples:

```bash
pip install -e ".[docs,dev,neuro]"
python examples/01_walk_bids.py fixtures/sub-tiny
mkdocs serve  # preview this site locally
```

The code is intentionally small and readable. If a page on this site refers to a snippet, the snippet exists in the repo and is tested in CI.

## Contributing

This is a community reference. The DWI-focused parts reflect one team's experience; broader coverage is welcome. See the [repo](https://github.com/phindagijimana/neuro_handbook) for how to file issues and open PRs.

## License

Content and code are released under the [MIT license](https://github.com/phindagijimana/neuro_handbook/blob/main/LICENSE).
