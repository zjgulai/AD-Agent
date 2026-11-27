"""KB 图谱查询层：节点解析 / 邻居 / 最短路径 / 社区。

数据源 service.get_graph()（dist/graph.json，缺失自动重建）。
返回 markdown 文本，供 MCP 工具与未来 HTTP 端点复用。
遍历口径：无向（双向都算邻居），边方向仅作标注。
"""

from __future__ import annotations

from collections import deque
from pathlib import Path

from .web import service

MAX_NEIGHBORS = 100
MAX_COMMUNITY = 50
MAX_PATH_DEPTH = 6
MAX_PATH_VISITS = 500
_SEARCH_LIMIT = 10


class GraphIndex:
    """graph.json 的内存索引：节点表 + 邻接表（邻居, 关系类型, 方向）。

    adj[x] 中 dir 语义：">" 表示 x 是边的 source（x -[rel]-> nbr），
    "<" 表示 x 是边的 target（nbr -[rel]-> x）。
    """

    def __init__(self, data: dict) -> None:
        self.data = data
        self.nodes: dict[str, dict] = {
            n["id"]: n for n in data.get("nodes", []) if n.get("id")
        }
        self.adj: dict[str, list[tuple[str, str, str]]] = {}
        for e in data.get("edges", []):
            s, t = e.get("source"), e.get("target")
            if not s or not t:
                continue
            rel = e.get("type") or ""
            self.adj.setdefault(s, []).append((t, rel, ">"))
            self.adj.setdefault(t, []).append((s, rel, "<"))


_CACHE: dict[Path, tuple[float, GraphIndex]] = {}


def load_index(root: Path) -> GraphIndex:
    """按 graph.json mtime 缓存 GraphIndex，KB 重建图谱后自动失效。"""
    data = service.get_graph(root)  # 内部已处理缺失重建与缓存
    json_path = root / "graph" / "dist" / "graph.json"
    try:
        mtime = json_path.stat().st_mtime
    except OSError:
        mtime = 0.0
    ent = _CACHE.get(root)
    if ent is None or ent[0] != mtime:
        ent = (mtime, GraphIndex(data))
        _CACHE[root] = ent
    return ent[1]


def _fmt_node(n: dict) -> str:
    label = n.get("label") or n["id"]
    return f"`{n['id']}` — {label}"


def search_nodes(index: GraphIndex, query: str,
                 type_filter: str | None = None,
                 cluster: str | None = None) -> list[dict]:
    """id/label 子串匹配，id 精确 > label 子串 > id 子串；degree 降序。"""
    q = query.strip().lower()
    if not q:
        return []
    hits: list[tuple[int, dict]] = []
    for n in index.nodes.values():
        if type_filter and not (n.get("type") or "").startswith(type_filter):
            continue
        if cluster and n.get("cluster") != cluster:
            continue
        nid = n["id"].lower()
        label = (n.get("label") or "").lower()
        if q == nid or q == label:
            score = 0
        elif q in label:
            score = 1
        elif q in nid:
            score = 2
        else:
            continue
        hits.append((score, n))
    hits.sort(key=lambda x: (x[0], -(x[1].get("degree") or 0)))
    return [n for _, n in hits[:_SEARCH_LIMIT]]


def resolve_node(index: GraphIndex, ref: str) -> tuple[dict | None, str | None]:
    """把用户输入解析为单个节点。

    返回 (node, None) 或 (None, markdown 错误/消歧提示)。
    """
    ref = ref.strip()
    if ref in index.nodes:
        return index.nodes[ref], None
    cands = search_nodes(index, ref)
    if not cands:
        return None, (f"Error: node not found: `{ref}`\n"
                      "提示：用 kb_graph_search 先解析节点 id。")
    if len(cands) == 1:
        return cands[0], None
    lines = [f"Error: ambiguous node `{ref}`，候选 {len(cands)} 个：",
             "| id | label | type | degree |", "|---|---|---|---|"]
    for n in cands:
        lines.append(f"| `{n['id']}` | {n.get('label') or ''} "
                     f"| {n.get('type') or ''} | {n.get('degree') or 0} |")
    lines.append("请用精确 id 重试（kb_graph_neighbors/path/community）。")
    return None, "\n".join(lines)


def tool_graph_search(root: Path, query: str,
                      type_filter: str | None = None,
                      cluster: str | None = None) -> str:
    index = load_index(root)
    hits = search_nodes(index, query, type_filter, cluster)
    if not hits:
        return f"未找到匹配节点：`{query}`" + (
            f"（type={type_filter} cluster={cluster}）"
            if type_filter or cluster else "")
    lines = [f"匹配节点 {len(hits)} 个（query=`{query}`）：",
             "| id | label | type | cluster | degree |",
             "|---|---|---|---|---|"]
    for n in hits:
        lines.append(
            f"| `{n['id']}` | {n.get('label') or ''} "
            f"| {n.get('type') or ''} | {n.get('cluster') or ''} "
            f"| {n.get('degree') or 0} |")
    return "\n".join(lines)


