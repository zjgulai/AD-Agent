---
title: 归因模型算例与平台差异诊断 · 六模型同一旅程、DDA/Shapley、差异幅度表与退款不对称
doc_type: knowledge
module: ad-agent-qa
topic: attribution-models-reconciliation
status: review
created: 2026-11-27
updated: 2026-11-27
owner: self
source: human+ai
source_docs: [S25]
fetched_at: 2026-11-27
---

# 归因模型算例与平台差异诊断 · 六模型同一旅程、DDA/Shapley、差异幅度表与退款不对称

## 核心问题

「Google 说 50、Meta 说 40、GA 说 60、CRM 说 35——谁对？」——没人全对。各归因模型到底怎么分同一笔 $12,000 订单？DDA/算法归因凭什么可信/不可信？平台间数字差多少算正常、多少算坏了？退款怎么让各平台 ROAS 系统性失真？本卡蒸馏 marketingskills `attribution` skill——**归因的「算例层+差异诊断层」**，与 `attribution-measurement.md`（S22 三角测量/增量测试/MMM 选型）互补：那张卡管「用什么范式测」，本卡管「模型内部怎么算、数字对不上时怎么查」。

## 系统解答

### 1. 来源与分工

- **来源**：`github.com/coreyhaines31/marketingskills`（MIT，`raw/s25-marketingskills/skills/attribution/`）。SKILL.md v1.1.10 + 4 references（models/paradigms/first-party/by-business-type）。
- **与现有卡分工**：`attribution-measurement` 管三角测量框架（MTA/MMM/增量分工+geo MDE+Meridian/Robyn）；本卡管**模型算例**（六规则模型同一旅程各分多少）+**平台差异诊断**（差多少正常/何时坏+退款不对称+server-side 恢复边界）。两者合读=归因完整图景。

### 2. 六模型同一旅程算例（$12,000 年单）

一条 B2B 买家 38 天五触点旅程：T1 LinkedIn ad（d0）→ T2 organic blog（d5）→ T3 retargeting（d12）→ T4 branded search（d30）→ T5 direct→demo（d38 转化）。同一笔 $12k 各模型分法：

| 模型 | 规则 | $12k 给谁 | 故事 |
|------|------|----------|------|
| First-touch | 100% 给首触 | **LinkedIn ad $12k** | 擅长论证社交需求创造价值，对成交全盲 |
| Last-touch | 100% 给末触 | **Direct $12k** | Direct 是「不知道」垃圾抽屉——这是 top-funnel 被断粮的机制 |
| Last non-direct | 跳过 direct 给最后非直 | **branded search $12k** | 但品牌词只在 LinkedIn+blog 创造需求后才发生——给品牌词记功=让品牌为别人创造的需求收功 |
| Linear | 均分 | 各 $2.4k | 诚实但无决策力——一切看起来同等重要 |
| Time-decay | 越近转化权重越高（7 天半衰） | Direct $7.5k+branded $3.4k | 长周期下退化成准 last-touch，低估启动一切的 LinkedIn |
| Position-based (U) | 40% 首+40% 末+20% 中分 | 首末各 $4.8k | 通常 B2B 最可辩护——「创造」和「成交」是你真正要做的两个决定 |

**可操作结论**：**first-touch 和 last-touch 并排报告**——LinkedIn vs Direct 的差值本身就是洞察：社交创造的需求后来以 direct/branded 形式出现。没有单一数字能装下这个，**差值能**。

### 3. DDA/算法归因（Shapley）白话与门槛

数据驱动归因不问固定规则，问反事实：**每个触点实际把转化概率提升了多少**。Shapley 机制：把每个触点当团队成员，比较「有它 vs 没有它」的旅程转化率差，在所有触点组合上取平均边际提升。

**什么时候值得用**：
- 需要**量**——反事实要足够转化才稳定。Google 官方建议 DDA 质量需 ~**200 转化+~2,000 广告交互/30 天**；量不足时 DDA 常塌缩成 last-click 的噪声伪装；
- 旅程**主要数字化且被追踪**——Shapley 只能给喂过的触点打分，offline/dark social/cookie 丢失的触点对它隐形，高口碑 B2B 会得到「自信的错误 DDA」。

