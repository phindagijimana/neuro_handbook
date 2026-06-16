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

## Neuroimaging-specific stack

| Library | Use |
|---|---|
| [`nibabel`](https://nipy.org/nibabel/) | Read/write NIfTI, GIFTI, CIFTI, MGH |
| [`nilearn`](https://nilearn.github.io) | Masking, GLM, decoding, plotting |
| [`pybids`](https://bids-standard.github.io/pybids/) | Query BIDS layouts |
| [`dipy`](https://dipy.org) | Diffusion MRI modelling |
| [`mne`](https://mne.tools) | MEG / EEG |
| [`templateflow`](https://www.templateflow.org) | Versioned standard templates |
| [`MONAI`](https://monai.io) | Medical-imaging deep learning |

A minimal NIfTI workflow:

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

## References

1. **VanderPlas J.** *Python Data Science Handbook.* 2nd ed. O'Reilly; 2022. ISBN 978-1098121228. Free online: [https://jakevdp.github.io/PythonDataScienceHandbook/](https://jakevdp.github.io/PythonDataScienceHandbook/)
2. **Harris CR, Millman KJ, van der Walt SJ, et al.** Array programming with NumPy. *Nature.* 2020;585:357-362. [doi:10.1038/s41586-020-2649-2](https://doi.org/10.1038/s41586-020-2649-2)
3. **McKinney W.** *Python for Data Analysis.* 3rd ed. O'Reilly; 2022. ISBN 978-1098104030. Free online: [https://wesmckinney.com/book/](https://wesmckinney.com/book/)
4. **Virtanen P, Gommers R, Oliphant TE, et al.** SciPy 1.0: fundamental algorithms for scientific computing in Python. *Nat Methods.* 2020;17:261-272. [doi:10.1038/s41592-019-0686-2](https://doi.org/10.1038/s41592-019-0686-2)
5. **Abraham A, Pedregosa F, Eickenberg M, et al.** Machine learning for neuroimaging with scikit-learn. *Front Neuroinform.* 2014;8:14. [doi:10.3389/fninf.2014.00014](https://doi.org/10.3389/fninf.2014.00014) — Nilearn.
6. **Brett M, Markiewicz CJ, Hanke M, et al.** nipy/nibabel: documentation and software. *Zenodo.* Versioned. [https://doi.org/10.5281/zenodo.591597](https://doi.org/10.5281/zenodo.591597)

## Where to next

[Bash & CLI](bash-cli.md) — the shell that orchestrates the Python you just wrote.
