"""KB 数据访问层：卡片/QA/图谱/检索/健康检查，供 FastAPI 路由复用。

全部只读（graph 缺失时可触发一次性重建导出）。带轻量 mtime/TTL 缓存，
KB 内容变更后下次请求自动感知，无需重启服务。
"""

from __future__ import annotations

import json
import re
import time
from pathlib import Path

from .. import audit_runner, lint_semantic
from .. import graph_export
from ..paths import ensure_src_path
from ..retrieval import BM25Index, build_index, search_chunks

ensure_src_path()
from kb_bot.kb import KnowledgeBase  # noqa: E402  (ensure_src_path 之后导入)

_NAME_RE = re.compile(r"^[a-z0-9][a-z0-9\-]*$")
_DOC_NAMES = {
    "INDEX.md", "SOURCES.md", "CONFLICTS.md", "QUERY.md", "UPDATING.md",
    "REVIEW.md", "REVIEW-PRECHECK.md", "REVIEW-SEMANTIC.md", "glossary.md",
    "OVERVIEW.md",
}
_QA_ITEM = re.compile(r"###\s+(Q\d+)\.\s*(.+?)\n\*\*A\*\*：\s*(.+?)(?=\n###\s+Q|\Z)", re.S)

# ---- 缓存 ----
_GRAPH_CACHE: dict[Path, tuple[float, dict]] = {}
_SEARCH_CACHE: dict[Path, tuple[float, KnowledgeBase, BM25Index]] = {}
_AUDIT_CACHE: dict[Path, tuple[float, dict]] = {}
_AUDIT_TTL = 120.0


def _valid_name(s: str) -> bool:
    return bool(_NAME_RE.fullmatch(s))


def _split_frontmatter(text: str) -> tuple[dict, str]:
    """解析扁平 YAML frontmatter（标量 + [a, b] 内联列表），返回 (meta, body)。"""
    m = re.match(r"\A---\s*\n(.*?)\n---\s*\n?", text, re.S)
    if not m:
        return {}, text
    meta: dict = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        k, v = k.strip(), v.strip()
        if v.startswith("[") and v.endswith("]"):
            meta[k] = [x.strip().strip("'\"") for x in v[1:-1].split(",") if x.strip()]
        else:
            meta[k] = v.strip("'\"")
    return meta, text[m.end():]


# ---- Cards ----

def list_cards(root: Path) -> list[dict]:
    cards_dir = root / "cards"
    out: list[dict] = []
    if not cards_dir.is_dir():
        return out
    for p in sorted(cards_dir.rglob("*.md")):
        rel = p.relative_to(root).as_posix()
        parts = p.relative_to(cards_dir).parts
        cluster = parts[0] if len(parts) > 1 else "_root"
        try:
            text = p.read_text(encoding="utf-8")
        except OSError:
            continue
        meta, _ = _split_frontmatter(text)
        out.append({
            "cluster": cluster, "name": p.stem, "path": rel,
            "title": meta.get("title") or p.stem,
            "status": meta.get("status", ""),
            "topic": meta.get("topic", ""),
            "updated": meta.get("updated") or meta.get("created", ""),
            "source_docs": meta.get("source_docs", []),
        })
    return out


def get_card(root: Path, cluster: str, name: str) -> dict:
    if not (_valid_name(cluster) and _valid_name(name)):
        raise ValueError("invalid card id")
    path = root / "cards" / cluster / f"{name}.md"
    if not path.is_file():
        raise FileNotFoundError(path)
    text = path.read_text(encoding="utf-8")
    meta, body = _split_frontmatter(text)
    card = next((c for c in list_cards(root)
                 if c["cluster"] == cluster and c["name"] == name), {})
    return {**card, "meta": meta, "body": body}


# ---- QA ----

def _parse_qa_text(text: str) -> list[dict]:
    entries = []
    for m in _QA_ITEM.finditer(text):
        qid, question, answer = m.group(1), m.group(2).strip(), m.group(3).strip()
        src_m = re.search(r"溯源：`?([^`\n]+)`?", answer)
        source = src_m.group(1).strip() if src_m else ""
        answer = re.sub(r"\n>\s*溯源：.*", "", answer, flags=re.S).strip()
        entries.append({"qid": qid, "question": question,
                        "answer": answer, "source": source})
    return entries


def list_qa(root: Path) -> list[dict]:
    qa_dir = root / "qa"
    out: list[dict] = []
    if not qa_dir.is_dir():
        return out
    for p in sorted(qa_dir.glob("*.md")):
        if p.name in {"README.md", "COVERAGE.md"}:
            continue
        text = p.read_text(encoding="utf-8")
        title_m = re.search(r"^#\s+(.+)$", text, re.M)
        out.append({
            "cluster": p.stem, "file": p.name,
            "title": title_m.group(1).strip() if title_m else p.stem,
            "count": len(_QA_ITEM.findall(text)),
        })
    return out


