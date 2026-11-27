---
title: 知识工作台建设方案 — 借鉴 knowledge-pipline 的技术方案
doc_type: workflow
module: knowledge-base
topic: kb-workbench
status: draft
created: 2026-11-27
updated: 2026-11-27
owner: self
source: human+ai
---

# 知识工作台建设方案

## 1. 背景与目标

对话 Agent（`src/kb_bot`，飞书问答）之外，建设**知识工作台**：KB 的运维控制台 + 人类可视化层。

- **定位**：两者兼顾——内部运营控制台优先，架构预留对外化（auth/多租户后置）
- **范围**：P0 静态层 → P3 增强，全量推进
- **技术栈**：FastAPI + 原生 JS（无构建链）
- **核心纪律**：KB 源（`docs/knowledge/ad-agent-qa/` 的 markdown+JSON）仍是唯一事实源，git 版本化；工作台只读为主，写操作走既有批次流程

## 2. knowledge-pipline 技术剖析结论

来源：`github.com/YesIamGodt/knowledge-pipline`（MIT，已调研，克隆于 /tmp）。LLM Wiki 编译器——文档 → wiki 页面 + claims.json + 自动图谱 + LivePPT。

### 借鉴清单

| 模块 | 位置 | 借鉴方式 | 落地为 |
|------|------|----------|--------|
| BM25 检索（零依赖，中英文混合分词） | `core/retrieval.py` 175 行 | **vendor 源码**（MIT，保留署名） | `src/kb_ops/retrieval.py`，升级 kb.py 打分 + 工作台搜索 |
| 图谱导出（EXTRACTED/INFERRED 分层 + Louvain + vis.js 自包含 HTML + SHA256 缓存） | `tools/build_graph.py` 686 行 | **借模式重写**（我们的边是 schema 校验的策展边，无 EXTRACTED/INFERRED 之分；Louvain 社区 + vis.js 投影照搬） | `src/kb_ops/graph_export.py` → `graph/dist/graph.html` |
| BFS 推理链（图上找路径 → 可视化） | `pipeline_query.py --rc` | **借模式**（P3） | `/api/graph/path` + 图谱高亮路径 |
| 多格式文件处理器（PDF/DOCX/XLSX/PPTX/HTML/图片） | `backend/processors/` ~2000 行 | **vendor 子集**（pdf/docx/xlsx/html/image；video 暂缓） | `src/kb_ops/processors/` |
| claims.json 矛盾检测模式 | `pipeline_ingest.py` + `pipeline_lint.py` | **借模式**：抽 claims → 跨源 LLM 比对 → 候选矛盾进 pending 队列（人审裁决不变） | `src/kb_ops/lint_semantic.py` |
| 语义层 lint（孤立/过时/数据空白/缺失实体） | `pipeline_lint.py` | **借模式**：叠加在确定性 kb_audit 之上 | 同上 |
| 多源聚合查询（共识✅/分歧⚠️/单源❓三段式） | `pipeline_query.py` | **借模式**：bot 回答与工作台 ask 的升级方向 | P3 |
| 命令模式（ingest/query/lint/graph 均为 Python CLI） | `tools/*.py` | **已同构**：我们的 ops 层同样做成 CLI，工作台只是 GUI | `src/kb_ops/` 全部可 `python -m` 运行 |

### 不借鉴清单

| 项 | 原因 |
|----|------|
| wiki 松散页面模型（sources/entities/concepts/syntheses） | 我们的 cards/qa/graph-shard/CONFLICTS 分层更严格，已有 validate.py schema 门禁 |
| LLM auto-merge 实体页 | 降低人工蒸馏质量；卡片必须人审 |
| INFERRED 边直接入图 | 我们的边必须过 schema 校验；推断边只能进「建议队列」等人审后手工入分片 |
| LivePPT 子系统（~5000 行） | 体量过大，列为 P3+ 独立评估（KB→营销周报 PPT 是潜在下游） |

## 3. 总体架构

