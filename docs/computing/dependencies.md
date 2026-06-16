# Dependency management

> Lockfiles, virtual envs, and the discipline that lets you reproduce a run from 2024 today.

## The two problems

1. **Forward reproducibility** — can someone else, today, install what you used and get the same answer?
2. **Backward reproducibility** — can *you*, two years later, re-create the environment you used for that paper?

Both are dependency-management problems.

## Python — pick one virtual env per project

```bash
uv venv .venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

Never install into your system Python or a shared conda base. The "I changed something for project A and project B broke" cycle is avoidable.

## Lockfiles, always

A `pyproject.toml` declares *what you want*. A lockfile records *what you got*. The lockfile is what survives across machines.

- `uv` → `uv.lock`.
- `pixi` → `pixi.lock`.
- `conda` → `conda-lock.yml` (via the `conda-lock` tool).
- `poetry` → `poetry.lock`.

Commit the lockfile. Update it on a schedule, not on every install.

## Non-Python dependencies

Tools like FSL, FreeSurfer, AFNI, ANTs, MRtrix3 are not pip-installable. Options:

- **Container** — single source of truth; the [Containers](containers.md) page covers this.
- **`bioconda` / `nipreps`** — many neuroimaging tools are now on Conda; pinnable to a version.
- **Module system** — HPC clusters often expose `module load fsl/6.0.7`. Pin the version in your job script; don't trust the default.

When in doubt, container. Module systems vary by cluster; containers don't.

## Recording the environment in your output

Every pipeline run should emit:

- The lockfile that produced it (or a hash of it).
- The container digest (for any containers used).
- The git SHA of the analysis code.
- The hostname (so a "this only fails on the new node" is identifiable).

The `Manifest` schema in this repo (`neuro_handbook.qc.Manifest`) has fields for exactly this.

## When you inherit a project

The first three things to check:

1. Is there a lockfile in the repo? If yes, install from it directly (`uv pip sync uv.lock` or `pixi install`).
2. Is there a container? If yes, pull it and skip the env dance.
3. If neither, recreate the env from `pyproject.toml` / `environment.yml` and *write* a lockfile as you do. Pay the cost once; everyone after you benefits.

## Where to next

[Reproducibility checklist](reproducibility.md) — the audit that catches what discipline misses.
