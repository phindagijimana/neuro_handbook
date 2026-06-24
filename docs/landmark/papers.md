# Foundational papers

> Bibliographies are flat. Reading lists shouldn't be. Below: six **reading roadmaps** — each a 6-10 paper sequence with a one-sentence reason per entry — followed by the full alphabetical paper index for reference lookups.

Citations use the AMA-style author list, year, journal, and a clickable DOI link.

## Reading roadmaps by goal

Each roadmap is a deliberate ordering: each paper assumes what you read in the previous step. Don't shuffle — the punchlines stack.

### Roadmap 1 — "I want to understand *why* fMRIPrep preprocesses the way it does"

**For:** the methods-curious fMRI user who has run `fmriprep` and wants to know what every flag is defending against. ~8 papers, one long evening.

1. [Ogawa et al., 1990](https://doi.org/10.1073/pnas.87.24.9868) — the original BOLD-contrast paper; everything downstream is a correction on what this measures.
2. [Kwong et al., 1992](https://doi.org/10.1073/pnas.89.12.5675) — first human BOLD-fMRI; establishes the workflow shape.
3. [Friston et al., 1995](https://doi.org/10.1002/hbm.460020402) — the GLM applied to fMRI; the inferential layer every preprocessing decision serves.
4. [Worsley & Friston, 1995](https://doi.org/10.1006/nimg.1995.1023) — temporal autocorrelation correction; why fMRIPrep produces a confounds table.
5. [Power et al., 2012](https://doi.org/10.1016/j.neuroimage.2011.10.018) — motion scrubbing; why `framewise_displacement` is the most important number in the confounds CSV.
6. [Esteban et al., 2019](https://doi.org/10.1038/s41592-018-0235-4) — fMRIPrep itself; the synthesis of every prior lesson into one BIDS-app.
7. [Eklund et al., 2016](https://doi.org/10.1073/pnas.1602413113) — the cluster-failure paper; why fMRIPrep + permutation testing replaced fMRIPrep + parametric voxel-wise inference.
8. [Nichols et al., 2017](https://doi.org/10.1038/nn.4500) — COBIDAS; the community reporting standard that fMRIPrep's HTML report was built to satisfy.

### Roadmap 2 — "I want to do credible diffusion analysis on my cohort"

**For:** a postdoc or PhD student about to run a DWI study who has never written down what each preprocessing step corrects. ~9 papers.

1. [Stejskal & Tanner, 1965](https://doi.org/10.1063/1.1695690) — the pulsed-gradient sequence; the physics every DWI scan is implementing.
2. [Basser et al., 1994](https://doi.org/10.1016/S0006-3495(94)80775-1) — the diffusion tensor; FA / MD / AD / RD all live in this paper.
3. [Tuch, 2002](https://www.proquest.com/openview/c2d7ec1cd3f08bd1d1b9bb83960e9b21/1) — HARDI; why single-tensor models fail in crossing fibres.
4. [Tournier et al., 2007](https://doi.org/10.1016/j.neuroimage.2007.02.016) — constrained spherical deconvolution; the modern reconstruction default in MRtrix3 and QSIRecon.
5. [Andersson et al., 2003](https://doi.org/10.1016/S1053-8119(03)00336-7) — `topup`; susceptibility-induced distortion correction, the most common silent failure mode.
6. [Jenkinson et al., 2002](https://doi.org/10.1006/nimg.2002.1132) — FLIRT; the affine registration that anchors DWI in anatomical space.
7. [Maier-Hein et al., 2017](https://doi.org/10.1038/s41467-017-01285-x) — the Tractometer / 96-pipeline study; *false-positive bundles are the rule, not the exception*.
8. [Yeatman et al., 2012](https://doi.org/10.1371/journal.pone.0049790) — AFQ; the tract-profile approach that makes group statistics on diffusion tractable.
9. [Wasserthal et al., 2018](https://doi.org/10.1016/j.neuroimage.2018.07.070) — TractSeg; deep-learning bundle segmentation that closes the loop on (7).

### Roadmap 3 — "I want to do disease-biomarker work in Alzheimer's"

**For:** a clinical researcher pivoting into AD imaging. ~7 papers — short because the field's modern centre of gravity is recent.

1. [Jack et al., 2018](https://doi.org/10.1212/WNL.0000000000005354) — the A/T/N research framework; the vocabulary every modern AD trial uses.
2. [Klunk et al., 2015](https://doi.org/10.1016/j.jalz.2014.07.003) — the Centiloid scale; PET-amyloid quantification, harmonised across tracers.
3. [Sperling et al., 2011](https://doi.org/10.1016/j.jalz.2011.03.003) — preclinical AD diagnostic guidelines; defines the population biomarker studies actually study.
4. [Bateman et al., 2012](https://doi.org/10.1056/NEJMoa1202753) — DIAN; biomarker trajectories indexed to expected symptom onset in autosomal-dominant AD.
5. [Marek et al., 2022](https://doi.org/10.1038/s41586-022-04492-9) — BWAS; why brain-wide association studies require thousands of subjects, AD or otherwise.
6. [van Dyck et al., 2023](https://doi.org/10.1056/NEJMoa2212948) — the lecanemab Phase-III; the trial that re-anchored the field around anti-amyloid disease modification.
7. [Cummings et al., 2024](https://doi.org/10.1002/trc2.12465) — anti-amyloid trial design lessons; what imaging endpoints actually moved.

### Roadmap 4 — "I want to train a clinical-grade deep-learning model"

**For:** an ML engineer entering medical imaging who has trained ImageNet models but not regulated ones. ~8 papers.

1. [Ronneberger et al., 2015](https://doi.org/10.1007/978-3-319-24574-4_28) — U-Net; still the architectural default for medical segmentation.
2. [Isensee et al., 2021](https://doi.org/10.1038/s41592-020-01008-z) — nnU-Net; the self-configuring framework that turned U-Net from architecture into pipeline.
3. [Cardoso et al., 2022](https://doi.org/10.48550/arXiv.2211.02701) — MONAI; the medical-imaging-aware PyTorch extension you should build on instead of rolling your own.
4. [Dosovitskiy et al., 2020](https://doi.org/10.48550/arXiv.2010.11929) — ViT; the architecture displacing CNNs in volumetric segmentation (UNETR, Swin UNETR).
5. [Ma et al., 2024](https://doi.org/10.1038/s41467-024-44824-z) — MedSAM; the segment-anything foundation model adapted to medical imaging.
6. [Collins et al., 2024](https://doi.org/10.1136/bmj-2023-078378) — TRIPOD+AI; the reporting standard that defines what a *credible* clinical ML paper looks like.
7. [Pinto-Coelho, 2023](https://doi.org/10.3390/bioengineering10121435) — CLAIM checklist for medical-imaging AI; the practical companion to TRIPOD+AI.
8. [Roberts et al., 2021](https://doi.org/10.1038/s42256-021-00307-0) — the COVID-19 CT review; why 415 of 415 audited deep-learning papers failed to clear basic methodological bars, and what to fix.

### Roadmap 5 — "I want to do connectomics responsibly"

**For:** anyone running graph metrics on a parcellated connectome — structural or functional. ~8 papers.

1. [Sporns et al., 2005](https://doi.org/10.1371/journal.pcbi.0010042) — the *connectome* word coined; the agenda statement for the next twenty years of work.
2. [Rubinov & Sporns, 2010](https://doi.org/10.1016/j.neuroimage.2009.10.003) — the Brain Connectivity Toolbox paper; the precise definitions for every graph metric you'll report.
3. [Zalesky et al., 2010](https://doi.org/10.1016/j.neuroimage.2010.06.041) — Network-Based Statistic; multiple-comparison correction for connectome edges.
4. [Glasser et al., 2016](https://doi.org/10.1038/nature18933) — HCP-MMP1; the multimodal parcellation that anchors modern cortical connectomics.
5. [van den Heuvel & Sporns, 2011](https://doi.org/10.1523/JNEUROSCI.3539-11.2011) — rich-club organisation; the structural backbone every interpretation hangs on.
6. [Bullmore & Sporns, 2009](https://doi.org/10.1038/nrn2575) — the *Nature Reviews Neuroscience* synthesis; the readable overview that puts the metrics in biological context.
7. [Eklund et al., 2016](https://doi.org/10.1073/pnas.1602413113) — cluster failure; the inference lessons translate directly to NBS thresholding decisions.
8. [Marek et al., 2022](https://doi.org/10.1038/s41586-022-04492-9) — BWAS; the *N* required to make a connectome-behaviour association credible.

### Roadmap 6 — "I want to understand neuroimaging statistics from scratch"

**For:** a 1L PhD student or MD coming from a clinical-stats background who needs the imaging-specific inference apparatus. ~8 papers.

1. [Friston et al., 1995](https://doi.org/10.1002/hbm.460020402) — the GLM applied to fMRI; the substrate of every parametric inference that follows.
2. [Worsley et al., 1992](https://doi.org/10.1038/jcbfm.1992.127) — Random Field Theory; how to correct for spatial smoothness in a continuous statistical map.
3. [Benjamini & Hochberg, 1995](https://doi.org/10.1111/j.2517-6161.1995.tb02031.x) — FDR; the alternative-to-FWER framework you'll need before you read (4).
4. [Genovese et al., 2002](https://doi.org/10.1006/nimg.2001.1037) — FDR for fMRI; the imaging-specific FDR formulation.
5. [Nichols & Holmes, 2002](https://doi.org/10.1002/hbm.1058) — permutation inference; the non-parametric alternative that does not assume Gaussian smoothness.
6. [Smith & Nichols, 2009](https://doi.org/10.1016/j.neuroimage.2008.03.061) — Threshold-Free Cluster Enhancement; the modern default in FSL `randomise` and PALM.
7. [Eklund et al., 2016](https://doi.org/10.1073/pnas.1602413113) — cluster failure; why parametric cluster inference is the wrong default and permutation is the right one.
8. [Marek et al., 2022](https://doi.org/10.1038/s41586-022-04492-9) — BWAS; the sample-size humility that closes the loop on every statistical method above.

### How to use the roadmaps

- **Read in order.** The point of a roadmap is that paper *n* sets up the question paper *n+1* answers.
- **One sitting per roadmap.** Two evenings if the math is new. If you find yourself stalling, jump to the *Methods* section first and skim the rest.
- **Cross the rails.** Roadmaps 1 and 6 share three papers (Friston 1995, Eklund 2016, Marek 2022). The overlap is the point — those are the most-cited papers in the field for a reason.

## Full paper index

The complete reference list, alphabetical by first author. Use this as the lookup index; use the roadmaps above for the reading order.

- **Abraham A, Pedregosa F, Eickenberg M, et al.** Machine learning for neuroimaging with scikit-learn. *Front Neuroinform.* 2014;8:14. [doi:10.3389/fninf.2014.00014](https://doi.org/10.3389/fninf.2014.00014). — Nilearn.
- **Andersson JLR, Skare S, Ashburner J.** How to correct susceptibility distortions in spin-echo echo-planar images: application to diffusion tensor imaging. *NeuroImage.* 2003;20(2):870-888. [doi:10.1016/S1053-8119(03)00336-7](https://doi.org/10.1016/S1053-8119(03)00336-7). — `topup`.
- **Avants BB, Tustison NJ, Song G, Cook PA, Klein A, Gee JC.** A reproducible evaluation of ANTs similarity metric performance in brain image registration. *NeuroImage.* 2011;54(3):2033-2044. [doi:10.1016/j.neuroimage.2010.09.025](https://doi.org/10.1016/j.neuroimage.2010.09.025).
- **Basser PJ, Mattiello J, LeBihan D.** MR diffusion tensor spectroscopy and imaging. *Biophys J.* 1994;66(1):259-267. [doi:10.1016/S0006-3495(94)80775-1](https://doi.org/10.1016/S0006-3495(94)80775-1).
- **Bateman RJ, Xiong C, Benzinger TLS, et al.** Clinical and biomarker changes in dominantly inherited Alzheimer's disease. *N Engl J Med.* 2012;367(9):795-804. [doi:10.1056/NEJMoa1202753](https://doi.org/10.1056/NEJMoa1202753).
- **Benjamini Y, Hochberg Y.** Controlling the false discovery rate: a practical and powerful approach to multiple testing. *J R Stat Soc B.* 1995;57(1):289-300. [doi:10.1111/j.2517-6161.1995.tb02031.x](https://doi.org/10.1111/j.2517-6161.1995.tb02031.x).
- **Botvinik-Nezer R, Holzmeister F, Camerer CF, et al.** Variability in the analysis of a single neuroimaging dataset by many teams. *Nature.* 2020;582(7810):84-88. [doi:10.1038/s41586-020-2314-9](https://doi.org/10.1038/s41586-020-2314-9).
- **Bullmore E, Sporns O.** Complex brain networks: graph theoretical analysis of structural and functional systems. *Nat Rev Neurosci.* 2009;10(3):186-198. [doi:10.1038/nrn2575](https://doi.org/10.1038/nrn2575).
- **Cardoso MJ, Li W, Brown R, et al.** MONAI: an open-source framework for deep learning in healthcare. *arXiv:2211.02701.* 2022. [doi:10.48550/arXiv.2211.02701](https://doi.org/10.48550/arXiv.2211.02701).
- **Casey BJ, Cannonier T, Conley MI, et al.** The Adolescent Brain Cognitive Development (ABCD) study: imaging acquisition across 21 sites. *Dev Cogn Neurosci.* 2018;32:43-54. [doi:10.1016/j.dcn.2018.03.001](https://doi.org/10.1016/j.dcn.2018.03.001).
- **Cieslak M, Cook PA, He X, et al.** QSIPrep: an integrative platform for preprocessing and reconstructing diffusion MRI data. *Nat Methods.* 2021;18(7):775-778. [doi:10.1038/s41592-021-01185-5](https://doi.org/10.1038/s41592-021-01185-5).
- **Ciric R, Thompson WH, Lorenz R, et al.** TemplateFlow: FAIR-sharing of multi-scale, multi-species brain models. *Nat Methods.* 2022;19(12):1568-1571. [doi:10.1038/s41592-022-01681-2](https://doi.org/10.1038/s41592-022-01681-2).
- **Collins GS, Moons KGM, Dhiman P, et al.** TRIPOD+AI statement: updated guidance for reporting clinical prediction models that use regression or machine learning methods. *BMJ.* 2024;385:e078378. [doi:10.1136/bmj-2023-078378](https://doi.org/10.1136/bmj-2023-078378).
- **Cox RW.** AFNI: software for analysis and visualization of functional magnetic resonance neuroimages. *Comput Biomed Res.* 1996;29(3):162-173. [doi:10.1006/cbmr.1996.0014](https://doi.org/10.1006/cbmr.1996.0014).
- **Cummings J, Apostolova L, Rabinovici GD, et al.** Lecanemab: appropriate use recommendations. *J Prev Alzheimers Dis.* 2024. [doi:10.1002/trc2.12465](https://doi.org/10.1002/trc2.12465).
- **DeKraker J, Haast RAM, Yousif MD, et al.** Automated hippocampal unfolding for morphometry and subfield segmentation with HippUnfold. *eLife.* 2022;11:e77945. [doi:10.7554/eLife.77945](https://doi.org/10.7554/eLife.77945).
- **Desikan RS, Ségonne F, Fischl B, et al.** An automated labeling system for subdividing the human cerebral cortex on MRI scans into gyral based regions of interest. *NeuroImage.* 2006;31(3):968-980. [doi:10.1016/j.neuroimage.2006.01.021](https://doi.org/10.1016/j.neuroimage.2006.01.021). — DK atlas.
- **Destrieux C, Fischl B, Dale A, Halgren E.** Automatic parcellation of human cortical gyri and sulci using standard anatomical nomenclature. *NeuroImage.* 2010;53(1):1-15. [doi:10.1016/j.neuroimage.2010.06.010](https://doi.org/10.1016/j.neuroimage.2010.06.010). — Destrieux atlas.
- **Dosovitskiy A, Beyer L, Kolesnikov A, et al.** An image is worth 16x16 words: transformers for image recognition at scale. *arXiv:2010.11929.* 2020. [doi:10.48550/arXiv.2010.11929](https://doi.org/10.48550/arXiv.2010.11929). — ViT.
- **Eklund A, Nichols TE, Knutsson H.** Cluster failure: why fMRI inferences for spatial extent have inflated false-positive rates. *PNAS.* 2016;113(28):7900-7905. [doi:10.1073/pnas.1602413113](https://doi.org/10.1073/pnas.1602413113).
- **Esteban O, Birman D, Schaer M, Koyejo OO, Poldrack RA, Gorgolewski KJ.** MRIQC: Advancing the automatic prediction of image quality in MRI from unseen sites. *PLoS One.* 2017;12(9):e0184661. [doi:10.1371/journal.pone.0184661](https://doi.org/10.1371/journal.pone.0184661).
- **Esteban O, Markiewicz CJ, Blair RW, et al.** fMRIPrep: a robust preprocessing pipeline for functional MRI. *Nat Methods.* 2019;16(1):111-116. [doi:10.1038/s41592-018-0235-4](https://doi.org/10.1038/s41592-018-0235-4).
- **Fischl B.** FreeSurfer. *NeuroImage.* 2012;62(2):774-781. [doi:10.1016/j.neuroimage.2012.01.021](https://doi.org/10.1016/j.neuroimage.2012.01.021).
- **Fortin J-P, Cullen N, Sheline YI, et al.** Harmonization of cortical thickness measurements across scanners and sites. *NeuroImage.* 2018;167:104-120. [doi:10.1016/j.neuroimage.2017.11.024](https://doi.org/10.1016/j.neuroimage.2017.11.024). — ComBat for neuroimaging.
- **Friston KJ, Holmes AP, Worsley KJ, Poline J-B, Frith CD, Frackowiak RSJ.** Statistical parametric maps in functional imaging: a general linear approach. *Hum Brain Mapp.* 1995;2(4):189-210. [doi:10.1002/hbm.460020402](https://doi.org/10.1002/hbm.460020402).
- **Garyfallidis E, Brett M, Amirbekian B, et al.** DIPY, a library for the analysis of diffusion MRI data. *Front Neuroinform.* 2014;8:8. [doi:10.3389/fninf.2014.00008](https://doi.org/10.3389/fninf.2014.00008).
- **Genovese CR, Lazar NA, Nichols T.** Thresholding of statistical maps in functional neuroimaging using the false discovery rate. *NeuroImage.* 2002;15(4):870-878. [doi:10.1006/nimg.2001.1037](https://doi.org/10.1006/nimg.2001.1037).
- **Glasser MF, Coalson TS, Robinson EC, et al.** A multi-modal parcellation of human cerebral cortex. *Nature.* 2016;536(7615):171-178. [doi:10.1038/nature18933](https://doi.org/10.1038/nature18933). — HCP-MMP1.
- **Gorgolewski KJ, Auer T, Calhoun VD, et al.** The brain imaging data structure, a format for organizing and describing outputs of neuroimaging experiments. *Sci Data.* 2016;3:160044. [doi:10.1038/sdata.2016.44](https://doi.org/10.1038/sdata.2016.44). — BIDS.
- **Halchenko YO, Meyer K, Poldrack B, et al.** DataLad: distributed system for joint management of code, data, and their relationship. *J Open Source Softw.* 2021;6(63):3262. [doi:10.21105/joss.03262](https://doi.org/10.21105/joss.03262).
- **Hatamizadeh A, Nath V, Tang Y, Yang D, Roth HR, Xu D.** Swin UNETR: swin transformers for semantic segmentation of brain tumors in MRI images. *arXiv:2201.01266.* 2022. [doi:10.48550/arXiv.2201.01266](https://doi.org/10.48550/arXiv.2201.01266).
- **Henschel L, Conjeti S, Estrada S, Diers K, Fischl B, Reuter M.** FastSurfer — a fast and accurate deep learning based neuroimaging pipeline. *NeuroImage.* 2020;219:117012. [doi:10.1016/j.neuroimage.2020.117012](https://doi.org/10.1016/j.neuroimage.2020.117012).
- **Isensee F, Jaeger PF, Kohl SAA, Petersen J, Maier-Hein KH.** nnU-Net: a self-configuring method for deep learning-based biomedical image segmentation. *Nat Methods.* 2021;18(2):203-211. [doi:10.1038/s41592-020-01008-z](https://doi.org/10.1038/s41592-020-01008-z).
- **Jack CR Jr, Bennett DA, Blennow K, et al.** NIA-AA Research Framework: toward a biological definition of Alzheimer's disease. *Neurology.* 2018;90(12):126-135. [doi:10.1212/WNL.0000000000005354](https://doi.org/10.1212/WNL.0000000000005354). — A/T/N.
- **Jack CR Jr, Bernstein MA, Fox NC, et al.** The Alzheimer's Disease Neuroimaging Initiative (ADNI): MRI methods. *J Magn Reson Imaging.* 2008;27(4):685-691. [doi:10.1002/jmri.21049](https://doi.org/10.1002/jmri.21049).
- **Jenkinson M, Bannister P, Brady M, Smith S.** Improved optimization for the robust and accurate linear registration and motion correction of brain images. *NeuroImage.* 2002;17(2):825-841. [doi:10.1006/nimg.2002.1132](https://doi.org/10.1006/nimg.2002.1132). — FLIRT.
- **Jenkinson M, Beckmann CF, Behrens TEJ, Woolrich MW, Smith SM.** FSL. *NeuroImage.* 2012;62(2):782-790. [doi:10.1016/j.neuroimage.2011.09.015](https://doi.org/10.1016/j.neuroimage.2011.09.015).
- **Kirillov A, Mintun E, Ravi N, et al.** Segment Anything. *arXiv:2304.02643.* 2023. [doi:10.48550/arXiv.2304.02643](https://doi.org/10.48550/arXiv.2304.02643).
- **Klunk WE, Koeppe RA, Price JC, et al.** The Centiloid project: standardizing quantitative amyloid plaque estimation by PET. *Alzheimers Dement.* 2015;11(1):1-15. [doi:10.1016/j.jalz.2014.07.003](https://doi.org/10.1016/j.jalz.2014.07.003).
- **Kwong KK, Belliveau JW, Chesler DA, et al.** Dynamic magnetic resonance imaging of human brain activity during primary sensory stimulation. *PNAS.* 1992;89(12):5675-5679. [doi:10.1073/pnas.89.12.5675](https://doi.org/10.1073/pnas.89.12.5675).
- **LaMontagne PJ, Benzinger TLS, Morris JC, et al.** OASIS-3. *medRxiv.* 2019. [doi:10.1101/2019.12.13.19014902](https://doi.org/10.1101/2019.12.13.19014902).
- **Li X, Morgan PS, Ashburner J, Smith J, Rorden C.** The first step for neuroimaging data analysis: DICOM to NIfTI conversion. *J Neurosci Methods.* 2016;264:47-56. [doi:10.1016/j.jneumeth.2016.03.001](https://doi.org/10.1016/j.jneumeth.2016.03.001). — dcm2niix.
- **Ma J, He Y, Li F, Han L, You C, Wang B.** Segment Anything in Medical Images. *Nat Commun.* 2024;15:654. [doi:10.1038/s41467-024-44824-z](https://doi.org/10.1038/s41467-024-44824-z). — MedSAM.
- **Maier-Hein KH, Neher PF, Houde J-C, et al.** The challenge of mapping the human connectome based on diffusion tractography. *Nat Commun.* 2017;8:1349. [doi:10.1038/s41467-017-01285-x](https://doi.org/10.1038/s41467-017-01285-x). — Tractometer.
- **Marek S, Tervo-Clemmens B, Calabro FJ, et al.** Reproducible brain-wide association studies require thousands of individuals. *Nature.* 2022;603(7902):654-660. [doi:10.1038/s41586-022-04492-9](https://doi.org/10.1038/s41586-022-04492-9).
- **Markiewicz CJ, Gorgolewski KJ, Feingold F, et al.** The OpenNeuro resource for sharing of neuroscience data. *eLife.* 2021;10:e71774. [doi:10.7554/eLife.71774](https://doi.org/10.7554/eLife.71774).
- **Mei X, Liu Z, Robson PM, et al.** RadImageNet: an open radiologic deep learning research dataset for effective transfer learning. *Radiol Artif Intell.* 2022;4(5):e210315. [doi:10.1148/ryai.210315](https://doi.org/10.1148/ryai.210315).
- **Miller KL, Alfaro-Almagro F, Bangerter NK, et al.** Multimodal population brain imaging in the UK Biobank prospective epidemiological study. *Nat Neurosci.* 2016;19(11):1523-1536. [doi:10.1038/nn.4393](https://doi.org/10.1038/nn.4393).
- **Nichols T, Holmes AP.** Nonparametric permutation tests for functional neuroimaging: a primer with examples. *Hum Brain Mapp.* 2002;15(1):1-25. [doi:10.1002/hbm.1058](https://doi.org/10.1002/hbm.1058).
- **Nichols TE, Das S, Eickhoff SB, et al.** Best practices in data analysis and sharing in neuroimaging using MRI. *Nat Neurosci.* 2017;20(3):299-303. [doi:10.1038/nn.4500](https://doi.org/10.1038/nn.4500). — COBIDAS.
- **Ogawa S, Lee T-M, Kay AR, Tank DW.** Brain magnetic resonance imaging with contrast dependent on blood oxygenation. *PNAS.* 1990;87(24):9868-9872. [doi:10.1073/pnas.87.24.9868](https://doi.org/10.1073/pnas.87.24.9868). — BOLD.
- **Pinto-Coelho L.** How artificial intelligence is shaping medical imaging technology: a survey of innovations and applications. *Bioengineering.* 2023;10(12):1435. [doi:10.3390/bioengineering10121435](https://doi.org/10.3390/bioengineering10121435).
- **Power JD, Barnes KA, Snyder AZ, Schlaggar BL, Petersen SE.** Spurious but systematic correlations in functional connectivity MRI networks arise from subject motion. *NeuroImage.* 2012;59(3):2142-2154. [doi:10.1016/j.neuroimage.2011.10.018](https://doi.org/10.1016/j.neuroimage.2011.10.018).
- **Roberts M, Driggs D, Thorpe M, et al.** Common pitfalls and recommendations for using machine learning to detect and prognosticate for COVID-19 using chest radiographs and CT scans. *Nat Mach Intell.* 2021;3:199-217. [doi:10.1038/s42256-021-00307-0](https://doi.org/10.1038/s42256-021-00307-0).
- **Ronneberger O, Fischer P, Brox T.** U-Net: convolutional networks for biomedical image segmentation. *MICCAI.* 2015. [doi:10.1007/978-3-319-24574-4_28](https://doi.org/10.1007/978-3-319-24574-4_28).
- **Rubinov M, Sporns O.** Complex network measures of brain connectivity: uses and interpretations. *NeuroImage.* 2010;52(3):1059-1069. [doi:10.1016/j.neuroimage.2009.10.003](https://doi.org/10.1016/j.neuroimage.2009.10.003). — Brain Connectivity Toolbox.
- **Schaefer A, Kong R, Gordon EM, et al.** Local-global parcellation of the human cerebral cortex from intrinsic functional connectivity MRI. *Cereb Cortex.* 2018;28(9):3095-3114. [doi:10.1093/cercor/bhx179](https://doi.org/10.1093/cercor/bhx179).
- **Shafto MA, Tyler LK, Dixon M, et al.** The Cambridge Centre for Ageing and Neuroscience (Cam-CAN) study protocol. *BMC Neurol.* 2014;14:204. [doi:10.1186/s12883-014-0204-1](https://doi.org/10.1186/s12883-014-0204-1).
- **Smith SM, Nichols TE.** Threshold-free cluster enhancement: addressing problems of smoothing, threshold dependence and localisation in cluster inference. *NeuroImage.* 2009;44(1):83-98. [doi:10.1016/j.neuroimage.2008.03.061](https://doi.org/10.1016/j.neuroimage.2008.03.061). — TFCE.
- **Sperling RA, Aisen PS, Beckett LA, et al.** Toward defining the preclinical stages of Alzheimer's disease. *Alzheimers Dement.* 2011;7(3):280-292. [doi:10.1016/j.jalz.2011.03.003](https://doi.org/10.1016/j.jalz.2011.03.003).
- **Spitzer H, Ripart M, Whitaker K, et al.** Interpretable surface-based detection of focal cortical dysplasias: the MELD FCD tool. *Brain.* 2022;145(11):3859-3871. [doi:10.1093/brain/awac224](https://doi.org/10.1093/brain/awac224).
- **Sporns O, Tononi G, Kötter R.** The human connectome: a structural description of the human brain. *PLoS Comput Biol.* 2005;1(4):e42. [doi:10.1371/journal.pcbi.0010042](https://doi.org/10.1371/journal.pcbi.0010042).
- **Stejskal EO, Tanner JE.** Spin diffusion measurements: spin echoes in the presence of a time-dependent field gradient. *J Chem Phys.* 1965;42(1):288-292. [doi:10.1063/1.1695690](https://doi.org/10.1063/1.1695690).
- **Tournier J-D, Calamante F, Connelly A.** Robust determination of the fibre orientation distribution in diffusion MRI: non-negativity constrained super-resolved spherical deconvolution. *NeuroImage.* 2007;35(4):1459-1472. [doi:10.1016/j.neuroimage.2007.02.016](https://doi.org/10.1016/j.neuroimage.2007.02.016). — CSD.
- **Tournier J-D, Smith R, Raffelt D, et al.** MRtrix3: a fast, flexible and open software framework for medical image processing and visualisation. *NeuroImage.* 2019;202:116137. [doi:10.1016/j.neuroimage.2019.116137](https://doi.org/10.1016/j.neuroimage.2019.116137).
- **Tuch DS.** Q-ball imaging. *Magn Reson Med.* 2004;52(6):1358-1372. [doi:10.1002/mrm.20279](https://doi.org/10.1002/mrm.20279). — HARDI / Q-ball.
- **Tzourio-Mazoyer N, Landeau B, Papathanassiou D, et al.** Automated anatomical labeling of activations in SPM. *NeuroImage.* 2002;15(1):273-289. [doi:10.1006/nimg.2001.0978](https://doi.org/10.1006/nimg.2001.0978). — AAL.
- **van den Heuvel MP, Sporns O.** Rich-club organization of the human connectome. *J Neurosci.* 2011;31(44):15775-15786. [doi:10.1523/JNEUROSCI.3539-11.2011](https://doi.org/10.1523/JNEUROSCI.3539-11.2011).
- **van Dyck CH, Swanson CJ, Aisen P, et al.** Lecanemab in early Alzheimer's disease. *N Engl J Med.* 2023;388(1):9-21. [doi:10.1056/NEJMoa2212948](https://doi.org/10.1056/NEJMoa2212948).
- **Van Essen DC, Smith SM, Barch DM, Behrens TEJ, Yacoub E, Ugurbil K.** The WU-Minn Human Connectome Project: an overview. *NeuroImage.* 2013;80:62-79. [doi:10.1016/j.neuroimage.2013.05.041](https://doi.org/10.1016/j.neuroimage.2013.05.041).
- **Wasserthal J, Neher P, Maier-Hein KH.** TractSeg — fast and accurate white matter tract segmentation. *NeuroImage.* 2018;183:239-253. [doi:10.1016/j.neuroimage.2018.07.070](https://doi.org/10.1016/j.neuroimage.2018.07.070).
- **Winkler AM, Ridgway GR, Webster MA, Smith SM, Nichols TE.** Permutation inference for the general linear model. *NeuroImage.* 2014;92:381-397. [doi:10.1016/j.neuroimage.2014.01.060](https://doi.org/10.1016/j.neuroimage.2014.01.060). — PALM.
- **Worsley KJ, Evans AC, Marrett S, Neelin P.** A three-dimensional statistical analysis for CBF activation studies in human brain. *J Cereb Blood Flow Metab.* 1992;12(6):900-918. [doi:10.1038/jcbfm.1992.127](https://doi.org/10.1038/jcbfm.1992.127). — Random Field Theory.
- **Worsley KJ, Friston KJ.** Analysis of fMRI time-series revisited — again. *NeuroImage.* 1995;2(3):173-181. [doi:10.1006/nimg.1995.1023](https://doi.org/10.1006/nimg.1995.1023).
- **Yarkoni T, Markiewicz CJ, de la Vega A, et al.** PyBIDS: Python tools for BIDS datasets. *J Open Source Softw.* 2019;4(40):1294. [doi:10.21105/joss.01294](https://doi.org/10.21105/joss.01294).
- **Yeatman JD, Dougherty RF, Myall NJ, Wandell BA, Feldman HM.** Tract profiles of white matter properties: automating fiber-tract quantification. *PLoS One.* 2012;7(11):e49790. [doi:10.1371/journal.pone.0049790](https://doi.org/10.1371/journal.pone.0049790). — AFQ.
- **Zalesky A, Fornito A, Bullmore ET.** Network-based statistic: identifying differences in brain networks. *NeuroImage.* 2010;53(4):1197-1207. [doi:10.1016/j.neuroimage.2010.06.041](https://doi.org/10.1016/j.neuroimage.2010.06.041). — NBS.
- **Zhang S, Xu Y, Usuyama N, et al.** BiomedCLIP: a multimodal biomedical foundation model pretrained from fifteen million scientific image-text pairs. *arXiv:2303.00915.* 2023. [doi:10.48550/arXiv.2303.00915](https://doi.org/10.48550/arXiv.2303.00915).

## Where to next

- [Reference datasets](datasets.md) for the cohorts these methods were validated on.
- [Major pipelines](pipelines.md) for the tools that implement them.