```
┌─ 知识工作台 (FastAPI + 原生 JS SPA) ────────────┐
│  KB 浏览器 │ 图谱探索器 │ 摄入管道 │ 健康面板     │
│  搜索     │ 推理链(P3)│ 对话内嵌(P3)│             │
├─ src/kb_ops/ 共享运维层（CLI 可独立运行）────────┤
│  retrieval.py(BM25) │ loader.py │ graph_export  │
│  lint_semantic.py │ ingest.py │ audit_runner   │
│  processors/ (PDF/DOCX/XLSX/HTML/IMG)           │
├─ KB 源（git，唯一事实源，schema 契约不变）───────┤
│  docs/knowledge/ad-agent-qa/                    │
│  raw/ cards/ qa/ glossary.md graph/ INDEX...    │
└────────────────────────────────────────────────┘
     ▲ 同层消费        ▲ 同层消费
  kb_bot(飞书)      Devin 蒸馏批次 / CI
```

设计约束：
- `kb_ops` 零 FastAPI 依赖（stdlib + networkx + 可选 LLM），CLI/API/bot 三方复用
- 写操作不直改 KB：摄入走 staging → 人审 → 既有批次流程发布
- 对外化预留：app factory + 配置化 middleware 位，P1 不实现 auth

## 4. P0 — 静态层（先行，零服务器）

目标：当天见效，补齐「图谱不可见 + 检索可升级 + 语义健康不可见」三大盲区。

### 4.1 `src/kb_ops/retrieval.py`
- vendor `core/retrieval.py`（BM25Index + tokenize，中英文混合分词）
- 适配：索引对象从 wiki 页面改为复用 `kb.py` 的 Chunk（qa/card/glossary/index 四类）
- `search(query, top_k) -> [(chunk, score)]`
- kb_bot 检索升级为**可选开关**（config flag，默认先不切，workbench 先用）

### 4.2 `src/kb_ops/graph_export.py`
- 读 `graph/instances/*.nodes.json` + `*.edges.json`（14 分片）→ 合并去重（@id 合并，跨分片边保留）
- 节点投影：`{id, label, type, cluster(分片), degree, props摘要}`
- 边投影：`{type, source, target, ref}`
- Louvain 社区检测（`networkx`，新增依赖 `networkx>=3.2`）→ `community` 字段
- 输出 `docs/knowledge/ad-agent-qa/graph/dist/graph.json` + `graph.html`
- `graph.html`：自包含 vis.js（vendor `vis-network` standalone build 到 `src/kb_ops/static/vendor/`），特性：
  - 节点按 @type 着色、按 community 描边、按 cluster 分片过滤
  - 搜索框（label/@id 模糊匹配）、关系类型过滤、点击节点 → 详情侧栏（props + 一阶邻居 + sourced_from 溯源）
  - SHA256 内容哈希缓存（源分片未变跳过重建）
- CLI：`python -m kb_ops.graph_export [--open]`

### 4.3 `src/kb_ops/lint_semantic.py`
- 确定性部分（无 LLM 也可跑）：
  - 图谱孤儿节点：无任何边的节点、KnowledgeAsset 无卡片文件背书
  - 卡片时效：frontmatter/正文日期 vs SOURCES.md 最近批次
  - CONFLICTS pending_business 清单导出
- LLM 语义部分（可选，复用 `kb_bot/llm.py` 配置）：
  - 候选矛盾：卡片两两 claims 比对（限同集群、限高风险对）→ 输出到 `REVIEW-PRECHECK` 风格报告
  - 数据空白：flywheel logs 高频 no-hit 主题聚类 → 建议补源
- 输出：`docs/knowledge/ad-agent-qa/REVIEW-SEMANTIC.md`（不覆盖既有 REVIEW-PRECHECK）

### 4.4 `src/kb_ops/audit_runner.py`
- 子进程包装 `graph/tools/validate.py` + `src/kb_audit.py` → 解析输出为 JSON（供 API 用）+ 原样 markdown 报告
- CLI：`python -m kb_ops.audit_runner [--json]`

