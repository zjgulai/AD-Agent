"""python -m kb_ops.web [--host 127.0.0.1] [--port 8000] [--kb-root DIR] [--reload]"""

from __future__ import annotations

import argparse
from pathlib import Path

from ..paths import ensure_src_path

_PKG_DIR = Path(__file__).resolve().parents[1]  # src/kb_ops


def main() -> None:
    ensure_src_path()
    ap = argparse.ArgumentParser(description="ad-agent-qa KB Workbench (FastAPI)")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--kb-root", default=None, help="覆盖 KB 根目录（默认 repo 内 KB）")
    ap.add_argument("--reload", action="store_true", help="开发模式热重载")
    args = ap.parse_args()

    import uvicorn

    if args.reload:
        uvicorn.run(
            "kb_ops.web.app:create_app",
            factory=True,
            host=args.host, port=args.port, reload=True,
            reload_dirs=[str(_PKG_DIR)],
        )
    else:
        from .app import create_app
        uvicorn.run(create_app(args.kb_root), host=args.host, port=args.port)


if __name__ == "__main__":
    main()