def tool_graph_neighbors(root: Path, node_ref: str) -> str:
    index = load_index(root)
    node, err = resolve_node(index, node_ref)
    if err:
        return err
    assert node is not None
    # 聚合：nbr -> (rels set, dirs set)
    agg: dict[str, tuple[set[str], set[str]]] = {}
    for nbr, rel, d in index.adj.get(node["id"], []):
        rels, dirs = agg.setdefault(nbr, (set(), set()))
        if rel:
            rels.add(rel)
        dirs.add(d)
    if not agg:
        return f"{_fmt_node(node)} 没有邻居（孤立节点）。"
    items = sorted(agg.items(),
                   key=lambda kv: (-len(kv[1][0]), index.nodes.get(kv[0], {}).get("degree") or 0))
    total = len(items)
    shown = items[:MAX_NEIGHBORS]
    lines = [
        f"## {_fmt_node(node)}",
        f"type: {node.get('type') or '-'} · cluster: {node.get('cluster') or '-'} "
        f"· degree: {node.get('degree') or 0} · community: {node.get('community')}",
        f"邻居 {total} 个" + (f"（显示前 {MAX_NEIGHBORS}）" if total > MAX_NEIGHBORS else "")
        + "；out=中心 -[rel]-> 邻居，in=邻居 -[rel]-> 中心",
        "",
        "| neighbor | label | rel | dir |",
        "|---|---|---|---|",
    ]
    for nbr, (rels, dirs) in shown:
        n = index.nodes.get(nbr, {})
        d = "".join(sorted(dirs))
        lines.append(
            f"| `{nbr}` | {n.get('label') or ''} "
            f"| {', '.join(sorted(rels)) or '-'} | {d} |")
    return "\n".join(lines)


def tool_graph_path(root: Path, source_ref: str, target_ref: str) -> str:
    index = load_index(root)
    src, err = resolve_node(index, source_ref)
    if err:
        return err
    dst, err = resolve_node(index, target_ref)
    if err:
        return err
    assert src is not None and dst is not None
    if src["id"] == dst["id"]:
        return f"起点与终点相同：`{src['id']}`"

    # BFS：parent[v] = (u, rel, dir_of_u)，dir_of_u ">" 表示 u -[rel]-> v
    sid, did = src["id"], dst["id"]
    parent: dict[str, tuple[str, str, str]] = {}
    visited = {sid}
    queue = deque([sid])
    found = False
    while queue and len(visited) <= MAX_PATH_VISITS and not found:
        u = queue.popleft()
        depth = 0  # parent 链长度即 BFS 深度
        x = u
        while x in parent:
            x = parent[x][0]
            depth += 1
        if depth >= MAX_PATH_DEPTH:
            continue
        for v, rel, direction in index.adj.get(u, []):
            if v in visited:
                continue
            # direction ">" : u -[rel]-> v ; "<" : v -[rel]-> u
            parent[v] = (u, rel, direction)
            visited.add(v)
            if v == did:
                found = True
                break
            queue.append(v)

    if not found:
        return (f"Error: no path within {MAX_PATH_DEPTH} hops "
                f"（{sid} → {did}）")
    # 回溯：seq 为遍历顺序节点序列；edges 为每条树边的真实方向 a -[rel]-> b
    # （BFS 可能逆边遍历，故边方向不一定与路径方向一致，如实标注）
    seq = [did]
    edges: list[tuple[str, str, str]] = []
    cur = did
    while cur != sid:
        u, rel, direction = parent[cur]
        seq.append(u)
        edges.append((u, rel, cur) if direction == ">" else (cur, rel, u))
        cur = u
    seq.reverse()
    edges.reverse()
    lines = [f"路径 {len(edges)} 跳：{' → '.join(f'`{p}`' for p in seq)}", ""]
    for a, rel, b in edges:
        lines.append(f"- `{a}` -[{rel or '?'}]-> `{b}`")
    return "\n".join(lines)


def tool_graph_community(root: Path, node_ref: str) -> str:
    index = load_index(root)
    node, err = resolve_node(index, node_ref)
    if err:
        return err
    assert node is not None
    cid = node.get("community")
    members = [n for n in index.nodes.values() if n.get("community") == cid]
    members.sort(key=lambda n: -(n.get("degree") or 0))
    total = len(members)
    shown = members[:MAX_COMMUNITY]
    lines = [
        f"节点 `{node['id']}` 属于 community **{cid}**，共 {total} 个成员"
        + (f"（按 degree 显示前 {MAX_COMMUNITY}）" if total > MAX_COMMUNITY else ""),
        "",
        "| id | label | type | degree |",
        "|---|---|---|---|",
    ]
    for n in shown:
        lines.append(
            f"| `{n['id']}` | {n.get('label') or ''} "
            f"| {n.get('type') or ''} | {n.get('degree') or 0} |")
    return "\n".join(lines)
