"""图片提取：P2 暂不做 OCR（paddleocr 依赖重），返回元数据 + 人工处理提示。"""

from __future__ import annotations

from pathlib import Path

from . import ProcessedDoc


def extract(path: Path) -> ProcessedDoc:
    size = path.stat().st_size
    return ProcessedDoc(
        content="",
        metadata={"source": str(path), "type": path.suffix.lstrip("."),
                  "bytes": size},
        errors=["图片内容需 OCR 提取，paddleocr 未启用（可选依赖）；"
                "请人工转录图片中的文字/数据后再走蒸馏"],
    )
