"""ad-agent-qa KB 的 MCP Server（stdio）。

把知识库暴露为标准 MCP 工具：检索 / 读取 / 图谱 / 治理 + 唯一写工具
kb_ingest_propose（投递 staging 待审，不直接入库）。

用法：python -m kb_ops.mcp     （KB_ROOT env 可覆盖默认 KB 路径）

结构：tool_* 函数为 transport-agnostic 工具层（返回 markdown str，
便于 pytest 直测）；@mcp.tool() 装饰器仅做协议壳。v1.1 可用
mcp.run(transport="streamable-http") 复用同一工具层。
"""

from __future__ import annotations

import base64
import binascii
import subprocess
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from . import audit_runner, graph_query, ingest
from .paths import REPO_ROOT, kb_root
from .web import service

INSTRUCTIONS = """\
ad-agent-qa 知识库（Momcozy 广告投放 Agent 问答库）：56 张知识卡 + \
281 条原子 QA + 947 节点 1976 边的领域本体图谱（schema 校验、人工策展）。

推荐用法：
1. 先 kb_search 做 BM25 检索定位，再用 kb_get_card / kb_get_qa 取全文。
2. 需要实体关系或多跳推理时用图谱工具：kb_graph_search 解析节点 → \
kb_graph_neighbors（邻居）/ kb_graph_path（最短路径）/ kb_graph_community（社区）。
3. 涉及争议点先查 kb_conflicts（未裁决冲突）；kb_audit / kb_stats 查库健康度。
4. kb_ingest_propose 可把外部资料投递进 staging 待审队列——自动提取但不直接入库，
仍需人工评审；不要用它绕过人审门禁。

反模式：不要逐个拉取卡片/QA 做遍历式阅读；不要假设库内有实时投放数据
（库内是方法论、诊断框架与历史案例，不是实时数据源）。"""

mcp = FastMCP("kb-agent-qa", instructions=INSTRUCTIONS)


# ---------- tool 层（transport-agnostic，返回 markdown） ----------

def _err(msg: str) -> str:
    return f"Error: {msg}"


def tool_search(query: str, top_k: int = 8, root: Path | None = None) -> str:
    root = root or kb_root()
    try:
        top_k = max(1, min(int(top_k), 20))
    except (TypeError, ValueError):
        top_k = 8
    hits = service.search(root, query, top_k)
    if not hits:
        return f"无命中：`{query}`"
    lines = [f"检索 `{query}` 命中 {len(hits)} 条：", ""]
    for i, h in enumerate(hits, 1):
        lines.append(f"### {i}. [{h['score']}] `{h['source']}` ({h['kind']})")
        lines.append(h["text"].strip()[:600])
        lines.append("")
    return "\n".join(lines).rstrip()


def tool_get_card(cluster: str, name: str, root: Path | None = None) -> str:
    root = root or kb_root()
    try:
        card = service.get_card(root, cluster, name)
    except ValueError as e:
        return _err(str(e))
    except FileNotFoundError:
        return _err(f"card not found: cards/{cluster}/{name}.md")
    meta = card.get("meta", {})
    head = [
        f"# {card.get('title') or name}",
        "",
        f"- path: `{card.get('path')}`",
        f"- cluster: {card.get('cluster')} · status: {card.get('status') or '-'}",
        f"- topic: {card.get('topic') or '-'} · updated: {card.get('updated') or '-'}",
        f"- source_docs: {', '.join(card.get('source_docs') or []) or '-'}",
        "",
        "---",
        "",
    ]
    return "\n".join(head) + (card.get("body") or "").strip()


def tool_get_qa(cluster: str, qid: str | None = None,
                root: Path | None = None) -> str:
    root = root or kb_root()
    try:
        data = service.get_qa(root, cluster)
    except ValueError as e:
        return _err(str(e))
    except FileNotFoundError:
        return _err(f"qa not found: qa/{cluster}.md")
    entries = data["entries"]
    if qid:
        want = qid.strip().upper()
        if not want.startswith("Q"):
            want = "Q" + want
        entries = [e for e in entries if e["qid"].upper() == want]
        if not entries:
            return _err(f"qid not found in qa/{cluster}.md: {qid}")
    lines = [f"# QA · {cluster}" + (f" · {qid}" if qid else ""), ""]
    for e in entries:
        lines.append(f"### {e['qid']}. {e['question']}")
        lines.append(f"**A**：{e['answer']}")
        if e.get("source"):
            lines.append(f"> 溯源：{e['source']}")
        lines.append("")
    return "\n".join(lines).rstrip()