### P0 验收
- `python -m kb_ops.graph_export --open` 打开交互图谱（900+ 节点可探索）
- `pytest` 全绿（新增 ops 层单测）
- CI 不受影响（dist/ gitignore）

## 5. P1 — FastAPI 工作台 MVP

### 5.1 `src/kb_workbench/`
```
kb_workbench/
├── __init__.py
├── __main__.py        # python -m kb_workbench --port 8080
├── main.py            # FastAPI app factory + 路由
├── config.py          # KB_ROOT / LLM / env 配置
└── static/
    ├── index.html     # 单页 SPA（hash 路由）
    ├── app.js         # 原生 JS，无构建
    ├── style.css
    └── vendor/        # marked.js + vis-network（P0 已 vendor）
```

### 5.2 API（全部只读，GET only）
| 端点 | 数据源 | 说明 |
|------|--------|------|
| `GET /api/cards` | 扫描 cards/**/*.md frontmatter | 按 cluster 分组：title/path/cluster/status |
| `GET /api/cards/{path}` | 卡片 markdown | 服务端转 JSON（frontmatter+body），前端 marked.js 渲染 |
| `GET /api/qa` | qa/*.md 解析 Q 条目 | 按 cluster 分组，含溯源标签 |
| `GET /api/search?q=` | kb_ops BM25 | cards+qa+glossary+index 混合召回，返回 chunk+score+source |
| `GET /api/graph` | graph_export 输出 | nodes/edges/communities/meta |
| `GET /api/graph/stats` | 同上 | 分片/类型/关系分布统计 |
| `GET /api/health` | audit_runner + CONFLICTS + flywheel | FAIL/WARN/INFO、pending 裁决数、QA 日志统计 |
| `GET /api/sources` | SOURCES.md 解析 | 源登记表（批次/范围/排除项） |
| `GET /api/conflicts` | CONFLICTS.md 解析 | C1-C18 状态表（已裁决/待确认/pending_business） |

### 5.3 前端视图（hash 路由）
- **Cards**：左侧集群树，右侧卡片渲染（frontmatter 折叠、表格、代码块）
- **QA**：按 cluster 浏览 Q 条目，搜索过滤
- **Graph**：复用 P0 graph.html 的 vis.js 组件，嵌入式 + 路由联动（点节点跳卡片）
- **Health**：audit 结果表 + CONFLICTS 状态看板 + 飞轮统计（qa 日志按天/集群）
- **Search**：全局搜索框，结果按 kind 分组（qa/card/glossary）

### 5.4 工程约定
- `requirements.txt` 新增：`fastapi`、`uvicorn`、`networkx`（P0 已加）、`python-multipart`（P2 预留）
- `python -m kb_workbench` 启动；`KB_ROOT` env 可覆盖（默认 repo 内 KB 路径）
- 测试：`tests/test_kb_workbench.py` 用 fastapi TestClient 冒烟全部 GET 端点
- 对外化预留：`create_app(config)` 工厂签名；auth/HTTPS/域名映射不在 P1

### P1 验收
- `python -m kb_workbench` → 浏览器打开五个视图全部可用
- 搜索命中 QA/卡片/glossary，点击溯源跳转
- 图谱页与 P0 graph.html 同等交互
- `pytest tests/` 全绿（25 旧 + 新增）

## 6. P2 — 摄入管道

目标：把「扔文档进 KB」从手工流程变成工作台可视流程（蒸馏仍由 Agent/人完成）。

### 6.1 `src/kb_ops/processors/`
- vendor knowledge-pipline `backend/processors/` 子集：`file_processor.py` + `pdf/docx/xlsx/html/image` 处理器（MIT 署名保留）
- 裁剪：video_processor 暂缓；OCR（paddleocr）做成可选依赖
- 统一接口：`process(path) -> {content_md, metadata, tables?}`

### 6.2 `src/kb_ops/ingest.py` + staging 目录
- `staging/`（gitignore 或独立目录，不进 KB 源）：上传文件 + 提取结果 + 任务状态
- 流程：
  1. `POST /api/ingest/upload`（multipart）→ 存 `staging/inbox/<date>-<slug>.<ext>`
  2. processor 提取 → `staging/extracted/<id>.md` + 元数据
  3. 工作台「摄入」视图：预览提取 markdown + 元数据 + 「生成蒸馏简报」按钮
  4. 蒸馏简报 = 自动生成 batch prompt（格式对齐现有 S/G 批次：范围界定/排除项/卡片建议/QA 建议/图谱节点建议），复制给 Devin/Agent 会话执行
  5. 发布仍走既有批次流程（cards/qa/graph/SOURCES 登记）——工作台只追踪状态不自动写 KB
- 状态机：`uploaded → extracted → briefed → distilled → published`（人工推进）

### P2 验收
- 上传一份 PDF/xlsx → 提取预览正确 → 简报可生成 → 走完一次真实蒸馏批次闭环

## 7. P3 — 增强（按价值排序，独立评估）

| 项 | 说明 | 依赖 |
|----|------|------|
| 推理链可视化 | `/api/graph/path?a=&b=` BFS 最短路径 → 图谱高亮 + 关系序列说明（借鉴 pipeline_query --rc） | P1 graph |
| 对话内嵌 | `/api/ask` 复用 kb chunks + graph_query 实体链接 + llm.py，工作台内直接问答 | P1 + llm 配置 |
| 多源聚合回答 | 共识/分歧/单源三段式（借鉴 pipeline_query），升级 bot 与 ask | 对话内嵌后 |
| 语义 lint 定时跑 | lint_semantic 挂 cron/手动触发，结果进 Health 面板 | P0 lint + P1 health |
| LivePPT 式导出 | KB → 营销周报/复盘 PPT 大纲（独立评估，~5000 行级别工程） | 单独立项 |
| 对外化 | auth（token/SSO）、只读公开模式、域名/HTTPS | 有明确外部需求再做 |

## 8. 工程约定

- **License**：vendor 文件头部保留 `# Vendored from YesIamGodt/knowledge-pipline (MIT)`；SOURCES.md 不需登记（代码非知识源）
- **依赖最小化**：stdlib 优先；新增仅 fastapi/uvicorn/networkx/python-multipart（P2）+ 文件处理器依赖（pypdf/python-docx/openpyxl/beautifulsoup4，P2 按需）
- **测试**：ops 层单测（retrieval/graph_export/lint 纯函数部分）+ workbench TestClient 冒烟；CI 走现有 `pytest tests/`
- **不引入**：数据库、向量库、前端构建链、Docker（除非部署需要）
- **文档**：本文件即方案；实现时同步 `src/kb_bot/README.md` 同级补 `src/kb_workbench/README.md`

## 9. 风险与开放问题

| 风险 | 缓解 |
|------|------|
| graph.html 900+ 节点渲染性能 | vis.js 支持，必要时按 cluster 懒加载/过滤；P0 实测验证 |
| BM25 替换影响 bot 回答质量 | 默认不切；config flag 灰度，workbench 先用一段时间对比 |
| processors 依赖重（paddleocr 等） | OCR 可选依赖，图片先走「不处理/人工」路径 |
| 对外化需求临时出现 | app factory + config 预留；auth 中间件接口先占位 |
| 蒸馏瓶颈不在工作台 | P2 只解决「摄入→简报」，蒸馏仍靠 Agent 批次——这是刻意的人审门禁，不自动化 |

## 10. 验收总览

- P0：graph.html 可交互探索全图谱；BM25/lint/audit CLI 可用；pytest 绿
- P1：五视图可用的内部工作台；pytest 绿；CI 绿
- P2：一次真实文档摄入→蒸馏→发布闭环走通
- P3：按单项评估立项
