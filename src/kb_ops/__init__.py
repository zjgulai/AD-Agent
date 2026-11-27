"""kb_ops — KB 共享运维层（CLI 可独立运行，供 workbench/bot/CI 复用）。

模块：
- retrieval: BM25 检索（vendored from YesIamGodt/knowledge-pipline, MIT）
- graph_export: graph 分片 → graph.json + 自包含 graph.html（vis.js + Louvain）
- lint_semantic: 确定性语义健康检查（孤儿节点/卡片缺失/CONFLICTS 导出）
- audit_runner: validate.py + kb_audit 子进程包装 → JSON
"""
