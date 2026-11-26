---
title: 术语表
doc_type: knowledge
module: ad-agent-qa
topic: glossary
status: stable
created: 2026-11-26
updated: 2026-11-26
owner: self
source: human+ai
---

# 术语表

> 中英对照 + 一句话释义 + 首次出现位置。随卡片建设持续补充。

| 术语 | 英文/全称 | 释义 | 出处 |
|------|-----------|------|------|
| Agent Loop | — | 「感知→决策→执行→反馈」闭环式 Agent 工作流；本库核心组织单元 | S1/S2 |
| HITL | Human-In-The-Loop | 人工介入节点：Agent 推送卡片由人确认/修改后才继续执行 | S2/S5 |
| 加推 | Boost / Ad Boost | 将红人已有内容作为广告素材投放推广；Ad Boost Plan = 加推策略方案 | S2/S3 |
| Ad Potential Score | — | 素材潜力评分，6 维加权（内容质量/互动/产品匹配/人群匹配/历史表现/品牌安全） | S2 |
| 素材发现 Agent | Material Discovery Agent | 定时扫描三平台红人内容池并初筛潜力素材 | S2/S3 |
| 上线检查 Agent | Pre-launch Check Agent | 广告创建前的合规校验引擎（7 项通用 + 平台差异化规则） | S2 |
| 自动化分级 | Automation Level | L1 仅建议 / L2 执行前人工确认 / L3 低风险自动执行 | S2 |
| ROAS | Return On Ad Spend | 广告支出回报率 = 广告收入 / 广告花费 | 全部 |
| CPA | Cost Per Acquisition | 单次获客成本 | 全部 |
| CAC | Customer Acquisition Cost | 获客成本（含自然+付费口径时与 CPA 区分使用） | S1/S5 |
| CTR / CVR / CPM | Click-Through / Conversion / Cost Per Mille | 点击率 / 转化率 / 千次曝光成本 | 全部 |
| Spend | — | 广告消耗金额 | S2/S5 |
| LTV | Lifetime Value | 用户生命周期价值 | S1/S5 |
| Lookalike / LAL | — | Meta 相似受众扩展 | S2 |
| CBO | Campaign Budget Optimization | Meta 广告系列预算优化 | S2 |
| Advantage+ | — | Meta 自动化投放产品族（扩量/受众/版位自动化） | S2 |
| Spark Ads | — | TikTok 通过授权码把红人原生视频转为广告的格式 | S2 |
| TrueView | — | YouTube 可跳过信息流广告格式 | S2 |
| UTM | Urchin Tracking Module | 链接追踪参数规范 | S2/S5 |
| Pixel / TikTok Pixel / Google Tag | — | 各平台转化追踪像素/标签 | S2 |
| 诊断引擎 | Diagnosis Engine | 65 节点 / 196 分支的规则化诊断决策树（S4 策略树产品化） | S4/S5 |
| G0–G8 | — | S4 固定检查顺序：数据可信度→资格→追踪归因→目标事件→样本→预算→专项→分层→安全→复核 | S4 |
| P0/P1/P2 | — | 处置优先级：止血 / 当日 / 计划内 | S4 |
| 动作铁律 | Action Iron Rules | 一次只动一个主变量、学习期不判效、动作后 4h/24h/72h 复核、归因成熟度≥80% | S4 |
| 动作日志 | Action Log | 21 列留痕模板：每次诊断与动作必填 | S4/S5 |
| 授权码 | Authorization Code | 红人视频广告授权凭证（TikTok Spark Ads 等场景必需） | S2 |
| EQ | Event Quality / Event Match Quality | 事件质量分，衡量 Pixel/CAPI 回传数据与广告归因的匹配度（S4 阈值：≥6 正常、4~6 预警、<4 停止诊断） | S4 |
| CAPI | Conversions API | Meta 服务端转化回传接口，与 Pixel 并用提升归因质量 | S4 |
| Learning / 学习期 | Learning Phase | 广告系统学习投放模型的阶段，期间不判效果 | S4/S5 |
| Pacing | — | 预算消耗节奏，正常区间 80%~120%，<60% 或 >130% 判异常 | S4 |
| 熔断器 | Circuit Breaker | S5 自动化调整的安全机制：异常率超阈自动降级/停用自动执行 | S5 |
| 三档执行权限 | — | S5 自动调整权限：只建议 / 执行前人工确认 / 低风险自动执行（与 S2 优化 Agent L1-L3 同构） | S5 |
| 动作白名单/排除 | — | S5 允许自动执行的 5 个动作 vs 禁止自动执行的 4 个动作清单 | S5 |
| 上下文注入 | Context Injection | S5 机制：按对象+时间窗检索诊断 JSON 与动作日志注入 LLM 上下文（≤5s） | S5 |
| 五段式输出 | — | S4 诊断输出规范：异常→证据→根因→动作→影响预估 | S4 |
| 冷却期 | Cooldown | 同一对象同类动作两次执行的最小间隔（24h~72h） | S4 |
| L0–L4 | — | S7 诊断五层：L0 账户健康 / L1 Campaign / L2 AdSet / L3 Ad 素材 / L4 落地页漏斗 | S7 |
| T0–T5 | — | S7 主决策树节点编号：T0 前置排雷、T1 L1、T2 症状路由、T3 L2、T4 L3、T5 L4 | S7 |
| 到达率 | LPV/出站点击 | 广告点击后真正到达落地页的比例，基准 ≥70%，<60% 判链路问题 | S7 |
| 浏览率 | ViewContent/LPV | 到达后产生浏览行为的比例，基准 ≥60~70% | S7 |
| 加购率 | ATC/ViewContent | 浏览用户中加购比例，基准 3~8%（品类差异大） | S7 |
| 结账发起率 | IC/ATC | 加购用户中发起结账比例，基准 ≥60% | S7 |
| Learning Limited | — | 学习受限状态：预算过低/受众过窄/频繁编辑导致，7 天+ 需处理 | S7 |
| CAT | Creative Asset Tagging / 素材标签体系 | S7 L3 诊断项：素材标签与效果关联分析 | S7 |
| 五段式诊断 | — | 异常→证据→根因→动作→影响预估，S4/S7 共同的输出规范 | S4/S7 |
| 验证窗口 | — | S6 动作效果观察期：素材 48h、动作 72h、结构调整 7 天，未达预期回滚 | S6 |
| 一句话动作 | — | S7 速查表粒度：每个异常现象对应一行处置指令 | S7 |
| 投后数据明细 | Post-launch Data Detail | S8 三层级字段模板：系列/组/创意层指标+巡检结论+操作记录列块 | S8 |
| 广告巡检 | Ad Inspection | S8 预留列块：巡检日期/诊断结论/推荐动作/优先级/复检重点 | S8 |
| 末次归因 | Last-touch Attribution | S8 漏斗口径「当日末次归因」：转化记到最后一次点击 | S8 |
| CBO / ABO | Campaign / Ad Set Budget | 预算优化方式：CBO 系列级预算算法跨组分配；ABO 组级预算人工锁定 | S9 |
| OCPM / OCPC | Optimized CPM / CPC | 按转化目标优化的智能出价（巨量/腾讯/快手）；Meta 对应 Cost cap/Bid cap/Lowest cost | S9 |
| Adv+ Audience | — | Meta 受众扩量：人工定向降级为种子信号，算法探索-利用找人 | S9 |
| 优选广告位 / 版位自动分配 | Placement Optimization | 按各版位转化性价比实时分预算（Feed/Reels/Stories/AN/穿山甲/优量汇） | S9 |
| 广泛匹配 / 智能匹配 | Broad / Smart Match | 搜索广告关键词自动扩展（Google/百度专属，信息流无此概念） | S9 |
| RSA / DCO / 程序化创意 | Responsive Search Ad / Dynamic Creative Optimization | 素材池自动组合变体实时测试；Pin 固定位不参与组合 | S9 |
| 创意即定向 | Creative as Targeting | 素材内容语义自动匹配人群（巨量最成熟；Meta CAT 同类） | S9/S10 |
| 全托管模式 | PMax / SPC / ASC / 放量投放 | 人只给目标+预算+素材+回传，算法接管全部决策（Google/TikTok/Meta/巨量） | S9 |
| eCPM | Effective CPM | 预期千次展示收益：出价×pCTR（×pCVR）×1000，是竞价排序分 | S10 |
| GSP / VCG 次高价 | Generalized Second Price | 广义第二价格扣费：按第二名 eCPM 计费而非自己出价 | S10 |
| PacingFactor | — | 预算消耗速度调价因子：消耗快降价、慢提价，保证日预算全天平滑 | S10 |
| pCTR / pCVR / pValue | Predicted CTR / CVR / Value | 深度学习模型对「计划×创意」的点击率/转化率/转化价值预估 | S10 |
| Ad Quality Score | 广告质量分 | 素材质量/用户体验/历史转化调控项，加入 Total Score 竞价 | S10 |
| SKAN | SKAdNetwork | iOS 隐私归因方案：ATT 未授权时启用，延迟 24-48h、无单用户 click_id | S10 |
| MMP | Mobile Measurement Partner | 第三方移动归因（AppsFlyer/Adjust），跨渠道去重 | S10 |
| 有效曝光定义 | Viewability | 各版位曝光判定规则：信息流停留1秒/开屏完成/Banner可见50% | S10 |
| PMF | Product-Market Fit | 产品-市场匹配，测试期北极星前提 | S11 |
| SOV | Share of Voice 声量份额 | 发布期北极星指标之一 | S11 |
| MER | Marketing Efficiency Ratio | 综合营销效率回报率，常态期北极星 | S11 |
| BLS | Brand Lift Study 品牌提升研究 | 发布期必做实验：Test vs Control 问卷测认知提升，预算 $5K+ | S11 |
| Incrementality / Geo Holdout | 增量测试/地理对照 | 常态期必做：相似城市一组停投验证广告真实增量，月花 $75K+ 至少一次 | S11 |
| Win-back | 老客唤醒 | 衰退期必做：历史购买+加购未购人群低成本收割，成本比新客低 5 倍 | S11 |
| 生命周期 8 阶段 | — | 测试→预热→发布→首销→增长→常态→衰退清仓 + 大促横切（蓄水/开门红/返场） | S11 |
| Navos | — | 钛动科技（Tec-Do）出海营销 AI 产品，"AI 广告团队"六 Agent 编排，Meta 官方一级代理背景 | S12 |
| 钛动科技 / Tec-Do | — | Navos 母公司，中国大陆 11 家 Meta 官方一级代理商之一，服务 10 万+广告主 | S12 |
| Agentic Workflow | — | 多 Agent 自主协作的工作流模式，Navos 2.0 主打能力之一 | S12 |
| 素材预审 / Meta 素材预审 | Creative Pre-review | Navos 素材审核能力：提交前预判风险等级（案例判「高风险」） | S12 |
| Creative Boost | — | 素材衰退时的紧急替换机制，Navos 投放分析清单中的推荐动作 | S12 |
| GEO / AI 可见性诊断 | Generative Engine Optimization | Navos 能力：评估品牌在 AI 搜索/问答中的可见性（可访问性/爬行性/内容结构/内容质量） | S12 |
| KOL 布局分析（Htag） | — | 用标题 Htag 分析竞品 KOL 投放策略，Navos 调研中的方法 | S12 |
| GrowthGPT | — | 竞品：四层结构（大模型底座/专家技能层/平台API层/自然语言交互层）+ 六功能的广告 Agent 产品 | S13/S13b |
| 创编计划 | Creative + Campaign | GrowthGPT 一键生成素材与投放计划的合称 | S13b |
| 专家 skill 模型 | Expert Skill Model | GrowthGPT 数据逻辑：蒸馏 10 年+投手经验植入系统的经验模型 | S13b |
| Zalify | — | 被调研的广告系统类竞品；正文在无权限纪要中，能力边界 `[待确认]` | S15 |
| MP 环节 | Marketplace 环节 | Momcozy 广告作业分类：MP 环节/非 MP 环节 × 海外/国内 四象限；相关 wiki 文档无权限 | S14 |
| 33 列调研矩阵 | — | S16「人工作业全场景梳理」框架：场景→作业→输入/输出→成本→AI 可替代性→优先级 | S16 |
| AI 可替代性三档 | — | 完全替代/部分替代/无法替代，S16 矩阵的核心评估维度 | S16 |

