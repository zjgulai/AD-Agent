# KB MCP Server 接入指南 — ad-agent-qa

把 ad-agent-qa 知识库（56 卡 / 281 QA / 947 节点领域图谱）暴露为标准
MCP Server，任何支持 MCP 的 Agent（Sage.app / Claude Desktop / Cursor /
Codex CLI / DSH Java）都可直接消费。

- 方案文档：`drafts/docs/kb-mcp-server-plan-20261128.md`
- 工具契约：`drafts/docs/kb-mcp-server-spec-20261128.md`

## 1. 架构

```
Agent (Sage.app / Claude / Cursor)
   │  MCP stdio（JSON-RPC 2.0，newline-delimited）
   ▼
python -m kb_ops.mcp  →  src/kb_ops/mcp_server.py（FastMCP）
   │                        ├─ web/service.py（cards/qa/search/audit/stats）
   │                        ├─ graph_query.py（图谱遍历，dist/graph.json）
   │                        └─ ingest.py（propose → staging 待审）
   ▼
docs/knowledge/ad-agent-qa/（git 源，唯一事实源）
```

- **传输**：stdio only（v1）。HTTP streamable-http 为 v1.1 预留，需先定鉴权。
- **数据源**：直读仓库文件，不依赖 workbench 在线；`KB_ROOT` env 可覆盖。
- **写纪律**：唯一写工具 `kb_ingest_propose` 落 staging `extracted` 态，
  人审门禁不变——不直接写 KB。

## 2. 前置条件

- Python ≥3.10（项目用 3.12）
- 仓库依赖已装：`pip install -r requirements.txt`（含 `mcp>=1.26,<2`）
- KB 图谱已导出：`python -m kb_ops graph-export`（dist/graph.json；
  缺失时 MCP 首次图谱调用会自动重建）

## 3. 客户端配置

### 通用 mcpServers 片段

```json
{
  "kb-agent-qa": {
    "command": "/Users/pray/project/AD/.venv/bin/python",
    "args": ["-m", "kb_ops.mcp"],
    "cwd": "/Users/pray/project/AD/src"
  }
}
```

> **注意 `cwd`**：`src/` 布局下 `python -m kb_ops` 需要 `src/` 在
> sys.path——把 `cwd` 设为 `src/` 目录最省事（`paths.REPO_ROOT` 由
> `__file__` 解析，与 cwd 无关，KB 路径不受影响）。
> 若客户端不支持 cwd，用 `env: {"PYTHONPATH": "/Users/pray/project/AD/src"}`
> 替代。

### Sage.app（扩展中心）

「扩展 → 连接器 → 添加 MCP」→ 粘贴上方 JSON（或表单逐项填：
transport=stdio，command/args/cwd 同上）。配置持久化到
`$SAGE_ROOT/extensions/`。

### Claude Desktop

`~/Library/Application Support/Claude/claude_desktop_config.json` 的
`mcpServers` 节点加入同名条目，重启 Claude Desktop。

### Cursor / Codex CLI / 其他

同构 `mcpServers` JSON；Cursor 在 Settings → MCP 或 `.cursor/mcp.json`。

### 自定义 KB 路径 / staging

```json
{
  "kb-agent-qa": {
    "command": "...",
    "args": ["-m", "kb_ops.mcp"],
    "cwd": "/Users/pray/project/AD/src",
    "env": {"KB_ROOT": "/path/to/kb", "STAGING_DIR": "/path/to/staging"}
  }
}
```

## 4. 工具清单（11 个）

| 工具 | 用途 | 典型调用 |
|---|---|---|
| `kb_search` | BM25 检索 cards+QA+glossary | `kb_search("ROAS 下降排查")` |
| `kb_get_card` | 卡片全文 | `kb_get_card("fundamentals","ad-algo-auto-fields")` |
| `kb_get_qa` | QA 条目（可按 qid 单条） | `kb_get_qa("meta-ads-diagnosis","Q1")` |
| `kb_graph_search` | 图谱节点解析（其他图工具入口） | `kb_graph_search("roas")` |
| `kb_graph_neighbors` | 1-hop 邻居+关系类型 | `kb_graph_neighbors("ad:metric:roas")` |
| `kb_graph_path` | BFS 最短路径 ≤6 跳 | `kb_graph_path("ad:src:s9","ad:metric:roas")` |
| `kb_graph_community` | 社区成员（degree 排序） | `kb_graph_community("ad:metric:roas")` |
| `kb_audit` | validate+kb_audit 实时审计 | `kb_audit()` |
| `kb_conflicts` | CONFLICTS.md 冲突台账 | `kb_conflicts()` |
| `kb_stats` | 规模+commit+生成时间 | `kb_stats()` |
| `kb_ingest_propose` | 投递资料→staging 待审 | `kb_ingest_propose("doc.md", content="# ...")` |

**推荐路径**：`kb_search` 定位 → `kb_get_*` 取全文 → 图谱工具做关系/多跳推理。
Server 启动时通过 MCP `instructions` 注入同样的引导与反模式警告。

## 5. 验证

```bash
# 1. 直接冒烟（不依赖客户端）
cd src && python -m kb_ops.mcp   # stdio 等待 JSON-RPC

# 2. pytest（tool 层 + stdio 冒烟）
python -m pytest tests/test_mcp_server.py tests/test_mcp_smoke.py

# 3. 客户端侧：tools/list 应见 11 个 kb_* 工具；instructions 已注入
```

## 6. 故障排查

| 症状 | 排查 |
|---|---|
| `No module named kb_ops` | cwd 不是 `src/` 且无 PYTHONPATH——按 §3 修正 |
| `No module named mcp` | `.venv` 未装依赖：`uv pip install -r requirements.txt` |
| 图谱工具报 dist 缺失 | 跑 `python -m kb_ops graph-export`（MCP 也会自动重建） |
| propose 报格式错 | 扩展名白名单 + 50MB 上限（复用 ingest 校验） |
| 客户端连不上 | 看客户端日志；stdio server 无日志输出到 stdout（协议要求），stderr 有 FastMCP 日志 |

## 7. v1.1 预留（未实现）

- HTTP streamable-http：`mcp.run(transport="streamable-http")`，
  tool 层零改动；公网暴露前必须先定鉴权方案
- `kb_ask` 服务端应答（复用 kb_bot LLM 配置）
- 向量混合检索（触发条件：qa_logs 显示语义漏检）
