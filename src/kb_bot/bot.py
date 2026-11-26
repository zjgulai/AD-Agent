"""飞书机器人入口：lark-oapi WebSocket 长连接 + KB 检索 + LLM 应答。

用法：
  python -m kb_bot.bot                      # 启动 WebSocket 长连接（需全部环境变量）
  python -m kb_bot.bot --selftest           # KB 加载自检（无需凭证）
  python -m kb_bot.bot --retrieve "问题"     # 只看检索结果（无需凭证）
  python -m kb_bot.bot --ask "问题"          # 完整问答（需 LLM_* 环境变量）
"""

from __future__ import annotations

import asyncio
import datetime
import json
import os
import re
import sys
import threading
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import lark_oapi as lark
from lark_oapi.api.im.v1 import P2ImMessageReceiveV1
from lark_oapi.event.callback.model.p2_card_action_trigger import (
    CallBackToast,
    P2CardActionTriggerResponse,
)

from .config import DEFAULT_KB_ROOT, Settings, load_settings
from .kb import Chunk, KnowledgeBase
from .llm import chat as llm_chat

try:
    from graph_query import GraphIndex
except ImportError:  # 兼容从 src/kb_bot 直接运行的场景
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from graph_query import GraphIndex

_seen_messages: OrderedDict[str, None] = OrderedDict()
_seen_max = 1000

_LOG_DIR = Path(__file__).resolve().parent / "logs"
_log_lock = threading.Lock()


def _log_qa(record: dict) -> None:
    """问答日志：每条一行 JSONL，按天分文件。失败只打 stderr 不影响应答。"""
    _append_log("qa", record)


_answer_mid_to_qmid: OrderedDict[str, str] = OrderedDict()

_DOWN_MARKS = ("不对", "错", "有误", "👎", "❌", "错误")
_UP_MARKS = ("👍", "有用", "正确", "✅", "好评", "不错")


def _classify_feedback(text: str) -> tuple[str, str]:
    """把回复文本判成 (verdict, comment)。down 优先于 up（"不对"含"对"）。"""
    t = text.strip()
    if any(m in t for m in _DOWN_MARKS):
        return "down", t
    if any(m in t for m in _UP_MARKS):
        return "up", ""
    return "comment", t


def _handle_feedback(client: lark.Client, msg, text: str) -> bool:
    """parent_id 命中已回答消息 → 记为反馈而非新问题。返回是否已处理。"""
    parent = getattr(msg, "parent_id", "") or ""
    qmid = _answer_mid_to_qmid.get(parent)
    if not qmid:
        return False
    verdict, comment = _classify_feedback(text)
    _log_fb({
        "ts": datetime.datetime.now().isoformat(timespec="seconds"),
        "mid": getattr(msg, "message_id", ""),
        "chat_type": getattr(msg, "chat_type", ""),
        "ref_mid": qmid,
        "verdict": verdict,
        "comment": comment[:500],
        "channel": "reply",
    })
    _reply(client, msg.message_id, text="已记录反馈，感谢！")
    print(f"[feedback] {verdict} ref={qmid} comment={comment[:60]!r}", file=sys.stderr)
    return True


def _log_fb(record: dict) -> None:
    """用户反馈日志：fb-YYYY-MM-DD.jsonl，ref_mid 关联 qa 日志的 mid。"""
    _append_log("fb", record)


def _append_log(prefix: str, record: dict) -> None:
    try:
        _LOG_DIR.mkdir(parents=True, exist_ok=True)
        day = datetime.date.today().isoformat()
        with _log_lock, (_LOG_DIR / f"{prefix}-{day}.jsonl").open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception as exc:
        print(f"[log failed] {exc}", file=sys.stderr)


def _extract_text(message_type: str, content: str) -> str | None:
    try:
        body = json.loads(content)
    except json.JSONDecodeError:
        return None
    if message_type == "text":
        return body.get("text", "").strip() or None
    if message_type == "post":
        parts: list[str] = []

        def walk(node):
            if isinstance(node, dict):
                if node.get("tag") == "text" and node.get("text"):
                    parts.append(node["text"])
                for v in node.values():
                    walk(v)
            elif isinstance(node, list):
                for v in node:
                    walk(v)

        walk(body.get("content", []))
        title = body.get("title")
        return ((title + "\n" if title else "") + "".join(parts)).strip() or None
    return None


