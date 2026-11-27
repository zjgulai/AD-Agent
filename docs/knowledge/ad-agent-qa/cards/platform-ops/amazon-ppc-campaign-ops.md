---
title: Amazon PPC 建计划与优化 · ACoS 财务框架、Auto→Broad→Exact 漏斗、出价阶梯与周操作规则
doc_type: knowledge
module: ad-agent-qa
topic: amazon-ppc-campaign-ops
status: review
created: 2026-11-27
updated: 2026-11-27
owner: self
source: human+ai
source_docs: [S26]
fetched_at: 2026-11-27
---

# Amazon PPC 建计划与优化 · ACoS 财务框架、Auto→Broad→Exact 漏斗、出价阶梯与周操作规则

## 核心问题

Amazon 广告 ACoS 目标怎么从产品毛利算出来？新品 launch 和成熟品的目标 ACoS 差多少？Auto/Broad/Exact 三个 campaign 怎么分工不打架？每个关键词出多少 bid？搜索词报告每周怎么处理？本卡蒸馏 nexscope-ai/Amazon-Skills 的 `amazon-ppc-campaign` + `amazon-brand-analytics`——**Amazon PPC 的「建+优」双模式操作手册**，与现有两张 Amazon 卡分工：`amazon-ads-playbook` 管诊断顺序与否定词三层、`amazon-ads-operations`（S22）管架构树/预算%/Day7-14-30 检查点，本卡管**财务数学层+漏斗迁移规则+出价调整表**。

## 系统解答

### 1. 来源

- **来源**：`github.com/nexscope-ai/Amazon-Skills`（Nexscope AI，MIT，`raw/s26-amazon-skills/amazon-ppc-campaign/` + `amazon-brand-analytics/`）。Mode A=从零建计划（Build），Mode B=审计优化现有计划（Optimize）。
- **与 S22/S23 关系**：增量不冲突——S22 给架构/预算%/出价表框架，本卡补**财务公式+具体迁移阈值+出价调整百分比表**。S22 的 Day7/14/30 是检查点框架，本卡的 Day1/3/7/14/21 是**启动执行节奏**。

### 2. ACoS 财务框架（三个公式定所有出价）

```
Break-even ACoS = 广告前利润率 = (售价 − 全部成本) / 售价
Target ACoS     = Break-even ACoS − 目标利润率
Max CPC         = 售价 × Target ACoS × 转化率
```

算例（便携榨汁机 $39.99，成本 $18.50）：利润前广告 $21.49 → **毛利 53.7%** → Break-even ACoS **53.7%** → Target ACoS（成熟）**30%**（留 ~24% 利润）→ Target ACoS（**launch 激进期 50%**，前 4-8 周可接受）→ Max CPC（10% CVR）**$1.20**。

**Launch vs Mature 目标 ACoS 是本卡第一增量**：新品期允许 ~1.7 倍于成熟目标的 ACoS 换排名和评论，4-8 周后收回到成熟线——S22 的出价表没有这个时间维度。

**Max CPC 是盈利天花板不是实际出价**：实际竞争 bid 看 Amazon suggested bid range（建计划时 Seller Central 显示的真实拍卖数据）；suggested > Max CPC 时三选一——接受亏损（冲排名 launch）/提价/弃词。无 suggested 数据时按品类相对起点：Exact=suggested 或 MaxCPC 取低、Broad=Exact 的 70-80%、Auto=50-70%、Product Targeting=50-70%。

### 3. 账户结构：标准 4 campaign + 关键词漏斗

**默认 4 campaign**（预算紧可只先上 P1+P2）：

| 优先级 | Campaign | 角色 | 何时加 |
|:---:|----------|------|--------|
| P1 | **Auto Discovery** | Amazon 自动匹配收搜索词数据 | ✅ 必建 |
| P2 | **Manual Exact** | top 10-15 个已验证词最高控制最低 ACoS | ✅ 必建 |
| P3 | **Manual Broad** | 全部调研词宽匹配发现变体和长尾 | ✅ 数据一周后加 |
| P4 | **Product Targeting** | 打竞品详情页抢流量 | ✅ 有竞品 ASIN 时加 |

**预算紧启动序**：Day1 建 P1+P2 → Day3 查曝光（太低=bid 低于竞争区间提向 suggested）→ **Day7 加 P3+P4**+审 Auto 搜索词加明显否定 → **Day14 全量分析**迁移 2+ 单赢家 → **Day21** 对 20+ 点击词调 bid。

**关键词漏斗（核心优化循环）**：

```
Auto（发现新词）→ 出现 2+ 订单的词 → Manual Broad（宽匹配测试）
    → 出现 2+ 销售的词 → Manual Exact（赢家精确放量）
每步：把迁移词在源 campaign 加为否定词，防内部重复花费
```

### 4. 否定词三类种子（上线即建）

1. **跨 campaign 否定**：Exact campaign 的所有关键词在 Broad+Auto 里加 Negative Exact——漏斗隔离防自相残杀（这是漏斗能成立的前提）；
2. **无关词否定**：词面相同品类/意图不同——错材质（bamboo cutting board 否定 "plastic/glass cutting board"）、错产品（"cutting board oil/stand"）、错意图（"how to clean/DIY"）；
3. **通用浪费否定**：低意图修饰词 "free/cheap/used/DIY/review/reddit/how to"。

