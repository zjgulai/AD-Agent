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

### Q21. Amazon 新品广告架构怎么搭？
**A**：SP-Auto（自动挖数据，20%）+ SP-Exact（核心出单，35%）+ SP-Broad（拓流量，20%）+ SP-ASIN（竞品定向，15%）+ SD-Retarget（再营销，10%）；Month 3+ 追加 SB-Brand 品牌词防御、SBV 视频、SD-Compete 竞品页拦截。
> 溯源：`cards/platform-ops/amazon-ads-operations.md`（CBE:amazon-ad-architecture）

### Q22. Amazon 广告出价怎么定？
**A**：Exact=建议 CPC 的 80-100%、Phrase 60-80%、Broad 50-70%、Auto 系统建议价、ASIN 定向 $0.50-1 起。14 天数据后按 ACoS 调：优→+10-20%，差→-20% 或暂停；新建 Exact 组出价=该词实际 CPC 的 110-120%。
> 溯源：`cards/platform-ops/amazon-ads-operations.md`（CBE:amazon-ad-architecture）

### Q23. Amazon 每周广告复盘看什么？
**A**：本周 vs 上周 vs 月均 KPI（ACoS/TACoS/CTR/CVR/CPC/自然单占比）→ Campaign 红绿灯（绿保持/黄调优/红降 20% 或暂停）→ STR 收割（高转化词提 Exact、烂词否定）→ 出价预算调整 → SB new-to-brand+SD 受众拆分 → Prompts 被动扣费单列 → 竞品扫描 → P0/P1/P2 清单。
> 溯源：`cards/platform-ops/amazon-ads-operations.md`（CBE:amazon-weekly-ad-review）

### Q24. Amazon 广告 CTR/CVR 健康线是多少？
**A**：Amazon 口径 CTR>0.4%（<0.3% 优化文案图）、CVR>10%（<8% 优化 Listing）、TACoS 健康带 8-15%、>25% 过度依赖广告——与 Meta 口径不同勿混用。
> 溯源：`cards/platform-ops/amazon-ads-operations.md`（CBE:amazon-weekly-ad-review）

### Q25. Amazon 冷启动账户前 14 天能频繁调吗？
**A**：不能。新像素前 100 个事件决定机器学习方向；日预算≥目标 CPA 5 倍；Day1-3 装像素预热→Day4-14 投 Traffic/Engagement 攒数据→Day15-30 切 Purchase 转化目标；扩量每次增幅≤20%、间隔≥3 天。
> 溯源：`cards/platform-ops/amazon-ads-operations.md`（CBE:dsite-sem-ads 冷启动 SOP + amazon-ad-architecture）

### Q26. Prompts 广告会偷偷花钱吗？
**A**：会。2026-03-25 起美国 SP/SB campaign 自动注册 Prompts 广告、沿用父 campaign 竞价 CPC 计费、无独立出价、文案 AI 自动生成——预算已在 AI 对话位花钱，必须纳入预算与周检（Ads Console→Reports→Prompts）。
> 溯源：`cards/platform-ops/amazon-ads-operations.md`（CBE:amazon-ad-architecture + amazon-ad-diagnosis + amazon-weekly-ad-review）

### Q27. Amazon 广告 TACoS 多少算健康？
**A**：8-15% 视阶段健康，>25% 过度依赖广告需提升自然位/品牌建设。周复盘关键判断：TACoS 降+自然单占比升=健康增长；TACoS 升+自然占比降=广告依赖加深。
> 溯源：`cards/platform-ops/amazon-ads-operations.md`（CBE:amazon-weekly-ad-review）

### Q28. Amazon 周复盘调了还是不行说明什么？
**A**：结构性问题——品牌词 CPC 持续升+搜索量不增=单渠道天花板（需品牌建设）；ACoS>盈亏平衡线持续 30 天+=结构性亏损；TACoS>25%=广告依赖。转深度诊断（市场/词库/Listing/广告四位一体 pipeline），不再周调。
> 溯源：`cards/platform-ops/amazon-ads-operations.md`（CBE:amazon-ad-diagnosis）

### Q29. Amazon 关键词怎么分层建词库？
**A**：T1 主力词（CVR>目标稳定出单→Exact 高竞价）/ T2 锚位词（流量中等转化向好→Phrase）/ T3 长尾词（精准但量低→只进 Listing 不开精准）。筛选四维：搜索量/CPC/竞争度/转化意图。数据源优先级：SQP/OPQ（Brand Registry 一方数据）>前台扒词>第三方估算。
> 溯源：`cards/platform-ops/amazon-keyword-listing-ops.md`（CBE:amazon-keyword-research + amazon-ad-diagnosis）

