# Evaluation pitfalls

> The traps that turn a "0.92 Dice" paper into an unreproducible result.

This is the most important chapter in the AI / ML section. Many published neuroimaging-ML results don't replicate; almost all the failures cluster around the issues below.

## 1. Leakage from subject-level splits

A subject's two timepoints, two sessions, or augmented copies must never straddle train and test. Otherwise the model is partly memorising the subject, not learning the task.

**Rules:**

- Split *by subject* (and ideally by site, see #2).
- For longitudinal data: assign each subject to exactly one split.
- For augmentations: generate them *inside* the train loop, never as files that might leak.

A `GroupKFold` keyed on `subject_id` is the minimum. `StratifiedGroupKFold` is better when classes are imbalanced.

## 2. Site / scanner effects [Fortin et al., 2018](https://doi.org/10.1016/j.neuroimage.2017.11.024)[^combat]

A model trained on Siemens 3T data at Site A often falls over on GE 1.5T data at Site B. Site differences (field strength, coil, sequence, vendor) can dwarf biological signal.

**Approaches:**

- **Hold out a whole site as a test set.** This is the only honest measure of cross-site generalisation. Within-site k-fold accuracy can be wildly optimistic.
- **Harmonise with ComBat** [Johnson et al., 2007](https://doi.org/10.1093/biostatistics/kxj037)[^combat_origin]; [Fortin et al., 2018](https://doi.org/10.1016/j.neuroimage.2017.11.024)[^combat] (or its variants: longitudinal ComBat, neuroHarmonize). ComBat models site as a fixed effect on each feature. Powerful for tabular features; trickier for raw volumes.
- **Train on multi-site data.** A model trained on 5 sites usually generalises to a 6th better than a model trained on the largest single site.
- **Domain adaptation / adversarial training** when labels exist on source but not target.

## 3. Metrics — pick the right one and report it honestly

| Task | Metric | Caveat |
| --- | --- | --- |
| Segmentation | Dice, HD95, ASSD, recall, precision | Dice rewards big regions; HD95 catches missed small ones |
| Binary classification | AUROC, AUPR, sensitivity at fixed specificity | AUROC misleads with imbalanced classes; report AUPR too |
| Multi-class | Macro-F1, per-class accuracy | Don't report only weighted average — minority classes hide |
| Regression | MAE, R², calibration plot | R² alone misses systematic bias |

Report all of (a) the metric on the test set, (b) the metric on a held-out site / cohort, (c) per-subject variance, (d) failure cases.

## 4. Calibration

A model that's 90% confident should be right 90% of the time. Deep networks are typically over-confident.

- Plot a **reliability diagram** (predicted probability bin → observed frequency).
- Report **Expected Calibration Error (ECE)**.
- Post-hoc fixes: **temperature scaling** is a one-parameter recipe that fixes most calibration problems for free.

## 5. The "tiny cohort, big claim" trap

`p < 0.05` on n=30 means very little [Marek et al., 2022](https://doi.org/10.1038/s41586-022-04492-9)[^marek]; a single dataset analysed by 70 teams will yield 70 different conclusions [Botvinik-Nezer et al., 2020](https://doi.org/10.1038/s41586-020-2314-9)[^botvinik]. A 2-point Dice improvement on a 50-subject test set means even less. Specific defences:

- **Effect sizes**, not just p-values.
- **Confidence intervals** on every metric — bootstrap is fine, cheap, and honest.
- **Pre-registered analyses** when you can. At minimum, freeze the analysis plan before peeking at the test set.

## 6. Common reporting failures

- "We tuned hyperparameters on the test set." — Sometimes phrased as "we picked the best epoch on the test set." Same thing. Don't.
- "Our model is interpretable because here are some Grad-CAM maps." — Show, don't tell. Quantify.
- "Our method is state-of-the-art." — Compare against the same train/test split as the baseline. Re-run the baseline if needed.
- "We didn't see any failure cases." — Yes you did, and they tell the reader more than the average score.

## A pre-publication checklist

- [ ] Subject-level split, ideally with at least one held-out site.
- [ ] Both training and evaluation code committed and runnable.
- [ ] Performance reported with confidence intervals.
- [ ] At least one failure case shown.
- [ ] Calibration discussed.
- [ ] Documented why this model + dataset is *not* yet ready for clinical use.

If all six are true, you're already in the top decile of published medical-imaging-ML papers.

## References

[^combat]: Fortin J-P, Cullen N, Sheline YI, et al. Harmonization of cortical thickness measurements across scanners and sites. *NeuroImage.* 2018;167:104-120. [doi:10.1016/j.neuroimage.2017.11.024](https://doi.org/10.1016/j.neuroimage.2017.11.024)
[^combat_origin]: Johnson WE, Li C, Rabinovic A. Adjusting batch effects in microarray expression data using empirical Bayes methods. *Biostatistics.* 2007;8(1):118-127. [doi:10.1093/biostatistics/kxj037](https://doi.org/10.1093/biostatistics/kxj037)
[^marek]: Marek S, Tervo-Clemmens B, Calabro FJ, et al. Reproducible brain-wide association studies require thousands of individuals. *Nature.* 2022;603(7902):654-660. [doi:10.1038/s41586-022-04492-9](https://doi.org/10.1038/s41586-022-04492-9)
[^botvinik]: Botvinik-Nezer R, Holzmeister F, Camerer CF, et al. Variability in the analysis of a single neuroimaging dataset by many teams. *Nature.* 2020;582(7810):84-88. [doi:10.1038/s41586-020-2314-9](https://doi.org/10.1038/s41586-020-2314-9)

## Where to next

If you've made it through this section, loop back to the [Data engineering portfolio roadmap](../data-engineering/portfolio-roadmap.md) and read it with new eyes — a good evaluation pipeline is, itself, a data engineering artifact.
