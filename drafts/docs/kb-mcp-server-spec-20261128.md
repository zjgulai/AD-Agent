# KB MCP Server Spec — 工具契约

日期：2026-11-28 · 配套：`kb-mcp-server-plan-20261128.md`

## 0. 总体约定

- **传输**：stdio（newline-delimited JSON-RPC 2.0）。入口 `python -m kb_ops.mcp`。
- **工具层**：`src/kb_ops/mcp_server.py` 中 transport-agnostic 函数 `tool_*`，FastMCP 装饰器仅做协议壳；v1.1 可挂 streamable-http 复用同一层。
- **数据源**：`paths.kb_root()`（`KB_ROOT` env 可覆盖）+ `web/service.py` 加载器；graph 数据走 `service.get_graph()`（dist/graph.json，缺失自动重建）。
- **返回格式**：一律 markdown 文本（MCP `content[].type="text"`），LLM 可读性优先；错误返回 `Error: <原因>` 文本而非协议错误（Agent 可自愈）。
- **规模保护**：所有列表/遍历结果设上限（邻居 100、社区 50、路径 ≤6 跳、search excerpt 600 字符），防上下文爆炸。
- **instructions**：FastMCP 初始化时注入，引导优先 `kb_search`/`kb_get_*`/图谱工具，禁止遍历式拉取。

## 1. 工具契约

### kb_search — BM25 检索

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `query` | string | ✓ | 自然语言或关键词，中英文混合 |
| `top_k` | int | — | 默认 8，范围 1–20 |

**返回**：markdown 列表，每条 `### [score] source (kind)` + 摘要（≤600 字符）。kind ∈ qa/card/glossary。
**复用**：`service.search(root, query, top_k)`（内含 BM25Index 缓存，KB 变更自动重建索引）。
**示例调用**：`kb_search("ROAS 下降怎么排查")`

### kb_get_card — 取卡片全文

| 参数 | 类型 | 必填 |
|---|---|---|
| `cluster` | string | ✓ | 集群目录名，如 `fundamentals`、`meta-ads-diagnosis` |
| `name` | string | ✓ | 卡片文件名（不含 .md），如 `ad-algo-auto-fields` |

**返回**：frontmatter + 正文全文 markdown。带 `status`/`topic`/`source_docs` 元信息头。
**复用**：`service.get_card(root, cluster, name)`；非法 id → `Error: invalid card id`，不存在 → `Error: card not found`。
**提示**：search 命中 card chunk 后用此取全文；QA 用 `kb_get_qa`。

### kb_get_qa — 取 QA 条目

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `cluster` | string | ✓ | QA 文件名（不含 .md），如 `meta-ads-diagnosis` |
| `qid` | string | — | 如 `Q5`；缺省返回全集群全部条目（可能很长） |

**返回**：`### Q5. 问题` + `**A**：答案` + 溯源行。单条模式精确返回。
**复用**：`service.get_qa(root, cluster)` → `_parse_qa_text`。
**注意**：集群文件 40+ 条时全集群返回可能超长——instructions 引导优先用 qid 或先 search。

### kb_graph_search — 节点解析

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `query` | string | ✓ | 节点 id/label 子串（大小写不敏感），如 `roas`、`Meta`、`ad:metric:` |
| `type` | string | — | 类型过滤，`ad:Metric` 等前缀匹配 |
| `cluster` | string | — | 集群过滤 |

**返回**：markdown 表 `id | label | type | cluster | degree`，top 10，附"未找到"提示。
**数据**：`service.get_graph(root)` → nodes 数组线性扫描（947 节点，毫秒级）。
**定位**：其他三个图谱工具的入口——Agent 不知 node_id 时先用此解析。

### kb_graph_neighbors — 1-hop 邻居

| 参数 | 类型 | 必填 |
|---|---|---|
| `node_id` | string | ✓ | 精确节点 id（如 `ad:metric:roas`）；也接受 label 唯一匹配 |

**返回**：中心节点信息 + 邻居列表 `neighbor_id —label→ —[rel_type]→`，标注方向（出边 `->` / 入边 `<-`）；多重边聚合 rel 类型。上限 100 条。
**口径**：无向遍历（双向都算邻居），方向仅作标注。
**数据**：edges 建邻接表（缓存于模块级，graph.json mtime 变化时重建）。

### kb_graph_path — 最短路径

| 参数 | 类型 | 必填 |
|---|---|---|
| `source_id` | string | ✓ |
| `target_id` | string | ✓ |

