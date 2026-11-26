"""graph_query — 广告投放域知识图谱查询包（多消费者契约）。

消费 `docs/knowledge/ad-agent-qa/graph/` 下的 schema + instances 分片：
- 实体链接：把自然语言问题解析成图谱节点（label/@id/term 三级匹配）
- 邻居遍历：按关系类型取一阶（可多跳）邻居
- 上下文装配：把「实体 + 阈值口径 + 冲突边 + 关联 playbook/action」
  渲染成可直接注入 LLM 的紧凑文本块

设计约束：
- 只读、零依赖（stdlib）、加载失败返回空上下文（调用方降级）
- consumers: kb_bot（实体链接增强）、graph/tools CLI、未来 SCN-011 Agent
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

# 上下文渲染时优先展示的关系（噪声大的 sourced_from/belongs_to 降级）
_PRIMARY_RELATIONS = [
    "conflicts_with", "variant_of", "has_threshold", "checks", "triggers",
    "applies_when", "affects", "implements", "escalates_to", "pending_data",
    "recommends", "depends_on", "alternative_to", "targets", "measures",
    "involves", "part_of", "deprecated_by", "supersedes", "cross_domain_ref",
    "belongs_to", "sourced_from",
]
_RELATION_LABEL = {
    "conflicts_with": "冲突", "variant_of": "口径变体", "has_threshold": "阈值",
    "checks": "检查", "triggers": "触发", "applies_when": "适用条件",
    "affects": "影响", "implements": "实现", "escalates_to": "升级",
    "pending_data": "待数据", "recommends": "推荐", "depends_on": "依赖",
    "alternative_to": "替代", "targets": "定向", "measures": "度量",
    "involves": "涉及", "part_of": "属于", "deprecated_by": "被弃用",
    "supersedes": "取代", "cross_domain_ref": "跨域引用",
    "belongs_to": "归属", "sourced_from": "来源",
}

# 实体链接时跳过的节点类型（SourceDoc 是溯源容器不是实体；
# KnowledgeAsset 保留——pops 分片的 overlay/case/experiment 是高价值实体）
_SKIP_TYPES = {"ad:SourceDoc"}

MAX_CONTEXT_CHARS = 1400


@dataclass
class EntityHit:
    node_id: str
    node_type: str
    label: str
    score: float
    via: str  # label | id | term


@dataclass
class GraphIndex:
    graph_dir: Path
    nodes: dict = field(default_factory=dict)   # @id -> node dict
    edges: list = field(default_factory=list)   # edge dicts
    terms: dict = field(default_factory=dict)   # term_id -> term dict
    _adj: dict = field(default_factory=dict, init=False)  # node_id -> [edge]
    _labels: list = field(default_factory=list, init=False)  # (haystack, node_id, via, score_bonus)

    def __post_init__(self) -> None:
        self._load()

    # ---------- 加载 ----------

    def _load(self) -> None:
        inst = self.graph_dir / "instances"
        if not inst.is_dir():
            return
        for f in sorted(inst.glob("*.nodes.json")):
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
            except Exception:
                continue
            for n in data.get("nodes", []):
                nid = n.get("@id")
                if not nid:
                    continue
                if nid in self.nodes and self.nodes[nid].get("@type") != n.get("@type"):
                    continue  # 跨分片 @type 冲突时保留首个（validator 已保证一致）
                self.nodes.setdefault(nid, n)
        for f in sorted(inst.glob("*.edges.json")):
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
            except Exception:
                continue
            self.edges.extend(data.get("edges", []))
        terms_file = self.graph_dir / "schema" / "terms.json"
        if terms_file.is_file():
            try:
                data = json.loads(terms_file.read_text(encoding="utf-8"))
                items = data.get("terms", data if isinstance(data, list) else [])
                for t in items:
                    tid = t.get("term_id") or t.get("@id") or t.get("id")
                    if tid:
                        self.terms[tid] = t
            except Exception:
                pass
        # 邻接表（无向：边两端都可达）
        for e in self.edges:
            s, g, r = e.get("source"), e.get("target"), e.get("@type")
            if not (s and g and r):
                continue
            self._adj.setdefault(s, []).append((r, g, "out", e))
            self._adj.setdefault(g, []).append((r, s, "in", e))
        # 实体链接索引
        for nid, n in self.nodes.items():
            if n.get("@type") in _SKIP_TYPES:
                continue
            label = (n.get("label") or "").strip()
            if label:
                self._labels.append((label.lower(), nid, "label", 3.0))
            tail = nid.rsplit(":", 1)[-1]
            phrase = tail.replace("-", " ").lower()
            if len(phrase) >= 2:
                self._labels.append((phrase, nid, "id", 1.5))
            last = tail.rsplit("-", 1)[-1].lower()
            if len(last) >= 2 and last != phrase:
                self._labels.append((last, nid, "id_last", 1.0))
        for tid, t in self.terms.items():
            for alias in [t.get("term_id"), t.get("label"), t.get("zh"), t.get("en")] + list(t.get("alt_labels", []) or []):
                if alias and len(str(alias)) >= 2:
                    self._labels.append((str(alias).lower(), tid if tid.startswith("ad:") else f"ad:term:{tid}", "term", 2.5))

    # ---------- 查询 API ----------

    def node(self, node_id: str) -> dict | None:
        return self.nodes.get(node_id) or self.terms.get(node_id)

    def neighbors(self, node_id: str, relation: str | None = None,
                  direction: str = "both") -> list[dict]:
        """返回 [{relation, other, direction, note, when}]，direction=out|in|both。"""
        out = []
        for r, other, d, e in self._adj.get(node_id, []):
            if relation and r != relation:
                continue
            if direction != "both" and d != direction:
                continue
            item = {"relation": r, "other": other, "direction": d}
            for k in ("note", "when", "ref"):
                if e.get(k):
                    item[k] = e[k]
            out.append(item)
        return out

    def resolve(self, text: str, limit: int = 5) -> list[EntityHit]:
        """实体链接：问题文本 → 图谱节点。label 精确子串 > term 别名 > id 片段。"""
        q = text.lower()
        q_tokens = set(re.findall(r"[a-z0-9]+|[一-鿿]{2,}", q))
        # CJK bigram 集合：中文无空格分词，bigram 是最稳的局部匹配信号
        q_bg: set[str] = set()
        for run in re.findall(r"[一-鿿]+", q):
            if len(run) >= 2:
                q_bg.update(run[i : i + 2] for i in range(len(run) - 1))
        hits: dict[str, EntityHit] = {}
        for hay, nid, via, bonus in self._labels:
            n = self.nodes.get(nid) or self.terms.get(nid)
            if not n:
                continue
            ntype = n.get("@type") or "ad:term"
            if ntype in _SKIP_TYPES:
                continue
            score = 0.0
            if via == "label":
                if hay in q:
                    score = 10.0 + bonus + min(len(hay), 20) * 0.1
                else:
                    # token 重合度 + CJK bigram 重合度双通道
                    lt = {t for t in re.findall(r"[a-z0-9]+|[一-鿿]{2,}", hay) if len(t) >= 2}
                    shared = lt & q_tokens
                    ratio = len(shared) / len(lt) if lt else 0.0
                    if shared and ratio >= 0.4:
                        score += 4.0 + 4.0 * ratio
                    h_bg: set[str] = set()
                    for run in re.findall(r"[一-鿿]+", hay):
                        if len(run) >= 2:
                            h_bg.update(run[i : i + 2] for i in range(len(run) - 1))
                    score += min(5.0, 1.4 * len(h_bg & q_bg))
                    score += bonus
            elif via == "term" and hay in q:
                score = 8.0 + bonus
            elif via in {"id", "id_last"}:
                phrase = hay.replace(" ", "-")
                if via == "id" and phrase in q.replace(" ", "-"):
                    score = 6.0 + bonus
                elif hay in q_tokens or phrase in q_tokens:
                    score = (5.0 if via == "id" else 4.0) + bonus
            if score < 5.0:
                continue
            label = n.get("label") or n.get("term_id") or nid
            cur = hits.get(nid)
            if cur is None or score > cur.score:
                hits[nid] = EntityHit(nid, ntype, label, round(score, 2), via)
        ranked = sorted(hits.values(), key=lambda h: -h.score)
        # 同分时 label 命中优先
        ranked.sort(key=lambda h: -(h.score + (2 if h.via == "label" else 0)))
        return ranked[:limit]

    def _node_label(self, nid: str) -> str:
        n = self.nodes.get(nid) or self.terms.get(nid)
        if not n:
            return nid
        return n.get("label") or n.get("term_id") or nid

    def _node_type(self, nid: str) -> str:
        n = self.nodes.get(nid) or self.terms.get(nid) or {}
        return n.get("@type") or ("ad:term" if nid.startswith("ad:term") else "?")

    def context_for(self, query: str, max_entities: int = 3,
                    max_neighbors: int = 10) -> str:
        """问题 → 紧凑图谱上下文文本（供 LLM 注入）。无命中返回空串。"""
        hits = self.resolve(query, limit=max_entities)
        if not hits:
            return ""
        lines: list[str] = []
        used = 0
        for h in hits:
            if used >= MAX_CONTEXT_CHARS:
                break
            header = f"· {h.label}（{h.node_id}｜{h.node_type}）"
            lines.append(header)
            used += len(header)
            # term 消歧优先展示
            if h.node_id.startswith("ad:term:") or h.via == "term":
                t = self.terms.get(h.node_id) or self.terms.get(h.node_id.replace("ad:term:", "", 1))
                if t:
                    dis = t.get("disambiguation") or t.get("definition") or ""
                    if dis:
                        seg = f"  消歧：{str(dis)[:120]}"
                        lines.append(seg)
                        used += len(seg)
            # 收集邻居，按关系优先级排序
            nbrs = self.neighbors(h.node_id)
            nbrs.sort(key=lambda x: _PRIMARY_RELATIONS.index(x["relation"])
                      if x["relation"] in _PRIMARY_RELATIONS else 99)
            shown = 0
            for nb in nbrs:
                if shown >= max_neighbors or used >= MAX_CONTEXT_CHARS:
                    break
                rel = _RELATION_LABEL.get(nb["relation"], nb["relation"])
                direction = "→" if nb["direction"] == "out" else "←"
                target = self._node_label(nb["other"])
                extra = ""
                if nb.get("note"):
                    extra += f"（{str(nb['note'])[:60]}）"
                if nb.get("when"):
                    extra += f" when={str(nb['when'])[:60]}"
                seg = f"  {direction} {rel} {target}{extra}"
                lines.append(seg)
                used += len(seg)
                shown += 1
        return "\n".join(lines)

    def stats(self) -> str:
        types: dict[str, int] = {}
        for n in self.nodes.values():
            t = n.get("@type", "?")
            types[t] = types.get(t, 0) + 1
        rels: dict[str, int] = {}
        for e in self.edges:
            r = e.get("@type", "?")
            rels[r] = rels.get(r, 0) + 1
        return (f"{len(self.nodes)} nodes / {len(self.edges)} edges / "
                f"{len(self.terms)} terms @ {self.graph_dir}")
