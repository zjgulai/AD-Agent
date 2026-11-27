# KB MCP Server Tickets — 执行拆分

日期：2026-11-28 · 状态：T1–T5 完成已部署（commit 80e1cf2，镜像 kb-workbench:80e1cf2-20261128）；T6 余 Sage.app GUI 配置（协议已验证） · Spec：`kb-mcp-server-spec-20261128.md` · Plan：`kb-mcp-server-plan-20261128.md`

状态标记：[ ] 待办 / [~] 进行中 / [x] 完成

---

## T1 — 依赖 + mcp_server 骨架 + 非图工具

**文件**：`requirements.txt`、`src/kb_ops/mcp_server.py`（新建）、`src/kb_ops/__main__.py`（+`mcp` 子命令）

- [x] `requirements.txt` 加 `mcp`（选发布 ≥7 天的稳定版，`pip index versions mcp` 或 PyPI 确认；装到 `.venv` 验证 import）
- [x] `mcp_server.py` 骨架：`FastMCP("kb-agent-qa", instructions=...)` + `main()`（`mcp.run()` stdio）
- [x] tool 层函数（transport-agnostic，返回 markdown str）：
  - `tool_search(query, top_k=8)` → `service.search`
  - `tool_get_card(cluster, name)` → `service.get_card`（try/except → `Error:`）
  - `tool_get_qa(cluster, qid=None)` → `service.get_qa` + `_parse_qa_text` 过滤
  - `tool_audit()` → `audit_runner.run_all(root=kb_root())` markdown 化
  - `tool_conflicts()` → `service` 的 conflicts 解析（把 `_parse_conflicts` 提为公开 `parse_conflicts` 或 tool 内调用）
  - `tool_stats()` → `service.stats` + git commit + graph.generated
- [x] FastMCP `@mcp.tool()` 装饰器注册上述 6 个，docstring 即工具描述
- [x] `__main__.py` 加 `elif cmd == "mcp": from . import mcp_server; mcp_server.main()`

**验收**：`python -m kb_ops.mcp` 启动后手动 JSON-RPC initialize/tools-list 通；`pytest tests/test_mcp_server.py -k "search or get_card"` 绿。

## T2 — 图谱四件套

**文件**：`src/kb_ops/mcp_server.py`、`src/kb_ops/graph_query.py`（新建，或并入 mcp_server——倾向独立模块便于复用/测试）

- [x] `graph_query.py`：`load_graph(root)`（走 `service.get_graph`，缓存 adjacency：`dict[node_id, list[(neighbor_id, rel_type, direction)]]`，按 graph.json mtime 失效）
- [x] `find_node(graph, query)`：id 精确 → label/id 子串模糊（top1 唯一匹配才返回，多匹配返回候选列表）
- [x] `tool_graph_search(query, type=None, cluster=None)`：线性扫描 nodes，markdown 表 top10
- [x] `tool_graph_neighbors(node_id)`：adjacency 展开，聚合多重边 rel 类型，方向标注 `->`/`<-`，cap 100
- [x] `tool_graph_path(source_id, target_id)`：BFS 最短路径 ≤6 跳，返回节点+边序列
- [x] `tool_graph_community(node_id)`：node.community → 同社区成员按 degree 降序 cap 50
- [x] 注册 4 个 `@mcp.tool()`

**验收**：真实图谱上 `kb_graph_search("roas")`、`neighbors`、`path`（两已知节点）、`community` 各返回合理 markdown；孤立/不存在节点返回规范 `Error:`。

## T3 — kb_ingest_propose + instructions 收尾

**文件**：`src/kb_ops/mcp_server.py`

- [x] `tool_ingest_propose(filename, content=None, content_base64=None)`：二选一校验 → `base64.b64decode` 或 utf-8 encode → `ingest.ingest_bytes(filename, data)` → markdown 返回 item_id/status/content_chars/errors + 人审提示
- [x] `@mcp.tool()` 注册
- [x] FastMCP `instructions` 文案定稿（中文，约 10 行：定位/优先顺序 search→get→graph/反模式/ingest_propose 用途与人审门禁）

**验收**：pytest 临时 STAGING_DIR 投递 `.md` 文件 → `extracted/<id>.md` 存在、item status=extracted；非法扩展名/双空内容返回 Error。

