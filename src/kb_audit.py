"""KB 机器预审：cards/qa/glossary/INDEX/graph 溯源的结构完整性检查。

产出 REVIEW-PRECHECK.md（人审前的机器过滤层），把 REVIEW.md 的人工验收
范围压缩到真正需要人眼的高风险项。

用法：python -m kb_audit [--strict]   # strict 时有 FAIL 项 exit 1
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent
KB_ROOT = _SRC.parent / "docs" / "knowledge" / "ad-agent-qa"
CARDS = KB_ROOT / "cards"
QA = KB_ROOT / "qa"
GRAPH = KB_ROOT / "graph"

REQUIRED_FM = ["title", "doc_type", "module", "topic", "status", "created", "updated", "owner", "source"]
VALID_STATUS = {"draft", "review", "stable", "deprecated"}
CARD_SECTIONS = ["## 核心问题", "## 系统解答", "## 高频问答索引"]

FAIL, WARN, INFO = "FAIL", "WARN", "INFO"


def _fm(text: str) -> dict | None:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    out = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, _, v = line.partition(":")
            out[k.strip()] = v.strip()
    return out


def _links(text: str) -> list[str]:
    return re.findall(r"\]\(([^)#\s]+\.md[^)]*)\)", text)


def _check_frontmatter(path: Path, rel: str, findings: list) -> dict | None:
    text = path.read_text(encoding="utf-8")
    fm = _fm(text)
    if fm is None:
        findings.append((FAIL, rel, "frontmatter 缺失或无法解析"))
        return None
    for k in REQUIRED_FM:
        if k not in fm:
            findings.append((FAIL, rel, f"frontmatter 缺字段 `{k}`"))
    status = fm.get("status", "")
    if status and status not in VALID_STATUS:
        findings.append((WARN, rel, f"status={status} 非法值"))
    return fm


def _s_ids(fm: dict) -> list[str]:
    raw = fm.get("source_docs", "")
    return re.findall(r"\bS\d+[a-z]?\b", raw)


def _po_ids(fm: dict) -> list[str]:
    raw = fm.get("source_docs", "")
    return re.findall(r"PO:([\w-]+)", raw)


def audit(kb_root: Path = KB_ROOT) -> tuple[list, dict]:
    findings: list[tuple[str, str, str]] = []
    cards_dir, qa_dir, graph_dir = kb_root / "cards", kb_root / "qa", kb_root / "graph"
    index_text = (kb_root / "INDEX.md").read_text(encoding="utf-8")

    # ---- SOURCES.md 的 S-id 集合 ----
    sources_text = (kb_root / "SOURCES.md").read_text(encoding="utf-8")
    s_ids = set(re.findall(r"^\|\s*(S\d+[a-z]?)\s*\|", sources_text, re.M))

    # ---- graph 中 pops 对象 object_id 集合 + card: 溯源文件集合 ----
    po_ids: set[str] = set()
    card_refs: set[str] = set()
    nodes_file = graph_dir / "instances" / "platform-ops-kb.nodes.json"
    if nodes_file.exists():
        for n in json.loads(nodes_file.read_text(encoding="utf-8"))["nodes"]:
            oid = (n.get("props") or {}).get("object_id")
            if oid:
                po_ids.add(oid)
    for nf in graph_dir.glob("instances/*.nodes.json"):
        for n in json.loads(nf.read_text(encoding="utf-8"))["nodes"]:
            for s in n.get("src") or []:
                if s.startswith("card:"):
                    card_refs.add(s[5:])

    stats = {"cards": 0, "qa_entries": 0, "qa_files": 0, "links_checked": 0}

    # ---- cards/ ----
    for path in sorted(cards_dir.rglob("*.md")):
        rel = path.relative_to(kb_root).as_posix()
        stats["cards"] += 1
        fm = _check_frontmatter(path, rel, findings)
        if fm is None:
            continue
        text = path.read_text(encoding="utf-8")
        for s in _s_ids(fm):
            # S<n><字母> 视为 S<n> 的子源（如 S12b 内嵌 sheet），SOURCES.md 允许只登基行
            if s not in s_ids and re.sub(r"[a-z]$", "", s) not in s_ids:
                findings.append((WARN, rel, f"source_docs `{s}` 未在 SOURCES.md 登记"))
        for p in _po_ids(fm):
            if p not in po_ids:
                findings.append((WARN, rel, f"source_docs `PO:{p}` 不在 graph pops 对象集"))
        for sec in CARD_SECTIONS:
            if sec not in text:
                findings.append((WARN, rel, f"缺章节 `{sec}`"))
        for link in _links(text):
            stats["links_checked"] += 1
            if not (path.parent / link.split("#")[0]).resolve().exists():
                findings.append((FAIL, rel, f"死链 `{link}`"))
        if path.name not in index_text:
            findings.append((WARN, rel, "INDEX.md 未提及（孤儿卡？）"))
        n_todo = text.count("[待确认]")
        n_inf = text.count("[推断]")
        if n_todo >= 10:
            findings.append((INFO, rel, f"[待确认]×{n_todo} 残留偏多，验收时重点核"))
        if len(text.splitlines()) < 30:
            findings.append((WARN, rel, f"仅 {len(text.splitlines())} 行，疑似残卡"))

    # ---- qa/ 数据文件 ----
    sys.path.insert(0, str(_SRC))
    from kb_bot.kb import KnowledgeBase
    kb = KnowledgeBase(kb_root)
    qa_loaded: dict[str, int] = {}
    for c in kb.chunks:
        if c.kind == "qa" and c.source.startswith("qa/"):
            fn = c.source.split()[0]
            qa_loaded[fn] = qa_loaded.get(fn, 0) + 1

    for path in sorted(qa_dir.glob("*.md")):
        if path.name in {"README.md", "COVERAGE.md"}:
            continue
        rel = path.relative_to(kb_root).as_posix()
        stats["qa_files"] += 1
        fm = _check_frontmatter(path, rel, findings)
        if fm is None:
            continue
        text = path.read_text(encoding="utf-8")
        n_q = len(re.findall(r"^###\s+Q\d+\.", text, re.M))
        n_a = len(re.findall(r"^\*\*A\*\*：", text, re.M))
        n_src = len(re.findall(r"^>\s*溯源：", text, re.M))
        stats["qa_entries"] += n_q
        if not (n_q == n_a == n_src):
            findings.append((FAIL, rel,
                f"Q/A/溯源计数不齐：Q{n_q} A{n_a} 溯源{n_src}（检索正则可能静默丢条目）"))
        loaded = qa_loaded.get(f"qa/{path.name}", 0)
        if loaded != n_q:
            findings.append((FAIL, rel,
                f"检索加载 {loaded} 条 ≠ 文件 Q 条目 {n_q}（kb._QA_ENTRY 未覆盖）"))
        nums = [int(m) for m in re.findall(r"^###\s+Q(\d+)\.", text, re.M)]
        if nums != list(range(1, len(nums) + 1)):
            findings.append((INFO, rel, f"Q 编号非连续：{nums[:8]}…"))

    # ---- INDEX.md 链接 ----
    for link in _links(index_text):
        stats["links_checked"] += 1
        if not (kb_root / link.split("#")[0]).resolve().exists():
            findings.append((FAIL, "INDEX.md", f"死链 `{link}`"))

    # ---- graph card: 溯源完整性 ----
    # 两种写法：card:<cluster>/<file>.md（多数分片）与 card:<file>.md#L<n>
    # （meta-ads-diagnosis 试点分片的 basename 简写）
    card_basenames = {p.name: p for p in cards_dir.rglob("*.md")}
    for ref in sorted(card_refs):
        stats["links_checked"] += 1
        path_part = ref.split("#", 1)[0]
        ok = (cards_dir / path_part).exists()
        if not ok and "/" not in path_part:
            ok = path_part in card_basenames
        if not ok:
            findings.append((FAIL, "graph/instances", f"节点 src 引用不存在的卡 `{ref}`"))

    # ---- SOURCES.md raw/ 路径（* 通配；\d+~\d+ 为 sheet 序号区间记法，转 ? 通配）----
    for m in re.findall(r"`(raw/[^`]+)`", sources_text):
        if "*" in m or "~" in m:
            pat = re.sub(r"\d+~\d+", lambda mm: "?" * len(mm.group(0).split("~")[0]), m)
            if not list(kb_root.glob(pat)):
                findings.append((WARN, "SOURCES.md", f"raw 通配无匹配 `{m}`"))
        elif not (kb_root / m).exists():
            findings.append((WARN, "SOURCES.md", f"raw 路径不存在 `{m}`"))

    # ---- glossary ----
    g = kb_root / "glossary.md"
    if g.exists():
        n_terms = len(re.findall(r"^\|[^|\n]+\|[^|\n]+\|[^|\n]+\|[^|\n]+\|$", g.read_text(encoding="utf-8"), re.M)) - 2
        findings.append((INFO, "glossary.md", f"术语表约 {max(n_terms, 0)} 条"))

    return findings, stats


def render(findings: list, stats: dict) -> str:
    order = {FAIL: 0, WARN: 1, INFO: 2}
    findings.sort(key=lambda f: (order[f[0]], f[1]))
    counts = {s: sum(1 for f in findings if f[0] == s) for s in (FAIL, WARN, INFO)}
    lines = [
        "---",
        "title: KB 机器预审报告",
        "doc_type: knowledge",
        "module: ad-agent-qa",
        "topic: review-precheck",
        "status: review",
        f"created: {__import__('datetime').date.today().isoformat()}",
        "owner: self",
        "source: ai",
        "---",
        "",
        "# KB 机器预审报告",
        "",
        "> 由 `src/kb_audit.py` 生成——REVIEW.md 人工验收前的机器过滤层。",
        "> FAIL=结构性问题必修；WARN=需人眼判断；INFO=提示。",
        "",
        f"**统计**：{stats['cards']} 卡 / {stats['qa_files']} QA 文件 / "
        f"{stats['qa_entries']} Q 条目 / {stats['links_checked']} 链接检查",
        "",
        f"**结果**：FAIL {counts[FAIL]} · WARN {counts[WARN]} · INFO {counts[INFO]}",
        "",
        "| 级别 | 文件 | 问题 |",
        "|------|------|------|",
    ]
    for sev, rel, msg in findings:
        lines.append(f"| {sev} | `{rel}` | {msg} |")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    strict = "--strict" in sys.argv[1:]
    findings, stats = audit()
    report = render(findings, stats)
    out = KB_ROOT / "REVIEW-PRECHECK.md"
    out.write_text(report, encoding="utf-8")
    n_fail = sum(1 for f in findings if f[0] == FAIL)
    n_warn = sum(1 for f in findings if f[0] == WARN)
    print(f"audit: {stats['cards']} cards, {stats['qa_entries']} QA entries, "
          f"{stats['links_checked']} links → FAIL {n_fail} / WARN {n_warn} / "
          f"INFO {len(findings) - n_fail - n_warn}")
    print(f"report → {out}")
    for sev, rel, msg in findings:
        if sev != INFO:
            print(f"  [{sev}] {rel}: {msg}")
    return 1 if (strict and n_fail) else 0


if __name__ == "__main__":
    sys.exit(main())
