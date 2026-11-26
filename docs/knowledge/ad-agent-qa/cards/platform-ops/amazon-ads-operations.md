---
title: Amazon 广告运营打法（Campaign 架构 + 预算分配 + 周复盘 SOP + 出价规则）
doc_type: knowledge
module: ad-agent-qa
topic: amazon-ads-operations
status: review
created: 2026-11-26
updated: 2026-11-26
owner: self
source: human+ai
source_docs: [CBE:amazon-ad-architecture, CBE:amazon-ad-diagnosis, CBE:amazon-weekly-ad-review]
fetched_at: 2026-11-26
---

# Amazon 广告运营打法（Campaign 架构 + 预算分配 + 周复盘 SOP + 出价规则）

## 核心问题

Amazon PPC 从零搭架构怎么分 Campaign？日预算怎么分配？出价表怎么定？每周复盘看什么、怎么调？Prompts 广告这类被动扣费项怎么管？周调不动了说明什么？

## 系统解答

### 1. 文档定位

蒸馏自 S22 cross-border-ecommerce-skills 的 Amazon 广告三件套（ad-architecture / ad-diagnosis / weekly-ad-review）。**与 `amazon-ads-playbook.md` 的分工**：那张卡讲机制层（ACoS/TACoS、诊断顺序、否定词三层、SB/SP 分工、readiness）；本卡讲**运营执行层**——架构树、预算%、出价表、周复盘动作清单。

### 2. 广告类型速查（2025-2026）

| 类型 | 特点 | 适用 |
|------|------|------|
| SP（Sponsored Products） | 关键词/ASIN 定向，搜索结果页 | **核心出单，新品必开** |
| SB（Sponsored Brands） | 品牌旗舰店引流，搜索顶部；视频是 SB 格式非独立类型 | 品牌词防御+品牌曝光 |
| SD（Sponsored Display） | 受众/ASIN 定向，站内外 | 竞品拦截+再营销 |
| Performance+/Brand+ | 仅 Amazon DSP 内 | 程序化再营销/品牌拉新（DSP 侧） |
| Alexa+ Agentic Ads | 2026-06 上线，Echo Show 对话内成交，非自助投放 | 观察项，无自助入口 |

### 3. Campaign 架构（新品期 Month 1-2）

```
[品牌]-[产品]-/
├── SP-Auto/            # 自动广告=数据挖掘，2 周后按数据调整
│   ├── Close Match（紧密）/ Loose Match（宽泛）
│   ├── Substitutes（同类商品）/ Complements（关联商品）
├── SP-Manual-Exact/    # 手动精准=核心出单：Tier1-Core + Tier3-LongTail
├── SP-Manual-Broad/    # 手动宽泛=拓流量：Tier2-Expansion
├── SP-ASIN-Targeting/  # 竞品定向：Competitor-ASIN + Complementary
└── SD-Retargeting/     # 再营销：Viewed-Not-Purchased
```

**Month 3+ 追加**：SB-Brand（品牌词防御）、SBV-Video（核心词视频）、SD-Competitor（竞品页拦截）。

### 4. 预算分配与阶段目标

**新品期日预算占比**：SP-Auto 20% / SP-Exact 35% / SP-Broad 20% / SP-ASIN 15% / SD-Retarget 10%。

**阶段目标**（社区经验基准，非官方）：

| 阶段 | 目标 ACoS | 目标 TACoS |
|------|----------|-----------|
| 新品期 M1-2 | 30-40% | 15-25% |
| 成长期 M3-6 | 20-30% | 10-15% |
| 稳定期 M6+ | 15-25% | 8-12% |

**预算合理性红线**：稳定期日预算 ≤ 日均毛利 50%；新品期可放宽至 80-100%（广告换排名冷启动），但必须设降本时间节点。

**命名规则**：`[品牌]-[产品简称]-[广告类型]-[匹配类型]-[日期]`。

### 5. 出价策略表

