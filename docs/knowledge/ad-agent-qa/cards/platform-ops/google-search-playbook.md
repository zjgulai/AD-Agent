---
title: Google Search 广告运营手册 · 意图阶梯、账户结构、匹配类型门禁、周检仪式与 PMax 护栏
doc_type: knowledge
module: ad-agent-qa
topic: google-search-playbook
status: review
created: 2026-11-27
updated: 2026-11-27
owner: self
source: human+ai
source_docs: [S25]
fetched_at: 2026-11-27
---

# Google Search 广告运营手册 · 意图阶梯、账户结构、匹配类型门禁、周检仪式与 PMax 护栏

## 核心问题

Google Search 预算先投哪里？品牌词要不要投、投多少？广泛匹配什么时候能开？搜索词报告怎么变成否定词和关键词？PMax 会不会蚕食品牌词？本卡蒸馏 marketingskills `ads/references/google-search-playbook.md`——**Google Search 的操作层手册**，与 `dsite-sem-ads-playbook`（S22 架构层：10 平台矩阵/6-Campaign/AIPL）互补：那张卡回答「Google 在 SEM 组合里怎么摆」，本卡回答「Search 账户内部怎么运营」。

## 系统解答

### 1. 来源与 DTC 翻译口径

- **来源**：`github.com/coreyhaines31/marketingskills`（MIT，`raw/s25-marketingskills/skills/ads/references/google-search-playbook.md`）。框架改编自 Ivan Falco 的 ads-skills，B2B SaaS 口径。
- **⚠️ 口径翻译**：原文基准是 B2B（CPL/SQL/pipeline/offline conversions）。Momcozy 是 DTC——「offline conversions 导入 CRM 成交」翻译为「**导入真实订单价值/毛利回传**」（增强型转化/gclid+order_id），「SQL 率」翻译为「购买率/复购 cohort」，「brand pause test」对 DTC 同样适用。B2B 基准数字（CPC $8-40、CPL $80-400）不可直接套，须用自家前 30 天数据重标定。

### 2. 意图阶梯：预算逐层解锁，跳层=烧钱

Search **收割已存在的需求**，不能创造需求——品类搜索量近零时直接说，预算放上游（Meta/TikTok/YouTube）做需求创造，Search 负责接住落地流量。支出按阶梯逐级开启，每层须证明能转化为**真实成交**才解锁下一层：

1. **Brand**——「他们要的是你」（品牌名+品牌+价格/登录）；最便宜点击最高转化，常开；
2. **High-intent non-brand**——已准备购买（品类词+购买修饰）；利润中心，大部分预算在这；
3. **Competitor**——在比较替代品（竞品名+alternative/vs）；CPC 高 CVR 低，须配独立对比落地页才选择性投；
4. **Problem-aware**——有问题未购物（how to/how does）；回报周期长，1-2 层跑通后才碰；
5. **Demand-gen/awareness**——Display/YouTube 宽泛；最后，有富余预算才上。

🔴 **不跳层**——高意图未证明前上宽泛需求=账户烧预算而 CRM/订单里什么都没有。

### 3. 品牌词与暂停测试

默认投品牌词——不投竞品会投，你付的代价是丢单不是省点击。唯一例外：**你是唯一竞价者且自然结果吃掉整个 SERP 时**，可测试暂停品牌投放，盯的是**品牌总转化（付费+自然）**而非只看付费——总量持平=你在蚕食自己可省这笔；总量掉=立刻开回。品牌预算设上限，它很少需要多，且共享预算会让品牌词吃掉一切（见下）。

### 4. 账户结构：独立预算是核心

最小可行拆分（各自**独立预算**）：

- **Brand**（独立预算——永不共享）
- **Non-brand high-intent**（一个 campaign，按解决方案分主题 ad group）
- **Competitor**（独立预算+独立文案——CPC/CVR 经济性不同）
- **Remarketing**（与 Search 分离）

**为什么必须独立预算**：共享预算下最便宜转化最高的 campaign（永远是品牌词）会饿死你真正需要数据的那些——账户纸面盈利但在所有重要地方是瞎的。

