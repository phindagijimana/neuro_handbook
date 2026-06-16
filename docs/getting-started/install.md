# Installing your environment

> Everything you need on disk before the rest of the handbook makes sense. Aim: a clean, reproducible Python environment + a container runtime.

## 1. Pick a Python

Python 3.10 or newer. Check what you have:

```bash
python3 --version
```

If it's older or missing, install via your package manager:

```bash
# Ubuntu / Debian
sudo apt update && sudo apt install -y python3.12 python3.12-venv python3-pip

# macOS (Homebrew)
brew install python@3.12

# Windows — install WSL2 first, then run the Ubuntu commands above
```

## 2. Clone the handbook repo

```bash
git clone https://github.com/phindagijimana/neuro_stack.git
cd neuro_handbook
```

The bundled `fixtures/sub-tiny/` dataset is used by every example on the next three pages.

## 3. Create a virtual environment

```bash
python3.12 -m venv .venv          # isolated environment per project
source .venv/bin/activate          # on Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -e ".[dev,docs,neuro]"  # installs neuro_handbook + nibabel + nilearn + tests
```

Verify:

```bash
python -c "import nibabel, nilearn, pandas; print(nibabel.__version__, nilearn.__version__)"
```

If you'd rather use modern tooling, `uv` is faster and the lockfile is more deterministic:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv && source .venv/bin/activate
uv pip install -e ".[dev,docs,neuro]"
```

## 4. Install a container runtime

You'll need either Docker (laptop / non-HPC) or Apptainer (HPC).

```bash
# Docker (Ubuntu/Debian)
sudo apt install -y docker.io
sudo usermod -aG docker $USER && newgrp docker
docker --version

# Apptainer (HPC, or where Docker is forbidden)
# Most clusters have it pre-installed:
apptainer --version
# If not: https://apptainer.org/docs/admin/main/installation.html
```

Sanity check:

```bash
docker run --rm hello-world          # or
apptainer run docker://hello-world
```

## 5. (Optional) FreeSurfer license

Many BIDS apps (fMRIPrep, sMRIPrep, QSIPrep when reconstructing surfaces) embed FreeSurfer. The license is free but you must request it.

1. Request it at <https://surfer.nmr.mgh.harvard.edu/registration.html>.
2. Save the e-mailed `license.txt` somewhere stable — e.g. `~/freesurfer/license.txt`.
3. Set an environment variable so scripts find it:

```bash
echo 'export FS_LICENSE=$HOME/freesurfer/license.txt' >> ~/.bashrc
source ~/.bashrc
```

You can skip this for now — MRIQC (the first BIDS app you'll run on page 3 here) doesn't need it.

## 6. (Recommended) Editor + remote SSH

[VS Code](https://code.visualstudio.com) with the **Remote — SSH** and **Python** extensions is the dominant setup. From your laptop you can edit code that lives on the cluster and run it on the cluster. Configure once in `~/.ssh/config`; see [Computing → Editor and IDE setup](../computing/editor.md).

## 7. Verify your install

Run the bundled test suite — everything should pass:

```bash
pytest -q
```

If that succeeds, you're ready.

## Where to next

[Your first NIfTI](first-nifti.md) — load a brain volume and print its shape.