| 匹配类型 | 起始出价 | 调整 |
|---------|---------|------|
| Exact | 建议 CPC 的 80-100% | 14 天数据后 ACoS<目标→加价 10-20% |
| Phrase | 60-80% | 表现好的词提取到 Exact |
| Broad | 50-70% | 主要用于发现新词 |
| Auto | 系统建议价 | 2 周后分析 STR |
| ASIN Targeting | $0.50-1.00 起 | 按竞品价位调 |
| 规则竞价/Audience Bid Boost | 交给系统 | 规则竞价需 30 天+30 转化；ABB 自 2025-04 可用 |

> 🔑 **auto/broad campaign 保持开启且预算充足**——这是进入 Prompts 对话广告与语义匹配流量的入口，预算不足直接错过该曝光。

**Placement 加成**（最高 +900%）：Top of Search 转化最高 CPC 最贵→核心出单组重点加成；Product Pages→竞品定向组适度加成；先跑 Placement Report 按版位拆 ACoS 再定比例。

### 6. 每周复盘 SOP（loop，每周一次）

**核心指标健康范围**（Amazon 口径，与 Meta 不同勿混用）：ACoS 15-30% / TACoS 8-15% / **CTR>0.4%**（<0.3% 优化文案图）/ **CVR>10%**（<8% 优化 Listing）/ ROAS>3.0。

**数据概览**：本周 vs 上周 vs 月均全指标环比。**关键判断**：TACoS 降+自然单占比升=健康增长；TACoS 升+自然占比降=过度依赖广告。

**Campaign 红绿灯**：绿（ACoS<目标）保持可小幅加预算；黄（ACoS 为目标 100-150%）分析 STR+否定无效词+调价；红（ACoS>目标 150% 或 14 天无转化）降价 20% 或暂停。

**Search Term Report 收割**：高转化新词→提 Exact；高花费 0 转化→否定词库；高展示低 CTR→文案/图与搜索意图不匹配；竞品 ASIN 高转化→ASIN Targeting。

**出价/预算调整表**：ACoS 远低于目标+销量稳→出价+10-20%/预算+20%；略低→+5-10%；略高→-5-10%；远高→-20% 或暂停/预算-30%；展示量骤降→出价+15-25%。

**SB/SD 最小检查**：SB 看 SKU 级 new-to-brand%（2026 起细化到 SKU）+品牌词防御 CPC 溢价；SD 看受众定向 vs 上下文定向的花费/转化拆分。

**Prompts 广告必查**（被动扣费项）：美国 SP/SB campaign 自 2026-03-25 GA 起 CPC 计费、自动注册（authors/publishers 除外）、沿用父 campaign 竞价无独立出价、文案 AI 自动生成。必须纳入预算与周检单列。报表：Ads Console→Reports→Prompts。

**竞争扫描**（每周）：竞品价格变动/新 ASIN 入场首页/大促 Coupon/Alexa for Shopping AI overview 是否推荐竞品。

**行动清单**：P0 立即 / P1 本周内 / P2 下周规划。

### 7. 出价调整规则速查

| 条件 | 动作 |
|------|------|
| ACoS<目标 且销量稳定 | 加价 10-20% |
| ACoS>目标 150% | 降价 20% 或暂停 |
| 14 天无转化 | 暂停该词 |
| STR 出现新高转化词 | 提取到 Exact Campaign |
| STR 出现无关词 | 加入否定词库 |

### 8. 冷启动与扩量规则

- 新账户冷启动：Day1-3 装像素预热（$0）→ Day4-14 投 Traffic/Engagement 攒数据（$20-50/天）→ Day15-30 切转化目标（$30-100/天）→ Day31+ 扩量。**新像素前 100 事件决定机器学习方向；前 14 天不频繁调整；日预算 ≥ 目标 CPA 5 倍**。
- 扩量：预算每次增幅 ≤20%、间隔 ≥3 天（避免重置学习）；Lookalike 1%→3%→5% 逐级扩；时段向高转化倾斜。

### 9. 结构性问题识别

