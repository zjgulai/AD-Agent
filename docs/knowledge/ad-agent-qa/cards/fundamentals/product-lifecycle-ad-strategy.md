---
title: 产品不同阶段广告投放策略（v5 · 8 阶段完整生命周期）
doc_type: knowledge
module: ad-agent-qa
topic: product-lifecycle-ad-strategy
status: review
created: 2026-11-26
updated: 2026-11-26
owner: self
source: human+ai
source_docs: [S11]
fetched_at: 2026-11-26
---

# 产品不同阶段广告投放策略（v5 · 8 阶段完整生命周期）

## 核心问题

一个产品从测试到衰退的完整生命周期里，每个阶段投放的核心诉求、北极星指标、投放目标×出价方式、必须做的实验分别是什么？各阶段常见坑和演进规律是什么？

## 系统解答

### 1. 文档定位

HTML 可视化文档（飞书文件 `产品不同阶段的广告投放策略.html`，token `Tn5nbD3xYoliAqxhbTKc2cJ3nYg`），v5 版。覆盖 **8 阶段生命周期**：测试期→预热期→发布期→首销期→增长期→常态销售期→衰退/清仓/迭代期，外加横切所有阶段的**大促节点期**（蓄水→开门红→返场三段）。实验部分经 BLS/Incrementality/Lookalike 等专家实践交叉验证，每阶段只列 2-3 个与北极星强相关的「必须实验」。

这是**投放策略层知识**——回答「这个产品现在处于什么阶段、该用什么目标和出价方式、该做什么实验」，是 S8 案例中「系列01 Hook素材实验/系列02 出价策略实验/系列03 再营销人群实验」这类分阶段实验设计的策略依据 `[推断]`。

### 2. 八阶段投放目标与指标体系

| 阶段 | 业务核心诉求 | 北极星指标 | 投放目标 × 出价方式 | 预算心态 |
|------|--------------|------------|---------------------|----------|
| **测试期**（Soft Launch） | 小流量验证 PMF、渠道质量、素材天花板 | 留存率 Retention（D1/D7）/ 测试 CAC | App Installs/Traffic；tCPA/Max Conversion；日预算 5-10% 极小预算不冲量 | 不敢花钱 |
| **预热期**（Teasing） | 认知蓄水、预约加购、KOL 种草、品牌搜索预热 | 展示量/预约 Leads | Brand Exposure/Lead Gen/LPV/预注册；CPM/CPV/oCPM；均匀蓄水 KOL 先行 | 小钱试错 |
| **发布期**（Launch） | 集中曝光、声量引爆、下载激活、冲首发榜 | Reach + 声量份额 SOV | App Installs/Traffic/Reach；oCPM/tCPA/CPC；脉冲式集中投放（Launch Week） | 敢花钱 |
| **首销期**（First Sales） | 冲首销 GMV、首单转化、积累评价/UGC | 首销 GMV/购买次数 | Conversion/Sales/电商带货/直播引流；tROAS/oCPM 按购买优化；集中火力+再营销追未购 | 快速爬坡前夜 |
| **增长期**（Growth/Scaling） | 验证 PMF 与 ROI 后快速放量抢份额 | GMV 增速 + ROAS 守住下限 | Conversion/Sales/PMax；Max Conversion/tROAS 放宽阈值；每周翻倍测试 | 快速爬坡 |
| **常态销售期**（Sustained） | 稳定 ROAS、留存、复购、LTV 提升 | 边际利润率/MER | Sales/Conversion/PMax/复购高价值；tROAS/Value-based Bidding；持续稳定月度素材迭代 | 精算每一分钱 |
| **衰退/清仓/迭代期**（EOL） | 清库存收残值、老客迁移新品 | 剩余库存清理率/清仓净利润 ROI | Conversion 老款尾货/再营销/新品预热；tCPA/固定成本出价低预算收割；重定向为主拉新停止 | 低成本收尾 |
| **大促节点期**（横切） | 冲 GMV 峰值：蓄水→开门红→返场 | 大促 GMV/预售订单量 | Conversion/直播引流/线索；大促前 1-2 周提价抢量、当日 tROAS 控成本；脉冲分配（蓄水 20-30%/当日 40-50%/返场 20%） | 有限窗口爆破 |

