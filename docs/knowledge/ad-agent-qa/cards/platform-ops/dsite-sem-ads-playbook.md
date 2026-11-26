---
title: 独立站 SEM 广告打法（平台选择 + Google 账户架构 + AIPL 漏斗 + 优化节奏）
doc_type: knowledge
module: ad-agent-qa
topic: dsite-sem-ads-playbook
status: review
created: 2026-11-26
updated: 2026-11-26
owner: self
source: human+ai
source_docs: [CBE:dsite-sem-ads]
fetched_at: 2026-11-26
---

# 独立站 SEM 广告打法（平台选择 + Google 账户架构 + AIPL 漏斗 + 优化节奏）

## 核心问题

独立站投广告先选哪个平台？Google Ads 账户怎么搭？AIPL 漏斗预算怎么分？冷启动怎么过学习期？大促 SEM 怎么打？SEM 和 SEO 怎么协同？LTV 口径下 CPA 承受线怎么算？

## 系统解答

### 1. 文档定位

蒸馏自 S22 `dsite-sem-ads`（独立站 SEM 与广告投放全流程）。**填补 KB 的 Google/DTC 域空白**——现有诊断体系是 Meta 转化漏斗模型，本卡是独立站多平台 SEM 操作层。方法论归属：宋靖Mirror（AIPL/数据金字塔/视频结构）、朱峰April（大促 SEM）、张子轩（SEO-SEM 协同/PMF）、Sukey（平台选择）。

### 2. 平台选择矩阵（10 平台速查）

| 平台 | 流量特征 | 最低预算 | 反馈周期 | 最适产品 |
|------|---------|---------|---------|---------|
| Meta | 兴趣+行为定向 | $20/天 | 1-2 天 | 视觉型/冲动消费/DTC |
| Google Search | 搜索意图 | $30/天 | 7-15 天 | 已有品类认知产品 |
| Google Shopping | 产品比价 | $20/天 | 7-15 天 | 标品/有价格竞争力 |
| Google Pmax | AI 全渠道 | $50/天 | 14-30 天 | 有足够转化数据的账户 |
| TikTok Ads | 内容驱动 | $20/天 | 1-3 天 | 视觉冲击/新奇/低客单 |
| YouTube | 视频+意图 | $30/天 | 7-14 天 | 需教育/展示的产品 |
| Pinterest | 灵感发现 | $15/天 | 7-14 天 | 家居/时尚/美妆/婚礼 |
| Reddit | 社区+兴趣 | $10/天 | 3-7 天 | 科技/游戏/小众品类 |
| LINE | 日本本土 | ¥5,000/天 | 3-7 天 | 日本市场必投 |
| Snapchat | AR+视觉 | $20/天 | 1-3 天 | Z 世代/AR 产品 |

**按产品选平台**：视觉型→Meta→Pinterest→TikTok；功能型→Google Search→YouTube→Meta；冲动消费($10-50)→TikTok→Meta；高客单($100+)→Google Search→Meta；标品→Google Shopping；小众新品类→Meta→TikTok→Reddit；日本→LINE→Google JP→Meta。

**按预算分配**：$1-3k/月→1 平台集中；$3-10k→主 70%+辅 30%；$10-30k→主 50%+辅 30%+测试 20%；$30k+→全渠道按 ROAS 动态分配。

### 3. 账户架构

**Google Ads（6 Campaign）**：①Brand Search（品牌词防御）②Non-Brand Search（品类词/问题词/竞品词三 Ad Group）③Shopping（Best Sellers/New Arrivals/Sale）④Performance Max（全漏斗自动化，有数据后上）⑤Display Remarketing（Cart Abandoners 1-3d / Product Viewers 4-14d / Past Customers 15-30d）⑥YouTube（Awareness In-stream / Consideration Discovery）。

**Meta Ads（5 Campaign）**：Prospecting-TOF（Broad/Interest/Lookalike Purchase 1%）→ Prospecting-MOF（Lookalike ATC 1-3%/PV 1-3%）→ Retargeting-BOF（Cart 1-7d/Product Viewers 1-14d/Engagers 1-30d）→ Retention（Past Customers 30-90d/Email List LL）→ Testing（素材 A/B/C）。

**TikTok Ads（4 Campaign）**：Spark Ads（原生内容加热）/ Prospecting（Broad/Interest/LL Purchase）/ Retargeting（Video Viewers/Website Visitors）/ Testing（Hook/Offer）。

### 4. AIPL 漏斗与预算模型

| 阶段 | 目标 | 关键指标 |
|------|------|---------|
| A Awareness | 触达建认知 | CPM/Reach/Frequency |
| I Interest | 激发兴趣 | CTR/Video View/Engagement |
| P Purchase | 促成转化 | CVR/CPA/ROAS |
| L Loyalty | 复购提 LTV | Repeat Rate/LTV |

