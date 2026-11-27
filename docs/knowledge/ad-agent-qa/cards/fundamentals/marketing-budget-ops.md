---
title: 年度营销预算系统 · 总额三法、科目分配、月度权重、ROI 漏斗与再平衡规则
doc_type: knowledge
module: ad-agent-qa
topic: marketing-budget-ops
status: review
created: 2026-11-27
updated: 2026-11-27
owner: self
source: human+ai
source_docs: [CBE:brand-budget-ops, S27]
fetched_at: 2026-11-27
---

# 年度营销预算系统 · 总额三法、科目分配、月度权重、ROI 漏斗与再平衡规则

## 核心问题

年度营销预算总额怎么定？广告/PR/KOL/内容各分多少？月度怎么排峰值？渠道间怎么再平衡？这个数字该不该继续加？本卡蒸馏 CBE `brand-budget-ops`（645 行）+ S27 `ecommerce-marketing-strategy-builder` 的预算/ROI 基准表——**预算编制层**：位于 payback 闸门（channel 级能不能投）之上、campaign 日预算（单计划多少）之下的中间层。

## 系统解答

### 1. 来源与口径

- **来源**：`raw/s22-cbe-skills/brand-strategy/brand-budget-ops.md`（CC BY-NC）+ `raw/s27-ecommerce-skills/` 中 `ecommerce-marketing-strategy-builder` 的渠道 ROI 基准与 KPI 表（MIT）。
- **定位**：S25 payback 卡回答「单个渠道/计划可不可投」（LTV:CAC、毛利回本），本卡回答「一年总盘子怎么切」。两者衔接：科目分配 → 渠道预算 → payback gate 逐层下钻。

### 2. 三层预算科目体系

一级科目 10 类（占比为 Y1 参考区间）：**媒介广告 AD 30-45%**（二级展开：Amazon/Google/Meta/TikTok/KOL 等，各含 CPC/CPM/CPA）/ **PR 公关 8-15%** / **内容营销 RS 10-18%** / **设计制作 DG 5-10%** / **KOL 达人 15-25%**（分层：头部 1-3 人 / 腰部 5-15 人 / 尾部 20-50 人）/ **展会 EX 5-10%**（CES/AMAZON 等）/ **私域运营 SP 3-8%** / **工具 TL 2-5%**（SaaS/订阅）/ **人力 HR 8-15%**（项目制/工资+绩效）/ **调研 RS 2-5%**（VOC/市场调研）。

**结构健康度检查**：获客类（AD+KOL）占比 50-65%（早期可 70%+）；品牌建设类（PR+RS+DG+EX）15-25%；**CAC:LTV 比必须 <1:3**，超出则砍获客加品牌。

### 3. 总额确定三法

| 方法 | 公式/逻辑 | 适用 |
|---|---|---|
| 营收占比法 | 营销预算=营收×占比。Y1 25-40% / Y2-3 18-25% / Y4+ 12-18%（S27 基准交叉验证：新品牌 15-20%、早期 10-15%、成长期 7-12%、成熟期 5-8% of revenue——CBE 口径偏保守属「全营销投入」含非付费，S27 是「paid media only」口径，两者差异即品牌/内容预算部分） | 有营收基数的品牌 |
| 目标倒推法 | 目标营收÷目标转化率×目标 CPA+固定成本 | 无营收历史/新品类 |
| 竞品对标法 | Similarweb/Ahrefs 查竞品广告强度+行业报告 | 市场成熟期 |

**盈亏平衡 ROAS = 1/毛利率**；目标 ROAS = breakeven×(1+净利率/毛利率)。例：毛利率 40%→breakeven ROAS 2.5，净利率目标 10%→目标 ROAS ≈3.1。与 S26 Amazon ACoS 公式（target = break-even−利润目标）同族不同口径，注意别混用。

### 4. 月度权重与现金流规则

**Q4 集中是铁律**：参考月度权重——1月 6% / 2月 5% / 3月 6% / 4月 6% / 5月 6% / 6月 7% / 7月 10%（Prime Day）/ 8月 7% / 9月 8% / 10月 8% / **11月 14% / 12月 13%**（黑五+圣诞=Q4 占 27%）。**S27 阶段-渠道优先矩阵**：launch=Meta 40%/TikTok 25%/Google 20%/Email 15%；growing=Meta 30%/Google 25%/TikTok 20%/Email 15%/SEO 10%；established 加 Amazon/PR 分流。

