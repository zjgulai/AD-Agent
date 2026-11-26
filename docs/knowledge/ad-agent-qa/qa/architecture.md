---
title: Q&A 数据集 - 架构与 Agent 系统
doc_type: knowledge
module: ad-agent-qa
topic: qa-architecture
status: review
created: 2026-11-26
updated: 2026-11-26
owner: self
source: human+ai
---

# 架构与 Agent 系统 Q&A

覆盖 `cards/architecture/`（3 卡）与 `cards/influencer-boost/` 的架构部分。红人加推专项问答见 `influencer-boost.md`。

### Q1. Momcozy 广告 Agent 体系一共有几个 Loop？分别是什么？
**A**：双引擎 OCR 可辨 10 个 Loop：广告市场机会发现、竞品广告策略洞察、新品广告冷启动、广告创意生产与测试、广告投放策略制定、广告投放执行、广告异常诊断与恢复（Tesseract 新发现）、广告增长优化、广告复盘与知识进化、红人素材广告加推。Loop 原始编号与精确计数因画板 OCR 无法完全还原，个别节点名标 `[待确认]`。
> 溯源：`cards/architecture/ad-agent-system-landscape.md`

### Q2. 这套广告 Agent 体系的顶层目标是什么？
**A**：持续自动发现「产品×人群×市场×渠道×卖点」的广告增长机会，并形成可执行的投放机会——即从机会发现一路闭环到投放、优化、复盘沉淀，而不是单点工具。
> 溯源：`cards/architecture/ad-agent-system-landscape.md`

### Q3. 广告 Agent 大致分几类？
**A**：按职能分六类——机会发现类（Trend/Consumer/Competitor/Opportunity/Strategy Agent）、策略制定类（渠道/投放策略/预算/创建/账户治理/素材组装）、创意类（创意洞察/素材优化）、执行类（Campaign Planning→Monitoring 链路）、优化类（异常监控/机会发现/出价预算/Search Term/受众/Campaign 结构/广告优化）、复盘沉淀类（广告复盘/知识沉淀）。
> 溯源：`cards/architecture/ad-agent-system-landscape.md`

### Q4. 广告 Agent 哪些环节必须人工确认？
**A**：四处——① 市场/广告负责人确认广告机会；② 投放负责人确认「已审批广告策略」后才创建 Campaign；③ 创建链路中 AI 生成方案后人工确认再 API 落地；④ 高风险调整人工确认（优化域三级自动化：建议→确认→安全规则内自动）。
> 溯源：`cards/architecture/ad-agent-system-landscape.md`

### Q5. 广告创建怎么从「人工逐项配置」变自动？
**A**：画板对比的链路是：从人工打开 Meta/Google 后台逐项配置 → 自然语言需求 → AI 生成 Campaign 配置 → 人工确认 → API 自动创建 → 自动校验（命名/Tracking/预算/参数）。
> 溯源：`cards/architecture/ad-agent-system-landscape.md`

### Q6. 广告创意怎么持续变好？
**A**：Loop 4 的创意增长飞轮：创意洞察沉淀方法论 → 素材优化识别衰退并生成下一轮创意方向 → CMS 生成新素材 → A/B 测试 → 识别赢家 → 变体生成，循环迭代。
> 溯源：`cards/architecture/ad-agent-system-landscape.md`

### Q7. 投放经验怎么沉淀和复用？
**A**：Loop 9 广告知识沉淀 Agent 把每次投放的策略/素材/产品/人群/渠道/结果/复盘结论结构化进广告知识库，建立「产品×人群×渠道×创意×策略×效果」关系；新建广告时自动检索相似成功案例反哺策略 Agent。
> 溯源：`cards/architecture/ad-agent-system-landscape.md`

### Q8. 素材组装 Agent 建了吗？
**A**：两处口径不一致。S1 画板将其列为策略制定环节节点（CMS 素材智能组合+多变体批量上架）；但 S2/S3 红人加推建设任务中明确「暂不建设，直接使用红人原视频授权加推」。红人加推域的素材组装（⑤）也明确暂不建设、Demo 灰显标注「下一阶段建设」。两处冲突待业务确认，引用时应并列呈现。
> 溯源：`cards/architecture/ad-agent-system-landscape.md` + `cards/influencer-boost/influencer-boost-loop-overview.md`；冲突见 `CONFLICTS.md`

### Q9. Meta 监控优化 Agent 一期到底做什么？不做什么？
**A**：一期是面向 Meta 投放团队的自动化操作员——按 S4 策略树（65 节点/196 分支）自动巡检账户→系列→广告组→创意全量对象，异常变成带根因和处置建议的飞书预警，在安全边界内直接完成调整（白名单低风险动作），并把每次决策连同 4h/24h/72h 复核结果留痕。不做：仅覆盖 Meta；不做动态基线；合规域一期仅提示不处置；素材轮换本期不做；LLM 只做 L1–L3 文案/排序/周审计，L4 习惯学习与 L5 自然语言交互是二期；Google/TikTok 仅留数据层口。
> 溯源：`cards/architecture/monitoring-optimization-agent-prd.md`

