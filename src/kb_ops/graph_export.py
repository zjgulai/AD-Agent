"""graph 分片 → 交互式 graph.json + 自包含 graph.html。

模式借鉴 YesIamGodt/knowledge-pipline `tools/build_graph.py`（Louvain 社区 +
vis.js 可视化），差异：我们的边是 schema 校验的策展边（无 EXTRACTED/INFERRED
分层），社区检测只用于着色与聚类视图，不回写源数据。

CLI：python -m kb_ops.graph_export [--open] [--out-dir DIR] [--no-cache]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import webbrowser
from datetime import date
from pathlib import Path

from .paths import graph_dir, graph_dist_dir

# vis.js 中需要箭头的方向性关系；对称关系（conflicts_with/variant_of 等）不画箭头
_DIRECTIONAL = {
    "ad:depends_on", "ad:triggers", "ad:checks", "ad:applies_when", "ad:affects",
    "ad:measures", "ad:has_threshold", "ad:recommends", "ad:implements",
    "ad:escalates_to", "ad:supersedes", "ad:deprecated_by", "ad:sourced_from",
    "ad:defined_in", "ad:pending_data", "ad:belongs_to", "ad:part_of",
    "ad:targets", "ad:involves",
}

# 节点 @type → 颜色（vis.js group）
_TYPE_COLORS = {
    "ad:Playbook": "#4A90D9", "ad:Benchmark": "#50C878", "ad:Rule": "#E85D75",
    "ad:WorkflowStage": "#F5A623", "ad:KnowledgeAsset": "#9B59B6",
    "ad:Metric": "#1ABC9C", "ad:AdProduct": "#34495E", "ad:Platform": "#16A085",
    "ad:Channel": "#27AE60", "ad:Concept": "#8E44AD", "ad:Symptom": "#E67E22",
    "ad:DiagnosisCheck": "#C0392B", "ad:Action": "#2980B9", "ad:Agent": "#8E44AD",
    "ad:AgentLoop": "#7F8C8D", "ad:Role": "#95A5A6", "ad:Audience": "#F39C12",
    "ad:Product": "#2C3E50", "ad:Campaign": "#3D566E", "ad:AdSet": "#5D6D7E",
    "ad:AdEntity": "#707B7C", "ad:Competitor": "#B03A2E", "ad:SourceDoc": "#BDC3C7",
    "ad:LifecycleStage": "#16A085", "ad:HITLGate": "#C0392B",
}
_DEFAULT_COLOR = "#7F8C8D"
_COMMUNITY_COLORS = [
    "#E74C3C", "#3498DB", "#2ECC71", "#F39C12", "#9B59B6", "#1ABC9C",
    "#E67E22", "#34495E", "#16A085", "#C0392B", "#8E44AD", "#F1C40F",
]


def load_shards(inst_dir: Path) -> tuple[dict, list]:
    """加载全部分片，返回 ({@id: node+cluster}, [{edge+cluster}])。

    节点 cluster = 定义它的分片名；@id 跨分片冲突时保留首个（与 graph_query 一致）。
    """
    nodes: dict[str, dict] = {}
    edges: list[dict] = []
    for f in sorted(inst_dir.glob("*.nodes.json")):
        cluster = f.name.removesuffix(".nodes.json")
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        for n in data.get("nodes", []):
            nid = n.get("@id")
            if not nid:
                continue
            if nid in nodes and nodes[nid].get("@type") != n.get("@type"):
                continue
            node = dict(n)
            node["_cluster"] = cluster
            nodes.setdefault(nid, node)
    for f in sorted(inst_dir.glob("*.edges.json")):
        cluster = f.name.removesuffix(".edges.json")
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        for e in data.get("edges", []):
            s, g, r = e.get("source"), e.get("target"), e.get("@type")
            if not (s and g and r):
                continue
            edge = dict(e)
            edge["_cluster"] = cluster
            edges.append(edge)
    return nodes, edges


def detect_communities(nodes: dict, edges: list) -> dict[str, int]:
    """Louvain 社区检测；networkx 缺失时回退为 cluster 序号。"""
    try:
        import networkx as nx
        from networkx.algorithms import community as nx_community
    except ImportError:
        return {nid: abs(hash(n.get("_cluster", ""))) % 997 for nid, n in nodes.items()}
    G = nx.Graph()
    G.add_nodes_from(nodes.keys())
    for e in edges:
        if e["source"] in nodes and e["target"] in nodes:
            G.add_edge(e["source"], e["target"])
    comms = nx_community.louvain_communities(G, seed=42)
    out: dict[str, int] = {}
    for i, members in enumerate(comms):
        for nid in members:
            out[nid] = i
    # 孤立节点（无边）不在任何 community 里
    for nid in nodes:
        out.setdefault(nid, -1)
    return out


def build_graph(nodes: dict, edges: list) -> dict:
    communities = detect_communities(nodes, edges)
    degree: dict[str, int] = {nid: 0 for nid in nodes}
    valid_edges = []
    for e in edges:
        if e["source"] not in nodes or e["target"] not in nodes:
            continue
        degree[e["source"]] += 1
        degree[e["target"]] += 1
        item = {
            "source": e["source"], "target": e["target"],
            "type": e["@type"], "ref": e.get("ref", ""),
            "cluster": e.get("_cluster", ""),
        }
        for k in ("note", "when"):
            if e.get(k):
                item[k] = e[k]
        valid_edges.append(item)

    out_nodes = []
    for nid, n in nodes.items():
        props = {k: v for k, v in n.items() if not k.startswith("_") and k not in ("@id", "@type", "label")}
        out_nodes.append({
            "id": nid,
            "label": n.get("label") or nid.rsplit(":", 1)[-1],
            "type": n.get("@type", "?"),
            "cluster": n.get("_cluster", ""),
            "community": communities.get(nid, -1),
            "degree": degree.get(nid, 0),
            "props": props,
        })

    clusters = sorted({n["cluster"] for n in out_nodes if n["cluster"]})
    types = sorted({n["type"] for n in out_nodes})
    return {
        "generated": str(date.today()),
        "stats": {
            "nodes": len(out_nodes), "edges": len(valid_edges),
            "communities": len({c for c in communities.values() if c >= 0}),
            "clusters": clusters, "types": types,
        },
        "nodes": out_nodes,
        "edges": valid_edges,
    }


def _inputs_hash(inst_dir: Path) -> str:
    h = hashlib.sha256()
    for f in sorted(inst_dir.glob("*.json")):
        h.update(f.name.encode())
        h.update(f.read_bytes())
    return h.hexdigest()


def export(out_dir: Path | None = None, use_cache: bool = True) -> tuple[Path, Path, dict]:
    inst_dir = graph_dir() / "instances"
    out_dir = out_dir or graph_dist_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "graph.json"
    html_path = out_dir / "graph.html"
    cache_path = out_dir / ".graph-cache.json"

    digest = _inputs_hash(inst_dir)
    if use_cache and cache_path.is_file() and json_path.is_file() and html_path.is_file():
        try:
            if json.loads(cache_path.read_text()).get("hash") == digest:
                data = json.loads(json_path.read_text(encoding="utf-8"))
                return json_path, html_path, data
        except Exception:
            pass

    nodes, edges = load_shards(inst_dir)
    data = build_graph(nodes, edges)
    json_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    html_path.write_text(render_html(data), encoding="utf-8")
    cache_path.write_text(json.dumps({"hash": digest, "generated": data["generated"]}))
    return json_path, html_path, data


_VIS_CDN = "https://unpkg.com/vis-network@9.1.9/standalone/umd/vis-network.min.js"


def _vis_script_tag() -> str:
    """优先内联 vendor 文件（真自包含），缺失时回退 CDN。"""
    vendor = Path(__file__).resolve().parent / "static" / "vendor" / "vis-network.min.js"
    if vendor.is_file():
        return f"<script>\n{vendor.read_text(encoding='utf-8')}\n</script>"
    return f'<script src="{_VIS_CDN}"></script>'


def render_html(data: dict) -> str:
    nodes_js = json.dumps([
        {
            "id": n["id"], "label": n["label"], "group": n["type"],
            "cluster": n["cluster"], "community": n["community"],
            "degree": n["degree"], "type": n["type"], "props": n["props"],
        }
        for n in data["nodes"]
    ], ensure_ascii=False)
    edges_js = json.dumps([
        {
            "from": e["source"], "to": e["target"], "label": e["type"].replace("ad:", ""),
            "title": e.get("ref", ""), "cluster": e["cluster"],
            "arrows": "to" if e["type"] in _DIRECTIONAL else "",
        }
        for e in data["edges"]
    ], ensure_ascii=False)
    type_colors = json.dumps(_TYPE_COLORS, ensure_ascii=False)
    comm_colors = json.dumps(_COMMUNITY_COLORS)

    return f"""<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="utf-8">