**新品牌预算分配**：A 15-20% / I 20-25% / **P 45-55%** / L 5-10%。
**按成熟度**：冷启动 M1-3（A25/I25/P45/L5，预算 $3-10k/月）→ 增长期 M4-8（20/20/50/10，$10-30k）→ 成熟期 M9+（15/15/55/15，$30k+）。
**Google 广告类型×漏斗**（优先级）：Search(P,30-40%) > Shopping(P,20-30%) > Display(A/I,10-15%) > Video(A/I,5-10%) > Demand Gen(A,5-10%) > Pmax(全漏斗,10-20%)。

### 5. 冷启动 SOP（新账户学习期）

| 阶段 | 时间 | 日预算 | 动作 |
|------|------|--------|------|
| 像素预热 | Day1-3 | $0 | 装像素+全事件追踪 |
| 数据积累 | Day4-14 | $20-50 | 投 Traffic/Engagement 攒 LPV/ATC |
| 转化测试 | Day15-30 | $30-100 | 切 Purchase 优化 |
| 扩量 | Day31+ | 渐增 | 每次≤20%、间隔≥3 天 |

**关键规则**：新像素前 100 事件定学习方向；先优化 ATC 再切 Purchase；日预算≥目标 CPA 5 倍；前 14 天不频繁调整。

### 6. 关键词策略

**五步流程**：种子词 3-5 个 → Keyword Planner 扩 200-500 变体 → 筛月搜索量≥100 → 竞争度排序 → 意图分类 → 否定词。
**四大免费来源**：Google Autocomplete / Search Terms Report / Search Console / Trends。
**分层出价**：品牌词（最高，防守）> 高意图产品词 buy/best/price（高）> 品类通用词（中）> 问题教育词 how to（低，SEO 优先）> 竞品词（中，谨慎）。
**否定词四类**：行业通用（free/DIY/job）/不相关品牌/低意图（review/reddit）/STR 发现（每周更新）。

### 7. 素材体系与测试

**文案公式**：PAS（痛点-激化-方案）/ BAB（前-后-桥）/ AIDA / 4U（限时+独特+具体+价值）/ Star-Story-Solution。
**Google RSA 模板**：H1 核心卖点/H2 信任信号/H3 CTA（各≤30 字符）+ D1 详细卖点+社会证明/D2 保障+CTA（各≤90 字符）。
**视频结构 0-30s**：0-3s Hook（问题/冲突/惊讶/数据）→3-10s 痛点共鸣→10-20s 产品演示→20-25s 证明（评价/数据/认证）→25-30s CTA。
**素材测试（变量隔离）**：每次只测 1 变量；每变体≥1000 曝光或 100 点击；95% 置信度；获胜即扩量失败即停；每周上新 2-3 个变体。

### 8. 数据金字塔诊断

```
ROAS ← Conversions ← CTR/CVR ← CPC/CPA ← Impressions/CPM
```

健康范围：CTR>1%（搜索>3%）、CVR>1%、ROAS>2x（按利润率校准）。
**决策树**：ROAS 低→CTR 低？曝光足→换素材；曝光不足→预算/出价/受众。CTR 正常 CVR 低→查跳出率（页面）→加购率（产品/价格/信任）→结账完成率（流程）。CTR+CVR 都正常 ROAS 低→CPC 太高（换长尾词）或 AOV 太低（捆绑/追加销售）。

### 9. 大促 SEM 三阶段（朱峰April）

**年度日历**：BFCM/圣诞（极高，提前 6-8 周）、Prime Day/母亲节（高，4 周）、618/618/情人节等（中，2-4 周）。
**预热期 T-4 周**：活动策划→营收目标→渠道预算→素材制作→受众预建→小预算测素材→竞品情报→专属落地页→库存确认。
**大促期预算**：Brand Search 40-50%（出价+20-30%）/ Shopping 30-40%（+15-25%）/ Pmax 10-15%（预算+30-50%）/ Video+Display 5-10%（维持）。
**实时监控**：销售额每小时（<80% 告警）、CVR 每 2h（降>30% 暂停广告组）、CPA 每 2h（超 50% 降价）、库存每 4h（低于安全线减支 50%）、TTFB<800ms、竞品每 4h。触发器：品牌搜索量激增>200%→追加品牌预算；某素材 CTR>均值 2 倍→追加该素材预算；网站 503→立即停所有广告。
**收尾期**：T+1 数据归档+再营销加购未购；T+3 预算恢复日常；T+1 周素材沉淀；T+2 周经验文档。

### 10. SEO-SEM 协同（张子轩）

- **SEM→SEO**：高转化词优先 SEO 覆盖、高 CTR 文案参考 Meta Title、高 CVR 页面优先 SEO、受众画像指导选题、季节性提前布局
- **SEO→SEM**：GSC 高曝光低点击词 SEM 补位、高流量页做 SEM 着陆页候选、自然进 Top5 的词考虑降 SEM 投入
- **SERP 双重占位**：SEO 1-3 名→降/停 SEM；4-10→保持双展示；10+→积极 SEM 补位；品牌词始终投放防截流；竞品词策略投放
- **PMF 验证链**：SEM 验需求（搜索量+CTR）→验产品（CVR+ROAS）→验受众（定向测试）→验规模（扩预算测天花板）→SEO 长期布局
- **四大协同错误**：内部竞价/数据孤岛/目标冲突（SEO 求流量 SEM 求 ROAS）/资源浪费（SEO 已 Top5 还投 SEM）——统一 KPI=搜索渠道总利润

