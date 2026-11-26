---
title: 对话层问答覆盖审计
doc_type: knowledge
module: ad-agent-qa
topic: qa-coverage-audit
status: review
created: 2026-11-26
updated: 2026-11-26
owner: self
source: human+ai
---

# 问答覆盖审计（对话层 Step 1）

> 目的：站在真实用户（Momcozy 广告团队/Agent 建设者/管理者）视角生成自然语言问题，逐题映射知识库卡片，产出覆盖矩阵与缺口清单。
> 本清单同时是 Step 2 原子 Q&A 数据集的**出题种子**——标 ✓ 的题可直接扩写为 Q→A 对，标 △ 的需回卡片补内容，标 ✗ 的为知识库真缺口。
> 状态：✓ 卡内可答 / △ 部分可答（有口径冲突或覆盖不全）/ ✗ 无卡可答

## 一、架构与 Agent 系统（architecture + influencer-boost）

| # | 用户可能问的问题 | 映射卡片 | 状态 |
|---|------------------|----------|------|
| 1 | Momcozy 广告 Agent 体系一共有几个 Loop？分别是什么？ | ad-agent-system-landscape | ✓（10 Loop，OCR 待终核） |
| 2 | 广告 Agent 的顶层目标是什么？ | ad-agent-system-landscape | ✓ |
| 3 | 广告 Agent 大致分几类？ | ad-agent-system-landscape | ✓ |
| 4 | 哪些环节必须人工确认？ | ad-agent-system-landscape / monitoring-optimization-agent-prd | ✓ |
| 5 | 广告创建怎么从人工逐项配置变自动？ | ad-agent-system-landscape | ✓ |
| 6 | 广告创意怎么持续变好？ | ad-agent-system-landscape | ✓ |
| 7 | 投放经验怎么沉淀复用？ | ad-agent-system-landscape | ✓ |
| 8 | 素材组装 Agent 建了吗？ | ad-agent-system-landscape | △（S1 列了节点 vs S2/S3 明确不建，口径冲突） |
| 9 | 监控优化 Agent 一期做什么？不做什么？ | monitoring-optimization-agent-prd | ✓ |
| 10 | 监控 Agent 会不会乱动账户？防呆机制有哪些？ | monitoring-optimization-agent-prd | ✓ |
| 11 | LLM 在系统里干什么？会不会幻觉？ | monitoring-optimization-agent-prd | ✓ |
| 12 | 告警怎么分级？会不会轰炸投手？ | monitoring-optimization-agent-prd | ✓ |
| 13 | 新广告/学习期对象会被误杀吗？ | monitoring-optimization-agent-prd | ✓ |
| 14 | 执行动作后怎么验证？失败怎么回滚？ | monitoring-optimization-agent-prd / meta-action-library | ✓ |
| 15 | Agent 一期什么时候上线？排期怎么安排？ | monitoring-optimization-agent-prd | ✓（M0–M5 约 11 周） |
| 16 | 业务调研框架怎么组织？ | ad-ops-agent-research-framework | ✓ |
| 17 | 33 列矩阵的 AI 评估维度是什么？ | ad-ops-agent-research-framework | ✓ |
| 18 | 业务调研做完了吗？ | ad-ops-agent-research-framework | ✓（未完成，S16 空模板） |
| 19 | 红人素材怎么变成广告？全流程有哪些角色？ | influencer-boost-loop-overview | ✓ |
| 20 | 加推覆盖哪些平台？TikTok/IG/YouTube 差异？ | influencer-boost-loop-overview | ✓ |
| 21 | 素材没授权能投放吗？授权流程？ | influencer-boost-loop-overview / influencer-boost-agent-specs | ✓ |
| 22 | 素材组装 Agent 为什么没有？ | influencer-boost-loop-overview | ✓（明确暂不建设） |
| 23 | 潜力评分怎么算？ | influencer-boost-loop-overview / influencer-boost-agent-specs | ✓（6 维加权） |
| 24 | 优化 Agent 会不会自动改广告？人工把关在哪？ | influencer-boost-loop-overview | ✓（L1-L3 三级） |
| 25 | 上线检查具体查什么？ | influencer-boost-loop-overview | ✓（7 通用+平台专项） |
| 26 | 监控分析只看加推广告吗？ | influencer-boost-loop-overview | ✓（覆盖全量广告） |
| 27 | 复盘结果怎么用？ | influencer-boost-loop-overview | ✓ |
| 28 | 用户主要在哪些系统操作？ | influencer-boost-loop-overview | ✓（飞书 IM 主入口） |
| 29 | S3 Agent 表登记了多少 Agent？怎么分组？ | influencer-boost-agent-specs | ✓（13 条 9 组） |
| 30 | 哪些 Agent 填了接口规格？ | influencer-boost-agent-specs | ✓（仅 3 条） |
| 31 | Agent 名称和职责为什么对不上？ | influencer-boost-agent-specs | △（5 条疑似模板占位，待核实） |
| 32 | Meta 策略 Agent 的输入字段有哪些？ | influencer-boost-agent-specs | ✓（17 字段） |
| 33 | 策略 Agent 的处理逻辑是什么？ | influencer-boost-agent-specs | ✓（仅模板示例 6 步） |
| 34 | 授权状态由谁跟踪？ | influencer-boost-agent-specs | △（名称-职责错位记录） |
| 35 | 各 Agent 的训练人/负责人是谁？ | influencer-boost-agent-specs / influencer-boost-build-tracking | ✓ |
| 36 | 建设任务一共多少项？当前进度？ | influencer-boost-build-tracking | ✓（21 项：完成4/进行中4/待验收4/未开始9） |
| 37 | P0 最高优先级任务有哪些？ | influencer-boost-build-tracking | ✓（10 项） |
| 38 | YouTube 线建设进度如何？ | influencer-boost-build-tracking | ✓（整体未启动） |
| 39 | 预估人天投入多少？ | influencer-boost-build-tracking | ✓（78 人天） |
| 40 | 计划完成时间填了吗？ | influencer-boost-build-tracking | ✓（仅 2 条有值） |
| 41 | 效果监控 Agent 依赖的"上线检查 Agent"是什么？ | influencer-boost-build-tracking | ✗（任务表无此条目，待确认是否遗漏） |