def _already_seen(message_id: str) -> bool:
    if message_id in _seen_messages:
        return True
    _seen_messages[message_id] = None
    if len(_seen_messages) > _seen_max:
        _seen_messages.popitem(last=False)
    return False


def _should_answer(event_message, bot_open_id: str) -> bool:
    if event_message.chat_type == "p2p":
        return True
    mentions = getattr(event_message, "mentions", None) or []
    if bot_open_id:
        return any(
            getattr(getattr(m, "id", None), "open_id", "") == bot_open_id
            for m in mentions
        )
    bot_name = os.environ.get("BOT_NAME", "").strip()
    if not bot_name:
        return bool(mentions)
    return any(getattr(m, "name", "") == bot_name for m in mentions)


def fetch_bot_open_id(settings: Settings) -> str:
    """启动时取机器人 open_id，用于群聊 @ 精确判定。失败返回空串走降级逻辑。"""
    import httpx

    try:
        tok = httpx.post(
            "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
            json={
                "app_id": settings.lark_app_id,
                "app_secret": settings.lark_app_secret,
            },
            timeout=15,
        ).json()["tenant_access_token"]
        info = httpx.get(
            "https://open.feishu.cn/open-apis/bot/v3/info",
            headers={"Authorization": f"Bearer {tok}"},
            timeout=15,
        ).json()
        return info.get("bot", {}).get("open_id", "")
    except Exception as exc:
        print(f"[bot info fetch failed] {exc}", file=sys.stderr)
        return ""


_MD_PATTERNS = [
    (re.compile(r"\*\*(.+?)\*\*"), r"\1"),
    (re.compile(r"`([^`\n]+)`"), r"\1"),
    (re.compile(r"^#{1,6}\s*", re.M), ""),
    (re.compile(r"^>\s?", re.M), ""),
    (re.compile(r"^\s*[-*•]\s+", re.M), "· "),
]


def _strip_markdown(text: str) -> str:
    for pat, repl in _MD_PATTERNS:
        text = pat.sub(repl, text)
    return text


def _split_sources(answer: str) -> tuple[str, str]:
    """把末尾「来源：」行拆出，正文与来源分开渲染。"""
    lines = answer.split("\n")
    src = [l.strip() for l in lines if l.strip().startswith("来源：")]
    body = "\n".join(l for l in lines if not l.strip().startswith("来源：")).strip()
    return body, "\n".join(src)


def _build_card(answer: str, qmid: str = "") -> str:
    body, sources = _split_sources(_strip_markdown(answer))
    elements: list[dict] = [
        {"tag": "div", "text": {"tag": "plain_text", "content": body or "（无内容）"}}
    ]
    if sources:
        elements += [
            {"tag": "hr"},
            {"tag": "note", "elements": [{"tag": "plain_text", "content": sources}]},
        ]
    if qmid:
        elements += [
            {"tag": "hr"},
            {
                "tag": "action",
                "actions": [
                    {
                        "tag": "button",
                        "text": {"tag": "plain_text", "content": label},
                        "type": btype,
                        "value": {"fb": verdict, "qmid": qmid},
                    }
                    for label, btype, verdict in [
                        ("👍 有用", "default", "up"),
                        ("👎 不对", "danger", "down"),
                        ("📝 补充", "default", "comment"),
                    ]
                ],
            },
        ]
    card = {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {"tag": "plain_text", "content": "广告知识库问答"},
            "template": "blue",
        },
        "elements": elements,
    }
    return json.dumps(card, ensure_ascii=False)


def _reply(client: lark.Client, message_id: str, text: str | None = None, card: str | None = None) -> str:
    """回复消息，返回新消息的 message_id（失败返回空串）。"""
    if card is not None:
        msg_type, content = "interactive", card
    else:
        msg_type, content = "text", json.dumps({"text": text or ""}, ensure_ascii=False)
    req = (
        lark.im.v1.ReplyMessageRequest.builder()
        .message_id(message_id)
        .request_body(
            lark.im.v1.ReplyMessageRequestBody.builder()
            .msg_type(msg_type)
            .content(content)
            .build()
        )
        .build()
    )
    resp = client.im.v1.message.reply(req)
    if not resp.success():
        print(f"[reply failed] code={resp.code} msg={resp.msg}", file=sys.stderr)
        return ""
    return getattr(getattr(resp, "data", None), "message_id", "") or ""