**诚实局限**：黑箱（CFO 问「为什么 LinkedIn 23%」答不出）；相关非因果（这正是增量测试存在的理由——验证 DDA 声称的东西）；垃圾进垃圾出（继承追踪所有盲点——一半旅程是 direct 时 DDA 在半盲数据上自信分账）。

**模型可用性时效**：Google Ads/GA4 已退役 first-click/linear/time-decay/position-based 报表模型（2023）；Google UI 现只剩 **DDA+last-click**——六模型表是**概念和自有路径数据上的计算模型**，不是 Google 下拉选项。

### 4. 选型决策导引

| 情形 | 选什么 |
|------|--------|
| 短周期少触点小量级 | last non-direct + 自报问卷，别过度建模 |
| 长 B2B 周期有明确 created/closed | **自有路径数据上 position-based 为主**+first/last 并排（非 Google 选项） |
| 高量级主要数字化需日常分配 | DDA，定期用增量测试验证 |
| offline+品牌重真实预算 | 别靠任何用户级模型——MMM+增量测试 |

铁律：**选一个模型保持一致+配一个模型外检查**。为让某渠道好看而换模型=最快失去归因信任的方式。

### 5. 平台差异诊断：差多少正常、何时坏

**核心框架：GA4 和 Google Ads 永远对不上，这是正常的。** 动手诊断前先设期望：

**天然差异（好 setup 也会有）**：
1. **日期归因**：Ads 按点击日记账、GA4 按转化日；Ads 转化可在点击后 90 天回填，近期区间会追溯增长；
2. **归因模型范围**：Ads 只记自己点击的功、GA4 DDA 跨全渠道分——GA4 永远给付费搜索更少转化；
3. **View/engage-through+跨设备**：Ads/Meta 计入 GA4 看不到的；
4. **计数规则**：Every vs One（Ads）、All vs First（Meta）、per-event vs per-session（GA4）；
5. **建模**：Consent Mode 下各平台跑各自建模引擎；
6. **处理延迟**：GA4 24-48h、GA4→Ads 导入 +1-3 天——**永远别比截止 <3 天前的窗口**；
7. **时区/币种**错位挪动日界。

**正常 vs 异常**：**10-30% Ads-vs-GA4 差距正常**。以下才查：差距 >40%、方向翻转、差距突然变化、某平台读数为零。

**环境性漏计（追踪装对了仍丢）**——按量级排序的头号元凶：

| 原因 | 方向 | 量级 | 修复类 |
|------|------|------|--------|
| Consent banner 硬阻塞 GTM | 全指标降 | 严格 EU 市场最高 ~55% | 客户端（CMv2） |
| Consent Mode v2 错配 | Ads 转化崩 | 最高 ~90% 隔夜；修复后仅 ~40% 可经建模找回 | 客户端 |
| 广告拦截器 | 全降 | 全球 ~30%；B2B/开发者受众 40-60% | 服务端（部分） |
| Safari ITP | →direct | _ga/_gcl_aw 等 JS cookie 封顶 7 天、**带 gclid/fbclid 的落地页封顶 24 小时**；Safari 占美/澳 lead-gen 流量 20-30% | 服务端（HTTP Set-Cookie 豁免） |
| 跨设备旅程 | →未归因 | 手机点广告桌面成交；B2B/高客单最重 | 身份数据（EC/advanced matching/CAPI） |
| 重定向剥 gclid/fbclid | Ads→0 | 受影响路径 100% | 客户端（QSA/$is_args$args） |
| SPA/iframe 感谢页不加载 | →0 | 二元（要么全丢要么全有） | 客户端（History Change/dataLayer） |
| 双 tag/重复计数 | 虚高 | GA4 导入+原生 tag 双 Primary 最高 2x | 设置（降级其一） |
| Bot 表单填充 | 转化>真实 lead | 可达 ~50% | reCAPTCHA/排除测试/IP 排除 |

**两个高频错诊**：「有转化没 lead」= bot 填充/重复计数/邮件投递失败（先查表单工具自己的条目列表再怪追踪）；「有 lead 没转化」= 拦截器/consent/ITP/感谢页没加载/gclid 被剥/窗口过期。

**server-side 边界**：自建 sGTM 难——GCP 生产 ~$90+/月或托管 $17-83/月、50-120 开发小时、自定义子域+DNS、静默坏（「转化暗掉 72 小时才有人发现」）、consent 服务端同样适用（对 opt-out 用户发=违规）。Meta 自报 CAPI 数字（+19% 归因购买/-13% 单成本站本）和 Stape 案例（+46% Google 转化）是**上限值**。实操口径：先量自己账户 CRM-vs-平台的真实差距再决定投不投 server-side。

