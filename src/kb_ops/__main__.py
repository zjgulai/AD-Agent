"""python -m kb_ops <command> 统一入口。

子命令映射到各模块 main()：
  graph-export  → kb_ops.graph_export
  lint          → kb_ops.lint_semantic
  audit         → kb_ops.audit_runner
  search <q>    → kb_ops.retrieval
  mcp           → kb_ops.mcp_server（stdio MCP Server）
"""

from __future__ import annotations

import sys


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] in {"-h", "--help", "help"}:
        print("usage: python -m kb_ops <command> [args]")
        print("commands: graph-export | lint | audit | search | web | mcp")
        sys.exit(0 if len(sys.argv) < 2 or sys.argv[1] in {"-h", "--help", "help"} else 1)

    cmd, rest = sys.argv[1], sys.argv[2:]
    sys.argv = [f"kb_ops.{cmd.replace('-', '_')}", *rest]

    if cmd == "web":
        from .web.__main__ import main as web_main
        web_main()
    elif cmd == "graph-export":
        from . import graph_export
        graph_export.main()
    elif cmd == "lint":
        from . import lint_semantic
        lint_semantic.main()
    elif cmd == "audit":
        from . import audit_runner
        audit_runner.main()
    elif cmd == "search":
        from . import retrieval
        retrieval.main()
    elif cmd == "mcp":
        from . import mcp_server
        mcp_server.main()
    else:
        print(f"unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
