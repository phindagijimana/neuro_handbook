# Foundation models

> Large pre-trained models, how to fine-tune them on neuroimaging tasks, and when to bother.

A **foundation model** is a model pre-trained on a huge, diverse corpus that you adapt to a specific task with much less data. The neuroimaging community is mid-shift from "train your own U-Net" to "fine-tune a pre-trained encoder", and the next few years will reshape the playbook.

## Why neuroimaging needs them

The 2010s recipe — collect 200 labelled volumes, train a U-Net from scratch — worked for individual tasks but never generalised. Foundation models change the math:

- **Generalisation across sites** improves because pre-training has seen more scanner variation than any one cohort.
- **Sample efficiency improves** — fine-tuning a strong encoder on 50 labels can beat training from scratch on 500.
- **Multimodal capability** — vision encoders connect to text decoders, enabling captioning, retrieval, and reporting.

## The landscape (as of 2026)

| Model family | What it's pre-trained on | Strength |
| --- | --- | --- |
| **MONAI / SwinUNETR pre-trained checkpoints** | Multi-organ CT + MRI | Drop-in encoder for 3D segmentation |
| **MedSAM** | 1M+ segmentation masks | Promptable segmentation, zero-shot or low-shot |
| **BiomedCLIP** | Biomedical image–caption pairs | Image–text retrieval, report alignment |
| **Brain-specific FMs** (BrainFM, BrainGPT-style) | ADNI, UK Biobank, OASIS, etc. | Brain-specific generalisation |
| **General vision encoders** (DINOv2, SAM2) | Natural images | Surprisingly strong feature extractors, but require careful adaptation |

The landscape moves fast. The papers cited will be out of date; the principle — find the largest pre-trained model that's close to your modality, adapt it — is durable.

## When fine-tuning beats training from scratch

Rough rule:

- **N < 100 labelled subjects** → almost certainly fine-tune (or use zero/few-shot).
- **100 < N < 1000** → fine-tune is usually better than training from scratch.
- **N > 1000** → training from scratch is competitive; fine-tuning often still wins on out-of-distribution test sites.

## Fine-tuning techniques

- **Linear probing** — freeze the encoder, train only a final layer. Cheap; baseline you should always run.
- **Full fine-tuning** — backprop through everything. Strongest, most expensive.
- **LoRA / adapters** — insert low-rank update matrices; train ~1% of parameters. Usually within ~1 point of full fine-tuning for far less compute.
- **Prompt-based** (for promptable models like MedSAM) — engineer good prompts (point, bounding box) rather than retraining.

## Multimodal models

Models that combine imaging with text (e.g., RadFM, BiomedCLIP) enable:

- **Captioning** — auto-draft a radiology-style report.
- **Retrieval** — find similar prior cases.
- **Zero-shot classification** — describe what you're looking for in natural language; rank volumes.

For research these are powerful summarisation tools. For anything clinical-decision-adjacent, **never** deploy without rigorous, prospective validation. Hallucination is real.

## Honest warnings

- **Domain gap.** A model pre-trained on adult brain MRI does not magically work on paediatric or rodent brains. Verify on a held-out cohort from your population before believing the numbers.
- **License terms.** Some weights are research-only; some forbid clinical use. Read the license before integrating.
- **Compute.** Fine-tuning a 1B-parameter 3D encoder needs an A100 / H100, not a workstation. Budget accordingly.

## Where to next

[Evaluation pitfalls](evaluation.md) — once the model is trained, how do you know it actually works?
