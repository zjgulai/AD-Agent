---
title: 多渠道周期报告生成契约 · 日/周/月报三段式结构与量化行动指令纪律
doc_type: knowledge
module: ad-agent-qa
topic: multi-channel-report-contract
status: review
created: 2026-11-27
updated: 2026-11-27
owner: self
source: human+ai
source_docs: [S24]
fetched_at: 2026-11-27
---

# 多渠道周期报告生成契约 · 日/周/月报三段式结构与量化行动指令纪律

## 核心问题

多渠道（Shopify 大盘 + Google + Meta 多账户 + AppLovin）广告数据要自动生成日/周/月报时，报告结构怎么定、每章必须产出什么、行动建议如何防止「正确的废话」？这份契约从一个生产环境 Streamlit 应用（`meta-ad-analysis`）的 system prompt 逆向蒸馏，可直接复用为 Agent 自动化报告的输出规范。

## 系统解答

### 1. 来源与定位

- **来源**：`github.com/XingyuBillHou/meta-ad-analysis`（无 LICENSE，用户确认为内部知识库使用并授权原文存档，`raw/s24-meta-ad-analysis/`）。单文件 Streamlit 应用 `ad_analysis_app.py`（3087 行）：上传多渠道 Excel → LLM 生成分析报告 → 导出 Word/MD/HTML，可邮件投递。
- **本卡只蒸馏报告生成契约**（`build_system_prompt` + `REPORT_SECTIONS` 分节指令 + 确定性指标表逻辑）。Excel 解析管道（合并表头拍平/日期桶识别）、SMTP 邮件投递属工程实现，不在知识库范围。
- **角色设定**：顶尖跨境电商品牌 CMO，精通 Meta/Google/AppLovin 多渠道效果广告，风格「数据驱动、直击要害、敢于给出明确结论和行动建议」。

### 2. 报告类型与时间口径

| 报告类型 | 数据口径 | 解读要求 |
|---------|---------|---------|
| 日报 | 单日快照 | 即时表现、异常波动、与近期均值对比 |
| 周报 | 日期范围内逐日序列 | 区间趋势汇总 + 下周建议 |
| 月报 | 月份区间 | 体量、趋势、渠道贡献与结构性变化 + 下月策略 |
| （附加）周汇总行 | 表格 Week 列汇总行（非逐日） | 整周口径，与相邻周对比 |
| （附加）周末三日 | 周五+周六+周日合并 | 整个周末区间评估，与相邻工作日/周末对比 |

### 3. 三段式输出结构（硬性）

```
## 一、大盘纵览（Executive Summary）
## 二、渠道表现拆解
## 三、下一步行动指令（Action Items）
```

**第一章 · 大盘纵览**
- 结合 Shopify 总销售额（大盘）与各渠道总消耗（前端），估算**大盘 ROAS ≈ 总销售额 ÷ 总广告消耗**，评估整体投入产出比与业务体量。
- 周报/月报/区间模式必须明确趋势方向（增长/下降/波动）并点出关键时间节点或异常日期。
- 分节模式要求：引用 Shopify 总销售额、总广告消耗、订单数、MER/ROI 具体数字，计算并写出大盘 ROAS，3~5 条要点评估盈亏与体量。

**第二章 · 渠道表现拆解**
- 跨渠道对比消耗与 ROAS/转化，渠道清单至少含：Shopify 大盘、Google、Axon(AppLovin)、全部有数据的 Meta 账号。
- **渠道二分法**：
  - 「增长引擎」= 消耗增长且 ROAS 健康、转化稳健；
  - 「拖后腿」= ROAS 偏低、消耗虚高或转化下滑。
- 分节模式要求：3~5 条增长引擎 bullet（渠道名+具体 ROAS/消耗数字+原因）+ 3~5 条拖后腿 bullet（渠道名+问题数字+风险）+ 2~3 条 cross-channel 对比结论。

**第三章 · 下一步行动指令**
- 预算调整（哪个渠道/账号加多少 % 或金额、哪个减多少）、关停/暂停建议（持续亏损无改善趋势）、放量建议（预算上限/扩量人群包等具体方式）。
- 分节模式要求：**至少 5 条** numbered list，每条格式 `【渠道/账号】动作描述（含量化幅度，如 +20% / -500 USD / 暂停 XX 广告组）`；整报告模式要求至少 3 条且每条含渠道名+量化调整幅度。

### 4. 硬性纪律（防「正确的废话」的核心设计）

- **所有结论必须引用原始数据中的具体数字**（消耗、ROAS、ROI、销售额、订单数），禁止空泛描述。
- **禁止空泛建议**：「持续观察」「进一步优化」类表述视为失败。
- **缺失渠道正常处理**：某渠道该区间无数据 → 注明「该渠道此区间无数据」，不编造、不因此中断其他渠道分析。
- 篇幅下限：整报告 ≥800 字；分节模式各章有 min_chars（180/200/280）。
- 全文简体中文，专业、简洁、有决策力。

### 5. 确定性数据与 LLM 分工（prompt 工程亮点）

