"""graph_query 回归测试：实体链接/邻居/上下文注入的核心行为。"""

import pytest

from graph_query import GraphIndex


@pytest.fixture(scope="module")
def graph(graph_dir):
    return GraphIndex(graph_dir)


def test_loads_all_shards(graph):
    assert len(graph.nodes) > 500
    assert len(graph.edges) > 900
    assert len(graph.terms) >= 15


def test_resolve_metric_entity(graph):
    hits = graph.resolve("EQ")
    assert hits, "EQ 应命中指标/术语节点"
    types = {graph._node_type(h.node_id) for h in hits}
    assert "ad:Metric" in types or "ad:term" in types


def test_resolve_threshold_symptom(graph):
    hits = graph.resolve("EQ<4")
    assert hits
    assert hits[0].node_id == "ad:symptom:eq-lt4"


def test_resolve_platform_ops_entity(graph):
    hits = graph.resolve("GMV Max")
    assert hits
    assert any("gmv" in h.node_id.lower() for h in hits)


def test_resolve_no_match(graph):
    assert graph.resolve("xyzzy完全无关的字符串") == []


def test_neighbors_direction(graph):
    nbrs = graph.neighbors("ad:metric:eq")
    assert nbrs
    assert all(n["direction"] in {"in", "out"} for n in nbrs)
    assert all(n["relation"].startswith("ad:") for n in nbrs)


def test_neighbors_relation_filter(graph):
    all_n = graph.neighbors("ad:metric:eq")
    thr = graph.neighbors("ad:metric:eq", relation="ad:has_threshold")
    assert thr
    assert all(n["relation"] == "ad:has_threshold" for n in thr)
    assert len(thr) <= len(all_n)


def test_context_for_injects_disambiguation(graph):
    ctx = graph.context_for("EQ<4 会触发什么")
    assert ctx
    assert "EQ<4" in ctx
    # 触发关系或阈值口径至少出现一类
    assert ("triggers" in ctx) or ("has_threshold" in ctx) or ("触发" in ctx)


def test_context_for_empty_on_no_match(graph):
    assert graph.context_for("xyzzy完全无关的字符串") == ""


def test_stats(graph):
    s = graph.stats()
    assert "nodes" in s and "edges" in s and "terms" in s
