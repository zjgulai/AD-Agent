"""经验卡草稿生成器：扫 bot qa 日志 → 启发式信号 → experience/ 草稿卡。

信号驱动而非全量记录：只把「值得复盘」的会话变成草稿卡，人审后晋升为
卡片修订 / QA 新条 / 图谱边更新 / CONFLICTS 裁决。

用法（任意目录可跑，路径按 __file__ 解析）：
  python -m experience_drafter scan [--dry-run]   # 生成/更新草稿（幂等）
  python -m experience_drafter list               # 按 status/signal 统计
  python -m experience_drafter set-status EXP-... <status> [--action ...] [--verdict ...] [--reviewer ...]
"""

from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent
LOGS_DIR = _SRC / "kb_bot" / "logs"
KB_ROOT = _SRC.parent / "docs" / "knowledge" / "ad-agent-qa"
EXP_DIR = KB_ROOT / "experience"
GRAPH_DIR = KB_ROOT / "graph"

LOW_SCORE = 9.0          # hits 最高分低于此值视为弱命中
REPEAT_HIGH = 3          # 同一问题出现次数 ≥ 此值 → high 优先级
BOUNDARY_MARKS = ("暂无资料", "暂无可靠资料", "知识库暂无")

SIGNAL_DEF = {
    "user-feedback": ("user-feedback", "用户负反馈/补充：最高优先级信号，必看原文"),
    "user-upvote": ("positive", "用户正反馈：答案获认可，可沉淀为稳定 QA"),
    "no-hit": ("qa-gap", "检索零命中：补 qa/ 原子问答，或确认属知识边界"),
    "low-score": ("retrieval-tuning", "命中但分数偏低：检查 qa 标题措辞/卡片切片是否可命中"),
    "repeat": ("qa-gap", "重复提问：考虑补 qa/ 条目或在卡片中前置该问法"),
    "boundary-answer": ("coverage-review", "答案触边界声明：核对 COVERAGE.md，该扩则补源蒸馏"),
    "conflict-touch": ("graph-review", "命中冲突边实体：确认并列口径呈现是否充分"),
    "error": ("system-issue", "应答异常：查 bot 日志/LLM 配置，非知识问题"),
}
PRIORITY = {"critical": 4, "high": 3, "medium": 2, "low": 1}


def _norm_question(q: str) -> str:
    return re.sub(r"[\s\W_]+", "", q.lower())