### 11. 优化节奏与扩量

- **每日 15min**：超预算 20%+、CPA 超目标 50%+ 暂停低效组、素材 CTR 骤降评估疲劳、异常数据查像素/网站/支付
- **每周 1h**：平台/系列/组/素材/关键词/受众六层复盘
- **每月 2h**：数据总览+渠道 ROI+素材策略+竞品动态+测试规划+SEO 协同
- **扩量**：纵向（预算≤20%/3 天、Lookalike 1→3→5%、长尾词、素材变体、时段倾斜）；横向（主渠道 ROAS 稳再开第二平台 15-20%、边际递减开新受众 10-15%、人群未覆盖开细分平台 5-10%）

### 12. LTV 口径 CPA 承受线

```
最大可接受 CPA = LTV × 目标利润率
LTV = 首购 AOV × (1 + 复购率 × 平均复购次数)
```
例：AOV $60、复购率 30%×2 次→LTV $96、利润率 40%→CPA 上限 $38.4。短期 ROAS 看 7/14/28 天窗口，长期 LTV 看 6-12 月——预算规划用 LTV 口径，日常优化用 ROAS 口径。

### 13. iOS 隐私应对

ATT 弹窗→依赖第一方数据+服务端追踪；7 天归因窗→长决策链结合 GA4+UTM；数据延迟→48h 后再优化决策；Lookalike 精准度降→加 Broad 测试；部署 Meta CAPI+TikTok Events API。

## 高频问答索引

- **Q：独立站投广告先选哪个平台？**
  A：按产品类型——视觉型 Meta/Pinterest/TikTok、功能型 Google Search/YouTube、高客单 Google Search、标品 Google Shopping、小众 Meta/TikTok/Reddit、日本 LINE。按预算：$1-3k 单平台、$3-10k 主辅 70/30、$10k+ 多平台矩阵。
- **Q：Google Ads 新账户怎么搭？**
  A：6 Campaign——Brand Search（品牌防御）、Non-Brand Search（品类/问题/竞品词）、Shopping（ bestseller/new/sale 分组）、Pmax（有数据后）、Display Remarketing（弃购 1-3d/浏览 4-14d/老客 15-30d）、YouTube（认知+考虑）。
- **Q：AIPL 漏斗预算怎么分？**
  A：新品牌 A 15-20%/I 20-25%/P 45-55%/L 5-10%；冷启动期 A/I 各 25% 向 P 倾斜，成熟期 P 升至 55%、L 升至 15%。
- **Q：新广告账户前 14 天注意什么？**
  A：Day1-3 装像素预热；Day4-14 投 Traffic/Engagement 攒数据（先优化 ATC 不切 Purchase）；日预算≥目标 CPA 5 倍；前 14 天不频繁调整；新像素前 100 事件定学习方向。
- **Q：SEM 关键词怎么分层出价？**
  A：品牌词最高（防守）>高意图产品词（buy/best/price）>品类通用词>问题教育词（低，SEO 优先）>竞品词（中，谨慎）。免费来源：Autocomplete/STR/GSC/Trends。
- **Q：大促 SEM 怎么打？**
  A：T-4 周预热（策划/预算/素材/受众预建/素材测试/竞品情报/落地页/库存）；大促期 Brand Search 40-50%+Shopping 30-40%+Pmax 10-15%，出价+15-30%；实时监控销售额/CVR/CPA/库存/TTFB/竞品，触发器自动化；T+1 归档+再营销、T+3 预算恢复。
- **Q：SEM 和 SEO 怎么协同？**
  A：双向数据赋能（月度交叉）+SERP 双重占位（SEO 1-3 名降 SEM、10+ 名 SEM 补位、品牌词始终投）+PMF 验证链（SEM 验需求→SEO 长期布局）。统一 KPI=搜索渠道总利润，避免内部竞价。
- **Q：LTV 口径下 CPA 承受线怎么算？**
  A：最大可接受 CPA=LTV×目标利润率；LTV=首购 AOV×(1+复购率×平均复购次数)。例 AOV$60 复购30%×2 次→LTV$96→CPA 上限 $38.4（40% 利润率）。
- **Q：广告素材怎么测？**
  A：变量隔离——每次只测 1 变量（Hook/文案/素材类型/CTA/Offer）；每变体≥1000 曝光或 100 点击；95% 置信度；获胜扩量失败即停；每周上新 2-3 变体。

## 相关卡片

- [归因与测量体系](../fundamentals/attribution-measurement.md) — 跨渠道口径裁决（本卡管渠道内优化，归因卡管跨渠道分配）
- [TikTok 内容×广告打法](tiktok-content-ads-playbook.md) — TikTok 侧对照
- [Meta 广告诊断与优化 SOP](../meta-ads-diagnosis/meta-diagnosis-sop.md) — Meta 侧体系
- 知识图谱：S22 分片待抽取