### 5. Mode B 优化规则（阈值即知识）

**关键词漏斗三动作**：
- **迁移上**（2+ 订单）：Auto→Exact 或 Broad→Exact，源 campaign 加否定；
- **加否定**（**10+ 点击 0 销售**）：源 campaign 加 Negative Exact/Phrase；
- **观察名单**（<20 点击）：数据不够——标记下轮再看。

**出价调整表**（仅对 **20+ 点击**词——统计显著性下限）：

| 当前 ACoS | 动作 |
|---|---|
| >200% | 降 bid 30-50% |
| 100-199% | 降 bid 20% |
| target+10% ~ 99% | 降 bid 10-15% |
| target ±10% | 不动 |
| 低于 target | **加 bid 10-20%** |
| 10+ 点击 0 销售 | **暂停词** |

**五维审计**：①财务健康（break-even vs 当前 ACoS、月盈亏）②campaign 效率（逐 campaign ACoS 🔴🟡🟢）③关键词表现（盈利/边缘/亏损/零销售分组）④预算分配（花费与收入是否成比例，建议挪移）⑤漏掉的机会（转化词未进 Manual、高花费零销售词没否定、赢家欠预算）。

### 6. Brand Analytics 信号（SFR + Market Basket 两条规则）

`amazon-brand-analytics` 只有两条可蒸规则，作为关键词研究的上游信号：

- **SFR 机会缺口**：Search Frequency Rank 报告（近 90 天）对比「搜索频率排名 vs 你的 click share vs 品类平均 click share」——**高搜索频率低 click share=机会缺口**；转化份额显著低于点击份额=优化需求。输出按 opportunity score 分 High/Medium/Low；
- **Market Basket 共购阈值**：**>25% 共购率=强捆绑候选**；统计显著性下限 **10+ 共购**才算数。用法：bundle 设计/交叉推广/相邻品类扩张判断。

### 7. 边界与局限

源 skill 自述：无 Seller Central API 直连、不能拉实时 bid landscape、不能自动改计划——输出是「可直接在 Seller Central 执行的蓝图」。Amazon fees 按品类估（~15% referral+FBA 按尺寸），用户给不出精确成本时用品类估计并**显式标注假设**。CVR 无数据时用品类基准 10-15%。

## 高频问答索引

- **Q：Amazon 广告目标 ACoS 怎么定？launch 和成熟差多少？**
  A：Break-even ACoS=广告前利润率（售价−全部成本/售价）；Target ACoS=break-even−目标利润率。launch 期允许 ~1.7 倍激进（例：break-even 53.7%→成熟 target 30%/launch target 50%），前 4-8 周换排名评论后收回。Max CPC=售价×Target ACoS×CVR 是盈利天花板，实际 bid 看 Amazon suggested range 取低者。
- **Q：Auto/Broad/Exact 三个 campaign 怎么不打架？**
  A：关键词漏斗分工——Auto 发现新词、Broad 宽匹配测试、Exact 放量赢家。隔离靠否定词：Exact 的所有词在 Broad/Auto 里加 Negative Exact。迁移规则：2+ 订单 Auto→Broad/Exact、2+ 销售 Broad→Exact，每步源 campaign 加否定防重复花费。
- **Q：搜索词报告每周怎么处理？**
  A：三动作——2+ 订单的词迁移上（Exact）；**10+ 点击 0 销售**的词加否定；<20 点击的进观察名单下轮再看。出价调整只对 **20+ 点击**词：ACoS>200% 降 30-50%、100-199% 降 20%、target+10%~99% 降 10-15%、低于 target 加 10-20%、10+ 点击 0 销售直接暂停。
- **Q：新品广告预算怎么分配四个 campaign？**
  A：标准 4 campaign——P1 Auto Discovery（必建收数据）+P2 Manual Exact top10-15 词（必建）+P3 Manual Broad（数据一周后加）+P4 Product Targeting 竞品页（有 ASIN 时加）。预算紧先上 P1+P2。Day1 建 P1P2→Day3 查曝光→Day7 加 P3P4+审 Auto 否定→Day14 迁移赢家→Day21 调 bid。
- **Q：Brand Analytics 数据怎么用到广告？**
  A：两条——SFR 报告找「高搜索频率低 click share」机会缺口（你的 click share vs 品类均值对比）；Market Basket 找 >25% 共购率的捆绑候选（10+ 共购才算统计显著）。输出机会缺口按 High/Medium/Low 分级。

## 相关卡片

- [amazon-ads-playbook.md](./amazon-ads-playbook.md) — Amazon 广告打法（诊断顺序/否定词三层/SB+SP 协同）
- [amazon-ads-operations.md](./amazon-ads-operations.md) — Amazon 广告运营打法（S22；架构树/预算%/出价表/Day7-14-30）
- [amazon-keyword-listing-ops.md](./amazon-keyword-listing-ops.md) — 关键词与 Listing 运营（T1/T2/T3 词库/Listing 硬规则）
