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

### Q47. COSMO 算法对 Amazon Listing 有什么影响？
**A**：COSMO 是 Amazon Science 公开的电商常识知识系统——平台从「匹配商品文本」升级为「理解商品常识+用户任务+需求关系」。Listing 要从词覆盖升级为语义覆盖：讲清产品-场景-属性-问题-证据的关系，不是埋更多词。
> 溯源：`cards/platform-ops/amazon-listing-semantic-ops.md`（WB:amazon-listing-builder）

### Q48. Alexa/Rufus 时代 Listing 要怎么变？
**A**：四个转变——关键词覆盖→语义覆盖（每词有对应语义模块）、产品名→用户任务（列 5 个任务全覆盖）、卖点声明→证据支撑（UV resistant 要证明为什么）、短词→自然语言问题（QA 板块权重提升、A+ 做场景语义模块）。
> 溯源：`cards/platform-ops/amazon-listing-semantic-ops.md`（WB:amazon-listing-builder）

### Q49. Amazon Listing 八步工作流是什么？
**A**：准备三库（1关键词分层词库/2用户问题库/3卖点证据库）→生成五件（4标题3版/5五点决策链/6描述A+7段式/7 ST差集补充/8 QA答案型）→校验四项（合规/关键词覆盖/语义覆盖/转化逻辑）。铁律：禁止跳过三库直接让 AI 写——没有词库和证据库 AI 只会写漂亮废话。
> 溯源：`cards/platform-ops/amazon-listing-semantic-ops.md`（WB:amazon-listing-builder）

### Q50. 五点描述怎么写才不是卖点罗列？
**A**：按决策链写——每点对应一个用户疑虑+一个核心卖点（用户会问什么→我们怎么回答），建议结构=用途/场景/功能/材质安全/边界（第5条边界最重要）。禁空话（high quality/easy to use）；红线：emoji/特殊字符/竞品品牌名=政策违规必扣分。
> 溯源：`cards/platform-ops/amazon-listing-semantic-ops.md` + `cards/platform-ops/amazon-listing-ai-score-rubric.md`（WB:amazon-listing-builder + alexa-optimizer）

### Q51. Search Terms 该填什么？
**A**：只放前台（标题/五点/描述/A+/QA）未覆盖但有索引价值的词——与词库和标题做差集。不是垃圾桶也不是重复堆砌；机械规则（<250字节等）见 amazon-keyword-listing-ops 卡。
> 溯源：`cards/platform-ops/amazon-listing-semantic-ops.md`（WB:amazon-listing-builder）

### Q52. Listing 数据该从哪抓才可信？
**A**：MCP 工具优先——关键词量/竞品详情/评论走 sellersprite 类 MCP（keyword_miner/asin_detail/review）；浏览器只补 MCP 无覆盖的数据（Reddit/QA板块/官网/认证）。Amazon 反爬会让简单 HTTP 只返回 footer；MCP 失败标 DATA_MISSING，禁止用浏览器凑 Amazon 数据。
> 溯源：`cards/platform-ops/amazon-listing-semantic-ops.md`（WB:amazon-listing-builder 铁律0）

### Q53. Listing 的 AI 评分怎么打？
**A**：8 维×0-10 分（买家问题清单/标题/Item Highlights/五点/A+/Q&A评论/后台属性/关键词Prompts）→换算 100 制。等级：85+优秀/70+良好/55+需优化/40+需改进/<40 高风险。N/A 字段（A+/后台 ST/Prompts 未提供）按 5 分中性计入，不触发红线。
> 溯源：`cards/platform-ops/amazon-listing-ai-score-rubric.md`（WB:amazon-listing-alexa-optimizer）

### Q54. 标题 75 字符新规过渡期怎么评分？
**A**：2026-07-27 起美国站非媒体类目标题≤75字符。过渡期（至 2026-09-30）：75-150 字符但产品身份清晰给 4-5 分、Item Highlights 未填给 4 分；09-30 后恢复严格——超 75 字符最多 5 分。
> 溯源：`cards/platform-ops/amazon-listing-ai-score-rubric.md`（WB:amazon-listing-alexa-optimizer）

