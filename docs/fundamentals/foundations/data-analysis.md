# Data analysis

> Turning a folder of derivatives into a defensible analysis. The applied, hands-on layer between *statistics-the-theory* and *running-the-cluster*.

This page is about the day-to-day mechanics: cleaning tables, joining derivatives, exploring distributions, choosing a model, and producing the figure that will end up in the paper. The depth of *what test* is in [Statistics](statistics.md); this page is about *how the analysis actually happens*.

## A reproducible analysis workflow

Most published neuroimaging analyses follow a recognisable shape:

```text
raw BIDS dataset
    │
    ▼
preprocess (fMRIPrep, QSIPrep, FreeSurfer)
    │
    ▼
derivatives/  ── per-subject tables, NIfTI maps, surfaces
    │
    ▼
extract  ── one row per subject, columns = features
    │
    ▼
clean    ── missing, outliers, harmonisation (ComBat)
    │
    ▼
explore  ── distributions, correlations, QC plots
    │
    ▼
model    ── GLM, mixed effects, ML, group stats
    │
    ▼
report   ── figures, tables, methods text
```

Each arrow is a script you can re-run; the final figure is a function of the raw BIDS + the code.

## The cohort table — your single source of truth

For most analyses you'll end up with **one wide DataFrame** keyed by `subject_id` (or `(subject_id, session_id)`):

```python
import pandas as pd

participants = pd.read_csv("participants.tsv", sep="\t")
fs_stats     = gather_freesurfer_stats("derivatives/freesurfer/")  # 84 cols
qc           = pd.read_parquet("derivatives/mriqc/group_metrics.parquet")
beh          = pd.read_csv("behavioral.csv")

cohort = (
    participants
    .merge(fs_stats, on="subject_id", how="left", validate="one_to_one")
    .merge(qc,       on="subject_id", how="left", validate="one_to_one")
    .merge(beh,      on="subject_id", how="left", validate="one_to_one")
)
print(cohort.shape, cohort.columns.tolist())
```

Three habits to copy:

- **`validate="one_to_one"`** — fails loud if a join produces duplicates.
- **`how="left"`** — keep every subject; let missing imaging be `NaN`.
- **Save the joined table** to Parquet next to the inputs; the joining script is committed to git.

## Exploratory data analysis (EDA) — the part people skip

Before any inferential test, look at your data. The cost is hours; skipping it costs months.

### Univariate look

```python
import seaborn as sns, matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 3, figsize=(12, 6))
for ax, col in zip(axes.ravel(), ["age", "fd_mean", "wm_volume",
                                  "lh_thickness_mean", "behavior_z",
                                  "education_years"]):
    sns.histplot(cohort[col].dropna(), ax=ax, kde=True)
    ax.set_title(col)
fig.tight_layout()
```

Check: range, skew, multimodality, the proportion of `NaN`. A bimodal "age" with peaks at 25 and 65 is a *cohort* problem, not an analysis problem.

### Bivariate look

```python
sns.pairplot(cohort[["age", "fd_mean", "behavior_z", "wm_volume"]],
             diag_kind="kde", corner=True)
```

Look for: implausible outliers, monotonic vs non-linear relationships, the well-known motion-age coupling.

### Missing-data audit

```python
miss = cohort.isna().mean().sort_values(ascending=False)
print(miss.head(20))
```

Three classes of missingness:

- **MCAR** — Missing Completely at Random. Drop or impute, your choice.
- **MAR** — Missing at Random *given* other observed variables. Multiple imputation.
- **MNAR** — Missing Not at Random. The hard case; usually requires sensitivity analysis.

Subjects who failed `recon-all` are *not* MCAR — they probably moved more. Drop them and you bias your effect.

## Outlier handling

Two categories:

- **Statistical outliers** — outside expected distribution. Often legitimate biology; rarely drop.
- **QC failures** — bad acquisition, failed preprocessing. Drop, but document.

