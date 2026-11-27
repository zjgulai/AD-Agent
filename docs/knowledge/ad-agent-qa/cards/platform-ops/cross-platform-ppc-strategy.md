---
title: 跨平台 PPC 策略规划 · 买家行为选平台、ROAS 财务框架、预算分配与 Mode B 审计重分配
doc_type: knowledge
module: ad-agent-qa
topic: cross-platform-ppc-strategy
status: review
created: 2026-11-27
updated: 2026-11-27
owner: self
source: human+ai
source_docs: [S27]
fetched_at: 2026-11-27
---

# 跨平台 PPC 策略规划 · 买家行为选平台、ROAS 财务框架、预算分配与 Mode B 审计重分配

## 核心问题

新品投广告先投哪个平台、各投多少？ROAS 目标怎么算？Google/Meta/TikTok 现有投放该怎么审计重分配预算？本卡蒸馏 nexscope-ai/eCommerce-Skills 的 `ecommerce-ppc-strategy-planner`——**跨平台投放的「选平台+分钱」决策层**，在各平台内部打法（Meta 诊断、Amazon 漏斗、Google 6C）之上的编排层。

## 系统解答

### 1. 来源

- **来源**：`github.com/nexscope-ai/eCommerce-Skills`（Nexscope AI，MIT，`raw/s27-ecom-skills/ecommerce-ppc-strategy-planner/`）。两模式：**A=Build 从零设计多平台策略**；**B=Optimize 审计现有跨平台投放重分预算**。
- **与 KB 关系**：KB 各平台卡回答「在 X 平台怎么投」；本卡回答「先投哪个、各投多少、总盘怎么调」。**不生成素材**（文案/创意方向给方向不给产出）。

### 2. 财务框架三公式（所有平台决策的地基）

```
Break-even ROAS = 1 ÷ Profit Margin        （不亏本的最低 ROAS）
Target ROAS     = Break-even × 1.5~2       （可持续增长的目标，留利润缓冲）
Max CPA         = AOV × Profit Margin      （单次获客成本天花板）
```

| 毛利率 | Break-even ROAS | 含义 |
|:---:|:---:|------|
| 25% | 4.0x | 每 $1 广告费须产出 $4 才不亏 |
| 50% | 2.0x | |
| 60% | 1.67x | 毛利越高广告空间越大 |
| 75% | 1.33x | |

算例：$34 商品毛利 76.5%、月预算 $2,000 → break-even 1.31x / target 2.5x / Max CPA $26.01；按 target 投放预期月广告收入 $5,000。

### 3. 平台选择：买家行为类型是第一驱动

**先问买家怎么找到你的产品**（Mode A 必问项），答案直接定主平台：

| 买家行为 | 主平台 | 次平台 | 逻辑 |
|---------|--------|--------|------|
| **a) 主动搜索**（知道要什么，如 "soy candles"） | Google Shopping/Search | Meta retargeting | 捕获存量需求 |
| **b) 视觉种草**（看到想要，如 lifestyle/fashion） | Meta Ads | Google Shopping | 用图像创造需求 |
| **c) 需要看演示**（demo 才能打动） | TikTok Ads | Meta Ads | 视频 wow 感驱动发现 |
| d) 不确定 | 按品类推断并标 ⚠️ estimated | — | 给推理过程 |

品类→平台映射补充：大宗商品（人们会搜）→Google 主；高客单慎重购买→Google Search 主+Meta retargeting；复购消耗品→Meta+Email 主+Google Brand；新奇 demo 型→TikTok 主。

**分配规则**：有网站流量或邮件列表+预算>$1,000/月→必含 retargeting（Meta 或 Google Display，通常是最高 ROAS 渠道）；**预算<$1,000/月→只选一个主平台不摊薄**。

### 4. 预算分配三套模板（按主平台类型）

**搜索意图型（Google 主）**：Google Shopping/PMax 50-60% + Meta prospecting 20-25% + retargeting 10-15% + 测试渠道 5-10%。

**视觉冲动型（Meta 主）**：Meta prospecting 45-55% + Google Shopping 20-25%（承接搜索溢出）+ retargeting 15-20% + TikTok 5-10%。

