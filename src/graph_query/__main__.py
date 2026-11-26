"""graph_query CLI — 人工/Agent 探查图谱。

用法（repo 根或 src/ 下均可）：
  python -m graph_query stats
  python -m graph_query resolve "EQ<4 会触发什么动作"
  python -m graph_query neighbors ad:metric:eq [relation]
  python -m graph_query context "新计划 EQ 异常怎么排查"
  python -m graph_query node ad:diag:s7:l4-01
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_GRAPH_DIR = REPO_ROOT / "docs" / "knowledge" / "ad-agent-qa" / "graph"


def _graph_dir(argv: list[str]) -> Path:
    if "--dir" in argv:
        return Path(argv[argv.index("--dir") + 1])
    return DEFAULT_GRAPH_DIR


def main() -> None:
    argv = sys.argv[1:]
    if not argv or argv[0] in {"-h", "--help"}:
        print(__doc__)
        return
    from . import GraphIndex

    g = GraphIndex(_graph_dir(argv))
    cmd = argv[0]
    rest = argv[1:]

    if cmd == "stats":
        print(g.stats())
        types: dict[str, int] = {}
        for n in g.nodes.values():
            t = n.get("@type", "?")
            types[t] = types.get(t, 0) + 1
        for t, c in sorted(types.items(), key=lambda x: -x[1]):
            print(f"  {t}: {c}")
    elif cmd == "resolve":
        for h in g.resolve(" ".join(rest) or " ", limit=10):
            print(f"[{h.score:5.1f}] {h.via:5s} {h.node_id}  {h.label}  ({h.node_type})")
    elif cmd == "neighbors":
        if not rest:
            print("usage: neighbors <node_id> [relation]")
            return
        rel = rest[1] if len(rest) > 1 else None
        for nb in g.neighbors(rest[0], relation=rel):
            print(f"{nb['direction']} {nb['relation']} -> {nb['other']}")
            for k in ("note", "when"):
                if nb.get(k):
                    print(f"    {k}: {nb[k]}")
    elif cmd == "context":
        print(g.context_for(" ".join(rest) or " ", max_entities=4, max_neighbors=12) or "(无命中)")
    elif cmd == "node":
        if not rest:
            print("usage: node <node_id>")
            return
        n = g.node(rest[0])
        print(json.dumps(n, ensure_ascii=False, indent=2) if n else "(not found)")
    else:
        print(f"unknown command: {cmd}\n{__doc__}")


if __name__ == "__main__":
    main()
