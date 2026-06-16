.DEFAULT_GOAL := help
PY ?= python3.12

.PHONY: help install lint test cov docs serve clean

help:
	@echo "Targets:"
	@echo "  install   Create .venv and install the package + dev + docs extras"
	@echo "  lint      Run ruff over src/ tests/ examples/"
	@echo "  test      Run pytest"
	@echo "  cov       Run pytest with coverage"
	@echo "  docs      Build the MkDocs site into site/"
	@echo "  serve     Serve the docs locally at http://127.0.0.1:8000"
	@echo "  clean     Remove caches and build artifacts"

install:
	$(PY) -m venv .venv
	./.venv/bin/pip install -U pip
	./.venv/bin/pip install -e ".[dev,docs]"

lint:
	./.venv/bin/ruff check src tests examples

test:
	./.venv/bin/pytest

cov:
	./.venv/bin/pytest --cov=neuro_handbook --cov-report=term-missing

docs:
	./.venv/bin/mkdocs build --strict

serve:
	./.venv/bin/mkdocs serve

clean:
	rm -rf site .pytest_cache .ruff_cache .mypy_cache .coverage htmlcov build dist *.egg-info
	find . -name __pycache__ -type d -exec rm -rf {} +
