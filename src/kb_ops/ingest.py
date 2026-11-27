"""摄入管道：上传 → staging/ → 提取 → 蒸馏简报。

写操作只落 staging/（gitignored，不进 KB 源）；蒸馏与发布仍走既有
Agent 批次流程——本模块只生成简报与状态追踪，人审门禁不自动化。

目录约定（staging/ 默认 repo 根，可用 STAGING_DIR 覆盖）：
  staging/inbox/<id>.<ext>        原始上传
  staging/extracted/<id>.md       提取的 Markdown（含 frontmatter）
  staging/extracted/<id>.json     元数据 + 状态机
  staging/briefs/<id>.md          蒸馏简报

状态机：uploaded → extracted → briefed → distilled → published
"""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

from .paths import ensure_src_path, kb_root
from .processors import process_file, supported_ext
from .retrieval import build_index, search_chunks, tokenize

STAGING_DIR = Path(__file__).resolve().parents[2] / "staging"
_ID_RE = re.compile(r"^[a-z0-9一-鿿][a-z0-9一-鿿\-]*$")
_STATUSES = ("uploaded", "extracted", "briefed", "distilled", "published")
_MAX_UPLOAD = 50 * 1024 * 1024  # 50MB


def _staging() -> Path:
    return Path(__import__("os").environ.get("STAGING_DIR", str(STAGING_DIR)))


def _dirs(staging: Path) -> tuple[Path, Path, Path, Path]:
    inbox = staging / "inbox"
    ext_dir = staging / "extracted"
    brief_dir = staging / "briefs"
    for d in (inbox, ext_dir, brief_dir):
        d.mkdir(parents=True, exist_ok=True)
    return inbox, ext_dir, brief_dir, staging


def _slugify(filename: str) -> str:
    stem = Path(filename).stem.lower()
    slug = re.sub(r"[^a-z0-9一-鿿]+", "-", stem).strip("-")
    # 中文 slug 保留（文件名可读性），过长截断
    return (slug or "upload")[:48]


def _item_path(ext_dir: Path, item_id: str) -> Path:
    return ext_dir / f"{item_id}.json"


def _load_item(ext_dir: Path, item_id: str) -> dict:
    if not _ID_RE.fullmatch(item_id):
        raise ValueError("invalid item id")
    p = _item_path(ext_dir, item_id)
    if not p.is_file():
        raise FileNotFoundError(item_id)
    return json.loads(p.read_text(encoding="utf-8"))


def _save_item(ext_dir: Path, item: dict) -> None:
    _item_path(ext_dir, item["id"]).write_text(
        json.dumps(item, ensure_ascii=False, indent=2), encoding="utf-8")


def ingest_bytes(filename: str, data: bytes,
                 staging: Path | None = None) -> dict:
    """保存上传并提取，返回 item dict。staging 默认 STAGING_DIR。"""
    staging = staging or _staging()
    inbox, ext_dir, _, _ = _dirs(staging)
    ext = Path(filename).suffix.lower()
    if not ext or not supported_ext(ext):
        raise ValueError(f"不支持的文件格式: {ext or '(无扩展名)'}")
    if len(data) > _MAX_UPLOAD:
        raise ValueError(f"文件超过 {_MAX_UPLOAD // 1024 // 1024}MB 上限")
    if not data:
        raise ValueError("空文件")

    today = datetime.now().strftime("%Y%m%d")
    base = f"{today}-{_slugify(filename)}"
    item_id, n = base, 2
    while _item_path(ext_dir, item_id).exists():
        item_id = f"{base}-{n}"
        n += 1

    inbox_file = inbox / f"{item_id}{ext}"
    inbox_file.write_bytes(data)

    doc = process_file(inbox_file)
    extracted_md = ext_dir / f"{item_id}.md"
    fm = (
        "---\n"
        f"title: {Path(filename).name}\n"
        f"ingest_id: {item_id}\n"
        f"source_file: staging/inbox/{item_id}{ext}\n"
        f"type: {doc.metadata.get('type', ext.lstrip('.'))}\n"
        f"ingested_at: {datetime.now().isoformat(timespec='seconds')}\n"
        "---\n\n"
    )
    extracted_md.write_text(fm + doc.content, encoding="utf-8")

    item = {
        "id": item_id,
        "filename": Path(filename).name,
        "ext": ext,
        "size_bytes": len(data),
        "uploaded_at": datetime.now().isoformat(timespec="seconds"),
        "status": "extracted",
        "metadata": doc.metadata,
        "errors": doc.errors,
        "content_file": f"extracted/{item_id}.md",
        "content_chars": len(doc.content),
        "tables": len(doc.tables),
    }
    _save_item(ext_dir, item)
    return item


def list_items(staging: Path | None = None) -> list[dict]:
    _, ext_dir, _, _ = _dirs(staging or _staging())
    items = []
    for p in sorted(ext_dir.glob("*.json"), reverse=True):
        try:
            items.append(json.loads(p.read_text(encoding="utf-8")))
        except Exception:
            continue
    return items


def get_item(item_id: str, staging: Path | None = None) -> dict:
    staging = staging or _staging()
    _, ext_dir, _, _ = _dirs(staging)
    item = _load_item(ext_dir, item_id)
    md_path = ext_dir / f"{item_id}.md"
    item["extracted_preview"] = (
        md_path.read_text(encoding="utf-8")[:3000] if md_path.is_file() else "")
    item["has_brief"] = (staging / "briefs" / f"{item_id}.md").is_file()
    return item


