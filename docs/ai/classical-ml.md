# Classical ML on volumetrics

> When you do not need deep learning.

Neuroimaging cohorts are small (hundreds to low-thousands of subjects) and features are highly structured (volumes, surfaces, connectomes). For many questions, a linear model on engineered features beats a deep network you don't have the data to train.

## Where classical ML still wins

- **Predicting a scalar outcome** (age, cognitive score, group label) from cohort-level features.
- **Sample size < ~5,000 subjects**. Below that, the bias-variance tradeoff usually favours simpler models.
- **Interpretability matters** — weights on Desikan-Killiany regions are easy to communicate; CNN feature maps are not.
- **You need fast iteration** — a scikit-learn pipeline trains in seconds, not hours.

## Feature engineering on the standard outputs

The big neuroimaging pipelines emit numbers you can use directly:

| Source | Features | Typical dimension |
| --- | --- | --- |
| FreeSurfer / sMRIPrep | Cortical thickness, surface area, subcortical volumes, parcellations | 70–1,000 per subject |
| QSIRecon | Microstructure averages per tract | 30–100 per subject |
| Connectome | Edge weights between region pairs | 30–10,000 (symmetric) |
| fMRI | Region-mean BOLD, ALFF, functional connectivity | 100–10,000 |

Combine these into a wide subject × feature table. Standard ML libraries take it from there.

## A minimal scikit-learn pipeline

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.linear_model import RidgeCV
from sklearn.model_selection import GroupKFold, cross_val_score
import pandas as pd

df = pd.read_csv("cohort_features.csv")
X = df.drop(columns=["age", "subject_id", "site"]).values
y = df["age"].values
groups = df["site"].values  # split by site to test generalisation

pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("select", SelectKBest(f_regression, k=200)),
    ("model", RidgeCV(alphas=[0.1, 1.0, 10.0, 100.0])),
])

scores = cross_val_score(
    pipe, X, y, groups=groups,
    cv=GroupKFold(n_splits=5),
    scoring="neg_mean_absolute_error",
)
print(-scores.mean(), -scores.std())
```

Three things this snippet gets right that beginners often miss:

1. **`GroupKFold(groups=site)`** — never let subjects from the same site appear in train and test. Otherwise the model learns site, not biology.
2. **`SelectKBest` inside the pipeline** — feature selection on the full data is leakage; selecting inside `cross_val_score` is not.
3. **Ridge with CV over `alphas`** — regularisation strength is a hyperparameter, and the cohort is too small to pretend otherwise.

## Sample-size reality check

Rule of thumb: you need **~10 subjects per feature** for a stable linear model, **~100 per feature** for a deep one. A typical lab cohort (n = 300) supports ~30 effective features, not 84×84 connectome edges. Either:

- Aggregate (mean per network, mean per lobe).
- Use a sparse model (`Lasso`, `ElasticNet`).
- Use representation learning to reduce dimensionality *without* peeking at the label.

## Common mistakes

- Z-scoring the entire dataset before train/test split — leakage.
- Reporting in-sample fit instead of cross-validated performance.
- Forgetting site / scanner / batch as a confounder.
- Using vanilla `KFold` on a dataset with repeated measures per subject — the same subject ends up in train and test.

## Where to next

[Deep learning for imaging](deep-learning.md) — when the inputs are voxels rather than scalars and you need a CNN or transformer.
