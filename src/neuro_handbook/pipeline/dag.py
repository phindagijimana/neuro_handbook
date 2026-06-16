"""A ~100-line DAG runner for teaching.

Supports:

- Declaring named tasks with explicit dependencies.
- Topological scheduling.
- Cycle detection.
- Skipping tasks whose outputs already exist (the idempotency pillar).

Does *not* support: parallelism, retries, container isolation, distributed
execution. For any of those, reach for Snakemake. The point of this code is
to make the DAG concept tangible.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Task:
    """A single node in the DAG."""

    name: str
    run: Callable[[], None]
    depends_on: tuple[str, ...] = ()
    outputs: tuple[Path, ...] = ()

    def is_done(self) -> bool:
        """A task is done when all declared outputs exist on disk."""
        return bool(self.outputs) and all(p.exists() for p in self.outputs)


@dataclass
class DAG:
    """A minimal DAG runner.

    Add tasks with :meth:`add`, then call :meth:`run`. Tasks whose outputs
    already exist are skipped (idempotency). Cycles raise at run-time.
    """

    tasks: dict[str, Task] = field(default_factory=dict)

    def add(self, task: Task) -> Task:
        if task.name in self.tasks:
            raise ValueError(f"duplicate task name: {task.name}")
        self.tasks[task.name] = task
        return task

    def topological_order(self) -> list[Task]:
        order: list[Task] = []
        seen: set[str] = set()
        visiting: set[str] = set()

        def visit(name: str) -> None:
            if name in seen:
                return
            if name in visiting:
                raise ValueError(f"cycle detected at task '{name}'")
            visiting.add(name)
            task = self.tasks[name]
            for dep in task.depends_on:
                if dep not in self.tasks:
                    raise KeyError(f"task '{name}' depends on missing '{dep}'")
                visit(dep)
            visiting.remove(name)
            seen.add(name)
            order.append(task)

        for name in self.tasks:
            visit(name)
        return order

    def run(self, *, dry_run: bool = False) -> list[str]:
        """Run all tasks in topological order. Skips already-complete tasks.

        Returns the list of task names actually executed (i.e. not skipped).
        """
        executed: list[str] = []
        for task in self.topological_order():
            if task.is_done():
                continue
            if dry_run:
                executed.append(task.name)
                continue
            task.run()
            executed.append(task.name)
        return executed
