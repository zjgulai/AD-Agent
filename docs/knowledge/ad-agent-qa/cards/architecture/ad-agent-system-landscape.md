---
title: 广告 Agent 系统全景架构
doc_type: knowledge
module: ad-agent-qa
topic: ad-agent-system-landscape
status: review
created: 2026-11-26
updated: 2026-11-26
owner: self
source: human+ai
source_docs: [S1]
fetched_at: 2026-11-26
---

# 广告 Agent 系统全景架构

## 核心问题

Momcozy 的广告 Agent 体系由哪些 Loop 和 Agent 构成？从「发现市场机会」到「策略制定、创意生产、投放执行、增长优化、复盘沉淀」再到「红人素材加推」，整体如何分层？哪些环节必须人工确认（HITL）？

## 系统解答

### 1. 顶层定位

画板首部定位语：**持续自动发现「产品×人群×市场×渠道×卖点」的广告增长机会，并形成可执行的投放机会**。

全图由 **10 个 Loop 区域**（任务概述为「约 7 个」；Vision OCR 可辨 9 个，Tesseract 二次 OCR 新发现「广告异常诊断与恢复 Loop」，合计 10 个标题 `[待确认：终核原图]`）+ 30 余个 Agent/节点职责描述构成，另有「市场/品类数据」等数据来源标注。

> **OCR 保真说明**：画板经 2560×2560 渲染图提取，先后用 macOS Vision OCR 与 Tesseract（chi_sim+eng, psm 11）双引擎交叉（原始文本 `raw/s1-whiteboard-ocr.txt` / `-tesseract.txt`）。Vision 对中文主体识别好但专有名词粘连（「策路」=策略、「L00p」=Loop、「竟品」=竞品）；Tesseract 对英文节点名（@ 前缀）识别更好但中文破碎。两引擎一致处视为确认；引擎间冲突或单方孤证处仍标 `[待确认]`。Agent→Loop 归属为 `[推断]`（连线/布局无法从 OCR 还原）；职责描述只取 OCR 可辨部分，乱码段不臆造。

### 2. Loop 全景总览

| # | Loop | 一句话定位 | 主要 Agent/节点 |
|---|------|-----------|----------------|
| 1 | 广告市场机会发现 Loop | 监测市场/品类/用户/竞品信号，评估并形成广告机会策略 | Trend、Consumer Insight、Competitor、Opportunity、Strategy Agent + Opportunity Database |
| 2 | 竞品广告策略洞察 Loop | 深入拆解竞品投放策略（OCR 未分离出独立节点） | 推断与 ③ Competitor Agent 输出衔接 `[推断][待确认]` |
| 3 | 新品广告冷启动 Loop | 基于 PLM/历史案例生成新品冷启动投放策略 | 新品投放策略 Agent |
| 4 | 广告创意生产与测试 Loop | 创意资产沉淀 + 素材衰退识别 + 新素材 A/B 测试飞轮 | 创意洞察 Agent、素材优化 Agent |
| 5 | 广告投放策略制定 Loop | 渠道/预算/策略/创建/账户/素材六个策略制定类 Agent | 渠道策略、广告投放策略、预算分配、广告创建、账户治理、素材组装 Agent `[推断归属]` |
| 6 | 广告投放执行 Loop | 已审批策略 → Campaign 创建 → 校验 → 上线监控的执行链路 | 执行链路节点 ①-⑨（Campaign Planning → Monitoring，含 Tracking Agent） |
| 7 | 广告异常诊断与恢复 Loop | 异常监控、归因诊断与恢复建议（Tesseract 新发现的 Loop 标题，节点归属 `[推断]`） | 异常监控 Agent、机会发现 Agent `[推断]` |
| 8 | 广告增长优化 Loop | 五维优化建议与分阶段执行（出价预算/Search Term/受众/广告优化） | 出价预算优化、Search Term 优化、受众优化、广告优化 Agent `[推断归属]` |
| 9 | 广告复盘与知识进化 Loop | 多维复盘报告 + 投放知识库沉淀反哺策略 | 广告复盘 Agent、广告知识沉淀 Agent |
| 10 | 红人素材广告加推 Loop | 红人内容→广告资产规模化加推，尾链含优化/HITL/复盘/回流 | ⑨ 广告优化 → ⑩ HITL → … → ⑮ 沉淀 → 回流红人素材池（前半段与 S2/S3 对应）`[推断]` |