**演示新奇型（TikTok 主）**：TikTok 40-50% + Meta 20-30% + Google Shopping 10-20%（接住 viral 带来的搜索）+ retargeting 10-15%。

### 5. 平台 ROAS 基准（2025-2026 行业均值，标注时效）

| 平台 | 平均 ROAS | Top Quartile | 最适合 |
|------|:---:|:---:|--------|
| Google Shopping | 4.5x | 6x+ | 高意图买家 |
| Meta（FB/IG） | 2.2x（retargeting 3.6x） | 4-5x | 视觉品/冲动购/再营销 |
| TikTok | 1.4x | 2x+ | 发现型/demo 驱动/年轻客群 |

电商全行业平均 2.87x。⚠️ 这些是第三方基准，用自家数据校准——Mode B 的判定永远以自家 break-even/target 为准。

### 6. Mode B 审计重分配规则

逐平台对照 break-even/target ROAS 打状态，然后动预算：

| 状态 | 判定 | 动作 |
|------|------|------|
| 🟢 超 target | ROAS 高于目标 | **加预算 20-30%** |
| 🟡 break-even~target 之间 | 不亏但没达标 | **先优化再放量**（不加钱） |
| 🔴 低于 break-even | 在亏钱 | **砍 50% 或暂停** |

新 campaign 上线 **2-4 周内不做优化判断**——学习期数据不可信，这是 Mode B 的硬门槛。

逐平台优化方向速查：Google→否定词/出价策略/campaign 类型切换；Meta→受众收窄/素材更新/版位优化/lookalike 扩展；TikTok→hook 改版/定向调整/Spark Ads 转向。

### 7. 与单平台打法的关系

本卡是**编排层**：产出「投哪些平台、各多少钱、每平台 campaign 类型+定向方向+出价策略+日预算」的 brief；素材文案只给方向（钩子概念/关键卖点/禁忌），**不产出成品素材**。30 天测试计划四周节奏：W1 上线→W2 看早期指标做初步优化→W3 放量赢家砍输家→W4 全面复盘重分配。

## 高频问答索引

- **Q：新品先投 Google 还是 Meta 还是 TikTok？**
  A：问买家行为——主动搜索型→Google Shopping 主；视觉种草型→Meta 主；要看演示才懂→TikTok 主。不确定按品类推断并标 ⚠️。预算<$1,000/月只投一个主平台。
- **Q：跨平台 ROAS 目标怎么定？**
  A：Break-even ROAS=1÷毛利率；Target=Break-even×1.5~2 留利润缓冲；Max CPA=AOV×毛利率。例：$34 商品 76.5% 毛利→break-even 1.31x/target 2.5x/Max CPA $26。
- **Q：Google ROAS 4x、Meta 1.5x，该把预算全挪给 Google 吗？**
  A：先看是否超各自 break-even/target。🟢超 target 加 20-30%、🟡区间内先优化不加钱、🔴低于 break-even 砍 50% 或暂停。注意 Meta prospecting 低 ROAS 但在为 Google/retargeting 供受众——纯 ROAS 排序会误杀漏斗上游。
- **Q：新 campaign 跑了一周 ROAS 0.8 要不要关？**
  A：不要。新 campaign 需 2-4 周度过学习期再判；一周数据不具统计意义。先检查预算是否过低（学习受限）和定向是否过窄。
- **Q：retargeting 值得单独投吗？**
  A：值得且通常是全盘最高 ROAS（Meta retargeting 基准 3.6x vs prospecting 2.2x）。前提：有网站流量或邮件列表积累受众；预算>$1,000/月才值得单列。

## 相关卡片

- [dsite-sem-ads-playbook.md](../platform-ops/dsite-sem-ads-playbook.md) — 独立站 SEM（Google 侧的 6C 架构细节）
- [meta-ads-diagnosis](./meta-ads-diagnosis/) — Meta 单平台诊断体系（Mode B 优化动作落点）
- [attribution-measurement.md](../fundamentals/attribution-measurement.md) — 跨平台归因（跨平台对比 ROAS 前先解决口径）
- [payback-period-budget-gate.md](../fundamentals/payback-period-budget-gate.md) — 回本周期预算闸门（比单点 ROAS 更长期的健康度）
