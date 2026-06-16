# Neuroscience & neurology for neuroimaging

> The biology behind the voxels. Enough neuroanatomy, systems neuroscience, and clinical neurology to know *what* you're looking at and *why* it matters.

A pipeline that computes the right number against the wrong region is still wrong. This page is the minimum neuroscience an engineer / data engineer / AI engineer in neuroimaging needs to do the work credibly.

## Macroscale anatomy

The brain has a small set of structural landmarks worth knowing cold.

### Lobes and major sulci

- **Frontal** — anterior of the central sulcus. Motor (precentral gyrus), executive (prefrontal), language production (Broca, BA 44/45 left-lateralised).
- **Parietal** — posterior of the central sulcus, above the lateral sulcus. Sensory (postcentral), spatial (intraparietal sulcus).
- **Temporal** — below the lateral sulcus. Auditory (Heschl), language comprehension (Wernicke, posterior superior temporal), memory (hippocampus).
- **Occipital** — posterior. Primary visual cortex (V1) along the calcarine sulcus; extrastriate visual areas anterior to it.
- **Insula** — buried in the lateral sulcus. Interoception, salience, viscero-motor.
- **Cingulate** — medial, around the corpus callosum. Limbic, conflict, pain.

The two reference sulci every analyst should identify on a coronal slice: **central** (motor / sensory boundary) and **lateral** (Sylvian fissure, top of temporal lobe).

### Subcortex

- **Thalamus** — the relay hub. Almost every cortical projection passes through it.
- **Basal ganglia** — caudate, putamen, globus pallidus, substantia nigra, subthalamic nucleus. Action selection; Parkinson's disease territory.
- **Hippocampus** — declarative memory; first site of Alzheimer's tau pathology.
- **Amygdala** — salience and threat learning.
- **Cerebellum** — motor coordination, increasingly cognition.
- **Brainstem** — midbrain / pons / medulla. Cardiorespiratory, arousal, cranial nerves.

### White-matter pathways

DWI tractography makes these tractable in vivo. The bundles every paper assumes you know:

- **Corpus callosum** — interhemispheric. Genu (frontal), body, splenium (occipital).
- **Cingulum** — limbic.
- **Superior longitudinal fasciculus (SLF) / arcuate fasciculus** — language-relevant fronto-parietal / fronto-temporal.
- **Inferior longitudinal fasciculus (ILF)** — temporo-occipital.
- **Inferior fronto-occipital fasciculus (IFOF)** — semantic processing.
- **Uncinate fasciculus** — fronto-temporal.
- **Corticospinal tract** — motor.