- **主题 ad group 而非 SKAG**：5-15 个共享同一意图、可由同一承诺回答的紧密关键词；两个词需要不同落地页/价值主张就拆组；每组 2-3 个 RSA；
- **合并规则**：月转化 <15-30 的 campaign 喂不饱智能出价——合并。低量级账户里「更少但喂得饱」胜过精巧结构；
- **每个新 Search campaign 默认关掉**：Search Partners 和 Display Network（证明有效前不开）；地理定位设 **"Presence"**（物理在目标地域的人——默认的 "presence or interest" 会投给只是对该地感兴趣的人）；语言定位按用户 Google 界面语言而非查询语言；
- **不自相残杀**：同一关键词同一匹配类型出现在多个 ad group 会拆散数据还互相竞价——用否定词把每个查询路由到唯一归属。

### 5. 关键词与匹配类型门禁

关键词从**买家描述问题的方式**来（销售电话语言/自家搜索词报告/竞品广告文案）——不是你描述产品的方式。「每月 50 次搜索+意图清晰」胜过「5000 次+意图混杂」。每个词标意图层级。

**匹配类型推进顺序（不可跳步）**：

1. 高意图词先上 **Phrase + Exact**（Exact 仍匹配近似变体，Phrase 是 B2B 主力），低量期用手动 CPC 或 Max Conversions；
2. 每周挖搜索词报告（仪式见下）；
3. **Broad 只在三个条件全满足后开**：campaign 月转化 30+、智能出价已上线、否定词表够紧。缺一是「给 Google 捐款」。

**AI Max for Search 同门禁**：它能匹配关键词表之外的搜索、改写广告文案、把点击导到站内其他页面（final URL expansion）——B2B 里可能把买家导到招聘页/博客。测试时：排除不该接广告流量的 URL、周检时审它选的搜索词和落地页、与无 AI Max 的 campaign 对比。

### 6. 否定词

**上线即用的启动清单**：

- **通用垃圾**：free, cheap, jobs, salary, hiring, career, intern, student, course, tutorial, training, certification, pdf, template, reddit, wiki, login（品牌 campaign 除外）
- **研究意图**："what is"/"how to"/"examples"/"meaning"/"definition"
- **品类碰撞**：与无关品类共享的词（卖 sales engagement 就否定 "employee engagement"）
- **非品牌 campaign 里否定自己的品牌**——把品牌流量路由回品牌 campaign

**匹配类型机制坑**：否定 broad 要求**所有词都在**（任意顺序）——否定 broad "free trial" **不挡**单独的 "free"；否定 phrase 挡有序短语；否定 exact 只挡完全一致查询。绝大多数误伤和漏挡都源于此。

🔴 **不过度否定**——每条否定都收窄覆盖，B2B 量级下复利很快。否定明确错误的，不否定「只是不确定」的——含糊词该先多攒数据再砍。

### 7. 每周搜索词仪式（三遍扫描）

每 campaign 每周一次：

1. **浪费**：有花费（3+ 点击）零转化的词 → 无关的否定掉；
2. **赢家**：已转化但还不是关键词的搜索词 → 以 Exact/Phrase 加进正确 ad group；
3. **漂移**：broad/phrase 匹配拉来相邻但错误含义的 → 收紧匹配类型或否定漂移。

### 8. 按转化量选出价策略

| 月转化数（campaign） | 策略 |
|---|---|
| 0-15 | 手动 CPC 或 Maximize Conversions（无目标） |
| 15-30 | Maximize Conversions |
| 30+ 稳定 | Target CPA——设在或略高于近 30 天实际值 |
| 真实收入价值回传 | Target ROAS |

经验法则：智能出价需 campaign 30 天内 ~30 次转化才能学习；tCPA 贴近实际值——激进低目标会掐死投放（Google 直接不出价了）；目标调整走 **±10-15% 步进+等 1-2 周**，每次改动重启学习期别在窗口内慌改。预算机制：campaign 单日可花**日预算 2 倍**（Google 按月平衡——单日超支正常）；预算顶死但在转化的 campaign **提预算反而降 CPA**（受限的智能出价表现差）。

### 9. 离线转化导入（B2B 单点最高杠杆，DTC 翻译为订单价值回传）

原文口径：把 CRM 结果（SQL/opportunity/closed-won）经 GCLID+offline conversion import 或原生 CRM 集成导回 Google，带真实 deal value——否则智能出价只对表单填充优化，买到垃圾线索。

**DTC 翻译**：导入**真实订单（order_id+金额/毛利）**而非平台自报转化——增强型转化（gclid/gbraid+wbraid 例外）或数据管理平台回传。理由相同：平台自报转化含 view-through/建模/重复计数，拿它训练出价=在优化虚荣指标。**CRM/订单系统是裁决方，平台内转化数永远不可信**（B2B 点击 60-180 天才成交；DTC 也有 7-30 天归因窗口+退款）。每月对账，订单系统赢。

