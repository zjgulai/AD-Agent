---
title: 红人素材广告加推 13 个 Agent 职责矩阵与接口规格
doc_type: knowledge
module: ad-agent-qa
topic: influencer-boost-agent-specs
status: review
created: 2026-11-26
updated: 2026-11-26
owner: self
source: human+ai
source_docs: [S3, S2]
fetched_at: 2026-11-26
---

# 红人素材广告加推 13 个 Agent 职责矩阵与接口规格

## 核心问题

S3「Agent」多维表格登记了哪些 Agent？每个 Agent 的职责、输入/输出规格、处理逻辑、训练人与负责人、需求文档分别是什么？数据填到了什么程度？

## 系统解答

### 1. 数据概况与质量提示

- 共 **13 条记录**，填写状态全部为「未开始」。
- 实质内容极度不均：仅「Meta策略Agent（模板示例）」填写了完整的输入/输出/处理逻辑三段式；「Meta 策略 Agent」「Meta 创建 Agent」有 JSON spec 输入/输出与需求文档链接；「潜力评分 Agent」的输入/输出/处理逻辑均为「讨论」占位；其余记录的输入/输出/处理逻辑/需求文档大面积为 null。
- ⚠️ **名称-职责错位**：5 条记录的「Agent 名称」是"平台 × 职能"式命名（TikTok/YouTube 策略、TikTok/Meta/YouTube 创建），但「所属模块」+「Agent 职责」描述的是另一种职能（授权管理/广告创建/效果监控/优化建议/复盘总结）。本卡按「所属模块」分组、以「Agent 职责」字段为准，名称差异一律标 [待确认]。
- 「Meta策略Agent（模板示例）」的训练人、负责人为空，需求文档为 null——模板行不计入正式分工 [推断]。

### 2. 职责矩阵（按所属模块分组）

#### 素材发现（1 个）

- **素材发现 Agent** · 状态：未开始
  - 职责：从红人内容池和社媒渠道自动发现与品牌匹配的优质素材，按素材质量、互动数据等维度筛选并推送给潜力评分环节。
  - 训练人：胡深深、雍娜｜负责人：李莹
  - 输入/输出/处理逻辑/需求文档：[待确认]（均为 null）

#### 潜力评分（1 个）

- **潜力评分 Agent** · 状态：未开始
  - 职责：对候选素材和红人进行多维度潜力评分，结合历史表现和互动数据输出分数与推荐等级，为加推决策提供依据。
  - 训练人：胡深深、雍娜｜负责人：李莹
  - 输入：[待确认]；输出：「讨论」；处理逻辑：「讨论」（均为占位符）；需求文档：无

#### 授权管理（1 个）

- **「TikTok 策略 Agent」** · 状态：未开始 ⚠️ 名称与模块/职责不符 [待确认]
  - 所属模块登记为「授权管理」，职责为：跟踪红人素材的授权状态与有效期，自动识别未授权、即将到期和已过期素材，提醒负责人补签授权——实为授权管理类 Agent 职责，"TikTok 策略"名称疑为模板占位。
  - 训练人：雍娜、陈英凯｜负责人：周文军
  - 输入/输出/处理逻辑/需求文档：[待确认]

#### 广告策略（2 个）

