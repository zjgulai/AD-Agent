"""KB MCP Server 测试：tool 层直测（真实 KB 只读断言 + 临时 staging 写测）。"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from kb_ops import graph_query, mcp_server  # noqa: E402


# ---------- kb_search / kb_get_* ----------

def test_tool_search_hits(kb_root):
    out = mcp_server.tool_search("ROAS 下降怎么排查", 5, root=kb_root)
    assert "命中" in out
    assert "score" not in out.splitlines()[0].lower() or "[" in out
    assert "`" in out  # 溯源路径


def test_tool_search_empty(kb_root):
    out = mcp_server.tool_search("zzqxjkvbnm-wqpl", 3, root=kb_root)
    assert "无命中" in out


def test_tool_get_card(kb_root):
    out = mcp_server.tool_get_card("fundamentals", "ad-algo-auto-fields",
                                   root=kb_root)
    assert "广告平台" in out
    assert "cards/fundamentals/ad-algo-auto-fields.md" in out


def test_tool_get_card_invalid(kb_root):
    assert "Error:" in mcp_server.tool_get_card("BAD CLUSTER!", "x", root=kb_root)
    assert "Error:" in mcp_server.tool_get_card("fundamentals", "no-such", root=kb_root)


def test_tool_get_qa_qid(kb_root):
    out = mcp_server.tool_get_qa("meta-ads-diagnosis", "Q1", root=kb_root)
    assert "### Q1." in out
    assert "**A**" in out
    assert "溯源" in out


def test_tool_get_qa_bad_qid(kb_root):
    assert "Error:" in mcp_server.tool_get_qa("meta-ads-diagnosis", "Q999",
                                              root=kb_root)
    assert "Error:" in mcp_server.tool_get_qa("no-such-cluster", root=kb_root)


# ---------- 图谱工具 ----------

def test_graph_search_finds_metric(kb_root):
    out = mcp_server.tool_graph_search("roas", root=kb_root)
    assert "ad:metric:roas" in out
    assert "| id |" in out


def test_graph_search_type_filter(kb_root):
    out = mcp_server.tool_graph_search("roas", type_filter="ad:Metric",
                                       root=kb_root)
    assert "ad:metric:roas" in out
    assert "ad:playbook" not in out


def test_graph_search_no_hit(kb_root):
    out = mcp_server.tool_graph_search("zzz-no-such-node", root=kb_root)
    assert "未找到" in out


def test_graph_neighbors(kb_root):
    out = mcp_server.tool_graph_neighbors("ad:metric:roas", root=kb_root)
    assert "邻居" in out
    assert "ad:sourced_from" in out or "rel" in out


def test_graph_neighbors_not_found(kb_root):
    out = mcp_server.tool_graph_neighbors("ad:no:such", root=kb_root)
    assert "Error:" in out


def test_graph_path(kb_root):
    out = mcp_server.tool_graph_path("ad:src:s9", "ad:metric:roas",
                                     root=kb_root)
    assert "路径" in out and "跳" in out
    assert "ad:sourced_from" in out or "ad:recommends" in out


def test_graph_path_same_node(kb_root):
    out = mcp_server.tool_graph_path("ad:metric:roas", "ad:metric:roas",
                                     root=kb_root)
    assert "相同" in out


def test_graph_community(kb_root):
    out = mcp_server.tool_graph_community("ad:metric:roas", root=kb_root)
    assert "community" in out
    assert "ad:metric:cpa" in out  # 同社区高连接度成员


# ---------- 治理工具 ----------

def test_tool_conflicts(kb_root):
    out = mcp_server.tool_conflicts(root=kb_root)
    assert "冲突总表" in out
    assert "C1" in out
    assert "裁决" in out


def test_tool_stats(kb_root):
    out = mcp_server.tool_stats(root=kb_root)
    assert "cards:" in out
    assert "graph:" in out
    assert "repo commit" in out


def test_tool_audit_ok(kb_root):
    out = mcp_server.tool_audit(root=kb_root)
    assert "overall: OK" in out


# ---------- kb_ingest_propose ----------

def test_ingest_propose_text(tmp_path):
    out = mcp_server.tool_ingest_propose(
        "probe-note.md", content="# 探针\n\nROAS 诊断笔记。" * 30,
        staging=tmp_path)
    assert "摄入提案已受理" in out
    assert "extracted" in out
    items = list((tmp_path / "extracted").glob("*.json"))
    assert len(items) == 1
    assert (tmp_path / "extracted" / f"{items[0].stem}.md").is_file()


def test_ingest_propose_base64(tmp_path):
    import base64
    data = base64.b64encode("# 二进制通道\n内容。".encode()).decode()
    out = mcp_server.tool_ingest_propose("b64-note.md", content_base64=data,
                                         staging=tmp_path)
    assert "摄入提案已受理" in out


def test_ingest_propose_errors(tmp_path):
    assert "Error:" in mcp_server.tool_ingest_propose(
        "x.exe", content="abc", staging=tmp_path)
    assert "Error:" in mcp_server.tool_ingest_propose(
        "x.md", staging=tmp_path)  # 两个内容参数都缺
    assert "Error:" in mcp_server.tool_ingest_propose(
        "x.md", content="a", content_base64="YQ==", staging=tmp_path)  # 同时给
    assert "Error:" in mcp_server.tool_ingest_propose(
        "x.md", content_base64="!!!notb64!!!", staging=tmp_path)


# ---------- graph_query 单元 ----------

def test_load_index_cached(kb_root):
    i1 = graph_query.load_index(kb_root)
    i2 = graph_query.load_index(kb_root)
    assert i1 is i2  # mtime 未变 → 缓存命中
    assert "ad:metric:roas" in i1.nodes
    assert len(i1.adj) > 100


def test_resolve_node_unique_label(kb_root):
    idx = graph_query.load_index(kb_root)
    node, err = graph_query.resolve_node(idx, "ad:metric:roas")
    assert err is None and node["id"] == "ad:metric:roas"
