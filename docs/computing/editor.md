# Editor and IDE setup

> The small productivity choices that compound across years.

There's no one-true-editor. There are good and bad versions of any setup. This page lists the wins that show up in any decent setup.

## VS Code + Remote-SSH

The dominant editor in modern neuroimaging dev:

- **Remote-SSH extension** — edit code that lives on the cluster, run it on the cluster, no file syncing.
- **Python extension** — type-checks, refactors, debugger.
- **Jupyter extension** — notebooks in the editor.
- **Ruff extension** — linting + formatting on save.
- **GitHub Copilot** or **Claude** — fine on boilerplate; never let it write your statistics.

Configure on first install:

```jsonc
// .vscode/settings.json
{
  "python.analysis.typeCheckingMode": "basic",
  "[python]": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.codeActionsOnSave": {"source.organizeImports": "always"}
  },
  "files.exclude": {"**/__pycache__": true, "**/.venv": true}
}
```

## JupyterLab on the cluster

For exploratory work, JupyterLab beats remote-editing a `.py` file. Two patterns:

- **`srun --pty` + Jupyter** — interactive Slurm allocation, then `jupyter lab --no-browser --port 8888`. Tunnel back with `ssh -L 8888:node-XXX:8888`.
- **JupyterHub** — many clusters now run a hub; click "Launch" and you get a Jupyter session on a compute node.

Use Jupyter for one-off analysis; promote anything that runs more than once into a script in version control.

## Notebook → script discipline

A notebook that's been edited 50 times in random order is a research-integrity risk. Two habits:

1. **Restart and run-all** before declaring a notebook "the analysis". If it doesn't work top-to-bottom, the result isn't reproducible.
2. **Promote stable cells into a `.py` module** that the notebook imports. Notebooks become thin presentation layers; logic lives in tested Python.

## Terminal multiplexers — boring win

`tmux` or `screen` on the cluster keeps your session alive when your SSH dies. Learn three commands:

- `tmux new -s mywork` — start a named session.
- `tmux a -t mywork` — re-attach after SSH drops.
- `Ctrl-b d` — detach without killing.

Twenty minutes of muscle memory, hundreds of hours saved.

## Where to next

[Dependency management](dependencies.md) — the "what's the actual version of FSL on this node" problem.