### Q55. Item Highlights 是什么字段？
**A**：2026 新字段 ≤125 字符，覆盖材料/用途/场景/兼容/差异点/人群尺寸 ≥5 项——比标题更适合放结构化卖点，AI 可读性高；未填过渡期给 4 分。
> 溯源：`cards/platform-ops/amazon-listing-ai-score-rubric.md`（WB:amazon-listing-alexa-optimizer）

### Q56. 五点描述评分红线是什么？
**A**：全是形容词空话/无边界说明/重复标题/含 emoji·特殊字符·竞品品牌名（政策违规必扣分）。第 5 条应是「注意事项和边界」——评分细则认为最重要；边界信息示例：转换插头注明不是电压转换器、宠物水杯注明容量和适用犬型。
> 溯源：`cards/platform-ops/amazon-listing-ai-score-rubric.md`（WB:amazon-listing-alexa-optimizer）

### Q57. Amazon 差评怎么分类归因？
**A**：6 大类——结构/组装、电子模块、设计/功能缺陷、外观/材质、描述不符、服务/物流（v7.0 新增服务维度，含收到二手品/配件缺失等细分）。每类按高/中/低严重度分级：高=影响核心功能或安全隐患、中=影响体验、低=外观细节。
> 溯源：`cards/platform-ops/amazon-review-voc-ops.md`（WB:review-analysis）

### Q58. VOC 评论洞察怎么反哺 Listing 和广告？
**A**：三向闭环——高频负面词→五点「边界说明」补强+页面说明（评分维度6红线）；「描述不符」差评→文案/图片纠偏；差评高频问题→QA 必答清单；高频正面词→强化进 Listing。广告侧：差评暴露的真实痛点=素材「诚实边界」，承诺不能超出产品实际能力。
> 溯源：`cards/platform-ops/amazon-review-voc-ops.md`（WB:review-analysis）

### Q59. 广告 hook 怎么系统化生成？
**A**：管线 Segment→Motivation→Format→Hook 三组件——视频 hook=视觉动作+口播+字幕三槽不重复分工（静态图塌缩为视觉+headline）。输出 hook matrix 跨 segment×motivation 单元覆盖而非单列改写。动机用客户评论原话不改写营销腔；先选形式再写词。诊断漏斗：thumbstop 弱改视觉开场、hold rate 弱改 on-ramp(3-15s)、CTR 弱改中段承诺、CVR 弱修落地页一致性；一次迭代只改一个组件。
> 溯源：`cards/platform-ops/ad-creative-strategy-system.md`（S25:ad-creative/hook-system）

### Q60. 新素材概念怎么排序优先级？
**A**：先按证据分级（自家转化广告>客户逐字>竞品60天+>有机互动>跨领域>直觉）再按格式角色——unicorn scaler 刺穿冷受众 vs supporting cast 只转化中低漏斗。Meta 51 格式 S→F：S=founder content/partnership ads/VSL；按团队真实产能砍 slate（20概念对8产能=20条妥协货）。每月 retro 评概念不评广告。
> 溯源：`cards/platform-ops/ad-creative-strategy-system.md`（S25:ad-creative/creative-roadmap+meta-formats）

### Q61. Andromeda 时代为什么 partnership ads/creator 内容优先？
**A**：Andromeda 按 persona 定向不按兴趣列表——创作者粉丝=预组装画像种子，partnership ad 从创作者 handle 投放继承种子向外扩展，是触达净新增受众的第一杠杆（#1 投资优先级）。rolling MoM reach 下降=受众饱和信号→部署 creator-fronted 格式。选人按画像重合度不看粉丝数。
> 溯源：`cards/platform-ops/ad-creative-strategy-system.md`（S25:ad-creative/meta-creative-formats）

### Q62. 竖屏广告视频怎么避开平台 UI？
**A**：1080×1920 画布留中央 720×1200 文字安全带（上220px/下500px/左右各180px——动作栏/字幕栈/音乐键压边缘）；字幕白字黑描边无 pill、静态不动画、自动缩字号到带内。有机内容不烘音乐 app 内挂 trending sound 赚算法加权，付费广告烘进视频。
> 溯源：`cards/platform-ops/ad-creative-strategy-system.md`（S25:ad-creative/short-form-video-specs）

