---
title: 广告投放 Agent 竞品分析（Navos / GrowthGPT / Zalify）
doc_type: knowledge
module: ad-agent-qa
topic: ad-agent-competitor-landscape
status: review
created: 2026-11-26
updated: 2026-11-26
owner: self
source: human+ai
source_docs: [S12, S12b, S13, S13b, S15]
fetched_at: 2026-11-26
---

# 广告投放 Agent 竞品分析（Navos / GrowthGPT / Zalify）

## 核心问题

Momcozy 在做广告 Agent 时调研了哪些竞品？各竞品的产品形态、Agent 编排方式、能力边界是什么？与自家体系相比的差异和可借鉴点在哪？

## 系统解答

### 1. 文档定位与证据边界

三篇竞品调研均为**容器型文档**：S12（navos）正文最完整但关键能力细节在截图图片中；S13（GrowthGPT）正文在引用 wiki（S13b）；S15（zalify）仅有一条引用、正文在无权限纪要中。卡片以可获取文本 + 图片 alt 描述为准，截图未逐张下载 `[待确认]`。

### 2. Navos（钛动科技 Tec-Do）

**定位**：全时域、全链路智能营销助手，本质是"由多个 AI Agent 协作组成的 AI 广告团队"，主打中国品牌出海营销。钛动科技是 Meta 官方一级代理商（中国大陆 11 家之一），服务超 10 万广告主、覆盖 200+ 国家；2026 年 7 月 WAIC 发布 Navos 2.0，主打 AI 选品、Agentic Workflow，宣称营销效率提升 10 倍以上。

**六 Agent 分工**（内嵌表格 S12b，原表未命名）：

| Agent | 职责 |
|-------|------|
| 市场洞察 Agent | 24 小时监测海外市场趋势、热销榜、竞品广告动向 |
| 创意策划 Agent | 把洞察转化为完整营销策略和 Campaign 方案 |
| 创意创作 Agent | 文生图/图生视频，批量生成适配各平台的广告素材 |
| 广告投放 Agent | 直连 Meta/TikTok/Google，自动搭建投放、A/B 测试、优化预算 |
| 数据分析 Agent | 自动分析 ROI、人群、素材表现，输出可落地优化建议 |
| 资产管理 Agent | 统一管理素材库、版本和投放历史 |

**调研中拆解的能力模块**（图片 alt 文本）：

- **VOC 分析**：评论抓取与用户声音分析（讨论 rede 评论抓取限制等）
- **GEO / AI 可见性诊断**：可访问性、爬行性、内容结构、内容质量四维评分（示例 80/100/72/72），支持全球 AI 监控、15 Token 输入 `[待确认]`
- **竞品营销数据**：商品上架时间、库存变化、营销打法追踪
- **KOL 选取**：用 Htag 标题分析竞品 KOL 布局策略（示例 YouTube 达人 TOP10 表：排名/订阅量/月观看量/互动率）
- **广告投放自动化**：账户新建、素材新建等方向的能力清单与记录
- **素材审核**：输入→执行逻辑→输出三段式；案例显示 Meta 素材预审可判「高风险」并给出处理建议
- **投放分析**：按平台/广告组/广告/国家分组的效果报告（ROAS/CPC/CTR/CVR/CPM）；素材衰退预警清单（标注「建议立即替换」的紧急级素材）；「结论与建议」模块输出关键指标分析 + 5 项行动清单

**同名产品区分**（调研中明确排除）：greytHR NAVOS（印度 HR 软件）、Navos Technologies（英国金融科技）、Navos AI（高管战略决策平台）。

### 3. GrowthGPT

**容器页**（S13）仅含四层结构截图与章节标题，正文在引用 wiki《GrowthGPT整体情况介绍》（S13b）。

**四层产品结构**（截图 alt）：

| 层 | 内容 | 定位 |
|----|------|------|
| 01 AI 大模型底座 | 理解意图、推理决策、多模态内容生成 | Agent 的「脑」 |
| 02 专家技能层 | 内外部知识库 + 沉淀的方法经验（怎么分析/提问/判断素材） | 经验沉淀 |
| 03 广告平台 API 层 | 对接 Meta/TikTok/Google，一键计划、一键上量、短周期投放 | Agent 的「手」 |
| 04 自然语言交互层 | 无需熟悉平台操作，对话即操作 | 交互入口 |