### Q10. 监控 Agent 会不会乱动广告账户？防呆机制有哪些？
**A**：五层防线——① 规则引擎判断不靠 LLM，且有两道保护期闸门（冷启动 <24h、归因成熟度 <80% 只监控不判效不动作）；② G8 执行前安全检查四项（近 12h 人工变更/大促窗口/冷却期/回滚条件缺失）+ 执行器二次检查（幅度截断、熔断转人工、快照缺失禁执行）；③ 四维熔断（动作数量/资金消耗/预算设置/技术接口）；④ 动作前快照 + 21 字段日志 + 自动回滚；⑤ 三档权限默认观察模式，自动模式默认关闭、白名单仅 5 个低风险动作且按账户开启。
> 溯源：`cards/architecture/monitoring-optimization-agent-prd.md`

### Q11. LLM 在监控系统里干什么？会不会幻觉出错误建议？
**A**：LLM 只做四件规则引擎做不了的事：预警叙事（LLM-1）、候选根因集内排序解释（LLM-2）、周度审计聚合（LLM-3）、二期习惯学习。护栏：只在候选集内工作不产生规则外动作；数字与对象名必须原样来自输入并做字段级校验，不过则降级模板文案；不覆盖规则优先级、不跳过 G8；三级失败降级，规则诊断链任何情况下独立可运行。
> 溯源：`cards/architecture/monitoring-optimization-agent-prd.md`

### Q12. 告警怎么分级？怎么防止卡片轰炸投手？
**A**：P0（14 条分支）紧急级飞书卡片+电话/群升级 ≤30 分钟；P1（55 条）高危飞书卡片 ≤2 小时；P2（62 条）+趋势类进工作台聚合+每日摘要。五段式卡片（异常/证据/根因/动作/影响预估）。去重靠冷却期（默认 24h 可配）；同周期同根因 ≥10 条聚合为一张批量异常卡；提案卡片 2 小时超时自动失效不执行 `[待确认]`。
> 溯源：`cards/architecture/monitoring-optimization-agent-prd.md`

### Q13. 新上线的广告、学习期对象会不会被误杀？
**A**：不会——两道引擎级前置闸门：新建对象冷启动保护期（上线 <24h 或消耗未达 1 倍目标转化成本当量，只监控不动作）与归因延迟缓冲期（成熟度 <80% 禁止判断 CPA/ROAS，只诊断流量成本侧）；另有铁律「学习期不判效」「样本不足仅监控预约复测」。保护期状态写回日志并在工作台展示。
> 溯源：`cards/architecture/monitoring-optimization-agent-prd.md`

### Q14. Agent 执行动作之后怎么验证有效？失败怎么办？
**A**：执行即写 21 字段动作日志并创建 4h/24h/72h 三个复核任务自动回填。复核判定：CPA +≥20% 或 ROAS -≥20% 或延迟 >6h → 自动回滚到动作前快照 + 升级 P0 告警；+10%~20% 区间 → 待观察禁止追加；达标 → 闭环沉淀为正样本。建议熔断：7 天内 ≥2 次回滚自动降级观察模式 `[待确认]`。
> 溯源：`cards/architecture/monitoring-optimization-agent-prd.md`

### Q15. Agent 一期什么时候上线？排期怎么安排？
**A**：M0–M5 共约 11 周：M0 规则确认与决策拍板 → M1 十个数据域接入+限流治理 → M2 巡检预警（观察+确认模式）→ M3 执行闭环（白名单自动模式默认关+周审计）→ M4 阈值校准+4 周试运行验收 → M5 二期立项评估。上线走灰度：1 账户观察 2 周 → 确认模式 → 1 账户自动模式。试点建议 1 个 Meta 账户起步 `[待确认]`。
> 溯源：`cards/architecture/monitoring-optimization-agent-prd.md`

### Q16. Momcozy 做广告 Agent 前的业务调研怎么组织？
**A**：两层——S14 总容器先定调研输入（核心玩法会议纪要、老板方向规划、最新讨论纪要），再按「广告投放作业流程」梳理 MP/非 MP × 海外/国内四象限场景；S16 用 33 列矩阵逐场景填「角色→作业项→输入/输出规范→频率/人力成本→AI 可替代性→优先级」。
> 溯源：`cards/architecture/ad-ops-agent-research-framework.md`

### Q17. 33 列矩阵的 AI 评估维度是什么？
**A**：Ai 提效方式三档（完全替代/部分替代/无法替代）+ AI 可用性预估 + 环节优先级；前置度量含作业频率、日作业量、单作业耗时、人力/非人力成本、经营收入。
> 溯源：`cards/architecture/ad-ops-agent-research-framework.md`

### Q18. 业务调研做完了吗？
**A**：没有。S14 止于「调研细化材料」空标题，S16 矩阵零数据行；且 5 篇关键引用（会议纪要×3、wiki×2）无权限，作业全貌仅能从流程图还原 `[待确认]`。
> 溯源：`cards/architecture/ad-ops-agent-research-framework.md`

### Q19. 这份架构知识库讲的 Agent 和已建成的投放 SOP 是什么关系？
**A**：`[推断]`：S6/S7 是 Meta 投放师单环节的已落地 SOP（细节样本）；S14/S16 是全业务 Agent 立项的方法论框架——前者证明「单点能做」，后者决定「先做哪一点」。S1 全景画板是目标架构蓝图（10 Loop），S5 PRD 是其中 Meta 监控优化域的一期落地。
> 溯源：`cards/architecture/ad-ops-agent-research-framework.md` + `cards/architecture/ad-agent-system-landscape.md`