def get_content(item_id: str, staging: Path | None = None) -> str:
    _, ext_dir, _, _ = _dirs(staging or _staging())
    _load_item(ext_dir, item_id)  # 校验存在
    md_path = ext_dir / f"{item_id}.md"
    if not md_path.is_file():
        raise FileNotFoundError(item_id)
    return md_path.read_text(encoding="utf-8")


def set_status(item_id: str, status: str,
               staging: Path | None = None) -> dict:
    if status not in _STATUSES:
        raise ValueError(f"非法状态: {status}（允许: {'/'.join(_STATUSES)}）")
    staging = staging or _staging()
    _, ext_dir, _, _ = _dirs(staging)
    item = _load_item(ext_dir, item_id)
    item["status"] = status
    item["status_updated_at"] = datetime.now().isoformat(timespec="seconds")
    _save_item(ext_dir, item)
    return item


def _related_hits(text: str, top_k: int = 6) -> list[dict]:
    """用提取内容的高频 token 查 KB BM25，辅助蒸馏定位相关卡片/QA。"""
    ensure_src_path()
    try:
        from kb_bot.kb import KnowledgeBase
        tokens = [t for t in dict.fromkeys(tokenize(text[:8000]))
                  if len(t) >= 3][:30]
        if not tokens:
            return []
        kb = KnowledgeBase(kb_root())
        hits = search_chunks(kb, build_index(kb), " ".join(tokens), top_k)
        return [{"source": ch.source, "kind": ch.kind, "score": s}
                for ch, s in hits]
    except Exception:
        return []


def generate_brief(item_id: str, staging: Path | None = None) -> str:
    """生成蒸馏简报 markdown，状态 → briefed。返回简报文本。"""
    staging = staging or _staging()
    _, ext_dir, brief_dir, _ = _dirs(staging)
    item = _load_item(ext_dir, item_id)
    content = get_content(item_id, staging)
    hits = _related_hits(content)

    meta = item.get("metadata", {})
    slug = re.sub(r"[^a-z0-9\-]+", "-", Path(item["filename"]).stem.lower())[:40] or "source"

    hit_lines = "\n".join(
        f"- `{h['source']}`（{h['kind']}，score {h['score']}）" for h in hits) or "- （无明显相关既有内容）"

    brief = f"""# 蒸馏简报 — {item['filename']}

> 由 kb_ops.ingest 自动生成（{datetime.now().isoformat(timespec='seconds')}）。
> 用途：作为 Agent 蒸馏批次（S/G 批同格式）的输入简报；蒸馏与发布仍走既有批次流程。

## 源信息

| 项 | 值 |
|----|-----|
| 文件 | `{item['filename']}` |
| 类型 | {item['ext']}（提取类型 {meta.get('type', '?')}） |
| 大小 | {item['size_bytes'] / 1024:.1f} KB |
| 提取字符 | {item['content_chars']} |
| 表格数 | {item.get('tables', 0)} |
| 摄入时间 | {item['uploaded_at']} |
| 状态 | {item['status']} |

### 提取元数据

```json
{json.dumps(meta, ensure_ascii=False, indent=2)}
```

### 提取错误/警告

{chr(10).join('- ' + e for e in item.get('errors', [])) or '无'}

## 提取内容预览（前 2000 字）

```
{content[:2000]}
```

## 与既有 KB 的相关度（BM25 反查 top{len(hits)}）

{hit_lines}

## 建议蒸馏范围（待人工/Agent 确认）

- **raw 归档**：`raw/sXX-{slug}/`（下一个批次编号待定）
- **卡片候选集群**：按上方命中 chunk 的 source 路径聚类（cards/<cluster>/）
- **QA 归属**：对应集群 qa/<cluster>.md 追加 Q 编号
- **图谱分片**：新增 `graph/instances/sXX-{slug}.nodes.json/.edges.json`，节点须过 `validate.py` schema
- **SOURCES.md**：登记源表行（编号 + URL/文件名 + license + 处理方式）

## 批次执行清单（对齐现有 S/G 批格式）

1. 通读 `staging/extracted/{item_id}.md` 全文（勿只看预览）
2. 界定蒸馏范围：选定卡片集群 + QA 文件 + 图谱节点类型（ad:* schema）
3. 写卡：frontmatter `source_docs: [SXX:<file>]` 或 `CBE:<skill>` 约定
4. 写 QA：原子问答，`> 溯源：` 必填
5. 图谱：节点带 `src` provenance，边带 `ref`；validate.py PASS 0/0
6. `kb_audit --strict` FAIL 0；`pytest tests/` 全绿
7. 更新 SOURCES.md / INDEX.md / REVIEW-PRECHECK.md（kb_audit 自动重生成）
8. 提交推送后回工作台把状态推进到 distilled → published
"""
    out = brief_dir / f"{item_id}.md"
    out.write_text(brief, encoding="utf-8")
    item["status"] = "briefed"
    item["brief_file"] = f"briefs/{item_id}.md"
    item["briefed_at"] = datetime.now().isoformat(timespec="seconds")
    _save_item(ext_dir, item)
    return brief


def get_brief(item_id: str, staging: Path | None = None) -> str:
    staging = staging or _staging()
    _, ext_dir, brief_dir, _ = _dirs(staging)
    _load_item(ext_dir, item_id)
    p = brief_dir / f"{item_id}.md"
    if not p.is_file():
        raise FileNotFoundError(item_id)
    return p.read_text(encoding="utf-8")
