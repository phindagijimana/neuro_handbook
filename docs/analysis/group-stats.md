# Group-level statistics

> Going from per-subject maps to "is this effect real across the cohort?"

## The general linear model

Almost everything is a GLM:

```text
y = X β + ε
```

- `y` — a per-subject value at each voxel / vertex / edge.
- `X` — the design matrix: one column per regressor (group label, age, sex, motion, etc.).
- `β` — the regression weights (what you want to estimate).
- `ε` — noise, assumed iid Gaussian.

Run the GLM at each voxel; produce a statistical map; correct for multiple comparisons.

## Two analysis levels

- **First-level** — within a single subject. For fMRI, this is the BOLD timeseries regressed against the task design matrix; the output per voxel is one β per condition.
- **Group-level (second-level)** — across subjects. The βs from first level become the `y` of the group GLM.

This is the "summary-statistics approach" — FSL's FEAT and SPM's basic pipeline both implement it. It's an approximation (it ignores within-subject variance heterogeneity) but it works well in practice.

## Mixed models when subjects vary

When subjects contribute different numbers of timepoints (longitudinal data), or first-level variance differs dramatically (different number of trials, dropouts), the summary-statistics approximation breaks. Switch to a proper mixed model:

- **`nilearn.glm.second_level`** — handles weighted least squares with per-subject variance.
- **FSL FLAME / FLAME1** — Bayesian; the gold standard for noisy second-level fits.
- **`afex` / `lme4`** in R — when you want full mixed-model flexibility.

## Designs you'll meet

- **Two-sample t-test** — group A vs group B.
- **Paired t-test** — same subjects, two conditions / timepoints.
- **One-way ANOVA** — three or more groups.
- **Regression on a covariate** — e.g., effect of age on cortical thickness.
- **Interaction** — group × covariate, group × condition.

Always sketch the design matrix on paper before you trust the output of any tool.

## Permutation testing — the safe default

Parametric GLM p-values assume normality, independence, and the right model. For neuroimaging — small samples, heavy-tailed errors, spatial correlation — permutation tests are usually more honest:

- **PALM** (FSL) — voxel-wise or vertex-wise, supports arbitrary designs, including freedman-lane for confound regression.
- **`nilearn.mass_univariate.permuted_ols`** — simpler, Python-native.

The cost is compute (~1000× a single GLM); the benefit is p-values that survive review.

## Effect sizes — report them

A `p < 0.05` map says where the effect is unlikely-to-be-noise; it does not say where the effect is *large*. Always report:

- **Cohen's d** (for group differences).
- **R²** (for regressions).
- **Confidence intervals** on the effect, not just on the test statistic.

A reviewer can't tell a Cohen's d = 0.05 result from a d = 1.5 result from a thresholded map alone. Show both.

## Where to next

[Multiple comparisons](multiple-comparisons.md) — what to do about the 100 000 tests you just ran.