- **表格由代码生成，不依赖 LLM**：`build_channel_tables_markdown` 从原始数据确定性提取每渠道 spend/ROAS/orders（关键词族匹配：Spend/消耗/Cost、ROAS/ROI/MER、出单量/Orders/订单），生成渠道汇总表 + 全指标明细表。
- **LLM 只写洞察**：分节模式第二章中 LLM 只产出 `### 2.3 渠道洞察与诊断` 文字 bullet，禁止重复输出表格——「数据用代码算，判断用模型写」的分工消除数字幻觉面。
- **spend 口径优先级**：优先取 Shopify 行内 `Ad Spent_<渠道>` 列（大盘侧记账口径），渠道本地 spend 字段兜底——**跨源口径不一致时以 Shopify 为准**。
- **分节生成防截断**：报告分 3 次 LLM 调用各写一章再合并，单章 temperature ≤0.4，避免长报告中途截断。

### 6. 渠道与账户结构观察

- **Shopify = 大盘锚点**：不是广告渠道，是全店销售/订单/MER 的事实源；广告渠道消耗与它对照才有「大盘 ROAS」概念。
- **Meta 多账户矩阵**：同一品牌拆多个 Meta 广告账户（案例中 WearNuage/NuageBra/Nuage2026/NuageWear 四个账户 Sheet，已停投账户自动跳过）——账户级拆分常见于品牌矩阵/品线分投场景 `[推断]`。
- **AppLovin 以 Axon 名义出现**：增长投放平台，KB 中此前无方法论覆盖，本批仅登记平台实体。

### 7. 与现有 KB 的关系

- 与 `meta-operator-daily-workflow`（S6）互补：S6 是**单渠道 Meta 日内操作节奏**（8 环节 IF/ELSE），本卡是**多渠道周期报告输出契约**（日报/周报/月报结构）。S6 的五段式日报偏「今日动作闭环」，本卡偏「跨渠道体量判断+预算指令」。
- 与 `attribution-measurement`（S22）衔接：本卡「大盘 ROAS ≈ 总销售额/总广告消耗」即 MER 口径的朴素实现，与归因三角测量中的 MER/增量层对应。
- 与 SCN-011 Agent 的关系：本契约可直接作为自动化广告报告的输出规范底稿——三段式结构、量化行动指令、禁空泛词、确定性表格+LLM 洞察分工均可复用 `[推断]`。

## 高频问答索引

- **Q：多渠道广告日报/周报/月报的标准结构是什么？**
  A：三段式——①大盘纵览（Shopify 总销售额+总广告消耗→大盘 ROAS≈销售额÷消耗，趋势方向+关键节点）②渠道拆解（每渠道 spend/ROAS/orders 表格 + 增长引擎 vs 拖后腿二分 + cross-channel 对比）③行动指令（≥3~5 条量化建议：渠道名+加减预算 %/金额+关停/放量方式）。
- **Q：什么是「大盘 ROAS」？和渠道 ROAS 什么关系？**
  A：大盘 ROAS ≈ Shopify 总销售额 ÷ 全渠道总广告消耗（MER 朴素口径），衡量整体投入产出比；渠道 ROAS 是单渠道口径。报告第一章用大盘 ROAS 评估业务体量，第二章用渠道 ROAS 排序找增长引擎/拖后腿。
- **Q：AI 生成的广告报告怎么防止「正确的废话」？**
  A：四条硬纪律——所有结论必须引用具体数字（消耗/ROAS/销售额/订单）；禁止「持续观察」「进一步优化」等空泛表述；行动指令每条必须含渠道名+量化幅度（+20%/-500 USD/暂停 XX）；渠道无数据时注明而非编造。另加分工防线：数据表格由代码确定性生成，LLM 只写洞察文字。
- **Q：同一品牌为什么要拆多个 Meta 广告账户？报告里怎么处理？**
  A：品牌矩阵/品线分投场景常见（案例：WearNuage/NuageBra/Nuage2026/NuageWear 四账户）。报告按账户维度各自拆解再 cross-channel 对比；已停投账户 Sheet 自动跳过，不纳入当期分析。
- **Q：AppLovin 在多渠道报告里算什么角色？**
  A：效果广告渠道之一（案例中以 Axon 名义），与 Google/Meta 并列做 spend/ROAS/orders 对比。KB 中 AppLovin 方法论目前空白，本批仅登记平台实体与报告口径。
- **Q：这份报告契约和投放师一日工作流 SOP 什么关系？**
  A：互补不冲突——S6（meta-operator-daily-workflow）管单渠道 Meta 的日内操作节奏与动作铁律；本契约管多渠道周期报告的输出结构与量化纪律。前者回答「今天做什么」，后者回答「这周期整体怎么样、预算往哪调」。

## 相关卡片

- [meta-operator-daily-workflow.md](./meta-operator-daily-workflow.md) — Meta 投放师一日工作流 SOP（S6，单渠道日内节奏）
- [meta-post-launch-data-inspection.md](./meta-post-launch-data-inspection.md) — 投后巡检数据采集与模板（S8，报告数据源头）
- [../fundamentals/attribution-measurement.md](../fundamentals/attribution-measurement.md) — 归因测量（S22，大盘 ROAS/MER 的归因层对应）
- [../platform-ops/dsite-sem-ads-playbook.md](../platform-ops/dsite-sem-ads-playbook.md) — 独立站 SEM 打法（S22，Google/Meta 渠道策略层）
