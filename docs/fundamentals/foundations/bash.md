# Bash

> Bash as a programming language: variables, control flow, functions, scripts, strict mode, and the orchestration patterns that show up in every HPC neuroimaging pipeline.

This page is about Bash **the language**. The companion page [CLI commands](cli.md) catalogues the *individual programs* (`ls`, `cp`, `rsync`, `ssh`, …) that Bash glues together.

## 1. What Bash is

Bash (**B**ourne **A**gain **SH**ell) is an interactive command interpreter *and* a scripting language. Both modes share the same syntax. The canonical reference is the [GNU Bash manual](https://www.gnu.org/software/bash/manual/bash.html).

```bash
echo $SHELL                              # current login shell
bash --version | head -1                 # version string
```

When you write a `.sh` file, line 1 is the **shebang**:

```bash
#!/usr/bin/env bash
# everything below is a Bash program
```

`env bash` is portable across Linux, macOS, and HPC nodes; `/bin/bash` is also common but assumes a fixed path.

## 2. Strict mode — every script starts with this

```bash
#!/usr/bin/env bash
set -euo pipefail
# -e: exit on error
# -u: error on unset variables
# -o pipefail: a pipeline fails if any stage fails
IFS=$'\n\t'                              # safer word-splitting
```

Three flags + one IFS line; that's the single highest-leverage thing you can put in a script. The cost of *not* doing this is silent failures inside long cluster jobs.

## 3. Variables, quoting, expansion

```bash
SUB="sub-001"                            # no spaces around =
echo "Working on ${SUB}"                 # ${} clarifies boundaries
echo 'Literal: $SUB'                     # single quotes = literal
WORK="${SCRATCH:-/tmp}/${USER}/work"     # ${VAR:-default}
mkdir -p "$WORK"                         # always quote paths
```

Parameter expansion is a small mini-language:

```bash
${VAR:-default}        # value or default
${VAR:=default}        # set if unset
${VAR:?message}        # error out if unset
${VAR%pattern}         # strip shortest suffix matching pattern
${VAR%%pattern}        # strip longest suffix
${VAR#pattern}         # strip shortest prefix
${VAR##pattern}        # strip longest prefix
${VAR/pattern/repl}    # replace first match
${VAR//pattern/repl}   # replace all
${#VAR}                # string length
```

Rule of thumb: **quote every variable that may contain spaces** — which means every path.

## 4. Conditionals and exit codes

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

Common `[[ ... ]]` tests:

| Test | True when |
|---|---|
| `-f FILE` | file exists |
| `-d DIR` | directory exists |
| `-e PATH` | anything exists at path |
| `-s FILE` | file exists and is non-empty |
| `-r FILE` | file is readable |
| `-w FILE` | writable |
| `-x FILE` | executable |
| `STR == pat` | glob match (in `[[ ]]`) |
| `STR =~ regex` | regex match |
| `n -eq m` | numeric equal |
| `n -lt m` | numeric less-than |

`$?` holds the last command's exit code. `0` = success; non-zero = failure.

## 5. Loops

```bash
# C-style
for i in {1..10}; do
  echo "iter $i"
done

# Iterate over filenames safely
for f in sub-*/anat/*_T1w.nii.gz; do
  echo "processing $f"
done

# Iterate over a file of subjects
while IFS= read -r sub; do
  echo "$sub"
done < subjects.txt

# Until loop
until pingable host; do
  sleep 5
done
```

The `IFS= read -r` form preserves leading whitespace and backslashes; use it for paths.

## 6. Redirection — the language operators

```bash
cmd > out.txt                            # stdout to file (overwrite)
cmd >> out.txt                           # append
cmd 2> err.txt                           # stderr only
cmd > all.txt 2>&1                       # combine to one file
cmd1 | cmd2                              # pipe cmd1 stdout → cmd2 stdin
cmd <<< "string"                         # here-string
cmd <<EOF
multi-line
input
EOF
```

Process substitution is a powerful next step:

```bash
diff <(sort a.tsv) <(sort b.tsv)         # diff two on-the-fly streams
join <(awk 'NR>1' a.tsv) <(awk 'NR>1' b.tsv)
```

## 7. Functions for reuse

Functions are the single biggest gain over "one giant script":

```bash
process_subject() {
  local sub="$1"
  local out="$2"
  local img="$WORK/${sub}.nii.gz"
  [[ -f "$img" ]] || { echo "missing $img" >&2; return 1; }
  fslstats "$img" -M -S > "${out}/${sub}_stats.txt"
}

process_subject "sub-001" "results/"
```

Patterns to copy:

- `local var` inside functions; never leak shell variables.
- `"$1"`, `"$2"` for positional arguments; `"$@"` for "all the rest".
- Return non-zero on error; log to stderr with `>&2`.
- Treat each function like a tiny script.

## 8. Arrays

Bash arrays are 0-indexed and support both numeric and associative variants:

```bash
subs=( "sub-001" "sub-002" "sub-003" )
echo "${subs[0]}"                        # first
echo "${subs[@]}"                        # all
echo "${#subs[@]}"                       # length
for s in "${subs[@]}"; do echo "$s"; done

declare -A modality_to_dir
modality_to_dir[anat]="anatomy"
modality_to_dir[func]="functional"
echo "${modality_to_dir[anat]}"
```

Arrays are how you safely pass *lists of paths with spaces* around.

## 9. Subject-wise automation — the canonical pattern

```bash
process_subject() {
  local sub="$1"
  fmriprep --participant-label "$sub" "$BIDS" "$DERIV" participant
}

mapfile -t subjects < subjects.txt        # read file into array

for sub in "${subjects[@]}"; do
  process_subject "$sub" || echo "FAILED $sub" >> failures.log
done
```

For cluster scale, replace the `for` with an `sbatch --array`.

## 10. HPC / Slurm patterns

A Slurm batch script *is* a Bash script. Strict mode + parameter expansion give you robust submissions:

```bash
#!/usr/bin/env bash
#SBATCH --job-name=qc
#SBATCH --array=1-100%20
#SBATCH --time=02:00:00
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --output=logs/%x_%A_%a.out
set -euo pipefail

# Pick this task's subject from a file
subjects=( $(cat subjects.txt) )
sub="${subjects[$SLURM_ARRAY_TASK_ID - 1]}"

# Containerised invocation
apptainer run \
  -B "$BIDS":/data:ro \
  -B "$DERIV":/out \
  -B "$FS_LICENSE":/license.txt:ro \
  mriqc.sif \
  /data /out participant \
  --participant-label "$sub" \
  --nthreads "$SLURM_CPUS_PER_TASK"
```

See [Computing → HPC and Slurm](../../computing/hpc-slurm.md) for the full exemplar.

## 11. `trap` — clean up on exit

```bash
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT INT TERM        # always clean up
# ... use $tmp ...
```

`trap` makes scripts safe under SIGINT, SIGTERM, or normal exit.

## 12. Debugging

```bash
bash -x script.sh                         # trace every line
set -x                                    # turn tracing on
set +x                                    # turn it off

shellcheck script.sh                      # lint
```

[ShellCheck](https://www.shellcheck.net) catches ~95% of beginner bugs (unquoted variables, wrong test syntax, useless `cat`). Run it on every script before committing.

## 13. When to stop using Bash

Bash is **great glue** for:

- Stringing together CLI tools.
- Per-subject parallelism on a cluster.
- Quick one-offs.

Bash is **terrible** for:

- Floating-point arithmetic.
- Complex data structures (nested dicts, anything tabular).
- Scripts longer than ~200 lines.
- Anything that processes a non-trivial data format.

The signal to rewrite in Python: you start reaching for `awk` to do math, or you find yourself parsing the same JSON in three different places. Promote to a `python` module; keep the Bash as the thin orchestration layer.

## 14. Worked example — minimal robust pipeline driver

```bash
#!/usr/bin/env bash
# Usage: ./run_cohort.sh BIDS_DIR DERIV_DIR
set -euo pipefail
IFS=$'\n\t'

usage() {
  echo "usage: $0 BIDS_DIR DERIV_DIR" >&2
  exit 1
}

BIDS="${1:?$(usage)}"
DERIV="${2:?$(usage)}"
mkdir -p "$DERIV/logs"

main() {
  local sub
  for sub in "$BIDS"/sub-*; do
    sub="$(basename "$sub" | sed 's/^sub-//')"
    process_subject "$sub" \
      &> "$DERIV/logs/sub-${sub}.log" \
      || echo "FAILED $sub" >> "$DERIV/logs/failures.log"
  done
}

process_subject() {
  local sub="$1"
  apptainer run mriqc.sif "$BIDS" "$DERIV" participant \
      --participant-label "$sub"
}

main "$@"
```

Strict mode, usage helper, per-subject logging, fail-soft on individual subjects, function-based structure. A real driver looks like this; anything shorter is a toy.

## 15. References

1. **GNU Bash Reference Manual.** [https://www.gnu.org/software/bash/manual/bash.html](https://www.gnu.org/software/bash/manual/bash.html) — the authoritative spec.
2. **Newham C, Rosenblatt B.** *Learning the Bash Shell.* 3rd ed. O'Reilly; 2005. ISBN 978-0596009656.
3. **Robbins A.** *bash Pocket Reference.* 2nd ed. O'Reilly; 2016. ISBN 978-1491941591.
4. **Cooper M.** *Advanced Bash-Scripting Guide.* Free online: [https://tldp.org/LDP/abs/html/](https://tldp.org/LDP/abs/html/)
5. **ShellCheck.** [https://www.shellcheck.net](https://www.shellcheck.net) — static analysis for shell scripts.
6. **Aaron Maxwell.** Use the Unofficial Bash Strict Mode (Unless You Looove Debugging). [http://redsymbol.net/articles/unofficial-bash-strict-mode/](http://redsymbol.net/articles/unofficial-bash-strict-mode/)
7. **POSIX Shell Standard.** IEEE Std 1003.1-2017. [https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html)

## Exercises

1. **Strict-mode debugging.** Write a script that fails when a variable is unset; explain why `set -u` catches the bug `set -e` doesn't.
2. **Parameter expansion.** Given `SUB="sub-001_T1w.nii.gz"`, use parameter expansion (no external tools) to print `001`.
3. **Subject array job.** Write a Slurm array script that reads `subjects.txt` (one subject per line) and runs `process_subject "$sub"` on the indexed entry.

??? success "Solutions"
    1. `set -u`: `echo "${UNDEFINED}"` fails immediately; under `set -e` only, `false || echo ok` would silently mask it.
    2. `tmp=${SUB#sub-}; tmp=${tmp%_T1w*}; echo "$tmp"`.
    3. `subjects=($(cat subjects.txt)); sub=${subjects[$SLURM_ARRAY_TASK_ID - 1]}; process_subject "$sub"`.

## Where to next

[CLI commands](cli.md) — the individual programs your Bash scripts will orchestrate (`ls`, `rsync`, `ssh`, `find`, `grep`, …).