**周调不动→升级诊断**：品牌词 CPC 持续升但搜索量不增=单渠道天花板（需品牌建设非调价）；ACoS>盈亏平衡线持续 30 天+=结构性亏损；TACoS>25%=过度依赖广告。周复盘只做战术优化，结构问题转 `amazon-ad-diagnosis` 式深度诊断（市场/词库/Listing/广告四位一体）。

### 10. 时效事实（as of 2026-11）

- Prompts 广告：2026-03-25 美国 GA+CPC 计费，自动注册被动扣费；唯一官方表现数字≈20% 交互者继续该品牌对话（Q1 2026 电话会）。
- AMC 自助开通：2025-09-16 起 sponsored ads 主可在 Ads Console 自助开通（34 国，本体免费）；**2026-06-02→12-31** Amazon Retail Purchases+Audience Segment Insights 限时免费。
- 归因窗口：**SP 7 天、SB/SD 14 天**——本周数据下周可能补充，重大决策等窗口闭合。
- 广告方法论归属：奇赞大课 Sukey（平台选择）+Ada（天花板识别）+宋靖Mirror（AIPL/Google 类型优先级）等，详见 `raw/s22-cbe-skills/` 原文。

## 高频问答索引

- **Q：Amazon 新品广告架构怎么搭？**
  A：SP-Auto（数据挖掘 20%）+SP-Exact（核心出单 35%）+SP-Broad（拓流量 20%）+SP-ASIN（竞品定向 15%）+SD-Retarget（10%）；Month3+ 加 SB-Brand/SBV/SD-Compete。
- **Q：Amazon 广告出价怎么定？**
  A：Exact=建议CPC 80-100%、Phrase 60-80%、Broad 50-70%、Auto 系统价、ASIN 定向 $0.50-1 起。14 天数据后按 ACoS 调：优→+10-20%，差→-20%或暂停。
- **Q：Amazon 每周广告复盘看什么？**
  A：本周vs上周vs月均 KPI（ACoS/TACoS/CTR/CVR/CPC）→Campaign 红绿灯→STR 收割（新词提 Exact/烂词否定）→出价预算调整→SB new-to-brand+SD 受众拆分→Prompts 被动扣费单列→竞品扫描→P0/P1/P2 清单。
- **Q：TACoS 多少算健康？**
  A：健康 8-15%（视阶段），>25% 过度依赖广告需提升自然位/品牌建设。周复盘关键判断：TACoS降+自然单升=健康；TACoS升+自然占比降=广告依赖加深。
- **Q：Amazon 广告 CTR/CVR 健康线是多少？**
  A：Amazon 口径 CTR>0.4%（<0.3% 优化文案图）、CVR>10%（<8% 优化 Listing）——与 Meta 口径不同勿混用。
- **Q：冷启动账户前 14 天能频繁调吗？**
  A：不能。新像素前 100 事件决定机器学习方向；日预算≥目标CPA 5 倍；Day4-14 先投 Traffic/Engagement 攒数据再切 Purchase；前 14 天不动。
- **Q：Prompts 广告会偷偷花钱吗？**
  A：会。2026-03-25 起美国 SP/SB 自动注册、沿用父 campaign 竞价 CPC 计费、无独立出价——预算已在 AI 对话位花钱，必须纳入预算与周检（Ads Console→Reports→Prompts）。
- **Q：周复盘调了还是不行说明什么？**
  A：结构性问题——品牌词CPC升+搜索量不增=单渠道天花板；ACoS>盈亏线持续30天=结构性亏损；TACoS>25%=广告依赖。转深度诊断（市场/词库/Listing/广告四位一体），不再周调。

## 相关卡片

- [Amazon 广告打法](amazon-ads-playbook.md) — 机制层姊妹卡（ACoS/TACoS/诊断顺序/否定词三层/SB-SP 分工）
- [Amazon 关键词与 Listing 运营](amazon-keyword-listing-ops.md) — 词库/埋词/否定词库姊妹卡
- [独立站 SEM 广告打法](dsite-sem-ads-playbook.md) — Google/Meta 侧对照
- 知识图谱：S22 分片 `ad:adproduct:amazon-*` / `ad:metric:amazon-*`（待抽取）