- **Meta策略Agent（模板示例）** · 状态：未开始 ⚠️ 模板行
  - 职责：根据品牌目标、预算、受众和历史投放效果，生成平台适配的投放策略（定向、出价、预算分配等）供人工确认。
  - 所属模块：广告策略｜训练人：无｜负责人：无｜需求文档：无
  - 其它功能说明：支持按周自动刷新策略；预算超支或效果异常时自动预警；策略变更记录留痕，供复盘总结 Agent 使用。
  - **输入**（三部分）：① 业务上下文 JSON——`campaign_id`、`influencer{id,name,platform,followers,avg_views,engagement_rate,content_tags}`、`content_list[]`（content_id/type/post_time/likes/comments/shares/views/link）、`product{sku,name,price_usd,category,selling_points}`、`budget{daily_budget_usd,total_budget_usd,schedule{start,end}}`、`target{kpi,target_value,audience{region,age,interests}}`；② 历史投放数据（近 30 天）——`account_id`、`recent_campaigns[]{roas,ctr,cpc,best_creative_type}`、`audience_insights{top_age,top_placement}`；③ 平台能力配置——Meta 广告目标枚举（OUTCOME_AWARENESS / OUTCOME_TRAFFIC / OUTCOME_SALES）、版位白名单、素材规格（9:16 竖版视频 ≤30s、首图 3 秒出效果）。
  - **输出**：结构化 JSON——`trace_id`、`strategy{campaign_id, objective, budget, ad_sets[{adset_id,name,audience,placements,bid_strategy,creatives[{content_id,format,copy,cta}]}]}`、`forecast{est_ctr,est_cpc,est_roas,confidence}`、`compliance{passed,checked_items[敏感词/版权/平台政策]}`、`next_action=queue_to_ad_creation_agent`、`notify{channel=feishu_card, receivers}`。
  - **处理逻辑**（6 步，为全表唯一完整填写）：
    1. 参数校验与补全：`campaign_id`、预算、KPI 必填，缺失返回错误码 `INVALID_PARAM` 及缺失字段清单；受众为空时默认使用红人粉丝画像。
    2. 内容潜力预筛：调潜力评分 Agent 接口（`POST /api/scoring/contents`）逐条打分，仅保留 `score ≥ 70` 素材并按分降序。
    3. 策略生成（规则层 + LLM 层混合）：规则层按 KPI 映射广告目标（ROAS/转化→OUTCOME_SALES，曝光→OUTCOME_AWARENESS）；日预算 < $1000 限 1 广告组、3 条以内创意；自动排除受众重叠 >60% 的历史广告组。LLM 层将红人内容摘要、产品卖点、受众洞察拼 Prompt 输出结构化策略 JSON，约束"不得虚构素材 ID、预算不得超限"。
    4. 合规检查：调上线检查 Agent 预检接口，校验文案敏感词、图片版权、平台政策；不通过回写并重新生成（最多 2 次，仍失败转人工）。
    5. 输出编排：合并规则层与 LLM 层结果为最终策略 JSON，基于历史 CTR/CPC 生成预估指标，落库到广告创建任务队列。
    6. 异常与降级：广告系统 API 超时（>5s）重试 2 次后降级为"仅输出策略不自动创建"；全链路写 `trace_id` 日志供复盘。
