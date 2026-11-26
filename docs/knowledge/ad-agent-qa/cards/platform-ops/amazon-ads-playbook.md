---
title: Amazon 广告打法（ACoS/TACoS + AI 广告能力 + 诊断闭环 + SB/SP 协同）
doc_type: knowledge
module: ad-agent-qa
topic: amazon-ads-playbook
status: review
created: 2026-11-26
updated: 2026-11-26
owner: self
source: human+ai
source_docs: [PO:metric-amazon-acos-us, PO:metric-amazon-tacos-us, PO:capability-amazon-ads-prompts-us, PO:capability-amazon-sponsored-brands-collections-us, PO:experiment-amazon-ads-diagnostic-loop-us, PO:experiment-amazon-prelaunch-negative-keyword-filtering-us, PO:experiment-amazon-sb-sp-coordination-scaling-us, PO:experiment-amazon-cosmo-rufus-readiness-us]
fetched_at: 2026-11-26
---

# Amazon 广告打法（ACoS/TACoS + AI 广告能力 + 诊断闭环 + SB/SP 协同）

## 核心问题

Amazon 广告和 Meta 信息流广告的思路有什么不同？ACoS 和 TACoS 怎么分工？Amazon 的 AI 广告新能力（Rufus prompts、SB collections 自动生成）是什么？广告诊断应该按什么顺序走？新品上线前怎么做否定词？SP-only 卡住时 SB 能解决什么？

## 系统解答

### 1. 文档定位

蒸馏自 platform-ops-wiki 的 Amazon 对象组：2 指标卡（ACoS/TACoS）+ 2 能力卡（Ads Prompts、SB Collections）+ 4 实验记录（诊断闭环、否定词前置、SB/SP 协同、COSMO/Rufus readiness）。全部 `status: review`、`market: us`。

**与现有 KB 的关系**：现有诊断体系（L0-L4/G0-G8）是 Meta 的「转化漏斗+竞价」模型；Amazon 是「搜索意图+商品页承接」模型，诊断顺序完全不同。本卡给出 Amazon 侧的打法层框架。

### 2. 核心指标分工：ACoS 看广告，TACoS 看经营

| 指标 | 公式 | 回答的问题 | 误用 |
|------|------|-----------|------|
| **ACoS** | 广告花费 ÷ 广告归因销售额 | 广告效率：广告销售额中多少被成本吃掉 | 它是广告效率指标，**不是利润指标** |
| **TACoS** | 广告花费 ÷ 总销售额 | 经营结构：广告对整体销售的侵蚀程度 | TACoS 降但自然单不涨=广告只是在买单 |

- **ACoS 信号**：Good=低于 SKU 可承受阈值且没牺牲增长；Warning=快速上升但自然位/CTR/CVR 没同步改善；Bad=长期高于毛利承受线且没带动自然增长或评论沉淀。
- **TACoS 信号**：Good=TACoS 降且总销售/自然单升；Bad=TACoS 高不降=广告依赖加深但品牌资产没沉淀。
- **必须联合看**：ACoS 要和 TACoS、CVR、自然位变化一起看，不能单看；TACoS 要和 sessions、unit session percentage、CVR 一起看。

### 3. AI 广告能力：从关键词匹配到意图满足

Amazon 官方方向明确：广告能力在向「可被 AI 理解、提示、引用的内容」倾斜（COSMO/Rufus 实验记录的官方信号印证）。

- **Amazon Ads Prompts**（SP/SB，2026 美国 GA）：广告可在 **Rufus 对话式购物**中被触发——从传统检索触发延伸到问题驱动触发。约束：不是所有商品适配，**更依赖「可解释卖点」而非关键词堆积**；仍受 PDP 内容质量约束。
- **AI-powered Sponsored Brands Collections**：根据 landing page、关键词、商品、图像**自动生成 collection 创意**，15 分钟内形成可投放版本。美/加/英/德/法/意/西/日可用。约束：生成效率高≠内容最优，仍需人工审核品牌叙事与合规。
- **核心判断（COSMO/Rufus 实验）**：广告不再适合「救差链接」，而是**放大器**——只会放大已具备成交确定性的链接。「广告是显微镜，不是急救包」。

### 4. 诊断闭环：固定顺序，不看单点 ACoS

实验记录给出的诊断顺序（`SKU → 投放 → 搜索词 → 广告位`）：

1. **推广的商品 + 业务 + 库存报告**：确认重点优化 SKU（不同 SKU 的 CPC/CTR/CVR/毛利差异大，不能用统一 bid 思路）
2. **定位报告**：判断投放词/商品投放是否有继续意义
3. **搜索词报告**：区分高转化词与低转化词
4. **广告位报告**：只对数据充足、转化高的位置加价

**决策逻辑**：`ACOS = CPC / CR / 客单价`；词有点击无转化→先判相关性再存档/观察；词有转化但 ACoS 亏本→先降 bid 不盲目扩量；词效果优排名可提→提价幅度控制 **10%-20%**；广告位高转化且数据充足→做 placement uplift。

**样例数据观察**（内部周报）：Auto campaign 有单日 ACoS 约 3%-8%；存在「有花费但 0 销售」的 burn day；高销售 SKU≠高效率 SKU。

### 5. 投放前否定词：先切 wrong traffic，再谈扩量

实验记录的方法论：新品启动前先做 `wrong traffic suppression`，不是投后被动止损。

