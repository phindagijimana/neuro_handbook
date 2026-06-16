from pathlib import Path

import pytest

from neuro_handbook.pipeline import DAG, Task


def _writer(path: Path, content: str):
    def _do() -> None:
        path.write_text(content)
    return _do


def test_topological_order(tmp_path: Path) -> None:
    a = tmp_path / "a"
    b = tmp_path / "b"
    c = tmp_path / "c"

    dag = DAG()
    dag.add(Task(name="a", run=_writer(a, "A"), outputs=(a,)))
    dag.add(Task(name="b", run=_writer(b, "B"), depends_on=("a",), outputs=(b,)))
    dag.add(Task(name="c", run=_writer(c, "C"), depends_on=("b", "a"), outputs=(c,)))

    order = [t.name for t in dag.topological_order()]
    assert order.index("a") < order.index("b") < order.index("c")


def test_cycle_detected() -> None:
    dag = DAG()
    dag.add(Task(name="a", run=lambda: None, depends_on=("b",)))
    dag.add(Task(name="b", run=lambda: None, depends_on=("a",)))
    with pytest.raises(ValueError, match="cycle"):
        dag.topological_order()


def test_idempotent_rerun_skips(tmp_path: Path) -> None:
    a = tmp_path / "a"
    dag = DAG()
    dag.add(Task(name="a", run=_writer(a, "first"), outputs=(a,)))

    assert dag.run() == ["a"]
    # Second run sees the output already exists and skips.
    assert dag.run() == []
    # Output is unchanged.
    assert a.read_text() == "first"
