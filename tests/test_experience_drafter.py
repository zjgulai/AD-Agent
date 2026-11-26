"""experience_drafter 信号分类与幂等扫描回归测试。"""

import json
from types import SimpleNamespace

import pytest

import experience_drafter as ed


def _rec(**kw):
    base = {
        "ts": "2026-11-26T10:00:00", "mid": "om_x", "chat_type": "p2p",
        "question": "测试问题", "hits": [{"kind": "qa", "source": "s", "score": 12.0}],
        "graph_entities": [], "answer": "正常回答。", "status": "ok",
        "_log": "/tmp/x.jsonl",
    }
    base.update(kw)
    return base


def test_norm_question():
    assert ed._norm_question("EQ<4 会触发什么？") == ed._norm_question("eq 4 会触发什么")


def test_classify_no_hit():
    sig = ed._classify(_rec(hits=[], answer="知识库暂无可靠资料"))
    assert "no-hit" in sig and "boundary-answer" in sig


def test_classify_low_score():
    sig = ed._classify(_rec(hits=[{"kind": "g", "source": "s", "score": 7.0}]))
    assert "low-score" in sig and "no-hit" not in sig


def test_classify_error():
    sig = ed._classify(_rec(status="error: timeout", answer=None))
    assert "error" in sig


def test_classify_clean():
    assert ed._classify(_rec()) == {}


def test_aggregate_repeat(tmp_path, monkeypatch):
    monkeypatch.setattr(ed, "GRAPH_DIR", tmp_path / "no-graph")
    recs = [
        _rec(mid="a", ts="2026-11-26T10:00:00"),
        _rec(mid="b", ts="2026-11-26T11:00:00"),
        _rec(mid="c", ts="2026-11-27T10:00:00"),
    ]
    # repeat 问题需要 hits 低分才有信号——用 no-hit 版本
    for r in recs:
        r["hits"] = []
        r["answer"] = "暂无资料"
    buckets = ed._aggregate(recs, None)
    assert len(buckets) == 1
    b = next(iter(buckets.values()))
    assert len(b["occurrences"]) == 3
    assert b["signals"]["repeat"] == "high"


@pytest.fixture
def exp_env(tmp_path, monkeypatch):
    logs = tmp_path / "logs"
    exp = tmp_path / "experience"
    logs.mkdir()
    exp.mkdir()
    monkeypatch.setattr(ed, "EXP_DIR", exp)
    monkeypatch.setattr(ed, "GRAPH_DIR", tmp_path / "no-graph")
    return logs, exp


def _write_log(logs, records, name="qa-2026-11-26.jsonl"):
    with (logs / name).open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def test_scan_idempotent_and_freeze(exp_env):
    logs, exp = exp_env
    _write_log(logs, [_rec(hits=[], answer="暂无资料", question="Q1 缺口")])
    args = SimpleNamespace(logs_dir=str(logs), dry_run=False)
    assert ed.cmd_scan(args) == 0
    cards = list(exp.glob("EXP-*.md"))
    assert len(cards) == 1
    # 重跑：更新而非新建
    assert ed.cmd_scan(args) == 0
    assert len(list(exp.glob("EXP-*.md"))) == 1
    # approved 后冻结
    eid = cards[0].stem
    assert ed.cmd_set_status(SimpleNamespace(
        exp_id=eid, status="approved", verdict="approved",
        reviewer="t", action="done")) == 0
    _write_log(logs, [_rec(hits=[], answer="暂无资料", question="Q1 缺口"),
                      _rec(hits=[], answer="暂无资料", question="Q2 新缺口", mid="om_y")])
    assert ed.cmd_scan(args) == 0
    cards = list(exp.glob("EXP-*.md"))
    assert len(cards) == 2
    approved = (exp / f"{eid}.md").read_text()
    assert "status: approved" in approved
    assert "occurrences: 1" in approved  # 冻结：未吸收新出现


def test_scan_skips_clean_questions(exp_env):
    logs, exp = exp_env
    _write_log(logs, [_rec(question="正常问题")])
    assert ed.cmd_scan(SimpleNamespace(logs_dir=str(logs), dry_run=False)) == 0
    assert list(exp.glob("EXP-*.md")) == []


def test_scan_user_feedback_signal(exp_env):
    """fb-*.jsonl 的 ref_mid 关联 qa mid → user-feedback 信号（critical）。"""
    logs, exp = exp_env
    qa = _rec(question="有争议的问题", mid="om_q9", hits=[], answer="暂无资料")
    _write_log(logs, [qa])
    with (logs / "fb-2026-11-26.jsonl").open("w", encoding="utf-8") as f:
        f.write(json.dumps({
            "ts": "2026-11-26T11:00:00", "mid": "fb1", "chat_type": "card",
            "ref_mid": "om_q9", "verdict": "down", "comment": "",
            "channel": "card",
        }, ensure_ascii=False) + "\n")
        f.write(json.dumps({
            "ts": "2026-11-26T11:01:00", "mid": "fb2", "chat_type": "p2p",
            "ref_mid": "om_missing", "verdict": "down", "comment": "",
            "channel": "reply",
        }, ensure_ascii=False) + "\n")
    assert ed.cmd_scan(SimpleNamespace(logs_dir=str(logs), dry_run=False)) == 0
    cards = list(exp.glob("EXP-*.md"))
    assert len(cards) == 1
    text = cards[0].read_text(encoding="utf-8")
    assert "signal: user-feedback" in text
    assert "priority: critical" in text
    assert "## 用户反馈" in text
