---
title: 经验卡池（自进化飞轮）
doc_type: knowledge
module: ad-agent-qa
topic: experience-pool
status: review
created: 2026-11-26
updated: 2026-11-26
owner: self
source: human+ai
---

# 经验卡池 — 自进化飞轮

> 知识系统的价值 ≈ 修复率 × 代谢率。本目录是 bot/Agent 使用沉淀的**经验入口**：
> 日志信号 → 草稿卡 → 人审 → 晋升为正式知识修订（qa/卡片/图谱边/CONFLICTS）。

## 闭环

```
src/kb_bot/logs/qa-*.jsonl          # 燃料：每次问答的 question/hits/graph_entities/answer/status
        │
        ▼  python -m experience_drafter scan        （src/ 下运行，幂等）
experience/EXP-*.md                 # 草稿卡：启发式信号聚合，status: draft
        │
        ▼  人审（改 frontmatter 或 set-status）
   approved → 执行修订 → promoted   # 修订落地：qa 新条/卡片修订/图谱边/conflicts 裁决
   rejected / archived              # 证伪或无需修，留档作负样本
```

## 信号分类（v1 启发式）

| signal | 含义 | suggestion_kind | 默认优先级 |
|--------|------|-----------------|-----------|
| `no-hit` | 检索零命中 | qa-gap | high |
| `low-score` | 命中但最高分 < 9 | retrieval-tuning | medium |
| `repeat` | 同一问题 ≥2 次（归一化去重） | qa-gap | 2 次 medium / ≥3 次 high |
| `boundary-answer` | 回答含「暂无资料」类边界声明 | coverage-review | medium |
| `conflict-touch` | 命中实体存在 conflicts_with 边 | graph-review | low |
| `error` | 应答异常（LLM 超时等） | system-issue | low |

无信号的正常问答**不进池**——经验卡只记录「暴露了什么问题」，不是流水账。

## 经验卡格式

每条一卡一个文件 `EXP-YYYYMMDD-NNN.md`，frontmatter 承载生命周期：

- `status`：`draft → approved → promoted`；旁路 `rejected` / `archived`
- `signal` / `signals`：主信号 + 全部命中信号
- `occurrences`：同一问题的出现次数（归一化 question 为聚合键）
- `hits` / `graph_entities`：最新一次的检索命中与图谱实体
- `review.verdict`：`pending → approved / rejected / needs-info`
- `review.action`：promoted 时回填实际修订位置（文件/commit/边 id）

## 人审 SOP

```bash
cd src
python -m experience_drafter scan --dry-run   # 预览将生成/更新的卡
python -m experience_drafter scan             # 实际生成
python -m experience_drafter list             # 状态统计
python -m experience_drafter set-status EXP-20261126-001 approved \
    --verdict approved --reviewer <name> --action "<修订落点>"
```

1. **draft**：机器生成，内容含原始会话摘录 + 信号分析 + 建议方向
2. **approved**：人确认值得修（卡片已冻结，scan 不再覆盖）
3. **promoted**：修订已落地（改 qa//cards//graph instances/CONFLICTS.md），action 回填 commit 或文件路径
4. **rejected**：证伪或判定无需修——留档防止重复提同一问题

## 晋升去向

| 经验类型 | 落点 |
|----------|------|
| 高频问法无 qa 条目 | `qa/<cluster>.md` 新增原子问答 |
| 卡片内容缺/错 | `cards/` 对应卡修订（走 REVIEW.md 流程） |
| 图谱缺边/缺实体/边过期 | `graph/instances/` 修订 + `validate.py` 校验 |
| 口径冲突新发现 | `CONFLICTS.md` 登记，能裁自裁、业务口径进 pending_business |
| 检索质量问题（非知识缺口） | `src/kb_bot/kb.py` 打分/切片调参 |
| 系统异常 | bot 日志/LLM 配置排查，不进知识层 |

## 边界与隐私

- 草稿卡含用户原始问题文本——仓库为私有，**promoted 修订不得照搬敏感原文**
- 日志本体在 `.gitignore`（`logs/`），经验卡是其蒸馏产物，可提交
- 图谱边生命周期字段（`status/confidence/freshness/last_verified`）已在 schema 就位；经验卡证伪的边走 `status` 降权而非删除，保持可追溯
- 多消费者兼容：信号格式不绑定 bot——SCN-011 Agent 将来可 emit 同构 `{question, hits, graph_entities, answer, status}` 记录进同一池