- **产品边界定义**：先定义「我们卖什么 / 我们绝不是什么」（例：memory foam 旅行枕 vs inflatable 充气枕——材质/结构/用途完全冲突）
- **三层分组**：
  - **A 组·属性完全冲突**（inflatable/beads/water）→ Negative Phrase
  - **B 组·品牌防御**（强忠诚品牌词，新品评论基础弱时）→ 自动/广泛中 Negative Phrase
  - **C 组·场景/配件纠偏**（travel pillow case、foot rest）→ Negative Exact，避免误伤长尾
- **语义风控**：防止把 `support/sleeping/pain relief` 等核心转化词误杀；Phrase 和 Exact 分开处理不一刀切
- **失败模式**：过度否定杀掉高价值大词；只看词面不看产品真实边界；竞品品牌词全否导致抢量路径过窄

### 6. SB + SP 协同：SB 抢解释权，SP 收割确定性

内部案例（证据级 `internal-playbook`）：产品早期只跑 SP 转化低亏损，**引入 SB 后月单量到 1500+，SB 贡献近 20% 订单并帮自然位进类目前 25**。

- **分工**：SP=低漏损成交工具（高意图确定性词）；SB=高意图大词与品牌叙事入口（解释权+自然位助推）
- **判断**：SP 已能稳定吃高意图词但大词/类目词无品牌心智位→可引入 SB；SB 素材能更好回答用户问题建立场景差异化→自然位外溢价值更强；高成本 SB 只带点击不拉搜索/加购/自然位→收缩
- **素材洞察**：普通红人实拍素材转化优于「华丽」竞品素材——**素材适配性大于创意华丽度**

### 7. 放量前 Readiness：链接确定性先于广告预算

COSMO/Rufus 实验的 checklist——回答「这个链接是不是确定性答案，再问要不要加广告」：

1. 主要搜索意图是否已被标题/图片/A+/QA 完整覆盖
2. 评论区是否有大量未解释的负面疑问
3. 加购率、转化率是否已进入可放量安全区
4. 是否存在「边界未解释」问题（适配性、使用条件、安全边界）

失败模式：流量下滑直接加预算没先修链接；关键词覆盖多但页面不能被 AI 快速抽取成答案；CTR 还行但点击后加购/停留/转化差还硬推。

## 高频问答索引

- **Q：ACoS 和 TACoS 有什么区别？**
  A：ACoS=广告花费÷广告归因销售额，衡量广告效率；TACoS=广告花费÷总销售额，衡量广告对整体销售结构的侵蚀。ACoS 要和 TACoS/CVR/自然位一起看，不能单看。
- **Q：Amazon 广告诊断应该按什么顺序？**
  A：SKU（推广商品+业务+库存报告）→ 投放词（定位报告）→ 搜索词报告 → 广告位报告。提价幅度 10%-20%，只对数据充足高转化位加价。
- **Q：新品 Amazon 广告上线前怎么做否定词？**
  A：先定义产品边界（卖什么/绝不是什么），把竞品流量词分三层：A 属性完全冲突→Negative Phrase；B 品牌防御→Negative Phrase；C 场景/配件纠偏→Negative Exact。加语义风控防误杀核心词。
- **Q：只跑 SP 亏损，SB 能救吗？**
  A：SB 不是替代 SP，是分工：SP 收割确定性高意图词，SB 抢大词入口和品牌叙事、助推自然位。内部案例 SB 协同后月单 1500+、自然位进前 25。前提是 PDP 承接力够、素材能回答用户问题。
- **Q：Amazon Ads Prompts 和 SB Collections 自动生成是什么？**
  A：Prompts=广告可在 Rufus AI 对话购物中被触发（SP/SB，美国 GA），依赖可解释卖点而非关键词堆砌；SB Collections=根据 LP/关键词/商品/图片自动生成品牌合集创意，15 分钟可投放，但仍需人工审核品牌叙事与合规。
- **Q：Amazon 广告是「放大器」还是「急救包」？**
  A：放大器。COSMO/Rufus 实验结论：广告不再救差链接，只放大已具备成交确定性的链接。先做 readiness checklist（意图覆盖/评论疑问/加购转化/边界解释）再加预算。
- **Q：Amazon 广告和 Meta 广告诊断思路一样吗？**
  A：不一样。Meta 是转化漏斗+竞价诊断（L0-L4），Amazon 是搜索意图+PDP 承接诊断，且多了 TACoS 经营视角、否定词前置、SB/SP 协同这些 Meta 没有的结构。

## 相关卡片

- [TikTok Shop 广告增长打法](tiktok-shop-growth-playbook.md) — 另一平台打法对照
- [母婴跨平台增长 Overlay](baby-maternity-growth-overlay.md) — Amazon PDP/评论体系在母婴类目的合规要求
- [Meta 广告诊断与优化 SOP](../meta-ads-diagnosis/meta-diagnosis-sop.md) — Meta 侧诊断体系（S4）
- [广告竞价全链路流程图](../fundamentals/ad-bidding-full-chain.md) — 通用竞价机制（S10）
- 知识图谱：`ad:metric:amazon-{acos,tacos}` / `ad:adproduct:amazon-{ads-prompts,sponsored-brands}` / `ad:asset:pops-exp-amazon-*`（platform-ops-kb 分片）
