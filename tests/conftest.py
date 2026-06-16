from pathlib import Path

import pytest

FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"


@pytest.fixture
def sub_tiny_root() -> Path:
    return FIXTURES / "sub-tiny"
