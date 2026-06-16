# AI / ML for neuroimaging

> What machine learning on brain data actually looks like.

This section assumes you can write training loops in PyTorch (or are willing to learn). It focuses on the parts of ML that are *specific* to neuroimaging — the parts that bite teams who arrive from generic computer vision or NLP.

## Chapters

- **[Classical ML on volumetrics](classical-ml.md)** — when you don't need deep learning. Feature engineering on volumes, surfaces, and connectomes; linear models, SVMs, gradient-boosted trees; sample-size reality checks.
- **[Deep learning for imaging](deep-learning.md)** — 2D vs 2.5D vs 3D convolutional architectures, U-Nets for segmentation, ViTs and Swin variants for volumes, training tricks that matter (patch sampling, class imbalance, augmentation in 3D).
- **[Foundation models](foundation-models.md)** — the landscape of large pre-trained models for medical imaging, what's actually available, when fine-tuning beats training from scratch, multimodal models that combine imaging with text or genomics.
- **[Evaluation pitfalls](evaluation.md)** — leakage from subject-level splits, site/scanner effects (ComBat and friends), reporting Dice/HD95/AUROC honestly, calibration, and the "p<0.05 on tiny cohorts" trap.

## Why this is separate from generic ML

Three reasons neuroimaging ML is different enough to warrant its own section:

1. **The data is 3D or 4D and small.** A medical dataset is typically hundreds to low-thousands of subjects, not millions of images. Most of your engineering effort goes into *not* overfitting.
2. **Site and scanner effects dominate noise.** A model that "works" on Site A often falls over on Site B because of magnetic-field strength, coil, sequence, or vendor differences. Harmonisation is a first-class concern.
3. **Clinical context shapes what good means.** A 0.85 Dice that misses a small lesion is worse than a 0.80 Dice that catches it. Metrics that ignore failure modes are misleading.

Everything in this section is written with those three constraints in mind.
