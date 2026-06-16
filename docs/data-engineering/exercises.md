# Exercises

Each exercise is a small, contained task in your current repo. Sized at a few hours; not a weekend.

1. **Draw the DAG** of your existing pipeline by hand, including any dotted-line dependency (e.g., a `.lta` registration consumed two steps later). Save it as `docs/dag.png` (Mermaid, Graphviz, or paper photo).

2. **Make `run_recon()` content-addressable**: cache key = sha256 of (T1w nifti + container hash + tool flag). Skip if a hash file already exists. Compare with the current mtime / existence check.

3. **Add a `manifest.json` per subject** capturing: subject ID, container SHA, git SHA, start / end timestamps, exit code per stage, host name, peak RSS (from `seff` / `time -v`).

4. **Write three data tests** (any framework, or hand-rolled `pytest`):
    - DK matrix is 84×84 numeric.
    - Tractogram count is between 100 k and 100 M.
    - Every QSIPrep `*.bval` parses and contains at least one b > 0.

5. **Implement atomic writes** for the DK CSV: write `dk_connectome.csv.tmp` then `mv`. Verify by killing the job mid-write and re-running — the output should never be half-written.

6. **Introduce a Pydantic config object** (`dwi_pipeline/config.py`) that mirrors today's env vars. Replace `${RESULTS_ROOT:-…}` with `cfg.results_root`. Run with both a valid and an invalid config; observe the error surface.

7. **Add a `--dry-run` flag** to `submit.sh` that prints the planned `sbatch` command without submitting and a list of subjects that would actually be processed (skipping those already complete).

8. **Port one stage to Snakemake** — `recon` is a good first choice because it has clear inputs and outputs. Get `snakemake --executor slurm -j 2` to run it for `sub-001` and `sub-007`.

9. **Build the cohort-summary DuckDB** (Milestone 4 lite): load `dk_connectome.csv` from every subject into a single table; write a SQL query that returns mean edge weight per (`subject`, `source_region`).

10. **Write a one-page runbook**, `docs/runbook_recon_failed.md`: symptoms, common causes, diagnostic commands, remediation, escalation.

## Where to next

If you've worked through several of these, you're ready for [Advanced topics](advanced/index.md) — data modeling, lakehouses, Spark, streaming, dbt, and the rest of the senior DE landscape.
