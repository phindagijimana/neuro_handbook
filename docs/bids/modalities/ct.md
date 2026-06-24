# CT in BIDS

> BEP024 brings Computed Tomography into the BIDS family — folder layout, suffixes, required JSON sidecars, and the conversion path from DICOM.

!!! warning "BEP024 is still a draft proposal"
    As of 2026, [BEP024 — Computed Tomography scan](https://bids.neuroimaging.io/extensions/) (lead: Hugo Boniface) is **in the Google-Doc / proposal stage** — not yet merged into the stable [BIDS specification](https://bids-specification.readthedocs.io). The folder structure and sidecar fields described here follow the published BEP024 proposal and represent the convention users should adopt in anticipation. Verify status before publishing a CT-BIDS dataset:
    - [BIDS Extensions page](https://bids.neuroimaging.io/extensions/)
    - [bids-standard/bids-specification PRs](https://github.com/bids-standard/bids-specification/pulls?q=CT) — search for CT / computed-tomography PRs
    - [bids-standard issue tracker](https://github.com/bids-standard/bids-specification/issues?q=CT) — open issues on CT support
    
    Where the spec is silent or in flux, this page errs toward the conventions already merged for `anat/` (suffix-style entities, sidecar conventions) and notes the divergence explicitly.

Course map: spec status → folder layout → suffixes → entities → required JSON → recommended JSON → conversion recipes → validation → pitfalls → disease use → tools → refs → next.

## Folder layout — one-glance

```text
ds-ct/
├── dataset_description.json
├── participants.tsv
└── sub-01/
    ├── ses-baseline/
    │   ├── anat/
    │   │   └── sub-01_ses-baseline_T1w.nii.gz       # optional MR for fusion
    │   └── ct/
    │       ├── sub-01_ses-baseline_ct.nii.gz                       # non-contrast CT
    │       ├── sub-01_ses-baseline_ct.json
    │       ├── sub-01_ses-baseline_ce-iodine_ctangio.nii.gz        # CT angiography
    │       ├── sub-01_ses-baseline_ce-iodine_ctangio.json
    │       ├── sub-01_ses-baseline_ce-iodine_ctperf.nii.gz         # 4D CT perfusion
    │       ├── sub-01_ses-baseline_ce-iodine_ctperf.json
    │       └── sub-01_ses-baseline_ce-iodine_acq-mip_ctangio.nii.gz # MIP reformat
    └── ses-followup/
        └── ct/
            └── sub-01_ses-followup_ct.nii.gz
```

The `ct/` folder sits alongside `anat/` (for MR-CT fusion in radiotherapy planning and stereotactic neurosurgery) and is the only data-type folder for pure-CT studies. Cross-link: [fundamentals/sequences/ct.md](../../fundamentals/sequences/ct.md) for the physics, [analysis/ct.md](../../analysis/ct.md) for downstream processing.

## Allowed suffixes (BEP024 proposal)

| Suffix | What it is |
|---|---|
| `ct` | The main 3D CT volume — NCCT, contrast-enhanced CT (with `ce-`), or any single-pass acquisition |
| `ctangio` | CT angiography — single helical pass timed to iodinated arterial bolus |
| `ctperf` | CT perfusion — 4D dynamic (repeated axial passes after contrast bolus) |
| `ctmip` | Maximum-intensity-projection reformat (vessel-tree visualisation) |

Note: BEP024 may evolve these. Some early proposals collapse `ctangio` / `ctperf` into entity variants of a single `ct` suffix (e.g., `_acq-angio_ct`). Track the proposal commit for your dataset.

## Filename entities — in order

```
sub-<label>[_ses-<label>][_acq-<label>][_ce-<label>][_rec-<label>][_run-<index>][_chunk-<index>]_<suffix>.<ext>
```

| Entity | Used when | Example |
|---|---|---|
| `sub-` | always | subject label |
| `ses-` | longitudinal | baseline, followup, stroke-day-1 |
| `acq-` | distinguish protocols sharing a suffix | `acq-thinslice`, `acq-mip` |
| `ce-` | contrast enhancement | `ce-iodine` for iodinated; `ce-none` for non-contrast (often omitted) |
| `rec-` | different reconstruction kernel | `rec-soft`, `rec-bone`, `rec-iter`, `rec-dlr` |
| `run-` | repeated identical-protocol scans | `run-01`, `run-02` |
| `chunk-` | multi-pass acquisitions | reserved for the 4D CTP frame stack when split |

The validator enforces this order. `sub-01_run-01_acq-thinslice_ct.nii.gz` will fail; the correct form is `sub-01_acq-thinslice_run-01_ct.nii.gz`.

## Required JSON sidecar fields (BEP024 proposal)

The proposal partitions required fields into acquisition, dose, reconstruction, and hardware blocks. Skip none — `n/a` is acceptable in a handful of places (noted).

### Acquisition

| Field | Type | Example |
|---|---|---|
| `KVP` | number (kV) | `120` |
| `XRayTubeCurrent` | number (mA) | `300` |
| `ExposureTime` | number (s) | `0.5` |
| `RotationTime` | number (s) | `0.5` |
| `PitchFactor` | number | `0.984` |
| `SliceThickness` | number (mm) | `5.0` |
| `SpacingBetweenSlices` | number (mm) | `5.0` |
| `DataCollectionDiameter` | number (mm) | `500` |
| `ReconstructionDiameter` | number (mm) | `220` |

### Reconstruction

| Field | Type | Example |
|---|---|---|
| `ConvolutionKernel` | string | `"H30s"` (Siemens), `"FC18"` (Canon), `"Br36"` (Siemens) |
| `FilterType` | string | `"FBP"`, `"ASIR-V"`, `"AIDR-3D"`, `"MBIR"`, `"DLR"` |
| `IterativeReconstructionLevel` | string or `"n/a"` | `"60%"` (ASIR-V), `"strong"` (AIDR-3D) |

### Contrast (when `ce-` entity is present)

| Field | Type | Example |
|---|---|---|
| `ContrastBolusAgent` | string | `"Iohexol 350"`, `"Iopamidol 370"` |
| `ContrastBolusVolume` | number (mL) | `70` |
| `ContrastBolusIngredient` | string | `"Iodine"` |
| `ContrastBolusIngredientConcentration` | number (mg/mL) | `350` |
| `ContrastFlowRate` | number (mL/s) | `4.5` |
| `ContrastBolusStartTime` | string (HH:MM:SS) | `"10:32:15"` |

### Dose

| Field | Type | Example |
|---|---|---|
| `CTDIvol` | number (mGy) | `52.4` |
| `DoseLengthProduct` | number (mGy·cm) | `1042` |
| `ExposureModulationType` | string | `"XYZ_EC"`, `"Z_EC"`, `"None"` |

### Hardware

| Field | Type | Example |
|---|---|---|
| `Manufacturer` | string | `"Siemens"` |
| `ManufacturersModelName` | string | `"SOMATOM Force"` |
| `SoftwareVersions` | string | `"syngo CT VA50A"` |
| `InstitutionName` | string | `"URMC"` |

### Minimal sidecar — copy-paste

```json
{
  "Manufacturer": "Siemens",
  "ManufacturersModelName": "SOMATOM Force",
  "SoftwareVersions": "syngo CT VA50A",
  "InstitutionName": "URMC",
  "KVP": 120,
  "XRayTubeCurrent": 300,
  "ExposureTime": 0.5,
  "RotationTime": 0.5,
  "PitchFactor": 0.984,
  "SliceThickness": 5.0,
  "SpacingBetweenSlices": 5.0,
  "DataCollectionDiameter": 500,
  "ReconstructionDiameter": 220,
  "ConvolutionKernel": "H30s",
  "FilterType": "ADMIRE",
  "IterativeReconstructionLevel": "3",
  "CTDIvol": 52.4,
  "DoseLengthProduct": 1042,
  "ExposureModulationType": "XYZ_EC"
}
```

For a contrast-enhanced or perfusion acquisition, add the contrast block:

```json
{
  "ContrastBolusAgent": "Iohexol 350",
  "ContrastBolusVolume": 70,
  "ContrastBolusIngredient": "Iodine",
  "ContrastBolusIngredientConcentration": 350,
  "ContrastFlowRate": 4.5,
  "ContrastBolusStartTime": "10:32:15"
}
```

## Recommended JSON fields

| Field | Why it matters |
|---|---|
| `TableSpeed` | mm/s; reconstructs pitch when not directly recorded |
| `ScanOptions` | DICOM tag (0018,0022) — `"AXIAL_CT_MODE"`, `"HELICAL_CT"`, `"PERFUSION"` |
| `ReconstructionTargetCenterPatient` | x, y, z target centre in patient coordinates |
| `GeneratorPower` | tube power (kW) at acquisition |
| `FocalSpot` | small / large focal-spot selection |
| `BodyPartExamined` | `"HEAD"`, `"NECK"`, `"CHEST"` — downstream pipelines filter on this |
| `Modality` | always `"CT"` |
| `EstimatedDoseSaving` | when iterative or DL reconstruction is in use |
| `AcquisitionDateTime` | full timestamp; useful for longitudinal datasets |
| `DeidentificationMethod` | audit trail per [BIDS 1.10](https://bids-specification.readthedocs.io/en/latest/common-principles.html#deidentification) |

## CT perfusion — the 4D special case

CTP is the most awkward acquisition for BIDS because it is *dynamic*: repeated axial passes every 1-2 s for 60-90 s after a contrast bolus produce a 4D volume in NIfTI (x, y, z, t). The BEP024 proposal handles this with the `ctperf` suffix and per-frame timing fields analogous to PET:

| Field | Type | Notes |
|---|---|---|
| `FrameTimesStart` | array of numbers (s) | Per-frame start time relative to `TimeZero` or `ContrastBolusStartTime` |
| `FrameDuration` | array of numbers (s) | Per-frame duration; `len == N_frames` |
| `ContrastBolusStartTime` | string (HH:MM:SS) | Anchor for the timing arrays |
| `NumberOfTemporalPositions` | integer | Number of dynamic frames |

The 4D NIfTI's fourth dimension must match `len(FrameTimesStart)` and `NumberOfTemporalPositions`.

Some early adopters store CTP as a sequence of 3D NIfTIs with `chunk-` entities instead of a 4D file; both are defensible — pick one per dataset and document in `dataset_description.json`.

## Conversion recipes

### DICOM → BIDS-CT with `dcm2niix`

[`dcm2niix`](https://github.com/rordenlab/dcm2niix) has native CT support and writes BIDS-style sidecars. For a single CT series:

```bash
# Single subject, single series
dcm2niix -b y -ba y -z y \
  -f "sub-%i_%d" \
  -o bids/sub-01/ses-baseline/ct/ \
  raw/sub-01/ct/
```

`-b y` writes the JSON sidecar; `-ba y` anonymises; `-z y` gzip-compresses the NIfTI. For 4D CTP, `dcm2niix` collapses repeated axial passes into a 4D NIfTI automatically when the temporal dimension is encoded in `(0020,0100)` or the equivalent.

### HeuDiConv pattern

For a small batch with a fixed naming convention, [HeuDiConv](https://heudiconv.readthedocs.io) is the right tool:

```python
def infotodict(seqinfo):
    ct      = create_key("sub-{subject}/[ses-{session}/]ct/sub-{subject}[_ses-{session}]_ct")
    ctangio = create_key("sub-{subject}/[ses-{session}/]ct/sub-{subject}[_ses-{session}]_ce-iodine_ctangio")
    ctperf  = create_key("sub-{subject}/[ses-{session}/]ct/sub-{subject}[_ses-{session}]_ce-iodine_ctperf")
    info = {ct: [], ctangio: [], ctperf: []}
    for s in seqinfo:
        pn = s.protocol_name.upper()
        if "NON_CON" in pn or "NCCT" in pn:
            info[ct].append(s.series_id)
        elif "ANGIO" in pn or "CTA" in pn:
            info[ctangio].append(s.series_id)
        elif "PERF" in pn or "CTP" in pn:
            info[ctperf].append(s.series_id)
    return info
```

After conversion, post-process the sidecar to add the BEP024-required fields that `dcm2niix` does not emit (`PitchFactor`, `CTDIvol`, `DoseLengthProduct`, `IterativeReconstructionLevel`).

### Programmatic sidecar enrichment

```python
import json
from pathlib import Path
import pydicom

src_dcm  = pydicom.dcmread(next(Path("raw/sub-01/ct/").rglob("*.dcm")))
side     = Path("bids/sub-01/ses-baseline/ct/sub-01_ses-baseline_ct.json")
meta     = json.loads(side.read_text())

meta["PitchFactor"]                  = float(src_dcm.get((0x0018, 0x9311), 1.0))
meta["CTDIvol"]                      = float(src_dcm.get((0x0018, 0x9345), 0.0))
meta["DoseLengthProduct"]            = float(src_dcm.get((0x0018, 0x9346), 0.0))
meta["IterativeReconstructionLevel"] = str(src_dcm.get((0x0018, 0x9739), "n/a"))
side.write_text(json.dumps(meta, indent=2))
```

The DICOM dose-report tags (CTDIvol = `(0018,9345)`, DLP = `(0018,9346)`) are part of the IEC dose-report module and reliably populated by all modern vendors.

## Validation checks

The mainline [bids-validator](https://bids-standard.github.io/bids-validator/) does not (yet, while BEP024 is in draft) understand the `ct/` folder. Until merger, validate the rest of the dataset (subjects, sessions, anat) with the official validator and manually verify the CT block. Things to look for:

- `len(FrameTimesStart) == len(FrameDuration) == N_frames_in_nifti` for `ctperf`.
- `CTDIvol` and `DoseLengthProduct` populated — these are auditable dose metrics, not optional.
- `KVP` numeric, not string ("120" vs 120).
- `ConvolutionKernel` matches the vendor's actual exported kernel; some sites strip this in PACS export.
- `Modality == "CT"` in the sidecar and in every contributing DICOM (no MR slipping into the `ct/` folder).

## Common pitfalls

1. **Multi-bolus CT-perfusion stacking.** A CTP acquisition is dynamic — `dcm2niix` will sometimes split passes into separate NIfTIs if the temporal-dimension DICOM tag is wonky. Inspect the output dimensionality; if you have N separate 3D files instead of one 4D, recombine with `fslmerge -t` or `nibabel.concat_images`.
2. **`ce-iodine` vs `ce-Iodine` vs `ce-iohexol`.** BIDS labels are case-sensitive but otherwise free-form. Pick a convention and apply it everywhere — most sites use `ce-iodine` generically; document the actual agent in `ContrastBolusAgent`.
3. **Beam-hardening artifact** is not a BIDS issue, but document any known artefacts in the dataset README; downstream pipelines can sometimes flag affected scans automatically.
4. **Dual-energy CT (DECT)** vendor naming is inconsistent — Siemens dual-source, GE GSI fast-kVp switching, Philips spectral-detector — and BEP024 is still finalising the entity scheme. For now, store each energy as a separate file with `acq-low` / `acq-high` and record `KVP` per file; revisit when BEP024 stabilises a DECT schema.
5. **Photon-counting CT (PCCT)** is very new (FDA-cleared 2021); the BEP024 proposal may have limited explicit coverage. Use the `ct` suffix and capture detector specifics in a custom `Detector` field, documenting the convention in your README until the spec catches up.
6. **Reconstruction-kernel proliferation.** Most clinical CT exports include both soft-tissue and bone reconstructions of the same raw data. Use `rec-soft` and `rec-bone` to disambiguate; do not bury them in `acq-`.
7. **Iterative-reconstruction level encoding.** Vendors use percentages (ASIR-V "60%"), strength labels (AIDR-3D "strong"), and integer scales (ADMIRE "3"). Keep the vendor's native string in `IterativeReconstructionLevel`; do not normalise to a fictional cross-vendor scale.
8. **Anonymisation footgun.** DICOM CT exports often contain the patient's date of birth in the `(0010,0030)` tag and the exact study time in `(0008,0030)`. The dose-report `(0018,9346)` and structured-report sequences can leak private headers if not scrubbed. Use `dcm2niix -ba y` plus a Lua / `dicom-anonymizer` pass.

## Disease-specific use cases

- **Acute ischemic stroke**: store the canonical three-step protocol as `_ct`, `_ce-iodine_ctangio`, `_ce-iodine_ctperf` in one session. Cross-link [clinical/stroke-and-tbi.md](../../clinical/stroke-and-tbi.md).
- **Intracerebral hemorrhage (ICH)**: NCCT-only — store as `_ct`; ICH volume derived in `derivatives/<pipeline>/sub-XX/ct/sub-XX_desc-ich_mask.nii.gz`.
- **Traumatic brain injury (TBI)**: store NCCT in both soft-tissue and bone reconstructions — `_rec-soft_ct` and `_rec-bone_ct`. The bone window is essential for fracture detection.
- **Subarachnoid hemorrhage (SAH)**: NCCT as `_ct`; the modified Fisher grade lives in `participants.tsv` or per-session phenotype TSV.
- **Tumour staging (when MR contraindicated)**: contrast-enhanced CT as `_ce-iodine_ct`; pre-contrast NCCT as `_ct` in the same session.
- **Brain death adjunct**: CTA — `_ce-iodine_ctangio` — with a structured-report sidecar noting circulatory-arrest finding.

## Software & resources

| Tool | Role | Link |
|---|---|---|
| [dcm2niix](https://github.com/rordenlab/dcm2niix) | Primary DICOM → NIfTI converter with native CT support | github.com/rordenlab/dcm2niix |
| [HeuDiConv](https://heudiconv.readthedocs.io) | Heuristic-driven BIDS routing for batch curation | heudiconv.readthedocs.io |
| [Dcm2Bids](https://unfmontreal.github.io/Dcm2Bids/) | JSON-config converter (alternative to HeuDiConv) | unfmontreal.github.io |
| [bids-validator](https://bids-standard.github.io/bids-validator/) | Validate the rest of the dataset; manual check for CT until BEP024 merges | bids-standard.github.io |
| [pydicom](https://pydicom.github.io) | Programmatic DICOM tag access for sidecar enrichment | pydicom.github.io |
| [highdicom](https://highdicom.readthedocs.io) | Modern Python API for structured reports and CT segmentations | highdicom.readthedocs.io |

## References & spec links

- BIDS specification — [bids-specification.readthedocs.io](https://bids-specification.readthedocs.io/en/latest/) (stable).
- BIDS extensions page — [bids.neuroimaging.io/extensions](https://bids.neuroimaging.io/extensions/) (lists BEP024 status; verify before publishing).
- BEP024 proposal: [bids.neuroimaging.io/extensions/](https://bids.neuroimaging.io/extensions/) — Computed Tomography scan, lead Hugo Boniface.
- Gorgolewski KJ, Auer T, Calhoun VD, et al. The brain imaging data structure, a format for organizing and describing outputs of neuroimaging experiments. *Sci Data.* 2016;3:160044. [doi:10.1038/sdata.2016.44](https://doi.org/10.1038/sdata.2016.44) — the original BIDS paper.
- Hounsfield GN. Computerized transverse axial scanning (tomography): Part 1. Description of system. *Br J Radiol.* 1973;46(552):1016-1022. [doi:10.1259/0007-1285-46-552-1016](https://doi.org/10.1259/0007-1285-46-552-1016) — the HU scale.
- Rorden C, Bonilha L, Fridriksson J, Bender B, Karnath HO. Age-specific CT and MRI templates for spatial normalization. *NeuroImage.* 2012;61(4):957-965. [doi:10.1016/j.neuroimage.2012.03.020](https://doi.org/10.1016/j.neuroimage.2012.03.020) — the CT-template work most CT-BIDS pipelines warp to.

## Where to next

- Physics + reconstruction: [fundamentals/sequences/ct.md](../../fundamentals/sequences/ct.md).
- Analysis pipeline: [analysis/ct.md](../../analysis/ct.md) — HU calibration, ASPECTS, CTP deconvolution.
- Clinical context: [clinical/stroke-and-tbi.md](../../clinical/stroke-and-tbi.md) — the trials behind the three-step CT protocol.
- DICOM-to-BIDS mental model that applies here too: [bids/dicom-to-bids.md](../dicom-to-bids.md).
- Derivative layout once you have segmentations and quantitative maps: [bids/derivatives.md](../derivatives.md).
