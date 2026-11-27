"""语义层 lint：确定性健康检查（借鉴 knowledge-pipline pipeline_lint 的模式，
叠加在 validate.py/kb_audit 确定性检查之上，不替代它们）。

检查项：
- 孤儿图谱节点（degree=0）
- KnowledgeAsset 节点的卡片文件缺失
- cards/ 下存在但图谱无 KnowledgeAsset 节点的卡片
- CONFLICTS.md 未决项导出（pending_business / [待确认] 计数）
- QA 条目按集群统计（覆盖度速览）

CLI：python -m kb_ops.lint_semantic [--json] [--write]
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

from .graph_export import load_shards
from .paths import kb_root


def collect_findings(root: Path) -> dict:
    inst_dir = root / "graph" / "instances"
    nodes, edges = load_shards(inst_dir) if inst_dir.is_dir() else ({}, [])

    # 度数
    degree: Counter = Counter()
    for e in edges:
        degree[e["source"]] += 1
        degree[e["target"]] += 1

    orphan_nodes = [
        {"id": nid, "label": n.get("label", nid), "type": n.get("@type", "?"),
         "cluster": n.get("_cluster", "")}
        for nid, n in nodes.items() if degree[nid] == 0
    ]

    # KnowledgeAsset → 卡片文件存在性
    missing_cards, card_assets = [], {}
    for nid, n in nodes.items():
        if n.get("@type") != "ad:KnowledgeAsset":
            continue
        rel = (n.get("props") or {}).get("path") or ""
        if not rel:
            src = (n.get("src") or [""])[0]
            m = re.match(r"card:(.+)$", src)
            rel = m.group(1) if m else ""
        if rel:
            card_assets[rel] = nid
            if not (root / rel).is_file():
                missing_cards.append({"node": nid, "path": rel})

    # cards/ 实际文件 vs 图谱 asset 覆盖
    cards_on_disk = {
        p.relative_to(root).as_posix()
        for p in (root / "cards").rglob("*.md")
    } if (root / "cards").is_dir() else set()
    uncovered_cards = sorted(cards_on_disk - set(card_assets))

    # CONFLICTS 未决项
    conflicts = {"pending_business": 0, "todo_confirm": 0, "total_rows": 0}
    cfile = root / "CONFLICTS.md"
    if cfile.is_file():
        text = cfile.read_text(encoding="utf-8")
        for line in text.splitlines():
            if line.startswith("|") and "C" in line[:8]:
                conflicts["total_rows"] += 1
                if "pending_business" in line or "待确认" in line:
                    conflicts["pending_business"] += 1
                elif "待确认" in line:
                    conflicts["todo_confirm"] += 1

    # QA 条目统计
    qa_counts: Counter = Counter()
    qa_dir = root / "qa"
    if qa_dir.is_dir():
        for p in qa_dir.glob("*.md"):
            if p.name in {"README.md", "COVERAGE.md"}:
                continue
            qa_counts[p.stem] = len(re.findall(r"^###\s+Q\d+", p.read_text(encoding="utf-8"), re.M))

    return {
        "graph": {"nodes": len(nodes), "edges": len(edges)},
        "orphan_nodes": orphan_nodes,
        "missing_card_files": missing_cards,
        "uncovered_cards": uncovered_cards,
        "conflicts": conflicts,
        "qa_counts": dict(qa_counts),
        "qa_total": sum(qa_counts.values()),
    }


def render_report(f: dict) -> str:
    lines = [
        "# KB 语义 lint 报告（kb_ops.lint_semantic）",
        "",
        f"- 图谱: {f['graph']['nodes']} 节点 / {f['graph']['edges']} 边",
        f"- QA 条目: {f['qa_total']} 条 / {len(f['qa_counts'])} 个集群文件",
        f"- CONFLICTS: {f['conflicts']['total_rows']} 行裁决记录，"
        f"{f['conflicts']['pending_business']} 行含待确认/pending_business",
        "",
        "## 孤儿图谱节点（degree=0）",
    ]
    if f["orphan_nodes"]:
        for n in f["orphan_nodes"][:50]:
            lines.append(f"- `{n['id']}` {n['label']}（{n['type']} @ {n['cluster']}）")
        if len(f["orphan_nodes"]) > 50:
            lines.append(f"- …共 {len(f['orphan_nodes'])} 个")
    else:
        lines.append("- 无")
    lines += ["", "## KnowledgeAsset 卡片文件缺失"]
    if f["missing_card_files"]:
        for m in f["missing_card_files"]:
            lines.append(f"- `{m['node']}` → `{m['path']}` 不存在")
    else:
        lines.append("- 无")
    lines += ["", "## cards/ 未被图谱 KnowledgeAsset 覆盖"]
    if f["uncovered_cards"]:
        for c in f["uncovered_cards"]:
            lines.append(f"- `{c}`")
    else:
        lines.append("- 无（全部卡片均有 asset 节点）")
    lines += ["", "## QA 集群分布"]
    for k, v in sorted(f["qa_counts"].items(), key=lambda x: -x[1]):
        lines.append(f"- {k}: {v} 条")
    return "\n".join(lines) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(description="KB 语义 lint（确定性检查）")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--write", action="store_true", help="写入 KB_ROOT/REVIEW-SEMANTIC.md")
    args = ap.parse_args()

    findings = collect_findings(kb_root())
    if args.json:
        print(json.dumps(findings, ensure_ascii=False, indent=2))
        return
    report = render_report(findings)
    if args.write:
        out = kb_root() / "REVIEW-SEMANTIC.md"
        out.write_text(report, encoding="utf-8")
        print(f"report → {out}")
    else:
        print(report)


if __name__ == "__main__":
    main()
