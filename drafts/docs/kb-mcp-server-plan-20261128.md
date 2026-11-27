# KB MCP Server 方案 — ad-agent-qa 知识库对外暴露

日期：2026-11-28 · 状态：已确认（grill 三轮收敛）· 前置：kb-workbench P0-P2 已上线

## 1. 背景与目标

小傅哥《AI Agent 通识教程》第三篇（Ch12 RAG §12.13 + Ch13 LLM-Wiki）提出：**RAG + MCP = 知识库即服务**——实现一次 MCP Server，所有支持 MCP 的 Agent（Claude Desktop / Cursor / Copilot / DSH Java / 自研）即可消费知识库，解决"知识库孤岛"（N 个工具 = N 套对接）。

ad-agent-qa KB 现状：56 卡 / 281 QA / 947 节点 1976 边 schema 图谱 / CONFLICTS 人工裁决 / Ingest 人审管道。消费通道仅两个：飞书 bot（封闭）+ workbench REST（无 MCP 协议、无鉴权）。**外部 Agent 无法接入**——这是相对教程方案唯一的质变级缺口。

**目标**：把 KB 暴露为标准 MCP Server，v1 走 stdio（本机 Agent 直连），tool 层 transport-agnostic，为 v1.1 HTTP 端点铺路。兼容目标客户端：Sage.app（DSH Java 系，stdio/sse/streamable-http 三传输）、Claude Desktop、Cursor、Codex CLI。

## 2. 调研结论（教程技术选型 vs 本项目）

| 教程方案 | 本项目现状 | 判定 |
|---|---|---|
| MCP Server + 13 工具 + instructions 注入 | 无 | 🔴 本方案核心 |
| BM25+向量混合检索（40/60） | BM25 已 vendor + bigram 兜底 | ✅ 语料 ~500 chunks，向量暂缓 |
| GraphRAG（LLM 自动抽三元组） | **人工策展 schema 图谱**（更准） | ✅ 差异化：包装成图工具即"穷人版 GraphRAG" |
| 向量库选型（Chroma/Pinecone/SQLite） | 内存索引即建即用 | ✅ 规模不需要 |
| LLM-Wiki 目录约定 | cards/qa/shards/CONFLICTS 更严 | ✅ 已超越；补 OVERVIEW.md 小缺口 |
| KB 增删改工具 | raw 不可变 + 人审门禁 | ❌ 不学：唯一写工具 = propose 入 staging |

**核心判断**：知识组织层我们已严格超越教程；缺的是"对外暴露层"。MCP 是纯增量，不推翻任何现有结构。

## 3. 架构

```
Agent (Sage.app / Claude / Cursor / Codex)
   │  MCP stdio (JSON-RPC 2.0, newline-delimited)
   ▼
python -m kb_ops.mcp  →  kb_ops/mcp_server.py (FastMCP)
   │                        │ tool 层（transport-agnostic 函数）
   │                        ├─ web/service.py（cards/qa/graph/search/audit/stats）
   │                        ├─ graph shards → dist/graph.json（邻居/路径/社区计算）
   │                        └─ ingest.py（propose → staging，auto-extract）
   ▼
docs/knowledge/ad-agent-qa/（git 源，唯一事实源）
```

- **数据源**：直读仓库文件（`paths.kb_root()`），不依赖 workbench 在线；进程启动建内存索引（~500 chunks，毫秒级）。
- **写纪律**：唯一写工具 `kb_ingest_propose` 走 `ingest.ingest_bytes()` → staging `extracted` 状态；蒸馏简报仍手动，人审门禁不变。
- **v1.1 预留**：tool 层为普通函数，FastMCP 仅做协议壳；HTTP streamable-http 挂载点已预留（`mcp.streamable_http_app()` 可并入现有 FastAPI）。

## 4. 工具集（11 个 + instructions）

