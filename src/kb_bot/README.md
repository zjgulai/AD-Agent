---
title: KB 飞书问答机器人
doc_type: architecture
module: kb-bot
topic: feishu-qa-bot
status: review
created: 2026-11-26
updated: 2026-11-26
owner: self
source: human+ai
---

# KB 飞书问答机器人（MVP）

把 `docs/knowledge/ad-agent-qa/` 知识库通过飞书聊天机器人开放问答。

## 架构

```
飞书用户 @机器人 / 私聊
  → lark-oapi WebSocket 长连接（无需公网域名）
  → kb.py 检索（qa/ 原子问答 + cards/ 章节切片 + glossary，字符 bigram 打分）
  → QUERY.md 协议约束的 system prompt + top-k 参考资料
  → OpenAI 兼容 LLM 生成回答（含来源行）
  → message.reply 回复原消息
```

## 运行

```bash
cd src/kb_bot
uv venv .venv --python 3.12
uv pip install --python .venv/bin/python -r requirements.txt
cp .env.example .env   # 填入凭证
set -a && source .env && set +a
.venv/bin/python -m kb_bot.bot
```

## 飞书应用配置（开放平台）

1. 创建自建应用 → 拿 App ID/Secret
2. 权限开通：`im:message`、`im:message:send_as_bot`（回复）、事件订阅 `im.message.receive_v1`
3. 事件订阅方式选 **长连接**（WebSocket），不需要公网域名/加密密钥
4. 可用范围：把机器人加进目标群，或开放给指定成员私聊

## 开发自检（无需凭证）

```bash
.venv/bin/python -m kb_bot.bot --selftest            # KB 加载统计
.venv/bin/python -m kb_bot.bot --retrieve "EQ 阈值"   # 看检索命中
.venv/bin/python -m kb_bot.bot --ask "EQ 阈值"        # 需 LLM_* 环境变量
```

## 已知限制（MVP）

- 群聊按 mention `open_id` 精确匹配机器人（启动时自动获取）；获取失败时降级为 BOT_NAME/任意 @ 应答
- 检索为字符 bigram 打分，无语义向量——21 卡规模够用，语料涨到数百卡后应换 embedding
- 每条消息独立 `asyncio.run`，无会话记忆/多轮上下文
- 仅文本/富文本；图片、文件、卡片消息回复「暂不支持」
- 回答走 `msg_type=text`，无富文本卡片排版