## 二、Meta 广告诊断与优化（meta-ads-diagnosis，8 卡）

| # | 用户可能问的问题 | 映射卡片 | 状态 |
|---|------------------|----------|------|
| 42 | 诊断必须按什么顺序？能跳过前置检查吗？ | meta-diagnosis-sop | ✓（G0–G8 固定） |
| 43 | P0/P1/P2 怎么分？P0 会冻结什么？ | meta-diagnosis-sop / meta-diagnosis-metrics | ✓ |
| 44 | 动作铁律具体有哪些？ | meta-diagnosis-sop | ✓ |
| 45 | 65 节点/196 分支怎么组织？ | meta-diagnosis-sop | ✓ |
| 46 | 诊断输出是什么格式？ | meta-diagnosis-sop / meta-action-library | ✓（五段式） |
| 47 | 数据不可信/归因差怎么办？ | meta-diagnosis-sop / meta-diagnosis-layers-l0-l4 | △（多口径：差异 10%/20%/30%/40% 分属不同检查点） |
| 48 | 多个分支同时命中怎么办？ | meta-diagnosis-sop / meta-action-library | ✓（一次只出一个主动作） |
| 49 | 样本不足能做诊断吗？ | meta-diagnosis-sop / meta-diagnosis-layers-l0-l4 / meta-operator-daily-workflow | △（$50+Purchase30 vs $100+Purchase50 vs $50/14天 三套门槛） |
| 50 | G5 预算异常为什么「结束本轮」？ | meta-diagnosis-sop | ✓ |
| 51 | 这套 SOP 适用什么场景？ | meta-diagnosis-sop / meta-diagnosis-sop-agent-training | ✓ |
| 52 | 投放师的一天按什么顺序做事？ | meta-operator-daily-workflow | ✓ |
| 53 | 哪些情况禁止直接动预算？ | meta-operator-daily-workflow | ✓ |
| 54 | Campaign 处于 Learning 怎么处理？ | meta-operator-daily-workflow / meta-diagnosis-layers-l0-l4 | ✓（周转化<50 不动） |
| 55 | 怎么区分素材问题和受众问题？ | meta-operator-daily-workflow / meta-diagnosis-layers-l0-l4 | ✓（交叉验证法） |
| 56 | 落地页 CVR 低怎么定位断在哪层？ | meta-operator-daily-workflow / meta-diagnosis-layers-l0-l4 | ✓（六层漏斗找断崖） |
| 57 | 素材什么时候换？怎么给创意团队提需求？ | meta-operator-daily-workflow / meta-action-library | ✓ |
| 58 | 新素材上线后多久能判？疲劳怎么识别？ | meta-operator-daily-workflow / meta-diagnosis-metrics / meta-diagnosis-layers-l0-l4 | △（CTR<0.5% / 周环比-30% / 峰值<0.70 / 频次>4-5 多口径） |
| 59 | 动作做完多久验证？不达预期怎么办？ | meta-operator-daily-workflow / meta-action-library | ✓（48h/72h/7d 窗口） |
| 60 | 日报必须包含什么？ | meta-operator-daily-workflow | ✓（五段式） |
| 61 | S6（人类 SOP）和 S4/S5/S7（规则资产）什么关系？ | meta-operator-daily-workflow / meta-diagnosis-layers-l0-l4 / meta-diagnosis-sop-agent-training | ✓（同源异构） |
| 62 | ROAS 突然崩了第一步做什么？ | meta-diagnosis-layers-l0-l4 | ✓（先排归因假崩盘） |
| 63 | L0–L4 五层各管什么？先查哪层？ | meta-diagnosis-layers-l0-l4 / meta-diagnosis-sop-agent-training | ✓ |
| 64 | 数据不够能做 L4 细分诊断吗？ | meta-diagnosis-layers-l0-l4 / meta-diagnosis-sop-agent-training | △（$50/14天 vs $100+Purchase≥50） |
| 65 | 归因差异多少算异常？ | meta-diagnosis-layers-l0-l4 / meta-diagnosis-metrics / meta-diagnosis-sop | △（<10%通过/>30%异常；≤20%放行；>30~40%判追踪——分检查点不同） |
| 66 | 素材疲劳怎么判断？ | meta-diagnosis-layers-l0-l4 / meta-diagnosis-metrics / meta-operator-daily-workflow | △（-30%周环比 vs CTR/峰值<0.70，两套指标定义） |
| 67 | Learning 期能做优化动作吗？ | meta-diagnosis-layers-l0-l4 / meta-operator-daily-workflow | ✓ |
| 68 | 看数的固定顺序是什么？ | meta-operator-daily-workflow / mp-project-methodology | ✓（大盘→下钻→素材人群→归类） |
| 69 | 动作库一共有多少动作？都是什么类型？ | meta-action-library | ✓（A-01~A-16） |
| 70 | 动作预估幅度可以当承诺吗？ | meta-action-library | ✓（经验值±50%浮动） |
| 71 | 什么时候只「继续观察」？ | meta-action-library | ✓（A-01） |
| 72 | 扩量预算怎么操作才安全？ | meta-action-library | ✓（20%分2-3次/50%分3次） |
| 73 | P0 止血用什么动作？ | meta-action-library | ✓（A-04/A-05） |
| 74 | 为什么动作日志必须 21 列全填？ | meta-action-library | ✓ |
| 75 | 复核谁回填、什么时候回填？ | meta-action-library | ✓（4h/24h/72h） |
| 76 | 达到回滚条件会怎样？ | meta-action-library | ✓（CPA+20%/ROAS-20%/延迟>6h） |
| 77 | A-16 修复归因算投放动作吗？ | meta-action-library | ✓（数据修复非投放） |
| 78 | A-15 结构重构为什么中高风险？ | meta-action-library | ✓（重置学习-10%） |
| 79 | 诊断指标一共有多少个？ | meta-diagnosis-metrics | ✓（26 行，S5 口径 25 项差 1） |
| 80 | 所有阈值都是固定值吗？ | meta-diagnosis-metrics | ✓（第一版可配置默认值） |
| 81 | CPA/ROAS 什么条件下才能正常判断？ | meta-diagnosis-metrics | ✓（成熟度≥80%+购买≥10） |
| 82 | CTR/CPC/CPM 健康区间？ | meta-diagnosis-metrics | ✓（按目标分） |
| 83 | 落地页漏斗各环节基准线？ | meta-diagnosis-metrics | ✓（六段） |
| 84 | 哪些指标只观察不动作？ | meta-diagnosis-metrics | ✓ |
| 85 | 素材疲劳比怎么算？ | meta-diagnosis-metrics | ✓（当前CTR÷峰值CTR<0.70） |
| 86 | 视频素材专属指标？ | meta-diagnosis-metrics | △（3秒播放/完播率两套阈值并存） |
| 87 | 频次多少算过高？ | meta-diagnosis-metrics / meta-diagnosis-sop / meta-diagnosis-layers-l0-l4 | △（≤3/≤5/>5/>10 四档口径） |
| 88 | 异常方向是双向的吗？ | meta-diagnosis-metrics | ✓（部分双向） |
| 89 | S7（Agent 训练版）和 S4（策略树）什么关系？ | meta-diagnosis-sop-agent-training | ✓ |
| 90 | T0–T5 主决策树怎么走？ | meta-diagnosis-sop-agent-training | ✓ |
| 91 | T2.x 症状路由是干什么的？ | meta-diagnosis-sop-agent-training | ✓ |
| 92 | S7 和 S4 阈值冲突听谁的？ | meta-diagnosis-sop-agent-training / meta-diagnosis-layers-l0-l4 | ✓（并列+执行级以 S4 为准[推断]） |
| 93 | S7 的 P0/P1/P2 和 S4 一样吗？ | meta-diagnosis-sop-agent-training | ✓（同名不同定义） |
| 94 | S7 和 S4 哪个更新？ | meta-diagnosis-sop-agent-training | ✗（无法判断版本新旧） |
| 95 | Meta 投后巡检采集哪些数据？ | meta-post-launch-data-inspection | ✓（三层级 ~40 字段） |
| 96 | 巡检结论和操作记录在模板里怎么设计？ | meta-post-launch-data-inspection | ✓（双列块） |
| 97 | S8 的漏斗口径和 S7 L4 一样吗？ | meta-post-launch-data-inspection | △（访客数四段 vs 事件数五段） |
| 98 | 案例数据说明了什么？ | meta-post-launch-data-inspection | ✓（吸奶器X1 三实验） |
| 99 | S8 和 S5 监控 Agent PRD 什么关系？ | meta-post-launch-data-inspection | ✓ |
| 100 | 为什么 AdSet 命名这么长？ | meta-post-launch-data-inspection | ✓（全要素可解析） |

