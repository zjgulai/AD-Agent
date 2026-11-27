"""KB 路径解析：默认 repo 内 KB，KB_ROOT 环境变量可覆盖。"""

from __future__ import annotations

import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_KB_ROOT = REPO_ROOT / "docs" / "knowledge" / "ad-agent-qa"


def ensure_src_path() -> None:
    """保证 src/ 在 sys.path（kb_bot/kb_ops 跨包导入的前提）。"""
    src = str(REPO_ROOT / "src")
    if src not in sys.path:
        sys.path.insert(0, src)


def kb_root() -> Path:
    return Path(os.environ.get("KB_ROOT", str(DEFAULT_KB_ROOT)))


def graph_dir() -> Path:
    return kb_root() / "graph"


def graph_dist_dir() -> Path:
    return graph_dir() / "dist"
