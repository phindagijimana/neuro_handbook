# Reference datasets

> The public datasets that anchor most modern neuroimaging method development.

## Adult, healthy

| Dataset | What | Size | Access |
| --- | --- | --- | --- |
| **HCP Young Adult** (1200) | 3 T multimodal, high-quality | ~1100 subjects | Free + DUA |
| **HCP Lifespan** | Same protocol across age | ~1000+ | Free + DUA |
| **UK Biobank** | Population scale, multimodal | 100 000+ | Application + fee |
| **OASIS-3** | Aging, longitudinal | ~1000 | Free + DUA |
| **MICA-MICs** | High-resolution structural | ~50 | Open |

## Developmental

| Dataset | What | Size |
| --- | --- | --- |
| **ABCD** | Adolescent longitudinal | 12 000+ |
| **HCP-Development** | 5–21 years | ~1500 |
| **dHCP** | Neonatal | ~800 |

## Clinical

| Dataset | What | Size |
| --- | --- | --- |
| **ADNI** | Alzheimer's longitudinal | ~2000 |
| **PPMI** | Parkinson's longitudinal | ~1000 |
| **ENIGMA cohorts** | Meta-analytic across disorders | varies |

## Open repositories

- **OpenNeuro** (<https://openneuro.org>) — open BIDS datasets, mostly task fMRI and structural. Versioned. Often the easiest place to test a pipeline.
- **NeuroVault** (<https://neurovault.org>) — derived statistical maps, not raw data.
- **The Cambridge Centre for Ageing and Neuroscience (Cam-CAN)** — 700+ subjects, lifespan.

## Access patterns

Three tiers:

- **Open** — clone from OpenNeuro, no application needed. Start your method development here.
- **Data-use agreement (DUA)** — HCP, OASIS. Sign a form, get credentials, download.
- **Application + IRB** — UK Biobank, ABCD. Months of paperwork. Worth it for production-scale work.

## Why use a reference dataset

- **Pipeline validation.** If your pipeline produces sensible numbers on HCP, it's probably correct. If it doesn't, the dataset isn't the problem.
- **Generalisation tests.** Train on your cohort, test on HCP, report both.
- **Baseline comparisons.** Most methods papers benchmark on these datasets; you should too.

## Where to next

[Major pipelines](pipelines.md) — the tools that emit the derivatives these datasets ship with.