## 三、行业通用机制（fundamentals，3 卡）

| # | 用户可能问的问题 | 映射卡片 | 状态 |
|---|------------------|----------|------|
| 101 | CBO 和 ABO 的区别？ | ad-algo-auto-fields | ✓ |
| 102 | 智能出价（tCPA/tROAS/oCPM）怎么工作？ | ad-algo-auto-fields / ad-bidding-full-chain | ✓ |
| 103 | 新账户能直接开智能出价/全托管吗？ | ad-algo-auto-fields | ✓（需 20-50 转化积累） |
| 104 | 受众扩量（Adv+ Audience）是什么？ | ad-algo-auto-fields | ✓ |
| 105 | 什么是「创意即定向」？ | ad-algo-auto-fields / ad-bidding-full-chain | ✓ |
| 106 | 程序化创意（DCO/RSA）和普通多素材区别？ | ad-algo-auto-fields | ✓ |
| 107 | Meta 新创意冷启动和其他平台差异？ | ad-algo-auto-fields | ✓（Meta 更激进压流量） |
| 108 | 全托管模式人还能调什么？ | ad-algo-auto-fields | ✓ |
| 109 | Audience Network 版位为什么要单独监控？ | ad-algo-auto-fields / meta-diagnosis-layers-l0-l4 | ✓ |
| 110 | 广告是怎么被选出来展示的？ | ad-bidding-full-chain | ✓（14 步） |
| 111 | eCPM 公式？oCPM 为什么乘 pCVR？ | ad-bidding-full-chain | ✓ |
| 112 | GSP 次高价是什么意思？会多扣钱吗？ | ad-bidding-full-chain | ✓ |
| 113 | Pacing 因子是什么？ | ad-bidding-full-chain | ✓ |
| 114 | iOS ATT 拒绝后归因怎样？ | ad-bidding-full-chain | ✓（SKAN 降级） |
| 115 | 什么是「创意即召回」？ | ad-bidding-full-chain | ✓ |
| 116 | 频控为什么前置到召回阶段？ | ad-bidding-full-chain | ✓ |
| 117 | 曝光和点击分别什么时候计费？ | ad-bidding-full-chain | ✓ |
| 118 | 模型更新怎么形成飞轮？ | ad-bidding-full-chain | ✓ |
| 119 | 新产品投放第一阶段做什么？ | product-lifecycle-ad-strategy | ✓（测试期） |
| 120 | 预热期和发布期区别？目标一样吗？ | product-lifecycle-ad-strategy | ✓ |
| 121 | 首销期怎么投？ | product-lifecycle-ad-strategy | ✓ |
| 122 | 增长期加预算怎么加？ | product-lifecycle-ad-strategy | ✓（每3-4天+20%） |
| 123 | 常态期怎么判断广告真有效？ | product-lifecycle-ad-strategy | ✓（Incrementality） |
| 124 | 产品衰退/清仓期还投吗？ | product-lifecycle-ad-strategy | ✓（低预算收割） |
| 125 | 大促期（618/双11/BFCM）怎么投？ | product-lifecycle-ad-strategy | ✓（蓄水/开门红/返场） |
| 126 | 为什么增长期 ROAS 设下限而非目标？ | product-lifecycle-ad-strategy | ✓ |

