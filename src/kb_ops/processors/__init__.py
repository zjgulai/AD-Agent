"""多格式文件提取器：process_file(path) -> ProcessedDoc。

自研实现（不用 knowledge-pipline processors 原文——其 pdf/xlsx 处理器存在
\\n 双重转义与类重复定义缺陷）。依赖按需导入，缺依赖时返回 errors 而非崩溃。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ProcessedDoc:
    content: str = ""                # 提取的 Markdown 文本
    metadata: dict = field(default_factory=dict)
    tables: list = field(default_factory=list)
    errors: list = field(default_factory=list)


_SUPPORTED = {
    ".txt", ".md", ".markdown", ".csv",
    ".pdf", ".docx", ".xlsx", ".pptx",
    ".html", ".htm",
    ".png", ".jpg", ".jpeg", ".webp", ".gif",
}

_MAX_TABLE_ROWS = 500   # xlsx 单表截断保护
_MAX_CONTENT_CHARS = 2_000_000


def supported_ext(ext: str) -> bool:
    return ext.lower() in _SUPPORTED


def process_file(path: str | Path) -> ProcessedDoc:
    path = Path(path)
    ext = path.suffix.lower()
    try:
        if ext in {".txt", ".md", ".markdown", ".csv"}:
            from . import text
            return text.extract(path)
        if ext in {".pdf", ".docx", ".xlsx", ".pptx"}:
            from . import office
            return office.extract(path, ext)
        if ext in {".html", ".htm"}:
            from . import web
            return web.extract(path)
        if ext in {".png", ".jpg", ".jpeg", ".webp", ".gif"}:
            from . import image
            return image.extract(path)
        return ProcessedDoc(errors=[f"不支持的格式: {ext}"])
    except Exception as e:  # 处理器自身异常兜底
        return ProcessedDoc(errors=[f"提取异常: {e}"])


def finalize(doc: ProcessedDoc) -> ProcessedDoc:
    """统一收口：截断超长内容、补齐 metadata.type。"""
    if len(doc.content) > _MAX_CONTENT_CHARS:
        doc.content = doc.content[:_MAX_CONTENT_CHARS] + "\n\n…[内容过长已截断]"
        doc.errors.append(f"内容超过 {_MAX_CONTENT_CHARS} 字符，已截断")
    return doc
