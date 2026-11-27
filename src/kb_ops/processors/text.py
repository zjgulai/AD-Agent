"""纯文本 / Markdown / CSV 提取。"""

from __future__ import annotations

import csv
import io
from pathlib import Path

from . import ProcessedDoc, finalize

_ENCODINGS = ("utf-8-sig", "utf-8", "gb18030")  # 中文 Windows 导出常见 gbk 系


def _read_text(path: Path) -> str:
    raw = path.read_bytes()
    for enc in _ENCODINGS:
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def _csv_to_markdown(text: str) -> str:
    rows = list(csv.reader(io.StringIO(text)))
    rows = [r for r in rows if any(c.strip() for c in r)]
    if not rows:
        return ""
    width = max(len(r) for r in rows)
    lines = []
    for i, r in enumerate(rows):
        r = r + [""] * (width - len(r))
        lines.append("| " + " | ".join(c.strip().replace("|", "\\|") for c in r) + " |")
        if i == 0:
            lines.append("|" + "|".join(["---"] * width) + "|")
    return "\n".join(lines)


def extract(path: Path) -> ProcessedDoc:
    text = _read_text(path)
    ext = path.suffix.lower()
    content = _csv_to_markdown(text) if ext == ".csv" else text
    return finalize(ProcessedDoc(
        content=content,
        metadata={"source": str(path), "type": ext.lstrip("."),
                  "chars": len(content)},
    ))
