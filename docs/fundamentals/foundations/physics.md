# Physics

> Why a magnetic field and some radio pulses produce a brain image — and what every acquisition parameter is really doing.

You don't need to derive the Bloch equations from Maxwell's, but you do need a working physical model so that a "TE = 35 ms" or "b = 1000 s/mm²" line in a methods section actually tells you something. This page is that working model.

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

## PET physics in one paragraph

A positron-emitting radiotracer (FDG, amyloid-PET ligands) is injected; positrons annihilate with electrons to produce two 511 keV photons in opposite directions; the scanner detects coincidences along lines of response; reconstruction (OSEM, MLEM) produces a 3D tracer-concentration map. Quantitative PET uses arterial input function or reference-region models to estimate kinetic parameters (Ki for FDG glucose uptake, SUVR for binding).

## EEG / MEG physics in one paragraph

Neuronal pyramidal cells generate dipolar currents. Their summed activity produces measurable electric potentials on the scalp (EEG, ~10 µV) and magnetic fields outside the head (MEG, ~10 fT — 8 orders of magnitude below Earth's field, requiring a magnetically shielded room and SQUID sensors). Spatial resolution is poor (~cm) because of head-tissue conductivity; temporal resolution is excellent (~ms).

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

## Where to next

That closes the Foundations sub-section. From here, the rest of the handbook ([Analysis](../../analysis/index.md), [Data engineering](../../data-engineering/index.md), [AI / ML](../../ai/index.md)) builds on top of the conceptual stack you've just assembled.
