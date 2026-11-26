---
title: 广告投放域知识图谱
doc_type: knowledge
module: ad-agent-qa
topic: knowledge-graph
status: review
created: 2026-11-26
updated: 2026-11-26
owner: self
source: human+ai
---

# 广告投放域知识图谱（graph/）

> 本目录是 ad-agent-qa 的**语义层**：cards/qa 管「文档正文」，graph/ 管「实体-关系结构」。
> 设计对齐语义底座（SKOS-lite 模式层 + JSON 实例层），不建语义数据库。

## 目录结构

```
graph/
├── schema/        # 模式层：什么可以存在（类/关系/术语/规则）
│   ├── classes.json     # 对象类型（Metric/DiagnosisNode/Action/Agent…）
│   ├── relations.json   # 关系类型（checks/triggers/conflicts_with…）
│   ├── terms.json       # SKOS-lite 术语（term_id + 消歧 + alt_labels）
│   └── rules.json       # 契约规则（铁律/阈值/冲突登记指针）
├── instances/     # 实例层：实际节点与边（P3 起按集群分片 JSON）
└── provenance/    # 溯源：每条边的 source_ref → 卡片节号 / raw 源 / object_id

experience/        # 经验卡池（飞轮）：draft → approved → promoted / archived
logs/              # bot 问答日志（gitignore）
```

## 约定

- **ID 方案**：`ad:` 前缀。类 `ad:Metric`；术语 `ad:term:eq`；实例 `ad:metric:eq`；边 `ad:edge:<from>-<rel>-<to>`
- **每条边必须带 `source_ref`**：`{card, section}` 或 `{object_id}`（platform-ops-kb）或 `{raw, locator}`。无来源不入图
- **生命周期字段**（实例与边通用）：`status`（active/deprecated/candidate）、`confidence`（high/medium/low）、`freshness`（fresh/watch/stale）、`last_verified`
- **口径冲突**：不静默选边。冲突实体用 `conflicts_with` 边连接，`status` 标 `pending_business` 或 `dual-口径`
- **platform-ops-kb 对象**：provenance 记 `object_id` + 仓内相对路径，不复制内容进图
- **变更流程**：schema 变更需用户评审；实例变更走 git diff 可 review；经验卡晋升才改 schema/实例

## 与上下游的关系

| 层 | 位置 | 消费者 |
|----|------|--------|
| 源文档 | 飞书 S1–S21 / platform-ops-kb objects | 人 |
| 文档层 | `cards/` + `qa/` | bot 检索、agent 路由 |
| **语义层** | `graph/`（本目录） | bot 实体链接、SCN-011 Agent、graph_query 包 |
| 语义底座 | AI-Native-Organization（外部仓） | 组织级——本图谱将来以 `ad:` 域接入 |