### 10. Quality Score 与落地页

QS（1-10/关键词）= 预期 CTR+广告相关性+落地页体验。QS 低=同位置付更多钱——**先修弱组件再提价**。落地页规则：message match（页面标题回声广告承诺和查询词——不是丢通用首页）；一页一事一 CTA；速度；首屏上方放证明。**表单长度是意图门**：短表单买量低质、长限定表单买少而精——匹配你回传为转化事件的那个。

### 11. PMax 护栏（B2B 价值排序，DTC 适用但基准不同）

价值排序：**brand Search > high-intent non-brand Search > remarketing > PMax > broad demand-gen**——PMax 只在更便宜更清晰的胜利榨干后才配预算；永不首发、永不在弱追踪/小预算上跑。

护栏：账户级**品牌排除**（否则蚕食品牌 Search 还抢功）；受众信号用一方数据；上线第一天就上否定词；扩量**之前**先导入离线转化；按 campaign 查 PMax 线索的 CRM 质量——若转化率只有 Search 线索一半，PMax 是「便宜看起来贵实际上」。Google 不给视频会自动生成烂视频，须自供。

**重叠检查是常规动作**：Optmyzr 2025-02 对其管理的 503 个账户研究发现 91% 存在 Search↔PMax 完全关键词重叠（覆盖 5768 个 Search campaign 的 56%）——这是重叠普遍性证据不是花费成本证据；要量化自己账户：拿 PMax search-terms insights 对 Search 关键词，找品牌词和高意图词这类 Search 能更便宜赢的。

### 12. 基准与周记分卡

原文 B2B SaaS Search 区间（故意放宽——锚定自家前 30 天）：brand CTR 8-20%/CVR 15-40%；non-brand high-intent CTR 2-6%/CVR 3-10%/CPC $8-40+/CPL $80-400+；竞品词 CPC 更高 CVR 更低。**DTC 口径须自标定**——Momcozy 品类（母婴耐用品）搜索意图和客单价与 B2B SaaS 完全不同。

周记分卡固定八个数：**spend·转化·CPL/CPA·转化→成交率·成交数·单成本站本·Search 展示份额·最大浪费搜索词**。诊断：**Lost IS (budget)** vs **Lost IS (rank)** 区分「钱不够」还是「Ad Rank 不够」——不同问题不同解法。八个数健康且趋势对=账户健康。

## 高频问答索引

- **Q：Google Search 预算先投哪里？**
  A：意图阶梯逐层解锁——brand（常开）→high-intent non-brand（利润中心）→competitor（须对比页）→problem-aware→demand-gen。跳层=烧预算。Search 收割需求不创造需求，品类搜索量近零就把预算放上游社媒。
- **Q：品牌词投不投？**
  A：默认投——不投竞品投你付丢单代价。唯一例外：你是唯一竞价者且自然结果吃掉整个 SERP 时测暂停，看品牌总转化（付费+自然）不只看付费。品牌预算独立不共享。
- **Q：广泛匹配什么时候能开？**
  A：三个条件全满足——campaign 月转化 30+、智能出价已上线、否定词表够紧。缺一是给 Google 捐款。推进顺序：Phrase+Exact 起步→周检搜索词→条件满足才上 Broad。AI Max 同门禁且要排除不该接流量的 URL。
- **Q：共享预算为什么是坑？**
  A：最便宜转化最高的 campaign（永远是品牌词）会饿死需要数据的 campaign——账户纸面盈利但重要地方全瞎。Brand/Non-brand/Competitor/Remarketing 各自独立预算。
- **Q：PMax 会不会蚕食品牌 Search？**
  A：会——须账户级品牌排除+受众信号+上线即否定词+先导离线转化再扩量。Optmyzr 研究 91% 账户存在 Search↔PMax 完全关键词重叠。价值排序 brand>non-brand>remarketing>PMax>demand-gen。

## 相关卡片

- [dsite-sem-ads-playbook.md](./dsite-sem-ads-playbook.md) — 独立站 SEM 架构层（S22；本卡管 Google Search 账户内部运营）
- [attribution-measurement.md](../fundamentals/attribution-measurement.md) — 归因测量体系（离线转化导入的「为什么」在那张卡）
- [payback-period-budget-gate.md](../fundamentals/payback-period-budget-gate.md) — payback 闸门（同批 S25；预算能不能投的财务判据）
