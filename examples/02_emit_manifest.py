"""Emit a per-subject manifest for a (mock) pipeline run.

Demonstrates the manifest pattern from the data-engineering Portfolio
roadmap, Milestone 3.

    python examples/02_emit_manifest.py sub-001 /tmp/manifest.json
"""

from __future__ import annotations

import socket
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from neuro_handbook.qc import Manifest, StageRecord, write_manifest


def _git_sha() -> str | None:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], text=True
        ).strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None


def _fake_stage(name: str, duration_s: float, exit_code: int = 0) -> StageRecord:
    start = datetime.now(timezone.utc)
    time.sleep(duration_s)
    end = datetime.now(timezone.utc)
    return StageRecord(
        name=name,
        started_at=start,
        ended_at=end,
        exit_code=exit_code,
        container_digest=f"sha256:fake-{name}",
    )


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: 02_emit_manifest.py <subject_id> <out.json>", file=sys.stderr)
        return 2
    subject_id, out_path = argv[1], Path(argv[2])

    m = Manifest(
        subject_id=subject_id,
        pipeline="dwi_pipeline",
        pipeline_version="0.1.0",
        git_sha=_git_sha(),
        host=socket.gethostname(),
    )
    for stage_name in ("qsiprep", "recon", "qsirecon", "dk_connectome"):
        m.add_stage(_fake_stage(stage_name, duration_s=0.05))
    m.finish(success=True)

    write_manifest(m, out_path)
    print(f"wrote manifest -> {out_path} ({len(m.stages)} stages)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