## 四、Momcozy 业务实操（business-context，4 卡）

| # | 用户可能问的问题 | 映射卡片 | 状态 |
|---|------------------|----------|------|
| 127 | Momcozy 核心人群是谁？ | momcozy-audience-persona | ✓（品质型新妈妈 孕→哺→育） |
| 128 | 哪个阶段投放 ROI 最高？ | momcozy-audience-persona | ✓（孕期，预算被低估） |
| 129 | 哪个阶段是复购金矿？ | momcozy-audience-persona | ✓（哺乳期 18.8%/27.7%） |
| 130 | 哪个阶段体量最大？ | momcozy-audience-persona | ✓（育儿期 61,832 首单） |
| 131 | DTC 和 Amazon 的人群画像有何不同？ | momcozy-audience-persona | ✓ |
| 132 | 出价怎么分层？ | momcozy-audience-persona | ✓（T0–T3） |
| 133 | 渠道怎么分工？ | momcozy-audience-persona | ✓（TikTok引流/Google收割） |
| 134 | 高价值交叉复购对有哪些？ | momcozy-audience-persona | ✓ |
| 135 | 清洗机单品类怎么分层投放？ | audience-layering-playbook | ✓（浅/中/深+四阶段） |
| 136 | 孕早期为什么不投清洗机？ | audience-layering-playbook | ✓（需求未觉醒，种草蓄水） |
| 137 | 产后 0-6 月为什么可以直接转化？ | audience-layering-playbook | ✓（痛点顶峰） |
| 138 | 素材怎么匹配投放层级？ | audience-layering-playbook | ✓（唤醒/教育/促单） |
| 139 | 多产品矩阵下各阶段卖什么？ | audience-layering-playbook | ✓ |
| 140 | 已购人群怎么交叉销售？ | audience-layering-playbook | ✓（三组测试） |
| 141 | 投放需求怎么进入系统？ | mp-project-methodology | ✓（A/B 两类触发） |
| 142 | MP 文档必须包含什么？ | mp-project-methodology | ✓ |
| 143 | 怎么保证复盘时能解释「为什么中途改了」？ | mp-project-methodology | ✓（变更记录+审计日志） |
| 144 | 广告新建怎么批量化又不失控？ | mp-project-methodology | ✓（笛卡尔积+Preflight+熔断） |
| 145 | AB Test 怎么系统化管理？ | mp-project-methodology | ✓（测试组+MAB） |
| 146 | 哪些数据口径问题会让复盘失真？ | mp-project-methodology | ✓ |
| 147 | 文档识别的 AI 机会最多在哪？ | mp-project-methodology | ✓（20+ 项清单） |
| 148 | 吸奶器用户生命周期有几阶段？ | customer-touchpoint-map | ✓（7 阶段） |
| 149 | 购前触点怎么分层？ | customer-touchpoint-map | ✓（认知/兴趣/考虑） |
| 150 | 配件复购为什么是利润核心？ | customer-touchpoint-map | ✓（耗材飞轮+订阅） |
| 151 | 独立站和 Amazon 怎么分工？ | customer-touchpoint-map / momcozy-audience-persona | ✓（65%新客 vs 35%留存） |
| 152 | Momcozy 的触点差异化打法？ | customer-touchpoint-map | ✓ |
| 153 | 新站冷启动先补哪些触点？ | customer-touchpoint-map | ✓（自检清单） |