### 3. 各 Loop 明细

#### Loop 1 · 广告市场机会发现

数据侧标注「市场/品类数据」。节点按 OCR 编号 ①②③…⑤⑦⑧（④⑥ 编号缺失 `[待确认]`）。Tesseract 确认画板节点名带 `@` 前缀，六个 Agent 英文名全部可读：

- **① Trend Agent**（画板另标注「品类机会洞察 Agent」，是否同一节点 `[待确认]`）：识别品类、搜索、消费趋势；接入 Google Trends、搜索词、广告数据、竞品数据、销售数据，持续监测品类增长、产品需求、搜索趋势和竞品动作，识别快速增长的细分需求，输出「机会品类+目标人群+推荐产品+推荐渠道」机会清单。
- **② Consumer Insight Agent**（另标注「消费者广告洞察 Agent」`[待确认]`）：分析用户需求/痛点/人群；汇总广告点击/转化、GA4、订单、CRM、用户评论、社媒等数据，建立「人群—需求—痛点—卖点—广告素材—转化」关联分析，识别高转化人群及核心购买驱动，输出人群定向和广告内容建议。下游节点：**市场/广告负责人确认机会**（HITL）。
- **③ Competitor Agent**：分析竞品投放变化；通过 AI 自动识别竞品投放渠道、主推产品、核心卖点、创意方向、投放节奏和策略变化，最终输出竞品投放策略及对我方的机会建议。
- **Product Agent**（Vision OCR 原文「小srocucaaent」，Tesseract 确认为 `@ Product Agent`）：匹配公司产品及卖点。
- **Opportunity Agent**（Vision OCR「5 aonortunitu Aaent」，Tesseract 确认为 `@ Opportunity Agent`；编号 ④/⑤ `[待确认]`）：评估市场机会。
- **Strategy Agent**（Tesseract `@ Strategy Agent`）：形成广告机会策略。
- **Opportunity Database**：机会清单持续监控变化（数据库节点，非 Agent）。

#### Loop 2 · 竞品广告策略洞察

OCR 仅辨出 Loop 标题（原文「竞品广告策路洞察L00p」），未分离出独立节点描述 `[待确认]`。推断其内容即 ③ Competitor Agent 的深化输出——「竞品投放策略及对我方的机会建议」，或与 Loop 1 竞品分析节点部分重叠 `[推断]`。

#### Loop 3 · 新品广告冷启动

- **新品投放策略 Agent**：接入 PLM/商品库、历史相似产品广告数据及市场洞察，自动识别新品核心卖点和目标人群，匹配历史成功投放案例，生成新品冷启动策略——首批渠道、Campaign、预算、人群、素材和测试节奏。

#### Loop 4 · 广告创意生产与测试

- **创意洞察 Agent**：建立广告创意资产库，将素材拆解为 Hook、场景、人物、卖点、产品、文案、CTA 等结构化标签，并关联 CTR、CVR、CPA、ROAS 等效果数据，通过历史数据识别高表现创意元素及组合，形成可复用的创意方法论。
- **素材优化 Agent**：将素材表现数据与创意标签关联，分析 Hook、场景、卖点、人物、时长等元素对 CTR/CVR/ROAS 的影响，识别素材衰退原因，自动生成下一轮 Hook、Copy、脚本和创意方向，最终进入 CMS 生成新素材并进行 A/B Test。
- **广告创意增长飞轮**：洞察 → 生成 → 审核 → 测试 → 识别赢家 → 变体生成（循环）。Tesseract 在画板该区域另辨出英文节点标签 `@ Ad Launch`、`@ A/B Test`、`@ Performance Analysis`、`@ Winner Detection`、`Creative Optimization` 等 `[待确认：与中文飞轮阶段的对应关系]`。

#### Loop 5 · 广告投放策略制定

OCR 中独立 Loop 标题（原文「广告投放策路制定L00p」）。以下 6 个 Agent 职责描述连续呈现，归属本 Loop 为 `[推断]`：

