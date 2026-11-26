---
title: 对话层 Q&A 数据集说明
doc_type: knowledge
module: ad-agent-qa
topic: qa-dataset
status: review
created: 2026-11-26
updated: 2026-11-26
owner: self
source: human+ai
---

# Q&A 数据集（对话层）

本目录是知识库的**对话消费层**：把 `cards/` 中的主题卡片蒸馏为自包含的原子 Q→A 对，供 LLM/Agent 直接检索引用。

## 与 cards/ 的关系

- `cards/`：主题长文，完整知识脉络，人读+深读用
- `qa/`：原子问答，答案不依赖卡片上下文即可独立成立，对话/RAG 用
- 每条 Q→A 标注 `source_card` 溯源；内容与卡片冲突时以卡片+CONFLICTS.md 为准

## 文件组织

按知识库集群分文件，与 `cards/` 一一对应：

| QA 文件 | 覆盖卡片集群 | 题量 |
|---------|--------------|------|
| `architecture.md` | architecture/（4 卡） | ~20 |
| `influencer-boost.md` | influencer-boost/（3 卡） | ~20 |
| `meta-ads-diagnosis.md` | meta-ads-diagnosis/（8 卡） | ~30 |
| `fundamentals.md` | fundamentals/（3 卡） | ~20 |
| `business-context.md` | business-context/（4 卡） | ~25 |
| `competitor-analysis.md` | competitor-analysis/（1 卡） | ~6 |

## 条目格式

```markdown
### Qn. <自然语言问题>
**A**：<自包含答案，2-6 句>
> 溯源：`cards/<cluster>/<card>.md` §<章节>；冲突时见 `CONFLICTS.md` #<n>
```

## 冲突处理规则

源文档存在多套口径（EQ 阈值、L4 数据门槛、素材疲劳定义、频次阈值等，详见 `CONFLICTS.md`）。QA 条目遇冲突时：

1. 答案中**并列呈现各口径**，不静默选边
2. 标注各口径出自哪份源文档（S4/S6/S7/S8）
3. 执行级判定建议以 S4 节点 IF 条件为准（卡片共识 `[推断]`），但须注明这是推断

## 边界声明

以下领域知识库**无可靠来源**，对话层应如实回答「暂无资料」而非编造：红人 BD/建联流程、素材拍摄制作方法论、Google/TikTok 平台级 Momcozy 投放 playbook、系统预算规划、团队组织、合规申诉细节、多语言本地化、物流履约、价格促销机制。详见 `COVERAGE.md` §七。

## 状态

`status: review`——与卡片同步验收，验收通过后转 stable。
