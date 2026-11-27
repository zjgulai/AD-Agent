"""kb_ops 运维层测试：BM25 检索 / 图谱导出 / 语义 lint / audit 解析。"""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from kb_ops import audit_runner, graph_export, lint_semantic, retrieval  # noqa: E402


# ---------- retrieval ----------

def test_tokenize_mixed():
    toks = retrieval.tokenize("Meta 广告 ROAS 优化")
    assert "meta" in toks
    assert "roas" in toks
    assert any("广告" in t or "告" in t for t in toks) or "广告" in toks or any(len(t) == 2 for t in toks)


def test_bm25_ranking():
    idx = retrieval.BM25Index()
    idx.add("a", "独立站转化率优化 落地页 CRO")
    idx.add("b", "Meta 广告出价策略 日预算")
    idx.add("c", "独立站 SEO 关键词 外链建设")
    hits = idx.search("独立站转化率", top_k=3)
    assert hits and hits[0][0] == "a"


def test_search_kb_real(kb_root):
    hits = retrieval.search_kb(kb_root, "独立站转化率怎么优化", top_k=5)
    assert hits, "真实 KB 应有命中"
    top_sources = {c.source for c, _ in hits}
    assert any("dsite-cro" in s for s in top_sources)


# ---------- graph_export ----------

def test_load_shards_has_cluster(kb_root):
    nodes, edges = graph_export.load_shards(kb_root / "graph" / "instances")
    assert len(nodes) > 500 and len(edges) > 1000
    assert all("_cluster" in n for n in nodes.values())
    assert all("_cluster" in e for e in edges)


def test_export_produces_json_and_html(kb_root, tmp_path):
    json_path, html_path, data = graph_export.export(out_dir=tmp_path, use_cache=False)
    assert json_path.is_file() and html_path.is_file()
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload["stats"]["nodes"] == len(payload["nodes"]) > 500
    assert payload["stats"]["edges"] == len(payload["edges"]) > 1000
    html = html_path.read_text(encoding="utf-8")
    assert "vis.DataSet" in html and "ad:Playbook" in html or "vis-network" in html
    # 节点 id 与边端点一致性（导出时已过滤悬空边）
    ids = {n["id"] for n in payload["nodes"]}
    assert all(e["source"] in ids and e["target"] in ids for e in payload["edges"])


def test_export_cache(tmp_path, kb_root):
    p1, h1, d1 = graph_export.export(out_dir=tmp_path, use_cache=True)
    mtime = h1.stat().st_mtime_ns
    p2, h2, d2 = graph_export.export(out_dir=tmp_path, use_cache=True)
    assert h2.stat().st_mtime_ns == mtime  # 缓存命中不重建


# ---------- lint_semantic ----------

def test_collect_findings_shape(kb_root):
    f = lint_semantic.collect_findings(kb_root)
    assert f["graph"]["nodes"] > 500
    assert f["qa_total"] > 200
    assert isinstance(f["orphan_nodes"], list)
    assert isinstance(f["missing_card_files"], list)
    assert f["conflicts"]["total_rows"] > 0


def test_render_report_contains_sections(kb_root):
    report = lint_semantic.render_report(lint_semantic.collect_findings(kb_root))
    for section in ["孤儿图谱节点", "KnowledgeAsset", "QA 集群分布"]:
        assert section in report


# ---------- audit_runner 解析 ----------

def test_parse_validate_pass():
    out = "s22: 115 nodes\nPASS: 0 errors, 0 warnings\n"
    r = audit_runner.parse_validate(out)
    assert r["status"] == "PASS" and r["errors"] == 0 and r["warnings"] == 0


def test_parse_validate_fail_with_errors():
    out = "ERROR: x:edge[1] bad\nERROR: y:edge[2] bad2\nFAIL: 2 errors, 1 warnings\n"
    r = audit_runner.parse_validate(out)
    assert r["status"] == "FAIL" and r["errors"] == 2
    assert len(r["error_lines"]) == 2


def test_parse_audit_line():
    out = "audit: 56 cards, 283 QA entries, 520 links → FAIL 0 / WARN 0 / INFO 4\n"
    r = audit_runner.parse_audit(out)
    assert r["fail"] == 0 and r["warn"] == 0 and r["info"] == 4


def test_run_all_ok(kb_root):
    """真实仓库当前应全绿（CI 同口径）。"""
    result = audit_runner.run_all(strict=False)
    assert result["ok"], json.dumps(result, ensure_ascii=False)[:500]
