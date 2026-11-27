---
title: 广告 Agent 问答知识库索引
doc_type: knowledge
module: ad-agent-qa
topic: index
status: draft
created: 2026-11-26
updated: 2026-11-26
owner: self
source: human+ai
---

# 广告 Agent 问答知识库 · INDEX

> 跨境电商品牌出海 · 广告类 Agent 知识库。主题卡片为主干，每卡含「核心问题 → 系统解答 → 高频问答索引」。
> 源文档见 [SOURCES.md](SOURCES.md)，术语见 [glossary.md](glossary.md)，原始快照见 [raw/](raw/)，增量更新流程见 [UPDATING.md](UPDATING.md)，跨源矛盾登记见 [CONFLICTS.md](CONFLICTS.md)。

## 按主题找卡片

### 系统全景与产品方案

| 卡片 | 回答的问题 | 来源 |
|------|-----------|------|
| [广告 Agent 系统全景架构](cards/architecture/ad-agent-system-landscape.md) | Momcozy 广告 Agent 体系由哪些 Loop 和 Agent 构成？全局增长飞轮怎么转？ | S1 |
| [广告监控与优化 Agent（一期：Meta）产品方案](cards/architecture/monitoring-optimization-agent-prd.md) | 监控工作台+飞书预警+自动化调整怎么落地？三档权限与回滚怎么设计？一期边界在哪？ | S5 |
| [广告投放 Agent 业务调研框架](cards/architecture/ad-ops-agent-research-framework.md) | Agent 设计前怎么调研人工作业全貌？33 列人工作业→AI 提效矩阵怎么用？调研进行到哪了？ | S14/S16 |

### 红人素材广告加推

| 卡片 | 回答的问题 | 来源 |
|------|-----------|------|
| [红人素材广告加推 Agent Loop · 角色·触点·链路全景](cards/influencer-boost/influencer-boost-loop-overview.md) | 红人优质素材如何自动化转化为广告？角色分工、触点、13 个 Agent 编排与 HITL 节点？ | S2 |
| [红人加推 Agent 清单与职责规格](cards/influencer-boost/influencer-boost-agent-specs.md) | 每个 Agent 的输入/输出/处理逻辑/负责人是什么？建设进度如何？ | S3 |
| [红人加推建设任务与进度](cards/influencer-boost/influencer-boost-build-tracking.md) | 21 项建设任务的状态、依赖、优先级、预估人天？ | S3 |

### Meta 广告诊断与优化

| 卡片 | 回答的问题 | 来源 |
|------|-----------|------|
| [Meta 广告诊断与优化 SOP](cards/meta-ads-diagnosis/meta-diagnosis-sop.md) | 广告异常按什么顺序排查（G0-G8）？优先级怎么定？动作铁律是什么？ | S4 |
| [Meta 诊断指标与基准线](cards/meta-ads-diagnosis/meta-diagnosis-metrics.md) | 每个检查阶段看哪些指标？阈值/基准线是多少？异常怎么判？ | S4 |
| [Meta 动作库与动作日志](cards/meta-ads-diagnosis/meta-action-library.md) | 可用动作有哪些（A-01~）？每个动作改什么、预期影响、回滚条件？日志怎么记？ | S4 |
| [Meta 投放师一日工作流 SOP](cards/meta-ads-diagnosis/meta-operator-daily-workflow.md) | 投放师的一天怎么过？8 环节各自的决策树和动作铁律？（人类执行版） | S6 |
| [Meta 诊断优化 SOP · Agent 训练版](cards/meta-ads-diagnosis/meta-diagnosis-sop-agent-training.md) | T0-T5 主决策树怎么走？L0-L4 五层各管什么？与 S4 策略树什么关系？ | S7 |
| [Meta 诊断五层规程与配套工具](cards/meta-ads-diagnosis/meta-diagnosis-layers-l0-l4.md) | L0-L4 每层诊断项细节？异常速查表？字段字典阈值？ | S7 |
| [Meta 投后数据明细与巡检模板](cards/meta-ads-diagnosis/meta-post-launch-data-inspection.md) | 投后巡检采集哪些数据？三层级字段模板怎么设计？巡检/操作记录列块怎么闭环？ | S8 |
| [多渠道周期报告生成契约](cards/meta-ads-diagnosis/multi-channel-report-contract.md) | 日/周/月报三段式结构？大盘 ROAS 怎么算？增长引擎 vs 拖后腿？行动指令怎么防「正确的废话」？ | S24 |
| [Meta 量化决策引擎](cards/meta-ads-diagnosis/meta-quantified-decision-engine.md) | 广告留还是杀怎么定量化？TCPL 锚点/广告数上限/80-20 双 CBO/毕业标准/衰退分档/放量协议？ | S25 |

### 广告基础机制与策略（行业通用）

