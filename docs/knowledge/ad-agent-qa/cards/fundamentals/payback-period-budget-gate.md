---
title: Payback Period 预算闸门 · LTV:CAC 四宗罪、毛利回本算法、Cohort 恢复路径与渠道准入判据
doc_type: knowledge
module: ad-agent-qa
topic: payback-period-budget-gate
status: review
created: 2026-11-27
updated: 2026-11-27
owner: self
source: human+ai
source_docs: [S25]
fetched_at: 2026-11-27
---

# Payback Period 预算闸门 · LTV:CAC 四宗罪、毛利回本算法、Cohort 恢复路径与渠道准入判据

## 核心问题

一个渠道「能不能投」的财务判据是什么？LTV:CAC=3:1 是不是就能放量？CAC $300 拉来的客户多久回本？为什么同一个 CAC 在不同价位计划下 affordability 天差地别？本卡蒸馏 marketingskills `ads/references/payback-period.md`——**渠道预算的现金流闸门**，补 KB「预算方法」缺口：breakeven 告诉你最多付多少，payback 告诉你现金被占多久，两者都要才敢扩。

## 系统解答

### 1. 来源与口径

- **来源**：`github.com/coreyhaines31/marketingskills`（MIT，`raw/s25-marketingskills/skills/ads/references/payback-period.md`）。出自 Corey Haines《Founding Marketing》ch.7，SaaS 订阅口径——**DTC 翻译**：ARPU→客单价/复购贡献，churn→退货+流失 cohort，gross margin→SKU 毛利率；3-12 月目标带是规划参考不是普适批准线。

### 2. 先杀 LTV:CAC——四宗罪

**LTV:CAC 是无用且常有破坏性的指标**——感觉严谨其实通常是谎言：

1. **假设所有客户都会流失**：LTV 给每个账户预写讣告。你最好的客户不 churn——他们复利。预设人人死亡的指标低估了真实基本盘；
2. **假设 churn 均匀发生**：实际不是。Baremetrics 数据：**更多 churn 发生在最初 3 个月**——前置集中不是平滑。混合 LTV 把这个尖峰抹成平直均值，藏住真实风险（和真实回本数学）；
3. **混合 ARPU 掩盖分计划差异**：$9/月计划和 $999/月计划被平均成一个谁都不描述的数字。对 $9 买家有效的渠道/创意/payback 和 $999 买家完全不同——但混合 LTV:CAC 说「3:1 没问题」，你就去放大错的东西；
4. **忽略收入延迟**：免费试用/免费计划/长销售周期意味着钱在 CAC 花出去后数周数月才到。LTV:CAC 把获客和收入当同时发生——**差距正是 startup 断现金的地方**。

「健康」的 3:1 LTV:CAC 可以盖在会让你破产的渠道上，因为这个比率从不问**现金什么时候回来**。

### 3. 替代品：Payback Period

```
Revenue-only ratio = CAC / monthly ARPU
毛利回本 = CAC / (monthly ARPU × gross margin)
```

（gross margin 用小数；revenue-only 假设 100% 毛利不含履约成本。）简化比率单位是月、假设稳定月毛利无 churn 无回款延迟。**3-12 月目标是规划参考**——按现金跑道/毛利/cohort 恢复自选目标，比率本身长短不构成改预算的理由。它按 cohort 按计划算（不混合），正好暴露 LTV:CAC 藏的东西。

**算例——同 CAC 天差地别**（CAC=$300，revenue-only 仅为对比非放量许可）：

| 计划 | ARPU/月 | Revenue-only=300/ARPU | 判定 |
|------|---------|----------------------|------|
| Starter | $9 | **33.3 月** | 别为它投付费获客——33 月还没算成本和 churn |
| Pro | $99 | **3.0 月** | 先查毛利：80% 毛利→3.8 月；20% 毛利→**15.2 月**太慢不能扩 |
| Enterprise | $999 | **0.3 月** | 可扩，但先确认现金实际何时到账（年付/net-60） |

同 CAC 不意味着同 affordability。**$99 计划在 20% 毛利下是 300/(99×0.20)=15.2 月**——尽管 revenue-only 只有 3.0 月。同计划同 cohort 对照实测毛利/留存/回款时点再批预算。

### 4. Cohort 恢复路径（churn 时点要算进去）

