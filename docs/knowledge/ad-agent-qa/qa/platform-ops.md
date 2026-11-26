---
title: Q&A 数据集 - 平台运营知识（platform-ops-kb 蒸馏）
doc_type: knowledge
module: ad-agent-qa
topic: qa-platform-ops
status: review
created: 2026-11-26
updated: 2026-11-26
owner: self
source: human+ai
---

# 平台运营 Q&A

覆盖 `cards/platform-ops/`（4 卡：tiktok-shop-growth-playbook、amazon-ads-playbook、creator-commerce-compliance、baby-maternity-growth-overlay）。来源为 platform-ops-wiki 知识库对象（PO:*），全部 `status: review`，高风险结论已在卡内标注证据边界。

### Q1. TikTok Shop 现在还能投 Video Shopping Ads 吗？
**A**：2025-07 起 GMV Max 成为 TikTok Shop Ads 默认且唯一受支持的 campaign type，旧的 VSA/PSA/LSA 会被暂停或受影响。每个 shop 仅一个 primary ad account 可获 GMV Max 权限。
> 溯源：`cards/platform-ops/tiktok-shop-growth-playbook.md`（PO:capability-tiktok-gmv-max-us）

### Q2. GMV Max 的 ROI 和老 campaign 能直接比吗？
**A**：不能。GMV Max 把 campaign 期间相关商品的 organic 和 paid 订单都计入归因——先厘清口径再对比，否则会高估或低估真实效率。
> 溯源：`cards/platform-ops/tiktok-shop-growth-playbook.md`

### Q3. SPS/NBFR/VoC Index 是什么？SPS 低于多少不能做 affiliate？
**A**：三个 TikTok Shop 准入指标——SPS（店铺健康分，<3.0 可能被取消 affiliate 资格、<3.5 不进标准扩张）、NBFR（非买家责任退货退款率，影响 SPS 和商品可见性）、VoC Index（商品声音风险，超门槛移出 affiliate eligibility）。公式未公开，按官方门槛使用。
> 溯源：`cards/platform-ops/tiktok-shop-growth-playbook.md`（PO:metric-tiktok-*）

### Q4. TikTok affiliate 放量前要检查什么？
**A**：SPS≥3.5、商品 product qualification、creator eligibility 与披露路径、seller 责任、内容合规、类目额外要求、评论层安全/信任风险。输出 `ready/conditional/blocked` + blocking reasons + required fixes。
> 溯源：`cards/platform-ops/tiktok-shop-growth-playbook.md`（PO:scenario+workflow-tiktok-affiliate-*）

### Q5. GMV Max 能自动帮我选品和写脚本吗？
**A**：不能。它是放量层，承接已验证的商品与内容信号；选品判断和脚本质量仍需上游保证。达人数据要先结构化（SKU/creator/date/angle）再接入放量——先结构化经营，再自动化扩量。
> 溯源：`cards/platform-ops/tiktok-shop-growth-playbook.md`（PO:experiment-tiktok-creator-tracking-and-gmv-max-us）

### Q6. ACoS 和 TACoS 怎么分工？
**A**：ACoS=广告花费÷广告归因销售额（广告效率），TACoS=广告花费÷总销售额（经营结构/广告侵蚀度）。ACoS 要和 TACoS/CVR/自然位一起看；TACoS 降但自然单不涨=广告只是在买单。
> 溯源：`cards/platform-ops/amazon-ads-playbook.md`（PO:metric-amazon-*）

### Q7. Amazon 广告诊断按什么顺序？
**A**：SKU（推广商品+业务+库存报告）→ 投放词（定位报告）→ 搜索词报告 → 广告位报告。提价幅度 10%-20%，只对数据充足高转化位加价；`ACOS=CPC/CR/客单价`。
> 溯源：`cards/platform-ops/amazon-ads-playbook.md`（PO:experiment-amazon-ads-diagnostic-loop-us）

### Q8. Amazon 新品上线前怎么做否定词？
**A**：先定义产品边界（卖什么/绝不是什么），竞品词分三层——A 属性完全冲突→Negative Phrase；B 品牌防御→Negative Phrase；C 场景/配件纠偏→Negative Exact。加语义风控防误杀 `support/sleeping` 等核心词。
> 溯源：`cards/platform-ops/amazon-ads-playbook.md`（PO:experiment-amazon-prelaunch-negative-keyword-filtering-us）

### Q9. Amazon 只跑 SP 亏损，SB 能救吗？
**A**：SB 不是替代 SP 是分工：SP 收割确定性高意图词，SB 抢大词入口+品牌叙事+助推自然位。内部案例 SB 协同后月单 1500+、自然位进前 25。前提是 PDP 承接力够、素材能回答用户问题。
> 溯源：`cards/platform-ops/amazon-ads-playbook.md`（PO:experiment-amazon-sb-sp-coordination-scaling-us）