### Q63. AI 批量生成广告怎么避免「一看就是 AI」？
**A**：禁对比揭示「It's not X, it's Y」、否定排比、stock phrases、em dash、泛化 hook/CTA slop；批次内变化句式。测试假设必须可证伪（指名指标+对比对象+预期方向）。每条创意溯源到语料库（评论原话/赢家广告/评论区异议），无来源不进 icebox；语料为空停下来要料不许无 grounding 降级生成。
> 溯源：`cards/platform-ops/ad-creative-strategy-system.md`（S25:ad-creative/SKILL.md）

### Q64. Google Search 预算先投哪里？
**A**：意图阶梯逐层解锁——brand（常开）→high-intent non-brand（利润中心大部分预算）→competitor（须对比落地页）→problem-aware→demand-gen（有富余才上）。每层须证明转化为真实成交才解锁下一层；Search 收割需求不创造需求，品类搜索量近零就把预算放上游社媒。
> 溯源：`cards/platform-ops/google-search-playbook.md`（S25:google-search-playbook）

### Q65. 广泛匹配什么时候能开？
**A**：三条件全满足——campaign 月转化 30+、智能出价已上线、否定词表够紧。顺序：Phrase+Exact 起步→每周挖搜索词报告→条件满足才上 Broad。AI Max for Search 同门禁，且要排除不该接广告流量的 URL、周检它选的落地页。
> 溯源：`cards/platform-ops/google-search-playbook.md`（S25:google-search-playbook）

### Q66. 为什么品牌词/非品牌/竞品要独立预算？
**A**：共享预算下最便宜转化最高的 campaign（永远是品牌词）会饿死需要数据的 campaign——账户纸面盈利但重要地方全瞎。Brand 独立预算永不共享；竞品词 CPC/CVR 经济性不同也独立。品牌词默认投（不投竞品投），唯一例外是你是唯一竞价者且自然结果吃掉 SERP 时可测暂停——看品牌总转化（付费+自然）不只看付费。
> 溯源：`cards/platform-ops/google-search-playbook.md`（S25:google-search-playbook）

### Q67. PMax 会不会蚕食品牌 Search？
**A**：会——须账户级品牌排除+一方数据受众信号+上线第一天否定词+先导离线转化再扩量。Optmyzr 2025-02 研究 91% 账户存在 Search↔PMax 完全关键词重叠。价值排序：brand Search>non-brand>remarketing>PMax>demand-gen；PMax 永不首发、永不弱追踪/小预算。
> 溯源：`cards/platform-ops/google-search-playbook.md`（S25:google-search-playbook）

### Q68. 每周搜索词报告怎么处理？
**A**：三遍扫描——①浪费：3+点击零转化的无关词→否定；②赢家：已转化未建词的搜索词→Exact/Phrase 加进正确 ad group；③漂移：broad/phrase 拉来错误含义→收紧匹配或否定。注意否定 broad 要求所有词都在（"free trial" 不挡单独 "free"）；不过度否定——含糊词先攒数据再砍。
> 溯源：`cards/platform-ops/google-search-playbook.md`（S25:google-search-playbook）

### Q69. Amazon 广告目标 ACoS 怎么从毛利算？launch 和成熟差多少？
**A**：Break-even ACoS=广告前利润率；Target ACoS=break-even−目标利润率。例：$39.99 售价成本 $18.50→毛利 53.7%→成熟 target 30%/launch target 50%（前 4-8 周激进换排名）。Max CPC=售价×Target ACoS×CVR 是盈利天花板，实际 bid 取 Amazon suggested range 与 MaxCPC 的低者。
> 溯源：`cards/platform-ops/amazon-ppc-campaign-ops.md`（S26:amazon-ppc-campaign）

### Q70. Amazon Auto/Broad/Exact 怎么分工不打架？
**A**：关键词漏斗——Auto 发现新词→2+ 订单迁 Broad/Exact、2+ 销售迁 Exact；隔离靠 Exact 的所有词在 Broad/Auto 加 Negative Exact。标准 4 campaign：P1 Auto+P2 Exact 必建，P3 Broad 数据一周后加，P4 Product Targeting 有竞品 ASIN 时加。
> 溯源：`cards/platform-ops/amazon-ppc-campaign-ops.md`（S26:amazon-ppc-campaign）

