"""KB 加载与检索。

规模 ~400 chunks（qa/ 原子问答 + cards/ 章节切片 + glossary 术语），
内存全量加载，字符 bigram 重合度打分——不引入向量库，零额外依赖。
检索协议见 docs/knowledge/ad-agent-qa/QUERY.md。
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

MAX_CARD_SECTION_CHARS = 1200
MIN_SCORE = 6.0


@dataclass(frozen=True)
class Chunk:
    text: str
    source: str  # 溯源标签，如 "qa/meta-ads-diagnosis.md Q5"
    kind: str  # qa | card | glossary | index


def _bigrams(text: str) -> set[str]:
    t = re.sub(r"[^\w一-鿿]+", "", text.lower())
    if len(t) < 2:
        return {t} if t else set()
    return {t[i : i + 2] for i in range(len(t) - 1)}


_QA_ENTRY = re.compile(r"^###\s+Q\d+\.\s*(.+?)\n\n?\*\*A\*\*：(.+?)(?=\n>\s*溯源：(.+?))?\n", re.S)


def _load_qa_files(kb_root: Path) -> list[Chunk]:
    chunks: list[Chunk] = []
    qa_dir = kb_root / "qa"
    if not qa_dir.is_dir():
        return chunks
    for path in sorted(qa_dir.glob("*.md")):
        if path.name in {"README.md", "COVERAGE.md"}:
            continue
        text = path.read_text(encoding="utf-8")
        for m in re.finditer(r"###\s+(Q\d+\.\s*.+?)\n\*\*A\*\*：\s*(.+?)(?=\n###\s+Q|\Z)", text, re.S):
            q_raw, a_raw = m.group(1).strip(), m.group(2).strip()
            src_m = re.search(r"溯源：`?([^`\n]+)`?", a_raw)
            source = src_m.group(1).strip() if src_m else path.name
            answer = re.sub(r"\n>\s*溯源：.*", "", a_raw, flags=re.S).strip()
            chunks.append(
                Chunk(
                    text=f"Q: {q_raw}\nA: {answer}",
                    source=f"{path.relative_to(kb_root)} {q_raw.split('.')[0]}",
                    kind="qa",
                )
            )
    return chunks


def _split_card_sections(text: str) -> list[tuple[str, str]]:
    """按 ## / ### 标题切片，返回 (标题路径, 内容)。"""
    sections: list[tuple[str, str]] = []
    current_title, buf = "概览", []
    for line in text.splitlines():
        if line.startswith("## "):
            if buf:
                sections.append((current_title, "\n".join(buf)))
            current_title, buf = line[3:].strip(), []
        elif line.startswith("### "):
            if buf:
                sections.append((current_title, "\n".join(buf)))
            current_title, buf = f"{current_title} > {line[4:].strip()}", []
        else:
            buf.append(line)
    if buf:
        sections.append((current_title, "\n".join(buf)))
    return sections


def _load_card_sections(kb_root: Path) -> list[Chunk]:
    chunks: list[Chunk] = []
    cards_dir = kb_root / "cards"
    if not cards_dir.is_dir():
        return chunks
    for path in sorted(cards_dir.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        title_m = re.search(r"^title:\s*(.+)$", text, re.M)
        title = title_m.group(1).strip() if title_m else path.stem
        rel = path.relative_to(kb_root).as_posix()
        for sec_title, body in _split_card_sections(text):
            body = re.sub(r"^---.*?---", "", body, flags=re.S).strip()
            if len(body) < 30:
                continue
            chunk_text = f"{title} / {sec_title}\n{body[:MAX_CARD_SECTION_CHARS]}"
            chunks.append(Chunk(text=chunk_text, source=rel, kind="card"))
    return chunks


def _load_glossary(kb_root: Path) -> list[Chunk]:
    path = kb_root / "glossary.md"
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8")
    chunks: list[Chunk] = []
    for m in re.finditer(r"^\|\s*`?([^|`]+?)`?\s*\|\s*([^|]+)\|\s*([^|]+)\|", text, re.M):
        term, en, desc = (g.strip() for g in m.groups())
        if term in {"术语", "Term", "---"} or set(term) <= {"-", ":"}:
            continue
        chunks.append(
            Chunk(text=f"术语 {term} ({en}): {desc}", source="glossary.md", kind="glossary")
        )
    return chunks


class KnowledgeBase:
    def __init__(self, kb_root: Path) -> None:
        self.kb_root = kb_root
        self.chunks: list[Chunk] = []
        self._reload()

    def _reload(self) -> None:
        self.chunks = (
            _load_qa_files(self.kb_root)
            + _load_card_sections(self.kb_root)
            + _load_glossary(self.kb_root)
        )
        self._index = [_bigrams(c.text) for c in self.chunks]

    def retrieve(self, query: str, top_k: int = 5) -> list[tuple[Chunk, float]]:
        q_bg = _bigrams(query)
        if not q_bg:
            return []
        tokens = [t.lower() for t in re.findall(r"[A-Za-z0-9]+|[一-鿿]+", query) if len(t) >= 2]
        scored: list[tuple[Chunk, float]] = []
        for chunk, c_bg in zip(self.chunks, self._index):
            if not c_bg:
                continue
            lower = chunk.text.lower()
            score = 2.0 * len(q_bg & c_bg) + sum(
                3.0 for t in tokens if t in lower
            )
            if chunk.kind == "qa":
                score *= 1.25
            elif chunk.kind == "glossary":
                score *= 1.1
            if score >= MIN_SCORE:
                scored.append((chunk, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]

    @property
    def stats(self) -> str:
        kinds: dict[str, int] = {}
        for c in self.chunks:
            kinds[c.kind] = kinds.get(c.kind, 0) + 1
        return f"{len(self.chunks)} chunks {kinds} @ {self.kb_root}"