### 6. 退款不对称（电商专属坑）

平台对「退款的购买还算不算转化」答案不一致：

- **Google Ads**：支持转化调整——restate 改价值（部分退款）、retract 整单撤销；要 gclid/gbraid（不含 wbraid）、一般需 order_id、须 54 天内（出价使用需 7 天内）、一次性（retract 后不能再 adjust）；
- **GA4**：有标准 `refund` 事件按 transaction_id；
- **Meta**：**无退款机制文档**——发出的 Purchase 永远算数。

两个后果：①老老实实 adjust Google+发 GA4 退款的店，Meta ROAS 会**结构性**高于 Google ROAS——这是平台不对称不是追踪 bug；②几乎没人接调整——高退货店所有平台 ROAS 都被高估约等于退货率，「退款调整接了没」是审计必问题，通常答案是没有。

### 7. 归因谎言的结构性偏差（MTA 层）

click-based 路径有第二重偏差：**impression 渠道（社交/视频/展示）经常根本进不了 journey**——无点击的浏览不留可缝合触点，MTA 系统性**高估需求捕获**（搜索/邮件/direct）、**低估需求创造**。MTA 不会宣布这个缺口：看不见的静默塞进 direct、看得见的过度计量。**把 MTA 当不完整且方向性有偏的信号——不是干净的下界**（其再营销/品牌词数字常被高估）——永不作大预算重分配的唯一依据。

**三角校准规则**：当增量测试/调研/平台差距一致指向某渠道在 click-MTA 里被低估时，**别发明平台差距乘数**。走文档化规则：
1. **渠道级 override（报表层）**：MTA 跑完后在有证据的窗口把一部分转化从 Direct/品牌词移入被低估渠道；原始 MTA 表保留，决策看板读调整后表——快但只到渠道粒度；
2. **用户级插入（进阶）**：MTA 跑前给 Direct 旅程子集合成触点（如 YouTube impression），再打分——要工程量但解锁创意/受众粒度。

从单渠道单窗口单个保守 lift 切片开始，别上 100% 噪声点估计；干系人信第一条规则后再扩。

## 高频问答索引

- **Q：各平台转化数加起来超过真实订单，谁错了？**
  A：没人全对。每平台按自己窗口和口径认领同一订单+view-through+建模。选一个真理源（CRM/订单系统）定转化总数，平台数字只解释来源不重新定义数量；绝不跨平台相加。
- **Q：Ads 和 GA4 差 20% 正常吗？**
  A：正常——10-30% 是好 setup 也会有的天然差（日期归因/模型范围/view-through/计数规则/建模/延迟）。查的信号：>40%、方向翻转、突然变化、某平台读零。
- **Q：DDA 数据驱动归因什么条件下可信？**
  A：需要量（Google 建议 ~200 转化+~2,000 交互/30 天，量不足塌缩成 last-click 噪声）+旅程主要数字化被追踪（offline/dark social 对它隐形）。它是相关非因果的黑箱，须定期用增量测试验证。
- **Q：退款怎么让平台 ROAS 失真？**
  A：Google Ads 支持转化调整（restate/retract，有时限和 order_id 要求）；GA4 有 refund 事件；**Meta 无退款机制**——发出的 Purchase 永远算数。老实接调整的店 Meta ROAS 会结构性虚高；没人接调整时所有平台 ROAS 都高估约等于退货率。
- **Q：direct 和品牌词占比超高说明什么？**
  A：最常见解释是 top-funnel 在起作用而归因把它藏起来了——先排除老客/丢 referrer/线下发现，再用自报问卷或增量测试确认；别直接当追踪缺陷也别当 direct 真实。

## 相关卡片

- [attribution-measurement.md](./attribution-measurement.md) — 三角测量+增量测试+MMM 选型（S22；本卡管模型算例与差异诊断）
- [payback-period-budget-gate.md](./payback-period-budget-gate.md) — payback 闸门（CAC 的财务判据，与归因输入衔接）
- [google-search-playbook.md](../platform-ops/google-search-playbook.md) — Google Search 运营（离线转化导入在那张卡操作层）