各阶段核心观测指标（节选）：测试期看 CPI/留存/早期 ROAS/CTR/CVR；预热期看 Reach/频次/CPM/CTR/Hook率/完播/互动/线索 CPL；发布期看 Reach/频次/CPM/完播/Search Lift/BLS/到达率/Installs；首销期看加购/发起结账/购买 CPA/CVR/AOV/ROAS；增长期看 ROAS 下限/新客占比/CAC/CPM 变化/频次疲劳拐点/Pacing；常态期看 7/30 日 ROAS/AOV/CAC/LTV/复购/留存/Cohort/CPA/素材衰退周期；衰退期看清仓 CPA/尾货折扣率/老客迁移率/退货率/复购率。

### 3. 每阶段「必须做」实验（2-3 个/阶段）

- **测试期**：①多渠道小预算并行测试（Meta/Google/TikTok/巨量各 $50-100/天×7-14 天，比 CPI/D7 留存/早期 ROAS 找主攻阵地）②留存驱动的 PMF 验证（不同 Onboarding/落地页分流看 D1/D7 留存与 CAC，留存不达标不上量）
- **预热期**：①前 3 秒 Hook 素材测试（视觉冲击 vs 悬念 vs 痛点提问，比 CPL）②种子人群探索（相同素材跑不同兴趣包+LAL 1%，找加购/预约率最高人群）
- **发布期**：①品牌提升研究 BLS（Test vs Control 问卷测 Awareness/Ad Recall/Purchase Intent，预算 $5K+）②频控与触达效率（1天1次 vs 1天3次 vs 1周5次对 CPM/Search Lift 的影响）
- **首销期**：①出价策略 A/B（tCPA/tROAS/Max Conversion 看放量速度与达成）②落地页 CRO（50/50 分流测按钮位置/价格锚点/评价区/CTA）③再营销追投（加购未购/预约未购专属优惠）
- **增长期**：①预算爬坡测试（每 3-4 天加 20% 而非翻倍，观察 ROAS/CPA/CPM 容忍区间，跌破下限即停）②Lookalike 扩量（购买者 LAL 1%→3%→5%，种子用高 LTV 客户）
- **常态期**：①Incrementality 增量测试（Geo Holdout 选相似城市一组停投，月花 $75K+ 至少一次）②素材抗疲劳/DCO（周更 20% vs 批量换新）③拉新/再营销预算比例（基准 75-85% 拉新/15-25% 再营销，看 blended ROAS 和新客数）
- **衰退/清仓期**：①老客 Win-back 唤醒（历史购买+加购未购 8-21 天，稀缺性话术「最后几仓」，唤醒成本比新客低 5 倍）②折扣/Bundle 方案（尾货直降 vs 买老款赠新品券 vs 老新套餐——Bundle 最优解既清库存又带新品）
- **大促期**：①出价抢量策略（Bid Cap vs Max Conversion，高峰晚 6-10 点手动提价 25%）②大促素材/利益点（紧迫话术比功能话术 CTR 高约 22%）③再营销加码（BFCM 期间再营销预算+30-50%，倒计时/限时券追投）

### 4. 阶段演进规律与七大坑

**演进规律**：北极星从「留存/CAC（验证）→线索（蓄水）→Reach/SOV（声量）→GMV（首销）→GMV 增速（扩张）→MER/LTV/CAC（稳态）→清仓 ROI（收尾）」；出价方式「tCPA/Max Conversion → CPM/CPV → oCPM 浅层→深层 → 放宽 tROAS → tROAS/Value-based → 低预算固定成本收割」；实验重心「验 PMF→找 Hook→验品牌→找承接→爬坡扩量→抗疲劳算增量→老客收割」。

**七大坑**：
1. 测试期就大预算——PMF 未验证前加量=漏桶倒水
2. 预热期就背 ROAS——无转化样本模型冷启动失败
3. 发布期只看首周 CPA——品牌搜索外溢自然量被低估
4. 首销期不追再营销——浪费预热/发布期积累的便宜转化流量
5. 增长期死守 ROAS——错失抢占份额窗口，应设下限而非极致值
6. 常态期只看当日 ROAS——误杀高 LTV 低首日 ROAS 人群
7. 衰退期把老款当新品打——清仓期不应再投拉新，须老客收割+新品预热迁移，折扣不能破坏价格锚点

## 高频问答索引

