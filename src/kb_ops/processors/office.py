"""Office 文档提取：PDF / DOCX / XLSX / PPTX → Markdown。"""

from __future__ import annotations

from pathlib import Path

from . import ProcessedDoc, finalize, _MAX_TABLE_ROWS


def _dep_error(name: str, pkg: str) -> ProcessedDoc:
    return ProcessedDoc(errors=[f"缺少依赖: {name}。请运行: pip install {pkg}"])


def _pdf(path: Path) -> ProcessedDoc:
    try:
        from pypdf import PdfReader
    except ImportError:
        return _dep_error("pypdf", "pypdf")
    reader = PdfReader(str(path))
    meta = {"source": str(path), "type": "pdf", "pages": len(reader.pages)}
    if reader.metadata:
        for k, mk in (("title", "/Title"), ("author", "/Author"), ("creator", "/Creator")):
            v = reader.metadata.get(mk)
            if v:
                meta[k] = str(v)
    if reader.is_encrypted:
        try:
            reader.decrypt("")
        except Exception:
            return ProcessedDoc(metadata=meta, errors=["PDF 已加密，空密码解密失败"])
    parts, errors = [], []
    for i, page in enumerate(reader.pages):
        try:
            t = page.extract_text() or ""
        except Exception as e:
            errors.append(f"第{i + 1}页提取失败: {e}")
            continue
        if t.strip():
            parts.append(f"\n\n--- 第 {i + 1} 页 ---\n\n{t}")
    return ProcessedDoc("\n".join(parts), meta, errors=errors)


def _rows_to_md(rows: list[list[str]]) -> str:
    rows = [r for r in rows if any(c.strip() for c in r)]
    if not rows:
        return ""
    width = max(len(r) for r in rows)
    lines = []
    for i, r in enumerate(rows):
        r = (r + [""] * width)[:width]
        lines.append("| " + " | ".join(c.strip().replace("|", "\\|") for c in r) + " |")
        if i == 0:
            lines.append("|" + "|".join(["---"] * width) + "|")
    return "\n".join(lines)


def _docx(path: Path) -> ProcessedDoc:
    try:
        from docx import Document
    except ImportError:
        return _dep_error("python-docx", "python-docx")
    doc = Document(str(path))
    cp = doc.core_properties
    meta = {"source": str(path), "type": "docx",
            "title": cp.title or "", "author": cp.author or ""}
    parts = [p.text for p in doc.paragraphs if p.text.strip()]
    tables = []
    for i, table in enumerate(doc.tables):
        rows = [[cell.text.strip() for cell in row.cells] for row in table.rows]
        md = _rows_to_md(rows)
        if md:
            tables.append(f"\n### 表格 {i + 1}\n{md}")
    return ProcessedDoc("\n\n".join(parts) + "".join(tables), meta, tables=tables)


def _xlsx(path: Path) -> ProcessedDoc:
    try:
        import openpyxl
    except ImportError:
        return _dep_error("openpyxl", "openpyxl")
    wb = openpyxl.load_workbook(str(path), data_only=True, read_only=True)
    meta = {"source": str(path), "type": "xlsx",
            "sheets": len(wb.sheetnames), "sheet_names": wb.sheetnames}
    parts, tables, errors = [], [], []
    for name in wb.sheetnames:
        ws = wb[name]
        rows = []
        for row in ws.iter_rows(max_row=_MAX_TABLE_ROWS, values_only=True):
            vals = ["" if v is None else str(v).strip() for v in row]
            if any(vals):
                rows.append(vals)
        md = _rows_to_md(rows)
        if md:
            section = f"\n\n## 工作表: {name}\n\n{md}"
            parts.append(section)
            tables.append(section)
        total = ws.max_row or 0
        if total > _MAX_TABLE_ROWS:
            errors.append(f"工作表 {name} 共 {total} 行，仅提取前 {_MAX_TABLE_ROWS} 行")
    wb.close()
    return ProcessedDoc("".join(parts), meta, tables=tables, errors=errors)


def _pptx(path: Path) -> ProcessedDoc:
    try:
        from pptx import Presentation
    except ImportError:
        return _dep_error("python-pptx", "python-pptx")
    prs = Presentation(str(path))
    meta = {"source": str(path), "type": "pptx", "slides": len(prs.slides)}
    parts = []
    for i, slide in enumerate(prs.slides, 1):
        texts = []
        for shape in slide.shapes:
            if shape.has_text_frame:
                t = shape.text_frame.text.strip()
                if t:
                    texts.append(t)
            if getattr(shape, "has_table", False) and shape.has_table:
                rows = [[c.text.strip() for c in r.cells] for r in shape.table.rows]
                md = _rows_to_md(rows)
                if md:
                    texts.append(md)
        if texts:
            parts.append(f"\n\n## 幻灯片 {i}\n\n" + "\n".join(texts))
    return ProcessedDoc("".join(parts), meta)


def extract(path: Path, ext: str) -> ProcessedDoc:
    fn = {".pdf": _pdf, ".docx": _docx, ".xlsx": _xlsx, ".pptx": _pptx}.get(ext)
    if not fn:
        return ProcessedDoc(errors=[f"不支持的格式: {ext}"])
    return finalize(fn(path))
