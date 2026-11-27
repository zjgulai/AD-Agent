"""audit_runner：包装 validate.py + kb_audit，输出统一 JSON 结果。

供 workbench /api/health 与 CLI 使用；不重新实现检查逻辑，只解析输出。

CLI：python -m kb_ops.audit_runner [--json] [--strict]
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

from .paths import REPO_ROOT, kb_root

_AUDIT_MODULE = "kb_audit"
_AUDIT_CWD = REPO_ROOT / "src"


def _run(cmd: list[str], cwd: Path) -> dict:
    proc = subprocess.run(
        cmd, cwd=cwd, capture_output=True, text=True, timeout=300,
    )
    return {"cmd": " ".join(cmd), "returncode": proc.returncode,
            "stdout": proc.stdout, "stderr": proc.stderr}


def parse_validate(stdout: str) -> dict:
    m = re.search(r"(PASS|FAIL):\s*(\d+)\s+errors?,\s*(\d+)\s+warnings?", stdout)
    errors = [ln for ln in stdout.splitlines() if ln.startswith("ERROR")]
    warns = [ln for ln in stdout.splitlines() if ln.startswith("WARN")]
    return {
        "status": m.group(1) if m else "UNKNOWN",
        "errors": int(m.group(2)) if m else len(errors),
        "warnings": int(m.group(3)) if m else len(warns),
        "error_lines": errors[:50],
        "warning_lines": warns[:50],
    }


def parse_audit(stdout: str) -> dict:
    m = re.search(r"audit:\s*\d+\s+cards,\s*\d+\s+QA entries.*?FAIL\s+(\d+)\s*/\s*WARN\s+(\d+)\s*/\s*INFO\s+(\d+)", stdout)
    warns = [ln.strip() for ln in stdout.splitlines() if "[WARN]" in ln]
    return {
        "fail": int(m.group(1)) if m else None,
        "warn": int(m.group(2)) if m else None,
        "info": int(m.group(3)) if m else None,
        "warning_lines": warns[:50],
    }


def run_all(strict: bool = False, root: Path | None = None) -> dict:
    """跑全部审计，返回 {validate, audit, ok}。strict 时任一 FAIL → ok=False。

    root 仅作用于 validate.py 的 instances 目录；kb_audit CLI 固定审 repo KB
    （自定义 KB_ROOT 属测试场景，audit 结果以 repo KB 为准）。
    """
    root = root or kb_root()
    validate = root / "graph" / "tools" / "validate.py"
    py = sys.executable
    v = _run([py, str(validate), str(root / "graph" / "instances")], cwd=REPO_ROOT)
    a = _run([py, "-m", _AUDIT_MODULE] + (["--strict"] if strict else []), cwd=_AUDIT_CWD)
    result = {
        "validate": {**parse_validate(v["stdout"] + v["stderr"]),
                     "returncode": v["returncode"]},
        "audit": {**parse_audit(a["stdout"] + a["stderr"]),
                  "returncode": a["returncode"]},
    }
    val_fail = result["validate"]["status"] == "FAIL" or result["validate"]["errors"] > 0
    audit_fail = (result["audit"]["fail"] or 0) > 0
    result["ok"] = not (val_fail or audit_fail)
    return result


def main() -> None:
    ap = argparse.ArgumentParser(description="KB 审计聚合（validate + kb_audit）")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true", help="有 FAIL 时 exit 1")
    args = ap.parse_args()

    result = run_all(strict=args.strict)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        v, a = result["validate"], result["audit"]
        print(f"validate: {v['status']} ({v['errors']} errors / {v['warnings']} warnings)")
        print(f"kb_audit: FAIL {a['fail']} / WARN {a['warn']} / INFO {a['info']}")
        for ln in (v["error_lines"] + a["warning_lines"])[:20]:
            print(f"  {ln}")
        print(f"overall: {'OK' if result['ok'] else 'FAIL'}")
    if args.strict and not result["ok"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
