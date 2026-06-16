# Statistics

> The inferential machinery every neuroimaging analysis sits on. Get this layer right and the rest is technical work; get it wrong and your conclusions are decoration.

## Probability — the layer underneath

Probability quantifies uncertainty. Three concepts to keep clear:

- **Random variable** — a measurable function from outcomes to numbers (the BOLD value at voxel $v$ at time $t$).
- **Probability density / mass function** — describes how likely each value is.
- **Expectation, variance, covariance** — moments that summarise distributions:

$$
\mathbb{E}[X] = \int x \, p(x) \, dx, \quad
\mathrm{Var}(X) = \mathbb{E}\!\left[(X - \mathbb{E}[X])^2\right]
$$

The Gaussian (normal) distribution dominates neuroimaging modelling because of the **Central Limit Theorem** — the sum of many independent contributions tends Gaussian. Tests like the t-test rest on that assumption; check it.

## Descriptive statistics

Always report, per variable:

- **Centre** — mean or median.
- **Spread** — standard deviation or IQR.
- **Shape** — skewness, kurtosis, or just a histogram.
- **Sample size** — and the missing-data rate.

Effect sizes (next section) often matter more than significance.

## Hypothesis testing — the GLM is most of what you need

The **general linear model** subsumes the t-test, ANOVA, regression, and most fMRI / morphometry tests:

$$
y = X\beta + \varepsilon, \qquad \varepsilon \sim \mathcal{N}(0, \sigma^2 I)
$$

- $y$ — observed values (per subject or per voxel).
- $X$ — design matrix (regressors).
- $\beta$ — unknown coefficients to estimate.
- $\varepsilon$ — Gaussian noise.

The OLS estimator $\hat\beta = (X^TX)^{-1}X^Ty$ is the best linear unbiased estimator under standard assumptions (Gauss-Markov theorem). t- and F-statistics from this fit are the workhorses of mass-univariate neuroimaging.

### A one-line worked example (per-voxel age effect on thickness)

$$
\text{thickness}_{i} = \beta_0 + \beta_1\,\text{age}_i + \beta_2\,\text{sex}_i + \beta_3\,\text{site}_i + \varepsilon_i
$$

$\beta_1$ is the per-voxel effect of age controlling for sex and site. Repeat at every voxel/vertex; correct for multiple comparisons (next section).

## Mixed models — when measurements are not independent

Longitudinal scans of the same subject share subject-level variance; multi-site cohorts share site-level variance. **Linear mixed-effects models** explicitly model these:

$$
y_{ij} = X_{ij}\beta + Z_{ij}b_i + \varepsilon_{ij}, \quad b_i \sim \mathcal{N}(0, \Sigma)
$$

- $b_i$ — random effects per cluster (subject, site).
- Fitted with REML.

In R: `lme4::lmer(y ~ age + (1 | subject))`. In Python: `statsmodels.formula.api.mixedlm`. In MATLAB: `fitlme`. Always.

## Multiple comparisons — the wake-up call

A typical voxel-wise GLM is ≈ 10⁵ tests. At $\alpha = 0.05$, **5 000 false positives** by chance. Without correction, every "result" is mostly noise.

| Method | Controls | When to use |
|---|---|---|
| **Bonferroni** | FWER | Tiny number of tests |
| **FDR (BH / BY)** | False Discovery Rate | Most cases; less conservative than FWE |
| **FWE permutation** | FWER, empirically | Strong, distribution-free |
| **Cluster-extent** | FWER on cluster size | Spatial effects; threshold p ≤ 0.001 |
| **TFCE** | FWER on weighted clusters | The modern default for voxel-wise neuroimaging |

See [Analysis → Multiple comparisons](../../analysis/multiple-comparisons.md) for the depth on each.

## Permutation testing — the safe default

Parametric p-values assume normality, independence, and the right model. Permutation tests assume only that, under the null, labels are exchangeable.

The recipe:

1. Compute the observed test statistic.
2. Randomly permute group labels; recompute the statistic. Repeat 10 000 times.
3. The p-value is the fraction of permuted statistics ≥ the observed.

For neuroimaging GLMs, [PALM](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/PALM) (Winkler et al., 2014) is the canonical tool.

## Effect sizes — always report them

A "significant" p-value with a tiny effect is rarely clinically meaningful. Standard effect-size measures:

- **Cohen's d** — standardised mean difference: $d = (\bar x_1 - \bar x_2) / s_p$.
- **$R^2$ / $\eta^2$** — fraction of variance explained.
- **Odds ratio / risk ratio** — for binary outcomes.