## 五、竞品分析（competitor-analysis，1 卡）

| # | 用户可能问的问题 | 映射卡片 | 状态 |
|---|------------------|----------|------|
| 154 | Navos 是什么？有哪些 Agent？ | ad-agent-competitor-landscape | ✓（六 Agent+7 能力模块） |
| 155 | Navos 除投放外还做什么？ | ad-agent-competitor-landscape | ✓（VOC/GEO/KOL/预审） |
| 156 | GrowthGPT 的产品结构是什么？ | ad-agent-competitor-landscape | ✓（四层+六功能） |
| 157 | GrowthGPT 的数据从哪来？ | ad-agent-competitor-landscape | ✓（四路数据逻辑） |
| 158 | Zalify 竞品调研了什么？ | ad-agent-competitor-landscape | ✗（纪要无权限，能力边界未知） |
| 159 | 竞品能给自家广告 Agent 提供什么参考？ | ad-agent-competitor-landscape | ✓ |

## 六、知识库元问题

| # | 用户可能问的问题 | 映射 | 状态 |
|---|------------------|------|------|
| 160 | 这个知识库能回答什么问题？有哪些内容？ | INDEX.md → QUERY.md（Step3） | △（待 QUERY.md） |
| 161 | 术语不懂（如 Pacing/CBO/SKAN）？ | glossary.md | ✓ |
| 162 | EQ<6 和 EQ<4 哪个对？ | CONFLICTS.md | △（源文档矛盾，需呈现分歧） |
| 163 | L4 数据门槛 $50 和 $100 哪个对？ | CONFLICTS.md | △（同上） |
| 164 | 素材疲劳 -30% 和 CTR/峰值<0.70 哪个对？ | CONFLICTS.md | △（同上） |
| 165 | S7 和 S4 哪个诊断文档更新？ | meta-diagnosis-sop-agent-training | ✗ |