def tool_graph_search(query: str, type_filter: str | None = None,
                      cluster: str | None = None,
                      root: Path | None = None) -> str:
    return graph_query.tool_graph_search(root or kb_root(), query,
                                        type_filter, cluster)


def tool_graph_neighbors(node_ref: str, root: Path | None = None) -> str:
    return graph_query.tool_graph_neighbors(root or kb_root(), node_ref)


def tool_graph_path(source_ref: str, target_ref: str,
                    root: Path | None = None) -> str:
    return graph_query.tool_graph_path(root or kb_root(), source_ref, target_ref)


def tool_graph_community(node_ref: str, root: Path | None = None) -> str:
    return graph_query.tool_graph_community(root or kb_root(), node_ref)


def tool_audit(root: Path | None = None) -> str:
    root = root or kb_root()
    try:
        r = audit_runner.run_all(root=root)
    except Exception as e:  # noqa: BLE001 — 工具层兜底，返回可读错误
        return _err(f"audit failed: {e!r}")
    v, a = r["validate"], r["audit"]
    lines = [
        "## validate.py（图谱 schema）",
        f"status: {v['status']} · errors: {v['errors']} · warnings: {v['warnings']}",
    ]
    lines += [f"- {ln}" for ln in v["error_lines"][:20]]
    lines += [
        "",
        "## kb_audit（卡片/QA/索引一致性）",
        f"FAIL {a['fail']} / WARN {a['warn']} / INFO {a['info']}",
    ]
    lines += [f"- {ln}" for ln in a["warning_lines"][:20]]
    lines += ["", f"overall: {'OK' if r['ok'] else 'FAIL'}"]
    return "\n".join(lines)


def tool_conflicts(root: Path | None = None) -> str:
    root = root or kb_root()
    data = service.parse_conflicts(root)
    lines = ["# CONFLICTS.md 冲突台账", ""]
    rows = data.get("rows", [])
    if rows:
        lines += [f"## 冲突总表（{len(rows)} 项）", "",
                  "| id | 冲突 | side A | side B | 性质 | 状态 |",
                  "|---|---|---|---|---|---|"]
        for r in rows:
            lines.append(
                f"| {r['id']} | {r['conflict']} | {r['side_a']} "
                f"| {r['side_b']} | {r['nature']} | {r['status']} |")
        lines.append("")
    adj = data.get("adjudication", [])
    if adj:
        lines += [f"## 裁决记录（{len(adj)} 项）", "",
                  "| id | 状态 | 决议 |", "|---|---|---|"]
        for r in adj:
            lines.append(f"| {r['id']} | {r['status']} | {r['decision']} |")
        lines.append("")
    if not rows and not adj:
        lines.append("（无冲突记录）")
    return "\n".join(lines)


def _git_commit() -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=REPO_ROOT, capture_output=True, text=True, timeout=10)
        return out.stdout.strip() or "unknown"
    except Exception:  # noqa: BLE001
        return "unknown"


def tool_stats(root: Path | None = None) -> str:
    root = root or kb_root()
    try:
        s = service.stats(root)
    except Exception as e:  # noqa: BLE001
        return _err(f"stats failed: {e!r}")
    try:
        generated = service.get_graph(root).get("generated", "?")
    except Exception:  # noqa: BLE001
        generated = "?"
    lines = [
        "# KB 统计",
        "",
        f"- KB_ROOT: `{root}`",
        f"- cards: {s['cards']}（{s['card_clusters']} 集群）",
        f"- QA: {s['qa_entries']} 条 / {s['qa_files']} 文件",
        f"- graph: {s['graph_nodes']} nodes / {s['graph_edges']} edges "
        f"/ {s['graph_communities']} communities / {s['graph_clusters']} clusters",
        f"- graph.json generated: {generated}",
        f"- repo commit: `{_git_commit()}`",
    ]
    return "\n".join(lines)


