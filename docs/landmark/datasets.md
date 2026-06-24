# Reference datasets

> The public datasets that anchor most modern neuroimaging method development, with full citations and access notes.

## Adult, healthy

| Dataset | Description | Size | Access | Reference |
|---|---|---|---|---|
| **HCP Young Adult** | 3T multimodal, behavioural + genetic | ~1100 | Free + DUA | [Van Essen et al., 2013](https://doi.org/10.1016/j.neuroimage.2013.05.041)[^1] |
| **HCP Lifespan** | Same protocol across age | ~1000+ | Free + DUA | [Bookheimer et al., 2019](https://doi.org/10.1016/j.neuroimage.2018.10.009)[^2] |
| **UK Biobank** | Population-scale multimodal | 100 000+ | Application + fee | [Miller et al., 2016](https://doi.org/10.1038/nn.4393)[^3] |
| **OASIS-3** | Aging, longitudinal | ~1000 | Free + DUA | [LaMontagne et al., 2019](https://doi.org/10.1101/2019.12.13.19014902)[^4] |
| **Cam-CAN** | Lifespan, 18–88 yr | ~700 | Open registration | [Shafto et al., 2014](https://doi.org/10.1186/s12883-014-0204-1)[^5] |
| **MICA-MICs** | High-resolution structural + functional | ~50 | Open | [Royer et al., 2022](https://doi.org/10.1038/s41597-022-01682-y)[^6] |
| **[IXI](https://brain-development.org/ixi-dataset)** | Healthy structural (T1 / T2 / PD / MRA / DWI) | ~600 | Open | Multi-centre, no clinical labels — common ML pretraining cohort. |

## Developmental

| Dataset | Description | Size | Reference |
|---|---|---|---|
| **ABCD** | Adolescent longitudinal, 10-year follow-up | 12 000+ | [Casey et al., 2018](https://doi.org/10.1016/j.dcn.2018.03.001)[^7] |
| **HCP-Development** | 5–21 years | ~1500 | [Somerville et al., 2018](https://doi.org/10.1016/j.neuroimage.2018.04.038)[^8] |
| **dHCP** | Neonatal | ~800 | [Edwards et al., 2022](https://doi.org/10.1016/j.neuroimage.2022.119085)[^9] |
| **[HBCD](https://hbcdstudy.org)** | Healthy Brain and Child Development, birth to age 10 | 7 000+ | Sibling of ABCD covering the earlier age range. |
| **[HBN](https://fcon_1000.projects.nitrc.org/indi/cmi_healthy_brain_network/)** | Healthy Brain Network pediatric (CMI) | 5 000+ | Transdiagnostic pediatric phenotyping. |

## Clinical

| Dataset | Description | Size | Reference |
|---|---|---|---|
| **ADNI** | Alzheimer's longitudinal | ~2000 | [Jack et al., 2008](https://doi.org/10.1002/jmri.21049)[^10] |
| **PPMI** | Parkinson's longitudinal | ~1000+ | [Marek et al., 2011](https://doi.org/10.1016/j.pneurobio.2011.09.005)[^11] |
| **ENIGMA cohorts** | Meta-analytic across disorders | varies | [Thompson et al., 2020](https://doi.org/10.1038/s41398-020-0705-1)[^12] |
| **[ATLAS (stroke)](https://fcon_1000.projects.nitrc.org/indi/retro/atlas.html)** | Lesion-segmented stroke T1w | 1 453 | The reference cohort for stroke segmentation method development. |

## CT-specific datasets

| Dataset | Description | Size | Reference |
|---|---|---|---|
| **[RSNA Intracranial Hemorrhage Detection](https://www.kaggle.com/competitions/rsna-intracranial-hemorrhage-detection)** | Multi-class ICH detection (epidural, subdural, intraparenchymal, intraventricular, subarachnoid) on head CT slices | ~875k slices, ~25k studies | [Flanders 2020, *Radiology AI*](https://doi.org/10.1148/ryai.2020190211); 2019 Kaggle challenge. The de-facto pretraining cohort for any open ICH model. |
| **[CQ500](http://headctstudy.qure.ai/dataset)** | Head CT scans from 491 patients labelled by 3 radiologists for haemorrhage, fracture, mass effect, midline shift | 491 scans (~200 GB) | [Chilamkurthy 2018, *Lancet*](https://doi.org/10.1016/S0140-6736(18)31645-3). Open externally-validated benchmark. |
| **[INSTANCE (Intracranial Haemorrhage Segmentation)](https://instance.grand-challenge.org/)** | MICCAI challenge: ICH segmentation on head CT | 200 cases | [Li 2023, *Computer Methods and Programs in Biomedicine*](https://doi.org/10.1016/j.cmpb.2023.107524). |
| **[ISLES 2018 / 2024](https://www.isles-challenge.org/)** | Stroke lesion segmentation; 2018 + 2024 editions include CT-perfusion and NCCT alongside MRI | varies (~100s) | [Hakim 2024](https://doi.org/10.1038/s41597-023-02828-2); the canonical stroke-segmentation benchmark. |
| **[AISD (Acute Ischemic Stroke Dataset)](https://github.com/GriffinLiang/AISD)** | NCCT + DWI pairs with infarct masks | 397 | Open Chinese acute-stroke cohort; the rare open pairing of acute NCCT with ground-truth DWI infarct. |
| **[Head CT-ICH (PhysioNet)](https://physionet.org/content/ct-ich/1.3.1/)** | Head CT scans with ICH segmentation and clinical metadata | 75 scans | [Hssayeni 2020, *Data*](https://doi.org/10.3390/data5010014). Small but fully open with permissive licence. |
| **[CENTER-TBI Imaging](https://www.center-tbi.eu)** | Multi-site European TBI cohort — CT + MRI + clinical | ~5000 | [Maas 2015](https://doi.org/10.1227/NEU.0000000000000575); imaging arm is governed application. |
| **[TRACK-TBI Imaging](https://tracktbi.ucsf.edu)** | North American TBI cohort — CT + MRI + biomarkers + outcomes | ~3000 | [Yue 2013](https://doi.org/10.1089/neu.2012.2802); CT is the first-line modality on enrolment. |

Most published CT-AI work pretrains on RSNA-ICH (the only open dataset large enough to support modern architectures) and externally validates on CQ500. INSTANCE and ISLES are the segmentation benchmarks.

## Open repositories

- **OpenNeuro** ([portal](https://openneuro.org), [docs](https://docs.openneuro.org)) — open BIDS datasets, versioned, browser + CLI. [Markiewicz et al., 2021](https://doi.org/10.7554/eLife.71774)[^13]. <https://openneuro.org>
- **NeuroVault** ([portal](https://neurovault.org)) — repository for unthresholded statistical maps and atlases. [Gorgolewski et al., 2015](https://doi.org/10.3389/fninf.2015.00008)[^14]. <https://neurovault.org>
- **[NeuroStore](https://neurostore.org)** — 30 000+ studies with pre-extracted activation coordinates; powers Neurosynth Compose meta-analyses.
- **[BrainMap](https://www.brainmap.org)** — coordinate database powering GingerALE; the historical complement to Neurosynth.
- **OpenfMRI** (legacy) — preceded OpenNeuro; most datasets migrated.

## Access patterns

Three tiers:

- **Open** — clone from OpenNeuro [here](https://openneuro.org), no application needed. Start your method development here.
- **Data-use agreement (DUA)** — HCP ([portal](https://www.humanconnectome.org)), OASIS ([portal](https://www.oasis-brains.org)). Sign a form, get credentials, download via AWS S3 or `aws s3 sync`.
- **Application + IRB** — UK Biobank ([portal](https://www.ukbiobank.ac.uk)), ABCD ([portal](https://abcdstudy.org)). Months of paperwork. Worth it for production-scale work.

## Why use a reference dataset

- **Pipeline validation.** If your pipeline produces sensible numbers on HCP, it's probably correct.
- **Generalisation tests.** Train on your cohort, test on HCP, report both.
- **Baseline comparisons.** Most methods papers benchmark on these datasets; you should too.

## Quick-start: how to actually load these

The tables above tell you *what exists*. This section tells you *how to get bytes onto disk and into Python* for the five datasets you'll meet most often. Every one of them has a non-trivial access path; budget weeks, not minutes, for the paperwork on the gated ones.

### 1. HCP Young Adult (1200 subjects)

**Access.** Register on [ConnectomeDB](https://db.humanconnectome.org) and accept the open-access DUA (instant) or restricted DUA (institutional signature; covers family structure, handedness, etc.). Three data variants ship: **unprocessed** (raw DICOMs converted to NIfTI), **minimally-preprocessed** (`HCPpipelines` outputs — surfaces, registrations), **preprocessed** (task GLMs, ICA-FIX-denoised resting-state). Pick the variant *before* you start downloading; they have different S3 prefixes.

**Download.** All three live in the [`hcp-openaccess` requester-pays S3 bucket](https://registry.opendata.aws/hcp-openaccess/). You pay egress; HCP pays storage.

```bash
# Single subject, T1w only, minimally-preprocessed
aws s3 sync \
  s3://hcp-openaccess/HCP_1200/100307/T1w/ \
  ./HCP_1200/100307/T1w/ \
  --request-payer requester

# Whole-cohort manifest first (free listing, then targeted sync)
aws s3 ls s3://hcp-openaccess/HCP_1200/ --request-payer requester > subjects.txt
```

**Python — walk the cohort.**

```python
from pathlib import Path
import pandas as pd

root = Path("HCP_1200")
subjects = sorted(p.name for p in root.iterdir() if p.name.isdigit())

# Behavioural / demographic table ships separately from ConnectomeDB
demo = pd.read_csv("unrestricted_hcp_s1200.csv")  # 1206 rows, ~500 columns
demo = demo.set_index("Subject")
demo.loc[[int(s) for s in subjects], ["Age", "Gender", "PMAT24_A_CR"]].head()
```

**Pitfall.** Requester-pays means *you* pay egress: ~$0.09/GB out of `us-east-1`. The full unprocessed cohort is ~80 TB. Stage compute *inside* `us-east-1` (EC2, AWS Batch) so the bytes never leave the region. See [The cost math](../computing/cloud.md#the-cost-math) for the arithmetic.

### 2. UK Biobank (~40k imaged so far, ~100k planned)

**Access.** Application-only via the [UK Biobank Showcase](https://biobank.ndph.ox.ac.uk). The process is: register an institutional account → submit a scientific-merit application (3-6 months typical) → pay the access fee (tiered by data category) → sign the [Material Transfer Agreement](https://www.ukbiobank.ac.uk/enable-your-research/apply-for-access). Imaging is a sub-cohort; not every approved application includes it.

**Download.** The official tool is [`ukbfetch`](https://biobank.ndph.ox.ac.uk/showcase/help.cgi?cd=accessing_data_guide). It reads a *bulk file* (subject IDs × field IDs) and an auth token.

```bash
# bulk.txt lines look like:  1234567 20252_2_0
ukbfetch -bbulk.txt -aauthfile -ot1     # output prefix "t1"
```

**Python — parse the `.tab` clinical dump.**

```python
import pandas as pd

# UKB .tab files are tab-separated with one column per (field_id, instance, array)
df = pd.read_csv("ukb_main.tab", sep="\t", low_memory=False)
df = df.rename(columns={"f.eid": "eid"})            # subject identifier
df.filter(regex=r"^f\.25756").head()                # all T1 IDP fields
```

For BIDS conversion: [ukb2bids](https://github.com/AndrewBard/ukb2bids) is the community wrapper. The official [UKB Imaging Documentation](https://biobank.ndph.ox.ac.uk/showcase/showcase/docs/brain_mri.pdf) is the canonical reference.

**Pitfall.** Field IDs (`20252` = T1, `20253` = T2 FLAIR, etc.) get renumbered between releases; always re-resolve from the showcase rather than hard-coding. And imaging is a *subset* of the cohort — joining naively on `eid` will silently produce 100k rows where only 40k have scans.

### 3. ADNI (Alzheimer's, ~3000 subjects across ADNI 1/2/3/4)

**Access.** Application + DUA via [ida.loni.usc.edu](https://ida.loni.usc.edu). Faster than UKB (weeks), still gated. Pick the imaging collection (ADNI 1 / GO / 2 / 3 / 4) before applying; merging across phases is non-trivial.

**Download.** The IDA web client supports browser download for small collections; for cohort-scale grabs use the [`adnidata`](https://github.com/nipy/adnidata) Python tool or the [LONI Image Data Archive CLI](https://ida.loni.usc.edu/collaboration/access/appLicense.jsp).

```bash
# Browser pattern: search → add to collection → download as zip
# CLI pattern (adnidata):
adnidata fetch --collection ADNI3 --modality MRI --out ./adni3/
```

**Python — join clinical with imaging.**

```python
import pandas as pd

merge = pd.read_csv("ADNIMERGE.csv")   # the canonical clinical-data table
# RID = Roster ID, the stable subject key across visits and modalities
merge.set_index(["RID", "VISCODE"]).head()

# Cross-reference with imaging via RID
imaging_idx = pd.read_csv("MRILIST.csv")
joined = merge.merge(imaging_idx, on=["RID", "VISCODE"], how="inner")
```

**Pitfall.** ADNI 1 (1.5 T, MP-RAGE) and ADNI 2/3 (3 T, often MP2RAGE) acquire on materially different protocols; sequence parameters also drift mid-phase. Always read the [imaging protocol revision date](https://adni.loni.usc.edu/methods/mri-tool/mri-acquisition/) on each subject's `MRI3META.csv` row before pooling.

### 4. ABCD (adolescent, ~12k subjects)

**Access.** Application via the [NIMH Data Archive (NDA)](https://nda.nih.gov/abcd/). Need an NDA account, an institutional Data Access Request, and an IRB letter. Releases ship annually (3.0, 4.0, **5.0**, ...); pick a release and pin it — the field schemas change between them.

**Download.** Use [`downloadcmd`](https://nda.nih.gov/nda/training-videos.html), NDA's command-line client.

```bash
downloadcmd -dp 1226 -t s3_links.txt   # data package 1226 = an ABCD release
# Outputs land in ~/AbcdDownload/ by default
```

**Python — load BIDS + tabular phenotype.**

```python
from bids import BIDSLayout
import pandas as pd

layout = BIDSLayout("./abcd_bids/", validate=False)   # release is BIDS-compliant
subs = layout.get_subjects()

# Tabular phenotype lives outside BIDS, in NDA's "studies" tables
pheno = pd.read_csv("abcd_lt01.txt", sep="\t", skiprows=[1])
```

The [`pyabcd`](https://github.com/ABCD-STUDY) toolkit wraps common derivative-loading patterns.

**Pitfall.** ABCD 5.0 renamed many derivative fields from 4.0 (`smri_thick_cdk_*` → `mrisdp_*`, for example). Version-pin your analysis (`release == "5.0"`) and use a translation layer if you must cross-version. The [release notes PDFs](https://nda.nih.gov/abcd/abcd-annual-releases) document every rename.

### 5. dHCP (developing, fetal + neonatal, ~800 subjects)

**Access.** Open after [signing the DUA](http://www.developingconnectome.org/data-release/) (email-driven, days). No fee.

**Download.** Hosted on the [GIN data server](https://gin.g-node.org/lana_pena/dHCP/) and managed with [DataLad](https://www.datalad.org/) — the metadata is small and instant; the bytes are pulled on demand.

```bash
datalad clone https://gin.g-node.org/lana_pena/dHCP
cd dHCP
datalad get sub-CC00060XX03/        # pull one subject
datalad get .                       # pull everything (≈1 TB)
```

**Python — DataLad + PyBIDS work together.**

```python
from bids import BIDSLayout

layout = BIDSLayout(".", validate=False)
for img in layout.get(subject="CC00060XX03", suffix="T2w", extension="nii.gz"):
    print(img.path)
```

**Pitfall.** Neonatal brains do *not* register cleanly to adult MNI templates — the cortex hasn't fully myelinated and the ventricles are disproportionate. Use the [dHCP volumetric atlas](https://brain-development.org/brain-atlases/atlases-from-the-dhcp-project/) (40-week template) and the per-week age atlases that ship with the release; the transforms between them and adult MNI are also shipped.

### Which dataset pairs with which chapter

| Dataset | Primary handbook chapter | Why |
|---|---|---|
| HCP Young Adult | [Resting-state analysis](../analysis/resting-state.md) | The dense rs-fMRI protocol is the field's reference for connectomics |
| UK Biobank | [Reliability — BWAS](../analysis/reliability.md) | Sample size large enough to actually run BWAS |
| ADNI | [Alzheimer's and dementia](../clinical/alzheimers-and-dementia.md) | The canonical longitudinal A/T/N cohort |
| ABCD | [Psychiatry](../clinical/psychiatry.md) | The cohort that powers modern adolescent-psychiatry imaging work |
| dHCP | [Paediatric BIDS / neonatal acquisition](../bids/modalities/index.md) | Neonatal protocols, neonatal templates |

## References

[^1]: Van Essen DC, Smith SM, Barch DM, Behrens TEJ, Yacoub E, Ugurbil K. The WU-Minn Human Connectome Project: an overview. *NeuroImage.* 2013;80:62-79.
[^2]: Bookheimer SY, Salat DH, Terpstra M, et al. The Lifespan Human Connectome Project in Aging. *NeuroImage.* 2019;185:335-348.
[^3]: Miller KL, Alfaro-Almagro F, Bangerter NK, et al. Multimodal population brain imaging in the UK Biobank. *Nat Neurosci.* 2016;19(11):1523-1536.
[^4]: LaMontagne PJ, Benzinger TLS, Morris JC, et al. OASIS-3: longitudinal neuroimaging, clinical, and cognitive dataset for normal aging and Alzheimer disease. *medRxiv.* 2019.
[^5]: Shafto MA, Tyler LK, Dixon M, et al. The Cambridge Centre for Ageing and Neuroscience (Cam-CAN) study protocol. *BMC Neurol.* 2014;14:204.
[^6]: Royer J, Rodríguez-Cruces R, Tavakol S, et al. An open MRI dataset for multiscale neuroscience. *Sci Data.* 2022;9:569.
[^7]: Casey BJ, Cannonier T, Conley MI, et al. The Adolescent Brain Cognitive Development (ABCD) study. *Dev Cogn Neurosci.* 2018;32:43-54.
[^8]: Somerville LH, Bookheimer SY, Buckner RL, et al. The Lifespan Human Connectome Project in Development. *NeuroImage.* 2018;183:456-468.
[^9]: Edwards AD, Rueckert D, Smith SM, et al. The Developing Human Connectome Project Neonatal Data Release. *NeuroImage.* 2022;253:119085.
[^10]: Jack CR Jr, Bernstein MA, Fox NC, et al. The Alzheimer's Disease Neuroimaging Initiative (ADNI): MRI methods. *J Magn Reson Imaging.* 2008;27(4):685-691.
[^11]: Marek K, Jennings D, Lasch S, et al. The Parkinson Progression Marker Initiative (PPMI). *Prog Neurobiol.* 2011;95(4):629-635.
[^12]: Thompson PM, Jahanshad N, Ching CRK, et al. ENIGMA and global neuroscience: a decade of large-scale studies. *Transl Psychiatry.* 2020;10:100.
[^13]: Markiewicz CJ, Gorgolewski KJ, Feingold F, et al. The OpenNeuro resource for sharing of neuroscience data. *eLife.* 2021;10:e71774.
[^14]: Gorgolewski KJ, Varoquaux G, Rivera G, et al. NeuroVault.org: a web-based repository for collecting and sharing unthresholded statistical maps of the human brain. *Front Neuroinform.* 2015;9:8.

## Where to next

[Major pipelines](pipelines.md) — the tools that emit the derivatives these datasets ship with.
