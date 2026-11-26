---
title: Q&A 数据集 - 红人素材加推 Agent Loop
doc_type: knowledge
module: ad-agent-qa
topic: qa-influencer-boost
status: review
created: 2026-11-26
updated: 2026-11-26
owner: self
source: human+ai
---

# 红人素材加推 Agent Loop Q&A

覆盖 `cards/influencer-boost/`（3 卡：loop-overview、agent-specs、build-tracking）。通用架构问答见 `architecture.md`。

### Q1. 红人素材怎么变成广告？全流程有哪些角色？
**A**：红人内容经素材发现与潜力评分进入授权管理（未授权走授权索要 HITL），授权完成后进待确认加推池；广告策略 Agent 生成投放策略 → 创建 Agent 生成 Campaign 草稿 → 上线检查（授权/UTM/追踪/命名/预算/品牌安全/禁用词+平台专项）→ 人工确认后 API 落地 → 监控 → 优化（三级自动化）→ 复盘沉淀回流素材池。用户主要在飞书 IM 交互（通知/确认/问询），红人系统管内容池与授权，广告系统管策略/草稿/异常/建议，三方平台后台是最终投放地。
> 溯源：`cards/influencer-boost/influencer-boost-loop-overview.md`

### Q2. 加推覆盖哪些平台？平台差异怎么处理？
**A**：TikTok、Instagram（Meta）、YouTube（Google）。策略、创建、监控、优化按平台拆分独立 Agent 或独立规则；上线检查用统一引擎+平台差异化规则；监控阈值按平台独立配置。YouTube 线建设整体未启动（策略/创建 Agent 均 P2 未开始）。
> 溯源：`cards/influencer-boost/influencer-boost-loop-overview.md` + `influencer-boost-build-tracking.md`

### Q3. 素材没授权能投放吗？授权流程怎么走？
**A**：不能。高评分素材自动检查授权状态，未授权进入授权索要 HITL：IM/邮件向红人发邀约 → 红人回复授权码 → 负责人在红人系统登记授权码+有效期（或 Agent 自动识别登记）→ 授权完成才进待确认加推池。这是 3 个人工确认节点之一。
> 溯源：`cards/influencer-boost/influencer-boost-loop-overview.md`

### Q4. 素材组装 Agent（⑤）为什么没有？
**A**：明确暂不建设，直接用红人原视频授权加推；Demo 中灰显标注「下一阶段建设」。注意这与 S1 全景画板「素材组装 Agent」节点存在口径差异——S1 列了该节点但 S2/S3 明确不建，冲突待确认。
> 溯源：`cards/influencer-boost/influencer-boost-loop-overview.md`；冲突见 `CONFLICTS.md`

### Q5. 潜力评分怎么算？
**A**：6 维加权——内容质量 20%、自然互动 15%、产品匹配 20%、人群匹配 15%、历史表现 20%、品牌安全 10%，输出分数+等级+推荐平台。处理逻辑中潜力预筛调评分接口，score≥70 入池（仅模板示例填写）。
> 溯源：`cards/influencer-boost/influencer-boost-loop-overview.md` + `influencer-boost-agent-specs.md`

### Q6. Agent 会不会自动改广告？人工把关在哪？
**A**：优化 Agent 分三级自动化：L1 仅建议、L2 执行前 IM 审批、L3 低风险动作（如低效素材降预算 10%）自动执行后通知。另有 3 个人工确认节点：授权索要、加推确认、策略/投放确认。
> 溯源：`cards/influencer-boost/influencer-boost-loop-overview.md`

### Q7. 上线检查具体查什么？
**A**：通用 7 项（素材授权/UTM 规范/追踪配置/命名规则/预算阈值/品牌安全/禁用词）+ 平台专项（TikTok Spark Ads 授权码与时长、Meta 版权/Reels/Pixel 事件、YouTube TrueView/Google Ads 关联/频道关联）。不通过则阻断创建并 IM 通知修改重检。
> 溯源：`cards/influencer-boost/influencer-boost-loop-overview.md`

### Q8. 监控和分析是只看加推广告吗？
**A**：不是。⑧监控和⑨分析覆盖**全量广告**（三平台汇总+分平台对比），不只限于红人加推。
> 溯源：`cards/influencer-boost/influencer-boost-loop-overview.md`

### Q9. 复盘结果怎么用？
**A**：⑬复盘 Agent 输出日/周报（红人内容数据+广告数据+平台对比+结论+下一步建议），同时推给广告负责人和红人推广负责人；结论反哺下一轮素材发现，形成 Loop 闭环。
> 溯源：`cards/influencer-boost/influencer-boost-loop-overview.md`

### Q10. 信息不全时策略 Agent 怎么办？
**A**：缺目标国家、预算上限、平台素材格式等关键信息时，经飞书 IM 主动向广告负责人问询，补齐后继续生成策略。
> 溯源：`cards/influencer-boost/influencer-boost-loop-overview.md`

### Q11. S3「Agent」表登记了多少 Agent？怎么分组？
**A**：13 条记录。按「所属模块」分 9 组：素材发现 1、潜力评分 1、授权管理 1、广告策略 2、广告创建 1、效果监控 2、优化建议 2、复盘总结 2、Agent 编排框架 1。「授权管理」不在任务预设的 8 模块清单中，是源数据实际值。
> 溯源：`cards/influencer-boost/influencer-boost-agent-specs.md`

