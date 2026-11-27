---
title: 页面转化优化（CRO）· 七维诊断框架、表单字段成本律与 DTC 页面实验清单
doc_type: knowledge
module: ad-agent-qa
topic: cro-page-optimization
status: review
created: 2026-11-27
updated: 2026-11-27
owner: self
source: human+ai
source_docs: [S25]
fetched_at: 2026-11-27
---

# 页面转化优化（CRO）· 七维诊断框架、表单字段成本律与 DTC 页面实验清单

## 核心问题

广告引流到的页面为什么不转化？先查什么？表单每多一个字段掉多少转化？哪些页面实验最值得测？本卡蒸馏 marketingskills 的 `cro`——**页面级转化诊断与优化层**，补 KB「流量侧有打法、页面侧只有零散 checklist」的缺口。

## 系统解答

### 1. 来源与口径

- **来源**：`github.com/coreyhaines31/marketingskills` → `skills/cro/`（MIT，`raw/s25-marketingskills/skills/cro/`）。SKILL.md 是通用 CRO 诊断框架 + form.md 表单专项 + experiments.md 按页面类型的实验清单。
- **口径翻译**：源文偏 B2B SaaS（demo request/pricing page/SaaS 术语），蒸馏时映射到 DTC：**landing page→PDP/Collection/活动页，demo form→留资表单/邮箱订阅，pricing page→产品定价与促销页**。B2B 特有实验（ROI calculator/G2 评分）标注不适用。

### 2. 七维诊断框架（按影响排序）

1. **价值主张清晰度（最高影响）**：访客 5 秒内能否理解「这是什么+为什么关我事」？写的是客户语言还是公司黑话？最常见问题：讲功能不讲收益、太模糊或太 clever、想一次说完所有事；
2. **标题效力**：是否传达核心价值主张？是否够具体？是否与流量来源文案一致（**message match**——广告说什么，落地页首屏必须接住）；够具体的模式：「Get [结果] without [痛点]」、带数字/时间框架、「Join 10,000+ …」类社会证明；
3. **CTA 层级**：是否有一个清晰主行动？不滚动可见？按钮文案传达价值而非动作——弱「Submit/Sign Up/Learn More」→强「Start Free Trial/Get My Report/See Pricing」；主次 CTA 结构+在关键决策点重复出现；
4. **视觉层级与可扫读性**：扫一眼能否拿到主信息？重点元素是否视觉突出？留白够不够？图片是辅助还是干扰？
5. **信任信号与社会证明**：客户 logo（知名度优先）、具体署名带照片的 testimonial、带真实数字的 case snippet、评分数、（相关场景的）安全徽章——**放在 CTA 附近和收益声明之后**；
6. **异议处理**：价格/价值疑虑、「适不适合我」、实施难度、「不行怎么办」——用 FAQ 区、保证、对比内容、流程透明来回应；
7. **摩擦点**：表单字段太多、下一步不清、导航混乱、不该必填的必填、移动端问题、加载慢。

### 3. 表单字段成本律（form.md 核心）

**每个字段都有成本**——经验法则：3 字段为基线；4-6 字段完成率降 10-25%；7+ 字段降 25-50%+。逐字段拷问：跟进时真的用它吗？能自动补全就别问。

字段级要点：邮箱单字段不确认、用正确移动键盘；姓名合并为单字段降摩擦；电话/公司/职位等敏感字段放最后；下拉框慎用（选项多改搜索、必加「Other」）；多选用 checkbox。布局：单列完成率更高（移动友好），仅短关联字段可双列（First/Last）；标签在字段上方优于 placeholder 充当标签；多步表单用于字段确实多的场景并配进度条。

### 4. 页面类型实验清单（experiments.md 蒸馏）

源文按 7 类页面给实验假设表，DTC 可迁移的高价值项：

| 页面 | 高价值实验 |
|------|-----------|
| **首页/落地页** | Hero 标题变体（具体 vs 抽象）、首屏 CTA 有无、视觉格式（截图/GIF/视频）、CTA 文案、社会证明位置（首屏 vs 下方）、sticky nav+CTA、exit-intent popup |
| **产品页（PDP）** | 卖点 benefit vs feature 导向、评价展示位置与数量、图片序列（生活方式 vs 白底）、尺寸/使用场景图、FAQ 位置、捆绑/对比模块 |
| **定价/促销页** | 价格心理学（$99 vs $100 vs $97）、锚定（高价方案在前）、层级数量（2 vs 3 档）、年付/月付切换省钱标注、money-back guarantee 位置 |
| **留资/订阅表单** | 字段数、单步 vs 多步、表单位置（首屏 vs 内容后）、埋字段自动补全 |
| **博客/内容页** | 内容内 CTA、资源区、inline vs 末尾转化点 |

### 5. 与 KB 衔接

- 流量侧：`customer-touchpoint-map`（触点地图）解决「人从哪来」，本卡解决「来了转不转化」；
- 测试纪律：所有页面实验走 `ab-testing-methodology`（fundamentals）的样本量/显著性/peeking 规则——**CRO 给假设，本卡给判读**；
- 广告侧：message match 要求落地页承接广告卖点——`cross-platform-ppc-strategy` 的 creative brief 与 PDP 优化是同一链条两端；
- 优先级：先跑七维诊断找最大短板，再从对应页面类型实验清单选 1-2 个测，别一次改一堆。

## 高频问答索引

- **Q：落地页转化差先查什么？**
  A：按影响排序七维——价值主张 5 秒清晰度→标题与流量来源 message match→单一主 CTA 可见且文案传价值→视觉层级可扫读→CTA 附近信任信号→异议处理（FAQ/保证）→摩擦点（字段/移动端/速度）。
- **Q：表单每多一个字段掉多少转化？**
  A：经验法则——3 字段基线，4-6 字段完成率降 10-25%，7+ 降 25-50%+。逐字段拷问「跟进真的用它吗」，能自动补全不问，敏感字段放最后。
- **Q：CTA 按钮文案怎么写？**
  A：传达价值而非动作——弱「Submit/Sign Up/Learn More」，强「Start Free Trial/Get My Report/See Pricing」。一个清晰主行动+不滚动可见+在关键决策点重复。
- **Q：广告说的卖点和落地页不一致怎么办？**
  A：message match 断裂是常见转化杀手——广告承诺什么，落地页首屏必须 5 秒内接住同一卖点。诊断时把广告素材文案和落地页首屏并排看。
- **Q：先改哪个？**
  A：先七维诊断定位最大短板（通常是价值主张或 CTA），再从对应页面类型实验清单选 1-2 个假设，走 A/B 测试纪律验证——别凭感觉一次改一堆。

## 相关卡片

- [ab-testing-methodology.md](../fundamentals/ab-testing-methodology.md) — 页面实验的统计判读纪律
- [customer-touchpoint-map.md](../business-context/customer-touchpoint-map.md) — 流量从哪来（CRO 的上游）
- [cross-platform-ppc-strategy.md](./cross-platform-ppc-strategy.md) — 广告侧 message match 对端
- [dsite-sem-ads-playbook.md](./dsite-sem-ads-playbook.md) — 独立站 SEM 引流侧
