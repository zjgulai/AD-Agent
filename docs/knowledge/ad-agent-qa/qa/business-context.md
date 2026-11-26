---
title: Q&A 数据集 - Momcozy 业务实操
doc_type: knowledge
module: ad-agent-qa
topic: qa-business-context
status: review
created: 2026-11-26
updated: 2026-11-26
owner: self
source: human+ai
---

# Momcozy 业务实操 Q&A

覆盖 `cards/business-context/`（4 卡：momcozy-audience-persona、audience-layering-playbook、mp-project-methodology、customer-touchpoint-map）。Momcozy 内部业务知识，与 fundamentals 行业通用机制分开。

### Q1. Momcozy 的核心人群是谁？
**A**：一个「北美品质型新妈妈」，沿孕→哺→育被连续承接 2-3 年，不是三拨独立人群。人群画像报告基于 56,938 条复购数据：孕期是获客窗口（CPA 全场最低 Google 产品 $8.95、ROAS 最高 Meta 6.77），哺乳期是复购金矿（复购率 18.8%、订单复购率 27.7%），育儿期是体量最大阶段（首单 61,832 占 42%）。
> 溯源：`cards/business-context/momcozy-audience-persona.md`

### Q2. 哪个阶段投放 ROI 最高？预算分配有什么问题？
**A**：孕期 ROI 最高——CPA 全场最低（Google 产品 $8.95）、ROAS 最高（Meta 6.77），但 Meta 预算只给 11.4% 被系统性低估，建议加码至 20%+。哺乳期靠配件/储奶袋订阅锁复购（吸奶器配件自复购 4,437 人全场最高）；育儿期靠品类扩张（清洗机 BS03 花费 $313K）而非耗材复购。
> 溯源：`cards/business-context/momcozy-audience-persona.md`

### Q3. DTC 和 Amazon 的人群画像有何不同？渠道怎么分工？
**A**：Amazon TGI 上升的全是站内婴儿硬件（+20~37），下降的全是站外泛母婴（-14~-21）；NTB 93.9% 几乎全是新客，是拉新金矿。渠道分工：TikTok 低价引流（AOV $61-97）、Google 关键词高价收割（AOV $158-161）、Meta 中间价大盘；哺乳期重心 Google+Amazon、孕期 Meta+TikTok、育儿期全渠道。独立站和 Amazon 分工：Amazon 开疆拓土（65% 新客），独立站玩留存与复购（35% 高价值用户+第一方数据），Amazon 包裹插卡/售后邮件向独立站导流。
> 溯源：`cards/business-context/momcozy-audience-persona.md` + `customer-touchpoint-map.md`

### Q4. 出价怎么分层？（T0–T3）
**A**：T0 核心溢价包 +30~50%（孕期+硬件 in-market+NTB）、T1 标准±10%（哺乳期复购）、T2 前置事件 +15~25%（Getting Married/Future Movers）、T3 测试 -20~-30%（泛家庭/职场妈妈）、排除站外泛人群。注意此 T0–T3 是**出价分层**，与 S7 决策树 T0–T5 编号体系不同，勿混淆。
> 溯源：`cards/business-context/momcozy-audience-persona.md`；消歧见 `glossary.md`

### Q5. 高价值交叉复购对有哪些？
**A**：吸奶器→配件（1,493 人，耗材飞轮）、哺乳内衣→吸奶器（859 人，低价引流高价）、清洗机→洗涤剂（576 人，育儿期耗材）。
> 溯源：`cards/business-context/momcozy-audience-persona.md`

### Q6. 清洗机单品类怎么做浅/中/深三层受众分层投放？
**A**：浅层=兴趣定向+通用词（唤醒痛点），中层=行为定制受众+品类品牌词（卖点教育），深层=高意向行为+再营销（促单）。配合 Meta/TikTok 浅层兴趣定向、Google 品类词收割的组合；用户链路按孕早期→孕晚期→产后 0-6 月→辅食期分四阶段，不同阶段承接不同产品（孕早期卖孕期品如枕/托腹带→孕晚期卖备产品如吸奶器/内衣/待产包→产后卖刚需家电如清洗机/监视器→辅食期卖场景扩展如推车/辅食机）。
> 溯源：`cards/business-context/audience-layering-playbook.md`

### Q7. 孕早期为什么不投清洗机？产后 0-6 月为什么可以直接转化？
**A**：孕早期用户刚怀孕只关注自身变化，清洗机需求未觉醒——此阶段目标是种草+沉淀 Pixel 数据+拉入品牌受众池，为后续承接蓄水。产后 0-6 月痛点顶峰（睡眠剥夺+每天手洗十几次），不再需要教育，直接抛解决方案+对比+限时优惠。
> 溯源：`cards/business-context/audience-layering-playbook.md`