### Q12. 哪些 Agent 填了接口规格（输入/输出）？
**A**：仅 3 条。「Meta策略Agent（模板示例）」有完整三段式（输入=业务上下文+历史投放+平台配置；输出=策略+预估+合规 JSON）；「Meta 策略 Agent」有素材侧输入 spec（17 字段）和投放侧输出 spec；「Meta 创建 Agent」的输入与 Meta 策略 Agent 输出 spec 完全相同。
> 溯源：`cards/influencer-boost/influencer-boost-agent-specs.md`

### Q13. 为什么有的 Agent 名称和职责对不上？
**A**：5 条记录（「TikTok 策略 Agent」「YouTube 策略 Agent」「TikTok 创建 Agent」「Meta 创建 Agent」「YouTube 创建 Agent」）疑似按"平台 × 职能"模板命名，但所属模块和职责字段记录的是授权管理/创建/监控/优化/复盘职能。卡片以模块+职责为准归位，名称差异标 `[待确认]`，需向表负责人核实。
> 溯源：`cards/influencer-boost/influencer-boost-agent-specs.md`

### Q14. Meta 策略 Agent 的输入包含哪些字段？
**A**：素材侧 17 字段：material_id、material_seq、creator_name、source_platform、country、hook_type、potential_score、score_reasons、authorization_code、authorization_expiry、SPU_CODE、product_name、gtm_product_line、optimizer、link、kol_owner。
> 溯源：`cards/influencer-boost/influencer-boost-agent-specs.md`

### Q15. 策略 Agent 的处理逻辑是什么？
**A**：仅模板示例填写了 6 步：参数校验（INVALID_PARAM）→ 潜力预筛（调评分接口，score≥70 入池）→ 规则层+LLM 层生成策略 → 合规预检（上线检查 Agent，最多重生成 2 次）→ 输出编排落库创建队列 → API 超时降级为"仅输出不自动创建"。
> 溯源：`cards/influencer-boost/influencer-boost-agent-specs.md`

### Q16. 红人素材授权状态由谁跟踪？
**A**：「TikTok 策略 Agent」这条记录的所属模块是「授权管理」、职责是跟踪授权状态与有效期并提醒补签——名称疑为占位，实际应为授权管理类 Agent。训练人雍娜、陈英凯，负责人周文军。
> 溯源：`cards/influencer-boost/influencer-boost-agent-specs.md`

### Q17. 需求文档链接有哪些？
**A**：仅「Meta 策略 Agent」和「Meta 创建 Agent」挂了同一链接：[红人广告策略Agent、广告创建 Agent Dify 工作流搭建指南](https://momcozy-in.feishu.cn/docx/W83wdekI5ojPhuxvFXycZpIUnig)。其余 11 条需求文档均为 null。
> 溯源：`cards/influencer-boost/influencer-boost-agent-specs.md`

### Q18. 各模块的训练人与负责人是谁？
**A**：素材发现/潜力评分：训练胡深深+雍娜、负责人李莹；授权管理/广告策略/广告创建/效果监控/优化建议/复盘总结的平台条目：训练雍娜+陈英凯、负责人周文军；效果监控/广告优化通用条目：训练易思琦、负责人陈亮利；复盘总结通用条目：训练余越+易思琦、负责人李莹；Agent 编排框架：负责人李尚毅（无训练人）。
> 溯源：`cards/influencer-boost/influencer-boost-agent-specs.md` + `influencer-boost-build-tracking.md`

### Q19. 建设任务一共多少项？当前进度分布？
**A**：21 项。类型分布：Agent 建设 11、集成对接 5、系统功能页面 4、基础设施 1。进度：已完成 4（Meta 策略/创建、TikTok 策略/创建 Agent）；进行中 4（潜力评分 Agent、Agent 编排框架、飞书 IM 集成、Meta Ads API 对接）；待验收 4（授权索要、红人内容池页、加推工作台页、广告列表页）；未开始 9。
> 溯源：`cards/influencer-boost/influencer-boost-build-tracking.md`

### Q20. P0 最高优先级任务、YouTube 线进度、预估人天分别如何？
**A**：P0 共 10 项：潜力评分 Agent、Meta 策略/创建 Agent、复盘总结 Agent、Agent 编排框架、飞书 IM 集成、TikTok/Meta Ads API 对接、红人内容池页面、效果分析页面。YouTube 线整体未启动（策略/创建 Agent P2、API 对接 P1 均未开始且无计划时间）。12 项有预估人天合计 78 人天（Agent 建设 73 + 工作台页 5），最大单项效果监控/复盘总结各 10 人天。FDE 分工：周文军 10 项、李尚毅 5 项、李莹 5 项、王璐瑶 1 项。计划完成时间仅 2 条有值（均 2026-10-29）。
> 溯源：`cards/influencer-boost/influencer-boost-build-tracking.md`

### Q21. 效果监控 Agent 依赖的「上线检查 Agent」是什么？
**A**：建设任务表中无此条目 `[待确认]`。可能对应 S2 Loop 全景中的上线检查环节（⑦），但未在建设任务中单列，需向表负责人确认是否遗漏或归并到其他任务。
> 溯源：`cards/influencer-boost/influencer-boost-build-tracking.md`
