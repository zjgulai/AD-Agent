"""KB 路径解析：默认 repo 内 KB，KB_ROOT 环境变量可覆盖。"""

from __future__ import annotations

import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_KB_ROOT = REPO_ROOT / "docs" / "knowledge" / "ad-agent-qa"


def kb_root() -> Path:
    return Path(os.environ.get("KB_ROOT", str(DEFAULT_KB_ROOT)))


def graph_dir() -> Path:
    return kb_root() / "graph"


def graph_dist_dir() -> Path:
    return graph_dir() / "dist"
