# The DWI pipeline as a DE case study

Let's map a typical DWI pipeline onto data-engineering concepts so the bridge to "industry DE" is concrete.

| Stage | What it does | DE primitive |
| --- | --- | --- |
| BIDS dataset | Raw input | **Extract** — source of truth. |
| QSIPrep | Preprocessing (motion, distortion, registration) | **Transform** — cleans and conforms. |
| Recon-all | Cortical surfaces, parcellation | **Transform** — generates a derived view. |
| QSIRecon (HSVS) | Reconstruction using FreeSurfer surfaces | **Join** — requires both QSIPrep output and Recon output. |
| DK connectome | Region-to-region streamline count | **Aggregation** — produces analysis-ready artifact. |
| `dk_connectome.csv` | Final output | **Gold layer** — what downstream consumers query. |

Note the recurring shapes — transformation, join, aggregation — these are the same primitives a tabular pipeline uses; only the data type changes.

## 4.1 The "medallion" architecture

A widely-used industry mental model:

- **Bronze** — raw data as received (your BIDS dataset).
- **Silver** — cleaned, validated, conformed (preprocessed DWI, FreeSurfer subjects dir).
- **Gold** — business-ready / analysis-ready artifacts (connectome CSV, cohort QC summary).

Your DAG already follows this. Most tabular pipelines do too, even if they don't use the colour names. The value of having names: when something is broken, you can say "the silver layer is fine, the gold materialisation is wrong" and everyone instantly knows which step to look at.

## Where to next

[Concepts in depth](concepts.md) — the specific concepts you'll meet daily: ETL vs ELT, idempotency mechanics, determinism, schemas, lineage, partitioning, retries, cost.
