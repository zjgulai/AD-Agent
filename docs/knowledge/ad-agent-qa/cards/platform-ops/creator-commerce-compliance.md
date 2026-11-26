---
title: 达人商业合作能力与合规（Meta/YouTube/Shopify + FTC 披露）
doc_type: knowledge
module: ad-agent-qa
topic: creator-commerce-compliance
status: review
created: 2026-11-26
updated: 2026-11-26
owner: self
source: human+ai
source_docs: [PO:capability-meta-partnership-ads-us, PO:capability-instagram-creator-marketplace-us, PO:capability-shopify-collabs-us, PO:capability-youtube-shopping-collections-us, PO:workflow-creator-brief-assembly-us, PO:workflow-meta-creator-amplification-us, PO:rule-ftc-endorsement-disclosures-us, PO:scenario-creator-commercial-compliance-us]
fetched_at: 2026-11-26
---

# 达人商业合作能力与合规（Meta/YouTube/Shopify + FTC 披露）

## 核心问题

品牌和达人合作有哪些官方能力入口？Meta Partnership Ads、IG Creator Marketplace、Shopify Collabs、YouTube Shopping 各解决什么问题？FTC 对达人披露的要求是什么红线？organic 内容能直接拿去做付费投放吗？creator brief 怎么写才不是「讲真实体验」这种空指令？

## 系统解答

### 1. 文档定位

蒸馏自 platform-ops-wiki 的 creator/commerce 对象组：4 能力卡（Meta Partnership Ads、IG Creator Marketplace、Shopify Collabs、YouTube Shopping Collections）+ 2 工作流（brief 组装、Meta 放大）+ 2 规则/场景（FTC 披露、creator 商业合规场景包）。全部 `status: review`、`market: us`。

**与现有 KB 的关系**：influencer-boost 集群（S2/S3）是 Momcozy **内部**红人加推 Agent 的建设视角；本卡是**外部平台能力+合规**视角——回答「平台官方给了哪些合作入口、合规边界在哪」。两者互补：内部 Agent 建设要消费这些平台规则。

### 2. 四大平台合作能力对照

| 能力 | 平台 | 本质 | 关键约束 |
|------|------|------|---------|
| **Partnership Ads** | Meta | 把 creator 内容授权后放进 Ads Manager 做 paid amplification，以 creator handle 呈现 | 必须完成 permissioning；受 branded content 规则约束 |
| **IG Creator Marketplace** | Meta/IG | 官方 creator 发现与撮合（first-party data），服务 branded content + partnership ads | 仅 IG business/creator 账号；不是所有 creator 在 marketplace 内 |
| **Shopify Collabs** | DTC 独立站 | creator/affiliate 招募+归因+佣金结算一体化 | 不替代平台内达人曝光；需与站点 offer/归因协同 |
| **YouTube Shopping Collections** | YouTube | 创作者把商品按主题组织成可浏览集合，承接 Shorts/长视频流量 | 是承接能力不替代内容转化力；受商品可售性+披露义务约束 |

- **共同模式**：都是「creator 内容 → 商业化放大」的官方管道，但**都不替代内容质量与落地页承接**。
- **TikTok 侧对照**：TikTok Shop affiliate 是第四种模式（shop 内挂车+分佣+SPS 准入），见 [TikTok Shop 打法卡](tiktok-shop-growth-playbook.md)。

### 3. FTC 披露红线（美国市场硬约束）

`rule-ftc-endorsement-disclosures` 的核心：**只要存在 material connection 就必须 clear and conspicuous disclosure**。

- **material connection 不只是付费**：免费样品、折扣、返点、雇佣、家庭/个人关系都算。
- **Allowed**：`ad/sponsored/advertisement` 等清晰语言；图片叠加 disclosure；视频内画面+语音双披露；直播周期性重复；平台 disclosure tool + 自定义披露并用。
- **Prohibited**：披露藏在 profile/About/折叠 more/描述末尾；只用 `sp/spon/collab/thanks` 模糊词；声称没体验过的产品；无证据做疗效/安全性 claim。
- **责任在 creator 自身**：不得依赖品牌或平台代披露；发帖人在海外但内容影响美国消费者也适用美国法。
- **Agent 含义**：disclosure 不是「可选文案」而是 workflow 强制节点；生成脚本时默认同时检查 material connection 与 claim substantiation；多平台分发要为不同载体生成不同位置的披露。

### 4. Creator 商业合规场景包：四步判断

`scenario-creator-commercial-compliance` 给出标准判定链：

1. **material connection?** 有免费样/返点/佣金/赞助/雇佣/亲属关系→强制披露路径
2. **creator eligible?** 不符合 TikTok/YouTube/Meta 资格→不进入该平台合作
3. **product safe to narrate?** claim 敏感/功效难证/使用有风险→先收紧脚本不放量
4. **amplification path allowed?** organic 可发≠能直接做 paid amplification

