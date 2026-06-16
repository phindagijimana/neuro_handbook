"""Tiny DAG primitives used by handbook examples.

For real pipelines use Snakemake, Nextflow, Airflow, Dagster, or Prefect.
The DAG here exists to make the mental model in
docs/data-engineering/dag.md concrete and runnable in <100 lines of Python.
"""

from neuro_handbook.pipeline.dag import DAG, Task

__all__ = ["DAG", "Task"]
