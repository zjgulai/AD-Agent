"""飞书机器人入口：lark-oapi WebSocket 长连接 + KB 检索 + LLM 应答。

用法：
  python -m kb_bot.bot                      # 启动 WebSocket 长连接（需全部环境变量）
  python -m kb_bot.bot --selftest           # KB 加载自检（无需凭证）
  python -m kb_bot.bot --retrieve "问题"     # 只看检索结果（无需凭证）
  python -m kb_bot.bot --ask "问题"          # 完整问答（需 LLM_* 环境变量）
"""

from __future__ import annotations

import asyncio
import json
import os
import re
import sys
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor

import lark_oapi as lark
from lark_oapi.api.im.v1 import P2ImMessageReceiveV1

from .config import DEFAULT_KB_ROOT, Settings, load_settings
from .kb import Chunk, KnowledgeBase
from .llm import chat as llm_chat

_seen_messages: OrderedDict[str, None] = OrderedDict()
_seen_max = 1000


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


def _build_card(answer: str) -> str:
    body, sources = _split_sources(_strip_markdown(answer))
    elements: list[dict] = [
        {"tag": "div", "text": {"tag": "plain_text", "content": body or "（无内容）"}}
    ]
    if sources:
        elements += [
            {"tag": "hr"},
            {"tag": "note", "elements": [{"tag": "plain_text", "content": sources}]},
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


def _reply(client: lark.Client, message_id: str, text: str | None = None, card: str | None = None) -> None:
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


async def _answer(kb: KnowledgeBase, settings: Settings, question: str) -> str:
    hits = kb.retrieve(question, top_k=settings.retrieve_top_k)
    if not hits:
        return "知识库暂无相关资料。可换个问法，或参考 qa/COVERAGE.md 的边界声明。"
    return await llm_chat(settings, question, hits)


_executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix="kb-answer")


def _handle_question(client: lark.Client, kb: KnowledgeBase, settings: Settings, message_id: str, question: str) -> None:
    try:
        answer = asyncio.run(_answer(kb, settings, question))
        _reply(client, message_id, card=_build_card(answer))
    except Exception as exc:  # 不向飞书泄露内部错误细节
        print(f"[answer error] {exc}", file=sys.stderr)
        _reply(client, message_id, text="内部错误，稍后重试。")


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
        if not question:
            if msg.message_type not in {"text", "post"}:
                _reply(client, msg.message_id, "暂只支持文本/富文本提问。")
            return
        # WS 回调跑在 SDK 的 event loop 里，LLM 调用必须丢到工作线程，
        # 否则 asyncio.run 会报 "cannot be called from a running event loop"
        _executor.submit(_handle_question, client, kb, settings, msg.message_id, question)

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
