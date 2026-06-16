# Your first figure

> Render a publication-style brain figure from the data you just produced. ~10 lines, ~5 minutes.

By the end of this page you'll have closed the loop from a downloaded NIfTI to a saved PNG that could go in a paper — the complete mini-pipeline.

## 1. Two paths — quick brain figure or QC summary

### Path A — a quick brain figure with Nilearn

```python
from nilearn import plotting, datasets

# Use the MNI152 template that ships with Nilearn so we don't depend on any download
mni = datasets.load_mni152_template()

fig = plotting.plot_anat(
    mni,
    display_mode="ortho",            # three orthogonal cuts
    cut_coords=(0, 0, 0),             # at the origin (MNI centre)
    title="MNI152 — orthogonal view",
    annotate=True,
)
fig.savefig("figs/mni152_ortho.png", dpi=300, bbox_inches="tight")
fig.close()
```

That's a publication-quality figure. Now substitute in your own subject:

```python
plotting.plot_anat(
    "data/derivatives/mriqc/sub-01/anat/sub-01_T1w.nii.gz",
    title="sub-01 T1w",
    output_file="figs/sub01_T1w.png",
)
```

### Path B — a cohort QC summary

If you ran MRIQC on more than one subject, the group `*.tsv` files in `data/derivatives/mriqc/` are a real cohort table:

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(context="paper", style="whitegrid", font_scale=1.1)

df = pd.read_csv("data/derivatives/mriqc/group_T1w.tsv", sep="\t")
print(df.shape, df.columns.tolist())

fig, ax = plt.subplots(figsize=(6, 4), dpi=150)
sns.histplot(df["cnr"], kde=True, ax=ax, color="#4c72b0")
ax.set(title="Cohort CNR distribution", xlabel="Contrast-to-noise ratio")
fig.tight_layout()
fig.savefig("figs/cohort_cnr.png", dpi=300, bbox_inches="tight")
```

If you only ran on one subject, the same recipe still works as a "lab QC dashboard" template that grows with your cohort.

## 2. Overlay a parcellation

For a more impressive figure, overlay an atlas:

```python
from nilearn import datasets, plotting

mni = datasets.load_mni152_template()
atlas = datasets.fetch_atlas_destrieux_2009()

plotting.plot_roi(
    atlas["maps"],
    bg_img=mni,
    title="Destrieux atlas on MNI152",
    output_file="figs/atlas_overlay.png",
    cmap="tab20",
)
```

That's a standard "atlas-on-template" figure that appears in countless methods sections.

## 3. The two-rule recipe for paper-quality figures

- Save vector (`.pdf`, `.svg`) or high-DPI raster (`>=300`).
- `bbox_inches="tight"` to avoid wasted whitespace.

```python
fig.savefig("figs/final.pdf")
fig.savefig("figs/final.png", dpi=300, bbox_inches="tight")
```

## 4. Commit the script — never just the figure

A figure without its script is unverifiable. Commit `make_fig2.py` next to the saved `figs/fig2.pdf` so a reviewer (and you in two years) can regenerate it.

## What you've achieved end-to-end

- Installed a Python environment + a container runtime.
- Loaded and inspected a NIfTI.
- Ran a containerised BIDS app on a real dataset.
- Rendered a publication-style figure from the result.

That's the complete shape of every neuroimaging analysis. Everything else in this handbook is a deeper version of one of these four steps.

## Where to next

- **Pick a path** in [Reading paths](../paths/index.md) based on your background.
- **Or go broad**: open the [Fundamentals](../fundamentals/index.md) section and read top-to-bottom.
- **Or go deep on one thing**: jump to [BIDS toolkit](../bids/index.md) (data plumbing), [Analysis](../analysis/index.md) (methods), or [Data engineering](../data-engineering/index.md) (scaling).
