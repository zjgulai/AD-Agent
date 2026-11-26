---
title: 知识库验收与状态流转清单
doc_type: knowledge
module: ad-agent-qa
topic: review-checklist
status: stable
created: 2026-11-26
updated: 2026-11-26
owner: self
source: human+ai
---

# 知识库验收清单（review → stable）

> 21 张卡片全部 `status: review`。本文档帮你分批验收：先看高风险卡，再扫低风险卡，最后统一翻状态。

## 一、验收方法（每卡 3 步）

1. **读卡**：核对「核心问题→系统解答→高频问答索引」结构完整、`[推断]`/`[待确认]` 标注合理
2. **抽查**：每卡抽 2-3 个关键数字/论断，对照 `raw/` 快照验证（卡片 frontmatter 有 `source_docs` 指向 SOURCES.md 登记的 raw 文件）
3. **判定**：通过 → frontmatter `status: review` 改 `stable` + 更新 `updated` 日期；有问题 → 在卡内标注或告诉我修

## 二、风险分层（建议验收顺序）

### 🔴 高风险卡（先验，含 OCR/子代理/源文档自身问题）

| 卡片 | 风险点 | 验收重点 |
|------|--------|----------|
| `architecture/ad-agent-system-landscape.md` | S1 画板双引擎 OCR，19 处 `[待确认]` 残留 | 对照 `raw/s1-whiteboard.png` 原图终核：Loop 计数=10、Tracking Agent、Campaign Structure 归位执行链⑥、Agent→Loop 归属 `[推断]` |
| `meta-ads-diagnosis/meta-operator-daily-workflow.md` | S6 源文档内部矛盾（EQ<6 vs EQ<4） | 确认卡片如实保留矛盾+`[待确认]`（已验证 raw line 13 确有 EQ<6，忠实无误） |
| `meta-ads-diagnosis/meta-diagnosis-layers-l0-l4.md` | S7 字段字典 CPM 双口径、子代理中途退出后补写 | CPM「$8-25 vs ≥5且≤12」双口径标注是否合理；L0-L4 28 项完整性 |
| `meta-ads-diagnosis/meta-diagnosis-sop-agent-training.md` | S7+S4 双源对照，子代理产出 | T0-T5 与 S4 G0-G8 的对应关系描述是否准确 |
| `meta-ads-diagnosis/meta-post-launch-data-inspection.md` | S8 标题「待业务确认」字段口径未定稿 | 卡片是否如实标注源文档状态；漏斗口径差异 `[待确认]` |
| `competitor-analysis/ad-agent-competitor-landscape.md` | S12/S13/S15 容器型壳文档，5 篇引用无权限 | Zalify 卡内容单薄是否符合预期；截图未逐张下载的缺口是否接受 |
| `architecture/ad-ops-agent-research-framework.md` | S14 壳文档+S16 空模板 | MP 方法论回填后（见 business-context/mp-project-methodology）本卡定位是否仍清晰 |

### 🟡 中风险卡（结构复杂但源清晰）

| 卡片 | 风险点 |
|------|--------|
| `meta-ads-diagnosis/meta-diagnosis-sop.md` / `meta-diagnosis-metrics.md` / `meta-action-library.md` | S4 策略树 65 节点/196 分支的拆分边界是否合理 |
| `influencer-boost/` 三张卡 | S3 bitable 5 条「名称-职责错位」记录的归位处理是否正确 |
| `architecture/monitoring-optimization-agent-prd.md` | S5 PRD 细节保真度（六交付物/待评审清单/防呆体系） |

### 🟢 低风险卡（本批新产出，直接从提取文本写成）

| 卡片 | 抽查建议 |
|------|----------|
| `business-context/` 四张卡 | 人群画像关键数字（CPA $16.45/ROAS 6.77/复购 18.8%/NTB 93.9%/T0-T3 分层）对照 `raw/s1-attachments/Momcozy人群画像洞察报告.html`；MP 方法论对照两份 PDF；触点地图对照全触点 HTML |
| `fundamentals/` 三张卡 | S9/S10/S11 HTML 原件文本提取质量高，抽查 eCPM/GSP 公式、8 阶段表即可 |

## 三、已知未决项（验收时可一并确认）

- **S1 画板原图终核**：19 处 `[待确认]` 需要人眼对照 `raw/s1-whiteboard.png`，确认后可批量去标
- **S6 版本号**：文件名 v6 vs 文内 v5.0
- **S8 vs S7 漏斗口径**：访客数+末次归因（四段）vs 事件数（五段）
- **S16 空模板**：等业务填数后增量更新
- **5 篇无权限文档**：用户已确认不补抓，相关 `[待确认]` 保持现状
- **S2 兄弟文档**：父 wiki 空间无权限，01/03 子文档是否存在未确认

## 四、状态流转规则

- 单卡通过 → 该卡 `status: stable`，`updated` 改当日日期
- 全部 21 卡 stable 后，INDEX.md `status` 可从 draft 提为 stable
- 源文档更新 → 走 [UPDATING.md](UPDATING.md) 流程，受影响卡片回到 review
- 发现跨卡新矛盾 → 登记 [CONFLICTS.md](CONFLICTS.md)