### Q71. Amazon 搜索词报告每周怎么处理？
**A**：三动作——2+ 订单迁移上 Exact（源 campaign 加否定）；**10+ 点击 0 销售**加否定；<20 点击进观察名单。出价调整只对 20+ 点击词：ACoS>200% 降 30-50%、100-199% 降 20%、target+10%~99% 降 10-15%、低于 target 加 10-20%、10+ 点击 0 销售暂停。
> 溯源：`cards/platform-ops/amazon-ppc-campaign-ops.md`（S26:amazon-ppc-campaign）

### Q72. Amazon 新品广告 Day1-21 怎么排？
**A**：Day1 建 P1 Auto+P2 Exact→Day3 查曝光（太低提 bid 向 suggested）→Day7 加 P3 Broad+P4 Product Targeting 并审 Auto 搜索词加明显否定→Day14 全量分析迁移 2+ 单赢家→Day21 对 20+ 点击词调 bid。launch 期目标 ACoS 可放宽到 ~1.7 倍成熟线。
> 溯源：`cards/platform-ops/amazon-ppc-campaign-ops.md`（S26:amazon-ppc-campaign）

### Q73. Brand Analytics 数据怎么反哺广告？
**A**：两条——SFR 报告找「高搜索频率低 click share」机会缺口（你的 click share vs 品类均值，按 High/Medium/Low 分级）；Market Basket 找 >25% 共购率捆绑候选（10+ 共购才算统计显著），用于 bundle/交叉推广/品类扩张判断。
> 溯源：`cards/platform-ops/amazon-ppc-campaign-ops.md`（S26:amazon-brand-analytics）

### Q74. 新品投广告先投 Google/Meta/TikTok 哪个？
**A**：先问买家行为——主动搜索型→Google Shopping 主；视觉种草型→Meta 主；要看演示才懂→TikTok 主；不确定按品类推断并标 ⚠️ estimated。预算 < $1,000/月只投一个主平台不摊薄；有网站流量或邮件列表且预算 > $1,000/月必含 retargeting（通常是全盘最高 ROAS）。
> 溯源：`cards/platform-ops/cross-platform-ppc-strategy.md`（S27:ecommerce-ppc-strategy-planner）

### Q75. 跨平台 ROAS 目标和 Max CPA 怎么算？
**A**：Break-even ROAS = 1÷毛利率（25%→4.0x、50%→2.0x、75%→1.33x）；Target ROAS = Break-even×1.5~2 留利润缓冲；Max CPA = AOV×毛利率。例：$34 商品 76.5% 毛利→break-even 1.31x / target 2.5x / Max CPA $26.01。
> 溯源：`cards/platform-ops/cross-platform-ppc-strategy.md`（S27:ecommerce-ppc-strategy-planner）

### Q76. Google ROAS 4x、Meta prospecting 1.5x，预算该全挪给 Google 吗？
**A**：先对照各自 break-even/target 分三档——🟢超 target 加预算 20-30%；🟡在 break-even~target 间先优化不加钱；🔴低于 break-even 砍 50% 或暂停。警惕纯 ROAS 排序误杀漏斗上游：Meta prospecting 低 ROAS 但在为 retargeting/Google 供受众。
> 溯源：`cards/platform-ops/cross-platform-ppc-strategy.md`（S27:ecommerce-ppc-strategy-planner）

### Q77. 新 campaign 跑一周 ROAS 0.8 要不要关停？
**A**：不要。新 campaign 需 2-4 周度过学习期，期间数据不具统计意义。先查预算是否过低导致学习受限、定向是否过窄，再决定是否动结构；Mode B 审计的硬门槛就是 2-4 周。
> 溯源：`cards/platform-ops/cross-platform-ppc-strategy.md`（S27:ecommerce-ppc-strategy-planner）

### Q78. 各平台 ROAS 基准大概多少？
**A**：2025-2026 行业均值——Google Shopping 4.5x（top quartile 6x+）、Meta 2.2x（retargeting 3.6x，top 4-5x）、TikTok 1.4x（top 2x+）、全行业 2.87x。⚠️ 第三方基准只做 sanity check，判定永远以自家 break-even/target 为准。
> 溯源：`cards/platform-ops/cross-platform-ppc-strategy.md`（S27:ecommerce-ppc-strategy-planner）
