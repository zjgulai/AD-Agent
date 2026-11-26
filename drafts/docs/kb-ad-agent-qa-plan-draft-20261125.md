---
title: 跨境电商广告 Agent 问答知识库 — 端到端建设方案
doc_type: workflow
module: knowledge-base
topic: ad-agent-qa
status: draft
created: 2026-11-25
updated: 2026-11-25
owner: self
source: human+ai
---

# 跨境电商广告 Agent 问答知识库 — 端到端建设方案

## 1. 目标

从 ego lite 浏览器中 5 个飞书文档标签页采集原始资料，经蒸馏萃取，建成 `docs/knowledge/ad-agent-qa/` 下的问答知识库。主题：跨境电商品牌出海 · 广告类 Agent。

## 2. 已锁定决策（两轮 grilling 结论）

| # | 决策点 | 结论 |
|---|--------|------|
| Q1 | 用途/受众 | markdown 为主，人 + Agent 双消费 |
| Q2 | 范围 | 5 篇全做；电子表格走独立蒸馏路径；结构预留扩展 |
| Q3 | 颗粒度 | 主题卡片 + 高频问答索引（混合） |
| Q4 | 保真度 | 忠于原文；推断内容显式标注 `[推断]` |
| Q5 | 形态/位置 | `docs/knowledge/ad-agent-qa/` + INDEX.md + frontmatter 溯源 |
| Q6 | 节奏 | 试点先行（《广告agent梳理》）→ 门禁 → 批量 |
| Q7 | 组织原则 | 按主题跨文档聚合，卡片标注 `source_docs[]` |
| Q8 | 分类法 | 涌现式，试点门禁时定骨架 |
| Q9 | 术语表 | 纳入 `glossary.md`，中英对照 |
| Q10 | 验收 | 对话样例 + 落盘文件双轨 |
| Q11 | 版本机制 | `raw/` 快照 + `SOURCES.md` 登记 + `fetched_at` |

## 3. 源文档清单

| ID | 标题 | URL | 类型 |
|----|------|-----|------|
| S1 | 广告agent梳理 | https://momcozy-in.feishu.cn/wiki/Vz2hw4OsoiMEDUkuB13cRnrsn7d | wiki 文档（试点） |
| S2 | 红人素材广告加推Agent Loop建设 | https://momcozy-in.feishu.cn/wiki/YwzBwYCxPin0zNkAT1VcVyPdnRf | wiki 文档 |
| S3 | 04 红人广告加推 Agent Loop 建设跟进 | https://momcozy-in.feishu.cn/wiki/UrxQw65qJiJZy3khi8gcR3MUnFh?table=tblc23Lk8CGPyMYY&view=vewr4PGEa7 | wiki 文档 + 内嵌多维表格 |
| S4 | 【产品整理】Meta广告AI自动诊断与优化_完整策略树 | https://momcozy-in.feishu.cn/sheets/Vl9FsvYkOhs74AtbOglcjjzWnDg | 飞书电子表格 |
| S5 | 广告监控&广告优化 Agent（一期：Meta） | https://momcozy-in.feishu.cn/wiki/WEenwzLRLi8xczkSHNlcfwySnGf | wiki 文档 |

## 4. 目标目录结构

```text
/Users/pray/project/AD/
├─ docs/knowledge/ad-agent-qa/        # 知识库本体（正式资产）
│  ├─ INDEX.md                        # 主题 → 卡片路由表
│  ├─ SOURCES.md                      # 源登记：url / type / fetched_at / last_modified
│  ├─ glossary.md                     # 术语表（中英对照 + 释义 + 卡片链接）
│  ├─ raw/                            # 原始快照（不可变溯源证据）
│  │  ├─ s1-ad-agent-overview.md
│  │  ├─ s2-influencer-push-loop.md
│  │  ├─ s3-influencer-push-tracking.md (+ bitable 快照)
│  │  ├─ s4-meta-diagnosis-strategy-tree.(xlsx|csv|md)
│  │  └─ s5-ad-monitoring-agent-meta.md
│  └─ cards/                          # 主题卡片（分类骨架待门禁 G1 后定）
│     └─ <theme-slug>.md
├─ tmp/outputs/kb-distill/            # 蒸馏中间笔记（可丢弃）
└─ drafts/docs/kb-ad-agent-qa-plan-draft-20261125.md  # 本方案
```

