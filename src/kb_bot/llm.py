"""OpenAI 兼容 LLM 客户端（httpx 直连，兼容 DeepSeek/通义/自建网关）。"""

from __future__ import annotations

import httpx

from .config import Settings
from .kb import Chunk

SYSTEM_PROMPT = """你是 Momcozy 广告知识库问答助手。知识库蒸馏自公司内部飞书文档（Meta 广告诊断 SOP、红人素材加推 Agent、广告 Agent 全景架构、Momcozy 业务实操、行业机制、竞品分析）。

回答规则：
1. 只依据下方「参考资料」回答。资料没有的内容如实说「知识库暂无可靠资料」，禁止编造；可建议用户补充源文档。
2. 多口径冲突时并列呈现各口径及出处（如 S4/S6/S7/S8），不静默选边；执行级建议可注明「以 S4 节点 IF 条件为准 [推断]」。
3. 保留资料中的 [待确认]/[推断] 标记，不得省略或当成确定事实。
4. 输出**纯文本**：禁止使用 markdown 语法——不用 ** 加粗、## 标题、` 代码、> 引用、- 列表符、| 表格；分层用「一、二、」或换行表达，列举用「·」或序号。
5. 中文回答，先结论后依据，默认 300 字以内；问题要求展开时可到 800 字。
6. 回答末尾单独一行注明来源，格式为「来源：<参考资料中的 source 标签>」，每条来源一行。
7. 知识边界：红人 BD/建联、素材拍摄制作方法论、Google/TikTok 平台级投放 playbook、系统预算规划、团队组织、合规申诉、多语言本地化、物流履约、价格促销机制、Zalify 竞品能力——均无可靠来源，提问时答「暂无资料」。
"""


def build_context(chunks: list[tuple[Chunk, float]]) -> str:
    parts = []
    for i, (chunk, score) in enumerate(chunks, 1):
        parts.append(f"【资料{i}｜{chunk.source}】\n{chunk.text}")
    return "\n\n".join(parts)


async def chat(settings: Settings, question: str, chunks: list[tuple[Chunk, float]]) -> str:
    context = build_context(chunks) if chunks else "（无检索结果）"
    user_msg = f"参考资料：\n\n{context}\n\n---\n\n用户问题：{question}"
    payload = {
        "model": settings.llm_model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
        "temperature": 0.2,
        "max_tokens": 1500,
    }
    async with httpx.AsyncClient(timeout=settings.llm_timeout) as client:
        resp = await client.post(
            f"{settings.llm_base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.llm_api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
        )
        resp.raise_for_status()
        data = resp.json()
    answer = data["choices"][0]["message"]["content"].strip()
    return answer[: settings.max_answer_chars]
