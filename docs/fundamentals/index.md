# Fundamentals

> What a "neuroimaging dataset" actually is, and how it gets onto your disk.

If you've never touched neuroimaging data before, this is where to start. The section is in three layers:

## Layer 1 — What the data is

1. **[Modalities](modalities.md)** — what MRI, DWI, fMRI, PET, and EEG actually measure, and what their data looks like as files.
2. **[Coordinate systems](coordinate-systems.md)** — RAS vs LPS vs voxel space, world coordinates, and why "the same point" can have ten different addresses.
3. **[File formats](file-formats.md)** — DICOM, NIfTI, GIFTI/CIFTI, and the BIDS standard that ties them into a dataset.
4. **[Preprocessing overview](preprocessing.md)** — the steps almost every pipeline performs before analysis: denoising, motion correction, registration, normalisation.

## Layer 2 — How the scanner makes it

5. **[MRI sequences](sequences/index.md)** — the physics-and-parameters layer underneath every acquisition. MPRAGE, DWI, EPI, FLAIR, GRE, SWI, spin echo — each gets its own deep dive with peer-reviewed references.

## Layer 3 — The toolkit to think with

6. **[Computational & math foundations](foundations/index.md)** — Python, Bash & CLI, MATLAB, data analysis, statistics, mathematics, medical imaging physics, neuroscience & neurology. The programming languages, the inferential machinery, the math vocabulary, the cross-modality physics, and the brain biology you need to *think* about neuroimaging at PhD level.

## Layer 4 — The image-processing engineering layer

7. **[Medical imaging](medical-imaging/index.md)** — acquisition, reconstruction, segmentation, registration, enhancement & quality. The methodological pipeline that turns raw measurements into the volumes, surfaces, and labels every downstream analysis depends on. Each chapter is structured as *Theory → Mathematics → Steps → Practical example → References*.

By the end of this section you'll be able to look at a folder you've never seen, identify what's inside, choose tools for it, and reason quantitatively about every step that produced it.

## Where this material lives in the bigger picture

The fundamentals section answers **what is the data and how do I think about it** questions. The [BIDS toolkit](../bids/index.md) shows how to manipulate it. [Analysis](../analysis/index.md) is what you compute. [Data engineering](../data-engineering/index.md) is how to do it at scale. [AI / ML](../ai/index.md) is the modern modelling layer. Each later section assumes you've internalised the foundations.
