"""MCP stdio 冒烟：子进程 JSON-RPC initialize → tools/list → tools/call。

防回归：协议层（FastMCP/stdio）与工具注册的端到端验证。
"""

import json
import os
import queue
import subprocess
import sys
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

EXPECTED_TOOLS = {
    "kb_search", "kb_get_card", "kb_get_qa",
    "kb_graph_search", "kb_graph_neighbors", "kb_graph_path",
    "kb_graph_community",
    "kb_audit", "kb_conflicts", "kb_stats", "kb_ingest_propose",
}


def _recv(q: queue.Queue, timeout: float = 60):
    end = time.time() + timeout
    while time.time() < end:
        try:
            return json.loads(q.get(timeout=max(0.1, end - time.time())))
        except queue.Empty:
            return None
    return None


def test_stdio_smoke():
    env = {**os.environ, "PYTHONPATH": str(SRC)}
    proc = subprocess.Popen(
        [sys.executable, "-m", "kb_ops.mcp"],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL, text=True, env=env,
    )
    try:
        q: queue.Queue = queue.Queue()
        threading.Thread(
            target=lambda: [q.put(l) for l in proc.stdout], daemon=True
        ).start()

        def send(obj):
            proc.stdin.write(json.dumps(obj) + "\n")
            proc.stdin.flush()

        send({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
            "protocolVersion": "2025-03-26", "capabilities": {},
            "clientInfo": {"name": "pytest-smoke", "version": "0"}}})
        r = _recv(q)
        assert r and "result" in r, f"initialize failed: {r}"
        assert r["result"]["serverInfo"]["name"] == "kb-agent-qa"
        assert "instructions" in r["result"]

        send({"jsonrpc": "2.0", "method": "notifications/initialized"})
        send({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
        r = _recv(q)
        names = {t["name"] for t in r["result"]["tools"]}
        assert names == EXPECTED_TOOLS, f"tool set drift: {names ^ EXPECTED_TOOLS}"

        send({"jsonrpc": "2.0", "id": 3, "method": "tools/call",
              "params": {"name": "kb_stats", "arguments": {}}})
        r = _recv(q, timeout=90)  # 首次调用含图谱加载
        text = r["result"]["content"][0]["text"]
        assert "cards:" in text and "graph:" in text
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
