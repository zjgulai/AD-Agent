"""kb.py 检索回归测试：加载统计/命中/排序/边界。"""

import pytest

from kb_bot.kb import KnowledgeBase, MIN_SCORE


@pytest.fixture(scope="module")
def kb(kb_root):
    return KnowledgeBase(kb_root)


def test_load_counts(kb):
    kinds = kb.stats
    assert "qa" in kinds and "card" in kinds and "glossary" in kinds
    # 25 卡 + 7 qa 文件 + glossary ≈ 490 chunks（P4 后）
    assert len(kb.chunks) > 400
    from collections import Counter
    counts = Counter(c.kind for c in kb.chunks)
    assert counts["qa"] > 100 and counts["card"] > 200 and counts["glossary"] > 50


def test_retrieve_eq_question(kb):
    hits = kb.retrieve("EQ 阈值是多少", top_k=5)
    assert hits
    assert hits[0][1] >= MIN_SCORE
    assert hits[0][0].source  # 溯源标签非空


def test_retrieve_platform_ops(kb):
    hits = kb.retrieve("TikTok Shop GMV Max 是什么", top_k=5)
    assert hits
    assert any("platform-ops" in c.source for c, _ in hits[:3])


def test_retrieve_gibberish_empty_or_low(kb):
    hits = kb.retrieve("xyzzy qqq zzz 完全无关", top_k=5)
    # 允许零命中或全部低于阈值分——但绝不能有高分误命中
    assert all(s < 15 for _, s in hits)


def test_chunk_kinds(kb):
    kinds = {c.kind for c in kb.chunks}
    assert {"qa", "card", "glossary"} <= kinds


def test_top_k_respected(kb):
    hits = kb.retrieve("广告", top_k=3)
    assert len(hits) <= 3