- **渠道策略 Agent**：汇总各渠道 Spend、Revenue、ROAS、CAC、CVR、新客占比、LTV 等数据，建立渠道效果及边际收益模型，根据市场、产品、目标和预算自动评估各渠道增长潜力，输出媒体组合及预算方向建议。
- **广告投放策略 Agent**：用户输入产品、市场、目标、预算和周期后，基于历史投放经验、竞品策略、消费者洞察和平台最佳实践，自动生成 Campaign Structure、目标人群、渠道、预算、Bid Strategy、素材需求、KPI 和测试计划，形成标准化投放方案。
- **预算分配 Agent**：基于渠道、Campaign、产品、人群等维度的历史 ROAS、CAC、CVR、边际收益和预算约束建立预算优化模型，模拟不同预算组合下的预期收益，输出预算调整建议；后续可通过 API 自动执行。
- **广告创建 Agent**：打通 Meta、Google、TikTok 等广告平台 API，将自然语言投放需求转换成标准 Campaign 配置，自动完成 Campaign、Ad Set/Ad Group、Audience、Budget、Bid、Creative 等配置，并在创建前进行参数、命名、Tracking 和预算校验。（OCR 附近乱码「T/ com / Seript/ Wsad」疑为平台/API 标识 `[待确认]`。）
- **账户治理 Agent**：定期扫描广告账户结构和配置，通过规则+AI 识别重复 Campaign、Audience 重叠、预算碎片化、无效广告、命名错误、Tracking 缺失等问题，生成账户健康度评分及治理任务，并支持批量修复。
- **素材组装 Agent**：打通 CMS/素材中心，根据广告策略自动筛选适合的人群、产品和渠道素材，将视频、图片、Hook、Copy、CTA 等进行智能组合，自动生成多个广告变体，并按平台规格完成素材适配和批量上架。

#### Loop 6 · 广告投放执行

输入节点「已审批广告策略」，执行链路节点（双引擎 OCR 复核后补全）：

`已审批广告策略` → **① Campaign Planning Agent**（生成平台配置）→ **② Creative Matching Agent**（职责描述两引擎均未完整辨出 `[待确认]`）→ **③ Naming Agent**（检查命名）→ **④ Tracking Agent**（检查 Pixel/UTM/Event，Vision OCR 遗漏、Tesseract 新发现）→ **⑤ Compliance Agent**（检查平台规范）→ **⑥ Campaign Structure Agent**（分析 Campaign/Ad Set/Ad 层级结构、预算、受众、素材及效果数据，识别 Campaign 碎片化、预算分散、受众重叠、素材重复等问题，模拟不同账户结构效果，输出合并/拆分/迁移和预算重新分配方案；Vision OCR「Campagn结构优化Agnf」、Tesseract「Campaign stuff Agent」均为同一节点误读）→ **投放负责人最终确认**（HITL，位于创建前）→ **⑦ Ads API**（创建 Campaign）→ **⑧ Validation**（检查是否成功上线）→ **⑨ Monitoring**（进入投放监控）。

> 注：Vision OCR 曾将⑥节点误读为独立 Loop 7 成员「Campaign 结构优化 Agent」，双引擎复核后确认其为执行链路节点；⑥与⑦之间的「投放负责人最终确认」为人工卡点。

转型对比（画板标注）：从「人工打开 Meta/Google 后台逐项配置」变成「自然语言需求 → AI 生成 → 人工确认 → API 自动创建 → 自动校验」。

#### Loop 7 · 广告异常诊断与恢复

Tesseract 新辨出该 Loop 标题（Vision OCR 未捕获），位于执行链路与增长优化之间 `[待确认：终核原图]`。按语义推断其成员为监控/诊断/恢复类节点——**异常监控 Agent**（实时同步 Spend/CPM/CTR/CVR/CPA/ROAS 等核心指标，建立历史基准和异常阈值，发现异常后自动多维归因：预算突增、素材疲劳、流量变化、转化下降等，推送「异常原因+影响+建议动作」）与**机会发现 Agent**（主动扫描账户寻找增长机会——高 ROAS 但预算受限、高 CTR 低消耗、高 CVR 人群、表现优异素材等，通过边际收益分析判断增量空间，输出「建议加预算/扩大人群/复制…」等增长建议）`[推断归属]`。

#### Loop 8 · 广告增长优化

OCR 中独立 Loop 标题（原文「-广告增长优化Loop②」）。以下 Agent 归属 `[推断]`：

