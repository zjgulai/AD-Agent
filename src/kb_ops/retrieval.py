"""BM25 检索：中英文混合分词 + Okapi BM25。

Vendored from YesIamGodt/knowledge-pipline `core/retrieval.py` (MIT License)，
适配 ad-agent-qa 的 Chunk 模型（复用 kb_bot.kb 的分块加载，只换打分器）。

CLI：python -m kb_ops.retrieval "查询词" [-k 5]
"""

from __future__ import annotations

import math
import re
import sys
from collections import Counter
from pathlib import Path

# Vendored 分词与停用词（源：knowledge-pipline core/retrieval.py, MIT）
_CN_STOPWORDS = set(
    "的了和是在有这那我你他她它们与或但而也都就很太最更还再又才已"
    "已经正在将要会能可以应该必须需要这个那个这些那些什么怎么为什么哪里"
    "因为所以如果虽然但是而且或者还是之一方面部分整体全部一些一点"
    "进行实施开展推进落实执行完成实现新最新最近现在今天明天昨天时候时间"
    "推出发布宣布表示说认为指出说明解释就是从到等"
)

_EN_STOPWORDS = set(
    "the a an and or but in on at for with is are was were be been being to of by "
    "from up down over under again further then once here there when where why how "
    "all any both each few more most other some such no nor not only own same so "
    "than too very do does did has have had its this that these those".split()
)


def tokenize(text: str) -> list[str]:
    """中英文混合分词：英文按词边界，中文按 bigram 切分。"""
    tokens: list[str] = []
    text_lower = text.lower()

    en_words = re.findall(r"\b[a-z][a-z0-9\-]{1,30}\b", text_lower)
    for w in en_words:
        if w not in _EN_STOPWORDS:
            tokens.append(w)

    cn_seqs = re.findall(r"[\u4e00-\u9fff]+", text_lower)
    for seq in cn_seqs:
        if 2 <= len(seq) <= 6 and seq not in _CN_STOPWORDS:
            tokens.append(seq)
        if len(seq) >= 2:
            for i in range(len(seq) - 1):
                bg = seq[i : i + 2]
                if bg not in _CN_STOPWORDS:
                    tokens.append(bg)

    mixed = re.findall(r"[a-zA-Z][a-zA-Z0-9\-]*\d+[a-zA-Z0-9]*|[A-Z]{2,}", text)
    for m in mixed:
        tokens.append(m.lower())

    return tokens


class BM25Index:
    """Okapi BM25 检索索引（k1=1.5, b=0.75）。"""

    def __init__(self, k1: float = 1.5, b: float = 0.75) -> None:
        self.k1 = k1
        self.b = b
        self.doc_tokens: dict[str, list[str]] = {}
        self.doc_len: dict[str, int] = {}
        self.avgdl: float = 0.0
        self._df: Counter = Counter()
        self._n: int = 0
        self._dirty = True

    def add(self, doc_id: str, content: str) -> None:
        tokens = tokenize(content)
        self.doc_tokens[doc_id] = tokens
        self.doc_len[doc_id] = len(tokens)
        for t in set(tokens):
            self._df[t] += 1
        self._n += 1
        self._dirty = True

    def _recompute(self) -> None:
        if not self._dirty:
            return
        self.avgdl = sum(self.doc_len.values()) / max(self._n, 1)
        self._dirty = False

    def _idf(self, term: str) -> float:
        df = self._df.get(term, 0)
        return math.log((self._n - df + 0.5) / (df + 0.5) + 1.0)

    def search(self, query: str, top_k: int = 10) -> list[tuple[str, float]]:
        self._recompute()
        query_tokens = tokenize(query)
        if not query_tokens:
            return []
        scores: dict[str, float] = {}
        for doc_id, doc_toks in self.doc_tokens.items():
            tf_counter = Counter(doc_toks)
            dl = self.doc_len[doc_id]
            score = 0.0
            for qt in query_tokens:
                tf = tf_counter.get(qt, 0)
                if tf == 0:
                    continue
                idf = self._idf(qt)
                numerator = tf * (self.k1 + 1)
                denominator = tf + self.k1 * (1 - self.b + self.b * dl / max(self.avgdl, 1))
                score += idf * numerator / denominator
            if score > 0:
                scores[doc_id] = score
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]


def build_index(kb) -> BM25Index:
    """为 KnowledgeBase 建 BM25 索引（doc_id = chunk 下标）。"""
    index = BM25Index()
    for i, chunk in enumerate(kb.chunks):
        index.add(str(i), chunk.text)
    return index


def search_chunks(kb, index: BM25Index, query: str, top_k: int = 5):
    """对已建索引检索，返回 [(Chunk, score)]（含 kind 权重，与 retrieve 同族口径）。"""
    hits = index.search(query, top_k=top_k * 2)  # 多取再按 kind 微调
    out: list[tuple[object, float]] = []
    for doc_id, score in hits:
        chunk = kb.chunks[int(doc_id)]
        if chunk.kind == "qa":
            score *= 1.25
        elif chunk.kind == "glossary":
            score *= 1.1
        out.append((chunk, round(score, 3)))
    out.sort(key=lambda x: x[1], reverse=True)
    return out[:top_k]


def search_kb(kb_root: Path, query: str, top_k: int = 5):
    """对 ad-agent-qa KB 做 BM25 检索，返回 [(Chunk, score)]。

    分块加载复用 kb_bot.kb（qa/card/glossary 三类 chunk），只替换打分器。
    """
    from .paths import ensure_src_path
    ensure_src_path()
    from kb_bot.kb import KnowledgeBase

    kb = KnowledgeBase(kb_root)
    return search_chunks(kb, build_index(kb), query, top_k)


def main() -> None:
    import argparse

    from .paths import kb_root

    ap = argparse.ArgumentParser(description="BM25 检索 ad-agent-qa KB")
    ap.add_argument("query")
    ap.add_argument("-k", "--top-k", type=int, default=5)
    args = ap.parse_args()
    for chunk, score in search_kb(kb_root(), args.query, args.top_k):
        print(f"[{score:7.2f}] {chunk.source} ({chunk.kind})")
        print(f"    {chunk.text[:120].replace(chr(10), ' ')}")


if __name__ == "__main__":
    main()