The MRIQC group report ([Esteban et al., 2017](https://doi.org/10.1371/journal.pone.0184661)) gives per-subject IQMs (Image Quality Metrics) you can threshold. Don't drop subjects based on the analysis-of-interest variable — that's circular.

## Harmonisation — when sites or scanners differ

Multi-site cohorts have site/scanner variance that often exceeds biology.

### ComBat — the workhorse

[Johnson et al., 2007](https://doi.org/10.1093/biostatistics/kxj037) (microarray origin) and the neuroimaging adaptation [Fortin et al., 2018](https://doi.org/10.1016/j.neuroimage.2017.11.024) model site as an additive + multiplicative effect on each feature; estimate it empirical-Bayes-shrunk; subtract. Implementations: [`neuroCombat`](https://github.com/Jfortin1/ComBatHarmonization), [`neuroHarmonize`](https://github.com/rpomponio/neuroHarmonize) (preserves biology), longitudinal ComBat.

```python
from neuroCombat import neuroCombat
res = neuroCombat(
    dat=cohort_features.T.values,            # features × subjects
    covars=cohort[["site", "age", "sex", "diagnosis"]],
    batch_col="site",
    categorical_cols=["sex", "diagnosis"],
    continuous_cols=["age"],
)
harmonised = pd.DataFrame(res["data"].T, columns=cohort_features.columns)
```

Always preserve the **biological covariates** during harmonisation. Always validate that harmonisation didn't accidentally remove your effect.

### Site as a covariate — when ComBat overcorrects

Sometimes the right answer is `y ~ age + sex + site + ...` in the GLM. Cheap and transparent; doesn't generalise to a held-out site, but neither does ComBat.

## Confound regression — the fMRI special case

fMRIPrep emits `*_desc-confounds_timeseries.tsv` with ~30 columns. Standard regressors:

| Strategy | Columns |
|---|---|
| **6 motion** | `trans_x/y/z`, `rot_x/y/z` |
| **24 motion** | The 6 + squares + derivatives + derivative squares |
| **aCompCor** | Top 5 PCA components from CSF + WM masks |
| **ICA-AROMA** | Use the AROMA-cleaned BOLD as input |
| **Global signal** | Controversial; document either way |

Pick one strategy and use it across your cohort. Mixing strategies inside a single analysis is a reviewer's gift.

## Feature extraction — from voxels to a row

Many analyses become tabular at this step. Examples:

```python
# FreeSurfer thickness per DK region → 1 row of 68 features per subject
df = pd.read_csv("aparc.lh.thickness.tsv", sep="\t")

# Mean BOLD timecourse per Schaefer-400 parcel → 1 row per subject after FC
from nilearn.maskers import NiftiLabelsMasker
masker = NiftiLabelsMasker(labels_img="Schaefer400.nii.gz", standardize=True)
ts = masker.fit_transform("sub-001_bold.nii.gz",
                         confounds="sub-001_desc-confounds.tsv")

# Connectome upper triangle → 79,800 features per subject (Schaefer-400)
import numpy as np
conn = np.corrcoef(ts.T)
triu = conn[np.triu_indices_from(conn, k=1)]
```

Decide early whether to analyse voxel-wise (mass-univariate maps) or feature-wise (tabular ML). Both have a place; mixing strategies hurts.

## Pipelines for the analysis itself

The same data-engineering primitives apply to *analysis*: DAG, idempotency, observability. For an iterative analysis I recommend:

- **Snakemake / Nextflow** for cohort-scale recomputation. See [Data engineering → Foundations](../../data-engineering/foundations.md).
- **Make** for small projects (`make figs/fig2.pdf`).
- **Notebook** for the final figure, *restarted and run from the top* before publication.
- **`papermill` + parameterised notebooks** for per-subject reports.

## A pragmatic figure recipe

Most paper figures are some variant of:

```python
# Figure 2: cohort age effect on cortical thickness, by site
import seaborn as sns
sns.set_theme(style="whitegrid", context="paper", font_scale=1.1)

g = sns.lmplot(
    data=cohort, x="age", y="mean_thickness",
    hue="site", col="diagnosis", height=3.6, aspect=1.1,
    scatter_kws={"alpha": 0.5, "s": 25}, line_kws={"lw": 2},
)
g.set_axis_labels("Age (years)", "Mean cortical thickness (mm)")
for ax in g.axes.ravel():
    ax.set_xlim(18, 90)
g.savefig("figs/fig2_age_thickness.pdf", bbox_inches="tight", dpi=300)
```

Save vector formats (`.pdf`, `.svg`) — journals will rasterise them at 600+ DPI. Keep raw data behind every figure committed (`figs/fig2_data.parquet`) so reviewers can ask "but what about excluding...".

## Building dashboards / reports

For per-cohort reports (especially during data collection):

- **Plotly + Dash** ([docs](https://dash.plotly.com)) — Python web dashboards.
- **Streamlit** ([docs](https://docs.streamlit.io)) — minimal-code web apps.
- **Quarto** ([docs](https://quarto.org)) — versioned scientific reports, Python + R + Jupyter.
- **Static HTML** — sometimes the right choice; everyone can open it.

For internal labs that just want "is the QC dashboard fresh?", a single `cohort_qc.html` regenerated on every Snakemake run beats a stack of cloud infrastructure.

## Common pitfalls

- **Concatenating instead of joining.** `pd.concat(axis=0)` stacks; if you meant a wide join you'll silently double rows.
- **`pd.merge` without `validate`.** A many-to-many join produces row explosions you won't catch until the analysis says n=4892 instead of 489.
- **Plotting with default Matplotlib for paper figures.** Default DPI is too low; default font is ugly. Set up once, reuse.
- **Not saving the intermediate cohort table.** A reviewer asks "what happens if you exclude subjects with FD > 0.3?" — be able to answer in 30 seconds, not an afternoon.
- **Running analysis in a notebook only.** Notebooks should be the *presentation* layer; the logic should be importable modules with tests.

## A reproducibility audit (10 minutes)

Before sending an analysis to a co-author, run this checklist:

- [ ] `make` or `snakemake -n` reports zero changes (everything is up to date).
- [ ] `pytest` passes.
- [ ] The cohort table CSV / Parquet hash is committed.
- [ ] Every figure script writes a sibling `.tsv` of its raw data.
- [ ] The seed for any randomised step is fixed and recorded.
- [ ] The container / lockfile is documented.
- [ ] A `methods.md` paragraph summarising what was done is up to date.

## Exercises

1. **Missing-data audit.** Read `participants.tsv`. Print the percentage missing per column, sorted descending; classify each column as likely MCAR, MAR, or MNAR with one sentence each.
2. **Group K-Fold.** Using `sklearn.model_selection.GroupKFold`, set up a 5-fold split on a synthetic DataFrame with 50 subjects across 3 sites. Verify no subject ID appears in train and test of the same fold.
3. **ComBat sanity check.** After harmonisation, compute the F-statistic for `site` predicting each harmonised feature. Report what changed vs raw.

??? success "Solutions"
    1. `df.isna().mean().sort_values(ascending=False) * 100`; reason from domain knowledge.
    2. `gkf = GroupKFold(5); for tr, te in gkf.split(X, y, groups=df['subject_id']): assert set(df.iloc[tr]['subject_id']) & set(df.iloc[te]['subject_id']) == set()`.
    3. Use `scipy.stats.f_oneway` per feature, comparing pre/post; per-feature F values should drop substantially.

## References

1. **McKinney W.** *Python for Data Analysis.* 3rd ed. O'Reilly; 2022. ISBN 978-1098104030. Free online: [https://wesmckinney.com/book/](https://wesmckinney.com/book/)
2. **Tukey JW.** *Exploratory Data Analysis.* Addison-Wesley; 1977. ISBN 978-0201076165.
3. **Wickham H, Çetinkaya-Rundel M, Grolemund G.** *R for Data Science.* 2nd ed. O'Reilly; 2023. ISBN 978-1492097402. Free online: [https://r4ds.hadley.nz/](https://r4ds.hadley.nz/) — the EDA chapters generalise across languages.
4. **Fortin J-P, Cullen N, Sheline YI, et al.** Harmonization of cortical thickness measurements across scanners and sites. *NeuroImage.* 2018;167:104-120. [doi:10.1016/j.neuroimage.2017.11.024](https://doi.org/10.1016/j.neuroimage.2017.11.024)
5. **Pomponio R, Erus G, Habes M, et al.** Harmonization of large MRI datasets for the analysis of brain imaging patterns throughout the lifespan. *NeuroImage.* 2020;208:116450. [doi:10.1016/j.neuroimage.2019.116450](https://doi.org/10.1016/j.neuroimage.2019.116450) — neuroHarmonize.
6. **Esteban O, Birman D, Schaer M, et al.** MRIQC: advancing the automatic prediction of image quality in MRI from unseen sites. *PLoS One.* 2017;12(9):e0184661. [doi:10.1371/journal.pone.0184661](https://doi.org/10.1371/journal.pone.0184661)
7. **Botvinik-Nezer R, Holzmeister F, Camerer CF, et al.** Variability in the analysis of a single neuroimaging dataset by many teams. *Nature.* 2020;582:84-88. [doi:10.1038/s41586-020-2314-9](https://doi.org/10.1038/s41586-020-2314-9)
8. **Allen M, Poggiali D, Whitaker K, et al.** Raincloud plots: a multi-platform tool for robust data visualization. *Wellcome Open Res.* 2021;4:63. [doi:10.12688/wellcomeopenres.15191.2](https://doi.org/10.12688/wellcomeopenres.15191.2)

## Where to next

[Statistics](statistics.md) — the inferential layer on top of the workflows on this page.
