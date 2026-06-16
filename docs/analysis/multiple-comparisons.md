# Multiple comparisons

> Choosing between FDR, FWE, TFCE, and cluster correction — without lying to yourself or your reviewers.

## The problem

A typical voxel-wise GLM is ≈ 100 000 tests. At α = 0.05, you expect ≈ 5 000 false positives by chance. Without correction, every "result" is mostly noise.

## The toolbox

### Bonferroni — almost never the answer

Divide α by the number of tests. Correct, ultra-conservative, throws away every distributed effect. Useful as a sanity check, almost never as a primary correction.

### FDR (False Discovery Rate)

Control the *expected proportion of false positives among rejected nulls*. Less conservative than Bonferroni; widely accepted. Two flavours:

- **Benjamini-Hochberg** — independence or positive dependence.
- **Benjamini-Yekutieli** — arbitrary dependence; more conservative.

`statsmodels.stats.multitest.multipletests(p, method="fdr_bh")` is the Python entry point.

### FWE (Family-Wise Error)

Control the *probability of one or more false positives anywhere in the map*. Stricter than FDR. Two ways to compute it:

- **Random Field Theory (RFT)** — analytical, assumes smoothness; SPM and old FSL.
- **Permutation** — empirical, robust to smoothness assumptions; PALM, FSL `randomise`, `nilearn`.

For modern neuroimaging, prefer permutation FWE over RFT FWE.

### Cluster correction

Threshold the statistical map at a lenient voxel-wise threshold (e.g., p < 0.001), then keep only spatially contiguous clusters larger than a critical size. The cluster size threshold is calibrated to control FWE.

- Very high sensitivity for spatially extended effects.
- Notoriously sensitive to the cluster-forming threshold. **AFNI's 2017 retraction crisis** (Eklund et al.) traced back to cluster correction with p = 0.01 thresholds inflating FWE to > 70%. Use p ≤ 0.001 cluster-forming.

### TFCE (Threshold-Free Cluster Enhancement)

Combines cluster extent and peak intensity into a single statistic that doesn't require a cluster-forming threshold. Then a permutation distribution gives FWE-corrected p-values. **The current default for voxel-wise neuroimaging.**

FSL `randomise -T` and PALM `-T` both implement it.

## Picking one

| Situation | Choice |
| --- | --- |
| Voxel-wise (mass-univariate) | **TFCE + permutation** |
| ROI / atlas-level | **FDR** |
| Network-level (NBS) | **NBS** with permutation |
| Vertex-wise on the surface | **TFCE + permutation** (or FreeSurfer cluster-correction with strict threshold) |
| A few pre-registered tests | **Bonferroni** |

## The honest disclosure section

Whatever you pick, **report it explicitly**:

- The threshold (e.g., "TFCE-corrected p < 0.05 with 10 000 permutations").
- The cluster-forming threshold if you used voxel-wise cluster correction.
- The smoothing kernel — corrections that assume smoothness depend on it.

If your figures show uncorrected maps with a label like "p < 0.001 uncorrected", say so loudly in the legend. There's nothing wrong with showing exploratory maps; there's something wrong with hiding that they're exploratory.

## Where to next

That closes the Analysis section. From here, [Data engineering](../data-engineering/index.md) tells you how to make pipelines that produce these statistics reliably on hundreds of subjects.
