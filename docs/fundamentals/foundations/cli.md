# CLI commands

> The individual command-line tools your shell scripts will call. Navigation, file operations, transferring data between machines, text processing, processes, permissions, networking — what each one does and the flags worth knowing.

This page is a reference. Its companion [Bash](bash.md) covers the *scripting language* that orchestrates these tools.

Every example assumes a Linux / macOS shell. Windows users should run inside WSL2 ([install guide](https://learn.microsoft.com/en-us/windows/wsl/install)).

## 1. Where am I — navigation

| Command | Meaning |
|---|---|
| `pwd` | **P**rint **W**orking **D**irectory — where the shell currently is. |
| `cd PATH` | **C**hange **D**irectory to `PATH`. `cd` alone → home, `cd -` → previous. |
| `ls` | **L**i**S**t directory contents. |
| `pushd / popd` | Stack-based directory navigation. |
| `realpath PATH` | Resolve to an absolute, symlink-free path. |
| `tree -L 2 .` | Visualise directory tree to depth 2 (install separately). |

Useful `ls` flags:

```bash
ls -l        # long format (permissions, owner, size, date)
ls -a        # show hidden files (those starting with .)
ls -h        # human-readable sizes (K, M, G)
ls -t        # sort by modification time
ls -S        # sort by size
ls -R        # recursive
ls -lah      # the canonical "show me everything" combo
```

## 2. Files and directories — making, moving, deleting

| Command | Meaning |
|---|---|
| `mkdir DIR` | Make a directory. `-p` creates parents as needed. |
| `rmdir DIR` | Remove an *empty* directory. |
| `touch FILE` | Create an empty file or update its mtime. |
| `cp SRC DST` | Copy. `-r` recursive; `-p` preserve timestamps; `-a` archive (preserve everything). |
| `mv SRC DST` | Move or rename. Same file system → instantaneous rename; cross-filesystem → copy + delete. |
| `rm FILE` | Remove. `-r` recursive; `-f` force (no prompt). `rm -rf` is irreversible. |
| `ln -s TARGET LINK` | Symbolic link. Like a shortcut. |
| `stat FILE` | Detailed metadata: size, mtime, inode, permissions. |
| `file FILE` | Identify file type from contents (NIfTI, JSON, gzipped, …). |

**Safety rule.** Never `rm -rf "$var"` unless you've verified `$var` is non-empty:

```bash
[[ -n "$dir" && -d "$dir" ]] && rm -rf "$dir"
```

Better, install [`trash-cli`](https://github.com/andreafrancia/trash-cli) and use `trash` instead of `rm` on your laptop — it sends files to the OS trash instead of nuking them.

## 3. Looking inside files

| Command | Meaning |
|---|---|
| `cat FILE` | Print whole file (short ones only). |
| `head -n 20 FILE` | First 20 lines. |
| `tail -n 20 FILE` | Last 20 lines. |
| `tail -f log.out` | Follow a growing file (like `tail` watching a Slurm log). |
| `less FILE` | Page through interactively. `q` to quit, `/pattern` to search. |
| `more FILE` | Older, simpler pager. |
| `wc -l FILE` | Count lines. `-w` words, `-c` bytes. |
| `xxd FILE` | Hex dump for binary inspection. |
| `gunzip -c f.gz \| less` | Read a gzipped file without unzipping. |
| `zcat / bzcat / xzcat` | Same, for `.gz` / `.bz2` / `.xz`. |

## 4. Finding things — `find`, `locate`, `grep`

### `find` — by name, size, age

```bash
find . -name "*.nii.gz"                  # by glob name
find . -type f -size +50M                # files larger than 50 MB
find . -type d -name "anat"              # directories called "anat"
find . -name "*_bold.nii.gz" -mtime -7   # modified in last 7 days
find . -name "*.tmp" -delete             # find and delete (be careful)
find . -name "*_T1w.nii.gz" -exec dcm2niix -o ./out {} \;
```

`find` is the most powerful navigation tool you'll ever use. Worth a full afternoon ([find man](https://man7.org/linux/man-pages/man1/find.1.html)).

### `locate` — fast name search via a pre-built index

```bash
sudo updatedb                            # refresh index (admin)
locate fmriprep                          # instantaneous; uses cached DB
```

### `grep` — search inside files

```bash
grep "ERROR" log.txt                     # plain string
grep -i "warning" log.txt                # case-insensitive
grep -r "TODO" .                         # recursive
grep -rn "TODO" .                        # add line numbers
grep -l "ERROR" logs/                    # just list matching filenames
grep -v "DEBUG" log.txt                  # exclude lines
grep -E "^(error|warning):" log.txt      # extended regex
grep -A 3 -B 3 "panic" log.txt           # 3 lines after/before context
```

Use [`ripgrep`](https://github.com/BurntSushi/ripgrep) (`rg`) when you can — same flags, ~10× faster, respects `.gitignore` by default.

## 5. Permissions and ownership

```bash
chmod u+x script.sh                       # add execute for owner
chmod 755 script.sh                       # owner=rwx, group=rx, other=rx
chmod -R go-w private/                    # remove write for group/other
chown user:group file                     # change ownership (often needs sudo)
umask 022                                 # default permission mask
```

The numeric form: `r=4`, `w=2`, `x=1`, summed per role (owner/group/other). `755` = `rwxr-xr-x`. `644` = `rw-r--r--`. Common cases:

- **Scripts** — `chmod 755 script.sh`.
- **Sensitive keys** — `chmod 600 ~/.ssh/id_ed25519`.
- **Shared lab folder** — `chmod -R 775 /shared/project`.

## 6. Copying between machines — the big section

This is the part most newcomers want. Five tools cover almost every scenario.

### `scp` — secure copy, simplest case

```bash
# Local → remote
scp file.tsv user@cluster.example.org:/home/user/

# Remote → local
scp user@cluster.example.org:/home/user/file.tsv ./

# Recursive folder
scp -r local_folder/ user@cluster.example.org:/home/user/

# Through a jump host
scp -J user@bastion file.tsv user@cluster:/home/user/

# With a non-standard port
scp -P 2222 file.tsv user@host:/home/user/
```

`scp` is simple but **does not resume** if the connection drops. For anything larger than a few hundred MB, use `rsync`.

### `rsync` — the workhorse

```bash
# Mirror a folder local → remote (incremental, resumable)
rsync -av --progress local/ user@cluster:/remote/path/

# Same with deletions on the remote
rsync -av --delete local/ user@cluster:/remote/path/

# Dry run first — always
rsync -av --dry-run local/ user@cluster:/remote/path/

# Resume an interrupted transfer
rsync -avP local/ user@cluster:/remote/path/   # P = partial + progress

# Limit bandwidth so you don't saturate the network
rsync -av --bwlimit=50000 local/ user@cluster:/remote/   # 50 MB/s cap

# Use a non-standard SSH port
rsync -av -e "ssh -p 2222" local/ user@cluster:/remote/

# Exclude noisy patterns
rsync -av --exclude='*.tmp' --exclude='__pycache__' local/ user@cluster:/remote/

# Both ends remote: pull from A, push to B
rsync -av user@A:/path/ user@B:/path/         # transits via your machine
```

Trailing-slash trap: `local/` copies the **contents** of `local`; `local` (no slash) copies the folder *itself*. Get this wrong once and you'll never forget.

`rsync` is also the right tool for local-to-local copies of large datasets:

```bash
rsync -av --progress /mnt/scanner_export/ /mnt/study/raw/
```

Faster, resumable, and verifies checksums optionally (`--checksum`). The `-a` archive flag bundles `-rlptgoD` (recursive, links, perms, times, group, owner, devices) — usually what you want.

### `sftp` — interactive transfer

```bash
sftp user@cluster.example.org
sftp> put local.tsv                       # upload
sftp> get remote.tsv                       # download
sftp> ls / cd / pwd                        # navigate remote
sftp> mput *.tsv                           # upload many
sftp> bye
```

Useful for ad-hoc browsing of a remote system without leaving the shell.

### `ssh` — remote shell + tunnelling

```bash
ssh user@host                             # interactive shell
ssh user@host "ls /data"                  # one-shot remote command
ssh -i ~/.ssh/lab_key user@host           # specific key

# Local port forward: localhost:8080 → host:80 via SSH
ssh -L 8080:localhost:80 user@host

# Reverse port forward (expose your laptop to the remote)
ssh -R 9090:localhost:9090 user@host

# Run a command then keep the tunnel open
ssh -N -L 8888:node-XX:8888 user@cluster  # JupyterLab tunnel

# Jump through a bastion
ssh -J user@bastion user@inner-host

# Multiplexed SSH (one connection, many sessions)
# In ~/.ssh/config:
#   Host *
#       ControlMaster auto
#       ControlPath ~/.ssh/sockets/%r@%h:%p
#       ControlPersist 10m
```

`~/.ssh/config` is where you encode the messy details once:

```text
Host cluster
    HostName cluster.example.org
    User myuser
    Port 22
    IdentityFile ~/.ssh/lab_key
    ServerAliveInterval 60
```

Then `ssh cluster` and `scp file.tsv cluster:/path/` just work.

### `curl` and `wget` — download from URLs

```bash
curl -L -o file.zip https://example.org/data.zip   # follow redirects
curl -O https://example.org/data.zip                # save with same name
curl -u user:pass https://example.org/secure        # basic auth
curl -X POST -H 'Content-Type: application/json' \
     -d '{"k":"v"}' https://example.org/api

wget https://example.org/data.zip
wget -c URL                                          # continue partial
wget -r -np URL                                      # recursive, no parent
wget -i urls.txt                                     # list of URLs
```

`curl` for one-off APIs; `wget` for resumable HTTP/FTP downloads.

### `aws s3` / `gcloud storage` / `azcopy` — cloud transfers

```bash
# AWS S3
aws s3 cp file.parquet s3://bucket/path/file.parquet
aws s3 sync local_folder/ s3://bucket/folder/

# Google Cloud
gcloud storage cp file.parquet gs://bucket/path/
gcloud storage rsync local_folder gs://bucket/folder/

# Azure
azcopy copy 'local_folder' 'https://acct.blob.core.windows.net/cont/' --recursive
```

For research datasets (HCP, UK Biobank), `aws s3 sync` is the workhorse — resumable, parallel, requester-pays-aware.

## 7. Disk space and filesystem

| Command | Meaning |
|---|---|
| `df -h` | Free space per **mounted filesystem**. |
| `du -sh DIR` | Total size of a directory. `-s` summary, `-h` human-readable. |
| `du -h --max-depth=1 DIR` | Per-subdir sizes — find the disk hog. |
| `ncdu DIR` | Interactive disk usage browser. |
| `mount` | List currently mounted filesystems. |
| `lsblk` | List block devices. |
| `quota -s` | Per-user disk quota (HPC). |

Find the biggest files in a tree:

```bash
find . -type f -exec du -h {} + | sort -h | tail -20
```

## 8. Processes — what's running

| Command | Meaning |
|---|---|
| `ps aux` | All processes with full details. |
| `ps -ef \| grep python` | Filter for processes containing "python". |
| `top` | Interactive real-time process table. |
| `htop` | Friendlier `top` (install separately). |
| `pgrep python` | Just the PIDs matching a name. |
| `kill PID` | Send SIGTERM (graceful exit). |
| `kill -9 PID` | Send SIGKILL (force). |
| `nice -n 10 cmd` | Run with lower priority. |
| `nohup cmd &` | Run in background, survive logout. |
| `jobs / fg / bg` | Manage shell-managed background jobs. |

For long-running interactive work, prefer `tmux` or `screen` over `nohup`:

```bash
tmux new -s mywork                        # start named session
# detach with Ctrl-b d
tmux a -t mywork                          # re-attach later
```

## 9. Compression and archives

| Command | Meaning |
|---|---|
| `tar -cvzf out.tar.gz DIR/` | Create gzip-compressed tar archive. |
| `tar -xvzf out.tar.gz` | Extract. |
| `tar -tvzf out.tar.gz` | List without extracting. |
| `gzip FILE` / `gunzip FILE.gz` | Compress / decompress one file (replaces it). |
| `zip -r out.zip DIR/` / `unzip out.zip` | ZIP archives. |
| `pigz` / `pbzip2` | Parallel `gzip` / `bzip2` for big files. |
| `zstd FILE` | Modern compressor; faster than gzip, smaller than bzip2. |

Memorable `tar` mnemonic: **c**reate, e**x**tract, **t**est; **v**erbose; **z**=gzip, **j**=bzip2, **J**=xz; **f**=filename.

## 10. Text processing — small toolbox, huge leverage

`awk`, `sed`, `cut`, `sort`, `uniq`, `tr`, `wc`, `join`, `paste`:

```bash
# Count lines in a TSV
wc -l participants.tsv

# Print column 3 of a TSV
cut -f 3 participants.tsv

# Sort + unique
sort subjects.txt | uniq

# Count occurrences of each value
cut -f 2 participants.tsv | sort | uniq -c | sort -rn

# Join two TSVs on the first column (both must be sorted by it)
join -t $'\t' a.tsv b.tsv

# Replace text in a stream
sed 's/sub-0/sub-/g' subjects.txt

# Modify a file in place (keep .bak backup)
sed -i.bak 's/REPLACE/foo/g' template.sh

# awk: sum column 3, skipping the header
awk 'NR > 1 { sum += $3 } END { print sum }' participants.tsv

# awk: print subject_id where age > 60
awk -F'\t' 'NR == 1 { for (i=1; i<=NF; i++) col[$i]=i; next }
            $col["age"] > 60 { print $col["subject_id"] }' participants.tsv

# tr: translate / delete characters
tr ',' '\t' < a.csv > a.tsv               # comma → tab
echo "HELLO" | tr 'A-Z' 'a-z'             # lowercase
```

The [GNU awk manual](https://www.gnu.org/software/gawk/manual/) is worth a deep read; awk is the most underused powerful tool on every Linux system.

## 11. Networking and remote info

| Command | Meaning |
|---|---|
| `ping HOST` | ICMP round-trip. |
| `traceroute HOST` | Path your packets take. |
| `nslookup DOMAIN` / `dig DOMAIN` | DNS lookup. |
| `ip addr` | Local interfaces and addresses. (`ifconfig` on macOS) |
| `ss -tulpn` | Open TCP/UDP ports + listening processes. (`netstat` legacy) |
| `curl -I URL` | Just HTTP response headers. |
| `wget --spider URL` | Check a URL exists without downloading. |
| `whois DOMAIN` | Domain registration info. |

For HPC users, `ssh-keygen` + `ssh-copy-id user@host` is the one-time setup that lets you stop typing passwords:

```bash
ssh-keygen -t ed25519                    # generate a strong key
ssh-copy-id user@cluster.example.org    # install it on the remote
```

## 12. Working with neuroimaging files from the CLI

Once your data is BIDS-organised, these one-liners are gold:

```bash
# Header info on a NIfTI
fslhd sub-001_T1w.nii.gz

# Whole-image stats
fslstats sub-001_T1w.nii.gz -M -S         # mean + stddev within nonzero mask

# Crop a volume
fslroi input.nii.gz output.nii.gz 0 64 0 64 0 30 0 100

# Arithmetic on volumes
fslmaths a.nii.gz -add b.nii.gz sum.nii.gz
fslmaths a.nii.gz -mas mask.nii.gz a_masked.nii.gz

# Convert DICOM → NIfTI
dcm2niix -b y -z y -o out_dir/ dicom_root/

# MRtrix3 equivalents
mrinfo sub-001_dwi.mif
mrstats sub-001_dwi.mif
mrcalc a.mif b.mif -add sum.mif

# AFNI
3dinfo sub-001_T1w.nii.gz
3dBrickStat sub-001_T1w.nii.gz

# BIDS validation
npx bids-validator path/to/dataset
```

The full preprocessing CLIs (fMRIPrep, QSIPrep, MRIQC) follow the BIDS-app contract:

```bash
apptainer run fmriprep.sif BIDS_DIR DERIV_DIR participant \
    --participant-label 001 --fs-license-file license.txt
```

See [Landmark → BIDS-app workflows](../../landmark/bids-apps.md).

## 13. Environment and variables

```bash
env                                      # all environment variables
echo $PATH                                # search path for executables
export NEW_VAR=value                      # set + export to children
unset OLD_VAR                             # remove
which python3                             # find first match in PATH
type python3                              # is it a function/alias/binary?
hash -r                                   # forget cached binary locations
```

Persist by editing `~/.bashrc` (interactive shells) or `~/.bash_profile` (login shells).

## 14. Safety, hygiene, recovery

- **Quote variables.** `"$var"`, not `$var`. Catches every space-in-path bug.
- **Use `mktemp`** for temporary files; `trap '… cleanup …' EXIT` to delete them.
- **Use `cp -n`** to refuse to overwrite an existing file when you want fail-safe.
- **`set -euo pipefail`** at the top of every script.
- **`shellcheck`** your scripts before committing.
- **History is not a backup.** Don't trust `Ctrl-r` to recover yesterday's command.
- **`history -d N`** to remove an accidentally-recorded password from `~/.bash_history`; then `history -w`.

## 15. References

1. **Sobell MG.** *A Practical Guide to Linux Commands, Editors, and Shell Programming.* 4th ed. Pearson; 2017. ISBN 978-0134774602.
2. **Kerrisk M.** *The Linux Programming Interface.* No Starch Press; 2010. ISBN 978-1593272203.
3. **`man` pages.** [https://man7.org/linux/man-pages/](https://man7.org/linux/man-pages/) — `man COMMAND` is the offline authoritative reference.
4. **`tldr` pages.** [https://tldr.sh](https://tldr.sh) — community-maintained example-driven summaries.
5. **OpenSSH manuals.** [https://www.openssh.com/manual.html](https://www.openssh.com/manual.html)
6. **rsync man page.** [https://download.samba.org/pub/rsync/rsync.1](https://download.samba.org/pub/rsync/rsync.1)
7. **Linux Documentation Project.** *Bash Guide for Beginners.* [https://tldp.org/LDP/Bash-Beginners-Guide/html/](https://tldp.org/LDP/Bash-Beginners-Guide/html/)
8. **AWS CLI User Guide.** [https://docs.aws.amazon.com/cli/latest/userguide/](https://docs.aws.amazon.com/cli/latest/userguide/)

## Exercises

1. **Find the disk hogs.** In `~/`, print the 10 largest files. (Hint: combine `find`, `du`, `sort`, `tail`.)
2. **Resumable backup.** Write the `rsync` command that copies `~/work/study/` to `user@cluster:/backup/study/`, resumes if interrupted, excludes `__pycache__/`, and dry-runs first.
3. **Process pruning.** Find every `python` process owned by you and print PID + command, sorted by memory.

??? success "Solutions"
    1. `find ~ -type f -exec du -h {} + | sort -h | tail -10`.
    2. `rsync -avP --exclude='__pycache__' --dry-run ~/work/study/ user@cluster:/backup/study/` (drop `--dry-run` for real).
    3. `ps -u $USER -o pid,rss,cmd | grep '[p]ython' | sort -k2 -n`.

## Where to next

[MATLAB](matlab.md) — the second-most-common neuroimaging-analysis language, especially on the SPM / EEGLAB / FieldTrip side.
