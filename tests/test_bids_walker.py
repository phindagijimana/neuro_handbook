from pathlib import Path

import pytest

from neuro_handbook.bids import walk_bids


def test_walker_finds_subjects_and_sessions(sub_tiny_root: Path) -> None:
    images = list(walk_bids(sub_tiny_root))
    subjects = {img.subject for img in images}
    assert subjects == {"001", "002"}

    sub_001 = [img for img in images if img.subject == "001"]
    assert {img.datatype for img in sub_001} == {"anat", "dwi"}
    assert all(img.session is None for img in sub_001)

    sub_002 = [img for img in images if img.subject == "002"]
    assert all(img.session == "01" for img in sub_002)


def test_walker_extracts_suffix(sub_tiny_root: Path) -> None:
    suffixes = {img.suffix for img in walk_bids(sub_tiny_root)}
    assert "T1w" in suffixes
    assert "dwi" in suffixes


def test_walker_missing_root_raises(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        list(walk_bids(tmp_path / "does-not-exist"))
