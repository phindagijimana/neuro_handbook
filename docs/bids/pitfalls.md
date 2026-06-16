# Common BIDS pitfalls

> The bugs that bite real pipelines. Most are not in the spec — they're at the seams.

## Subject ID collisions

`sub-001` and `sub-01` look similar; the spec treats them as different subjects. Worse, some validators coerce one to the other on Windows because of case-insensitive paths.

**Mitigation.** Pick one zero-padding convention (`sub-001` for ≤ 999 subjects, `sub-0001` for ≤ 9999) and enforce it at conversion time. Validate every new dataset on a Linux runner before merging.

## IntendedFor

A `fmap/` sidecar carries an `IntendedFor` field listing which BOLD/DWI runs it corrects. If the path is wrong (typos, mismatched session prefixes, missing extension), the BIDS app silently skips the fieldmap and your distortion correction is just gone.

**Mitigation.**

- Write `IntendedFor` programmatically, not by hand.
- Use the `bids::` URI form introduced in BIDS 1.8 — paths are dataset-relative and clearer.
- Add a test that every `IntendedFor` path exists.

## Sidecar inheritance

BIDS lets a JSON at a higher level (root or subject) apply to all files below. fMRIPrep / QSIPrep read this inheritance correctly; many home-grown scripts do not.

**Mitigation.** Either commit fully-resolved sidecars next to each `.nii.gz`, or test the *resolved* metadata through PyBIDS (`f.get_metadata()`), not by reading the JSON file directly.

## TaskName in BOLD sidecars

Every `*_bold.nii.gz` needs a `TaskName` in its JSON sidecar. Forgetting this trips most BIDS apps. The converter usually puts it there; if you hand-edit, don't drop it.

## Phase-encoding direction

`PhaseEncodingDirection: j-` vs `j` (or `i-` vs `i`) matters for distortion correction. A single character flip inverts your correction.

**Mitigation.** Read the direction off the scanner protocol once, document it, and have the conversion fail loudly if a series produces a different direction.

## EventTSV files

Task fMRI runs need a `*_events.tsv`. Required columns: `onset` (seconds, from start of run), `duration` (seconds). Common bug: storing onsets in milliseconds, or relative to the trigger pulse rather than the first volume. Off by 1.5 seconds × TR; your statistics quietly degrade.

## participants.tsv vs sessions.tsv

`participants.tsv` describes one row per subject; `sub-XXX/sub-XXX_sessions.tsv` describes one row per session. Some pipelines look for both; others only one. When subjects don't have the columns expected, the BIDS app reports demographics as `None`.

## Special characters

BIDS IDs are alphanumeric only. No underscores in subject labels (`sub-001_a` ≠ `sub-001` ≠ `sub-001a`). The validator catches this but it's a common surprise.

## On-disk encoding

UTF-8 with `\n` line endings everywhere. CRLF in a `.tsv` from Windows can break parsers downstream. Pin git's `core.autocrlf=false` for BIDS repos.

## Where to next

You've completed the BIDS toolkit section. Move to [Analysis](../analysis/index.md) for what to do with the data once it's organised.
