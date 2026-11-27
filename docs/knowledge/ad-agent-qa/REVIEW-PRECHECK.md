---
title: KB 机器预审报告
doc_type: knowledge
module: ad-agent-qa
topic: review-precheck
status: review
created: 2026-11-27
owner: self
source: ai
---

# KB 机器预审报告

> 由 `src/kb_audit.py` 生成——REVIEW.md 人工验收前的机器过滤层。
> FAIL=结构性问题必修；WARN=需人眼判断；INFO=提示。

**统计**：37 卡 / 7 QA 文件 / 200 Q 条目 / 434 链接检查

**结果**：FAIL 0 · WARN 0 · INFO 4

| 级别 | 文件 | 问题 |
|------|------|------|
| INFO | `cards/architecture/ad-agent-system-landscape.md` | [待确认]×15 残留偏多，验收时重点核 |
| INFO | `cards/architecture/monitoring-optimization-agent-prd.md` | [待确认]×13 残留偏多，验收时重点核 |
| INFO | `cards/influencer-boost/influencer-boost-agent-specs.md` | [待确认]×20 残留偏多，验收时重点核 |
| INFO | `glossary.md` | 术语表约 113 条 |