_GRAPH: GraphIndex | None = None
_GRAPH_FAILED = False


def _get_graph(kb: KnowledgeBase) -> GraphIndex | None:
    """惰性加载图谱；目录缺失或加载异常时返回 None（降级为纯检索）。"""
    global _GRAPH, _GRAPH_FAILED
    if _GRAPH is not None or _GRAPH_FAILED:
        return _GRAPH
    graph_dir = kb.kb_root / "graph"
    try:
        g = GraphIndex(graph_dir)
        if g.nodes:
            _GRAPH = g
            print(f"graph loaded: {g.stats()}", file=sys.stderr)
        else:
            _GRAPH_FAILED = True
    except Exception as exc:
        _GRAPH_FAILED = True
        print(f"[graph load failed] {exc}", file=sys.stderr)
    return _GRAPH


def _graph_entities(graph: GraphIndex, question: str) -> list[str]:
    return [h.label for h in graph.resolve(question, limit=3)]


def _augment_hits(kb: KnowledgeBase, hits: list, question: str) -> tuple[list, list[str]]:
    """把图谱上下文作为一条合成 chunk 追加到检索结果末尾。"""
    graph = _get_graph(kb)
    if graph is None:
        return hits, []
    entities = _graph_entities(graph, question)
    ctx = graph.context_for(question)
    if not ctx:
        return hits, entities
    return hits + [(Chunk(text=ctx, source="graph:ad-ops", kind="graph"), 0.0)], entities


async def _answer(kb: KnowledgeBase, settings: Settings, question: str) -> str:
    hits = kb.retrieve(question, top_k=settings.retrieve_top_k)
    hits, _ = _augment_hits(kb, hits, question)
    if not hits:
        return "知识库暂无相关资料。可换个问法，或参考 qa/COVERAGE.md 的边界声明。"
    return await llm_chat(settings, question, hits)


_executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix="kb-answer")


def _handle_question(
    client: lark.Client,
    kb: KnowledgeBase,
    settings: Settings,
    message_id: str,
    question: str,
    chat_type: str = "",
) -> None:
    ts = datetime.datetime.now().isoformat(timespec="seconds")
    hits = kb.retrieve(question, top_k=settings.retrieve_top_k)
    hits, graph_entities = _augment_hits(kb, hits, question)
    hit_summary = [
        {"kind": c.kind, "source": c.source, "score": round(s, 3)}
        for c, s in hits[:5]
    ]
    answer: str | None = None
    status = "ok"
    try:
        if not hits:
            answer = "知识库暂无相关资料。可换个问法，或参考 qa/COVERAGE.md 的边界声明。"
        else:
            answer = asyncio.run(llm_chat(settings, question, hits))
        answer_mid = _reply(client, message_id, card=_build_card(answer, qmid=message_id))
        if answer_mid:
            _answer_mid_to_qmid[answer_mid] = message_id
            if len(_answer_mid_to_qmid) > _seen_max:
                _answer_mid_to_qmid.popitem(last=False)
    except Exception as exc:  # 不向飞书泄露内部错误细节
        status = f"error: {exc}"
        print(f"[answer error] {exc}", file=sys.stderr)
        _reply(client, message_id, text="内部错误，稍后重试。")
    _log_qa(
        {
            "ts": ts,
            "mid": message_id,
            "chat_type": chat_type,
            "question": question,
            "hits": hit_summary,
            "graph_entities": graph_entities,
            "answer": answer,
            "status": status,
        }
    )


def on_card_action(data) -> P2CardActionTriggerResponse:
    """卡片反馈按钮回调（需飞书后台订阅 card.action.trigger 事件）。"""
    ev = data.event
    val = (ev.action.value or {}) if ev.action else {}
    verdict = val.get("fb")
    qmid = str(val.get("qmid") or "")
    if verdict in {"up", "down", "comment"} and qmid:
        _log_fb({
            "ts": datetime.datetime.now().isoformat(timespec="seconds"),
            "mid": getattr(ev, "token", "") or "",
            "chat_type": "card",
            "ref_mid": qmid,
            "verdict": verdict,
            "comment": "",
            "channel": "card",
            "operator": getattr(getattr(ev, "operator", None), "open_id", ""),
        })
        print(f"[card feedback] {verdict} ref={qmid}", file=sys.stderr)
    resp = P2CardActionTriggerResponse()
    toast = CallBackToast()
    toast.type = "success" if verdict == "up" else "info"
    toast.content = "已记录反馈，感谢！"
    resp.toast = toast
    return resp