**现金流三规则**：月末现金储备 ≥ 下月预算 120%；大促（BFCM/Prime Day）预算提前 2 月充值进广告账户；KOL 付款 50-50（上线一半/数据达标一半）。

### 5. 渠道预算明细表（Y1 参考）

| 渠道 | 预算占比 | 预期 ACoS/ROAS | 核心指标 |
|---|---|---|---|
| Amazon SP | 15-20% | ACoS 25-40% | TACoS<10% |
| Google Search/PMax | 10-15% | ROAS 3-5 | 品牌词占比 |
| Meta | 15-25% | ROAS 2-4 | CPA vs LTV |
| TikTok | 10-20% | ROAS 1.5-3 | GMV Max 效率 |
| KOL/达人 | 10-15% | 间接 | 曝光 CPM/内容产出 |
| EDM/SMS | 3-5% | ROI $36-40/$1（S27） | 打开/点击/收入占比 |

### 6. S27 渠道 ROI 基准（$/1 spend）

Email $36-40 / SMS $21-71 / SEO $7.48 / Google $8 / Paid Social（Meta+TikTok）$2.5。**S27 KPI 基准**：LTV>3×CAC、复购率 28%+、email 收入占比 25-30%、blended ROAS 2.5×+。这些是全漏斗归因口径——直接对比各渠道「表观 ROAS」会误判（Meta 表观 $2.5 但引流后 EDM/自然搜索承接贡献被低估），**应结合 payback 卡的 cohort 口径使用**。

### 7. ROI 监控与再平衡

**24 指标 ROI 漏斗六层**：认知（曝光/CPM/触达）→ 兴趣（CTR/视频完播）→ 考虑（加购/收藏/评论）→ 转化（CVR/CPA/订单）→ 留存（复购/LTV/留存率）→ 效率（ROAS/ACoS/利润率）。每层 3-5 指标。

**差异预警三级**：红=偏差>20% 立即复盘 / 橙=10-20% 本周内调 / 黄=5-10% 观察。**再分配规则**：单渠道预算调整上限 ±20%（超出需季度评审）；连续 2 月达标→+20%，连续 2 月不达标→−20%。

**渠道天花板 5 信号**（任一命中考虑转移预算）：CPM 连涨 3 周+/转化率持续下降/受众饱和（频次>3）/竞品入场 CPO 上涨/边际 ROAS 跌破基准 50%。

**季度再平衡模板**：实际 vs 预算差异 → RYG 标色 → 超支砍/缺口补 → 下季分配调整 → 沉淀为新基准。多币种场景：统一折算 USD 记账，汇率波动>5% 单独披露。

## 高频问答索引

- **Q：营销预算占营收多少？** A：CBE 口径全营销 Y1 25-40%/Y4+ 12-18%；S27 paid-media-only 口径 15-20%（新）→5-8%（成熟）。差值≈品牌/内容/PR 预算，两者互补不冲突。
- **Q：盈亏平衡 ROAS 怎么算？** A：=1/毛利率。毛利率 40%→2.5；目标 ROAS=breakeven×(1+净利率/毛利率)，净利率 10%→≈3.1。别和 Amazon ACoS 公式混。
- **Q：月度预算怎么分？** A：Q4 占 27%（11月 14%+12月 13%），7 月 Prime Day 10%，其余均摊——BFCM/Prime Day 前 2 月提前充值。
- **Q：渠道 ROAS 表观差异大怎么办？** A：$36-40 email vs $2.5 social 是全漏斗 vs 直接归因口径差异，结合 cohort/payback 卡判断真实贡献，别只看表观。
- **Q：单渠道能加多少钱？** A：月度调整 ±20% 上限，连续 2 月达标才 +20%；天花板信号命中（CPM 连涨/频次>3/边际 ROAS 腰斩）即转移。

## 相关卡片

- 溯源卡：[Payback 预算闸门](payback-period-budget-gate.md)（下游：科目→渠道→计划逐层下钻）、[生命周期留存](../business-context/user-lifecycle-retention-ops.md)（SP 私域科目的承接）、[出海扩张框架](../business-context/cross-border-expansion-framework.md)（市场侧预算）、[GEO 优化](../platform-ops/geo-ai-search-optimization.md)（内容预算新投向）
- 上游 raw：`raw/s22-cbe-skills/brand-strategy/brand-budget-ops.md`（CC BY-NC）、`raw/s27-ecommerce-skills/`（MIT）
