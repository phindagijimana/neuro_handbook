from pathlib import Path

import pytest

from neuro_handbook.qc import check_connectome_shape
from neuro_handbook.qc.metrics import ConnectomeShapeError


def _write_matrix(path: Path, rows: int, cols: int) -> None:
    with path.open("w") as fh:
        for _ in range(rows):
            fh.write(",".join("0" for _ in range(cols)) + "\n")


def test_correct_shape_passes(tmp_path: Path) -> None:
    p = tmp_path / "dk.csv"
    _write_matrix(p, 84, 84)
    assert check_connectome_shape(p, 84, 84) == (84, 84)


def test_wrong_shape_raises(tmp_path: Path) -> None:
    p = tmp_path / "dk.csv"
    _write_matrix(p, 80, 84)
    with pytest.raises(ConnectomeShapeError, match="80x84"):
        check_connectome_shape(p, 84, 84)


def test_ragged_rows_raise(tmp_path: Path) -> None:
    p = tmp_path / "dk.csv"
    p.write_text("0,0,0\n0,0\n0,0,0\n")
    with pytest.raises(ConnectomeShapeError, match="ragged"):
        check_connectome_shape(p, 3, 3)