## 七、覆盖缺口清单（✗ + 高价值 △）

### 硬缺口（无任何卡片覆盖）

| 缺口 | 说明 | 建议动作 |
|------|------|----------|
| **G1 Zalify 竞品能力** | S15 仅引用、纪要无权限 | 保持 `[待确认]`，等权限或用户补充 |
| **G2 上线检查 Agent 在建设任务表中无条目** | S3 任务表可能遗漏 | 向表负责人确认是否归并 |
| **G3 S7/S4 版本新旧** | 无法判断 | 待业务确认 |
| **G4 红人 BD/建联流程** | 怎么找红人、谈合作、建联——库里只有授权环节 | 若有源文档可补；否则标注边界 |
| **G5 素材创意生产/拍摄策略** | 只有生命周期实验和触点内容策略，无素材制作方法论 | 同上 |
| **G6 Google/TikTok Momcozy 具体打法** | fundamentals 有机制、persona 有渠道数据，但缺平台级投放 playbook | 可从 persona+layering 卡交叉推断 `[推断]`，或等新源 |
| **G7 预算金额具体建议** | 只有阶段预算心态和测试预算（$50-100/天），缺系统预算规划方法 | MP 卡有预算拆分方法论可交叉 |
| **G8 团队组织/角色编制** | 只有 S3 负责人分工，无团队结构 | 边界外 |
| **G9 合规/审核申诉细节** | 只有合规 Agent 节点和预审风险分级 | 边界外 |
| **G10 多语言/本地化策略** | 未覆盖 | 边界外 |
| **G11 物流/履约/客服运营** | 仅触点地图提及 | 边界外（非广告 Agent 范围） |
| **G12 价格/促销机制** | 仅触点促销触点+大促预算分配 | 边界外 |