## 5. Phase 1 — 采集

对每个源文档，优先级降级：

1. **首选**：飞书原生导出（文档→docx/md，表格→xlsx/csv），经 ego-browser 下载到 `raw/`
2. **降级 A**：`page.evaluate` 滚动累积虚拟滚动容器（`.bear-web-x-container`）全文 innerText
3. **降级 B**：飞书内部 API（`page.fetch` 携带会话 cookie）
4. **兜底**：人工介入提示

S3 内嵌 bitable、S4 电子表格需单独处理：表格类优先原生导出，失败则 DOM 逐块提取。

采集时同步记录元数据：title、url、fetched_at、last_modified（页面可见则取）、doc_type。

浏览器操作边界：在已 claim 的 task space 0 内操作用户标签页；优先"导出/下载"动作，尽量减少可见滚动。

## 6. Phase 2 — 蒸馏

单源处理流：`raw/` 快照 → 通读 → 结构化蒸馏笔记（落 `tmp/outputs/kb-distill/`）→ 跨源主题归并 → 卡片草稿。

蒸馏笔记粒度：主题清单 / 核心概念 / 流程与决策逻辑 / 指标口径 / 案例 / 疑点。

标注规范：

- `[推断]` — 合理推断，非原文直述
- `[原文]` — 原文直述（默认省略，仅在易歧义处标注）
- `[待确认]` — 原文模糊或自相矛盾，需人工裁决

电子表格（S4）走独立路径：按 sheet/区域拆分 → 策略树/决策矩阵 → 场景化问答，不强行套文档蒸馏模板。

## 7. Phase 3 — 建库

### 卡片 frontmatter schema

```yaml
---
title: 主题卡片标题
doc_type: knowledge
module: ad-agent-qa
topic: <theme-slug>
status: draft | stable
created: YYYY-MM-DD
updated: YYYY-MM-DD
owner: self
source: human+ai
source_docs: [s1, s2, ...]
fetched_at: YYYY-MM-DD
tags: []
---
```

### 卡片正文结构

```markdown
# 主题名
> 一句话定位

## 核心问题
（本卡片回答的主题级问题）

## 系统解答
（分节正文，承载蒸馏后的知识）

## 高频问答索引
- Q: ... → 见 §小节 / 简短答案

## 相关卡片
- [[链接]] 或 md 相对链接
```

### 执行顺序

1. **试点**：S1《广告agent梳理》全流程（采集→蒸馏→1~2 张样例卡片 + glossary 种子 + INDEX 雏形）
2. **门禁 G1**：对话贴样例 + 文件落盘 → 用户确认风格/颗粒度
3. **门禁 G2**：提交建议分类骨架 → 用户确认
4. **批量**：S2~S5 采集 + 蒸馏 + 建卡
5. **汇总**：INDEX.md 路由表、SOURCES.md、glossary.md 定稿

## 8. Phase 4 — 验证

- 覆盖率矩阵：5 源 × 主题 → 每源关键主题 ≥1 卡覆盖
- 链接完整性：卡片间/INDEX/glossary 引用全部可解析
- 保真抽查：随机 ≥3 卡对照 raw 快照
- 术语表覆盖：正文高频术语均已收录
- 交付说明：产出统计 + 未覆盖/存疑清单

## 9. 风险与对策

| 风险 | 对策 |
|------|------|
| 飞书导出受限 | 降级链：原生导出 → 滚动提取 → 内部 API → 人工 |
| 内容量超预期 | 先抽取再评估，按"架构/策略 > 跟进细节"排优先级分批蒸馏 |
| S3/S4 表格结构复杂 | 独立提取路径，按区域拆分蒸馏 |
| 蒸馏跑偏 | 试点门禁 + `[推断]` 标注 + 保真抽查 |
| 文档后续更新 | raw 快照 + SOURCES.md 支持 diff 重跑（本期不建自动巡检） |

## 10. 里程碑

- M1：目录骨架 + SOURCES.md + S1 raw 快照
- M2：试点蒸馏产物（样例卡片 + 落盘）→ **G1**
- M3：分类骨架确认 → **G2**
- M4：5 源全部蒸馏入库
- M5：验证通过，交付
