# Tools landscape

> Opinionated map of the tools you'll meet — what they do and when to reach for each, with **official documentation links** so you can jump straight to the source.

This page is a quick index organised by what the tool *does* rather than where it sits in the stack. Each row links to the canonical documentation and (where one exists) to a deeper treatment elsewhere in the handbook.

!!! note "How to read this section"
    Tables on this page are the **catalogue** — names, one-liners, and when-to-pick notes. The companion pages turn that catalogue into decisions:

    - **[Decision trees](decision-trees.md)** — flowcharts for the five choices that bite teams hardest (orchestrator, storage, DICOM converter, preprocessing pipeline, DL framework).
    - **[Visualisation and EDA](viz-and-eda.md)** — viewers, plotting libraries, and QC dashboards, with opinions on when to reach for each.
    - **[Clinical deployment](clinical-deployment.md)** — DICOM I/O, PACS bridges, inference servers, and the regulatory wrappers around them.

    If you're new to the stack, skim the tables here first, then jump to the decision-tree page for the calls you actually have to make this week.

## Neuroimaging-specific

The neuroimaging-specific tools are mostly **non-substitutable** — they encode domain knowledge (BIDS layout, surface topology, diffusion modeling) that generic tools don't have. The real choices are between a few canonical options per task:

- **DICOM → NIfTI:** `dcm2niix` is the engine; `HeuDiConv` and `Dcm2Bids` are the BIDS-layout wrappers on top. Pick by team size and how stable your scan protocol is — see [Decision trees → Which DICOM converter?](decision-trees.md#which-dicom-converter).
- **Cortical surfaces:** FreeSurfer is the citation-weighted default; FastSurfer is the deep-learning drop-in when you have GPUs and need throughput.
- **Preprocessing:** BIDS apps (fMRIPrep, QSIPrep, sMRIPrep) are the path of least resistance and the right default. Roll your own only when you have a specific reason — see [Decision trees → Which preprocessing pipeline?](decision-trees.md#which-preprocessing-pipeline).

| Tool | What it does | Notes |
| --- | --- | --- |
| **dcm2niix** | DICOM → NIfTI conversion | The de-facto standard; embeds BIDS-friendly sidecars. |
| **HeuDiConv / Dcm2Bids** | Build a BIDS dataset from DICOM | Heuristic-driven; pick HeuDiConv for institutional repeatability, Dcm2Bids for one-off conversions. |
| **BIDS Validator** | Check a dataset against the BIDS spec | Run before *any* pipeline. |
| **FreeSurfer** (`recon-all`) | Cortical surface reconstruction, parcellations | Slow (≈10 h / subject); FastSurfer is the DL-accelerated drop-in. |
| **fMRIPrep / QSIPrep / sMRIPrep** | BIDS-app preprocessing | Standardised, container-shipped; outputs are reusable across downstream analyses. |
| **MRtrix3** | Diffusion modeling, tractography | Workhorse for DWI streamlines and FOD-based methods. |
| **ANTs / FSL / AFNI** | Registration, segmentation, fMRI stats | Mature, well-cited, slower-moving. |
| **Nilearn** | Python analytics on NIfTI / Niimg | Best Python entry point if you're coming from scikit-learn. |
| **PyBIDS** | Programmatic BIDS access | Use it instead of writing glob patterns. |
| **TemplateFlow** | Versioned standard templates | Pin versions in your pipeline. |

## Harmonization

Multi-site studies pay a hidden tax in scanner / site effects. The ComBat family of tools removes them post-hoc on derived features; deep-learning approaches go one step earlier and harmonise the images themselves. Pick by where in your pipeline you can intervene.

| Tool | What it does | Notes |
| --- | --- | --- |
| **[neuroCombat](https://github.com/Jfortin1/neuroCombat)** | ComBat in Python, removes scanner/site batch effects | The default first call on multi-site cortical thickness, FA, volumes. |
| **[neuroCombat (R)](https://github.com/Jfortin1/neuroCombat_Rpackage)** | Same in R | When your downstream stats are in R. |
| **[neuroHarmonize](https://github.com/rpomponio/neuroHarmonize)** | GAM-based nonlinear covariate modelling | When age / clinical scores enter the harmonisation model nonlinearly. |
| **[ComBatFamily](https://github.com/andy1764/ComBatFamily)** | Unified R wrapper for ComBat variants | One API across ComBat / CovBat / longComBat. |
| **[longCombat](https://github.com/jcbeer/longCombat)** | Longitudinal ComBat with subject random effects | Use it on within-subject longitudinal data; vanilla ComBat is misspecified. |
| **[CovBat](https://github.com/andy1764/CovBat_Harmonization)** | Covariance harmonisation | When site affects between-feature covariance, not just means. |
| **[dMRIharmonization](https://github.com/pnlbwh/dMRIharmonization)** | Diffusion harmonisation via RISH features | The right answer for cross-site DWI before tractography. |
| **[HACA3](https://github.com/lianruizuo/haca3)** | Deep-learning harmonisation with disentangled reps | Image-level harmonisation when feature-level ComBat isn't enough. |
| **[Harmonizer](https://github.com/Imaging-AI-for-Health-virtual-lab/harmonizer)** | scikit-learn-style transformer wrapping multiple harmonisation methods | Reach for it when you want pipeline-compatible objects you can slot into a `Pipeline` next to your downstream model. |
| **[RISH-GLM](https://github.com/delucaal/RISH-GLM)** | RISH-feature-based dMRI harmonisation without matched-subject training | The right call for cross-site DWI when you can't acquire travelling-subject data. |

## Lesion and WMH segmentation

For white-matter hyperintensities, MS lesions, and small-vessel disease, no single tool wins — performance depends on field strength, slice thickness, and lesion size. Most labs ensemble two.

| Tool | What it does | Notes |
| --- | --- | --- |
| **[LST](https://www.applied-statistics.de/lst.html)** | SPM toolbox for MS lesions | The long-standing default; LPA and LGA algorithms. |
| **[LST-AI](https://github.com/CompImg/LST-AI)** | Deep-learning ensemble for MS lesions | The modern successor; ensemble of UNets. |
| **[SHIVA-WMH](https://github.com/pboutinaud/SHIVA_WMH)** | 3D U-Net for small punctate WMH | Calibrated to catch small lesions other tools miss. |
| **[TrUE-Net](https://github.com/v-sundaresan/truenet)** | Triplanar ensemble for WMH | FSL-friendly; trained on multi-protocol data. |
| **[HyperMapp3r](https://github.com/AICONSlab/HyperMapp3r)** | Bayesian CNN with uncertainty | Outputs per-voxel uncertainty — useful for triage. |
| **[DeepWMH](https://github.com/lchdl/DeepWMH)** | Annotation-free training | Reach for it when you have no labelled WMH cohort. |
| **[wmh_seg](https://github.com/jinghangli98/wmh_seg)** | Transformer U-Net, multi-field-strength | Robust to 1.5T / 3T mixed cohorts. |
| **[segcsvd](https://github.com/AICONSlab/segcsvd)** | CSVD: WM + perivascular spaces | For cerebral small-vessel disease beyond WMH alone. |
| **[UBO Detector](https://github.com/cheba-nil/CNS)** | Automated WMH pipeline with regional quantification | End-to-end; produces lobar quantification tables. |

## Diffusion — extended

The diffusion stack already lists MRtrix3 above. The additions below cover tractography, automated bundle definition, and skeleton-based stats — most of which slot in after QSIPrep / QSIRecon. See [Landmark → Major pipelines](../landmark/pipelines.md) for the canonical reconstruction stack.

| Tool | What it does | Notes |
| --- | --- | --- |
| **[DSI Studio](https://github.com/frankyeh/DSI-Studio)** | Deterministic tractography, connectometry | GUI-friendly; strong connectometry workflow. |
| **[TractSeg](https://github.com/MIC-DKFZ/TractSeg)** | DL tract segmentation | The standard fast way to extract 72 named bundles. |
| **[TBSS](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/TBSS)** | Voxelwise FA-skeleton stats | The historical default for voxelwise DTI stats; cite even when you replace it. |
| **[Tracula](https://surfer.nmr.mgh.harvard.edu/fswiki/Tracula)** | Automated probabilistic tractography | FreeSurfer-integrated; uses anatomical priors. |
| **[XTRACT](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/XTRACT)** | Automated WM bundle protocols | FSL's bundle-protocol library; pairs with `probtrackx`. |

## Connectivity

Functional connectivity has its own post-processing layer between fMRIPrep and group analysis — denoising, parcellation, network construction, and gradient decomposition.

| Tool | What it does | Notes |
| --- | --- | --- |
| **[XCP-D](https://github.com/PennLINC/xcp_d)** | Post-processing for FC with denoising | The right call on top of fMRIPrep / NiBabies outputs. |
| **[CONN](https://web.conn-toolbox.org)** | MATLAB toolbox; seed/ROI/ICA | The historical FC default; still widely used. |
| **[BrainSpace](https://github.com/MICA-MNI/BrainSpace)** | Gradient decomposition / manifold learning | The diffusion-embedding / gradients workflow. |
| **[nibetaseries](https://github.com/HBClab/NiBetaSeries)** | Beta series for task-FC | Use it to turn task GLM betas into trial-level FC matrices. |

## Statistical analysis

Mass-univariate, meta-analysis, and harmonisation diagnostics all live here. Many of these tools assume your derivatives are already in standard space.

| Tool | What it does | Notes |
| --- | --- | --- |
| **[Fitlins](https://github.com/poldracklab/fitlins)** | First-level fMRI estimation from BIDS Stats Models | The reproducible way to spec a GLM in BIDS. |
| **[NiMARE](https://github.com/neurostuff/NiMARE)** | Coordinate + image meta-analysis | Python-native ALE / MKDA / IBMA workflows. |
| **[ENIGMA Toolbox](https://github.com/MICA-MNI/ENIGMA)** | Python/MATLAB, 80+ datasets with connectomics | Hook your derivatives into ENIGMA reference cohorts. |
| **[ENIGMA VBM](https://sites.google.com/view/enigmavbm)** | Automated DARTEL VBM | Reproducible VBM in the ENIGMA harmonised pipeline. |
| **[Neuromaps](https://github.com/netneurolab/neuromaps)** | Brain annotation vs receptor/transcriptomic atlases | The spatial-correlation toolbox; pairs with BrainSMASH. |
| **[BrainSMASH](https://github.com/murraylab/brainsmash)** | Spatially-autocorrelated null surrogates | The right null model when comparing brain maps; do not use random shuffles. |
| **[PALM](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/PALM)** | Permutation, TFCE, complex designs | The FSL permutation toolbox; covers designs `randomise` won't. |
| **[SnPM](https://github.com/SnPM-toolbox/SnPM-devel)** | Nonparametric SPM | SPM-native permutation inference. |
| **[Neurosynth Compose](https://compose.neurosynth.org)** | Web meta-analysis platform | Cloud-hosted, no install; the modern Neurosynth front-end. |
| **[GingerALE](https://www.brainmap.org/ale)** | ALE coordinate-based meta-analysis | The reference ALE implementation. |
| **[SDM-PSI](https://www.sdmproject.com)** | Hybrid coordinate + image meta-analysis | When you have a mix of maps and peaks. |
| **[IBMMA](https://github.com/sundelinustc/IBMMA)** | Image-based multi-site mass-univariate | For pooled image-based meta-analysis across sites. |
| **[DHARM](https://jake-turnbull.github.io/HarmonisationDiagnostics/)** | Harmonisation algorithm diagnostics | Sanity-check your ComBat / harmonisation before trusting downstream stats. |

## QC — extended

[MRIQC](https://mriqc.readthedocs.io) covers per-subject image quality; the page on [Visualisation and EDA](viz-and-eda.md) covers viewers and dashboards. One additional protocol-level QC tool deserves a callout:

| Tool | What it does | Notes |
| --- | --- | --- |
| **[mrQA](https://github.com/Open-Minds-Lab/mrQA)** | Protocol-compliance verification (acq-parameter drift) | Catches silent protocol drift across subjects / sessions before it contaminates analyses. |

## General-purpose imaging libraries and platforms

Outside the neuroimaging-specific stack, a handful of generic medical-image libraries underpin essentially everything — registration kernels, segmentation primitives, visualisation, and interactive editing.

| Tool | What it does | Notes |
| --- | --- | --- |
| **[ITK](https://itk.org/)** | Segmentation + registration C++ core | The substrate ANTs / Slicer / SimpleITK ride on. |
| **[SimpleITK](http://www.simpleitk.org/)** | Python wrapper around ITK | Reach for it when you need ITK from a notebook or pipeline. |
| **[VTK](https://www.vtk.org/)** | Visualisation toolkit | The substrate Slicer's rendering rides on. |
| **[3D Slicer](https://www.slicer.org/)** | Open platform for medical-image computing | The standard for interactive segmentation, registration, and DICOM workflows. |
| **[NiftyReg](http://cmictig.cs.ucl.ac.uk/wiki/index.php/NiftyReg)** | Non-ANTs registration option | Lighter, faster registration when ANTs is overkill. |

## Preprocessing — extended

Beyond the canonical BIDS apps already listed above, several more pipelines fill in modalities, populations, and quality-of-life gaps. Most ship as containers and slot in next to fMRIPrep / QSIPrep / sMRIPrep.

| Tool | What it does | Notes |
| --- | --- | --- |
| **[dMRIPrep](https://github.com/nipreps/dmriprep)** | DWI preprocessing in the nipreps family | Use it instead of rolling your own susceptibility / eddy / motion stack. |
| **[Nibabies](https://github.com/nipreps/nibabies)** | Infant fMRIPrep | Right answer when the cohort is neonatal / under-2y and fMRIPrep's adult priors fail. |
| **[HALFpipe](https://github.com/HALFpipe/HALFpipe)** | Containerised fMRI with interactive QA | Reach for it when you want fMRIPrep-style robustness plus a UI for review. |
| **[C-PAC](https://github.com/FCP-INDI/C-PAC)** | Configurable connectivity-analysis pipeline | The older, more customisable cousin of fMRIPrep; preferred by some FC labs. |
| **[ASLPrep](https://github.com/PennLINC/aslprep)** | ASL preprocessing → CBF | The BIDS app for perfusion; outputs CBF maps + QC. |
| **[Mindboggle](https://github.com/nipy/mindboggle)** | Automated morphometry from surfaces | FreeSurfer-compatible shape and labelling features. |
| **[Nighres](https://github.com/nighres/nighres)** | 7T high-res / laminar processing | When your cohort is 7T or you need cortical layers. |
| **[fMRIDenoise](https://github.com/compneuro-ncu/fmridenoise)** | Benchmark denoising strategies | Compare aCompCor / AROMA / scrubbing strategies systematically before committing. |
| **[LayNii](https://github.com/layerfMRI/LayNii)** | Layer-fMRI / VASO analysis | The de-facto toolkit for laminar BOLD / VASO analyses. |
| **[CAT12](https://neuro-jena.github.io/cat)** | SPM voxel/surface morphometry | The standard SPM-based VBM extension. |
| **[AFNI](https://afni.nimh.nih.gov)** | fMRI preprocessing + stats suite | Independent stack with first-class `afni_proc.py` script generation. |
| **[Tedana](https://github.com/ME-ICA/tedana)** | Multi-echo denoising | The right denoiser if you acquired multi-echo BOLD. |
| **[SynthStrip](https://surfer.nmr.mgh.harvard.edu/docs/synthstrip)** | DL skull-stripping | Contrast-agnostic; often replaces BET / `mri_synthstrip` calls. |
| **[SynthSeg](https://github.com/BBillot/SynthSeg)** | Contrast-agnostic brain segmentation | Works across modalities/protocols without retraining. |
| **[Templateflow](https://github.com/templateflow/templateflow)** | Versioned templates/atlases | The store the nipreps tools pull MNI / fsLR templates from. |

## Workflow orchestrators

Orchestrators differ along three axes: **how they model a job** (file targets vs channels vs assets), **how they scale** (HPC scheduler vs Kubernetes vs managed cloud), and **what they assume about your team** (Python-only vs polyglot, scientific vs warehouse). For a neuroimaging lab on Slurm with mostly Python tools, the default is Snakemake. For a translational team that already runs Nextflow on bioinformatics pipelines, keep using it. The full decision lives in [Decision trees → Which orchestrator?](decision-trees.md#which-orchestrator-for-my-lab).

| Tool | Strength | When to pick |
| --- | --- | --- |
| **Snakemake** | File-target rules; native HPC integration | Best fit for neuroimaging on Slurm. |
| **Nextflow** | Containerised, channel-based; massive bioinformatics adoption | When your team already uses it. |
| **Airflow** | Time-based scheduling; huge ecosystem | Tabular / warehouse-centric pipelines. |
| **Dagster** | Asset-based mental model; strong typing | Modern data platforms, software-defined assets. |
| **Prefect** | Pythonic; flexible deployment | Lighter weight than Airflow. |
| **Argo Workflows** | Kubernetes-native | When the rest of the stack is on K8s. |
| **[Nipype](https://github.com/nipy/nipype)** | Pipeline framework wrapping FSL / AFNI / FreeSurfer / SPM | The substrate fMRIPrep is built on; still the right answer when stitching legacy CLIs. |
| **[Pydra](https://github.com/nipype/pydra)** | Next-gen dataflow engine (Nipype successor) | Use it for new nipreps-style work; cleaner semantics than Nipype. |
| **[Nipoppy](https://github.com/nipoppy/nipoppy)** | Full raw→derivatives workflow management | Opinionated multi-pipeline orchestration with BIDS conventions baked in. |

### Platforms — when you don't want to host the orchestrator yourself

| Platform | What | When to reach for it |
| --- | --- | --- |
| **[Brainlife.io](https://brainlife.io)** | Cloud platform for containerised pipelines | Run shared apps without provisioning compute. |
| **[Neurodesk](https://github.com/NeuroDesk/neurodesktop)** | Containerised desktop, 100+ tools in browser | Teaching, demos, and ad-hoc analyses without local installs. |
| **[Clinica](https://aramislab.paris.inria.fr/clinica/docs/public/latest)** | Clinical study pipelines | Cohort-style clinical neuroimaging studies with built-in stat layers. |
| **[QuNex](https://qunex.yale.edu)** | HCP-style processing at scale | Reach for it when you want the HCP minimal-preprocessing stack on your own data. |

## Storage layers

Storage choices follow data volume and access pattern, not preference. POSIX is fastest within a node and miserable across one; object storage is the inverse. Lakehouse table formats sit on top of object stores to give you ACID and time travel without the warehouse price tag. For neuroimaging specifically, DataLad is the only tool that treats *datasets* as first-class versioned objects rather than blobs to back up. See [Decision trees → Which storage layer?](decision-trees.md#which-storage-layer) for the full call.

| Tool | What | Notes |
| --- | --- | --- |
| **POSIX filesystem** | Plain files | What HPC clusters give you. Fast within a node, painful across. |
| **S3 / GCS / Azure Blob** | Object storage | Cloud default; cheap at rest, network-egress costs bite. |
| **Parquet** | Columnar file format | The lingua franca of analytical data. |
| **Iceberg / Delta / Hudi** | Table formats on top of Parquet | ACID transactions, time-travel, schema evolution. See [Lakehouse internals](../data-engineering/advanced/lakehouse.md). |
| **DataLad** | Git-annex for datasets | The neuroimaging-native versioning answer. |
| **DICOM PACS** | Clinical image archives | Where data starts; rarely where it lives during research. |

## Analytics & transformation

For cohort-scale tabular work (subjects, sessions, derived metrics), the modern Python default is **DuckDB + Polars**: in-process, columnar, fast on a laptop, and they speak Parquet natively. Reach for Spark only when the data genuinely does not fit on one machine — which for neuroimaging derivatives is rarer than people assume. dbt earns its keep when SQL transformations need version control, tests, and lineage; see [dbt deeply](../data-engineering/advanced/dbt.md).

| Tool | When |
| --- | --- |
| **DuckDB** | In-process SQL on Parquet / CSV. Excellent for cohort summaries. |
| **Polars** | Fast single-node DataFrames. |
| **Pandas** | Familiar, ubiquitous, slower at scale. |
| **Spark / PySpark** | When the data doesn't fit on one machine. See [Spark](../data-engineering/advanced/spark.md). |
| **dbt** | SQL transformations with version control, tests, lineage. See [dbt](../data-engineering/advanced/dbt.md). |

## Visualisation & EDA

Volume viewers, surface viewers, programmatic plotting, and QC dashboards each have a clear best-in-class for the common cases. The pairing most labs settle on is **ITK-SNAP** for quick volumetric edits, **Connectome Workbench** for surfaces, **Nilearn plotting** in notebooks, and **MRIQC** for cohort-scale QC. See [Visualisation and EDA](viz-and-eda.md) for the full breakdown.

## Clinical deployment

Once a model leaves the lab, the tool list changes: DICOM libraries, PACS bridges, inference servers, FHIR for orders/results, and DICOM SR for structured outputs. Most of these are commercial-adjacent — pick the open option that matches your regulatory posture. See [Clinical deployment](clinical-deployment.md).

## Experiment tracking & MLOps

Once you're training models the catalogue of tools you actually need is small. The split between **experiment tracking** (per-run metrics, artifacts, configs) and **model registry / serving** (versioned models, deployment) is where most teams either pick a single platform or stitch two together.

| Tool | What it does | Notes |
| --- | --- | --- |
| **Weights & Biases** | Tracking + sweeps + reports | Best UX; SaaS by default, self-host available |
| **MLflow** | Tracking + registry + serving | The open-source default; runs anywhere |
| **TensorBoard** | Local metrics + tensor visualisations | Use alongside W&B / MLflow, not instead |
| **DVC** | Data + model versioning on git | Pairs with DataLad-style provenance |
| **Hugging Face Hub** | Model + dataset hosting + cards | Increasingly used for foundation-model checkpoints |

See [Data engineering → MLOps](../data-engineering/advanced/mlops.md) for how these fit into a production stack.

## Observability

Observability is the part that's almost identical to a generic data platform. Lift these patterns from industry rather than inventing them.

| Layer | Tool |
| --- | --- |
| Logs | Loki, ELK, Datadog Logs |
| Metrics | Prometheus + Grafana, Datadog |
| Traces | OpenTelemetry, Jaeger, Tempo |
| Lineage | OpenLineage + Marquez, DataHub, Atlan |
| Data quality | Great Expectations, Pandera, Soda |

---

## Further catalogues

This page is opinionated and incomplete by design. When the tool you need isn't here, these community catalogues will almost certainly have it.

- [openmritools.com](https://openmritools.com/) — a much larger, MRI-specific tool catalogue maintained by the community. Used as a source for many entries on this page.
- [awesome-medical-imaging](https://github.com/fepegar/awesome-medical-imaging) — general medical-imaging awesome list curated by Fernando Pérez-García.
- [MR-Hub](https://ismrm.github.io/mrhub) — ISMRM-maintained directory of MRI reconstruction software.
- [NITRC](https://www.nitrc.org) — searchable registry of analysis tools and computational resources.
- [NeuroStars](https://neurostars.org) — Q&A forum for neuroimaging methods and tool support.
- [NeuroBagel](https://github.com/neurobagel) — federated search across annotated neuroimaging datasets.

## References

1. **Gorgolewski KJ, Auer T, Calhoun VD, et al.** The brain imaging data structure (BIDS). *Sci Data.* 2016;3:160044. [doi:10.1038/sdata.2016.44](https://doi.org/10.1038/sdata.2016.44)
2. **Esteban O, Markiewicz CJ, Blair RW, et al.** fMRIPrep: a robust preprocessing pipeline for functional MRI. *Nat Methods.* 2019;16:111-116. [doi:10.1038/s41592-018-0235-4](https://doi.org/10.1038/s41592-018-0235-4)
3. **Halchenko YO, Goncalves M, Castello MVD, et al.** HeuDiConv — flexible DICOM conversion into structured directory layouts. *J Open Source Softw.* 2024. [doi:10.21105/joss.05839](https://doi.org/10.21105/joss.05839)
4. **Mölder F, Jablonski KP, Letcher B, et al.** Sustainable data analysis with Snakemake. *F1000Res.* 2021;10:33. [doi:10.12688/f1000research.29032.2](https://doi.org/10.12688/f1000research.29032.2)
5. **Di Tommaso P, Chatzou M, Floden EW, et al.** Nextflow enables reproducible computational workflows. *Nat Biotechnol.* 2017;35:316-319. [doi:10.1038/nbt.3820](https://doi.org/10.1038/nbt.3820)

## Where to next

- [Decision trees](decision-trees.md) — flowcharts for the choices teams agonise over.
- [Visualisation and EDA](viz-and-eda.md) — viewers, plotting, and QC dashboards.
- [Clinical deployment](clinical-deployment.md) — moving models from notebooks to scanners.

This is a starting map, not an exhaustive catalogue. Tools change; the *categories* don't.