### Q8. 素材怎么匹配投放层级？已购人群怎么交叉销售？
**A**：素材匹配——浅层唤醒痛点（对比视频/数字冲击/红人 FOMO）、中层卖点教育（功能演示/信任背书/对比图）、转化层促单（限时/套装/评价合集）。已购交叉销售三组测试：孕早已购→孕晚品、吸奶器已购→清洗机/监视器、清洗机已购→吸奶器/辅食机/推车。
> 溯源：`cards/business-context/audience-layering-playbook.md`

### Q9. 投放需求怎么进入系统？MP 文档必须包含什么？
**A**：两类触发——A 类走完整链路（Brief→澄清/预研→MP→上线→调节→复盘），B 类专题复盘需先补「迷你 Brief」。MP 文档必须包含：目标+节奏+预算拆分+结构模板+资源清单+KPI/阈值，版本化且可追溯至广告 ID。
> 溯源：`cards/business-context/mp-project-methodology.md`

### Q10. 怎么保证复盘时能解释「为什么中途改了」？广告新建怎么批量化又不失控？
**A**：执行版 MP 含变更记录作为实际打法基线+对象级变更日志+动作留痕。批量新建靠：笛卡尔积裂变+固定层级结构模板（1-3-3 测素材等）+Preflight 校验+高危操作审批/AI 熔断。AB Test 系统化管理：测试组对象+控制变量规则+自动化补位（固定预算依次新建，旧组迭代需更替红线）+可选 MAB 自动裁决。
> 溯源：`cards/business-context/mp-project-methodology.md`

### Q11. 看数的固定顺序是什么？哪些数据口径问题会让复盘失真？
**A**：先大盘（是否需紧急处理）→下钻（谁在贡献/掉量）→素材疲劳信号+人群指标对比→异常归类（预算/策略/素材/追踪/站内承接/外部）。失真口径：事件断流/重复计数/币种金额异常/UTM 缺失/关键参数缺失；多源对照广告端 vs GA4 vs Shopify vs UTM 末次/多归因。
> 溯源：`cards/business-context/mp-project-methodology.md` / `meta-operator-daily-workflow.md`

### Q12. 文档识别的 AI 机会最多在哪？
**A**：MP 模板化+RAG、Ad-hoc 咨询（Text-to-SQL）、自定义报表、裂变式搭建、accept edits 自动调节、全链路时间轴报告、元素级归因、语义化结论入库——共 20+ 项系统化机会清单。MP 方法论底座四件套：标签 ID/事件合同/资产库/权限审计（0.x 横切）。
> 溯源：`cards/business-context/mp-project-methodology.md`

### Q13. 吸奶器用户生命周期有几阶段？购前触点怎么分层？
**A**：7 阶段：备孕/孕期→孕晚期囤货→产后 0-7 天→哺乳期高频→断奶/过渡→二胎复购→口碑推荐。购前触点三层：认知（SEO/SEM/社媒/KOL/内容/社群/线下，让她第一次知道你）→兴趣（首页/产品发现/内容中心/邮件培育/再营销，让她想深入了解）→考虑（PDP/评价/客服/促销/竞品对比/社群验证，让她决定买）。
> 溯源：`cards/business-context/customer-touchpoint-map.md`

### Q14. 配件复购为什么是利润核心？Momcozy 的触点差异化打法？
**A**：吸奶器是耗材型产品：储奶袋/法兰/鸭嘴阀持续消耗，配件订阅包（每月自动配送）+用完前 7 天提醒形成复购飞轮；Momcozy 从泵延伸到储奶袋/文胸/背奶包形成生态。差异化打法：双轨独立站定价更低、TikTok+IG 主力（36万粉丝）、素人妈妈+中腰部达人（佣金 13.5%、美国达人占 50%）、Mom Village 社群、积分+会员日、不盲目扩 SKU 顺 18 个月契约逐环节延伸。
> 溯源：`cards/business-context/customer-touchpoint-map.md`

### Q15. 新站冷启动先补哪些触点？
**A**：对照自检清单——认知阶段先保品牌词 SEO 前 3+场景词广告+垂类达人；兴趣阶段保首屏 UVP+Lead Magnet+对比工具+EDM 序列；考虑阶段保 PDP 评价量+Q&A+Live Chat+首单优惠+竞品对比页。
> 溯源：`cards/business-context/customer-touchpoint-map.md`
