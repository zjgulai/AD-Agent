"""HTML 提取：stdlib HTMLParser，正文文本 + 表格→Markdown。"""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path

from . import ProcessedDoc, finalize

_SKIP = {"script", "style", "noscript", "svg"}


class _Extractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.parts: list[str] = []
        self.tables: list[list[list[str]]] = []   # table → rows → cells
        self._skip = 0
        self._in_title = False
        self._in_table = False
        self._cur_rows: list[list[str]] = []
        self._row: list[str] | None = None
        self._cell: list[str] | None = None
        self._buf: list[str] = []

    def _flush_text(self):
        t = " ".join("".join(self._buf).split())
        self._buf = []
        if t:
            self.parts.append(t)

    def handle_starttag(self, tag, attrs):
        if tag in _SKIP:
            self._skip += 1
            return
        if self._skip:
            return
        if tag == "title":
            self._in_title = True
        elif self._in_table:
            if tag == "tr":
                self._row = []
            elif tag in {"td", "th"}:
                self._cell = []
        elif tag == "table":
            self._flush_text()
            self._in_table = True
            self._cur_rows = []
        elif tag in {"p", "div", "section", "article", "br", "li",
                     "h1", "h2", "h3", "h4", "blockquote", "pre"}:
            self._flush_text()

    def handle_endtag(self, tag):
        if tag in _SKIP and self._skip:
            self._skip -= 1
            return
        if self._skip:
            return
        if tag == "title":
            self._in_title = False
        elif self._in_table:
            if tag in {"td", "th"} and self._cell is not None and self._row is not None:
                self._row.append(" ".join("".join(self._cell).split()))
                self._cell = None
            elif tag == "tr" and self._row is not None:
                if any(c.strip() for c in self._row):
                    self._cur_rows.append(self._row)
                self._row = None
            elif tag == "table":
                if self._cur_rows:
                    self.tables.append(self._cur_rows)
                self._in_table = False
                self._cur_rows, self._row, self._cell = [], None, None
        elif tag in {"p", "div", "section", "article", "li",
                     "h1", "h2", "h3", "h4", "blockquote", "pre"}:
            self._flush_text()

    def handle_data(self, data):
        if self._skip:
            return
        if self._in_title:
            self.title += data
        elif self._cell is not None:
            self._cell.append(data)
        elif not self._in_table:
            self._buf.append(data)


def _table_md(rows: list[list[str]]) -> str:
    width = max(len(r) for r in rows)
    lines = []
    for i, r in enumerate(rows):
        r = (r + [""] * width)[:width]
        lines.append("| " + " | ".join(c.replace("|", "\\|") for c in r) + " |")
        if i == 0:
            lines.append("|" + "|".join(["---"] * width) + "|")
    return "\n".join(lines)


def extract(path: Path) -> ProcessedDoc:
    raw = path.read_bytes()
    html = None
    for enc in ("utf-8", "gb18030"):
        try:
            html = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    if html is None:
        html = raw.decode("utf-8", errors="replace")
    p = _Extractor()
    p.feed(html)
    p._flush_text()
    body = "\n\n".join(p.parts)
    tables_md = [f"### 表格 {i + 1}\n{_table_md(t)}"
                 for i, t in enumerate(p.tables, 1)]
    tables_block = ("\n\n" + "\n\n".join(tables_md)) if tables_md else ""
    content = body + tables_block
    return finalize(ProcessedDoc(
        content=content,
        metadata={"source": str(path), "type": "html",
                  "title": p.title.strip(), "chars": len(content),
                  "tables": len(p.tables)},
        tables=tables_md,
    ))
