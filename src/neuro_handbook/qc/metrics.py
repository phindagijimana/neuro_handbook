"""Cheap, dependency-light QC checks.

For richer QC (FA / MD distributions, motion summaries, etc.) use the QC
reports emitted by QSIPrep / fMRIPrep. The functions here are designed for
the kind of schema test the handbook recommends in the testing chapter.
"""

from __future__ import annotations

import csv
from pathlib import Path


class ConnectomeShapeError(ValueError):
    """Raised when a connectome CSV does not match the expected shape."""


def check_connectome_shape(
    csv_path: Path | str, expected_rows: int, expected_cols: int
) -> tuple[int, int]:
    """Verify a connectome CSV has the expected (rows, cols) shape.

    Returns the observed (rows, cols). Raises :class:`ConnectomeShapeError`
    on mismatch with a helpful message.

    A typical Desikan-Killiany connectome is 84x84.
    """
    path = Path(csv_path)
    with path.open() as fh:
        reader = csv.reader(fh)
        rows = list(reader)
    if not rows:
        raise ConnectomeShapeError(f"{path} is empty")

    observed_rows = len(rows)
    observed_cols = len(rows[0])
    for i, row in enumerate(rows):
        if len(row) != observed_cols:
            raise ConnectomeShapeError(
                f"{path}: ragged row {i} has {len(row)} cols, "
                f"expected {observed_cols}"
            )

    if observed_rows != expected_rows or observed_cols != expected_cols:
        raise ConnectomeShapeError(
            f"{path}: shape is {observed_rows}x{observed_cols}, "
            f"expected {expected_rows}x{expected_cols}"
        )
    return observed_rows, observed_cols
