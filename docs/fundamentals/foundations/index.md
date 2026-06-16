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

-   :material-table-search: **[Data analysis](data-analysis.md)**

    ---

    Cohort tables, EDA, missing data, ComBat harmonisation, confound regression, paper-ready figure recipes, reproducibility audit.

-   :material-chart-bell-curve-cumulative: **[Statistics](statistics.md)**

    ---

    Probability, GLM, mixed models, multiple comparisons, permutation, effect sizes, power analysis, Bayesian thinking.

-   :material-function-variant: **[Mathematics](mathematics.md)**

    ---

    Linear algebra, calculus, optimisation, signal processing, Fourier transforms, geometry of the brain, and the math underneath neuroimaging AI (backprop, attention, diffusion models, graph nets).

-   :material-atom: **[Medical imaging physics](physics.md)**

    ---

    MRI Bloch / k-space deep dive, plus CT, PET kinetic modelling, ultrasound, NIRS / OCT, EEG/MEG biophysics, MRS — every modality you'll meet.

-   :material-brain: **[Neuroscience & neurology](neuroscience.md)**

    ---

    Macroscale anatomy, cells and circuits, large-scale functional networks, the clinical conditions neuroimaging studies (stroke, AD, PD, MS, epilepsy, TBI, tumours, psychiatric, paediatric), atlases.

</div>

## How to read this section

Pick the page that matches the gap you feel. Each is self-contained. If you're brand new, the natural sequence is **Neuroscience → Medical imaging physics → Mathematics → Statistics → Data analysis → Python → Bash & CLI → MATLAB** — every later page assumes the earlier ones. But for an experienced engineer arriving from outside neuroimaging, **Neuroscience → Medical imaging physics → MATLAB ↔ Python ↔ Data analysis** is usually the right shortcut.

Each page ends with a references block of canonical textbooks (with ISBN) and primary papers (with DOI). Treat the references as the next mile after the chapter.
