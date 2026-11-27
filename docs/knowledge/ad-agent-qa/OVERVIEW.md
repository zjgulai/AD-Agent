# KB OVERVIEW — ad-agent-qa

> 自动生成（`python -m kb_ops.audit`），反映 KB 内容最新状态 （2026-11-27）。目录权威见 INDEX.md，源登记见 SOURCES.md，冲突裁决见 CONFLICTS.md。

## 规模

| 维度 | 数量 |
|---|---|
| 知识卡 | 53 张 / 7 集群 |
| QA 条目 | 281 条 / 7 文件 |
| 图谱 | 947 节点 · 1976 边 · 72 社区 / 14 分片集群 |
| graph.json 生成 | 2026-11-27 |

## 集群地图

| 集群 | 卡片 | QA | 代表卡片 |
|---|---|---|---|
| architecture | 3 | 19 | `ad-agent-system-landscape`, `ad-ops-agent-research-framework`, `monitoring-optimization-agent-prd` |
| business-context | 7 | 31 | `audience-layering-playbook`, `cross-border-expansion-framework`, `customer-touchpoint-map` … |
| competitor-analysis | 1 | 6 | `ad-agent-competitor-landscape` |
| fundamentals | 9 | 53 | `ab-testing-methodology`, `ad-account-governance`, `ad-algo-auto-fields` … |
| influencer-boost | 4 | 26 | `creator-partnership-models`, `influencer-boost-agent-specs`, `influencer-boost-build-tracking` … |
| meta-ads-diagnosis | 9 | 40 | `meta-action-library`, `meta-diagnosis-layers-l0-l4`, `meta-diagnosis-metrics` … |
| platform-ops | 20 | 106 | `ad-creative-strategy-system`, `amazon-ads-operations`, `amazon-ads-playbook` … |

## 审计状态

- validate.py：PASS （0 errors / 0 warnings）
- kb_audit：FAIL 0 / WARN 0 / INFO 4 · overall OK

## 使用入口

- 检索：workbench Search 视图 · `python -m kb_ops search "<query>"` · MCP `kb_search`
- 全文：workbench Cards/QA 视图 · MCP `kb_get_card` / `kb_get_qa`
- 图谱：workbench Graph 视图 · MCP `kb_graph_search/neighbors/path/community`
- 摄入：workbench Ingest 视图 · MCP `kb_ingest_propose`（staging 待审，蒸馏与发布仍需人工）
