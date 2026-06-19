# Python

> The default glue language for neuroimaging analysis. NumPy and pandas in your bones; NiBabel and Nilearn in your toolbox.

This page assumes you've seen Python before. It fills in the parts that matter for research-grade neuroimaging work.

## Environment setup

```bash
python3 -m venv .venv                 # isolated environment per project
source .venv/bin/activate              # on Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install numpy scipy pandas matplotlib nibabel nilearn pybids
```

Verify:

```python
import numpy as np, scipy, pandas as pd, matplotlib, nibabel as nib
print(np.__version__, scipy.__version__, pd.__version__, nib.__version__)
```

A reproducible project pins a lockfile. With [uv](https://docs.astral.sh/uv/), `uv lock` writes `uv.lock`; with pip, `pip freeze > requirements.txt`. See [Computing → Dependency management](../../computing/dependencies.md).

## Core language — what matters

### Syntax, functions, type hints

```python
from __future__ import annotations
import numpy as np

def zscore(x: np.ndarray, axis: int = 0) -> np.ndarray:
    """Standardise along an axis. Returns NaN-safe z-scores."""
    mu = np.nanmean(x, axis=axis, keepdims=True)
    sd = np.nanstd(x, axis=axis, keepdims=True, ddof=1)
    return (x - mu) / sd
```

Type hints are documentation that `pyright` / `mypy` can verify. Use them on public functions.

### `pathlib` — paths without string bugs

```python
from pathlib import Path

bids = Path("derivatives/fmriprep/sub-001/func")
bold = next(bids.glob("*_task-rest_*_bold.nii.gz"))   # next() = first match
assert bold.exists()
```

Never write `os.path.join(...)` in 2026 code; `pathlib` is the right primitive. Documented [here](https://docs.python.org/3/library/pathlib.html).

### Lists, dicts, comprehensions

```python
subjects = ["001", "002", "003"]
runs = {s: [1, 2] for s in subjects}
flat = [(s, r) for s, rs in runs.items() for r in rs]   # nested comprehension
```

## NumPy — arrays, axes, broadcasting

NumPy ([docs](https://numpy.org/doc/stable/)) is the substrate every Python scientific library sits on. Three concepts to internalise.

### Shapes and indexing

```python
import numpy as np
img = np.random.rand(64, 64, 30, 200)    # 4D BOLD: X × Y × Z × T
print(img.shape, img.dtype, img.nbytes / 1e6, "MB")

mid_axial = img[:, :, 15, 0]              # one slice at t=0
ts_voxel  = img[32, 32, 15, :]            # 1D timeseries at a voxel
```

### Broadcasting

The single most useful NumPy concept. Shapes of `(64, 64, 30, 200)` and `(64, 64, 30, 1)` broadcast: NumPy stretches the singleton axis to match.

```python
ts_mean = img.mean(axis=-1, keepdims=True)   # (64, 64, 30, 1)
detrended = img - ts_mean                    # element-wise via broadcasting
```

### Missing data

`np.nan` is contagious; arithmetic propagates it. Use `nan*`-variants when you mean it:

```python
np.nanmean(x, axis=0)
np.nanstd(x, axis=0, ddof=1)
np.where(np.isnan(x), 0.0, x)               # explicit replace
```

## pandas — clinical-style tables

[pandas](https://pandas.pydata.org/docs/) is unavoidable when the data is tabular (participants.tsv, manifests, behavioural scores).

```python
import pandas as pd

df = pd.read_csv("participants.tsv", sep="\t")
df = df.dropna(subset=["age", "diagnosis"])              # drop incomplete rows
df["age_z"] = (df["age"] - df["age"].mean()) / df["age"].std()

groups = df.groupby("diagnosis")["age"].agg(["mean", "std", "count"])
merged = df.merge(qc, on="subject_id", how="left", validate="one_to_one")
```

The `validate="one_to_one"` argument is the cheapest schema test you can run.

## Matplotlib — figures that survive review

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(1, 2, figsize=(8, 4), dpi=150)
ax[0].imshow(mid_axial.T, cmap="gray", origin="lower")
ax[0].set_title("T1w mid-axial"); ax[0].axis("off")
ax[1].plot(ts_voxel)
ax[1].set(xlabel="TR index", ylabel="BOLD a.u.", title="Voxel timeseries")
fig.tight_layout()
fig.savefig("figs/qc_001.png", bbox_inches="tight", dpi=300)
```

Matplotlib OO API ([docs](https://matplotlib.org/stable/index.html)) is what you want for publication-quality figures. `dpi=300` for print; `bbox_inches="tight"` for tight crops.

## Script structure — argparse + `__main__`

A script anyone can run:

```python
"""qc_subject.py — emit a per-subject QC figure."""
import argparse
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("bids_root", type=Path)
    ap.add_argument("subject", help="subject label, e.g. 001")
    ap.add_argument("--out", type=Path, default=Path("figs"))
    args = ap.parse_args()

    log.info("processing sub-%s under %s", args.subject, args.bids_root)
    args.out.mkdir(parents=True, exist_ok=True)
    # ... QC logic ...
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
```

## Python packages for neuroimaging analysis

This section is the *map* — every Python package you'll plausibly touch in a neuroimaging career, framed by what it does to your data. (For *how* to install and pin these, see [Computing → Python stack](../../computing/python-stack.md).)

### Generic scientific stack — what each does for neuroimaging

These are the libraries you'll touch on every project. Learn the ones flagged "use weekly" — NumPy, pandas, SciPy, Matplotlib, scikit-learn — first; the rest you reach for when the problem arises.

| Package | Role in a neuroimaging pipeline | Where in NeuroStack |
|---|---|---|
| [NumPy](https://numpy.org) | The array backbone — every NIfTI you load becomes a NumPy array; voxel-wise stats, masks, and timeseries all live here. | This page above; [Mathematics](mathematics.md) |
| [SciPy](https://scipy.org) | Statistics (`scipy.stats`), interpolation (resampling), morphology (`scipy.ndimage` for mask cleanup), optimisation (custom model fits). | Below; [Statistics](statistics.md) |
| [pandas](https://pandas.pydata.org) | Cohort tables (`participants.tsv`), behavioural scores, QC summaries, manifests. The bridge between imaging and metadata. | Above |
| [Matplotlib](https://matplotlib.org) | Publication-grade figures. Brain slice overlays via Nilearn delegate to it. | Above; [Figures](../../getting-started/first-figure.md) |
| [Seaborn](https://seaborn.pydata.org) | Statistical plots on cohort tables — distplots, boxplots by site, regression overlays. | Below |
| [scikit-learn](https://scikit-learn.org) | Classical ML — SVMs / random forests / pipelines / cross-validation. The decoding workhorse Nilearn wraps. | [Classical ML on volumetrics](../../ai/classical-ml.md) |
| [scikit-image](https://scikit-image.org) | 2D / 3D image processing primitives — connected components for lesion volume, morphological operations on masks, edge detection. Often the right call for derivative-volume QC. | [Medical imaging → Segmentation](../medical-imaging/segmentation.md) |
| [statsmodels](https://www.statsmodels.org) | Frequentist statistics — OLS, GLM, mixed models, design-matrix introspection. The Python equivalent of R's `lme4` for mixed-effects. | [Statistics](statistics.md), [Group statistics](../../analysis/group-stats.md), [Longitudinal](../../analysis/longitudinal.md) |
| [pingouin](https://pingouin-stats.org) | Concise statistical tests with effect-size reporting; useful supplement to `scipy.stats` for clinical-style group comparisons. | [Statistics](statistics.md) |
| [PyMC](https://www.pymc.io) | Bayesian hierarchical models — partial pooling for multi-site cohorts, sub-N=10 sites borrowing strength. | [Statistics](statistics.md) |
| [bambi](https://bambinos.github.io/bambi/) | Formula-style Bayesian regression on top of PyMC; the R-`brms` analogue in Python. | [Statistics](statistics.md) |
| [PyTorch](https://pytorch.org) | The default deep-learning backbone in neuroimaging research. MONAI / nnU-Net / TorchIO all build on it. | [Deep learning](../../ai/deep-learning.md), [Training mechanics](../../ai/training-mechanics.md) |
| [TensorFlow](https://www.tensorflow.org) | The second deep-learning backbone — still common in clinical-product code, in nobrainer, and in older lab pipelines. | [Computing → Python stack](../../computing/python-stack.md) |
| [Keras](https://keras.io) | High-level deep-learning API; Keras 3 runs on TensorFlow, PyTorch, or JAX. Useful for fast prototyping with a stable API across backends. | [Deep learning](../../ai/deep-learning.md) |
| [Jupyter / IPython](https://jupyter.org) | Notebook-based exploration; the de-facto reading environment for every published analysis worth replicating. | [Tutorials](../../tutorials/index.md) |
| [PyArrow / Parquet](https://arrow.apache.org/docs/python/) | Columnar storage for cohort tables; ~10× faster than CSV for large manifests. | [Data engineering → Foundations](../../data-engineering/foundations.md) |
| [Polars](https://pola.rs/) | Modern, fast DataFrame library; usable alternative to pandas when cohorts grow into millions of rows. | [Data engineering → Performance](../../data-engineering/performance.md) |
| [DuckDB](https://duckdb.org) | In-process SQL over Parquet / DataFrames; the right tool for cohort-level summaries and ad-hoc filtering. | [Data engineering → SQL](../../data-engineering/advanced/sql.md) |

### Neuroimaging-specific packages

Grouped by where they sit in a pipeline. The bold-name entries are the ones you'll import almost every project; the rest you pull in when the modality / method demands.

**File I/O & format**

| Package | Role |
|---|---|
| [nibabel](https://nipy.org/nibabel/) | Read/write NIfTI, GIFTI, CIFTI, MGH, ANALYZE. The most-imported neuroimaging package in Python. |
| [pydicom](https://pydicom.github.io/) | Read DICOM files in pure Python. Used by every modern conversion tool. |
| [highdicom](https://highdicom.readthedocs.io/) | Write DICOM-compliant outputs (SEG, SR, PM) — essential for clinical-deployment pipelines. |
| [dcm2niix](https://github.com/rordenlab/dcm2niix) | DICOM → NIfTI converter (C++ but called from Python). The de-facto standard. |

**General analysis**

| Package | Role |
|---|---|
| [Nilearn](https://nilearn.github.io) | Masking, GLM, decoding, plotting, connectivity. Best entry point if you're coming from scikit-learn. |
| [PyBIDS](https://bids-standard.github.io/pybids/) | Query BIDS layouts programmatically; never write glob patterns. |
| [TemplateFlow](https://www.templateflow.org) | Versioned standard templates and atlases. Pin the version. |
| [neuroCombat](https://github.com/Jfortin1/neuroCombat) | ComBat in Python — remove scanner / site batch effects from cortical measures. |

**Diffusion**

| Package | Role |
|---|---|
| [DIPY](https://dipy.org) | Diffusion MRI modelling, tractography, registration. The Python analogue of MRtrix3. |
| [AMICO](https://github.com/daducci/AMICO) | Fast NODDI / SMT fitting. |

**Functional / EEG-MEG**

| Package | Role |
|---|---|
| [MNE-Python](https://mne.tools) | The canonical M/EEG analysis library; also handles EEG sensors aligned to MRI. |
| [Brainiak](https://brainiak.org) | Advanced fMRI analysis (RSA, hyperalignment, ISFC). |
| [rsatoolbox](https://rsatoolbox.readthedocs.io/) | Representational Similarity Analysis. |

**Deep learning for medical imaging**

| Package | Role |
|---|---|
| [MONAI](https://monai.io) | The PyTorch-based framework for medical-imaging DL — transforms, networks, losses, inference. |
| [TorchIO](https://torchio.readthedocs.io/) | Medical-image augmentation and patch sampling for 3D networks. |
| [nnU-Net](https://github.com/MIC-DKFZ/nnUNet) | Auto-configuring segmentation framework; the default for medical-imaging segmentation. |
| [PyTorch Geometric](https://pyg.org/) | Graph neural networks — for connectome learning. See [GNN page](../../ai/gnn.md). |
| [captum](https://captum.ai/) | Model interpretability for PyTorch (Grad-CAM, integrated gradients). See [Interpretability](../../ai/interpretability.md). |
| [nobrainer](https://github.com/neuronets/nobrainer) | TensorFlow-based DL framework for brain MRI. |

**Workflow / reproducibility**

| Package | Role |
|---|---|
| [Nipype](https://nipype.readthedocs.io/) | Pipeline framework wrapping FSL / SPM / FreeSurfer with Python interfaces. |
| [Pydra](https://github.com/nipype/pydra) | Next-generation dataflow engine; the Nipype successor. |
| [DataLad](http://datalad.org) | Git-annex-based dataset versioning. |

**Visualization**

| Package | Role |
|---|---|
| [surfplot](https://surfplot.readthedocs.io/) | Cortical surface plots from CIFTI / GIFTI. |
| [brainspace](https://brainspace.readthedocs.io/) | Gradient analysis and surface plotting. |
| [niwidgets](https://github.com/nipy/niwidgets) | Jupyter widgets for interactive neuro visualization. |
| [pyvista](https://pyvista.org/) | 3D visualization, used by some surface / mesh workflows. |

A minimal NIfTI workflow using the foundational package:

```python
import nibabel as nib
img = nib.load("sub-001_T1w.nii.gz")
data = img.get_fdata()
print(data.shape, data.dtype, img.header.get_zooms())
print(nib.aff2axcodes(img.affine))     # ('R', 'A', 'S') for canonical
```

## Statistics in Python

```python
from scipy import stats
t, p = stats.ttest_ind(group_a, group_b, equal_var=False)
r, p = stats.pearsonr(x, y)
u, p = stats.mannwhitneyu(group_a, group_b, alternative="two-sided")
```

For GLMs, [`statsmodels`](https://www.statsmodels.org/stable/index.html) is the canonical OLS / GLM / mixed-model library; [`scikit-learn`](https://scikit-learn.org/stable/) for predictive models. See [Statistics](statistics.md).

## Logging vs print

```python
log.debug("verbose detail")
log.info("normal progress")
log.warning("recoverable problem")
log.error("failure but continuing")
log.exception("failure + traceback")   # inside except: block
```

Configure logging at startup; never call `print` in pipeline code.

## Testing — pytest

```python
# tests/test_zscore.py
import numpy as np
from neuro_handbook.utils import zscore

def test_zscore_zero_mean():
    x = np.arange(10).astype(float)
    z = zscore(x)
    assert np.isclose(z.mean(), 0.0, atol=1e-12)
    assert np.isclose(z.std(ddof=1), 1.0, atol=1e-12)
```

Run with `pytest -q`. See [Data engineering → Testing](../../data-engineering/testing.md).

## Common pitfalls

- **Mutable default arguments** — `def f(x=[])` is a classic bug. Use `None` and create inside.
- **Comparison with `==`** for floats — use `np.isclose(a, b, atol=1e-9)`.
- **Modifying a DataFrame slice** — assign to a copy (`df.loc[mask, "col"] = ...`).
- **`np.array(list_of_arrays)`** when the inner shapes differ — produces an object array. Use `np.stack` or `np.concatenate`.
- **Off-by-one between voxel indices and world coordinates** — see [Coordinate systems](../coordinate-systems.md).

## Exercises

1. **Write `zscore_safe(x, axis)`** that returns z-scores along `axis`, ignoring NaNs and returning `0` when std is 0. Test with `np.array([1, 2, 3, np.nan, 5])`.
2. **Walk a BIDS dataset.** Using only `pathlib`, list every `sub-*/anat/sub-*_T1w.nii.gz` in `fixtures/sub-tiny/`. Don't use globs; use `iterdir` and pattern matching.
3. **Atomically merge two DataFrames.** Read `participants.tsv` and a synthetic `qc.csv`, join one-to-one, save as Parquet, and verify with `pyarrow.parquet.read_metadata` that the schema matches your expectation.

??? success "Solutions"
    1. `def zscore_safe(x, axis): mu=np.nanmean(x,axis,keepdims=True); sd=np.nanstd(x,axis,keepdims=True,ddof=1); return np.where(sd>0,(x-mu)/sd,0.0)`
    2. `for p in Path(root).iterdir(): if p.name.startswith('sub-'): for f in (p/'anat').iterdir(): if f.name.endswith('_T1w.nii.gz'): print(f)`
    3. Use `df.merge(qc, on='subject_id', how='left', validate='one_to_one')` then `df.to_parquet('out.parquet')`.

## References

1. **VanderPlas J.** *Python Data Science Handbook.* 2nd ed. O'Reilly; 2022. ISBN 978-1098121228. Free online: [https://jakevdp.github.io/PythonDataScienceHandbook/](https://jakevdp.github.io/PythonDataScienceHandbook/)
2. **Harris CR, Millman KJ, van der Walt SJ, et al.** Array programming with NumPy. *Nature.* 2020;585:357-362. [doi:10.1038/s41586-020-2649-2](https://doi.org/10.1038/s41586-020-2649-2)
3. **McKinney W.** *Python for Data Analysis.* 3rd ed. O'Reilly; 2022. ISBN 978-1098104030. Free online: [https://wesmckinney.com/book/](https://wesmckinney.com/book/)
4. **Virtanen P, Gommers R, Oliphant TE, et al.** SciPy 1.0: fundamental algorithms for scientific computing in Python. *Nat Methods.* 2020;17:261-272. [doi:10.1038/s41592-019-0686-2](https://doi.org/10.1038/s41592-019-0686-2)
5. **Abraham A, Pedregosa F, Eickenberg M, et al.** Machine learning for neuroimaging with scikit-learn. *Front Neuroinform.* 2014;8:14. [doi:10.3389/fninf.2014.00014](https://doi.org/10.3389/fninf.2014.00014) — Nilearn.
6. **Brett M, Markiewicz CJ, Hanke M, et al.** nipy/nibabel: documentation and software. *Zenodo.* Versioned. [https://doi.org/10.5281/zenodo.591597](https://doi.org/10.5281/zenodo.591597)
7. **Cardoso MJ, Li W, Brown R, et al.** MONAI: an open-source framework for deep learning in healthcare. *arXiv.* 2022;2211.02701. [https://arxiv.org/abs/2211.02701](https://arxiv.org/abs/2211.02701)
8. **Gramfort A, Luessi M, Larson E, et al.** MEG and EEG data analysis with MNE-Python. *Front Neurosci.* 2013;7:267. [doi:10.3389/fnins.2013.00267](https://doi.org/10.3389/fnins.2013.00267)
9. **Garyfallidis E, Brett M, Amirbekian B, et al.** Dipy, a library for the analysis of diffusion MRI data. *Front Neuroinform.* 2014;8:8. [doi:10.3389/fninf.2014.00008](https://doi.org/10.3389/fninf.2014.00008)

## Where to next

[Bash](bash.md) — the scripting language that orchestrates the Python you just wrote, followed by [CLI commands](cli.md) for the individual tools.