- **出价预算优化 Agent**：持续读取 Campaign 的成本、转化和预算消耗，结合目标 ROAS/CPA、转化趋势和预算约束判断是否需调整 Bid 或 Budget；**三级自动化**——初期以「优化建议」为主 → 中期支持人工确认执行 → 成熟后在安全规则范围内自动调整。
- **Search Term 优化 Agent**：接入 Google/Amazon 等平台 Search Term 数据，对搜索词进行意图识别、转化分析和价值分级，自动发现高潜力新词、低效词和无效词，生成「新增关键词/提高出价/降低出价/否定关键词」建议，并支持批量执行（双引擎复核确认，Vision OCR 末尾乱码已破解）。
- **受众优化 Agent**：汇总 Audience、用户属性、广告行为及订单转化数据，分析不同人群的 CTR、CVR、CAC、ROAS 和 LTV，识别高价值/低价值人群，输出扩量、收窄、排除和 Lookalike 拓展建议，并支持调用广告平台 API 执行。
- **广告优化 Agent**：汇总五维优化——预算优化、人群优化、出价优化、素材优化、Campaign 优化（画板列于 Loop 10 区域，推断为跨 Loop 复用的统一优化能力 `[推断]`；Tesseract 确认其英文标注 `@ 广告优化 Agent`）。

#### Loop 9 · 广告复盘与知识进化

- **广告复盘 Agent**：自动汇总 Campaign、产品、渠道、人群、素材等多维数据，对比目标、历史同期及基准，自动识别关键变化并进行归因，形成「结果—变化—原因—问题经验—下一步」的完整复盘报告，支持日报、周报、大促、新品等不同复盘场景。
- **广告知识沉淀 Agent**：每次投放的策略、素材、产品、人群、渠道、结果和复盘结论结构化沉淀到广告知识库，建立「产品×人群×渠道×创意×策略×效果」的知识关系；新建广告时自动检索相似成功案例，为策略 Agent 提供历史经验。

#### Loop 10 · 红人素材广告加推

画板定位语：自动识别高潜力红人内容，将优质红人素材快速转化为广告资产并规模化加推，通过持续监测和优化找到高 ROI 的「红人素材×人群×广告策略」组合，实现红人内容从自然传播到付费增长的规模化转化。

OCR 可辨的尾链节点（编号 ⑨-⑮；前半段节点未完整呈现，推断与 S2/S3 的 13 Agent Loop 对应 `[推断]`）：

**⑨ 广告优化 Agent**（预算/人群/出价/素材/Campaign 五维）→ **⑩ HITL**（高风险调整人工确认）→ **⑪ 持续投放** → **⑫ winning Creative 识别** → **⑬ 红人素材广告复盘 Agent** → **⑭ 广告分析报告** → **⑮ 优质素材/策略/效果沉淀** → **回流红人素材池**（闭环）。

### 4. Agent 全景清单