`CAC / (ARPU × 年留存率)` **不是**折现回本——单一年末留存率识别不了月度恢复路径。折现需显式贴现率；留存描述客户存活。

对 cohort，找首个累计毛利覆盖 CAC 的月：

```
第 n 月累计恢复 = Σ(ARPU_t × gross_margin_t × retained_fraction_t)
```

有实测「每原始获客客户留存收入」时直接用它，别再乘留存。评估现金恢复时计入回款延迟。**观察到的 cohort 未恢复 CAC 就如实报，不要编回本日期。**

算例：CAC $300、ARPU $99、毛利 80%。两个 cohort 年末留存都是 70%：
- **早流失**：1-12 月每月留存 70% → 每原始客户月毛利 $55.44 → **第 6 月**首次过 $300；
- **晚流失**：1-11 月 100% 留存、第 12 月 70% → 前 11 月每月 $79.20 → **第 4 月**过 $300。

旧的单留存比率给两 cohort 同样的 4.3 月且不算毛利——年末留存相同但实际恢复路径不同。

### 5. 渠道准入四步

1. 算渠道 CAC（全口径：spend/客户数，含创意和管理费）；
2. 算毛利回本+查实测 cohort 恢复路径（含回款时点）；
3. 与跑道和自选目标比（3-12 月带是规划参考非普适批准线）——**别用 revenue-only 比率或年留存乘数放量**；
4. **每月重跑**——CAC 随放量上漂，闸门跟着动。

与 breakeven CPL/CPC 数学配套：breakeven 告诉你**最多**能付多少/线索，payback 告诉你**现金被占多久**——两个都要才敢扩而不断粮。

### 6. 两条邻近规则

- **无社媒放大计划的 OOH 是烧钱**：户外广告（ billboard/transit/print）自身没有点击/pixel/确定性回路，只有被设计成「被拍照、被发到社媒、被社媒放大」才回本——OOH 买瞬间、社媒买 reach。跑没有社媒计划的 OOH=买不可测不可复利的 awareness；
- **叙事动量**（广告文案）：最强广告是把故事往前推而非复述 pitch——每行挣下一行的注意力朝 CTA 建张力而非前置功能堆砌。配「一次只测一个变量」（先文案再创意再受众）才知道是什么动了 payback。

## 高频问答索引

- **Q：LTV:CAC=3:1 是不是就能放量？**
  A：不是。LTV:CAC 四宗罪：假设全 churn（最好客户不 churn 反而复利）、假设 churn 均匀（实际前 3 月最集中）、混合 ARPU 掩盖分计划差异、忽略收入延迟（钱在 CAC 后数周数月才到）。它从不问现金何时回来——3:1 可以盖在会破产的渠道上。
- **Q：CAC $300 的客户多久回本？**
  A：看计划和毛利。revenue-only=CAC/ARPU：$9 计划 33.3 月别投、$99 计划 3.0 月但 20% 毛利下实际 15.2 月、$999 计划 0.3 月可扩（先确认回款时点）。用毛利回本=CAC/(ARPU×毛利率)，按 cohort 算累计恢复路径含 churn 时点。
- **Q：两个 cohort 年末留存率相同，回本一样吗？**
  A：不一样。早流失（每月留存 70%）第 6 月恢复 CAC；晚流失（前 11 月 100%）第 4 月——年末留存率相同但月度恢复路径不同。`CAC/(ARPU×年留存)` 给两者同样的错误答案。
- **Q：渠道能不能投的完整判据？**
  A：四步——全口径 CAC→毛利回本+实测 cohort 恢复路径（含回款时点）→与跑道和自选目标比（3-12 月是参考非批准线）→每月重跑（CAC 随放量漂移）。与 breakeven 配套：breakeven 管「最多付多少」，payback 管「现金占多久」。

## 相关卡片

- [ad-bidding-full-chain.md](./ad-bidding-full-chain.md) — 出价全链路（同 fundamentals 域；出价策略与 payback 闸门衔接）
- [attribution-measurement.md](./attribution-measurement.md) — 归因测量（CAC 的归因输入在那张卡）
- [attribution-models-reconciliation.md](./attribution-models-reconciliation.md) — 归因模型算例与平台差异（同批 S25）
- [google-search-playbook.md](../platform-ops/google-search-playbook.md) — Google Search 运营（离线转化导入=订单价值回传）