- **Meta 策略 Agent** · 状态：未开始
  - 职责：同模板示例（根据品牌目标、预算、受众和历史投放效果生成平台适配投放策略供人工确认）。
  - 所属模块：广告策略｜训练人：雍娜、陈英凯｜负责人：周文军
  - 需求文档：[红人广告策略Agent、广告创建 Agent Dify 工作流搭建指南](https://momcozy-in.feishu.cn/docx/W83wdekI5ojPhuxvFXycZpIUnig)
  - **输入**（素材侧字段 spec，17 字段）：`material_id`（如 26FF0911）、`material_seq`（如 2026潜力加热视频26FF0911）、`creator_name`、`source_platform`（tiktok/instagram/youtube）、`country`、`hook_type`（痛点开场/产品展示/对比测评/使用场景/开箱）、`potential_score`（0-100）、`score_reasons[]`、`authorization_code`（Partnership Ad Code / 品牌内容授权码）、`authorization_expiry`（YYYY-MM-DD）、`SPU_CODE`、`product_name`、`gtm_product_line`（9 枚举品线：吸奶器/喂养/家居/家纺/婴幼儿/快消/护肤/服纺/全品线）、`optimizer`、`link`（落地页 URL）、`kol_owner`（可选）。
  - **输出**（投放侧策略 spec）：`strategy_version`、`run_start_date`/`run_end_date`、`optimizer_name`、`strategy_template`、`account_config`、`default_config`、`campaigns[]`（`campaign_key`/`campaign_name`、`buying_type=AUCTION`、`objective`、`status=PAUSED`、`bid_strategy`、`budget_mode` ABO/CBO、`daily_budget`、`special_ad_categories`、`adsets[]`：`destination_type`/`optimization_goal`/`billing_event`/`attribution_spec`/`promoted_object{pixel_id,custom_event_type}`/`targeting{geo_locations,custom_audiences,excluded_custom_audiences,interests}`/`targeting_automation`/`ads[]`：`ad_name`/`material_id`/`creator_name`/`content_type`/`creative{use_partnership_ad,partnership_ad_code,video_id,image_hash,object_story_spec{page_id,instagram_actor_id,video_data{call_to_action,link_url_tags=utm_*}}}`/`tracking_specs`）、`strategy_summary`（人类可读摘要）。
  - 处理逻辑/其它功能说明：[待确认]（null）

#### 广告创建（1 个）

- **「YouTube 策略 Agent」** · 状态：未开始 ⚠️ 名称与模块/职责不符 [待确认]
  - 所属模块登记为「广告创建」，职责为：依据已确认的投放策略，自动在三平台广告系统中创建广告计划、单元和素材关联，生成创建结果回执——实为创建 Agent 职责。
  - 训练人：雍娜、陈英凯｜负责人：周文军；输入/输出/处理逻辑/需求文档：[待确认]

#### 效果监控（2 个）

- **「TikTok 创建 Agent」** · 状态：未开始 ⚠️ 名称与模块/职责不符 [待确认]
  - 所属模块登记为「效果监控」，职责为：实时拉取各平台广告投放数据（消耗、曝光、点击、转化等），监控异常波动并触发预警——实为监控 Agent 职责。
  - 训练人：雍娜、陈英凯｜负责人：周文军；其余字段：[待确认]
- **效果监控 Agent** · 状态：未开始
  - 职责：与上条文本相同（实时拉取各平台投放数据、监控异常波动并触发预警）。
  - 所属模块：效果监控｜训练人：易思琦｜负责人：陈亮利；其余字段：[待确认]

#### 优化建议（2 个）

- **「Meta 创建 Agent」** · 状态：未开始 ⚠️ 名称与模块/职责不符 [待确认]
  - 所属模块登记为「优化建议」，职责为：基于效果监控与分析结论，生成出价、预算、素材更换等优化建议，并跟踪建议的执行情况——实为优化 Agent 职责。
  - 数据矛盾点：其「输入」字段填的是与「Meta 策略 Agent」输出完全相同的策略 JSON spec（`strategy_version`/`campaigns`/`adsets`/`ads` 嵌套结构），更像创建 Agent 的入参而非优化建议输入；需求文档与 Meta 策略 Agent 相同（Dify 工作流搭建指南）。[待确认]
  - 训练人：雍娜、陈英凯｜负责人：周文军；输出/处理逻辑：[待确认]
- **广告优化 Agent** · 状态：未开始
  - 职责：与上条文本相同（生成出价、预算、素材更换等优化建议并跟踪执行情况）。
  - 所属模块：优化建议｜训练人：易思琦｜负责人：陈亮利；其余字段：[待确认]

#### 复盘总结（2 个）

- **「YouTube 创建 Agent」** · 状态：未开始 ⚠️ 名称与模块/职责不符 [待确认]
  - 所属模块登记为「复盘总结」，职责为：投放结束后对整体链路进行复盘，沉淀成功经验与问题清单，形成可复用的总结报告——实为复盘 Agent 职责。
  - 训练人：雍娜、陈英凯｜负责人：周文军；其余字段：[待确认]
- **复盘总结 Agent** · 状态：未开始
  - 职责：与上条文本相同（投放结束后复盘、沉淀经验与问题清单、形成可复用总结报告）。
  - 所属模块：复盘总结｜训练人：余越、易思琦｜负责人：李莹；其余字段：[待确认]

#### Agent 编排框架（1 个）

- **Agent 编排框架** · 状态：未开始
  - 职责：负责各 Agent 的注册、调度、依赖编排与上下文传递，串联素材发现到复盘总结的完整 Agent Loop。
  - 所属模块：Agent 编排框架｜训练人：无｜负责人：李尚毅；其余字段：[待确认]

### 3. 速查表

| 所属模块 | Agent 名称 | 职责（一句话） | 训练人 | 负责人 | 状态 |
|---------|-----------|---------------|--------|--------|------|
| 素材发现 | 素材发现 Agent | 发现品牌匹配优质素材并推送评分 | 胡深深、雍娜 | 李莹 | 未开始 |
| 潜力评分 | 潜力评分 Agent | 多维评分输出分数与推荐等级 | 胡深深、雍娜 | 李莹 | 未开始 |
| 授权管理 | 「TikTok 策略 Agent」⚠️ | 跟踪授权状态/有效期并提醒补签 | 雍娜、陈英凯 | 周文军 | 未开始 |
| 广告策略 | Meta策略Agent（模板示例）⚠️ | 生成平台投放策略供人工确认 | 无 | 无 | 未开始 |
| 广告策略 | Meta 策略 Agent | 同上 | 雍娜、陈英凯 | 周文军 | 未开始 |
| 广告创建 | 「YouTube 策略 Agent」⚠️ | 按已确认策略创建广告计划/单元/素材关联 | 雍娜、陈英凯 | 周文军 | 未开始 |
| 效果监控 | 「TikTok 创建 Agent」⚠️ | 拉取投放数据、监控异常并预警 | 雍娜、陈英凯 | 周文军 | 未开始 |
| 效果监控 | 效果监控 Agent | 同上 | 易思琦 | 陈亮利 | 未开始 |
| 优化建议 | 「Meta 创建 Agent」⚠️ | 生成出价/预算/素材更换优化建议并跟踪 | 雍娜、陈英凯 | 周文军 | 未开始 |
| 优化建议 | 广告优化 Agent | 同上 | 易思琦 | 陈亮利 | 未开始 |
| 复盘总结 | 「YouTube 创建 Agent」⚠️ | 复盘链路、沉淀经验与问题清单 | 雍娜、陈英凯 | 周文军 | 未开始 |
| 复盘总结 | 复盘总结 Agent | 同上 | 余越、易思琦 | 李莹 | 未开始 |
| Agent 编排框架 | Agent 编排框架 | Agent 注册/调度/依赖编排/上下文传递 | 无 | 李尚毅 | 未开始 |

### 4. 与 Loop 全景的对应关系 [推断]

- 无平台前缀的 6 条（素材发现、潜力评分、效果监控、广告优化、复盘总结、Agent 编排框架）与 S2 画板中的通用/统一汇总层 Agent 对应。
- 「广告策略」组目前只有 Meta 条目（含模板示例）有实质接口 spec；TikTok/YouTube 策略条目缺失，但建设任务表存在对应任务 [推断]。
- 授权管理模块在 S2 Loop 中对应 HITL 节点 ②.5 授权索要环节；Agent 表仅 1 条记录，建设任务表对应「授权索要（流程确认）」集成对接任务。

## 高频问答索引

- **Q：S3「Agent」表登记了多少 Agent？怎么分组？**
  A：13 条记录。按「所属模块」分 9 组：素材发现 1、潜力评分 1、授权管理 1、广告策略 2、广告创建 1、效果监控 2、优化建议 2、复盘总结 2、Agent 编排框架 1。注意「授权管理」不在任务预设的 8 模块清单中，是源数据实际值。
- **Q：哪些 Agent 填了接口规格（输入/输出）？**
  A：仅 3 条。「Meta策略Agent（模板示例）」有完整三段式（输入=业务上下文+历史投放+平台配置；输出=策略+预估+合规 JSON）；「Meta 策略 Agent」有素材侧输入 spec（17 字段）和投放侧输出 spec；「Meta 创建 Agent」的输入与 Meta 策略 Agent 输出 spec 完全相同。
- **Q：为什么有的 Agent 名称和职责对不上？**
  A：5 条记录（「TikTok 策略 Agent」「YouTube 策略 Agent」「TikTok 创建 Agent」「Meta 创建 Agent」「YouTube 创建 Agent」）疑似按"平台 × 职能"模板命名，但所属模块和职责字段记录的是授权管理/创建/监控/优化/复盘职能。本卡以模块+职责为准归位，名称差异标 [待确认]，需向表负责人核实。
- **Q：Meta 策略 Agent 的输入包含哪些字段？**
  A：素材侧 17 字段：material_id、material_seq、creator_name、source_platform、country、hook_type、potential_score、score_reasons、authorization_code、authorization_expiry、SPU_CODE、product_name、gtm_product_line、optimizer、link、kol_owner。
- **Q：策略 Agent 的处理逻辑是什么？**
  A：仅模板示例填写了 6 步：参数校验（INVALID_PARAM）→ 潜力预筛（调评分接口，score≥70 入池）→ 规则层+LLM 层生成策略 → 合规预检（上线检查 Agent，最多重生成 2 次）→ 输出编排落库创建队列 → API 超时降级为"仅输出不自动创建"。
- **Q：红人素材授权状态由谁跟踪？**
  A：「TikTok 策略 Agent」这条记录的所属模块是「授权管理」、职责是跟踪授权状态与有效期并提醒补签——名称疑为占位，实际应为授权管理类 Agent。训练人雍娜、陈英凯，负责人周文军。
- **Q：需求文档链接有哪些？**
  A：仅「Meta 策略 Agent」和「Meta 创建 Agent」挂了同一链接：[红人广告策略Agent、广告创建 Agent Dify 工作流搭建指南](https://momcozy-in.feishu.cn/docx/W83wdekI5ojPhuxvFXycZpIUnig)。其余 11 条需求文档均为 null。
- **Q：各模块的训练人与负责人是谁？**
  A：素材发现/潜力评分：训练胡深深+雍娜、负责人李莹；授权管理/广告策略/广告创建/效果监控/优化建议/复盘总结的平台条目：训练雍娜+陈英凯、负责人周文军；效果监控/广告优化通用条目：训练易思琦、负责人陈亮利；复盘总结通用条目：训练余越+易思琦、负责人李莹；Agent 编排框架：负责人李尚毅（无训练人）。
- **Q：所有 Agent 的填写状态？**
  A：全部为「未开始」。

## 相关卡片

- [红人素材广告加推 Agent Loop · 角色·触点·链路全景](./influencer-boost-loop-overview.md)
- [红人素材广告加推建设任务全景与进度](./influencer-boost-build-tracking.md)
- [广告监控与优化 Agent PRD（一期 Meta）](../architecture/monitoring-optimization-agent-prd.md) — S5
- [广告 Agent 系统全景架构](../architecture/ad-agent-system-landscape.md) — S1 画板