**返回**：BFS 最短路径节点序列 + 每跳边类型，如
`ad:src:s9 -[ad:sourced_from]-> ad:asset:card-algo-fields -[ad:relates_to]-> ...`
无路径 → `Error: no path within 6 hops`；同节点 → 直接返回。
**上限**：深度 ≤6、访问节点 ≤500（防爆）。

### kb_graph_community — 社区成员

| 参数 | 类型 | 必填 |
|---|---|---|
| `node_id` | string | ✓ |

**返回**：节点所在 community id + 成员列表（按 degree 降序，cap 50）`id | label | type | degree`，总数标注。
**数据**：node.community 字段（graph_export 已跑 Louvain，72 社区）。

### kb_audit — 审计结果

| 参数 | 无 |

**返回**：validate（PASS/FAIL, errors/warnings, error_lines 前 20）+ kb_audit（FAIL/WARN/INFO 计数 + warning_lines 前 20）+ overall ok。
**复用**：`audit_runner.run_all(root=root)`——每次实时跑（validate.py + kb_audit 子进程，秒级）。MCP 进程内无 HTTP 缓存。

### kb_conflicts — 冲突台账

| 参数 | 无 |

**返回**：CONFLICTS.md 两节——冲突总表（id/conflict/side_a/side_b/nature/status）+ 裁决记录（id/status/decision），markdown 表格。
**复用**：`service._parse_conflicts(root)`（私有函数——tool 层内调用，同包可接受；或提取为公开 `parse_conflicts`）。
**用途**：Agent 回答前可查"该知识点是否有未裁决冲突"。

### kb_stats — 规模与版本

| 参数 | 无 |

**返回**：cards 数/集群数、QA 条目数/文件数、graph nodes/edges/communities、graph.json generated 时间、`git rev-parse --short HEAD`（REPO_ROOT 下执行，失败显示 `unknown`）、KB_ROOT 路径。
**复用**：`service.stats(root)` + git subprocess。

### kb_ingest_propose — 投递资料（唯一写工具）

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `filename` | string | ✓ | 原始文件名含扩展名，决定类型与 slug |
| `content` | string | 二选一 | UTF-8 文本内容 |
| `content_base64` | string | 二选一 | 二进制内容（PDF/DOCX/XLSX 等）base64 |

**行为**：调 `ingest.ingest_bytes(filename, data)` → 落 `staging/inbox/` + 自动 `process_file` 提取 → `staging/extracted/<id>.md` + `<id>.json`，状态 `extracted`。
**返回**：item_id、status、content_chars、tables、errors（若有）、以及"待人工评审/生成简报"提示。
**纪律**：不写 KB 本体；不生成简报（`generate_brief` 手动）；staging gitignored。
**校验**：扩展名白名单、50MB 上限、空文件——全部复用 ingest 既有检查，错误透传为 `Error: <msg>`。

## 2. 错误约定

| 场景 | 返回 |
|---|---|
| 参数非法（id 格式/枚举） | `Error: invalid <what>` |
| 资源不存在 | `Error: <what> not found` |
| 图谱节点不存在 | `Error: node not found: <id>`（附 kb_graph_search 提示） |
| 无路径 | `Error: no path within 6 hops` |
| ingest 校验失败 | `Error: <ingest 异常消息>` |
| 意外异常 | `Error: internal: <repr>`（不吞栈到协议层） |

## 3. 非功能需求

- **启动**：`python -m kb_ops.mcp` 冷启动 = import + 首次 tool 调用时懒加载（KnowledgeBase ~500 chunks + graph.json 718KB，<2s）。不在 import 期建索引（避免 MCP initialize 超时）。
- **并发**：stdio 单会话；tool 函数无共享可变状态（service 层缓存 dict 按 root 键，线程安全读多写少可接受）。
- **依赖**：`mcp` 官方包（FastMCP）。requirements.txt 增加；Docker 镜像顺带携带（stdio 不受影响）。
- **测试**：`tests/test_mcp_server.py`——tool_* 函数直测（构造临时 KB_ROOT fixture 或用真实 KB 只读断言）+ stdio JSON-RPC 冒烟（subprocess initialize/tools-list/tools-call kb_stats）。

## 4. 客户端接入（交付文档 `docs/kb-mcp-setup.md`）

```json
// Sage.app「扩展→连接器→添加 MCP」mcpServers 片段
{
  "kb-agent-qa": {
    "command": "/Users/pray/project/AD/.venv/bin/python",
    "args": ["-m", "kb_ops.mcp"],
    "cwd": "/Users/pray/project/AD"
  }
}
```

Claude Desktop / Cursor 同构（`mcpServers` JSON）。环境变量 `KB_ROOT` 可覆盖默认 KB 路径（测试/多 KB 场景）。