## T4 — OVERVIEW.md + Health 展示

**文件**：`src/kb_ops/audit_runner.py`（+generate_overview）、`src/kb_ops/web/service.py`（`_DOC_NAMES` +`OVERVIEW.md`）、`src/kb_ops/web/static/app.js`（Health 视图加卡）、`docs/knowledge/ad-agent-qa/OVERVIEW.md`（生成产物，入库）

- [x] `audit_runner.py`：`generate_overview(root) -> str`——规模统计（复用 service.stats 口径或直接算）+ clusters 列表 + 每集群卡数/QA 数 + 图谱 communities 数 + generated 时间；`main()` 在 run_all 后写 `root/OVERVIEW.md`（内容不变不重写，避免无意义 diff）
- [x] `service.py` `_DOC_NAMES` 加 `"OVERVIEW.md"`
- [x] `app.js` Health 视图：新增「KB 概览」卡，从 `/api/doc/OVERVIEW.md` 拉取渲染（markdown 容器复用 `.md` 样式）；文件缺失时优雅降级显示"运行 kb_audit 生成"
- [x] 本地跑 `python -m kb_ops.audit` 生成 OVERVIEW.md 验证内容

**验收**：`/api/doc/OVERVIEW.md` 200；Health 页可见概览卡；`kb_audit` 重跑 OVERVIEW.md 无脏 diff（幂等）。

## T5 — 测试 + 冒烟 + 接入文档

**文件**：`tests/test_mcp_server.py`（新建）、`tests/test_mcp_smoke.py`（新建或并入）、`docs/kb-mcp-setup.md`（新建）

- [x] `test_mcp_server.py`：tool_* 函数直测——search 命中已知查询、get_card 真实卡、get_qa qid 过滤、graph_search/neighbors/path/community 正常+异常路径、conflicts/stats 结构、ingest_propose 到 tmp staging
- [x] `test_mcp_smoke.py`：subprocess 起 `python -m kb_ops.mcp`，stdin 发 JSON-RPC `initialize` → `notifications/initialized` → `tools/list`（断言 11 工具名）→ `tools/call kb_stats`（断言 markdown 含 cards 数）；用 `mcp` client SDK 或裸 JSON-RPC line-delimited
- [x] `docs/kb-mcp-setup.md`：原理一句话 + mcpServers JSON（Sage.app/Claude Desktop/Cursor 三形态同构）+ KB_ROOT/STAGING_DIR env + 工具清单速查 + 故障排查（python 路径、venv、KB_ROOT）
- [x] `AGENTS.md` 或 README 补一行入口指引（若有合适位置）

**验收**：`pytest tests/` 全绿（84 旧 + 新）；smoke 脚本独立可跑 `python tests/test_mcp_smoke.py`（或 pytest -k smoke）。

## T6 — Sage.app 实测 + 提交 + 部署

- [ ] 临时 config 实测：按 `docs/kb-mcp-setup.md` 片段在 Sage.app「扩展→连接器→添加 MCP」接入（协议层已用官方 mcp ClientSession 验证；GUI 配置留用户操作）
- [x] 验证：tools/list 11 工具可见、instructions 注入生效（官方 mcp ClientSession 握手通过；GUI 内问答留用户验证）
- [x] `git status/diff` 审查 → commit（含 drafts/docs 三件套 + OVERVIEW.md）
- [x] push（SSH remote，HTTPS 抖动绕过）
- [x] `./deploy/deploy.sh` 部署 workbench（T4 改了 web 静态文件+service，容器内需新镜像；MCP stdio 本身不依赖部署）
- [x] 生产验收：`/api/doc/OVERVIEW.md` 200、Health 卡渲染、其余视图回归

**验收**：Sage.app 内 MCP 工具可调用且返回正确；ad.sagegogo.com Health 视图含概览卡；pytest 全绿。

---

## 依赖关系

```
T1 ──► T2 ──► T3 ──► T5 ──► T6
         └──► T4 ──┘（T4 独立，可与 T2/T3 并行）
```

T1 是所有后续前置；T2/T3 可并行于 T4；T5 收口测试；T6 交付。
