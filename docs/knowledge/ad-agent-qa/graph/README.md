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
│   ├── classes.json     # 对象类型（Metric/DiagnosisNode/Action/Agent…）v0.1.1
│   ├── relations.json   # 关系类型 v0.1.2（22 种，含 ad:implements）
│   ├── terms.json       # SKOS-lite 术语（term_id + 消歧 + alt_labels）
│   └── rules.json       # 契约规则（铁律/阈值/冲突登记指针）
├── instances/     # 实例层：按集群分片，<cluster>.nodes.json + <cluster>.edges.json
│   └── meta-ads-diagnosis.*   # P2 试点：257 节点 / 570 边
├── tools/
│   └── validate.py     # 校验器：schema 一致性 + 溯源完整性 + domain/range
└── provenance/    # 溯源约定见下（实际以边上 ref 字段承载）

experience/        # 经验卡池（飞轮）：draft → approved → promoted / archived
logs/              # bot 问答日志（gitignore）
```

## 约定

- **ID 方案**：`ad:` 前缀。类 `ad:Metric`；术语 `ad:term:eq`；实例 `ad:metric:eq`；诊断节点 `ad:diag:s7:l0-02`（系统前缀 s4/s6/s7 区分编号体系）
- **实例文件格式**：每集群两个文件——`*.nodes.json`（`nodes` 数组）+ `*.edges.json`（`edges` 数组），文件头含 `defaults`（生命周期字段默认值）与 `coverage_notes`（抽取边界声明）
- **溯源**：节点用 `src: ["card:<file>", "raw:<src>"]`，边用 `ref: "card:<file>#L<lines>"`。无 ref 的边不入图；`raw:` 指向 raw/ 源文档，`card:` 指向 cards/ 卡片
- **生命周期字段**：`status`（active/deprecated/candidate）、`confidence`（high/medium/low）、`freshness`（fresh/watch/stale）、`last_verified`——文件级 `defaults` 统一给默认值，个别边/节点可覆盖（如 `status: pending_business`）
- **口径冲突**：不静默选边。`conflicts_with` = 同检查点阈值打架（挂 CONFLICTS C 编号 + pending_business）；`variant_of` = 不同检查点/分母的合法口径差异
- **厚图谱建模**：流程是一等公民——`ad:Playbook`（S4 策略树/S7 SOP/S6 工作流）作容器，`ad:DiagnosisCheck`（判定点）与 `ad:WorkflowStage`（S6 环节）经 `part_of`/`depends_on`/`triggers(when)` 表达决策流
- **platform-ops-kb 对象**：provenance 记 `object_id` + 仓内相对路径，不复制内容进图
- **变更流程**：schema 变更需用户评审；实例变更走 git diff 可 review；经验卡晋升才改 schema/实例
- **校验**：`python3 graph/tools/validate.py` —— 检查 @type 注册、边端点存在、ref 溯源、domain/range 约束

## 与上下游的关系

| 层 | 位置 | 消费者 |
|----|------|--------|
| 源文档 | 飞书 S1–S21 / platform-ops-kb objects | 人 |
| 文档层 | `cards/` + `qa/` | bot 检索、agent 路由 |
| **语义层** | `graph/`（本目录） | bot 实体链接、SCN-011 Agent、graph_query 包 |
| 语义底座 | AI-Native-Organization（外部仓） | 组织级——本图谱将来以 `ad:` 域接入 |
