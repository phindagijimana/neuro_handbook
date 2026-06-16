"""Run the example DAG runner over a toy pipeline.

Three tasks: extract, transform, load. Each writes a tiny output file.
Run twice and the second run does nothing (idempotency).

    python examples/03_run_mini_dag.py /tmp/mini-dag
"""

from __future__ import annotations

import sys
from pathlib import Path

from neuro_handbook.pipeline import DAG, Task


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: 03_run_mini_dag.py <work-dir>", file=sys.stderr)
        return 2
    work = Path(argv[1])
    work.mkdir(parents=True, exist_ok=True)

    extracted = work / "raw.txt"
    transformed = work / "clean.txt"
    loaded = work / "final.csv"

    def do_extract() -> None:
        extracted.write_text("hello bids\n")

    def do_transform() -> None:
        text = extracted.read_text().upper()
        transformed.write_text(text)

    def do_load() -> None:
        loaded.write_text("phrase\n" + transformed.read_text())

    dag = DAG()
    dag.add(Task(name="extract", run=do_extract, outputs=(extracted,)))
    dag.add(Task(
        name="transform",
        run=do_transform,
        depends_on=("extract",),
        outputs=(transformed,),
    ))
    dag.add(Task(
        name="load",
        run=do_load,
        depends_on=("transform",),
        outputs=(loaded,),
    ))

    executed = dag.run()
    if executed:
        print(f"ran: {', '.join(executed)}")
    else:
        print("nothing to do — all outputs present (idempotent skip)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