| 卡片 | 回答的问题 | 来源 |
|------|-----------|------|
| [广告平台「算法自动」优化字段详解](cards/fundamentals/ad-algo-auto-fields.md) | 预算分配/智能出价/受众扩量/版位/关键词/素材组合/创意即定向/全托管各是什么逻辑？跨平台差异？何时不该放权？ | S9 |
| [广告竞价全链路流程图（14 步）](cards/fundamentals/ad-bidding-full-chain.md) | 一次广告展示背后 14 步怎么走？eCPM/GSP/Pacing/SKAN 怎么工作？哪些配置字段影响哪个环节？ | S10 |
| [产品不同阶段广告投放策略（8 阶段）](cards/fundamentals/product-lifecycle-ad-strategy.md) | 产品各生命周期阶段投什么目标/出价？每阶段必做实验？常见坑？ | S11 |
| [归因与测量体系](cards/fundamentals/attribution-measurement.md) | 各平台归因转化为什么不能相加？Cookie 末日是不是谣言？GA4/Google Ads DDA 迁移？增量测试怎么设计？Meridian vs Robyn？ | S22 |
| [广告账户治理纪律](cards/fundamentals/ad-account-governance.md) | 周检六问+四态判定？AI 审计怎么防没查的也打分？品牌/非品牌怎么拆？净现金放量观？再营销异 offer 原则？ | S25 |
| [归因模型算例与差异诊断](cards/fundamentals/attribution-models-reconciliation.md) | 同一笔订单六模型各分多少？DDA 何时可信？Ads-GA4 差 20% 正常吗？退款不对称？direct/品牌词虚高怎么读？ | S25 |
| [Payback 预算闸门](cards/fundamentals/payback-period-budget-gate.md) | LTV:CAC 为什么不可信？毛利回本怎么算？cohort 恢复路径？渠道能不能投的四步判据？ | S25 |

### 竞品分析

| 卡片 | 回答的问题 | 来源 |
|------|-----------|------|
| [广告投放 Agent 竞品分析（Navos/GrowthGPT/Zalify）](cards/competitor-analysis/ad-agent-competitor-landscape.md) | 三家竞品的产品形态、Agent 编排、能力边界？与自家体系差异？ | S12–S15 |

### Momcozy 业务实操（S1 附件）

| 卡片 | 回答的问题 | 来源 |
|------|-----------|------|
| [单品类垂直分层投放 Playbook（清洗机实例）](cards/business-context/audience-layering-playbook.md) | 单品类怎么按决策深度分浅/中/深三层？受众×关键词×素材怎么匹配？多产品生命周期怎么承接？ | S17 |
| [MP 项目管理方法论](cards/business-context/mp-project-methodology.md) | 投放需求→MP→上线→调节→复盘全链路怎么跑？横切底座四件套？哪些环节已识别为 AI 机会？ | S18/S19 |
| [Momcozy 人群画像洞察（孕→哺→育）](cards/business-context/momcozy-audience-persona.md) | 核心人群是谁？三阶段定位/数据/渠道分工/T0-T3 出价分层/可执行人群包？ | S20 |
| [吸奶器品线独立站全触点地图](cards/business-context/customer-touchpoint-map.md) | 7 阶段×120+ 触点怎么拆？站内外矩阵？渠道协同分工？竞品对标？自检清单？ | S21 |

### 平台运营打法（platform-ops-kb 蒸馏）

