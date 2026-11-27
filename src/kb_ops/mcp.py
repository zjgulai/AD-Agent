"""python -m kb_ops.mcp 入口：stdio MCP Server。

实现在 mcp_server.py；本文件仅为 -m 可执行入口。
MCP 客户端配置见 docs/kb-mcp-setup.md。
"""

from .mcp_server import main

if __name__ == "__main__":
    main()