### Q30. Amazon 标题最多多少字符？
**A**：≤75 字符含空格（2026-07-27 起非媒体类目统一，旧分类目上限失效）。同词≤2 次（复数算重复）；长尾/场景词迁 Item Highlights（≤125 字符，可被搜索索引）。超限标题会被 Amazon 逐步 AI 改写。
> 溯源：`cards/platform-ops/amazon-keyword-listing-ops.md`（CBE:amazon-keyword-research + amazon-ad-diagnosis）

### Q31. Amazon 后台 Search Terms 怎么填？
**A**：<250 字节按 UTF-8 字节算（建议≤249 留白），空格分隔不用逗号。只放标题/BP 未覆盖的同义词/长尾/多语言词；严禁品牌名（含自有）、ASIN、临时词（new/on sale）、主观词（best/cheapest）——违者 ASIN suppression+影响 Account Health。
> 溯源：`cards/platform-ops/amazon-keyword-listing-ops.md`（CBE:amazon-keyword-research）

### Q32. Amazon 五点描述有什么硬规则？
**A**：每条 10-255 字符（200-255 不算超长勿砍）。BP1 必须是最大卖点（VOC 提及率高×满意度低的痛点）；前 3-4 词写 Benefit 非 Feature；T1 词覆盖 100%、T2 ≥70%；每条嵌一个使用场景/痛点词。
> 溯源：`cards/platform-ops/amazon-keyword-listing-ops.md`（CBE:amazon-ad-diagnosis + amazon-listing-copywriter）

### Q33. Amazon 广告数据怎么反哺 Listing？
**A**：闭环——广告跑出高转化词→查 Listing 是否覆盖，未覆盖立即嵌入标题/BP/ST；高花费 0 转化词→查是否误导匹配，否定该词+修正文案。Listing 关键词覆盖目标：T1 100%/T2 70%+。
> 溯源：`cards/platform-ops/amazon-keyword-listing-ops.md`（CBE:amazon-ad-diagnosis）

### Q34. Amazon 否定词阈值和分类怎么定？
**A**：运营期三类——属性不符词/用途不符词/品牌不符词（Negative Exact/Phrase 分治）。阈值：花费>2×目标 CPA 且 0 转化→Negative Exact；CTR<0.2% 且曝光>1000→查匹配度；需 ≥20-30 次点击数据量再判。投放前三层法见 amazon-ads-playbook 卡。
> 溯源：`cards/platform-ops/amazon-keyword-listing-ops.md`（CBE:amazon-keyword-research + amazon-ad-diagnosis）

### Q35. 独立站投广告先选哪个平台？
**A**：按产品类型——视觉型→Meta/Pinterest/TikTok、功能型→Google Search/YouTube、高客单→Google Search、标品→Google Shopping、小众→Meta/TikTok/Reddit、日本→LINE 必投。按预算：$1-3k/月单平台集中、$3-10k 主70%+辅30%、$10k+ 多平台矩阵。
> 溯源：`cards/platform-ops/dsite-sem-ads-playbook.md`（CBE:dsite-sem-ads）

### Q36. Google Ads 新账户怎么搭架构？
**A**：6 Campaign——Brand Search（品牌防御）、Non-Brand Search（品类/问题/竞品词三 Ad Group）、Shopping（Best Sellers/New/Sale 分组）、Performance Max（有转化数据后上）、Display Remarketing（弃购1-3d/浏览4-14d/老客15-30d）、YouTube（认知+考虑）。Meta 侧对应 5 Campaign 按 TOF/MOF/BOF/Retention/Testing 分层。
> 溯源：`cards/platform-ops/dsite-sem-ads-playbook.md`（CBE:dsite-sem-ads）

### Q37. AIPL 漏斗预算怎么分？新品牌和成熟期差别？
**A**：新品牌 A15-20%/I20-25%/P45-55%/L5-10%（P 是转化主战场）；冷启动 M1-3 A/I 各 25% 向 P 倾斜（预算$3-10k/月），成熟期 M9+ P 升至 55%、L 升至 15%（$30k+）。Google 广告类型优先级：Search>Shopping>Display>Video>DemandGen>Pmax。
> 溯源：`cards/platform-ops/dsite-sem-ads-playbook.md`（CBE:dsite-sem-ads）

### Q38. 新广告账户学习期前 14 天注意什么？
**A**：Day1-3 装像素全事件预热；Day4-14 投 Traffic/Engagement 攒 LPV/ATC（先优化 ATC 不切 Purchase）；日预算≥目标 CPA 5 倍；前 14 天不频繁调整；新像素前 100 事件定学习方向；Day31+ 扩量每次≤20%、间隔≥3 天。
> 溯源：`cards/platform-ops/dsite-sem-ads-playbook.md`（CBE:dsite-sem-ads）