The ICBM-DTI-81 atlas ([Mori et al., 2008](https://doi.org/10.1016/j.neuroimage.2007.07.053)) and the HCP-derived tract atlases formalise these.

## Cells and circuits

You don't need to derive Hodgkin-Huxley, but the abstractions show up in modelling.

### Neurons and synapses

A neuron integrates synaptic inputs (excitatory glutamatergic, inhibitory GABAergic) at the soma, fires action potentials along the axon, and releases neurotransmitter at synapses. Layer V pyramidal neurons in cortex generate the dipolar currents EEG / MEG detect.

### Cortical columns and layers

Cortex has six layers (I–VI). Layer IV is the primary input from thalamus; layers II/III project to other cortical areas; layers V/VI project subcortically. The columnar organisation is what gives V1 its orientation-tuned receptive fields and what makes laminar fMRI (7 T+) potentially powerful.

### Neurotransmitter systems

| System | Origin | Function | Imaging context |
|---|---|---|---|
| **Dopaminergic** | VTA, substantia nigra | Reward, motor | PET (DAT, raclopride); Parkinson's, addiction |
| **Serotonergic** | Raphe nuclei | Mood, sleep | PET; depression, OCD |
| **Cholinergic** | Nucleus basalis | Arousal, memory | Alzheimer's |
| **Noradrenergic** | Locus coeruleus | Arousal, attention | fMRI of LC |
| **Glutamatergic / GABAergic** | Cortex-wide | Excitation / inhibition | MRS; epilepsy |

PET ligands target specific receptors / transporters in these systems.

## Functional organisation

### Cortical networks

Resting-state fMRI revealed ~7-17 canonical large-scale networks, replicated across cohorts ([Yeo et al., 2011](https://doi.org/10.1152/jn.00338.2011); [Power et al., 2011](https://doi.org/10.1016/j.neuron.2011.09.006)):

- **Default mode (DMN)** — medial prefrontal, posterior cingulate, angular. Self-referential, mind-wandering, social cognition.
- **Salience** — anterior insula, dorsal anterior cingulate. Switching between networks.
- **Dorsal attention** — frontal eye fields, intraparietal sulcus. Top-down attention.
- **Ventral attention** — temporoparietal junction, ventral frontal. Stimulus-driven attention.
- **Frontoparietal control** — dorsolateral prefrontal, posterior parietal. Cognitive control.
- **Visual / somatomotor / auditory** — primary sensory.
- **Limbic** — orbitofrontal, temporal pole. Emotion, valuation.

These networks anchor most resting-state and task-fMRI interpretations.

### Lateralisation

Many functions are lateralised:

- **Language** — predominantly left-hemisphere in ~95% of right-handers.
- **Spatial attention** — predominantly right.
- **Face processing** — right fusiform face area is typically dominant.
- **Music** — bilateral with right > left for melody.

Handedness modulates this but doesn't reverse it cleanly.

## Cognitive neuroscience in one page

Frameworks you'll meet in papers:

- **Hierarchical predictive coding** — cortex as a hierarchy of generative models predicting sensory input; prediction errors propagate up.
- **Multiple-demand system** — frontoparietal regions that activate for any cognitively demanding task.
- **Two-streams model of vision** — dorsal "where/how" and ventral "what" pathways.
- **Multi-component working memory** (Baddeley) — phonological loop, visuospatial sketchpad, central executive.
- **Brain energetics** — the brain uses ~20% of body's energy at <2% of body mass; PET-FDG tracks glucose use.

## Neurology — the clinical conditions neuroimaging touches

A working vocabulary of the disorders the field studies.

### Stroke (cerebrovascular disease)

- **Ischemic** (~85%) — vessel occlusion → restricted diffusion → bright on DWI, dark on ADC. Time-critical; DWI is the gold-standard acute scan.
- **Haemorrhagic** — bleeding. SWI / GRE for old microbleeds.
- **Transient ischemic attack (TIA)** — symptoms resolve; may show DWI lesions.

### Neurodegeneration

- **Alzheimer's disease** — medial temporal atrophy (hippocampus, entorhinal); amyloid-PET positive; tau-PET in cortex. Diagnosed by [AT(N) framework](https://doi.org/10.1212/WNL.0000000000004826) (Jack et al., 2018).
- **Parkinson's disease** — substantia nigra dopaminergic loss; DAT-SPECT positive. MRI shows iron deposition (SWI), nigrostriatal degeneration.
- **Frontotemporal dementia** — frontal / temporal atrophy; behavioural or semantic variants.
- **Lewy body / multiple system atrophy / progressive supranuclear palsy** — overlapping movement-disorder spectrum.

### Multiple sclerosis (MS)

White-matter demyelinating lesions, classically periventricular, juxtacortical, infratentorial, spinal cord. FLAIR-hyperintense, T1-hypointense (black holes). McDonald criteria for diagnosis.

### Epilepsy

Focal cortical dysplasias (FCD), mesial temporal sclerosis, tumours, post-traumatic scars. [MELD project](https://doi.org/10.1093/brain/awac224) applies DL to FreeSurfer surfaces to detect subtle FCDs.

### Traumatic brain injury (TBI)

- **Mild TBI** — often imaging-negative on conventional MRI; DTI shows diffuse axonal injury.
- **Moderate / severe** — contusions, hemorrhages, oedema.
- **Chronic traumatic encephalopathy (CTE)** — repetitive head impact, tau-PET, atrophy.

### Brain tumours

- **Gliomas** (astrocytoma, oligodendroglioma, glioblastoma) — graded I–IV. T1-Gd enhancement = blood-brain barrier breakdown; T2/FLAIR = oedema + non-enhancing tumour.
- **Meningiomas** — typically benign, extra-axial.
- **Metastases** — usually multiple, T1-Gd enhancing.

The BraTS challenge ([Bakas et al., 2017](https://doi.org/10.1038/sdata.2017.117)) has formalised glioma segmentation benchmarks.

### Psychiatric

- **Schizophrenia** — ventricular enlargement, reduced grey matter (frontal, temporal); functional dysconnectivity.
- **Major depression** — reduced hippocampal volume; default-mode hyperactivity.
- **Autism spectrum disorder** — heterogeneous; atypical default-mode and salience network connectivity.
- **ADHD** — reduced caudate / putamen volumes; frontostriatal dysfunction.

Psychiatric imaging is hard; effect sizes are small, cohorts must be large ([Marek 2022](https://doi.org/10.1038/s41586-022-04492-9)).

### Developmental / paediatric

- **Cortical malformations** — focal cortical dysplasia, polymicrogyria, lissencephaly.
- **Tuberous sclerosis** — cortical tubers, subependymal nodules.
- **White-matter maturation** — myelination map changes T1 contrast across the first 2 years; specialised pipelines (NiBabies, dHCP) required.

## Clinical reading conventions

Quick orientation if you ever look at a clinical-looking image:

- **Radiological convention** — left of image = patient's right (you're looking at the patient from the foot of the bed).
- **Neurological convention** — left of image = patient's left (you're looking at the brain itself).
- **Slice orientations**: axial (horizontal), coronal (front view), sagittal (side view).
- **Contrast classes** to recognise:
  - T1: GM dark, WM bright, CSF dark.
  - T2: GM medium, WM dark, CSF bright.
  - FLAIR: like T2 but CSF suppressed; lesions stand out.
  - DWI: acute strokes bright.

Radiology reports use a stereotyped structure: indication, technique, findings, impression. Reading a few of these alongside the imaging is one of the fastest ways to calibrate your intuition.

## The atlases neuroimagers cite

| Atlas | What it parcellates | Reference |
|---|---|---|
| **Desikan-Killiany** | 68 cortical regions | [Desikan 2006](https://doi.org/10.1016/j.neuroimage.2006.01.021) |
| **HCP-MMP1 (Glasser)** | 360 multi-modal regions | [Glasser 2016](https://doi.org/10.1038/nature18933) |
| **Schaefer** | 100-1000 functional regions | [Schaefer 2018](https://doi.org/10.1093/cercor/bhx179) |
| **AAL** | 116 anatomical regions | [Tzourio-Mazoyer 2002](https://doi.org/10.1006/nimg.2001.0978) |
| **Brodmann** | Historical cyto-architectonic | Brodmann 1909 |
| **Yeo 7 / 17 networks** | Resting-state networks | [Yeo 2011](https://doi.org/10.1152/jn.00338.2011) |

See [Landmark → Atlases](../../landmark/atlases.md) for the full bibliographic treatment.

## How this informs engineering decisions

- **A bug in subject-to-template registration is harder to spot in basal ganglia than in cortex.** Always QC the deep grey matter alignment.
- **An "improved" cortical parcellation that splits motor cortex unevenly across hemispheres will quietly break group statistics.** Validate against known lateralisation.
- **A segmentation that misses small periventricular FLAIR lesions doesn't help an MS pipeline even if Dice = 0.92.** Clinical importance and average-over-pixels metric diverge.
- **A model trained on healthy adult HCP data will fail on a paediatric or stroke cohort.** Cohort coverage is part of model spec.

## Glossary of common terms

- **Anterior / posterior** — front / back.
- **Superior / inferior** — top / bottom.
- **Medial / lateral** — towards midline / towards side.
- **Rostral / caudal** — towards nose / towards tail (interchangeable with anterior/posterior for brain).
- **Ipsilateral / contralateral** — same side / opposite side.
- **Grey / white matter** — neuronal cell bodies / myelinated axons.
- **Cortex** — outermost layer of GM; ~2-4 mm thick.
- **Sulcus / gyrus** — groove / ridge of cortex.
- **Atrophy** — tissue loss, lower volume / thickness.
- **Hyperintensity / hypointensity** — bright / dark on the image.
- **Edema** — fluid accumulation, T2/FLAIR-bright.
- **Stenosis** — vessel narrowing.

## References

1. **Kandel ER, Schwartz JH, Jessell TM, et al.** *Principles of Neural Science.* 6th ed. McGraw-Hill; 2021. ISBN 978-1259642234. — the canonical textbook.
2. **Purves D, Augustine GJ, Fitzpatrick D, et al.** *Neuroscience.* 6th ed. Oxford University Press; 2018. ISBN 978-1605353807.
3. **Catani M, Thiebaut de Schotten M.** *Atlas of Human Brain Connections.* Oxford University Press; 2012. ISBN 978-0199541164.
4. **Mai JK, Majtanik M, Paxinos G.** *Atlas of the Human Brain.* 4th ed. Academic Press; 2015. ISBN 978-0128028001.
5. **Yeo BTT, Krienen FM, Sepulcre J, et al.** The organization of the human cerebral cortex estimated by intrinsic functional connectivity. *J Neurophysiol.* 2011;106(3):1125-1165. [doi:10.1152/jn.00338.2011](https://doi.org/10.1152/jn.00338.2011)
6. **Power JD, Cohen AL, Nelson SM, et al.** Functional network organization of the human brain. *Neuron.* 2011;72(4):665-678. [doi:10.1016/j.neuron.2011.09.006](https://doi.org/10.1016/j.neuron.2011.09.006)
7. **Glasser MF, Coalson TS, Robinson EC, et al.** A multi-modal parcellation of human cerebral cortex. *Nature.* 2016;536:171-178. [doi:10.1038/nature18933](https://doi.org/10.1038/nature18933)
8. **Jack CR Jr, Bennett DA, Blennow K, et al.** NIA-AA Research Framework: Toward a biological definition of Alzheimer's disease. *Alzheimers Dement.* 2018;14(4):535-562. [doi:10.1016/j.jalz.2018.02.018](https://doi.org/10.1016/j.jalz.2018.02.018)
9. **Filippi M, Bar-Or A, Piehl F, et al.** Multiple sclerosis. *Nat Rev Dis Primers.* 2018;4:43. [doi:10.1038/s41572-018-0041-4](https://doi.org/10.1038/s41572-018-0041-4)
10. **Bakas S, Akbari H, Sotiras A, et al.** Advancing The Cancer Genome Atlas glioma MRI collections with expert segmentation labels and radiomic features. *Sci Data.* 2017;4:170117. [doi:10.1038/sdata.2017.117](https://doi.org/10.1038/sdata.2017.117) — BraTS.
11. **Allen Brain Atlas.** Free online: [https://atlas.brain-map.org](https://atlas.brain-map.org)
12. **The Human Brain Atlas (Sandra Witelson)** — open online resources at [https://www.brainmuseum.org](https://www.brainmuseum.org).

## Where to next

That closes the Foundations sub-section's neuroscience layer. From here, [Analysis](../../analysis/index.md) is where you operationalise these concepts against derivatives, and the [Landmark](../../landmark/index.md) section gives you the published context to compare against.