### 口径冲突型 △（对话层必须呈现分歧，不能静默选边）

| 冲突点 | 涉及卡片 | CONFLICTS.md 编号 |
|--------|----------|-------------------|
| EQ 阈值 <6 vs <4 | sop / layers / daily-workflow | 已登记 |
| L4 数据门槛 $50 vs $100+Purchase≥50 | layers / sop / sop-agent-training | 已登记 |
| 素材疲劳：周环比-30% vs CTR/峰值<0.70 | layers / metrics / daily-workflow | 已登记 |
| 频次阈值 ≤3/≤5/>5/>10 四档 | metrics / sop / layers / daily-workflow | 已登记 |
| 归因差异 10%/20%/30%/40% 分检查点 | layers / metrics / sop | 已登记 |
| 漏斗口径：访客数四段 vs 事件数五段 | post-launch-data-inspection / layers | 已登记 |
| 视频指标双阈值（3秒播放/完播率） | metrics | 已登记 |
| S8 标题「待业务确认」字段口径 | post-launch-data-inspection | 已登记 |
| 素材组装 Agent 建/不建 | landscape / loop-overview | 已登记（待确认） |
| 动作库编号 A-xx 两套不对应 | sop-agent-training | 已登记 |

## 八、结论

- **165 题中 ✓ 148 题（90%）**：卡片可直接支撑对话回答
- **△ 13 题（8%）**：可答但含口径冲突或部分覆盖——对话层必须引用 CONFLICTS.md 呈现分歧
- **✗ 4 题（2%）**：真缺口（Zalify、上线检查 Agent 条目、S7/S4 版本、边界外领域）
- **12 个边界外缺口**：红人 BD、素材制作、平台级打法、预算规划、团队/合规/多语言/物流/价格——超出当前源文档范围，建议在 QUERY.md 中明确声明知识边界

**下一步**：Step 2 以本清单 ✓/△ 题为种子扩写原子 Q→A 对；✗ 题在 QA 数据集中标注「知识库暂无可靠来源」由对话层如实回答。