- **Q：新产品投放第一阶段应该做什么？**
  A：测试期（Soft Launch）：小流量验证 PMF——多渠道小预算并行（各 $50-100/天×7-14 天）比 CPI/D7 留存/早期 ROAS 找主攻阵地；同时做留存驱动 PMF 验证（Onboarding/落地页分流看留存与 CAC），留存不达标不上量。投放目标 App Installs/Traffic，出价 tCPA/Max Conversion，日预算仅 5-10%。
- **Q：预热期和发布期的区别？投放目标一样吗？**
  A：诉求不同：预热期=认知蓄水/预约加购/KOL 种草（Brand Exposure/Lead Gen/LPV，CPM/CPV/oCPM，均匀蓄水）；发布期=集中曝光声量引爆冲首发（Reach+SOV，App Installs/Traffic/Reach，oCPM/tCPA，脉冲式集中投放）。预热期必做 Hook 素材测试+种子人群探索；发布期必做 BLS 品牌提升研究+频控测试。
- **Q：首销期怎么投？**
  A：冲首销 GMV+首单转化+积累评价 UGC：Conversion/Sales 目标，tROAS/oCPM 按购买优化，集中火力转化+再营销追未购。必做三实验：出价策略 A/B（tCPA/tROAS/Max Conversion）、落地页 CRO（50/50 分流）、再营销追投（加购未购/预约未购专属优惠）。
- **Q：增长期加预算怎么加？**
  A：每 3-4 天加 20%（不是翻倍）——翻倍会触发学习期重置。观察 ROAS/CPA/CPM 是否在容忍区间，跌破下限即停。同步做 LAL 扩量：购买者 Lookalike 1%→3%→5%，种子用高 LTV 客户而非泛访问者。
- **Q：常态期怎么判断广告是否真有效？**
  A：做 Incrementality 增量测试（Geo Holdout：选相似城市一组停投一组继续看收入差）——Retargeting 的 ROAS 容易虚高，不测增量会把「本来就会买」算成广告功劳。月花 $75K+ 至少一次。另看拉新/再营销比例（基准 75-85%/15-25%）和素材疲劳（DCO 周更 20%）。
- **Q：产品衰退/清仓期还投广告吗？**
  A：投，但逻辑完全变了：低预算收割老客——100% 预算给老客/高意向，拉新停止；老客唤醒成本比新客低 5 倍；用稀缺性话术（「最后几仓」）；Bundle 优于直降（买老款赠新品券/老新套餐——既清库存又带新品）；同步做新品预热迁移，折扣不能破坏品牌价格锚点。
- **Q：大促期（618/双11/BFCM）怎么投？**
  A：横切所有阶段，拆三段：蓄水期（预约/加购，20-30% 预算）→开门红（CVR/CPA/ROAS，40-50%）→返场（剩余库存，20%）。出价：大促前 1-2 周提价抢量、当日 tROAS 控成本；高峰晚 6-10 点手动提价 25%；再营销预算+30-50% 用倒计时/限时券追投；素材用紧迫话术（CTR 比功能话术高约 22%）。
- **Q：为什么增长期 ROAS 设「下限」而不是「目标」？**
  A：增长期核心是抢市场份额窗口——死守 ROAS 极致值会错失扩量时机。设下限（守住即可不追求极致），跌破下限即停；同时监控新客占比不下降、CPM 不因扩量飙升、频次疲劳拐点。
- **Q：这套策略和 Momcozy 的广告 Agent 有什么关系？**
  A：S8 案例的「系列01 Hook素材实验（预热/测试思路）/系列02 出价策略实验/系列03 再营销人群实验」正是按阶段×实验类型设计的投放结构 `[推断]`；Agent 做投放建议时，「产品处于哪个生命周期阶段」应是策略路由的第一维度——不同阶段北极星指标和出价方式完全不同 `[推断]`。

## 相关卡片

- [广告平台「算法自动」优化字段详解](./ad-algo-auto-fields.md) — 出价方式/预算分配/受众扩量的机制层（S9）
- [广告竞价全链路流程图](./ad-bidding-full-chain.md) — 竞价与归因机制（S10）
- [Meta 投后数据明细与巡检](../meta-ads-diagnosis/meta-post-launch-data-inspection.md) — 投后数据模板与 C01-C03 分阶段实验案例（S8）
- [Meta 诊断五层规程与配套工具](../meta-ads-diagnosis/meta-diagnosis-layers-l0-l4.md) — 单个 Campaign/素材层的诊断执行（S7）
- [广告监控与优化 Agent PRD](../architecture/monitoring-optimization-agent-prd.md) — 自动化落地的产品方案（S5）
