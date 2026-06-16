# Bash & CLI

> The shell is how you log into clusters, move data, glue tools, and run pipelines. Treat it as a first-class skill.

This page assumes Linux / macOS. Windows users should use WSL2 ([install guide](https://learn.microsoft.com/en-us/windows/wsl/install)) — neuroimaging tooling is overwhelmingly POSIX-flavoured.

## What Bash is

Bash is an interactive command interpreter and a scripting language. The same syntax works in both modes. Reference [here](https://www.gnu.org/software/bash/manual/bash.html).

```bash
echo $SHELL                              # current login shell
bash --version | head -1                 # version
```

## Strict mode — every script starts with this

```bash
#!/usr/bin/env bash
set -euo pipefail
# -e: exit on error
# -u: error on unset variables
# -o pipefail: pipeline fails if any stage fails
IFS=$'\n\t'                              # safer word-splitting
```

The cost of *not* doing this is silent failures in long-running cluster jobs.

## Variables, quoting, expansion

```bash
SUB="sub-001"                            # no spaces around =
echo "Working on ${SUB}"                 # ${} clarifies boundaries
echo 'Literal: $SUB'                     # single quotes = literal
WORK="${SCRATCH:-/tmp}/${USER}/work"     # ${VAR:-default}
mkdir -p "$WORK"                         # always quote paths
```

Quote variables that may contain spaces (which means: every path).

## Conditionals and exit codes

```bash
if [[ -f "$file" ]]; then
  echo "exists"
fi

if grep -q "ERROR" log.txt; then
  echo "found error"
fi

cmd1 && cmd2                             # cmd2 only if cmd1 succeeds
cmd1 || cmd2                             # cmd2 only if cmd1 fails
test -d "$DIR" || mkdir -p "$DIR"        # idempotent
```

`$?` holds the last exit code. `0` = success.

## Redirection and pipelines

```bash
cmd > out.txt                            # stdout to file (overwrite)
cmd >> out.txt                           # append
cmd 2> err.txt                           # stderr
cmd > all.txt 2>&1                       # combined
cmd1 | cmd2                              # pipe stdout → stdin
```

## Everyday commands

```bash
ls -lah                                  # list, long, all, human sizes
find . -name '*.nii.gz' -size +50M       # large NIfTI files
find . -name '*_bold.nii.gz' -mtime -7   # modified in last 7 days
grep -ri "ERROR" logs/                   # recursive case-insensitive
wc -l participants.tsv                   # line count
sort -u subjects.txt                     # unique-sorted
head -n 5 file.tsv ; tail -n 5 file.tsv
du -sh derivatives/*                     # sizes per subdir
df -h                                    # filesystem usage
rsync -av --progress src/ dst/           # incremental copy
```

`find` and `rsync` deserve their own afternoon ([find man](https://man7.org/linux/man-pages/man1/find.1.html), [rsync man](https://man7.org/linux/man-pages/man1/rsync.1.html)).

## awk and sed — the text-processing duo

```bash
# awk: sum column 3 in a TSV, skipping the header
awk 'NR > 1 { sum += $3 } END { print sum }' participants.tsv

# awk: print subject_id where age > 60
awk -F'\t' 'NR == 1 { for (i=1; i<=NF; i++) col[$i]=i; next }
            $col["age"] > 60 { print $col["subject_id"] }' participants.tsv

# sed: replace pattern in place (BSD/GNU differ on -i)
sed -i.bak 's/REPLACE_ME/foo/g' template.sh
```

`awk` is a complete language; the [GNU awk manual](https://www.gnu.org/software/gawk/manual/) repays a deep read.

## Subject-wise loops

```bash
for sub in sub-001 sub-002 sub-003; do
  echo "=== $sub ==="
  apptainer run mriqc.sif /data /out participant --participant-label "${sub#sub-}"
done

# Or from a file:
while IFS= read -r sub; do
  echo "processing $sub"
done < subjects.txt
```

## Functions for reuse

```bash
process_subject() {
  local sub="$1"
  local out="$2"
  local img="$WORK/${sub}.nii.gz"
  [[ -f "$img" ]] || { echo "missing $img"; return 1; }
  fslstats "$img" -M -S > "$out/${sub}_stats.txt"
}

process_subject sub-001 results/
```

## HPC patterns (Slurm + Apptainer)

A production submission script — see [Computing → HPC and Slurm](../../computing/hpc-slurm.md) for the full exemplar:

```bash
#!/usr/bin/env bash
#SBATCH --job-name=qc
#SBATCH --array=1-100%20
#SBATCH --time=02:00:00
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
set -euo pipefail

subjects=( $(cat subjects.txt) )
sub=${subjects[$SLURM_ARRAY_TASK_ID - 1]}

apptainer run -B "$DATA":/data:ro -B "$OUT":/out mriqc.sif \
  /data /out participant --participant-label "$sub"
```

## Safety patterns

- **`set -euo pipefail`** at the top of every script.
- **`rm`** — never `rm -rf $variable` without confirming `$variable` is non-empty (`[[ -n "$d" ]] && rm -rf "$d"`). Even safer: `trash-cli`.
- **`mktemp`** for temporary files / dirs: `tmp=$(mktemp -d)`, then `trap 'rm -rf "$tmp"' EXIT`.
- **Quote everything** — `"$var"`, not `$var`.
- **`-i.bak`** with `sed -i` keeps a backup.

## When to stop using Bash

Bash is great glue and terrible for: arithmetic, complex data structures, anything > 200 lines, anything that touches more than one file format. Rewrite in Python before that point.

## Working with NIfTI from the CLI

Most BIDS-app tools expose a CLI. FSL conventions ([docs](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/)):

```bash
fslhd sub-001_T1w.nii.gz                 # header info
fslstats sub-001_T1w.nii.gz -M -S        # mean, stddev within nonzero mask
fslroi input.nii.gz output.nii.gz 0 64 0 64 0 30 0 100   # crop
fslmaths a.nii.gz -add b.nii.gz sum.nii.gz                # voxelwise arithmetic
```

AFNI and MRtrix3 have analogous CLIs.

## References

1. **Newham C, Rosenblatt B.** *Learning the Bash Shell.* 3rd ed. O'Reilly; 2005. ISBN 978-0596009656.
2. **Robbins A.** *bash Pocket Reference.* 2nd ed. O'Reilly; 2016. ISBN 978-1491941591.
3. **GNU Bash Reference Manual.** [https://www.gnu.org/software/bash/manual/bash.html](https://www.gnu.org/software/bash/manual/bash.html)
4. **Robbins A, Dougherty D.** *sed & awk.* 2nd ed. O'Reilly; 1997. ISBN 978-1565922259.
5. **Sobell MG.** *A Practical Guide to Linux Commands, Editors, and Shell Programming.* 4th ed. Pearson; 2017. ISBN 978-0134774602.
6. **The Slurm documentation.** [https://slurm.schedmd.com/documentation.html](https://slurm.schedmd.com/documentation.html)

## Where to next

[MATLAB](matlab.md) — the second-most-common neuroimaging-analysis language, especially on the SPM / EEGLAB / FieldTrip side.
