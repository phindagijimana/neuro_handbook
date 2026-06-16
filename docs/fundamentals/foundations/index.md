# Computational & math foundations

> Everything you need to *think* about neuroimaging before you can do it well.

The rest of the Fundamentals section explains what a neuroimaging dataset is. This sub-section explains the toolkit you need to manipulate it: a programming language, a shell, a statistics vocabulary, the math underneath, and a working grasp of the physics that produced the signal in the first place.

Each page is written for a PhD-level newcomer — someone who knows *some* programming or statistics and needs the gaps filled with the right depth for research work, not introductory snippets.

## Pages

<div class="grid cards" markdown>

-   :fontawesome-brands-python: **[Python](python.md)**

    ---

    The default glue language: NumPy, pandas, Matplotlib, `pathlib`, argparse, logging, and the neuroimaging stack (NIfTI, BIDS, fMRIPrep derivatives).

-   :material-console-line: **[Bash & CLI](bash-cli.md)**

    ---

    Shell, pipes, `awk` / `sed`, `find`, `rsync`, `grep`, strict-mode scripts, Slurm patterns, container invocation.

-   :material-language-matlab: **[MATLAB](matlab.md)**

    ---

    Arrays, scripts vs functions, tables, statistics, SPM / EEGLAB / FieldTrip ecosystem, and when to leave MATLAB for Python.

-   :material-chart-bell-curve-cumulative: **[Statistics](statistics.md)**

    ---

    Probability, GLM, mixed models, multiple comparisons, permutation, effect sizes, power analysis, Bayesian thinking.

-   :material-function-variant: **[Mathematics](mathematics.md)**

    ---

    Linear algebra, calculus, optimisation, signal processing, Fourier transforms, geometry of the brain.

-   :material-atom: **[Physics](physics.md)**

    ---

    MRI physics from Bloch equations to k-space; relaxation, gradients, RF, SNR; what the scanner is really measuring.

</div>

## How to read this section

Pick the page that matches the gap you feel. Each is self-contained. If you're brand new, the natural sequence is **Mathematics → Physics → Statistics → Python → Bash & CLI → MATLAB** — every later page assumes the earlier ones. But for an experienced engineer arriving from outside neuroimaging, **Physics → MATLAB ↔ Python** is usually the right shortcut.

Each page ends with a references block of canonical textbooks (with ISBN) and primary papers (with DOI). Treat the references as the next mile after the chapter.
