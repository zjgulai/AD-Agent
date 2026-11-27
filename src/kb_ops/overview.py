"""OVERVIEW.md 生成：KB 活体综述（规模 + 集群地图 + 审计状态）。

由 `python -m kb_ops.audit` 顺带刷新；幂等——内容不变不重写，
避免无意义 git diff。时间戳取 KB 内容最新 mtime，内容变更才翻新。
"""

from __future__ import annotations

import time
from datetime import date
from pathlib import Path

from .paths import kb_root
from .web import service


def _content_date(root: Path) -> str:
    sig = service._kb_signature(root)
    return time.strftime("%Y-%m-%d", time.localtime(sig)) if sig else date.today().isoformat()


def generate_overview(root: Path, audit_result: dict | None = None) -> str:
    cards = service.list_cards(root)
    qa_files = service.list_qa(root)
    s = service.stats(root)
    generated = "?"
    try:
        generated = service.get_graph(root).get("generated", "?")
    except Exception:  # noqa: BLE001 — graph 缺失不阻塞 overview
        pass

    # 集群地图：card cluster ∪ qa cluster
    card_by_cluster: dict[str, list[dict]] = {}
    for c in cards:
        card_by_cluster.setdefault(c["cluster"], []).append(c)
    qa_by_cluster: dict[str, int] = {q["cluster"]: q["count"] for q in qa_files}
    clusters = sorted(set(card_by_cluster) | set(qa_by_cluster))

    lines = [
        "# KB OVERVIEW — ad-agent-qa",
        "",
        "> 自动生成（`python -m kb_ops.audit`），反映 KB 内容最新状态 "
        f"（{_content_date(root)}）。目录权威见 INDEX.md，源登记见 SOURCES.md，"
        "冲突裁决见 CONFLICTS.md。",
        "",
        "## 规模",
        "",
        "| 维度 | 数量 |",
        "|---|---|",
        f"| 知识卡 | {s['cards']} 张 / {s['card_clusters']} 集群 |",
        f"| QA 条目 | {s['qa_entries']} 条 / {s['qa_files']} 文件 |",
        f"| 图谱 | {s['graph_nodes']} 节点 · {s['graph_edges']} 边 · "
        f"{s['graph_communities']} 社区 / {s['graph_clusters']} 分片集群 |",
        f"| graph.json 生成 | {generated} |",
        "",
        "## 集群地图",
        "",
        "| 集群 | 卡片 | QA | 代表卡片 |",
        "|---|---|---|---|",
    ]
    for cl in clusters:
        cls = card_by_cluster.get(cl, [])
        reps = ", ".join(f"`{c['name']}`" for c in cls[:3])
        if len(cls) > 3:
            reps += " …"
        lines.append(
            f"| {cl} | {len(cls)} | {qa_by_cluster.get(cl, '—')} | {reps or '—'} |")

    lines += ["", "## 审计状态", ""]
    if audit_result:
        v, a = audit_result.get("validate", {}), audit_result.get("audit", {})
        lines += [
            f"- validate.py：{v.get('status', '?')} "
            f"（{v.get('errors', '?')} errors / {v.get('warnings', '?')} warnings）",
            f"- kb_audit：FAIL {a.get('fail', '?')} / WARN {a.get('warn', '?')} "
            f"/ INFO {a.get('info', '?')} · overall {'OK' if audit_result.get('ok') else 'FAIL'}",
        ]
    else:
        lines.append("- （未附带审计结果；运行 `python -m kb_ops.audit` 获取）")

    lines += [
        "",
        "## 使用入口",
        "",
        "- 检索：workbench Search 视图 · `python -m kb_ops search \"<query>\"` · "
        "MCP `kb_search`",
        "- 全文：workbench Cards/QA 视图 · MCP `kb_get_card` / `kb_get_qa`",
        "- 图谱：workbench Graph 视图 · MCP `kb_graph_search/neighbors/path/community`",
        "- 摄入：workbench Ingest 视图 · MCP `kb_ingest_propose`（staging 待审，"
        "蒸馏与发布仍需人工）",
        "",
    ]
    return "\n".join(lines)


def write_overview(root: Path | None = None,
                   audit_result: dict | None = None) -> Path:
    """生成并写入 <root>/OVERVIEW.md；内容不变不重写。返回文件路径。"""
    root = root or kb_root()
    content = generate_overview(root, audit_result)
    out = root / "OVERVIEW.md"
    if out.is_file() and out.read_text(encoding="utf-8") == content:
        return out
    out.write_text(content, encoding="utf-8")
    return out
