# Fundamentals

> What a "neuroimaging dataset" actually is, and how it gets onto your disk.

If you've never touched neuroimaging data before, this is where to start. Four short chapters:

1. **[Modalities](modalities.md)** — what MRI, DWI, fMRI, PET, and EEG actually measure, and what their data looks like as files.
2. **[Coordinate systems](coordinate-systems.md)** — RAS vs LPS vs voxel space, world coordinates, and why "the same point" can have ten different addresses.
3. **[File formats](file-formats.md)** — DICOM, NIfTI, GIFTI/CIFTI, and the BIDS standard that ties them into a dataset.
4. **[Preprocessing overview](preprocessing.md)** — the steps almost every pipeline performs before analysis: denoising, motion correction, registration, normalisation.

By the end of this section you'll be able to look at a folder you've never seen, identify what's inside, and know which tools and which BIDS apps to point at it.

## Where this material lives in the bigger picture

The fundamentals section answers **what is the data** questions. The [Data engineering](../data-engineering/index.md) section answers **how do we process it at scale**, and the [AI / ML](../ai/index.md) section answers **what can we learn from it**. Each section assumes you've internalised the previous one but tries to remain useful as a standalone reference.
