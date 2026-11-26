---
title: Q&A 数据集 - 广告行业通用机制
doc_type: knowledge
module: ad-agent-qa
topic: qa-fundamentals
status: review
created: 2026-11-26
updated: 2026-11-26
owner: self
source: human+ai
---

# 广告行业通用机制 Q&A

覆盖 `cards/fundamentals/`（3 卡：ad-algo-auto-fields、ad-bidding-full-chain、product-lifecycle-ad-strategy）。行业通用知识，非 Momcozy 内部文档；与诊断树的关系见各条末尾标注。

### Q1. CBO 和 ABO 的区别？
**A**：CBO（系列预算优化）下组级预算锁死失效，算法跨组实时挪钱给赢家组，新组有 7 天学习期保护；ABO（广告组预算）组级预算独立锁定、人工控制分配。巨量/腾讯/快手默认 ABO 跨组分配弱。
> 溯源：`cards/fundamentals/ad-algo-auto-fields.md`

### Q2. 智能出价（tCPA/tROAS/oCPM）是怎么工作的？
**A**：每次拍卖前按设备/时段/地点/查询词/画像预测该用户的转化概率和价值，在目标值约束内算期望价值出价——高意向抢高价、低意向出低价或不抢。eCPM 换算：CPC=eCPM=出价×pCTR×1000；oCPM/tCPA=eCPM=Target CPA×pCTR×pCVR×1000×PacingFactor；tROAS=eCPM=(pValue/Target ROAS)×pCTR×pCVR×1000。Total Score=eCPM+Ad Quality Score。乘 pCVR 是因为转化出价的价值=点击意愿×转化意愿——只会点不会买的流量出价应更低。
> 溯源：`cards/fundamentals/ad-algo-auto-fields.md` + `ad-bidding-full-chain.md`

### Q3. 为什么新账户不能直接开智能出价/全托管？
**A**：放权依赖数据：智能出价和预算分配依赖转化回传质量，受众扩量和创意即定向依赖历史转化数据量。数据量不够算法会瞎跑——建议前 2 周手动跑，积累 20–50 个转化再切智能模式（与 S7「周转化≥50 脱离学习」口径呼应）`[推断]`。
> 溯源：`cards/fundamentals/ad-algo-auto-fields.md`

### Q4. 受众扩量（Adv+ Audience）把人工定向变成了什么？
**A**：从「硬筛条件」降级为「种子信号」——算法在种子内外做探索-利用找高价值人群；地域和法定年龄下限仍锁死。Meta 上画像变「建议」可保留可关闭。
> 溯源：`cards/fundamentals/ad-algo-auto-fields.md`

### Q5. 什么是「创意即定向」？和「创意即召回」是一回事吗？
**A**：「创意即定向」指算法用 CV/NLP/音频理解素材本体（画面物体/人物/场景、文案关键词、音频语义），自动匹配对这类内容感兴趣的人群，无需人工勾选兴趣标签——巨量最成熟，Meta Creative as Targeting 与 TikTok 智能定向同类。「创意即召回」是竞价链路视角：智能投放系统（Meta Adv+/巨量全域/PMax）中召回阶段就把创意作为特征——没有具体创意就没有确定的 pCTR/pCVR，素材语义自动匹配相似兴趣人群。两者是同一机制的定向侧与竞价侧表述 `[推断]`。
> 溯源：`cards/fundamentals/ad-algo-auto-fields.md` + `ad-bidding-full-chain.md`

### Q6. 程序化创意（DCO/RSA）和普通多素材有什么区别？
**A**：人传素材池，算法自动排列组合成 N 个「视频×标题×描述」变体实时测试效果；Pin 位锁死不参与组合。Meta Adv+ Creative 还会自动裁比例、叠字、加音乐、生成文案变体。
> 溯源：`cards/fundamentals/ad-algo-auto-fields.md`

### Q7. Meta 和其他平台在「新创意冷启动」上有什么差异？
**A**：巨量/Google 对新创意有学习期保护（前几百次展示不直接按效果砍）；**Meta 较激进，新创意表现差会很快被压流量**——所以 S6/S7 要求新素材给足 50 点击或 3 天保护期 `[推断]`。
> 溯源：`cards/fundamentals/ad-algo-auto-fields.md`

### Q8. 全托管模式（PMax/SPC/ASC/放量投放）人还能调什么？
**A**：几乎不能单独调版位/人群/出价——只填目标、预算、素材+落地页、转化回传，保留排除权和品牌资产。Google PMax 透明度最低（看不到具体词/人群）；巨量放量投放比 PMax 保留更多人工调参空间。
> 溯源：`cards/fundamentals/ad-algo-auto-fields.md`