### Q39. 大促 SEM 怎么打？
**A**：T-4 周预热（策划/预算/素材/受众预建/素材测试/竞品情报/落地页/库存）；大促期 Brand Search 40-50%+Shopping 30-40%+Pmax 10-15%，出价+15-30%；实时监控销售额/CVR/CPA/库存/TTFB/竞品并配触发器（品牌词激增>200% 追加预算、素材 CTR>均值2倍追加、网站 503 停全部广告）；T+1 归档再营销、T+3 预算恢复。
> 溯源：`cards/platform-ops/dsite-sem-ads-playbook.md`（CBE:dsite-sem-ads）

### Q40. SEM 和 SEO 怎么协同？
**A**：双向数据赋能（月度交叉：SEM 高转化词优先 SEO 覆盖、SEO 高曝光低点击词 SEM 补位）+SERP 双重占位（SEO 1-3 名降/停 SEM、10+ 名 SEM 补位、品牌词始终投防截流）+PMF 验证链（SEM 验需求→验产品→验受众→验规模→SEO 长期布局）。统一 KPI=搜索渠道总利润，避免内部竞价和资源浪费。
> 溯源：`cards/platform-ops/dsite-sem-ads-playbook.md`（CBE:dsite-sem-ads）

### Q41. LTV 口径下 CPA 承受线怎么算？
**A**：最大可接受 CPA=LTV×目标利润率；LTV=首购 AOV×(1+复购率×平均复购次数)。例 AOV$60、复购率30%×2次→LTV$96、利润率40%→CPA 上限 $38.4。预算规划用 LTV 口径，日常优化用 ROAS 口径。
> 溯源：`cards/platform-ops/dsite-sem-ads-playbook.md`（CBE:dsite-sem-ads）

### Q42. TikTok 爆款视频怎么批量产？
**A**：六叙事公式选 2-3 主力（F1痛点/F2惊喜/F3对比/F4测评/F5生活方式/F6互动）+六类 Hook（痛点共鸣/结果前置/争议/身份认同/FOMO/情绪触发；3秒完播率合格>40%/良好>55%/优秀>70%，每视频备3版Spark Ads A/B）+流量池递进（L1完播>30%→L2互动>5%→L3互动>8%分享>2%→L4爆款100K+）+70/30 内容矩阵（70%开箱/教程/测评/对比，30%生活方式/热点/互动）。
> 溯源：`cards/platform-ops/tiktok-content-ads-playbook.md`（CBE:tiktok-growth）

### Q43. TikTok 达人和广告怎么配合放大？
**A**：五层策略——L1蓄水头部100K+ 20%/L2破圈中腰部10K-100K 30%/L3种草垂直达人 20%/L4转化带货达人 20%/L5投流Spark Ads放大 10%；启动顺序 L2/L3→L4→L1→L5。阶段预算：Launch 达人70%+广告30%（$20-50/天）→Growth 50/50（$100-500/天）→Scale 达人40%+广告60%（$500+/天）。达人 SOP：筛选→外联→协商→寄样→24h 审核→48h 跟踪→周复盘。
> 溯源：`cards/platform-ops/tiktok-content-ads-playbook.md`（CBE:tiktok-growth）

### Q44. TikTok 广告测试四步法是什么？
**A**：Broad Reach（宽泛受众仅限国别+年龄+性别，5-10条素材 $20-30/条/天 3-5天，CPA>目标2倍淘汰）→Demographic（基于Step1转化画像细化兴趣标签，优胜3-5条 $30-50/组）→Cohort（自定义受众/购买Lookalike，$50-100/组 5-7天）→Targeted放量（最佳人群组合，每次加码≤20%，每周新素材2-3条防疲劳）。全程以 Complete Payment 为优化目标。
> 溯源：`cards/platform-ops/tiktok-content-ads-playbook.md`（CBE:tiktok-growth）

### Q45. TikTok Spark Ads 和信息流广告怎么选？
**A**：Spark Ads 加热已有达人/自有内容——原生真实、互动归原视频、CPM 通常更低，适合爆款放大，建议占广告预算 40-50%；In-Feed Ads 全新创建素材——可更商业化、互动归广告、CPM 较高，适合精准转化，占 50-60%。
> 溯源：`cards/platform-ops/tiktok-content-ads-playbook.md`（CBE:tiktok-growth）

### Q46. TikTok 广告 CPA/ROAS 承受线怎么算？
**A**：最大可承受 CPA=最低售价÷单位利润（最低售价=售价−平台佣金−物流成本，单位利润=最低售价−产品成本−包装成本）；最低 ROAS=售价÷单位利润；盈亏平衡 ROAS=最低 ROAS+0.2~0.5 安全边际（保守+0.5/均衡+0.3/激进+0.2）。例售价$30→CPA上限约$1.78、最低ROAS≈2.6、盈亏平衡2.8-3.1。
> 溯源：`cards/platform-ops/tiktok-content-ads-playbook.md`（CBE:tiktok-growth）