**产品功能六方面**：市场洞察、增长策略、预算分配、素材生产、广告投放、实时优化——贯穿投前/投中/投后，适配不同客户不同阶段。支持 TikTok/Meta/Google 三平台，一键生成素材、创编计划；账户绑定路径：左下角头像→设置→连接。

**数据产出逻辑**（四条）：
1. 接入 Claude、OpenAI、Seedance 等大模型，调用最新模型模块并跟随更新
2. 接入十几家 API：平台方（TikTok/Facebook/Google）+ 第三方数据（AppLovin、FastMoss、Kalodata），做数据拉取和交叉验证
3. 蒸馏十年以上投手经验植入系统，持续自我学习优化，形成专家 skill 模型
4. ChatGPT 式自然对话交互页面

**交付形态**：深度对话报告、视频素材、HTML 报告（浏览器打开）、图片。官网 growthgpt.app，支持 Google/Facebook 账号注册。

### 4. Zalify

S15 全文仅一条引用：《智能纪要：Zalify广告系统沟通 2026年9月2日》（无权限，未能获取）`[待确认]`。仅能确认 Zalify 是被纳入调研的广告系统类竞品，具体能力边界未知。

### 5. 与 Momcozy 自家体系的对照 `[推断]`

- **编排同构**：Navos 六 Agent（洞察→策划→创作→投放→分析→资产）与 S1 全景 9 大 Loop 架构同属「职能分身」模式；GrowthGPT 四层结构是更通用的「脑-经验-手-嘴」Agent 分层。
- **差异化缺口**：两家竞品均未覆盖「红人素材→广告加推」的细分闭环（S2/S3 的 Loop），这是 Momcozy 内部体系的独有场景 `[推断]`。
- **可借鉴点**：Navos 的素材预审风险分级、素材衰退紧急替换清单、「结论+行动清单」输出形态；GrowthGPT 的「平台 API 层」与「专家经验蒸馏」双引擎数据逻辑。

## 高频问答索引

- **Q：Navos 是什么？有哪些 Agent？**
  A：钛动科技的出海营销 AI 产品，"AI 广告团队"。六 Agent：市场洞察（24h 监测趋势/竞品）、创意策划（策略+Campaign 方案）、创意创作（文生图/图生视频）、广告投放（直连 Meta/TikTok/Google 自动投放+A/B 测试）、数据分析（ROI/人群/素材→优化建议）、资产管理（素材库/版本/历史）。
- **Q：Navos 除投放外还做什么？**
  A：调研拆出 VOC 分析、GEO/AI 可见性诊断、竞品营销数据追踪（上架时间/库存/打法）、KOL 布局分析（Htag）、素材审核（含 Meta 预审风险分级）、投放分析报告（含素材衰退预警与行动清单）。
- **Q：GrowthGPT 的产品结构是什么？**
  A：四层——AI 大模型底座（脑）、专家技能层（知识库+投手经验）、广告平台 API 层（手，对接 Meta/TikTok/Google）、自然语言交互层（对话即操作）。六大功能：市场洞察/增长策略/预算分配/素材生产/广告投放/实时优化。
- **Q：GrowthGPT 的数据从哪来？**
  A：四路——①Claude/OpenAI/Seedance 等大模型实时跟随更新；②十几家 API（平台方 + AppLovin/FastMoss/Kalodata 第三方数据）拉取+交叉验证；③十年+投手经验蒸馏成专家 skill 模型；④ChatGPT 式对话交互。
- **Q：Zalify 竞品调研了什么？**
  A：`[待确认]`——S15 仅含一条引用（2026-09-02 Zalify 广告系统沟通纪要），该纪要无权限未能获取，能力边界未知。
- **Q：竞品能给自家广告 Agent 提供什么参考？**
  A `[推断]`：Navos 的素材预审分级/衰退预警/行动清单输出形态、GrowthGPT 的「经验蒸馏+平台 API」双引擎逻辑可借鉴；红人素材加推 Loop 是竞品未覆盖的差异化场景。

## 相关卡片

- [广告 Agent 系统全景架构](../architecture/ad-agent-system-landscape.md) — Momcozy 自家 9 Loop 体系（对照基准，S1）
- [红人素材广告加推 Agent Loop](../influencer-boost/influencer-boost-loop-overview.md) — 竞品未覆盖的差异化场景（S2）
- [广告投放 Agent 业务调研框架](../architecture/ad-ops-agent-research-framework.md) — 竞品调研所属的业务调研体系（S14/S16）