| Agent / 节点 | 所属 Loop | 职责（一句话） |
|---|---|---|
| Trend Agent（品类机会洞察 Agent`[待确认]`） | 1 机会发现 | 识别品类/搜索/消费趋势，输出「机会品类+人群+产品+渠道」清单 |
| Consumer Insight Agent（消费者广告洞察 Agent`[待确认]`） | 1 机会发现 | 用户需求/痛点/人群关联分析，输出人群定向与广告内容建议 |
| Competitor Agent | 1/2 竞品 | 识别竞品投放渠道/产品/卖点/创意/节奏/策略，输出对我方机会建议 |
| Product Agent | 1 机会发现 | 匹配公司产品及卖点（双引擎确认英文名） |
| Opportunity Agent | 1 机会发现 | 评估市场机会 |
| Strategy Agent | 1 机会发现 | 形成广告机会策略 |
| Opportunity Database | 1 机会发现 | 机会清单持续监控变化（数据节点） |
| 新品投放策略 Agent | 3 新品冷启动 | 生成新品冷启动策略（渠道/Campaign/预算/人群/素材/测试节奏） |
| 创意洞察 Agent | 4 创意测试 | 创意资产库结构化标签 + 高表现元素方法论 |
| 素材优化 Agent | 4 创意测试 | 素材衰退识别 → 下一轮创意方向 → CMS 生成 + A/B Test |
| 渠道策略 Agent | 5 策略制定`[推断]` | 渠道效果与边际收益评估，媒体组合与预算方向 |
| 广告投放策略 Agent | 5 策略制定`[推断]` | NL 输入 → 标准化投放方案（结构/人群/渠道/预算/Bid/素材/KPI） |
| 预算分配 Agent | 5 策略制定`[推断]` | 预算优化模型模拟，输出预算调整建议（可 API 执行） |
| 广告创建 Agent | 5 策略制定`[推断]` | NL → Campaign 标准配置 + 创建前三重校验 |
| 账户治理 Agent | 5 策略制定`[推断]` | 账户健康度扫描、问题识别、批量修复 |
| 素材组装 Agent | 5 策略制定`[推断]` | 素材智能组合多变体，按平台规格批量上架 |
| Campaign Planning Agent | 6 执行链① | 执行链路首节点（职责 OCR 未展开） |
| Creative Matching Agent | 6 执行链② | 创意匹配（职责 OCR 未展开） |
| Naming Agent | 6 执行链③ | 检查命名 |
| Tracking Agent | 6 执行链④ | 检查 Pixel/UTM/Event（双引擎复核新发现） |
| Compliance Agent | 6 执行链⑤ | 检查平台规范 |
| Campaign Structure Agent | 6 执行链⑥ | Campaign 层级结构/预算/受众/素材分析，碎片化识别与合并拆分重分配（原误置优化域，已归位） |
| Ads API | 6 执行链⑦ | 创建 Campaign（平台 API 落地） |
| Validation | 6 执行链⑧ | 检查是否成功上线 |
| Monitoring | 6 执行链⑨ | 上线后监控（与异常监控 Agent 关系 `[待确认]`） |
| 异常监控 Agent | 7 异常诊断`[推断]` | 指标基准 + 异常多维归因 + 建议动作推送 |
| 机会发现 Agent | 7 异常诊断`[推断]` | 主动扫描增长机会，边际收益判断增量空间 |
| 出价预算优化 Agent | 8 增长优化`[推断]` | Bid/Budget 调整，三级自动化（建议→确认→安全自动） |
| Search Term 优化 Agent | 8 增长优化`[推断]` | 搜索词意图/价值分级，新增/出价/否定词建议+批量执行 |
| 受众优化 Agent | 8 增长优化`[推断]` | 人群价值分层，扩量/收窄/排除/Lookalike 建议 |
| 广告优化 Agent | 8/10 跨 Loop`[推断]` | 预算/人群/出价/素材/Campaign 五维优化总入口 |
| 广告复盘 Agent | 9 复盘进化 | 多维数据对比归因，输出「结果—变化—原因—经验—下一步」报告 |
| 广告知识沉淀 Agent | 9 复盘进化 | 投放知识库沉淀，「产品×人群×渠道×创意×策略×效果」关系，反哺策略 |
| 红人素材广告复盘 Agent | 10 红人加推 | ⑬ 复盘节点（与 S2/S3 Loop 13 对应）`[推断]` |

合计约 31 个具名 Agent/节点（去重后约 26 个独立能力单元；任务概述「约 20 个」与画板实际规模有出入 `[待确认]`）。

### 5. HITL 原则与飞轮机制

**HITL（人工确认）节点**：

| 位置 | 确认内容 | 决策人 |
|------|---------|--------|
| Loop 1 · Consumer Insight 后 | 市场/广告负责人确认机会 | 市场/广告负责人 |
| Loop 6 · 创建 Campaign 前 | 「已审批广告策略」→ 投放负责人最终确认 | 投放负责人 |
| Loop 6 · 创建链路 | 自然语言需求 → AI 生成 → **人工确认** → API 自动创建 → 自动校验 | 投放负责人 `[推断]` |
| Loop 8/10 · 优化执行 | 「高风险调整人工确认」（画板标注 ⑩ HITL）；出价预算优化 Agent 三级自动化：建议 → 人工确认 → 安全规则内自动 | 投放/广告负责人 `[推断]` |

**飞轮/闭环机制**：

- **创意增长飞轮**（Loop 4）：洞察 → 生成 → 审核 → 测试 → 识别赢家 → 变体生成。
- **知识进化飞轮**（Loop 9）：复盘结论 → 知识库 → 新建广告自动检索相似成功案例 → 反哺策略 Agent。
- **红人素材飞轮**（Loop 10）：…→ 优质素材/策略/效果沉淀 → 回流红人素材池。

## 高频问答索引

- **Q：Momcozy 广告 Agent 体系由哪些 Loop 构成？**
  A：双引擎 OCR 可辨 10 个 Loop 标题：广告市场机会发现、竞品广告策略洞察、新品广告冷启动、广告创意生产与测试、广告投放策略制定、广告投放执行、广告异常诊断与恢复（Tesseract 新发现）、广告增长优化、广告复盘与知识进化、红人素材广告加推。Loop 原始编号与精确计数因 OCR 无法完全还原 `[待确认]`。
