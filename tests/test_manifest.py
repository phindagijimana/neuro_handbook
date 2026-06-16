from datetime import datetime, timezone
from pathlib import Path

from neuro_handbook.qc import Manifest, StageRecord, write_manifest
from neuro_handbook.qc.manifest import load_manifest


def _stage(name: str) -> StageRecord:
    t0 = datetime(2026, 6, 15, 10, 0, 0, tzinfo=timezone.utc)
    t1 = datetime(2026, 6, 15, 10, 5, 0, tzinfo=timezone.utc)
    return StageRecord(name=name, started_at=t0, ended_at=t1, exit_code=0)


def test_manifest_roundtrip(tmp_path: Path) -> None:
    m = Manifest(
        subject_id="001",
        pipeline="dwi_pipeline",
        pipeline_version="0.1.0",
    )
    m.add_stage(_stage("qsiprep"))
    m.add_stage(_stage("recon"))
    m.finish(success=True)

    out = tmp_path / "manifest.json"
    write_manifest(m, out)
    loaded = load_manifest(out)

    assert loaded.subject_id == "001"
    assert loaded.success is True
    assert [s.name for s in loaded.stages] == ["qsiprep", "recon"]
    assert loaded.stages[0].duration_seconds == 300.0


def test_manifest_write_is_atomic(tmp_path: Path) -> None:
    m = Manifest(subject_id="001", pipeline="dwi_pipeline", pipeline_version="0.1.0")
    out = tmp_path / "manifest.json"
    write_manifest(m, out)
    # No leftover .tmp from the rename-based atomic write.
    assert not (tmp_path / "manifest.json.tmp").exists()
    assert out.exists()