**合作类型选择**：`gifted seeding / affiliate / sponsored post / paid amplification` 要按风险分级，不是越高级越好。

### 5. Creator Brief 组装：从空指令到可执行合同

`workflow-creator-brief-assembly` 的核心：brief 必须由 `roster + archetype + faq_gap + category overlay` 组装而成，不能只剩「讲真实体验」。

- **Brief lane 选择**（按 channel_type）：`expert-education / practitioner-review / editorial-commerce / comparison-review`
- **必备块**：`objective / audience / allowed narrative / must-answer-faq-gaps / forbidden claims / disclosure placement / CTA route`
- **Route block**（按 likely_commercial_model）：`study-only / targeted-sponsored / editorial-commerce / affiliate-with-guardrails / amplification-ready`
- **红线**：`quote_ready_status != quote-ready` 且无 reuse/licensing 明证时，brief 不得偷带报价假设、复用权限或素材交付承诺

### 6. Meta Creator 放大：从「合作发布」到「可放量 paid asset」

`workflow-meta-creator-amplification` 的升级路径：Creator Marketplace 找候选 → 品牌/合规/转化筛查 → 读 `channel_type / likely_commercial_model / disclosure_pressure` → 提取 `faq_gap / purchase_moment` 写进 adaptation brief → 获取 partnership ads 授权 → Ads Manager 建放大计划 → 二次筛选。

**关键质量检查**：
- creator 内容质量 ≠ paid scaling 能力，两者分开评
- 没有 landing page 承接不做 amplification
- 高风险类目（医疗/母婴/功效）必须人工审
- `drop-day decision` 素材 ≠ `post-click reassurance` 素材，不直接放大
- `quote_ready_status != quote-ready` 且无 reuse/licensing 明证→不推进成 paid asset

## 高频问答索引

- **Q：Meta Partnership Ads 和普通 whitelisting 有什么区别？**
  A：Partnership Ads 是官方能力：品牌以 creator handle 在 Ads Manager 跑 paid ads，必须完成 permissioning 并受 branded content 规则约束。IG Creator Marketplace 是前置的官方 creator 发现撮合入口。
- **Q：FTC 要求的 disclosure 具体是什么？**
  A：material connection（付费/样品/折扣/返点/雇佣/亲属）必须 clear and conspicuous 披露；视频要画面+语音双披露，直播要周期重复；`sp/collab/thanks` 等模糊词不合规；责任在 creator 不能甩给品牌或平台。
- **Q：organic 达人内容能直接投广告吗？**
  A：不能默认。organic 可发≠paid amplification 允许。要看 creator 的 commercial model、disclosure pressure、reuse/licensing 权限、LP 承接是否达标——Meta 放大工作流有 7 条质量检查和 4 个人工审批门。
- **Q：Shopify Collabs 解决什么问题？**
  A：独立站体系内的 creator/affiliate 招募+归因+佣金结算一体化。不替代平台内达人曝光能力，需与站点 offer、归因、付费投放协同设计。
- **Q：creator brief 应该包含什么？**
  A：六个必备块：objective/audience/allowed narrative/must-answer-faq-gaps/forbidden claims/disclosure placement/CTA route；外加按商业模式的 route block 和平台差异化要求。禁止在 quote 未就绪时偷带报价或复用权限假设。
- **Q：母婴/美妆类目做达人合作有什么特殊要求？**
  A：脚本与披露默认人工复核；不得演示危险使用场景；功效/安全/治疗型表述需证据；FTC 披露要求更严。详见 [母婴 Overlay 卡](baby-maternity-growth-overlay.md)。
- **Q：达人内容质量好就能放量吗？**
  A：不能。内容质量和 paid scaling 能力是两件事。放大前要过：授权完整、披露无风险、LP CVR 达标、faq_gap 可被内容或 LP 回答、类目非高风险——五条 rollback 条件任一触发即停。

## 相关卡片

- [TikTok Shop 广告增长打法](tiktok-shop-growth-playbook.md) — TikTok affiliate 模式与 SPS 准入
- [母婴跨平台增长 Overlay](baby-maternity-growth-overlay.md) — 高风险类目合规边界
- [红人素材广告加推 Agent Loop](../influencer-boost/influencer-boost-loop-overview.md) — Momcozy 内部加推体系（S2）
- [广告 Agent 系统全景架构](../architecture/ad-agent-system-landscape.md) — 全局 Loop 视角（S1）
- 知识图谱：`ad:adproduct:{meta-partnership-ads,ig-creator-marketplace,shopify-collabs,youtube-shopping}` / `ad:rule:pops-ftc-*` / `ad:playbook:pops-wf-*`（platform-ops-kb 分片）