- **Q：这套体系的顶层目标是什么？**
  A：持续自动发现「产品×人群×市场×渠道×卖点」的广告增长机会，并形成可执行的投放机会——即从机会发现一路闭环到投放、优化、复盘沉淀。
- **Q：Agent 大致分几类？**
  A：按职能分六类——机会发现类（Trend/Consumer/Competitor/Opportunity/Strategy）、策略制定类（渠道/投放策略/预算/创建/账户治理/素材组装）、创意类（创意洞察/素材优化）、执行类（Campaign Planning→Monitoring 链路）、优化类（异常监控/机会发现/出价预算/Search Term/受众/Campaign 结构/广告优化）、复盘沉淀类（广告复盘/知识沉淀）。
- **Q：哪些环节必须人工确认？**
  A：四处——① 市场/广告负责人确认广告机会；② 投放负责人确认「已审批广告策略」后才创建 Campaign；③ 创建链路中 AI 生成方案后人工确认再 API 落地；④ 高风险调整人工确认（优化域三级自动化：建议→确认→安全规则内自动）。
- **Q：广告创建如何从「人工逐项配置」变自动？**
  A：画板对比：从人工打开 Meta/Google 后台逐项配置 → 自然语言需求 → AI 生成 Campaign 配置 → 人工确认 → API 自动创建 → 自动校验（命名/Tracking/预算/参数）。
- **Q：广告创意如何持续变好？**
  A：Loop 4 的创意增长飞轮：创意洞察沉淀方法论 → 素材优化识别衰退并生成下一轮创意方向 → CMS 生成新素材 → A/B 测试 → 识别赢家 → 变体生成，循环迭代。
- **Q：投放经验如何沉淀和复用？**
  A：Loop 9 广告知识沉淀 Agent 把每次投放的策略/素材/产品/人群/渠道/结果/复盘结论结构化进广告知识库，建立「产品×人群×渠道×创意×策略×效果」关系；新建广告时自动检索相似成功案例反哺策略 Agent。
- **Q：红人素材加推在全景架构中是什么位置？**
  A：Loop 10「红人素材广告加推」是独立于主投放链路的增长飞轮：红人内容→广告资产→规模化加推→监控优化→复盘→沉淀回流红人素材池。其前半段节点与 S2/S3 的 13 Agent Loop 对应 `[推断]`。
- **Q：素材组装 Agent 现在能用吗？**
  A：S1 画板将其列为策略制定环节节点（CMS 素材智能组合+多变体批量上架）；但 S2/S3 红人加推建设任务中明确「暂不建设，直接使用红人原视频授权加推」`[来源：S2/S3]`，两处口径差异待确认。
- **Q：这份卡片有哪些内容不确定？**
  A：双引擎复核后仍标 `[待确认]`——Loop 2「竞品广告策略洞察」的独立节点内容、执行链路 ② Creative Matching Agent 职责、Chain 中 `[SE Agent` 等零星乱码标签、Loop 7/8「异常诊断与恢复」与「增长优化」的节点分界、Loop 4 飞轮英文节点名与中文阶段的对应、「TARMT SSR Agent」等红人 Loop 乱码节点、Agent→Loop 归属均为 `[推断]`。双引擎一致处（Product/Opportunity/Strategy Agent 名、Tracking Agent、Campaign Structure Agent 归位、Search Term 否定关键词等）已去标。

## 相关卡片

- [红人素材广告加推 Agent Loop · 角色·触点·链路全景](../influencer-boost/influencer-boost-loop-overview.md) — S2/S3 试点卡（Loop 10 的展开版）
- [红人素材广告加推 13 个 Agent 职责矩阵与接口规格](../influencer-boost/influencer-boost-agent-specs.md) — S2/S3
- [红人素材广告加推建设任务与进度](../influencer-boost/influencer-boost-build-tracking.md) — S3 bitable
- [广告监控与优化 Agent（一期：Meta）产品方案](monitoring-optimization-agent-prd.md) — S5（对应 Loop 7/8 诊断优化域一期落地）
- [Meta 广告诊断 SOP / 完整策略树](../meta-ads-diagnosis/meta-diagnosis-sop.md) — S4（优化域规则依据）
- [Meta 广告诊断指标基准](../meta-ads-diagnosis/meta-diagnosis-metrics.md) — S4
