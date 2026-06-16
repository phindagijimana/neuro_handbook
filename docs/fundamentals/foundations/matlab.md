# MATLAB

> The de-facto second language of neuroimaging — and the native tongue of SPM, EEGLAB, FieldTrip, and large parts of the MRI methods literature.

This page assumes you'll spend at least some time in MATLAB whether or not you'd choose it from scratch. If you're new to it, you can be productive in a week.

## Environment and reproducibility

MATLAB is licensed and versioned. Pin the version your project uses:

- MATLAB R2024a (and similar) ship with a stable [matlab](https://www.mathworks.com/help/matlab/) base.
- Toolboxes (Statistics & Machine Learning, Signal Processing, Image Processing, Parallel Computing) cost extra and must be on the path.
- Document the toolboxes used by every script. `ver` shows what's installed.

Reproducibility:

```matlab
rng(42)                                 % fix random seed
addpath(genpath('thirdparty/'))         % put your toolboxes on path
savepath                                % persist (or use startup.m)
```

## Core language — concepts with examples

### Arrays and indexing

MATLAB is column-major and 1-indexed. Everything is a matrix by default.

```matlab
A = magic(4)                            % 4x4 matrix
A(2, 3)                                  % row 2, col 3 (= 7)
A(:, 2)                                  % entire 2nd column
A(end, :)                                % last row
B = A > 8;                               % logical mask, same shape as A
A(B)                                     % elements > 8 as a column vector
```

### Vectorisation beats loops

```matlab
% slow
for k = 1:N
  y(k) = sin(k) + cos(k);
end

% fast — vectorised
k = 1:N;
y = sin(k) + cos(k);
```

### Scripts vs functions

- **Scripts** run in the base workspace; great for exploration, dangerous in pipelines.
- **Functions** have local scope; one per file (or local functions in the same file). Use functions for anything that runs more than once.

```matlab
function out = zscore_nan(x, dim)
% z-score along dimension dim, NaN-safe
  if nargin < 2, dim = 1; end
  mu = mean(x, dim, 'omitnan');
  sd = std(x, 0, dim, 'omitnan');     % 0 = N-1 normalisation
  out = (x - mu) ./ sd;
end
```

### Control flow

```matlab
if age > 60
  group = "older";
elseif age >= 18
  group = "adult";
else
  group = "minor";
end

for sub = subjects'
  fprintf('processing %s\n', sub);
end

while ~converged
  [theta, converged] = step(theta);
end

try
  fid = fopen('out.txt', 'w');
  fprintf(fid, 'hello\n');
catch ME
  warning('failed: %s', ME.message);
end
```

### File I/O — tables and matrices

```matlab
T = readtable('participants.tsv', 'FileType', 'text', 'Delimiter', '\t');
T.age_z = (T.age - mean(T.age, 'omitnan')) / std(T.age, 'omitnan');
writetable(T, 'participants_with_z.tsv', 'FileType', 'text', 'Delimiter', '\t');

X = readmatrix('connectome.csv');
writematrix(X, 'connectome.csv');
```

`table` and `timetable` are the modern equivalents of pandas DataFrames; use them.

## Plotting

```matlab
figure('Position', [100 100 800 400]);
subplot(1, 2, 1)
imagesc(T1w_axial); axis image off; colormap gray
title('T1w mid-axial')

subplot(1, 2, 2)
plot(t, bold); xlabel('t (s)'); ylabel('BOLD'); grid on
title('voxel timeseries')

exportgraphics(gcf, 'figs/qc_001.png', 'Resolution', 300);
```

`exportgraphics` (R2020a+) is the modern publication-quality saver.

## Statistics and modeling — essentials

```matlab
[h, p, ci, stats] = ttest2(group_a, group_b);    % independent t-test
[h, p, ci, stats] = ttest(paired_a, paired_b);   % paired
[r, p] = corr(x, y, 'Type', 'Pearson');

mdl = fitlm(T, 'y ~ age + sex + scanner');       % linear model
disp(mdl)
plotResiduals(mdl, 'probability')

mdl_me = fitlme(T, 'y ~ age + sex + (1 | scanner)');   % mixed-effects
```

`fitlm` / `fitglm` / `fitlme` / `fitrm` cover the regression universe.

## Toolboxes commonly used in neuroimaging

| Toolbox | Use | Docs |
|---|---|---|
| **SPM12 / SPM25** | fMRI, structural, GLM, DCM | [spm](https://www.fil.ion.ucl.ac.uk/spm/) |
| **EEGLAB** | EEG preprocessing + ICA | [eeglab](https://eeglab.org) |
| **FieldTrip** | EEG / MEG | [fieldtrip](https://www.fieldtriptoolbox.org) |
| **Brainstorm** | M/EEG / fMRI | [brainstorm](https://neuroimage.usc.edu/brainstorm/) |
| **CAT12** | Computational anatomy (SPM extension) | [cat12](https://neuro-jena.github.io/cat/) |
| **CONN** | Functional connectivity | [conn](https://web.conn-toolbox.org) |
| **Cosmo-MVPA** | Multivariate pattern analysis | [cosmo-mvpa](https://www.cosmomvpa.org) |

Add to the path with `addpath(genpath('spm12'))`. Many of these provide *both* a GUI and a callable function API — use the function API for pipelines.

## BIDS, paths, and interoperability

```matlab
img = niftiread('sub-001_T1w.nii.gz');           % read raw voxels
info = niftiinfo('sub-001_T1w.nii.gz');           % header + affine
disp(info.Transform.T)                            % 4x4 affine

niftiwrite(img, 'out_T1w.nii', info, 'Compressed', true);
```

For BIDS-aware MATLAB, the [BIDS-MATLAB](https://github.com/bids-standard/bids-matlab) layer is the de-facto wrapper.

To move between MATLAB and Python, MATLAB ships [MATLAB Engine for Python](https://www.mathworks.com/help/matlab/matlab-engine-for-python.html); the cleaner pattern in 2026 is to write data to disk (Parquet, MAT-v7.3 = HDF5) and switch language at the file boundary.

## Lab workflow checklist

- One `startup.m` per project that adds toolboxes to the path and sets `rng`.
- One driver script per analysis (`run_analysis.m`).
- One function per non-trivial step (`compute_thickness.m`, `gather_metrics.m`).
- Outputs land in `derivatives/` with timestamps.
- `diary` log files for each run.
- Push the *code* to git; never the data.

## Debugging, memory, batch runs

```matlab
dbstop if error                          % break into debugger on error
keyboard                                 % manual breakpoint
profile on; run('analysis.m'); profile viewer

whos                                     % variables + sizes
memory                                   % MATLAB memory status (Windows)

% Batch / headless on cluster
matlab -batch "addpath('src'); run_analysis('sub-001')"
```

## When to leave MATLAB for Python

- Container-first pipelines (Docker / Apptainer): Python wins on portability.
- Deep learning: PyTorch + MONAI is the modern stack.
- Tabular analytics: pandas + Polars.
- Anything you want others to run without a licence.

When to *stay*: SPM-based workflows where the heavy lifting is in SPM batches; EEGLAB ICA pipelines; collaborators who write MATLAB only.

## References

1. **Higham DJ, Higham NJ.** *MATLAB Guide.* 3rd ed. SIAM; 2017. ISBN 978-1611974652.
2. **Attaway S.** *MATLAB: A Practical Introduction to Programming and Problem Solving.* 5th ed. Butterworth-Heinemann; 2018. ISBN 978-0128154793.
3. **Friston K, Ashburner J, Kiebel S, Nichols T, Penny W (eds).** *Statistical Parametric Mapping: The Analysis of Functional Brain Images.* Academic Press; 2007. ISBN 978-0123725608. — SPM bible.
4. **Delorme A, Makeig S.** EEGLAB: an open source toolbox for analysis of single-trial EEG dynamics including independent component analysis. *J Neurosci Methods.* 2004;134(1):9-21. [doi:10.1016/j.jneumeth.2003.10.009](https://doi.org/10.1016/j.jneumeth.2003.10.009)
5. **Oostenveld R, Fries P, Maris E, Schoffelen J-M.** FieldTrip: open source software for advanced analysis of MEG, EEG, and invasive electrophysiological data. *Comput Intell Neurosci.* 2011;2011:156869. [doi:10.1155/2011/156869](https://doi.org/10.1155/2011/156869)

## Where to next

[Statistics](statistics.md) — the inferential machinery that turns numbers into conclusions.