def tool_ingest_propose(filename: str,
                        content: str | None = None,
                        content_base64: str | None = None,
                        staging: Path | None = None) -> str:
    """投递文件进 staging（自动提取到 extracted，待人工评审）。"""
    if bool(content) == bool(content_base64):
        return _err("content 与 content_base64 必须且只能提供一个")
    try:
        data = (base64.b64decode(content_base64, validate=True)
                if content_base64 else (content or "").encode("utf-8"))
    except (binascii.Error, ValueError) as e:
        return _err(f"content_base64 解码失败: {e}")
    if not data:
        return _err("空内容")
    try:
        item = ingest.ingest_bytes(filename, data, staging=staging)
    except Exception as e:  # noqa: BLE001 — 校验错误透传给 Agent
        return _err(str(e))
    lines = [
        "# 摄入提案已受理",
        "",
        f"- item_id: `{item['id']}`",
        f"- filename: {item['filename']}（{item['ext']}，{item['size_bytes']} bytes）",
        f"- status: **{item['status']}**（已自动提取，待人工评审）",
        f"- 提取字符: {item.get('content_chars', 0)} · 表格: {item.get('tables', 0)}",
    ]
    if item.get("errors"):
        lines.append("- 提取警告: " + "; ".join(item["errors"][:5]))
    lines += [
        "",
        "下一步（人工/Agent 在 workbench 或 CLI 完成）：生成蒸馏简报 → "
        "蒸馏 → 人工发布。详见 `docs/kb-mcp-setup.md` 与 workbench Ingest 视图。",
    ]
    return "\n".join(lines)


# ---------- FastMCP 协议壳 ----------

@mcp.tool()
def kb_search(query: str, top_k: int = 8) -> str:
    """BM25 检索 KB（cards + QA + glossary），返回命中块与溯源路径。
    先搜索定位，再用 kb_get_card / kb_get_qa 取全文。"""
    return tool_search(query, top_k)


@mcp.tool()
def kb_get_card(cluster: str, name: str) -> str:
    """取知识卡片全文。cluster 为集群目录名（如 fundamentals、
    meta-ads-diagnosis），name 为卡片文件名（不含 .md）。"""
    return tool_get_card(cluster, name)


@mcp.tool()
def kb_get_qa(cluster: str, qid: str | None = None) -> str:
    """取 QA 条目。cluster 为 qa 文件名（如 meta-ads-diagnosis）；
    qid 如 Q5 取单条，缺省返回全集群。"""
    return tool_get_qa(cluster, qid)


@mcp.tool()
def kb_graph_search(query: str, type: str | None = None,
                    cluster: str | None = None) -> str:
    """按 id/label 子串解析图谱节点（top10）。其他图谱工具的入口：
    不知道 node_id 时先用它。type 如 ad:Metric 前缀过滤。"""
    return tool_graph_search(query, type, cluster)


@mcp.tool()
def kb_graph_neighbors(node: str) -> str:
    """节点 1-hop 邻居及关系类型（无向遍历，标注边方向）。
    node 可为精确 id 或唯一 label/id 子串。"""
    return tool_graph_neighbors(node)


@mcp.tool()
def kb_graph_path(source: str, target: str) -> str:
    """两节点间 BFS 最短路径（≤6 跳），返回节点序列与每跳关系类型。"""
    return tool_graph_path(source, target)


@mcp.tool()
def kb_graph_community(node: str) -> str:
    """节点所在社区（Louvain）的成员列表，按连接度排序。"""
    return tool_graph_community(node)


@mcp.tool()
def kb_audit() -> str:
    """KB 健康审计：图谱 schema validate + 卡片/QA 一致性 kb_audit，实时执行。"""
    return tool_audit()


@mcp.tool()
def kb_conflicts() -> str:
    """CONFLICTS.md 冲突台账：未裁决/已裁决冲突及双方主张。回答争议点前先查。"""
    return tool_conflicts()


@mcp.tool()
def kb_stats() -> str:
    """KB 规模统计、图谱生成时间与 repo commit。"""
    return tool_stats()


@mcp.tool()
def kb_ingest_propose(filename: str, content: str | None = None,
                      content_base64: str | None = None) -> str:
    """把外部资料投递进摄入队列（staging→自动提取→待人工评审）。
    content 为 UTF-8 文本；content_base64 为二进制（PDF/DOCX 等）。
    唯一写工具：不直接入库，蒸馏与发布仍需人工。"""
    return tool_ingest_propose(filename, content, content_base64)


def main() -> None:
    mcp.run()  # stdio


if __name__ == "__main__":
    main()
