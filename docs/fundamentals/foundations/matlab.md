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

## Modern MATLAB (R2018b+)

> MATLAB modernised heavily after R2018b; if your mental model of MATLAB is pre-2018, this section is the update.

Five capability shifts now blur the line between "MATLAB" and "the Python/PyTorch stack". You can do most of what NumPy + PyTorch + Dask + Slurm do, in MATLAB, on the same data, with one license.

### 1. Deep Learning Toolbox / autodiff

`dlnetwork`, `dlarray`, and `dlgradient` give you a first-class autodiff engine — conceptually identical to PyTorch's autograd, syntactically MATLAB.

```matlab
function [loss, grads] = mseLoss(net, X, Y)
  Ypred = forward(net, X);
  loss  = mean((Ypred - Y).^2, 'all');
  grads = dlgradient(loss, net.Learnables);   % autodiff w.r.t. parameters
end

X = dlarray(rand(10, 32, 'single'), 'CB');    % 10-dim, batch=32, 'C'hannel/'B'atch
Y = dlarray(rand(1,  32, 'single'), 'CB');
net = dlnetwork(fullyConnectedLayer(1));

[loss, grads] = dlfeval(@mseLoss, net, X, Y); % dlfeval traces the graph
net = dlupdate(@(p, g) p - 0.01 * g, net, grads);
```

Same mental model as PyTorch: a *tape* records ops on `dlarray`s; `dlgradient` walks it backward. Reference: [MathWorks Deep Learning Toolbox](https://www.mathworks.com/products/deep-learning.html).

### 2. GPU computing

`gpuArray` makes the GPU transparent — wrap your array, MATLAB dispatches every supported op to the device.

```matlab
A = gpuArray(rand(10000, 'single'));     % uploads to GPU
B = A * A';                              % runs on GPU
C = gather(B);                           % brings result back to host

gpuDevice(2);                            % select GPU #2 explicitly
```

**When GPU wins:** dense linear algebra on matrices >~1000×1000, FFTs, convolutions, anything that runs the GPU at >50% utilisation. **When it doesn't:** small tight loops dominated by host-device transfer (the upload-compute-download round trip kills you). Always benchmark before and after. Reference: [GPU Computing in MATLAB](https://www.mathworks.com/help/parallel-computing/gpu-computing.html).

### 3. Out-of-core data — `tall` and `datastore`

`datastore` reads a directory of files lazily; `tall` arrays let you operate on data larger than RAM with familiar matrix syntax, deferred until `gather`.

```matlab
ds = datastore('derivatives/sub-*_dk.csv', 'Type', 'tabulartext');
T  = tall(ds);                              % rows on disk, not in RAM

mu = gather( groupsummary(T, 'site', 'mean', 'thickness_mean') );
```

The above aggregates a 10-GB BIDS-derivatives table by site without ever loading more than a chunk into memory. Reference: [Tall Arrays](https://www.mathworks.com/help/matlab/tall-arrays.html).

### 4. MEX for HPC

`mex` compiles C / C++ / Fortran into a callable MATLAB function. Use it when:

- You have a tight loop that *cannot* be vectorised (state-dependent, irregular branching).
- You need to call a custom CUDA kernel from MATLAB.
- You're calling into an existing C++ library and don't want to shell out.

```matlab
mex my_inner_loop.cpp                    % builds my_inner_loop.mexa64
out = my_inner_loop(x, y);               % call like any MATLAB function
```

For most users the vectorised MATLAB path is already fast enough; reach for MEX when the profiler shows a single function dominating runtime. Reference: [MEX File Functions](https://www.mathworks.com/help/matlab/call-mex-functions.html).

### 5. Parallel Computing Toolbox + Slurm

`parfor`, `parfeval`, and `distributed` arrays cover three parallelism patterns:

```matlab
parpool('local', 8)                      % 8-worker pool on this machine
parfor sub = 1:100
  process_subject(subjects(sub));        % each iter on a separate worker
end

f = parfeval(@expensive_step, 1, x);     % async fire-and-forget
result = fetchOutputs(f);
```

For multi-node Slurm clusters, [MATLAB Parallel Server](https://www.mathworks.com/help/matlab-parallel-server/index.html) lets a single `parfor` launch onto a Slurm cluster: configure a `parallel.cluster.Slurm` profile, then `parpool('slurm', 64)` and your loop runs across 64 nodes. The mental model is: same MATLAB code, larger pool.

### 6. Live Editor

The Live Editor (`.mlx` files) is MATLAB's notebook-style environment: code + formatted text + outputs + equations in one document, exportable to PDF / HTML. Useful for analysis writeups and teaching.

**Reproducibility caveat.** `.mlx` is a binary XML format; it doesn't `git diff` cleanly the way `.ipynb` (after `nbstripout`) does. For pipeline code, prefer `.m` scripts + a separate `.mlx` writeup. The [Live Editor docs](https://www.mathworks.com/help/matlab/live-scripts-and-functions.html) cover the export workflow.

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

## Exercises

1. **Logical indexing.** Given `x = randn(1000, 1)`, replace any value with `|x| > 3` by NaN without a loop.
2. **Table groupby.** Load `participants.tsv` as a `table`. Compute mean age per (`site`, `diagnosis`) using `groupsummary`.
3. **Paired t-test.** Read two same-length numeric vectors from `pre.csv` and `post.csv`; run a paired t-test and print the t-stat, degrees of freedom, and 95% CI.

??? success "Solutions"
    1. `x(abs(x) > 3) = NaN;`.
    2. `T = readtable('participants.tsv','FileType','text','Delimiter','\t'); G = groupsummary(T,{'site','diagnosis'},'mean','age');`.
    3. `[h,p,ci,stats] = ttest(pre, post); fprintf('t=%.2f df=%d CI=[%.3f, %.3f]\n', stats.tstat, stats.df, ci(1), ci(2));`.

## References

1. **Higham DJ, Higham NJ.** *MATLAB Guide.* 3rd ed. SIAM; 2017. ISBN 978-1611974652.
2. **Attaway S.** *MATLAB: A Practical Introduction to Programming and Problem Solving.* 5th ed. Butterworth-Heinemann; 2018. ISBN 978-0128154793.
3. **Friston K, Ashburner J, Kiebel S, Nichols T, Penny W (eds).** *Statistical Parametric Mapping: The Analysis of Functional Brain Images.* Academic Press; 2007. ISBN 978-0123725608. — SPM bible.
4. **Delorme A, Makeig S.** EEGLAB: an open source toolbox for analysis of single-trial EEG dynamics including independent component analysis. *J Neurosci Methods.* 2004;134(1):9-21. [doi:10.1016/j.jneumeth.2003.10.009](https://doi.org/10.1016/j.jneumeth.2003.10.009)
5. **Oostenveld R, Fries P, Maris E, Schoffelen J-M.** FieldTrip: open source software for advanced analysis of MEG, EEG, and invasive electrophysiological data. *Comput Intell Neurosci.* 2011;2011:156869. [doi:10.1155/2011/156869](https://doi.org/10.1155/2011/156869)

## Where to next

[Statistics](statistics.md) — the inferential machinery that turns numbers into conclusions.
