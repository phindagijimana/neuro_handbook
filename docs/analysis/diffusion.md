# Diffusion & tractography

> From a 4D DWI series to a connectome: the standard pipeline.

## Stages

1. **Preprocess** with QSIPrep [Cieslak et al., 2021](https://doi.org/10.1038/s41592-021-01185-5)[^qsiprep] (denoising, motion + distortion correction, registration to T1).
2. **Model** the local diffusion: tensor (single-shell), CSD or NODDI (multi-shell).
3. **Track** fibres through the model field: deterministic (FACT, EuDX) or probabilistic (iFOD2, PFT).
4. **Filter** the streamlines: SIFT / SIFT2 / COMMIT corrects for the over-representation of streamlines in dense regions.
5. **Connectome**: count streamlines connecting each pair of atlas regions.

## Local models

| Model | When | Tool |
| --- | --- | --- |
| **Tensor (DTI)** | Single-shell b ≈ 1000, quick estimates of FA / MD | FSL `dtifit`, MRtrix3 `dwi2tensor` |
| **CSD** | Multi-shell, robust to crossings | MRtrix3 `dwi2fod` |
| **NODDI** | Multi-shell, microstructure indices | AMICO, NODDI Matlab toolbox |
| **DSI / DKI** | Specific high-end protocols | MRtrix3, DIPY |

For a typical research-grade multi-shell acquisition, MRtrix3 CSD is the default. DIPY (Python) is the right choice for prototyping new models [Garyfallidis et al., 2014](https://doi.org/10.3389/fninf.2014.00008)[^dipy].

## Tractography in MRtrix3 [Tournier et al., 2019](https://doi.org/10.1016/j.neuroimage.2019.116137)[^mrtrix]

A minimal pipeline:

```bash
# After QSIPrep — you have preproc_dwi.mif and a 5tt segmentation.
dwi2response dhollander preproc_dwi.mif wm.txt gm.txt csf.txt
dwi2fod msmt_csd preproc_dwi.mif wm.txt wm_fod.mif \
                                    gm.txt gm_fod.mif \
                                    csf.txt csf_fod.mif
tckgen wm_fod.mif tractogram.tck \
    -act 5tt.nii.gz -backtrack -seed_dynamic wm_fod.mif \
    -select 10M -minlength 5 -maxlength 250
tcksift2 tractogram.tck wm_fod.mif weights.txt
```

10 M streamlines is overkill for many uses; 1 M is often enough for connectome construction. Memory and disk grow linearly with `-select`.

## Connectomes

```bash
# Map streamlines to an atlas-defined connectome
tck2connectome tractogram.tck atlas.nii.gz connectome.csv \
    -tck_weights_in weights.txt -symmetric -zero_diagonal
```

The output is an `N x N` matrix where `N` is the number of atlas regions. The Desikan-Killiany atlas gives 84×84 (68 cortical + 16 subcortical). Schaefer-400 + Tian-S4 gives ≈ 450.

The QC `check_connectome_shape` helper in this repo (`neuro_handbook.qc`) is exactly the schema test you should run on every connectome before treating it as analysis-ready.

## What "edge weight" actually means

A connectome's edge can be:

- **Streamline count** — the raw output of `tck2connectome`. Easy to bias by region size.
- **Streamline density** — count divided by region surface area or volume.
- **SIFT-weighted streamline count** — the COMMIT/SIFT correction tries to match diffusion data better.
- **Mean FA along the bundle** — a microstructure-weighted metric.

Always state which one. A "DK connectome" with no specification is ambiguous.

## Pitfalls

- **b-vector flips.** A swapped axis in `.bvec` mirrors your tractogram. Check by running a known commissural seed (corpus callosum) — streamlines should cross.
- **5TT segmentation errors.** Bad cortical / WM boundaries cause streamlines to terminate prematurely. Visualise 5TT before tractography.
- **Over-interpretation.** A streamline is a *modelling artifact*, not a real axon. "There's a connection between A and B" is a hypothesis, not a measurement.

## References

[^mrtrix]: Tournier J-D, Smith R, Raffelt D, et al. MRtrix3. *NeuroImage.* 2019;202:116137. [doi:10.1016/j.neuroimage.2019.116137](https://doi.org/10.1016/j.neuroimage.2019.116137)
[^qsiprep]: Cieslak M, Cook PA, He X, et al. QSIPrep. *Nat Methods.* 2021;18(7):775-778. [doi:10.1038/s41592-021-01185-5](https://doi.org/10.1038/s41592-021-01185-5)
[^dipy]: Garyfallidis E, Brett M, Amirbekian B, et al. DIPY, a library for the analysis of diffusion MRI data. *Front Neuroinform.* 2014;8:8. [doi:10.3389/fninf.2014.00008](https://doi.org/10.3389/fninf.2014.00008)

## Where to next

[Functional connectivity](functional.md) — what the BOLD signal tells you about the same connections.