### Q9. Audience Network 版位为什么要单独监控？
**A**：Meta Adv+ Placements 全版位自动分配时，AN（Audience Network）流量质量差、CPA 高——S7 L2-05 版位诊断要求低质版位消耗<20%，与此对应 `[推断]`。
> 溯源：`cards/fundamentals/ad-algo-auto-fields.md` / `cards/meta-ads-diagnosis/meta-diagnosis-layers-l0-l4.md`

### Q10. 广告是怎么被选出来展示的？（竞价全链路）
**A**：14 步：离线索引预过滤（封号/欠费/拒审/暂停/时段）→ SDK 发请求带 device_id+隐私状态 → 拉用户画像+频控历史 → 多路召回约 1000 个「计划×创意」→ 频控/版位/预算实时过滤 → 模型预估 pCTR/pCVR/pValue → 按 eCPM+Pacing+质量分换算竞价分 → 粗排精排取 Top 1 → GSP 次高价扣费 → DCO 渲染 → 曝光计费 → 点击计费 → 转化归因 → 模型更新反哺前序环节。
> 溯源：`cards/fundamentals/ad-bidding-full-chain.md`

### Q11. GSP 次高价是什么意思？广告主会被多扣钱吗？
**A**：胜出广告按**下一名的 eCPM**（而非自己的出价）计费+调价。出价 $10 但第二名只出 $3，实际按约 $3 付费——鼓励真实出价、不虚高。CPC/oCPM 扣费均基于此机制。
> 溯源：`cards/fundamentals/ad-bidding-full-chain.md`

### Q12. Pacing 因子是什么？为什么早上花钱快晚上又提价？
**A**：Pacing=预算消耗速度调控因子：消耗进度快于线性预期→降价控速；慢于预期（尤其临近结算）→提价抢量。它让日预算全天平滑消耗而非上午烧完。S4/S7 诊断中 Pacing 异常判定为 <60% 或 >130%（双向预警）。
> 溯源：`cards/fundamentals/ad-bidding-full-chain.md` / `cards/meta-ads-diagnosis/meta-diagnosis-metrics.md`

### Q13. iOS ATT 授权拒绝后归因会怎样？
**A**：IDFA 缺失→降级 SKAN 模式：转化延迟 24–48h、无单用户 click_id、数据粒度受限。这直接影响 S7/S8 的归因差异率指标和 L0-01 归因口径校准的必要性 `[推断]`。
> 溯源：`cards/fundamentals/ad-bidding-full-chain.md`

### Q14. 频控为什么前置到召回阶段？
**A**：在 1000 个候选召回后立即剔除「该用户已看 N 次」的广告，避免无效候选进入昂贵的精排预估环节——大幅降低算力损耗。对应 S7 的频次诊断（7 天≤3、>5 疲劳，另有 ≤5/≤6/>10 等多口径，见诊断集群 Q22）。
> 溯源：`cards/fundamentals/ad-bidding-full-chain.md`

### Q15. 曝光和点击分别什么时候计费？
**A**：素材满足有效曝光定义（信息流停留 1 秒/开屏完成/Banner 可见 50%——版位决定规则）→ CPM 计费点+归因起点；用户交互 → CPC 计费点。版位配置直接改变「什么时候算曝光」。
> 溯源：`cards/fundamentals/ad-bidding-full-chain.md`

### Q16. 模型更新怎么形成飞轮？
**A**：归因好的「曝光-点击-转化」样本流实时更新 pCTR/pCVR 权重 → 反哺用户画像更新、召回更准、预估更准、DCO 素材组合优选 → 更多有效曝光带来更多样本 → 持续进化。前提是回传数据完整（CAPI+正确归因窗口）——这正是诊断树 L0-01/L0-04 归因与事件质量检查的底层原因 `[推断]`。
> 溯源：`cards/fundamentals/ad-bidding-full-chain.md`

### Q17. 这份竞价流程图对诊断/Agent 有什么用？
**A**：它是诊断逻辑的「物理层」：S7/S4 的每个判定（Pacing 异常、频控触顶、归因差异、Learning 期）都对应 14 步中的具体环节——比如 Pacing 在 Step 6 调价、频控在 Step 4 过滤、归因在 Step 12、模型质量在 Step 13 `[推断]`。Agent 自动化调整本质是替人操作这些环节的配置字段。同理，「算法自动」字段卡解释了诊断树里 Learning 期、频控、版位、受众扩量等判定逻辑的行为本质。
> 溯源：`cards/fundamentals/ad-bidding-full-chain.md` / `ad-algo-auto-fields.md`