Cohen's conventions: $d \approx 0.2$ small, $0.5$ medium, $0.8$ large. Effect sizes plus confidence intervals beat p-values for communication.

## Power analysis

**Statistical power** = $1 - \beta$ = probability of detecting an effect of a given size with a given sample.

Given a target power (typically 0.8) and effect size, you can solve for the required $n$:

```python
from statsmodels.stats.power import TTestIndPower
analysis = TTestIndPower()
n = analysis.solve_power(effect_size=0.5, alpha=0.05, power=0.8)
print(n)   # ~64 per group
```

Marek et al., 2022 ([doi:10.1038/s41586-022-04492-9](https://doi.org/10.1038/s41586-022-04492-9)) demonstrated that brain-wide-association studies need **thousands** of subjects for reproducible effects. Plan accordingly.

## Bayesian thinking — when priors matter

Bayes's theorem:

$$
p(\theta \mid y) = \frac{p(y \mid \theta)\,p(\theta)}{p(y)}
$$

You update a prior belief about $\theta$ using the likelihood of observed data. In neuroimaging this shows up as:

- **Bayesian model averaging** — averaging over candidate models weighted by evidence.
- **Bayesian fMRI GLM** — SPM's default since ~2005.
- **PyMC / Stan** — general-purpose probabilistic programming.

Bayesian credibility intervals are intuitive (95% credibility = "I believe 95% probability that the true value lies here"); frequentist confidence intervals are *not* the same thing.

## Common pitfalls

- **HARKing** — Hypothesising After the Results are Known. Pre-register.
- **p-hacking** — repeatedly testing until something is significant.
- **Garden of forking paths** — analytical degrees of freedom inflate false-positive rate.
- **Confounding** — site, scanner, age, sex *will* confound your effect unless modelled.
- **Conditioning on a collider** — adjusting for a variable caused by both X and Y creates spurious associations.

[Botvinik-Nezer et al., 2020](https://doi.org/10.1038/s41586-020-2314-9) shows that 70 teams analysing the same data report 70 different conclusions. Discipline matters.

## Reporting checklist

- [ ] Effect size + confidence interval for every test.
- [ ] Multiple-comparison method explicitly named.
- [ ] Random effects (subject, site) modelled.
- [ ] Pre-registered or explicitly exploratory.
- [ ] Code + data available, or a justification for why not.
- [ ] Sensitivity analysis showing the conclusion is robust to reasonable analytic choices.

## References

1. **Gelman A, Carlin JB, Stern HS, Dunson DB, Vehtari A, Rubin DB.** *Bayesian Data Analysis.* 3rd ed. CRC Press; 2013. ISBN 978-1439840955. Free online: [http://www.stat.columbia.edu/~gelman/book/](http://www.stat.columbia.edu/~gelman/book/)
2. **Hastie T, Tibshirani R, Friedman J.** *The Elements of Statistical Learning.* 2nd ed. Springer; 2009. ISBN 978-0387848570. Free online: [https://hastie.su.domains/ElemStatLearn/](https://hastie.su.domains/ElemStatLearn/)
3. **Cohen J.** *Statistical Power Analysis for the Behavioral Sciences.* 2nd ed. Routledge; 1988. ISBN 978-0805802832.
4. **Eklund A, Nichols TE, Knutsson H.** Cluster failure: why fMRI inferences for spatial extent have inflated false-positive rates. *PNAS.* 2016;113(28):7900-7905. [doi:10.1073/pnas.1602413113](https://doi.org/10.1073/pnas.1602413113)
5. **Marek S, Tervo-Clemmens B, Calabro FJ, et al.** Reproducible brain-wide association studies require thousands of individuals. *Nature.* 2022;603:654-660. [doi:10.1038/s41586-022-04492-9](https://doi.org/10.1038/s41586-022-04492-9)
6. **Winkler AM, Ridgway GR, Webster MA, Smith SM, Nichols TE.** Permutation inference for the general linear model. *NeuroImage.* 2014;92:381-397. [doi:10.1016/j.neuroimage.2014.01.060](https://doi.org/10.1016/j.neuroimage.2014.01.060)
7. **Botvinik-Nezer R, Holzmeister F, Camerer CF, et al.** Variability in the analysis of a single neuroimaging dataset by many teams. *Nature.* 2020;582:84-88. [doi:10.1038/s41586-020-2314-9](https://doi.org/10.1038/s41586-020-2314-9)

## Where to next

[Mathematics](mathematics.md) — the linear algebra, calculus, and signal processing under the statistics.