def get_qa(root: Path, cluster: str) -> dict:
    if not _valid_name(cluster):
        raise ValueError("invalid qa cluster")
    path = root / "qa" / f"{cluster}.md"
    if not path.is_file():
        raise FileNotFoundError(path)
    text = path.read_text(encoding="utf-8")
    return {"cluster": cluster, "entries": _parse_qa_text(text)}


# ---- Graph ----

def _kb_signature(root: Path) -> float:
    latest = 0.0
    for sub in ("cards", "qa"):
        d = root / sub
        if d.is_dir():
            for p in d.rglob("*.md"):
                try:
                    latest = max(latest, p.stat().st_mtime)
                except OSError:
                    pass
    g = root / "glossary.md"
    if g.is_file():
        latest = max(latest, g.stat().st_mtime)
    return latest


def get_graph(root: Path, rebuild: bool = False) -> dict:
    """返回 graph.json 数据；dist 缺失/过期时先跑 graph_export 重建。"""
    dist = root / "graph" / "dist"
    json_path = dist / "graph.json"
    if rebuild or not json_path.is_file():
        graph_export.export(root=root)
    mtime = json_path.stat().st_mtime
    cached = _GRAPH_CACHE.get(root)
    if cached is None or cached[0] != mtime:
        data = json.loads(json_path.read_text(encoding="utf-8"))
        _GRAPH_CACHE[root] = (mtime, data)
    return _GRAPH_CACHE[root][1]


# ---- Search ----

def search(root: Path, query: str, top_k: int = 8) -> list[dict]:
    sig = _kb_signature(root)
    entry = _SEARCH_CACHE.get(root)
    if entry is None or entry[0] != sig:
        kb = KnowledgeBase(root)
        entry = (sig, kb, build_index(kb))
        _SEARCH_CACHE[root] = entry
    _, kb, index = entry
    return [
        {"source": ch.source, "kind": ch.kind, "score": score,
         "text": ch.text[:600]}
        for ch, score in search_chunks(kb, index, query, top_k)
    ]


# ---- Health ----

def _parse_conflicts(root: Path) -> dict:
    path = root / "CONFLICTS.md"
    if not path.is_file():
        return {"rows": [], "adjudication": []}
    rows: list[dict] = []
    adj: list[dict] = []
    section = ""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            section = line
            continue
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if all(set(c) <= {"-", ":", " "} for c in cells):
            continue
        if cells[0] in {"#", "id", "ID", ""}:
            continue  # 表头行
        if "冲突总表" in section and len(cells) >= 6:
            rows.append({"id": cells[0], "conflict": cells[1], "side_a": cells[2],
                         "side_b": cells[3], "nature": cells[4], "status": cells[5]})
        elif "裁决" in section and len(cells) >= 3:
            adj.append({"id": cells[0], "status": cells[1], "decision": cells[2]})
    return {"rows": rows, "adjudication": adj}


def parse_conflicts(root: Path) -> dict:
    """CONFLICTS.md 解析（冲突总表 + 裁决记录），供 health 与 MCP 复用。"""
    return _parse_conflicts(root)


def health(root: Path, refresh: bool = False) -> dict:
    now = time.time()
    audit = None
    if not refresh:
        ent = _AUDIT_CACHE.get(root)
        if ent and now - ent[0] < _AUDIT_TTL:
            audit = ent[1]
    if audit is None:
        audit = audit_runner.run_all(root=root)
        _AUDIT_CACHE[root] = (now, audit)
    lint = lint_semantic.collect_findings(root)
    return {
        "audit": audit,
        "graph": lint["graph"],
        "conflicts": lint["conflicts"],
        "qa_counts": lint["qa_counts"],
        "qa_total": lint["qa_total"],
        "orphan_total": len(lint["orphan_nodes"]),
        "orphan_nodes": lint["orphan_nodes"][:100],
        "missing_card_files": lint["missing_card_files"],
        "uncovered_cards": lint["uncovered_cards"],
        "conflict_table": _parse_conflicts(root),
        "cached_at": time.strftime("%H:%M:%S"),
    }


# ---- Stats / Docs ----

def stats(root: Path) -> dict:
    cards = list_cards(root)
    qa = list_qa(root)
    g = get_graph(root)["stats"]
    return {
        "cards": len(cards),
        "card_clusters": len({c["cluster"] for c in cards}),
        "qa_entries": sum(q["count"] for q in qa),
        "qa_files": len(qa),
        "graph_nodes": g["nodes"],
        "graph_edges": g["edges"],
        "graph_communities": g["communities"],
        "graph_clusters": len(g["clusters"]),
    }


def get_doc(root: Path, name: str) -> str:
    if name not in _DOC_NAMES:
        raise FileNotFoundError(name)
    path = root / name
    if not path.is_file():
        raise FileNotFoundError(path)
    return path.read_text(encoding="utf-8")
