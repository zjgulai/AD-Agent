"""kb_ops.web FastAPI 工作台测试：TestClient 全端点冒烟。"""

import pytest
from fastapi.testclient import TestClient

from kb_ops.web.app import create_app


@pytest.fixture(scope="module")
def client(kb_root):
    return TestClient(create_app(kb_root))


def test_index_html(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "KB Workbench" in r.text


def test_static_assets(client):
    for asset in ("/app.js", "/style.css", "/marked.min.js"):
        r = client.get(asset)
        assert r.status_code == 200, asset
    # vis-network vendor 走同一静态挂载
    r = client.get("/vendor/vis-network.min.js")
    assert r.status_code == 200


def test_stats(client):
    r = client.get("/api/stats")
    assert r.status_code == 200
    s = r.json()
    for key in ("cards", "qa_entries", "graph_nodes", "graph_edges"):
        assert s[key] > 0, key


def test_cards_list(client):
    r = client.get("/api/cards")
    assert r.status_code == 200
    cards = r.json()["cards"]
    assert len(cards) > 30
    assert all({"cluster", "name", "title", "path"} <= set(c) for c in cards)


def test_cards_cluster_filter(client):
    r = client.get("/api/cards", params={"cluster": "platform-ops"})
    cards = r.json()["cards"]
    assert cards and all(c["cluster"] == "platform-ops" for c in cards)


def test_card_detail(client, kb_root):
    # 取一个真实存在的卡
    cards = client.get("/api/cards").json()["cards"]
    c = cards[0]
    r = client.get(f"/api/cards/{c['cluster']}/{c['name']}")
    assert r.status_code == 200
    d = r.json()
    assert d["body"] and d["cluster"] == c["cluster"]


def test_card_404_and_traversal(client):
    assert client.get("/api/cards/nope/nope").status_code == 404
    assert client.get("/api/cards/..%2F..%2Fetc/passwd").status_code in (404, 422)


def test_qa_list_and_detail(client):
    files = client.get("/api/qa").json()["files"]
    assert len(files) >= 7
    f = files[0]
    assert f["count"] > 0
    d = client.get(f"/api/qa/{f['cluster']}").json()
    assert len(d["entries"]) == f["count"]
    e = d["entries"][0]
    assert e["qid"].startswith("Q") and e["question"] and e["answer"]


def test_qa_404(client):
    assert client.get("/api/qa/nonexistent").status_code == 404


def test_graph(client):
    r = client.get("/api/graph")
    assert r.status_code == 200
    g = r.json()
    assert g["stats"]["nodes"] > 500
    assert g["stats"]["edges"] > 500
    assert g["nodes"] and g["edges"]
    n = g["nodes"][0]
    assert {"id", "label", "type", "cluster", "community", "degree", "props"} <= set(n)


def test_search(client):
    r = client.get("/api/search", params={"q": "ROAS 归因", "k": 5})
    assert r.status_code == 200
    results = r.json()["results"]
    assert results, "BM25 应有命中"
    assert all({"source", "kind", "score", "text"} <= set(x) for x in results)
    assert results[0]["score"] > 0


def test_search_empty_query(client):
    assert client.get("/api/search", params={"q": ""}).status_code == 422


def test_health(client):
    r = client.get("/api/health")
    assert r.status_code == 200
    h = r.json()
    assert "audit" in h and "lint" not in h  # lint 字段平铺
    assert h["audit"]["validate"]["status"] in ("PASS", "FAIL", "UNKNOWN")
    assert "qa_counts" in h and "conflict_table" in h
    assert "rows" in h["conflict_table"] and "adjudication" in h["conflict_table"]


def test_doc(client):
    r = client.get("/api/doc/INDEX.md")
    assert r.status_code == 200
    assert "markdown" in r.json()
    assert client.get("/api/doc/../../etc/passwd").status_code == 404
    assert client.get("/api/doc/NOPE.md").status_code == 404
