import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

KB_ROOT = ROOT / "docs" / "knowledge" / "ad-agent-qa"
GRAPH_DIR = KB_ROOT / "graph"


@pytest.fixture(scope="session")
def kb_root():
    return KB_ROOT


@pytest.fixture(scope="session")
def graph_dir():
    return GRAPH_DIR
