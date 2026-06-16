# Glossary

> A working glossary that mixes neuroimaging, statistics, data-engineering, and machine-learning vocabulary because the audience for this handbook lives at that intersection.

Cross-linked into the chapters where each term is treated in depth.

## A

**ACID** — Atomicity, Consistency, Isolation, Durability. The four properties of a transactional database. See [Concurrency](data-engineering/advanced/concurrency.md).

**ADC** — Apparent Diffusion Coefficient. Effective diffusivity of water along an encoding direction in DWI. See [DWI sequence](fundamentals/sequences/dwi.md).

**Affine** — A linear map plus translation; 12 degrees of freedom in 3D. The transformation NIfTI's 4×4 header matrix encodes. See [Coordinate systems](fundamentals/coordinate-systems.md).

**Anisotropy** — Direction-dependent property (e.g. water diffusing more freely along axons than across). Quantified by FA.

**Apptainer** — The HPC-friendly container runtime (formerly Singularity). See [Containers](computing/containers.md).

**Atlas** — A pre-labelled brain volume / mesh used as a reference for parcellation. Examples: Desikan-Killiany, Schaefer, AAL. See [Landmark → Atlases](landmark/atlases.md).

**Atomic write** — A write that either completes fully or appears not to have happened. Pattern: write to `.tmp`, then `mv`. See [Idempotency](data-engineering/five-pillars.md#32-idempotency).

**AT(N) framework** — Amyloid / Tau / Neurodegeneration biomarker schema for Alzheimer's disease. See [Neuroscience](fundamentals/foundations/neuroscience.md).

**Attention** — `softmax(QK^T/√d) V` operation in transformer-style models. See [Mathematics for AI](fundamentals/foundations/mathematics.md#mathematics-for-neuroimaging-ai).

**AUROC / AUPRC** — Area Under the ROC / Precision-Recall Curve. Classifier-discrimination metrics. See [Evaluation pitfalls](ai/evaluation.md).

## B

**Backfill** — Re-processing historical partitions with a new pipeline version. See [Performance & scale](data-engineering/performance.md).

**Backpressure** — Mechanism by which a slow consumer signals an upstream producer to slow down. See [Concepts in depth](data-engineering/concepts.md).

**Backprop** — Backpropagation. The chain rule applied to a computational graph for gradient computation.

**BBR** — Boundary-Based Registration. Refines T1-to-EPI alignment using cortical-WM boundaries (Greve & Fischl 2009).

**b-value** — Strength of diffusion encoding in DWI, units s/mm². Typical: 1000 (DTI), 2000-3000 (HARDI). See [DWI sequence](fundamentals/sequences/dwi.md).

**BIDS** — Brain Imaging Data Structure. A community standard that prescribes folder layout, naming, and JSON sidecars for neuroimaging. See [BIDS toolkit](bids/index.md).

**BIDS app** — A containerised pipeline that accepts a BIDS dataset and writes BIDS-derivatives. See [BIDS-app workflows](landmark/bids-apps.md).

**Bloch equations** — The macroscopic dynamics of nuclear magnetisation under RF + relaxation. The physical model of MRI. See [Medical imaging physics](fundamentals/foundations/physics.md).

**BOLD** — Blood-Oxygen-Level-Dependent signal. The fMRI contrast mechanism. See [Modalities](fundamentals/modalities.md).

**Bonferroni** — Conservative multiple-comparison correction by dividing α by the number of tests. See [Multiple comparisons](analysis/multiple-comparisons.md).

**bval / bvec** — Per-volume DWI metadata: gradient magnitude (s/mm²) and direction unit vector.

## C

**CAP theorem** — In a network partition, you can have Consistency or Availability, not both. See [Distributed systems](data-engineering/advanced/distributed-systems.md).

**Catalyst optimiser** — Spark's SQL query optimiser. See [Spark](data-engineering/advanced/spark.md).

**CDC** — Change Data Capture. Stream of insert/update/delete events from a database. See [Ingestion patterns](data-engineering/advanced/ingestion.md).

**CIFTI** — File format combining cortical surfaces + subcortical volume for HCP-style multi-modal analysis. See [File formats](fundamentals/file-formats.md).

**ComBat** — Empirical-Bayes site harmonisation method (Johnson 2007, Fortin 2018 for neuroimaging). See [Data analysis](fundamentals/foundations/data-analysis.md).

**Compressed sensing** — Reconstruct from under-sampled measurements by enforcing sparsity in a transform domain. See [Reconstruction](fundamentals/medical-imaging/reconstruction.md).

**Connectome** — Region-by-region matrix of structural or functional brain connectivity.

**Container** — Frozen filesystem + binaries that runs identically everywhere. See [Containers](computing/containers.md).

**Convex optimisation** — Optimisation of a function with a unique global minimum; gradient descent works. See [Mathematics](fundamentals/foundations/mathematics.md#optimisation).

**Cortical thickness** — Per-vertex distance between pial and white-matter surfaces, mm. Output of FreeSurfer / FastSurfer.

**CSD** — Constrained Spherical Deconvolution. Multi-shell DWI reconstruction model. See [Diffusion analysis](analysis/diffusion.md).

**CTE** — Chronic Traumatic Encephalopathy. Repetitive-head-impact pathology with tau accumulation.

## D

**DAG** — Directed Acyclic Graph. The fundamental abstraction of every workflow engine. See [The DAG mental model](data-engineering/dag.md).

**DataLad** — Git + git-annex for datasets too large for plain git. See [DataLad versioning](bids/datalad.md).

**dbt** — Data build tool. SQL transformations with version control, tests, lineage. See [dbt deeply](data-engineering/advanced/dbt.md).

**DCM** — DICOM file extension.

**dcm2niix** — Canonical tool for DICOM → NIfTI conversion (Li et al., 2016).

**Default Mode Network (DMN)** — Medial prefrontal + posterior cingulate + angular gyri. Active during rest / self-referential thought.

**Derivatives** — BIDS-Derivatives. Outputs of preprocessing / analysis stored under `derivatives/<app>/` with their own dataset description. See [BIDS → Derivatives layout](bids/derivatives.md).

**DICOM** — Digital Imaging and Communications in Medicine. The clinical interchange format. See [File formats](fundamentals/file-formats.md).

**Diffeomorphism** — A smooth, invertible warp with smooth inverse. The transformation class for non-linear registration. See [Registration](fundamentals/medical-imaging/registration.md).

**Distortion correction** — Removing susceptibility-induced geometric distortion in EPI, typically via field maps + `topup`.

**Dice coefficient** — Segmentation overlap metric, `2|A∩B|/(|A|+|B|)`. See [Segmentation](fundamentals/medical-imaging/segmentation.md).

**DTI** — Diffusion Tensor Imaging. Models DWI signal as a 3×3 symmetric positive-definite tensor per voxel.

**DWI** — Diffusion-Weighted Imaging. MRI sensitised to water diffusion.

## E

**EDA** — Exploratory Data Analysis (Tukey). The "always look at your data first" practice. See [Data analysis](fundamentals/foundations/data-analysis.md).

**EEG** — Electroencephalography. Scalp electric potentials; ms temporal resolution. See [EEG / MEG analysis](analysis/eeg-meg.md).

**EPI** — Echo-Planar Imaging. Fast 2D readout used by BOLD fMRI and DWI.

**ERP / ERF** — Event-Related Potential / Field. Averaged EEG / MEG response time-locked to a stimulus.

**Event sourcing** — Persist events, derive state from them. See [Event-driven architectures](data-engineering/advanced/event-driven.md).

## F

**FA** — Fractional Anisotropy. DTI-derived scalar summarising directional dependence of diffusion, 0 (isotropic) to 1 (perfectly anisotropic).

**FastSurfer** — DL-accelerated drop-in for FreeSurfer `recon-all` (Henschel 2020).

**FBP** — Filtered Back-Projection. Analytic CT reconstruction via the Fourier Slice Theorem.

**FDG** — Fluorodeoxyglucose. Glucose-analogue radiotracer; the dominant clinical PET tracer.

**FDR** — False Discovery Rate. Multiple-comparison correction controlling the expected proportion of false positives. Benjamini-Hochberg is the standard estimator.

**Feast** — Open-source feature store. See [MLOps overlap](data-engineering/advanced/mlops.md).

**fMRI** — Functional MRI. Time-series MRI capturing BOLD signal as a neural-activity proxy.

**fMRIPrep** — The canonical BIDS app for fMRI preprocessing (Esteban et al., 2019).

**Forward model** — `y = Ax + n`. The mapping from tissue property to measurement. See [Acquisition](fundamentals/medical-imaging/acquisition.md).

**FreeSurfer** — Cortical surface reconstruction, parcellation, and morphometry (Fischl 2012).

**fsaverage / fsLR** — Standard surface spaces (FreeSurfer / HCP).

**FSL** — FMRIB Software Library. FLIRT / FNIRT / FEAT / topup / eddy.

**FWE / FWER** — Family-Wise Error / Rate. Probability of at least one false positive across all tests.

## G

**GAN** — Generative Adversarial Network.

**GCN** — Graph Convolutional Network. Generalises convolution to non-Euclidean domains (surfaces, connectomes).

**GIFTI** — XML-based file format for cortical surfaces and per-vertex data.

**GLM** — General Linear Model. Almost every voxel-wise neuroimaging test is a GLM.

**GMM** — Gaussian Mixture Model. Generative model used for tissue segmentation with EM.

**GRAPPA** — Generalised Autocalibrating Partially Parallel Acquisitions. Parallel-imaging reconstruction in k-space (Griswold 2002).

**GRE** — Gradient Echo. MR readout without 180° refocusing; T2* contrast.

**Group K-Fold** — Cross-validation respecting subject / site grouping. See [Classical ML](ai/classical-ml.md).

## H

**HARDI** — High Angular Resolution Diffusion Imaging. DWI with many directions; needed for crossing fibres.

**HCP** — Human Connectome Project. Reference open multimodal cohort.

**HCP-MMP1** — Multi-modal cortical parcellation with 360 regions (Glasser 2016).

**HD95** — 95th-percentile Hausdorff distance; boundary error for segmentation evaluation.

**HeuDiConv** — Heuristic-driven DICOM → BIDS converter.

**HRF** — Hemodynamic Response Function. Impulse response of the BOLD signal.

## I

**ICA** — Independent Component Analysis. Used in EEG / MEG / fMRI for artifact removal.

**Idempotent** — An operation whose effect is the same whether run once or many times. See [The five pillars](data-engineering/five-pillars.md).

**Inverse problem** — Recover unknown `x` from noisy measurements `y`. The mathematical core of reconstruction and source localisation.

**Iceberg** — Apache Iceberg, a modern lakehouse table format. See [Lakehouse internals](data-engineering/advanced/lakehouse.md).

## J

**Jacobian** — Matrix of first partial derivatives. Det(J) gives local volume change; the basis of VBM.

**JLF** — Joint Label Fusion (Wang et al., 2013). Multi-atlas segmentation method.

## K

**Kafka** — Distributed append-only log. The de facto event-streaming substrate. See [Streaming systems](data-engineering/advanced/streaming.md).

**k-space** — Spatial-frequency domain. The MR scanner samples `S(k)`; image is `IFFT{S}`.

**Kappa architecture** — Streaming-only data architecture (vs Lambda's batch + speed layers).

## L

**Lakehouse** — Object-storage-backed analytical platform with ACID guarantees (Iceberg / Delta / Hudi).

**Lambda architecture** — Batch + speed dual-pipeline architecture (Marz).

**LDDMM** — Large Deformation Diffeomorphic Metric Mapping. Time-varying-velocity registration framework (Beg 2005).

**Lineage** — The directed graph "X was produced by job Y consuming A, B, C". See [Catalogs & lineage](data-engineering/advanced/catalogs.md).

**Little's law** — `L = λ × W`. Stable-queue identity. See [Performance](data-engineering/advanced/performance.md).

## M

**MAR / MCAR / MNAR** — Missing At Random / Completely At Random / Not At Random. See [Data analysis](fundamentals/foundations/data-analysis.md).

**Marchenko-Pastur** — Random-matrix distribution used by MP-PCA to estimate the noise floor in DWI.

**MD** — Mean Diffusivity. Trace of the diffusion tensor over 3.

**Medallion architecture** — Bronze (raw) → Silver (cleaned) → Gold (analysis-ready) data layering. See [DWI case study](data-engineering/dwi-case-study.md).

**MEG** — Magnetoencephalography.

**MELD** — Multi-centre Epilepsy Lesion Detection (deep learning on FreeSurfer surfaces).

**MI** — Mutual Information. Multi-modal registration similarity metric.

**MLEM / OSEM** — Maximum-Likelihood Expectation-Maximisation / Ordered-Subsets EM. Iterative PET reconstruction.

**MLOps** — Machine-learning operations. See [MLOps overlap](data-engineering/advanced/mlops.md).

**MNI152** — Population-averaged MRI template space.

**MNE** — Minimum Norm Estimate. EEG / MEG inverse-solution algorithm and the Python package named after it.

**MONAI** — Medical Open Network for AI; PyTorch-based medical-imaging library.

**MPRAGE** — Magnetisation-Prepared Rapid Gradient Echo. T1-weighted structural sequence.

**MP-PCA** — Marchenko-Pastur PCA denoising (Veraart 2016). The DWI noise floor estimator.

**MRIQC** — Automated MRI quality-control BIDS app (Esteban 2017).

**MRtrix3** — DWI reconstruction + tractography toolkit (Tournier 2019).

**Multi-atlas segmentation** — Register N atlases to target, fuse warped labels. Strong on small datasets.

**MVCC** — Multi-Version Concurrency Control. Database concurrency primitive.

## N

**N4ITK** — Iterative bias-field correction (Tustison 2010).

**NBS** — Network-Based Statistic. Connectome group testing with cluster-style correction (Zalesky 2010).

**NIfTI** — Research-imaging file format (`.nii` / `.nii.gz`). Volume + affine + header.

**Nilearn** — Python library for fMRI analysis built on scikit-learn.

**nnU-Net** — Self-configuring 3D segmentation pipeline (Isensee 2021). The baseline to beat.

**Normative model** — Regression of brain measurement on age / sex / site; per-subject z-score against the cohort norm.

**NORDIC** — Noise reduction for fMRI based on Marchenko-Pastur PCA on complex data (Vizioli 2021).

## O

**OpenNeuro** — Public BIDS dataset repository. See [Reference datasets](landmark/datasets.md).

**OSEM** — Ordered-Subsets EM. Accelerated MLEM for PET reconstruction.

**Outbox pattern** — Dual-write fix: write to DB + an outbox table in one transaction; a separate process publishes the outbox. See [Event-driven architectures](data-engineering/advanced/event-driven.md).

## P

**PACELC** — Extension of CAP: in the absence of partitions, choose between Latency and Consistency.

**Parquet** — Columnar file format; the lingua franca of analytics. See [Lakehouse internals](data-engineering/advanced/lakehouse.md).

**Permutation test** — Empirical p-value from re-labelling under the null. Robust to non-normality.

**PET** — Positron Emission Tomography.

**PHI** — Protected Health Information (HIPAA-regulated).

**PII** — Personally Identifiable Information (GDPR / CCPA-regulated).

**PyBIDS** — Python tools for querying BIDS datasets.

## Q

**QSIPrep** — Diffusion-MRI preprocessing BIDS app (Cieslak 2021).

**QSIRecon** — Reconstruction layer on QSIPrep outputs (SS3T-CSD, NODDI, tractography).

**Quorum** — Replication discipline: `reads + writes ≥ replicas + 1`.

## R

**Radon transform** — Line integrals through a 2D function across many angles. The forward model for CT.

**Raft** — Modern consensus algorithm (Ongaro & Ousterhout). Powers etcd, Consul, CockroachDB.

**RAS / LPS** — Right-Anterior-Superior vs Left-Posterior-Superior axis conventions. NIfTI uses RAS; DICOM uses LPS.

**Read-replica** — Async copy of a database for offloading reads.

**Reproducibility** — A colleague can reproduce your result given code + container + data version.

**Resting-state fMRI** — fMRI acquired without an explicit task; basis for functional-connectivity analyses.

**RTO / RPO** — Recovery Time / Point Objective. DR planning. See [Disaster recovery](data-engineering/advanced/disaster-recovery.md).

**Runbook** — Short markdown file per common failure: symptoms, causes, remediation, escalation.

## S

**SAM / MedSAM** — Segment Anything (Kirillov 2023) and its medical-imaging fine-tune (Ma 2024).

**Saga pattern** — Long-lived distributed transaction as a chain of local transactions + compensating actions.

**Schaefer atlas** — Functional cortical parcellation at 100-1000 regions (Schaefer 2018).

**SCD** — Slowly-Changing Dimension. Patterns 1 (overwrite), 2 (history), 3 (previous-value).

**Schema registry** — Centralised store of versioned schemas with compatibility checking. See [Data contracts](data-engineering/advanced/data-contracts.md).

**SENSE** — Sensitivity Encoding (Pruessmann 1999). Image-domain parallel-imaging reconstruction.

**SIFT / SIFT2** — Spherical-deconvolution Informed Filtering of Tractograms. Streamline-weight correction (Smith 2013).

**SLI / SLO / SLA** — Service Level Indicator / Objective / Agreement. See [Reliability](data-engineering/reliability.md).

**Source localisation** — Inverse problem: estimate brain-current sources from EEG / MEG sensors.

**Spark** — Distributed compute engine. See [Spark](data-engineering/advanced/spark.md).

**SPM** — Statistical Parametric Mapping. Long-standing MATLAB toolbox; also the term for thresholded statistical brain maps.

**Snakemake** — File-rule-based DAG workflow engine; native HPC support. Common neuroimaging orchestrator.

**SQL** — Structured Query Language.

**SSIM** — Structural Similarity Index (Wang 2004). Image-quality metric.

**SUV / SUVR** — Standardised Uptake Value / Ratio. PET semi-quantitation.

**Surface-based analysis** — Statistics on a cortical mesh rather than a volume grid.

**SyN** — Symmetric Normalisation (Avants 2008). ANTs' diffeomorphic-registration algorithm.

**Schaefer-Tian** — Pairing of cortical (Schaefer) + subcortical (Tian) parcellations.

## T

**T1 / T2 / T2*** — MR relaxation times. T1 = longitudinal; T2 = transverse (spin-echo); T2* = T2 + static-inhomogeneity dephasing.

**Tau-PET** — PET imaging of tau pathology (e.g. [¹⁸F]flortaucipir).

**TemplateFlow** — Versioned distribution of MRI standard templates (Ciric 2022).

**TFCE** — Threshold-Free Cluster Enhancement (Smith & Nichols 2009). Modern voxel-wise multiple-comparison correction.

**Time-of-flight (PET)** — Detector-timing improvement that localises annihilation along the LOR.

**Tractography** — Estimation of white-matter pathways from DWI through model-derived directions.

**Tract-based spatial statistics (TBSS)** — Skeleton-based group analysis of FA.

**TFCE** — see above.

**Trace** — Distributed-tracing primitive; follows a request across services.

**Transformer** — Attention-based neural architecture.

**TR / TE / TI** — Repetition / Echo / Inversion time. MR-sequence parameters.

## U

**U-Net** — Encoder-decoder CNN with skip connections (Ronneberger 2015). The medical-segmentation default.

**UNETR / Swin UNETR** — Transformer variants of the U-Net for volumetric segmentation.

## V

**VAE** — Variational Autoencoder. Generative + representation-learning model.

**VBM** — Voxel-Based Morphometry. Group analysis of warped Jacobian / GM-density maps.

**Vertex** — A point in a triangle mesh; surface-data equivalent of "voxel".

**Vector store** — ANN-indexed embedding database. See [MLOps overlap](data-engineering/advanced/mlops.md).

**VoxelMorph** — DL-based deformable image registration (Balakrishnan 2019).

**Voxel** — Volume pixel; 3D analogue of a pixel.

## W

**WMH** — White-Matter Hyperintensity. T2/FLAIR-bright lesions in white matter.

**Watermark** — Stream-processing primitive declaring "events with timestamp ≤ W will not arrive late".

**Workflow** — DAG of dependent tasks; what every workflow engine schedules.

## X

**XNAT** — Research-imaging informatics platform.

## Y

**Yeo networks** — 7- and 17-network resting-state parcellation (Yeo 2011).

## Z

**z-score** — Standardised value `(x − μ) / σ`; the canonical normalisation.

---

*This glossary will grow as the handbook does. Open a PR to add or improve a term.*