def make_handler(client: lark.Client, kb: KnowledgeBase, settings: Settings, bot_open_id: str):
    def on_message(data: P2ImMessageReceiveV1) -> None:
        event = data.event
        msg = event.message
        sender = getattr(event, "sender", None)
        mentions = getattr(msg, "mentions", None) or []
        print(
            f"[event] chat={msg.chat_type} type={msg.message_type} "
            f"sender_type={getattr(sender, 'sender_type', '?')} "
            f"mentions={len(mentions)} mid={msg.message_id}",
            file=sys.stderr,
        )
        if getattr(sender, "sender_type", "") == "app":
            return
        if _already_seen(msg.message_id):
            return
        if not _should_answer(msg, bot_open_id):
            return
        question = _extract_text(msg.message_type, msg.content)
        if question:
            # 飞书把 @提及 编码为 @_user_N 占位符，清洗后再检索/记录
            question = re.sub(r"@_user_\d+\s*", "", question).strip()
        if not question:
            if msg.message_type not in {"text", "post"}:
                _reply(client, msg.message_id, "暂只支持文本/富文本提问。")
            return
        # 回复机器人回答 → 视为反馈而非新问题
        if _handle_feedback(client, msg, question):
            return
        # WS 回调跑在 SDK 的 event loop 里，LLM 调用必须丢到工作线程，
        # 否则 asyncio.run 会报 "cannot be called from a running event loop"
        _executor.submit(
            _handle_question, client, kb, settings, msg.message_id, question, msg.chat_type
        )

    return on_message


def main() -> None:
    argv = sys.argv[1:]

    if "--selftest" in argv:
        kb = KnowledgeBase(DEFAULT_KB_ROOT)
        print(kb.stats)
        return

    if "--retrieve" in argv:
        q = argv[argv.index("--retrieve") + 1]
        kb = KnowledgeBase(DEFAULT_KB_ROOT)
        for chunk, score in kb.retrieve(q, top_k=8):
            print(f"[{score:.2f}] {chunk.kind} {chunk.source}\n  {chunk.text[:120]}…\n")
        graph = _get_graph(kb)
        if graph is not None:
            entities = _graph_entities(graph, q)
            print(f"graph entities: {entities}")
            ctx = graph.context_for(q)
            if ctx:
                print(f"\n[graph context]\n{ctx}")
        return

    if "--ask" in argv:
        q = argv[argv.index("--ask") + 1]
        settings = load_settings(require_lark=False)
        kb = KnowledgeBase(settings.kb_root)
        answer = asyncio.run(_answer(kb, settings, q))
        print(answer)
        return

    settings = load_settings()
    kb = KnowledgeBase(settings.kb_root)
    print(f"KB loaded: {kb.stats}", file=sys.stderr)
    bot_open_id = fetch_bot_open_id(settings)
    print(f"bot open_id: {bot_open_id or '(unknown, fallback to BOT_NAME/any-mention)'}", file=sys.stderr)

    client = (
        lark.Client.builder()
        .app_id(settings.lark_app_id)
        .app_secret(settings.lark_app_secret)
        .log_level(lark.LogLevel.INFO)
        .build()
    )
    event_handler = (
        lark.EventDispatcherHandler.builder("", "")
        .register_p2_im_message_receive_v1(make_handler(client, kb, settings, bot_open_id))
        .register_p2_card_action_trigger(on_card_action)
        .build()
    )
    ws_client = lark.ws.Client(
        settings.lark_app_id,
        settings.lark_app_secret,
        event_handler=event_handler,
        log_level=lark.LogLevel.INFO,
    )
    print("WebSocket 长连接已启动，等待飞书消息…", file=sys.stderr)
    ws_client.start()


if __name__ == "__main__":
    main()