| 工具 | 参数 | 返回 |
|---|---|---|
| `kb_search` | query, top_k=8 | BM25 命中：score/source/kind/摘要 |
| `kb_get_card` | cluster, name | 卡片全文 markdown |
| `kb_get_qa` | cluster, qid? | QA 条目（单条或全集群） |
| `kb_graph_search` | query, type?, cluster? | 模糊解析节点（id/label 子串），top10 |
| `kb_graph_neighbors` | node_id | 1-hop 邻居 + 关系类型 + 方向 |
| `kb_graph_path` | source_id, target_id | BFS 最短路径（节点+边序列，≤6 跳） |
| `kb_graph_community` | node_id | 同社区成员（按 degree 排序，cap 50） |
| `kb_audit` | — | validate + kb_audit 结果摘要 |
| `kb_conflicts` | — | CONFLICTS.md 冲突表 + 裁决状态 |
| `kb_stats` | — | 规模统计 + git commit + graph 生成时间 |
| `kb_ingest_propose` | filename, content 或 content_base64 | 落 staging→extracted，返回 item_id |

instructions 注入（FastMCP `instructions` 参数）：引导优先 `kb_search`/`kb_get_*`/图谱工具；反模式：禁止遍历式拉取、禁止把卡片全文当通用文档读。

## 5. 决策记录（grill 三轮收敛）

| # | 决策 | 结论 |
|---|---|---|
| Q1 | 传输形态 | 双形态分阶段：v1 stdio，v1.1 HTTP（需先定鉴权） |
| Q2 | 写权限 | 只读 + `kb_ingest_propose` 唯一写工具（人审门禁不变） |
| Q3 | ask 应答 | v1 仅检索工具，答案由调用方 LLM 合成；`kb_ask` 延后 |
| Q4 | 图谱工具 | 本批做（neighbors/path/community/search 四件套） |
| Q5 | 向量检索 | 不做；触发条件 = qa_logs 显示语义漏检 |
| Q6 | OVERVIEW.md | audit_runner 生成轻量版，Health 视图展示 |
| Q7 | SDK | 官方 `mcp` 包 FastMCP（`mcp.server.fastmcp`） |
| Q8 | 数据源 | 直读文件 + service.py 加载器，不依赖 workbench |
| Q9 | 图谱工具 | 四件套全给 |
| Q10 | propose 深度 | 落盘 + 自动提取到 `extracted`；简报保持手动 |
| Q11 | 验收 | pytest tool 层 + stdio JSON-RPC 冒烟 + 真实客户端联调 |
| Q12 | 分发 | repo 文档 + mcpServers JSON 片段，不做独立 skill 包 |
| Q13 | DSH 兼容 | Sage.app 本机桌面端 → stdio 满足；已确认其扩展中心支持 stdio/sse/streamable-http + mcpServers JSON 导入 |

## 6. 风险与缓解

| 风险 | 缓解 |
|---|---|
| `mcp` 包版本漂移/过新 | 锁定发布 ≥7 天的稳定版进 requirements.txt |
| 图谱邻居/路径口径（有向 vs 无向） | 遍历按无向，返回注明方向（`A -[rel]-> B` / `A <-[rel]- B`） |
| propose 被滥用灌 staging | v1 仅本机 stdio（无公网暴露）；文件类型白名单 + 50MB 上限复用 ingest 既有校验 |
| MCP 启动建索引耗时 | ~500 chunks BM25 建索引 <1s；graph.json 718KB 一次性加载 |
| Sage.app 侧 python 环境 | 文档给 `.venv/bin/python` 绝对路径方案；备选 `uv run --with mcp` |

## 7. 明确不做（v1.1+）

- HTTP streamable-http 端点 + 公网鉴权（Bearer token 或只读白名单，待远程 Agent 真实需求）
- `kb_ask` 服务端 LLM 应答（需 LLM_API_KEY 注入 MCP 进程）
- 向量/Embedding 混合检索（触发条件见 Q5）
- KB 增删改类工具（create/update/delete/upload_document 等，违反人审门禁）
- Deep Research / Agentic RAG 多轮检索

## 8. 实施拆分（详见 tickets 文档）

T1 依赖+mcp_server 骨架+非图工具 → T2 图谱四件套 → T3 propose+入口+instructions → T4 OVERVIEW.md+Health → T5 测试+文档 → T6 Sage 实测+提交部署