### Q18. 新产品投放第一阶段（测试期）应该做什么？
**A**：测试期（Soft Launch）：小流量验证 PMF——多渠道小预算并行（各 $50-100/天×7-14 天）比 CPI/D7 留存/早期 ROAS 找主攻阵地；同时做留存驱动 PMF 验证（Onboarding/落地页分流看留存与 CAC），留存不达标不上量。投放目标 App Installs/Traffic，出价 tCPA/Max Conversion，日预算仅 5-10%。
> 溯源：`cards/fundamentals/product-lifecycle-ad-strategy.md`

### Q19. 预热期和发布期的区别？投放目标一样吗？
**A**：诉求不同：预热期=认知蓄水/预约加购/KOL 种草（Brand Exposure/Lead Gen/LPV，CPM/CPV/oCPM，均匀蓄水）；发布期=集中曝光声量引爆冲首发（Reach+SOV，App Installs/Traffic/Reach，oCPM/tCPA，脉冲式集中投放）。预热期必做 Hook 素材测试+种子人群探索；发布期必做 BLS 品牌提升研究+频控测试。
> 溯源：`cards/fundamentals/product-lifecycle-ad-strategy.md`

### Q20. 增长期加预算怎么加？常态期怎么判断广告真有效？
**A**：每 3-4 天加 20%（不是翻倍——翻倍会触发学习期重置），观察 ROAS/CPA/CPM 是否在容忍区间，跌破下限即停；同步做 LAL 扩量：购买者 Lookalike 1%→3%→5%，种子用高 LTV 客户而非泛访问者。常态期做 Incrementality 增量测试（Geo Holdout：选相似城市一组停投一组继续看收入差）——Retargeting 的 ROAS 容易虚高，不测增量会把「本来就会买」算成广告功劳，月花 $75K+ 至少一次；另看拉新/再营销比例（基准 75-85%/15-25%）和素材疲劳（DCO 周更 20%）。
> 溯源：`cards/fundamentals/product-lifecycle-ad-strategy.md`

### Q21. 产品衰退/清仓期还投广告吗？大促期怎么投？
**A**：投，但逻辑完全变了：低预算收割老客——100% 预算给老客/高意向，拉新停止；老客唤醒成本比新客低 5 倍；用稀缺性话术（「最后几仓」）；Bundle 优于直降（买老款赠新品券/老新套餐——既清库存又带新品）；同步做新品预热迁移，折扣不能破坏品牌价格锚点。大促期（618/双11/BFCM）横切所有阶段拆三段：蓄水期（预约/加购，20-30% 预算）→开门红（CVR/CPA/ROAS，40-50%）→返场（剩余库存，20%）；出价大促前 1-2 周提价抢量、当日 tROAS 控成本；高峰晚 6-10 点手动提价 25%；再营销预算+30-50% 用倒计时/限时券追投；素材用紧迫话术（CTR 比功能话术高约 22%）。
> 溯源：`cards/fundamentals/product-lifecycle-ad-strategy.md`

### Q22. 为什么增长期 ROAS 设「下限」而不是「目标」？首销期怎么投？
**A**：增长期核心是抢市场份额窗口——死守 ROAS 极致值会错失扩量时机，设下限（守住即可不追求极致），跌破下限即停；同时监控新客占比不下降、CPM 不因扩量飙升、频次疲劳拐点。首销期冲首销 GMV+首单转化+积累评价 UGC：Conversion/Sales 目标，tROAS/oCPM 按购买优化，集中火力转化+再营销追未购；必做三实验：出价策略 A/B（tCPA/tROAS/Max Conversion）、落地页 CRO（50/50 分流）、再营销追投（加购未购/预约未购专属优惠）。
> 溯源：`cards/fundamentals/product-lifecycle-ad-strategy.md`

### Q23. 这套生命周期策略和 Momcozy 广告 Agent 有什么关系？
**A**：`[推断]`：S8 案例的「系列01 Hook素材实验（预热/测试思路）/系列02 出价策略实验/系列03 再营销人群实验」正是按阶段×实验类型设计的投放结构；Agent 做投放建议时，「产品处于哪个生命周期阶段」应是策略路由的第一维度——不同阶段北极星指标和出价方式完全不同。
> 溯源：`cards/fundamentals/product-lifecycle-ad-strategy.md`
