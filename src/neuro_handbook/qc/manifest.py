"""Per-subject manifest schema.

A manifest is the simplest observability primitive a pipeline can emit. It
records what ran, on what inputs, in what environment, with what outcome.
The data-engineering handbook treats this as the cheapest observability win
you can ship — see docs/data-engineering/portfolio-roadmap.md Milestone 3.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class StageRecord(BaseModel):
    """One stage of one subject's run."""

    name: str
    started_at: datetime
    ended_at: datetime | None = None
    exit_code: int | None = None
    container_digest: str | None = None
    peak_rss_mb: float | None = None
    notes: str | None = None

    @property
    def duration_seconds(self) -> float | None:
        if self.ended_at is None:
            return None
        return (self.ended_at - self.started_at).total_seconds()


class Manifest(BaseModel):
    """A per-subject manifest.

    Emit one of these per subject per pipeline run. Aggregate them later to
    produce cohort dashboards (manifest.json -> cohort_report.parquet).
    """

    schema_version: Literal["1.0"] = "1.0"
    subject_id: str
    session_id: str | None = None
    pipeline: str
    pipeline_version: str
    git_sha: str | None = None
    host: str | None = None
    started_at: datetime = Field(default_factory=_utcnow)
    ended_at: datetime | None = None
    success: bool | None = None
    stages: list[StageRecord] = Field(default_factory=list)

    def add_stage(self, record: StageRecord) -> None:
        self.stages.append(record)

    def finish(self, success: bool) -> None:
        self.ended_at = _utcnow()
        self.success = success


def write_manifest(manifest: Manifest, path: Path | str) -> Path:
    """Write a manifest atomically as ``manifest.json``.

    Atomic = write to ``.tmp`` then rename. See the foundations chapter on
    idempotency for why this matters.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(manifest.model_dump_json(indent=2))
    tmp.replace(path)
    return path


def load_manifest(path: Path | str) -> Manifest:
    """Load a manifest written by :func:`write_manifest`."""
    return Manifest.model_validate_json(Path(path).read_text())


__all__ = ["Manifest", "StageRecord", "load_manifest", "write_manifest"]