### Q10. Amazon Ads Prompts 和 SB Collections 自动生成是什么？
**A**：Prompts=广告可在 Rufus AI 对话购物中被触发（SP/SB，美国 GA），依赖可解释卖点；SB Collections=根据 LP/关键词/商品/图片自动生成品牌合集创意，15 分钟可投放，仍需人工审核品牌叙事与合规。
> 溯源：`cards/platform-ops/amazon-ads-playbook.md`（PO:capability-amazon-*）

### Q11. Amazon 广告是放大器还是急救包？
**A**：放大器。先做 readiness checklist（搜索意图覆盖/评论负面疑问/加购转化安全区/边界解释）再加预算——广告不救差链接，只放大已具备成交确定性的链接。
> 溯源：`cards/platform-ops/amazon-ads-playbook.md`（PO:experiment-amazon-cosmo-rufus-readiness-us）

### Q12. FTC 对达人披露的要求是什么？
**A**：material connection（付费/样品/折扣/返点/雇佣/亲属关系）必须 clear and conspicuous 披露；视频画面+语音双披露、直播周期重复；`sp/collab/thanks` 模糊词不合规；责任在 creator 本人，不能依赖品牌或平台代披露。
> 溯源：`cards/platform-ops/creator-commerce-compliance.md`（PO:rule-ftc-endorsement-disclosures-us）

### Q13. organic 达人内容能直接投广告吗？
**A**：不能默认。organic 可发≠paid amplification 允许。需过：授权完整、披露无风险、LP CVR 达标、faq_gap 可被内容或 LP 回答、类目非高风险——Meta 放大工作流有 7 条质量检查+4 个人工审批门。
> 溯源：`cards/platform-ops/creator-commerce-compliance.md`（PO:workflow-meta-creator-amplification-us）

### Q14. creator brief 应该包含什么？
**A**：六必备块 objective/audience/allowed narrative/must-answer-faq-gaps/forbidden claims/disclosure placement/CTA route + route block（study-only→amplification-ready）+ 平台差异化要求。quote 未就绪时不得偷带报价或复用权限假设。
> 溯源：`cards/platform-ops/creator-commerce-compliance.md`（PO:workflow-creator-brief-assembly-us）

### Q15. Meta Partnership Ads / IG Creator Marketplace / Shopify Collabs / YouTube Shopping 各解决什么？
**A**：Partnership Ads=creator 内容授权后放 Ads Manager 做 paid amplification；IG Creator Marketplace=官方 creator 发现撮合；Shopify Collabs=独立站 affiliate 招募+归因+佣金一体化；YouTube Shopping Collections=创作者商品合集承接 Shorts/长视频流量。都是「内容→商业化」管道，都不替代内容质量与 LP 承接。
> 溯源：`cards/platform-ops/creator-commerce-compliance.md`（PO:capability-*）

### Q16. TikTok Shop 母婴商品上架有什么门槛？
**A**：三层——general category qualification（类目准入）、designated listing-level（睡衣/监视器/安全座椅/推车/背带/家具/安抚奶嘴/磨牙/护肤/防晒等逐 SKU 文档审核，需 CPC/CPSC 证据）、invite-only（纸尿裤类）。吸奶器需先确认是否触发 designated 级。
> 溯源：`cards/platform-ops/baby-maternity-growth-overlay.md`（PO:overlay-baby-and-maternity-us）

### Q17. 母婴广告文案绝对不能写什么？
**A**：「绝对安全」「零风险」「医生推荐」等未证实表述；医疗/治疗工具化表达；模糊年龄/承重/使用边界；材质/无毒/过敏友好无证据表述。安全边界前置到正文而非 FAQ；评论区出现安全质疑时创意内容不得自行 rebuttal。
> 溯源：`cards/platform-ops/baby-maternity-growth-overlay.md`

### Q18. Momcozy 案例证明了什么？
**A**：L1 级公开观察：M9 吸奶器存在「自有站承接+hands-on 长评+sponsored/affiliate 披露+YouTube review+TikTok 场景样本」完整链路。可复用的是结构假设（niche review+DTC proof+short-form sample+FAQ capture），不是「已验证有效」的结论。
> 溯源：`cards/platform-ops/baby-maternity-growth-overlay.md`（PO:case-momcozy-pumping-milk-wearable-pump-review-pattern-us）

### Q19. 母婴产品评论区出现安全质疑怎么处理？
**A**：视为合规+客服联动事件。创意内容不得自行 rebuttal，必须切回证据链、客服话术和合规审核；高频质疑集中在 setup/app/login/FSA 等 adoption friction 时，PDP/LP 必须前置这些信息。
> 溯源：`cards/platform-ops/baby-maternity-growth-overlay.md`

### Q20. 母婴类目跨平台上架顺序怎么定？
**A**：can-sell（资质）→ can-claim（证据）→ can-explain（DTC proof+长评）→ can-amplify（creator route 有 disclosure+guardrail）→ can-convert（LP/PDP 答 FAQ）。高解释成本优先 DTC proof+YouTube review/TikTok sample，高搜索意图才优先 Amazon。
> 溯源：`cards/platform-ops/baby-maternity-growth-overlay.md`（PO:scenario-baby-and-maternity-cross-platform-growth-us）