| 卡片 | 回答的问题 | 来源 |
|------|-----------|------|
| [TikTok Shop 广告增长打法](cards/platform-ops/tiktok-shop-growth-playbook.md) | GMV Max 是什么？SPS/NBFR/VoC 怎么读？affiliate 何时能放量？达人追踪怎么接 GMV Max？ | PO:* |
| [Amazon 广告打法](cards/platform-ops/amazon-ads-playbook.md) | ACoS/TACoS 分工？诊断顺序？否定词前置？SB+SP 协同？AI 广告能力？ | PO:* |
| [达人商业合作能力与合规](cards/platform-ops/creator-commerce-compliance.md) | Partnership Ads/IG Marketplace/Shopify Collabs/YouTube Shopping？FTC 披露红线？organic 能投广告吗？ | PO:* |
| [母婴类目跨平台增长 Overlay](cards/platform-ops/baby-maternity-growth-overlay.md) | 母婴资质三层？内容/claim 红线？跨平台上架顺序？Momcozy 案例证明什么？ | PO:* |
| [Amazon 广告运营打法](cards/platform-ops/amazon-ads-operations.md) | Campaign 架构树？预算分配%？出价表？Day7/14/30 检查点？周复盘 RYG？Prompts 被动扣费？AMC？ | S22 |
| [Amazon 关键词与 Listing 运营](cards/platform-ops/amazon-keyword-listing-ops.md) | T1/T2/T3 词库怎么分？否定词三类阈值？标题 75 字符等硬规则？VOC 挖词？广告反哺 Listing？ | S22 |
| [独立站 SEM 广告打法](cards/platform-ops/dsite-sem-ads-playbook.md) | 10 平台怎么选？Google 6-Campaign 架构？AIPL 预算分配？冷启动 SOP？大促 SEM？SEO-SEM 协同？LTV→CPA？ | S22 |
| [TikTok 内容×广告打法](cards/platform-ops/tiktok-content-ads-playbook.md) | 爆款公式/Hook/流量池？达人五层策略？四步广告测试？Spark vs In-Feed？CPA/ROAS 承受线？ | S22 |
| [Amazon Listing 语义化打造](cards/platform-ops/amazon-listing-semantic-ops.md) | COSMO/Alexa 对 Listing 意味着什么？八步工作流？五点决策链？ST/QA 怎么写？数据从哪抓？ | S23 |
| [Amazon Listing AI 评分细则](cards/platform-ops/amazon-listing-ai-score-rubric.md) | Listing 适不适合 AI 推荐？8 维怎么打分？75字符/Item Highlights 新规过渡期？N/A 怎么处理？ | S23 |
| [Amazon 评论洞察 VOC](cards/platform-ops/amazon-review-voc-ops.md) | 差评怎么分类归因？6 类痛点+严重度？VOC 怎么反哺 Listing/广告/QA？ | S23 |
| [广告创意策略系统](cards/platform-ops/ad-creative-strategy-system.md) | Hook 三组件管线？创意策略循环/证据分级？Meta 51 格式 S→F？Andromeda 下 partnership ads？竖屏 safe-zone/字幕/音频？防 AI 痕迹？ | S25 |
| [Google Search 广告手册](cards/platform-ops/google-search-playbook.md) | 意图阶梯怎么解锁？品牌词暂停测试？独立预算为什么？Broad 三条件？周检搜索词三遍？PMax 护栏？ | S25 |

## 按问题类型速查

- **想了解整体架构/有哪些 Agent** → ad-agent-system-landscape
- **红人素材加推怎么做** → influencer-boost 三张卡
- **Meta 广告效果差怎么诊断（规则引擎版）** → meta-diagnosis-sop → meta-diagnosis-metrics → meta-action-library（S4）
- **Meta 诊断的 Agent 训练版/五层规程细节** → meta-diagnosis-sop-agent-training → meta-diagnosis-layers-l0-l4（S7）
- **投放师一天怎么过（人类 SOP）** → meta-operator-daily-workflow（S6）
- **投后数据怎么采集/巡检台账怎么设计** → meta-post-launch-data-inspection（S8）
- **算法自动优化字段/竞价机制/产品阶段策略（行业通用）** → fundamentals 三张卡
- **竞品/Navos/GrowthGPT/Zalify/Agent 产品对比** → competitor-analysis 卡
- **单品类分层投放打法/受众×素材匹配** → audience-layering-playbook
- **MP/Brief/复盘方法论/项目管理** → mp-project-methodology
- **Momcozy 人群画像/出价分层 T0-T3/人群包** → momcozy-audience-persona
- **独立站触点/全生命周期/渠道协同/竞品对标** → customer-touchpoint-map
- **Agent 设计前的业务调研方法论** → ad-ops-agent-research-framework
- **监控预警与自动调整产品方案** → monitoring-optimization-agent-prd
- **TikTok Shop/GMV Max/SPS/affiliate 放量** → tiktok-shop-growth-playbook
- **Amazon 广告/ACoS/TACoS/否定词/SB+SP** → amazon-ads-playbook
- **达人合作/Partnership Ads/FTC 披露/creator brief** → creator-commerce-compliance
- **母婴类目合规/上架资质/Momcozy 案例** → baby-maternity-growth-overlay
- **术语不懂** → glossary.md

## 对话层（conversational access）

知识库提供三层消费接口：

| 层 | 入口 | 用途 |
|----|------|------|
| 查询协议 | [QUERY.md](QUERY.md) | 问题类型→资源路由表 + 冲突处理规则 + 引用规范 + 知识边界声明。任何 agent 按此协议即可对话式使用本库 |
| 原子问答 | [qa/](qa/) | ~132 条自包含 Q→A 对（按集群分文件），每条带溯源。覆盖审计见 [qa/COVERAGE.md](qa/COVERAGE.md) |
| 飞书机器人 | `src/kb_bot/`（项目根） | lark-oapi WebSocket + 本库检索 + OpenAI 兼容 LLM 的问答机器人 MVP |
| 语义层 | [graph/](graph/) | 广告投放域知识图谱 v0：611 节点 / 1010 边（SKOS-lite 模式层 + JSON 实例层）。查询契约见 `src/graph_query/`，bot 已接入实体链接 |
| 经验卡池 | [experience/](experience/) | 自进化飞轮：bot 日志信号→草稿卡→人审晋升为知识修订。扫描器 `src/experience_drafter.py` |

> qa/ 与 cards/ 同为 `status: review`，随卡片验收同步转 stable。
