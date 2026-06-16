# Medical imaging physics

> Why a magnetic field, an X-ray beam, a positron tracer, an ultrasound pulse, or a near-infrared photon produces a brain image — and what every acquisition parameter is really doing.

You don't need to derive the Bloch equations from Maxwell's, but you do need a working physical model for every modality you might encounter. MRI is the deep core of this page (it dominates research neuroimaging); CT, PET, ultrasound, optical, and EEG/MEG biophysics get their own treatment because you'll meet all of them in multimodal cohorts.

## The phenomenon — nuclear magnetic resonance

A proton has a tiny intrinsic magnetic moment (spin-½). Placed in a strong static field $B_0$ (the scanner's main magnet, 1.5 T / 3 T / 7 T), spins precess at the **Larmor frequency**:

$$
\omega_0 = \gamma B_0
$$

where $\gamma / 2\pi \approx 42.58$ MHz/T for hydrogen. At 3 T, $\omega_0/2\pi \approx 127.7$ MHz — right in the radio-frequency band.

At equilibrium, a slight excess of spins align with $B_0$, producing a net magnetisation $M_0$ along $B_0$ ($z$-axis convention). The signal we'll detect comes from tipping that magnetisation into the transverse plane.

## The Bloch equations

The macroscopic dynamics of $M(t) = (M_x, M_y, M_z)$ in the rotating frame, with RF field $B_1$:

$$
\frac{dM}{dt} = \gamma (M \times B) - \frac{M_x \hat x + M_y \hat y}{T_2} - \frac{(M_z - M_0)\hat z}{T_1}
$$

Two relaxation times appear:

- **$T_1$** — longitudinal recovery toward equilibrium. ~800 ms (WM) to ~4 s (CSF) at 3 T.
- **$T_2$** — transverse decay due to spin-spin interactions. ~70 ms (WM) to ~300 ms (CSF).
- **$T_2^*$** — additional decay from *static* field inhomogeneities. Always $T_2^* < T_2$.

Image contrast is engineered by choosing TR (repetition time) and TE (echo time) to differentially weight tissues by $T_1$ and $T_2$.

## RF pulses and contrast

A **flip angle** $\alpha$ pulse rotates $M$ from $z$ toward the transverse plane by $\alpha$.

- **Spin echo** — 90° excite, 180° refocus → cancels static dephasing; signal depends on $T_2$ (not $T_2^*$). The original MRI sequence.
- **Gradient echo (GRE)** — single excite, no refocus → signal depends on $T_2^*$. The substrate for EPI / fMRI / SWI.
- **Inversion recovery** — 180° invert, wait time TI, 90° excite. Tunes contrast by tissue $T_1$. The basis for FLAIR (suppress CSF) and MPRAGE (T1-weighted structural).

For sequence specifics see [Fundamentals → MRI sequences](../sequences/index.md).

## Gradients and spatial encoding

A second class of magnetic fields — **gradients** $G_x, G_y, G_z$ — make $B_z$ position-dependent:

$$
\omega(\vec r) = \gamma (B_0 + \vec G \cdot \vec r)
$$

Three gradient operations build an image:

- **Slice selection** — a slice-select gradient + a narrow-band RF pulse excites only one slice.
- **Phase encoding** — a brief $G_y$ applied between excitation and readout encodes the $y$ position into the phase of the signal.
- **Frequency encoding** — a $G_x$ during readout encodes $x$ into frequency.

## k-space — the Fourier dual

The measured signal at time $t$ during a readout is:

$$
S(t) = \int_V M(\vec r) \, e^{-j \, 2\pi \vec k(t) \cdot \vec r} \, d^3r
$$

with $\vec k(t) = \frac{\gamma}{2\pi}\int_0^t \vec G(\tau)\, d\tau$. The signal $S(t)$ is the **Fourier transform** of the spatial magnetisation. The image is reconstructed by the inverse DFT of the sampled k-space.

Practical consequences:

- The trajectory through k-space is controlled by the gradients. EPI fills a Cartesian grid in a single zigzag readout; spiral fills a spiral; radial fills spokes.
- The centre of k-space encodes contrast; the edges encode high-resolution detail.
- Sub-Nyquist sampling along $k_y$ → aliasing in the image (the "fold-over" artefact). Parallel imaging (SENSE, GRAPPA) recovers it.

## Signal-to-noise ratio

A canonical scaling result:

$$
\text{SNR} \propto B_0 \cdot \Delta x \cdot \Delta y \cdot \Delta z \cdot \sqrt{N_{\text{avg}} \cdot t_{\text{readout}}}
$$

Doubling voxel volume → 2× SNR. Doubling acquisitions → $\sqrt{2}\times$ SNR. Doubling $B_0$ from 3 T to 7 T → roughly 2× SNR but with worse $T_2^*$ at the same TE.

Receive coils matter: a 32-channel head coil collects ~3× the signal of an 8-channel.

## Distortion and susceptibility

Differences in magnetic susceptibility (air-tissue interfaces) perturb $B_0$ locally. Effects:

- **Signal dropout** near sinuses and ear canals — orbitofrontal and inferior temporal cortex are routinely affected on EPI.
- **Geometric distortion** along the phase-encode direction — fixed by field maps (`topup`, SyN-SDC).

Field strength makes this worse: a problem at 3 T becomes a crisis at 7 T.

## Diffusion-weighted imaging

A pair of strong, matched gradient lobes around a 180° refocusing pulse encodes water displacement:

$$
\frac{S(b)}{S_0} = e^{-b \cdot \mathrm{ADC}}, \quad b \approx \gamma^2 G^2 \delta^2 \left(\Delta - \frac{\delta}{3}\right)
$$

- $\delta$ — gradient duration, $\Delta$ — separation, $G$ — amplitude.
- ADC — apparent diffusion coefficient (mm²/s).
- Typical $b$: 0 (reference), 1000 (DTI), 2000-3000 (HARDI), >3000 (multi-shell).

Acquire many directions → fit a tensor (DTI) or spherical-deconvolution model (CSD). See [Fundamentals → MRI sequences → DWI](../sequences/dwi.md).

## BOLD contrast

Active neurons increase oxygen consumption locally, then over-compensated blood flow over-supplies oxygenated haemoglobin, decreasing local deoxy-Hb concentration. Deoxy-Hb is paramagnetic → it perturbs $B_0$ → less perturbation = stronger $T_2^*$ signal. Net effect: BOLD signal rises with neural activity, ~5% modulation, peak ~5 s after onset.

The hemodynamic response function (HRF) is the impulse response of this system:

$$
h(t) \approx \text{(gamma)} - \text{(gamma)}
$$

with the canonical "two-gamma" form used in SPM and FSL.

## Computed tomography (CT)

CT measures X-ray attenuation through the head from many angles, then reconstructs a 3D map of attenuation coefficients $\mu(\vec r)$ via filtered back-projection or iterative reconstruction (OSEM, model-based). The output is in **Hounsfield units (HU)**:

$$
\mathrm{HU} = 1000 \cdot \frac{\mu - \mu_{water}}{\mu_{water} - \mu_{air}}
$$

with $\mathrm{HU}(\text{water})=0$, $\mathrm{HU}(\text{air})=-1000$, $\mathrm{HU}(\text{bone})\approx 1000+$. Fresh blood is ~60-80 HU (hyperdense, bright); acute infarcts are slightly hypodense.

CT is the front-line modality for **acute stroke / haemorrhage** because of sub-minute scan times and exquisite sensitivity to fresh blood. **Dose** is the trade-off: a head CT is ~2 mSv (about a year of natural background). CT angiography (CTA) and perfusion CT (CTP) add iodinated contrast for vascular and tissue-perfusion maps.

For research, CT shows up in: skull / bone analyses (cranioplasty planning, PET-MR attenuation correction proxies), older multi-modal cohorts that pre-date MRI, and intracranial-electrode localisation (CT/MR fusion).

## Positron emission tomography (PET)

A positron-emitting radiotracer is injected; positrons travel a short distance, annihilate with electrons, and produce two **511 keV photons** in nearly opposite directions. The scanner detects coincident photon pairs along lines of response (LORs); reconstruction (OSEM, MLEM, time-of-flight) yields a 3D tracer-concentration map.

Common tracers and what they probe:

| Tracer | Target | Half-life | Use |
|---|---|---|---|
| **[¹⁸F]FDG** | Glucose metabolism | 110 min | Tumour, dementia, epilepsy |
| **[¹⁸F]florbetaben / florbetapir / flutemetamol** | Amyloid-β plaques | 110 min | Alzheimer's |
| **[¹⁸F]flortaucipir** | Tau tangles | 110 min | Alzheimer's, CTE |
| **[¹⁸F]FET / [¹¹C]MET** | Amino-acid uptake | 110 / 20 min | Glioma |
| **[¹¹C]PiB** | Amyloid-β | 20 min | Alzheimer's (research) |
| **[¹⁸F]FDOPA / [¹¹C]raclopride / [¹²³I]DAT-SPECT** | Dopamine system | varies | Parkinson's, addiction |

Quantitative PET uses **kinetic modelling**:

- **SUV / SUVR** — semi-quantitative ratio; common in clinical practice.
- **Patlak / Logan graphical methods** — slope = irreversible / reversible binding rate.
- **Two-tissue compartment model** — full kinetics; requires arterial input function or reference region.

Spatial resolution: ~3-5 mm FWHM. Quantitative accuracy needs **attenuation correction**; in PET/MR, that's done from a UTE / Dixon MR sequence or DL-based estimation.

## Ultrasound

Ultrasound transmits high-frequency sound waves (1-15 MHz) and times the echoes. The **speed of sound in tissue is ~1540 m/s**; round-trip time × half = depth. Pulse-echo amplitude maps tissue interfaces; Doppler shift maps flow velocity.

Brain ultrasound is limited by the **skull** which absorbs and scatters the beam. Practical use cases:

- **Neonatal transfontanelle** — the open fontanelle allows imaging through it; bedside, no radiation.
- **Intra-operative** — direct insonation after craniotomy.
- **Functional ultrasound (fUS)** — high-frame-rate plane-wave imaging tracks cerebral blood-volume changes at high spatial-temporal resolution in animal models and increasingly in humans.
- **Focused ultrasound (FUS)** — therapeutic; thermal ablation (essential tremor), transient BBB opening, neuromodulation.

For an engineer entering this space, [Bercoff et al., 2004](https://doi.org/10.1109/TUFFC.2004.1295425) (transient elastography) and [Macé et al., 2011](https://doi.org/10.1038/nmeth.1641) (functional ultrasound) are the landmark methods papers.

## Optical: NIRS and OCT

### Near-infrared spectroscopy (NIRS / fNIRS)

Two wavelengths of near-infrared light (~700-900 nm) penetrate ~1-3 cm of tissue and are absorbed differently by **oxy- and deoxy-haemoglobin**. Source-detector pairs on the scalp produce a map of cortical haemodynamic changes — a BOLD-like signal at lower spatial resolution but without a scanner.

Strengths: portable, tolerant of motion, infant-friendly. Limitations: only superficial cortex; skin/skull absorbance dominates.

### Optical coherence tomography (OCT)

Uses low-coherence interferometry to image micron-scale structure ~1-2 mm deep. In neuro-research, OCT is the workhorse for the **retina** — retinal-nerve-fibre-layer thinning is a biomarker for MS, glaucoma, and increasingly Alzheimer's.

## EEG and MEG biophysics

Neuronal **pyramidal cells** in cortex are spatially aligned perpendicular to the cortical surface. Their post-synaptic potentials sum into dipolar currents that produce measurable electric potentials on the scalp (EEG, ~10 µV) and magnetic fields outside the head (MEG, ~10 fT — 8 orders of magnitude below Earth's field, requiring a magnetically shielded room and SQUID or OPM sensors).

Some key physical facts:

- **EEG** sees both radial and tangential dipoles, but is severely distorted by skull conductivity (~1/80 of brain).
- **MEG** sees primarily *tangential* dipoles (sulcal walls); is unaffected by skull conductivity because magnetic permeability is uniform.
- **Spatial resolution** — EEG ~ centimetres; MEG ~ millimetres in optimal conditions.
- **Temporal resolution** — milliseconds; the only non-invasive method that resolves real neural timescales.
- **Source localisation** is an *inverse problem* — many cortical dipole configurations explain the same sensor data. Beamformer (LCMV), MNE / dSPM, and Bayesian (Champagne) algorithms regularise it differently.

For methods see [Hämäläinen et al., 1993](https://doi.org/10.1103/RevModPhys.65.413) (MEG physics review) and the [MNE-Python docs](https://mne.tools/).

## MRS — magnetic resonance spectroscopy

Same hardware as MRI, but the readout is in the *spectral* dimension: a 1H-MRS voxel-of-interest produces a chemical-shift spectrum (NAA, creatine, choline, lactate, glutamate, GABA peaks). Concentrations reported in mmol/kg. Useful for biochemistry of tumours, epilepsy, neurodegeneration. Modern implementations (MEGA-PRESS, J-PRESS) edit out water and resolve GABA / glutamate.

## What every modality has in common

- **Forward model** — physics maps `source → signal`.
- **Inverse problem** — algorithm maps `signal → image / source estimate`.
- **Noise sources** — modality-specific (thermal in MR, photon-counting in PET/CT, dipole-mismodel in EEG/MEG).
- **Resolution-SNR-time trade-off** — pick two.
- **Quantitative bias** — every modality has a systematic offset somewhere; always sanity-check the absolute values.

## A practical mental checklist before any acquisition

- [ ] $B_0$, sequence, TR, TE, TI, flip angle, voxel size, FOV.
- [ ] Phase-encoding direction; fmap available if EPI.
- [ ] Number of averages; receive coil configuration.
- [ ] DWI: b-values, directions, multi-shell or not.
- [ ] fMRI: TR, slice timing, multiband factor.
- [ ] Anything vendor-specific recorded in the BIDS sidecar.

If any of these are unknown when you process the data later, the methods section can't be written honestly.

## References

1. **Haacke EM, Brown RW, Thompson MR, Venkatesan R.** *Magnetic Resonance Imaging: Physical Principles and Sequence Design.* 2nd ed. Wiley-Liss; 2014. ISBN 978-0471720850.
2. **Bernstein MA, King KF, Zhou XJ.** *Handbook of MRI Pulse Sequences.* Academic Press; 2004. ISBN 978-0120928613.
3. **McRobbie DW, Moore EA, Graves MJ, Prince MR.** *MRI from Picture to Proton.* 3rd ed. Cambridge University Press; 2017. ISBN 978-1107643239.
4. **Mansfield P.** Multi-planar image formation using NMR spin echoes. *J Phys C Solid State Phys.* 1977;10(3):L55-L58. [doi:10.1088/0022-3719/10/3/004](https://doi.org/10.1088/0022-3719/10/3/004) — EPI.
5. **Stejskal EO, Tanner JE.** Spin diffusion measurements: spin echoes in the presence of a time-dependent field gradient. *J Chem Phys.* 1965;42(1):288-292. [doi:10.1063/1.1695690](https://doi.org/10.1063/1.1695690)
6. **Ogawa S, Tank DW, Menon R, et al.** Intrinsic signal changes accompanying sensory stimulation: functional brain mapping with magnetic resonance imaging. *PNAS.* 1992;89(13):5951-5955. [doi:10.1073/pnas.89.13.5951](https://doi.org/10.1073/pnas.89.13.5951)
7. **Buxton RB, Wong EC, Frank LR.** Dynamics of blood flow and oxygenation changes during brain activation: the balloon model. *Magn Reson Med.* 1998;39(6):855-864. [doi:10.1002/mrm.1910390602](https://doi.org/10.1002/mrm.1910390602)
8. **Pruessmann KP, Weiger M, Scheidegger MB, Boesiger P.** SENSE: sensitivity encoding for fast MRI. *Magn Reson Med.* 1999;42(5):952-962. [doi:10.1002/(SICI)1522-2594(199911)42:5<952::AID-MRM16>3.0.CO;2-S](https://doi.org/10.1002/(SICI)1522-2594(199911)42:5%3C952::AID-MRM16%3E3.0.CO;2-S)
9. **MR-Tip and MRI Questions** — online primers: [MRI Questions](https://mriquestions.com), [Allen D. Elster's resource](https://mriquestions.com/index.html).
10. **Bushberg JT, Seibert JA, Leidholdt EM Jr, Boone JM.** *The Essential Physics of Medical Imaging.* 4th ed. Lippincott Williams & Wilkins; 2020. ISBN 978-1496386427. — the cross-modality reference textbook.
11. **Kak AC, Slaney M.** *Principles of Computerized Tomographic Imaging.* SIAM; 2001. ISBN 978-0898714944. Free online: [https://engineering.purdue.edu/~malcolm/pct/CTI_Ch00.pdf](https://engineering.purdue.edu/~malcolm/pct/CTI_Ch00.pdf)
12. **Phelps ME.** *PET: Physics, Instrumentation, and Scanners.* Springer; 2006. ISBN 978-0387321288.
13. **Innis RB, Cunningham VJ, Delforge J, et al.** Consensus nomenclature for in vivo imaging of reversibly binding radioligands. *J Cereb Blood Flow Metab.* 2007;27(9):1533-1539. [doi:10.1038/sj.jcbfm.9600493](https://doi.org/10.1038/sj.jcbfm.9600493) — PET kinetic-modelling conventions.
14. **Macé E, Montaldo G, Cohen I, et al.** Functional ultrasound imaging of the brain. *Nat Methods.* 2011;8:662-664. [doi:10.1038/nmeth.1641](https://doi.org/10.1038/nmeth.1641)
15. **Boas DA, Elwell CE, Ferrari M, Taga G.** Twenty years of functional near-infrared spectroscopy: introduction for the special issue. *NeuroImage.* 2014;85(1):1-5. [doi:10.1016/j.neuroimage.2013.11.033](https://doi.org/10.1016/j.neuroimage.2013.11.033)
16. **Hämäläinen M, Hari R, Ilmoniemi RJ, Knuutila J, Lounasmaa OV.** Magnetoencephalography — theory, instrumentation, and applications to noninvasive studies of the working human brain. *Rev Mod Phys.* 1993;65(2):413-497. [doi:10.1103/RevModPhys.65.413](https://doi.org/10.1103/RevModPhys.65.413)
17. **Gross J.** Magnetoencephalography in cognitive neuroscience: a primer. *Neuron.* 2019;104(2):189-204. [doi:10.1016/j.neuron.2019.07.001](https://doi.org/10.1016/j.neuron.2019.07.001)

## Where to next

That closes the Foundations sub-section. From here, the rest of the handbook ([Analysis](../../analysis/index.md), [Data engineering](../../data-engineering/index.md), [AI / ML](../../ai/index.md)) builds on top of the conceptual stack you've just assembled.