<title>ad-agent-qa 知识图谱</title>
<style>
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; font-family: -apple-system, "PingFang SC", sans-serif; display: flex; height: 100vh; }}
  #sidebar {{ width: 300px; background: #1a1d23; color: #dfe3e8; padding: 14px; overflow-y: auto; flex-shrink: 0; }}
  #sidebar h1 {{ font-size: 15px; margin: 0 0 4px; }}
  #sidebar .stats {{ font-size: 12px; color: #8b93a1; margin-bottom: 12px; }}
  #search {{ width: 100%; padding: 7px 10px; border-radius: 6px; border: 1px solid #3a4150; background: #262a33; color: #fff; margin-bottom: 10px; }}
  .filter-group {{ margin-bottom: 10px; }}
  .filter-group label {{ display: block; font-size: 11px; color: #8b93a1; margin-bottom: 4px; text-transform: uppercase; letter-spacing: .5px; }}
  select {{ width: 100%; padding: 5px; border-radius: 5px; border: 1px solid #3a4150; background: #262a33; color: #fff; font-size: 12px; }}
  #detail {{ margin-top: 14px; font-size: 12px; border-top: 1px solid #3a4150; padding-top: 10px; display: none; }}
  #detail h3 {{ margin: 0 0 6px; font-size: 13px; color: #fff; word-break: break-all; }}
  #detail .meta {{ color: #8b93a1; margin-bottom: 8px; }}
  #detail table {{ width: 100%; border-collapse: collapse; }}
  #detail td {{ padding: 3px 4px; border-bottom: 1px solid #2a2f3a; vertical-align: top; word-break: break-all; }}
  #detail td:first-child {{ color: #8b93a1; white-space: nowrap; width: 70px; }}
  #detail .nbr {{ cursor: pointer; color: #6cb6ff; }}
  #detail .nbr:hover {{ text-decoration: underline; }}
  #graph {{ flex: 1; }}
  .legend {{ font-size: 11px; color: #8b93a1; margin-top: 10px; }}
</style>
</head>
<body>
<div id="sidebar">
  <h1>ad-agent-qa 知识图谱</h1>
  <div class="stats" id="stats"></div>
  <input id="search" placeholder="搜索节点 label / @id…">
  <div class="filter-group"><label>类型</label><select id="typeFilter"><option value="">全部类型</option></select></div>
  <div class="filter-group"><label>分片</label><select id="clusterFilter"><option value="">全部分片</option></select></div>
  <div class="filter-group"><label>关系</label><select id="relFilter"><option value="">全部关系</option></select></div>
  <div id="detail"></div>
  <div class="legend">填充色=节点类型 · 描边色=社区(Louvain)<br>箭头=方向性关系 · 数据生成于 {data["generated"]}</div>
</div>
<div id="graph"></div>
{_vis_script_tag()}
<script>
const NODES = {nodes_js};
const EDGES = {edges_js};
const TYPE_COLORS = {type_colors};
const COMM_COLORS = {comm_colors};
const STATS = {json.dumps(data["stats"], ensure_ascii=False)};

const byId = new Map(NODES.map(n => [n.id, n]));
const adj = new Map();
EDGES.forEach(e => {{
  if (!adj.has(e.from)) adj.set(e.from, []);
  adj.get(e.from).push({{rel: e.label, other: e.to, dir: "out", ref: e.title}});
  if (!adj.has(e.to)) adj.set(e.to, []);
  adj.get(e.to).push({{rel: e.label, other: e.from, dir: "in", ref: e.title}});
}});

const search = document.getElementById("search");
const typeFilter = document.getElementById("typeFilter");
const clusterFilter = document.getElementById("clusterFilter");
const relFilter = document.getElementById("relFilter");

const nodesDS = new vis.DataSet(NODES.map(n => {{
  const commColor = n.community >= 0 ? COMM_COLORS[n.community % COMM_COLORS.length] : "#555";
  return {{
    id: n.id, label: n.label,
    color: {{ background: TYPE_COLORS[n.type] || "#7F8C8D", border: commColor, highlight: {{ border: commColor }} }},
    borderWidth: n.community >= 0 ? 3 : 1,
    font: {{ color: "#dfe3e8", size: 11, face: "PingFang SC, sans-serif", strokeWidth: 2, strokeColor: "#1a1d23" }},
    shape: "dot", size: Math.min(6 + Math.sqrt(n.degree) * 2.5, 22),
    title: n.id + "\\n" + n.type,
    _type: n.type, _cluster: n.cluster,
  }};
}}));
const edgesDS = new vis.DataSet(EDGES.map((e, i) => {{
  const dir = e.arrows === "to";
  return {{ id: i, from: e.from, to: e.to, label: e.label, title: e.title,
    arrows: dir ? "to" : "", color: {{ color: dir ? "#5b6b7f" : "#3a4150", highlight: "#6cb6ff" }},
    font: {{ color: "#6b7484", size: 8, align: "middle" }}, smooth: {{ type: "continuous" }} }};
}}));

const network = new vis.Network(document.getElementById("graph"),
  {{ nodes: nodesDS, edges: edgesDS }},
  {{ physics: {{ stabilization: true, barnesHut: {{ gravitationalConstant: -6000, springLength: 90 }} }},
     interaction: {{ hover: true, tooltipDelay: 120, navigationButtons: true }},
     nodes: {{ shape: "dot" }} }});

document.getElementById("stats").textContent =
  `${{STATS.nodes}} 节点 · ${{STATS.edges}} 边 · ${{STATS.communities}} 社区 · ${{STATS.clusters.length}} 分片`;

// 筛选器
[...new Set(NODES.map(n => n.type))].sort().forEach(t =>
  typeFilter.add(new Option(t, t)));
[...new Set(NODES.map(n => n.cluster))].sort().forEach(c =>
  clusterFilter.add(new Option(c, c)));
[...new Set(EDGES.map(e => e.label))].sort().forEach(r =>
  relFilter.add(new Option(r, r)));

function applyFilters() {{
  const q = search.value.trim().toLowerCase();
  const tf = typeFilter.value, cf = clusterFilter.value, rf = relFilter.value;
  nodesDS.update(NODES.map(n => {{
    let vis = true;
    if (tf && n.type !== tf) vis = false;
    if (cf && n.cluster !== cf) vis = false;
    if (rf) {{
      const hasRel = (adj.get(n.id) || []).some(a => a.rel === rf);
      if (!hasRel) vis = false;
    }}
    if (q && !(n.id.toLowerCase().includes(q) || n.label.toLowerCase().includes(q))) vis = false;
    return {{ id: n.id, hidden: !vis }};
  }}));
  const visibleNodes = new Set(nodesDS.get({{ filter: n => !n.hidden }}).map(n => n.id));
  edgesDS.update(EDGES.map((e, i) => ({{ id: i, hidden: !(visibleNodes.has(e.from) && visibleNodes.has(e.to)) }})));
}}
[search, typeFilter, clusterFilter, relFilter].forEach(el => el.addEventListener("input", applyFilters));

// 节点详情
function showDetail(id) {{
  const n = byId.get(id); if (!n) return;
  const d = document.getElementById("detail");
  const propsRows = Object.entries(n.props || {{}})
    .map(([k, v]) => `<tr><td>${{k}}</td><td>${{typeof v === "object" ? JSON.stringify(v) : v}}</td></tr>`).join("");
  const nbrs = (adj.get(id) || []).slice(0, 30).map(nb => {{
    const arrow = nb.dir === "out" ? "→" : "←";
    return `<div class="nbr" onclick="focusNode('${{nb.other.replace(/'/g, "\\\\'")}}')">${{arrow}} ${{nb.rel}} ${{byId.get(nb.other)?.label || nb.other}}</div>`;
  }}).join("");
  d.style.display = "block";
  d.innerHTML = `<h3>${{n.label}}</h3>
    <div class="meta">${{n.id}}<br>${{n.type}} · ${{n.cluster}} · 社区${{n.community >= 0 ? n.community : "—"}} · 度${{n.degree}}</div>
    ${{propsRows ? `<table>${{propsRows}}</table>` : ""}}
    <div style="margin-top:8px;color:#8b93a1">邻居:</div>${{nbrs || "<i>无</i>"}}`;
}}
window.focusNode = function(id) {{ network.focus(id, {{ scale: 1.2, animation: true }}); showDetail(id); }};
network.on("click", p => {{ if (p.nodes.length) showDetail(p.nodes[0]); }});
network.once("stabilizationIterationsDone", () => network.setOptions({{ physics: {{ enabled: false }} }}));
</script>
</body>
</html>"""


def main() -> None:
    ap = argparse.ArgumentParser(description="导出知识图谱 graph.json + graph.html")
    ap.add_argument("--open", action="store_true", help="生成后用浏览器打开 graph.html")
    ap.add_argument("--out-dir", type=Path, default=None)
    ap.add_argument("--no-cache", action="store_true")
    args = ap.parse_args()

    json_path, html_path, data = export(args.out_dir, use_cache=not args.no_cache)
    s = data["stats"]
    print(f"graph: {s['nodes']} nodes / {s['edges']} edges / {s['communities']} communities")
    print(f"  json → {json_path}")
    print(f"  html → {html_path}")
    if args.open:
        webbrowser.open(html_path.as_uri())


if __name__ == "__main__":
    main()