| 加推工作台 | Boost Workbench | 广告系统中承载三平台策略确认与创建的页面 | S2 |
| MP / Marketing Plan | — | 投放策略文档：目标+节奏+预算拆分+结构模板+资源清单+KPI/阈值，版本化可追溯至广告 ID | S18 |
| Brief | — | 投放需求清单/需求合同：需求背景、目标 KPI、投放范围、目标事件、节奏周期、可用资源、约束 | S18 |
| 事件合同 | Event Contract | 事件触发条件/必要参数/去重键/验收方式的版本化约定，保证追踪数据可信 | S18 |
| 归因口径 | Attribution Rules | 时间窗+数据源优先级（平台/GA4/归因工具/订单系统）+例外场景的统一约定 | S18 |
| 资产库 | Asset Library | 素材/受众/落地页的版本化管理+投后表现回流（可对上广告 ID） | S18 |
| AOV | Average Order Value | 客单价 = 转化价值 ÷ 转化数 | S20 |
| TGI | Target Group Index | Amazon ASI 人群购买集中度指标，>100 表示超平均购买倾向 | S20 |
| NTB / NTBR | New-to-Brand (Rate) | Amazon 新客占比/新客率，衡量拉新程度；Baby Products NTB 93.9% 为拉新金矿 | S20 |
| SA 渗透率 | Share of Audience | Amazon ASI 站内人群渗透率，三季上升的人群=增长主引擎 | S20 |
| ASI | Amazon 站内数据源 | 报告中 Amazon 侧数据产品（TGI/SA/NTB 指标来源，AMC 实例 ID 780/1182/1183）`[待确认]` 具体产品名 | S20 |
| T0–T3 出价分层 | Bidding Tiers | S20 人群包出价分层：T0 核心溢价 +30~50%、T1 标准±10%、T2 前置事件 +15~25%、T3 测试 -20~-30%；**注意与 S7 T0–T5 决策树节点编号同名不同义** | S20 |
| 浅/中/深层分层 | Audience Layering | 按用户决策深度分层投放：浅层兴趣+通用词、中层行为信号+品类品牌词、深层高意向+再营销 | S17 |
| 全周期链路 | Full-lifecycle Funnel | 孕早→孕晚→产后 0-6 月→产后 6 月+ 四阶段受众策略（清洗机实例） | S17 |
| 耗材飞轮 | Consumable Flywheel | 吸奶器首单→配件（法兰/鸭嘴阀）→储奶袋订阅的复购闭环，配件自复购 4,437 人全场最高 | S20 |
| 精明品质妈妈 | — | Momcozy TikTok 归因核心人群名，投入 $517K 横跨孕→育三阶段 | S20 |
| Getting Married / Future Movers | 人生大事定向 | Meta/TikTok 人生大事事件定向，作为孕产前置触发包（T2） | S17/S20 |
| flange / flange size | 法兰/法兰尺寸 | 吸奶器罩杯尺寸，选购关键参数，Momcozy 提供 flange size calculator 工具 | S21 |
| RLSA | Remarketing Lists for Search Ads | Google 搜索再营销：对站点访客投搜索广告 | S21 |
| Lead Magnet | — | 免费留资诱饵（如待产包清单 PDF），用于邮件订阅获取 | S21 |
| UGC | User Generated Content | 用户生成内容（晒单/真实测评），Momcozy 用 #MomcozyMoments 沉淀 | S21 |
| PDP | Product Detail Page | 商品详情页，考虑阶段核心转化触点 | S21 |
| MAB | Multi-Armed Bandit | 多臂老虎机自动化测试模式，AB Test 可选裁决机制 | S18 |
| Preflight | — | 广告上线前校验：命名/标签合规、缺失项/高风险项检查 | S18 |
| accept edits on | — | Meta 广告自动调节模式：允许 AI 在选定对象上自动执行优化 | S18 |
| 人群包 | Audience Pack | 可复用受众资产：注明来源/更新时间/适用范围/排除关系/是否可模板化 | S18/S20 |