def _load_logs(logs_dir: Path) -> list[dict]:
    recs = []
    for path in sorted(logs_dir.glob("qa-*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            rec["_log"] = str(path)
            recs.append(rec)
    return recs


def _classify(rec: dict) -> dict[str, str]:
    """单条记录 → {signal: priority}。conflict-touch/repeat 在聚合后判定。"""
    out: dict[str, str] = {}
    status = str(rec.get("status", ""))
    hits = rec.get("hits") or []
    answer = str(rec.get("answer") or "")
    if status != "ok":
        out["error"] = "low"
    if not hits:
        out["no-hit"] = "high"
    elif max(float(h.get("score", 0)) for h in hits) < LOW_SCORE:
        out["low-score"] = "medium"
    if any(m in answer for m in BOUNDARY_MARKS):
        out["boundary-answer"] = "medium"
    return out


def _load_feedback(logs_dir: Path) -> list[dict]:
    recs = []
    for path in sorted(logs_dir.glob("fb-*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            rec["_log"] = str(path)
            recs.append(rec)
    return recs


def _conflict_nodes(graph, labels: list[str]) -> list[str]:
    """graph_entities 只存了 label，反查 node 判断是否有 conflicts_with 边。"""
    if graph is None or not labels:
        return []
    found = []
    for label in labels:
        hits = graph.resolve(label, limit=1)
        if hits and graph.neighbors(hits[0].node_id, relation="ad:conflicts_with"):
            found.append(hits[0].node_id)
    return found


def _question_key_to_id() -> dict[str, tuple[str, str]]:
    """norm_question → (exp_id, status)，从已有卡 frontmatter 读。"""
    out = {}
    for p in EXP_DIR.glob("EXP-*.md"):
        text = p.read_text(encoding="utf-8")
        mq = re.search(r'^question: (".*")$', text, re.M)
        ms = re.search(r"^status: (\S+)", text, re.M)
        if mq:
            try:
                out[_norm_question(json.loads(mq.group(1)))] = (
                    p.stem, ms.group(1) if ms else "draft")
            except json.JSONDecodeError:
                pass
    return out


def _next_seq(day: str, taken: set[str]) -> int:
    prefix = f"EXP-{day.replace('-', '')}-"
    seq = 1
    while _exp_id(day, seq) in taken:
        seq += 1
    return seq


def _exp_id(day: str, seq: int) -> str:
    return f"EXP-{day.replace('-', '')}-{seq:03d}"


def _render_card(exp_id: str, day: str, bucket: dict) -> str:
    occ = bucket["occurrences"]
    signals = sorted(bucket["signals"], key=lambda s: -PRIORITY.get(bucket["signals"][s], 0))
    primary = signals[0] if signals else "manual"
    kind, suggestion = SIGNAL_DEF.get(primary, ("manual-review", "人工判断"))
    priority = max((PRIORITY.get(p, 0) for p in bucket["signals"].values()), default=1)
    pri = {v: k for k, v in PRIORITY.items()}[priority]
    hits = bucket.get("hits") or []
    gents = sorted(bucket.get("graph_entities") or set())
    lines = [
        "---",
        f"exp_id: {exp_id}",
        "status: draft",
        f"created: {day}",
        f"last_seen: {occ[-1].get('ts', '')[:10]}",
        f"signal: {primary}",
        f"signals: [{', '.join(signals)}]",
        f"priority: {pri}",
        f"occurrences: {len(occ)}",
        f"suggestion_kind: {kind}",
        "question: " + json.dumps(bucket["question"], ensure_ascii=False),
        f"source_log: {occ[-1].get('log', '')}",
        f"log_mid: {occ[-1].get('mid', '')}",
        "hits:",
    ]
    for h in hits[:5]:
        lines.append(f"  - kind: {h.get('kind')} | source: {h.get('source')} | score: {h.get('score')}")
    if not hits:
        lines.append("  - (none)")
    lines.append("graph_entities: [" + ", ".join(json.dumps(e, ensure_ascii=False) for e in gents) + "]")
    lines.append("suggestion: " + json.dumps(suggestion, ensure_ascii=False))
    lines += [
        "review:",
        "  verdict: pending",
        "  reviewer:",
        "  reviewed_at:",
        '  action: ""',
        "---",
        "",
        "## 原始会话",
        "",
        f"- 问题：{bucket['question']}",
        f"- 出现次数：{len(occ)}",
    ]
    for o in occ[:10]:
        lines.append(f"  - {o.get('ts', '')} mid={o.get('mid', '')} chat={o.get('chat_type', '')}")
    if len(occ) > 10:
        lines.append(f"  - … 共 {len(occ)} 条，详见 source_log")
    lines += [
        "",
        f"- 最新回答摘录：{(bucket.get('answer_excerpt') or '')[:200]}",
        "",
        "## 信号分析",
        "",
    ]
    for s in signals:
        k, sug = SIGNAL_DEF.get(s, ("?", "?"))
        lines.append(f"- `{s}`（{k}）：{sug}")
    for nid in bucket.get("conflict_nodes") or []:
        lines += ["", "## 冲突边", "", f"- `{nid}` 存在 conflicts_with 边——确认回答已并列呈现各口径"]
    fbs = bucket.get("feedbacks") or []
    if fbs:
        lines += ["", "## 用户反馈", ""]
        for fb in fbs[:10]:
            lines.append(f"- {fb.get('ts', '')} [{fb.get('verdict')}/{fb.get('channel', '')}] "
                         f"{str(fb.get('comment') or '')[:120]}")
    lines += [
        "",
        "## 人审",
        "",
        "verdict 取值：approved（值得修）/ rejected（证伪或无需修）/ needs-info（信息不足）",
        "approved 后执行修订（qa/卡片/图谱边/CONFLICTS），回填 review.action 与 commit，status 改 promoted。",
        "",
    ]
    return "\n".join(lines)


def _aggregate(recs: list[dict], graph) -> dict[str, dict]:
    buckets: dict[str, dict] = {}
    for rec in recs:
        q = str(rec.get("question") or "").strip()
        if not q:
            continue
        key = _norm_question(q)
        b = buckets.setdefault(key, {
            "question": q, "occurrences": [], "signals": {},
            "hits": [], "graph_entities": set(), "answer_excerpt": "",
            "mids": set(),
        })
        if rec.get("mid"):
            b["mids"].add(str(rec["mid"]))
        b["occurrences"].append({
            "ts": rec.get("ts", ""), "mid": rec.get("mid", ""),
            "chat_type": rec.get("chat_type", ""), "log": rec.get("_log", ""),
        })
        for sig, pri in _classify(rec).items():
            b["signals"][sig] = pri
        if not b["hits"] and rec.get("hits"):
            b["hits"] = rec["hits"][:5]
        for e in rec.get("graph_entities") or []:
            b["graph_entities"].add(e)
        if rec.get("answer"):
            b["answer_excerpt"] = str(rec["answer"])
    for b in buckets.values():
        cn = _conflict_nodes(graph, sorted(b["graph_entities"]))
        if cn:
            b["conflict_nodes"] = cn
            b["signals"]["conflict-touch"] = "low"
        n = len(b["occurrences"])
        if n >= 2:
            b["signals"]["repeat"] = "high" if n >= REPEAT_HIGH else "medium"
    return buckets


def cmd_scan(args) -> int:
    logs_dir = Path(args.logs_dir) if args.logs_dir else LOGS_DIR
    recs = _load_logs(logs_dir)
    if not recs:
        print(f"no log records in {logs_dir}")
        return 0

    graph = None
    if GRAPH_DIR.exists():
        try:
            from graph_query import GraphIndex
            graph = GraphIndex(GRAPH_DIR)
        except Exception as exc:
            print(f"[graph load failed, conflict-touch disabled] {exc}", file=sys.stderr)

    buckets = _aggregate(recs, graph)

    # 用户反馈：fb-*.jsonl 的 ref_mid → qa mid → 问题聚合桶
    mid_to_key = {mid: key for key, b in buckets.items() for mid in b.get("mids", set())}
    fb_applied = fb_orphan = 0
    for fb in _load_feedback(logs_dir):
        key = mid_to_key.get(str(fb.get("ref_mid") or ""))
        if not key:
            fb_orphan += 1
            continue
        b = buckets[key]
        if fb.get("verdict") == "up":
            b["signals"]["user-upvote"] = "low"
        else:
            b["signals"]["user-feedback"] = "critical"
        b.setdefault("feedbacks", []).append({
            "ts": fb.get("ts", ""), "verdict": fb.get("verdict", ""),
            "comment": fb.get("comment", ""), "channel": fb.get("channel", ""),
        })
        fb_applied += 1
    if fb_applied or fb_orphan:
        print(f"feedback: {fb_applied} applied, {fb_orphan} orphan (ref_mid 无对应 qa 记录)")

    key_to_id = _question_key_to_id()
    today = datetime.date.today().isoformat()
    taken = {p.stem for p in EXP_DIR.glob("EXP-*.md")}

    plans: list[tuple[str, str, bool]] = []  # (exp_id, content, is_update)
    frozen = 0
    for key, b in sorted(buckets.items()):
        if not b["signals"]:
            continue
        existing = key_to_id.get(key)
        if existing and existing[1] != "draft":
            frozen += 1
            continue  # 已审卡冻结，不再覆盖
        if existing:
            eid = existing[0]
        else:
            eid = _exp_id(today, _next_seq(today, taken))
            taken.add(eid)
        plans.append((eid, _render_card(eid, today, b), bool(existing)))

    if args.dry_run:
        for eid, content, is_upd in plans:
            head = content.splitlines()[1] if content else ""
            print(f"{'update' if is_upd else 'create'} {eid}  {head[:80]}")
        print(f"dry-run: {len(plans)} cards planned "
              f"({sum(1 for _,_,u in plans if u)} updates, "
              f"{sum(1 for _,_,u in plans if not u)} new, {frozen} frozen); "
              f"{len(buckets)} unique questions scanned")
        return 0

    created = updated = 0
    for eid, content, is_upd in plans:
        (EXP_DIR / f"{eid}.md").write_text(content, encoding="utf-8")
        if is_upd:
            updated += 1
        else:
            created += 1
    print(f"scan: {len(recs)} records → {len(buckets)} unique questions → "
          f"{created} created, {updated} updated, {frozen} frozen-skipped")
    return 0


def cmd_list(_args) -> int:
    cards = sorted(EXP_DIR.glob("EXP-*.md"))
    if not cards:
        print("no experience cards")
        return 0
    by_status: dict[str, int] = {}
    by_signal: dict[str, int] = {}
    for p in cards:
        text = p.read_text(encoding="utf-8")
        ms = re.search(r"^status: (\S+)", text, re.M)
        mg = re.search(r"^signal: (\S+)", text, re.M)
        by_status[ms.group(1) if ms else "?"] = by_status.get(ms.group(1) if ms else "?", 0) + 1
        by_signal[mg.group(1) if mg else "?"] = by_signal.get(mg.group(1) if mg else "?", 0) + 1
    print(f"{len(cards)} cards")
    print("status:", dict(sorted(by_status.items())))
    print("signal:", dict(sorted(by_signal.items())))
    return 0


def cmd_set_status(args) -> int:
    path = EXP_DIR / f"{args.exp_id}.md"
    if not path.exists():
        print(f"not found: {path}", file=sys.stderr)
        return 1
    text = path.read_text(encoding="utf-8")
    today = datetime.date.today().isoformat()
    text = re.sub(r"^status: \S+", f"status: {args.status}", text, count=1, flags=re.M)
    if args.verdict:
        text = re.sub(r"^  verdict: .*", f"  verdict: {args.verdict}", text, count=1, flags=re.M)
    if args.reviewer:
        text = re.sub(r"^  reviewer:.*", f"  reviewer: {args.reviewer}", text, count=1, flags=re.M)
    text = re.sub(r"^  reviewed_at:.*", f"  reviewed_at: {today}", text, count=1, flags=re.M)
    if args.action is not None:
        text = re.sub(r'^  action:.*', f'  action: "{args.action}"', text, count=1, flags=re.M)
    path.write_text(text, encoding="utf-8")
    print(f"{args.exp_id} → status={args.status}" + (f" action={args.action}" if args.action else ""))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p_scan = sub.add_parser("scan", help="扫日志生成/更新草稿")
    p_scan.add_argument("--logs-dir", default=None)
    p_scan.add_argument("--dry-run", action="store_true")
    sub.add_parser("list", help="状态统计")
    p_set = sub.add_parser("set-status", help="更新经验卡状态")
    p_set.add_argument("exp_id")
    p_set.add_argument("status", choices=["draft", "approved", "promoted", "rejected", "archived"])
    p_set.add_argument("--action", default=None)
    p_set.add_argument("--verdict", default=None)
    p_set.add_argument("--reviewer", default=None)
    args = ap.parse_args()
    if args.cmd == "scan":
        return cmd_scan(args)
    if args.cmd == "list":
        return cmd_list(args)
    if args.cmd == "set-status":
        return cmd_set_status(args)
    return 1


if __name__ == "__main__":
    sys.exit(main())
