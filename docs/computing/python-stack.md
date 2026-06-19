# Python scientific stack

> The packages every neuroimaging Python project ends up importing — and the package manager that won't fight you.

## The unavoidable core

- **`numpy`** — every n-dimensional array.
- **`scipy`** — interpolation, optimisation, statistics, sparse linear algebra.
- **`pandas`** / **`polars`** — tabular data.
- **`matplotlib`** + **`seaborn`** — plots.
- **`scikit-learn`** — classical ML.

## Neuroimaging specifics

- **[`nibabel`](https://nipy.org/nibabel/)** — read/write every imaging format you'll meet (NIfTI, GIFTI, CIFTI, MGH, etc.).
- **[`nilearn`](https://nilearn.github.io)** — high-level fMRI analysis, statistical maps, plotting, masking.
- **[`pybids`](https://bids-standard.github.io/pybids/)** — query a BIDS dataset.
- **[`dipy`](https://dipy.org)** — diffusion MRI methods (registration, reconstruction, tractography).
- **[`mne`](https://mne.tools)** — MEG/EEG analysis (also surface-based; useful even for non-MEG work).
- **[`templateflow`](https://www.templateflow.org)** — versioned standard templates (MNI, fsaverage, fsLR).
- **[`pydicom`](https://pydicom.github.io/pydicom/stable/)** — read DICOM if you must.

## Deep learning specifics

- **`torch`** + **`torchvision`** — the default training framework.
- **[`MONAI`](https://monai.io)** — medical-imaging-aware extension. Use it unless you have a specific reason.
- **`accelerate`** + **`bitsandbytes`** — multi-GPU and quantisation.

## Package managers

| Tool | When |
| --- | --- |
| **`pip`** + `venv` | Pure-Python projects, simple environments |
| **`conda`** / **`mamba`** | When you need non-Python binaries (FSL, FreeSurfer Python wrappers, NumPy with MKL) |
| **`uv`** | New, fast, pip-compatible. Default for greenfield projects in 2026. |
| **`pixi`** | Conda-flavoured but reproducible by default; growing adoption in scientific Python |

For a brand-new project, the sane defaults are:

1. **`uv`** if you only need Python packages.
2. **`pixi`** or **`mamba`** if you need binaries (e.g., FSL via the `bioconda` channel).
3. Always commit a lockfile (`uv.lock`, `pixi.lock`, `conda-lock`).

## A minimal `pyproject.toml` for a neuroimaging project

```toml
[project]
name = "my_neuro_project"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "numpy>=1.26",
    "scipy>=1.13",
    "pandas>=2.2",
    "nibabel>=5.2",
    "nilearn>=0.10.4",
    "pybids>=0.16",
    "matplotlib>=3.8",
]

[project.optional-dependencies]
dev = ["pytest>=8.0", "ruff>=0.5"]
dl = ["torch>=2.4", "monai>=1.4"]
```

Pin major versions. Update intentionally, on a schedule, with the test suite as the safety net.

## Reproducibility beyond lockfiles

A committed `uv.lock` or `poetry.lock` or `pip-compile` output (see [pip-tools](https://github.com/jazzband/pip-tools), [Poetry](https://python-poetry.org/)) pins your Python dependency graph. It does *not* pin the system libraries those wheels link against (libpng, BLAS/LAPACK, glibc), the OS, or the GPU model. All of these can change neuroimaging outputs at the numerical level [Glatard et al., 2015](https://doi.org/10.3389/fninf.2015.00012)[^glatard]. Real reproducibility is a stack, not a file.

The layers, in order of how often they bite:

- **Digest-pin your container.** `FROM python:3.11` re-pulls a different image each week as Debian moves underneath. `FROM python:3.11@sha256:abc123...` does not. Use the digest, not the tag.
- **`PYTHONHASHSEED`.** Python randomises `hash()` for dict ordering since 3.3. If any of your code (or a transitive dep) depends on dict iteration order in pre-3.7 semantics, your output silently changes between runs. Set `PYTHONHASHSEED=0` in CI and Dockerfiles.
- **CUDA / cuDNN nondeterminism.** Many GPU kernels (atomics, reductions, some convolutions) are non-deterministic by default. Pin both:

    ```python
    import os, torch
    os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":4096:8"
    torch.use_deterministic_algorithms(True)
    torch.backends.cudnn.benchmark = False
    ```

    Expect ~30% throughput loss. The full recipe is in the [PyTorch reproducibility notes](https://pytorch.org/docs/stable/notes/randomness.html).

- **BLAS choice.** Intel MKL and OpenBLAS produce bit-different floating-point output for the same NumPy code. Pick one in your container (`conda install nomkl` or `MKL_NUM_THREADS=1` matters) and don't let pip silently swap it.
- **Seed everything that has an RNG.** `random.seed`, `np.random.seed`, `torch.manual_seed`, `torch.cuda.manual_seed_all`, plus `PYTHONHASHSEED` as above. Forgetting any one of them is enough to make a fold non-reproducible.

The honest recipe:

```text
lockfile  +  digest-pinned container  +  fixed PYTHONHASHSEED
         +  deterministic CUDA flags  +  pinned BLAS
         +  all RNGs seeded (random, numpy, torch, torch.cuda)
```

Anything less is reproducible-on-my-machine.

## References

[^glatard]: Glatard T, Lewis LB, Ferreira da Silva R, et al. Reproducibility of neuroimaging analyses across operating systems. *Front Neuroinform.* 2015;9:12. [doi:10.3389/fninf.2015.00012](https://doi.org/10.3389/fninf.2015.00012)

## Where to next

[Containers](containers.md) — for everything that isn't pure Python.
