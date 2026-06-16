# Tutorial — Classical ML on cortical thickness

> Predict age from FreeSurfer cortical thickness with proper site-stratified CV, ComBat harmonisation, and honest reporting. ~30 minutes.

## Prerequisites

- [Fundamentals → Foundations → Statistics + Data analysis](../fundamentals/foundations/statistics.md)
- [AI/ML → Classical ML on volumetrics](../ai/classical-ml.md)
- [AI/ML → Evaluation pitfalls](../ai/evaluation.md)

## Pipeline overview

```mermaid
flowchart LR
    FS[FreeSurfer<br/>derivatives] --> EX[Per-region<br/>thickness extract]
    EX --> CB[ComBat<br/>site harmonisation]
    CB --> SP[Site-stratified<br/>group K-Fold]
    SP --> MOD[Ridge / GBT<br/>train+eval]
    MOD --> REP[Honest report:<br/>MAE + CI per site]
    style FS fill:#fff,stroke:#888
    style REP fill:#e0e0ff,stroke:#444
```

## 1. Gather per-subject thickness vectors

```python
import pandas as pd, numpy as np
from pathlib import Path

def parse_aparc(path):
    """Parse a FreeSurfer aparc.stats file into a 1-row DataFrame of ThickAvg."""
    df = pd.read_csv(path, comment="#", sep=r"\s+", header=None,
                     names=["StructName", "NumVert", "SurfArea", "GrayVol",
                            "ThickAvg", "ThickStd", "MeanCurv", "GausCurv",
                            "FoldInd", "CurvInd"])
    return df[["StructName", "ThickAvg"]].set_index("StructName").T.reset_index(drop=True)

rows = []
for sub_dir in sorted(Path("derivatives/freesurfer").glob("sub-*")):
    sub = sub_dir.name
    lh = parse_aparc(sub_dir / "stats/lh.aparc.stats").rename(columns=lambda c: "lh_"+c)
    rh = parse_aparc(sub_dir / "stats/rh.aparc.stats").rename(columns=lambda c: "rh_"+c)
    rows.append(pd.concat([pd.DataFrame({"subject_id":[sub]}), lh, rh], axis=1))

X = pd.concat(rows, ignore_index=True)

# Join with the cohort metadata
meta = pd.read_csv("participants.tsv", sep="\t")
df = X.merge(meta, on="subject_id", how="inner", validate="one_to_one")
print(df.shape, df.columns[:6].tolist())
```

## 2. Harmonise across sites with ComBat

```python
from neuroCombat import neuroCombat

features = [c for c in df.columns if c.startswith(("lh_", "rh_"))]
res = neuroCombat(
    dat=df[features].T.values,           # features × subjects
    covars=df[["site", "age", "sex"]],
    batch_col="site",
    categorical_cols=["sex"],
    continuous_cols=["age"],
)
df_h = df.copy()
df_h[features] = res["data"].T
```

Always preserve the **biological covariates** during harmonisation.

## 3. Site-stratified group K-Fold + nested CV

```python
from sklearn.model_selection import GroupKFold, GridSearchCV
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import numpy as np

X = df_h[features].values
y = df_h["age"].values
groups = df_h["site"].values

pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("ridge", Ridge()),
])

outer = GroupKFold(n_splits=5)
mae_per_fold, predictions = [], np.zeros_like(y, dtype=float)

for train_idx, test_idx in outer.split(X, y, groups):
    inner = GroupKFold(n_splits=4)
    gs = GridSearchCV(pipe, param_grid={"ridge__alpha": [0.1, 1, 10, 100, 1000]},
                      cv=inner, scoring="neg_mean_absolute_error", n_jobs=4)
    gs.fit(X[train_idx], y[train_idx], groups=groups[train_idx])
    pred = gs.predict(X[test_idx])
    predictions[test_idx] = pred
    mae_per_fold.append(np.mean(np.abs(pred - y[test_idx])))

print(f"Outer MAE: mean={np.mean(mae_per_fold):.2f}, "
      f"std={np.std(mae_per_fold):.2f} years")
```

## 4. Report honestly

```python
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

sns.set_theme(style="whitegrid", context="paper", font_scale=1.1)

fig, ax = plt.subplots(1, 2, figsize=(10, 4.5), dpi=150)

# Predicted vs true
sns.scatterplot(x=y, y=predictions, hue=df_h["site"], ax=ax[0], alpha=0.7)
lo, hi = y.min(), y.max()
ax[0].plot([lo, hi], [lo, hi], "k--", lw=1)
ax[0].set(xlabel="Chronological age", ylabel="Predicted age",
          title=f"Cross-site CV (MAE={np.mean(mae_per_fold):.1f} y)")

# Per-site MAE
mae_df = pd.DataFrame({"site": groups, "abs_err": np.abs(predictions - y)})
sns.boxplot(data=mae_df, x="site", y="abs_err", ax=ax[1])
ax[1].set(xlabel="Site", ylabel="|prediction − truth| (years)",
          title="Per-site error distribution")
fig.tight_layout()
fig.savefig("figs/cv_results.pdf", bbox_inches="tight")

# Bootstrap CI on MAE
boot = []
rng = np.random.default_rng(42)
for _ in range(2000):
    idx = rng.integers(0, len(y), len(y))
    boot.append(np.mean(np.abs(predictions[idx] - y[idx])))
ci = np.percentile(boot, [2.5, 97.5])
print(f"95% bootstrap CI for MAE: [{ci[0]:.2f}, {ci[1]:.2f}]")
```

## Pitfalls

- **Subject-level leakage** if any subject appears in both train and test (e.g. two timepoints).
- **Per-site overfitting** — without site-stratified CV, your MAE is optimistic.
- **Harmonisation leakage** — ideally fit ComBat *within each train fold* and apply to test, not globally.
- **Reporting only mean MAE** — the per-site box-plot is what reviewers want.

## References

1. **Fortin J-P, Cullen N, Sheline YI, et al.** Harmonization of cortical thickness measurements across scanners and sites. *NeuroImage.* 2018;167:104-120. [doi:10.1016/j.neuroimage.2017.11.024](https://doi.org/10.1016/j.neuroimage.2017.11.024)
2. **Cole JH, Marioni RE, Harris SE, Deary IJ.** Brain age and other bodily 'ages': implications for neuropsychiatry. *Mol Psychiatry.* 2019;24:266-281. [doi:10.1038/s41380-018-0098-1](https://doi.org/10.1038/s41380-018-0098-1)
3. **Pedregosa F, Varoquaux G, Gramfort A, et al.** Scikit-learn: machine learning in Python. *JMLR.* 2011;12:2825-2830.
