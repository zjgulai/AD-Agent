---
title: KB 对话层查询路由规范
doc_type: knowledge
module: ad-agent-qa
topic: query-routing
status: review
created: 2026-11-26
updated: 2026-11-26
owner: self
source: human+ai
---

# QUERY.md — 对话层查询路由规范

本文档是任何 agent/LLM 消费本知识库的**查询协议**。遵循本规范即可对话式使用 KB，无需向量库。

## 1. 检索顺序（三级路由）

```
用户问题
  → L1 关键词/意图匹配 qa/*.md 条目标题（自包含答案，优先）
  → L2 未命中或需深读 → 按下表路由到 cards/ 主题卡片
  → L3 术语不懂 → glossary.md；源文档冲突 → CONFLICTS.md
```

**L1 优先原则**：`qa/` 条目答案自包含，命中即答，不必再读卡片。仅当问题需要完整脉络/表格/清单时才下钻 L2。

## 2. 问题类型 → 资源路由表

| 问题类型 | 关键词信号 | 首选资源 | 备选 |
|----------|-----------|----------|------|
| 系统全景/架构 | Loop、Agent 几类、体系、蓝图 | `qa/architecture.md` Q1-Q8 | `cards/architecture/ad-agent-system-landscape.md` |
| Agent 产品/排期/防呆 | 监控 Agent、PRD、上线、告警、防呆、LLM | `qa/architecture.md` Q9-Q15 | `monitoring-optimization-agent-prd.md` |
| 业务调研方法 | 调研、33列矩阵、MP/非MP、四象限 | `qa/architecture.md` Q16-Q18 | `ad-ops-agent-research-framework.md` |
| 红人加推全流程 | 红人、加推、授权、Spark Ads、KOL | `qa/influencer-boost.md` | 3 张 influencer-boost 卡 |
| 红人建设进度 | 任务、进度、人天、FDE、YouTube | `qa/influencer-boost.md` Q19-Q21 | `influencer-boost-build-tracking.md` |
| 诊断流程/SOP | 诊断顺序、G0-G8、T0-T5、L0-L4、一天怎么过 | `qa/meta-ads-diagnosis.md` Q1-Q3,Q7,Q25 | 4 张 SOP/流程卡 |
| 诊断阈值/指标 | EQ、归因差异、样本门槛、CTR/CPC/CPM、频次、疲劳 | `qa/meta-ads-diagnosis.md` Q4-Q6,Q11,Q20-Q23 | `meta-diagnosis-metrics.md` + `CONFLICTS.md` |
| 动作/处置 | 动作库、A-xx、扩量、止血、回滚、验证窗口 | `qa/meta-ads-diagnosis.md` Q13-Q19 | `meta-action-library.md` |
| 投后数据/巡检 | 巡检、投后、字段、漏斗口径、命名 | `qa/meta-ads-diagnosis.md` Q27 | `meta-post-launch-data-inspection.md` |
| 平台机制 | CBO/ABO、智能出价、eCPM、GSP、Pacing、SKAN、ATT | `qa/fundamentals.md` Q1-Q17 | 2 张 fundamentals 卡 |
| 生命周期策略 | 新品、预热、首销、增长、大促、衰退、Incrementality | `qa/fundamentals.md` Q18-Q23 | `product-lifecycle-ad-strategy.md` |
| Momcozy 人群/渠道 | 人群画像、孕哺育、T0-T3出价、DTC/Amazon、复购 | `qa/business-context.md` Q1-Q5 | `momcozy-audience-persona.md` |
| 分层投放/链路 | 清洗机、浅中深、受众分层、孕期链路、素材匹配 | `qa/business-context.md` Q6-Q8 | `audience-layering-playbook.md` |
| MP/项目方法 | MP 文档、Brief、复盘、AB Test、Preflight、看数顺序 | `qa/business-context.md` Q9-Q12 | `mp-project-methodology.md` |
| 触点/全链路 | 触点、生命周期7阶段、独立站、Amazon 分工、冷启动 | `qa/business-context.md` Q13-Q15 | `customer-touchpoint-map.md` |
| 竞品 | Navos、GrowthGPT、Zalify、竞品对比 | `qa/competitor-analysis.md` | `ad-agent-competitor-landscape.md` |
| 术语解释 | 任意缩写/黑话 | `glossary.md` | — |
| 知识边界 | 红人BD、素材制作、平台playbook、预算规划、合规等 | `qa/COVERAGE.md` §七 | 如实答「暂无资料」 |

## 3. 冲突处理规则（硬性）

源文档存在多套口径（`CONFLICTS.md` 登记 17 项）。对话层**必须**：

1. **并列呈现**各口径+出处，不静默选边。例：EQ 阈值答「S6 排雷用 EQ<6，S7/S4 用 EQ<4，源文档内部矛盾 `[待确认]`」
2. qa/ 条目已内建并列答案的直接引用；未内建的查 `CONFLICTS.md` 补充
3. 执行级判定建议可注明「以 S4 节点 IF 条件为准 `[推断]`」——必须带 `[推断]` 标记，不得伪装成源文档结论
4. `[待确认]`/`[推断]` 标记在转述时保留，不得省略

## 4. 引用规范

回答结尾附溯源行，格式：

```
> 来源：qa/meta-ads-diagnosis.md Q5 ← cards/meta-ads-diagnosis/meta-diagnosis-sop.md
```

- 优先引 qa/ 条目（自包含），深读需求引 cards/ 卡片
- 涉及冲突时加注 `CONFLICTS.md #<编号>`
- 飞书场景受长度限制时可省略来源行，但系统提示词要求模型保留 `[待确认]`/`[推断]` 标记

## 5. 知识边界声明（必须遵守）

以下领域**无可靠来源**，用户提问时必须如实回答「知识库暂无资料」并建议补充源文档，**禁止编造**：

- 红人 BD/建联/谈判流程（库内只有授权环节）
- 素材拍摄/创意制作方法论
- Google 平台级 Momcozy 投放 playbook（TikTok Shop/Amazon 已由 platform-ops 蒸馏卡覆盖，Google 仍只有机制层）
- 系统性预算规划方法（只有阶段预算心态）
- 团队组织/编制、合规申诉细节、多语言本地化、物流履约、价格促销机制
- Zalify 竞品能力（源文档无权限）

完整缺口清单见 `qa/COVERAGE.md` §七。

## 6. 使用方式

- **人/Agent 直接用**：读本文档 → 按 §2 路由 → 读 qa/ 条目作答 → 按 §4 附引用；结构化关系问题（阈值口径、实体冲突、多跳线索）可用 `src/graph_query/` 包查图谱（契约见 `graph/README.md`）
- **机器人用**：`src/kb_bot/` 实现本规范的自动化版（检索→图谱实体链接注入→LLM 生成→附引用）
