---
title: 知识库增量更新 SOP
doc_type: knowledge
module: ad-agent-qa
topic: updating-sop
status: stable
created: 2026-11-26
updated: 2026-11-26
owner: self
source: human+ai
---

# 知识库增量更新 SOP

> 新增飞书源 → raw 快照 → 登记 SOURCES → 蒸馏卡片 → 更新 INDEX/glossary 的完整操作流。本文件沉淀 4 批采集（S1–S16）趟出的所有可复用配方。

## 1. 总流程

```
新源 URL/文件夹
  → 判断源类型（wiki/docx/sheet/bitable/file/画板）
  → 按类型走对应采集路径 → raw/ 落快照
  → SOURCES.md 登记（ID 续编 S17+）
  → 若为容器型文档：追踪 cite 引用与内嵌资源，能抓则抓、无权限则标 [待确认]
  → 内容预览 → 定卡片规划（归入既有集群 or 新建集群）
  → 蒸馏写卡（schema 见下）
  → INDEX.md 加行 + 速查；glossary.md 补新术语
  → 链接校验（python 遍历 .md 相对链接）
```

## 2. 源类型 → 采集命令速查（lark-cli v1.0.99）

| 源类型 | 命令 | 产出 |
|--------|------|------|
| wiki / docx 文档 | `lark-cli docs +fetch --doc <url> --doc-format markdown --detail simple` | JSON，取 `data.document.content` 字段落盘 `.md` |
| drive 文件夹列举 | `lark-cli drive files list --folder-token <t>` | JSON 文件清单（含子文件夹） |
| HTML/附件下载 | `lark-cli drive +download --file-token <t> --output <path>` | 二进制原件 |
| sheet 导出 | `lark-cli drive +export --url <sheet-url> --doc-type sheet --file-extension xlsx` → `drive +export-download` | xlsx |
| bitable | `lark-cli base +record-list`（S3 配方） | NDJSON |
| 画板/白板 | `lark-cli docs +media-download` → 渲染 PNG | PNG + OCR |
| 文档内嵌资源 | `lark-cli docs +media-preview` | 附件批量下载 |

**注意**：`docs +fetch` 的正确 flag 是 `--doc` 不是 `--url`；输出是 JSON 包装，正文在 `data.document.content`（含 `\n` 转义，需 python 提取）。

## 3. 已知坑与对策

### 3.1 sheets scope 缺失（高频坑）

`docs +fetch` / sheets API 报 `missing_scope: sheets:spreadsheet:read` 时，**不要走浏览器剪贴板**（S4/S7 的笨办法），改用：

```bash
lark-cli drive +export --url "https://momcozy-in.feishu.cn/sheets/<token>" \
  --doc-type sheet --file-extension xlsx
# 返回 file_token 后 export-download 到允许目录（cwd/tmp/~/files 白名单），再 mv 到 raw/
```

drive scope 与 sheets scope 独立，export 通常可用。xlsx → TSV 用 openpyxl（已装 3.1.5）。

### 3.2 容器型文档（cite 壳）

S12/S13/S14/S15 都是「壳文档」——正文在 `<cite doc-id="..." file-type="wiki|docx">` 引用、`<sheet token="...">` 内嵌表、图片附件 URL（feishu.cn/file/ 域名）截图里。处理流程：

1. 提取全部 cite token → 拼 URL 尝试 `docs +fetch`（wiki 用 `/wiki/`、docx 用 `/docx/`）
2. `<sheet>` token → 按 3.1 导出 xlsx
3. 截图只取 alt 文本进卡片，标注 `[待确认]`（图片未逐张下载）
4. 无权限文档（error 3380004）→ SOURCES.md 记缺口，卡片框架照写

### 3.3 画板/图片 OCR 双引擎

渲染 PNG 后**必须双引擎**：

```bash
# Vision OCR（macOS，中文好英文粘连）— 上一批用的脚本产物在 raw/*-ocr.txt
# Tesseract（英文节点名好中文破碎）
tesseract <img>.png stdout -l chi_sim+eng --psm 11 > <img>-tesseract.txt
```

两引擎一致处去 `[待确认]`，冲突处保留。S1 复核实证：单引擎会漏 Loop、错置节点归属。

### 3.4 无权限文档

`docs +fetch` 返回 `code 3380004` = 用户无查看权限。处理：SOURCES.md 记「无权限缺口」，卡片写容器框架 + `[待确认]`，不臆造内容。用户授权后增量补抓。

## 4. 卡片 schema（与既有 17 卡一致）

```yaml
---
title: 卡片标题
doc_type: knowledge
module: ad-agent-qa
topic: kebab-topic
status: review          # 验收后改 stable
created/updated: YYYY-MM-DD
owner: self
source: human+ai
source_docs: [S12, S13b]  # 可含派生源（引用文档单独编号）
fetched_at: YYYY-MM-DD
---
```

正文固定四段：**核心问题 → 系统解答 → 高频问答索引 → 相关卡片**。标注规范：`[推断]`=合理推断、`[待确认]`=源文档矛盾/缺失/OCR 存疑。

## 5. 集群路由（当前 5 个）

| 集群 | 收什么 |
|------|--------|
| `architecture/` | Momcozy 内部系统架构、产品方案、调研方法论 |
| `influencer-boost/` | 红人素材加推 Loop（S2/S3） |
| `meta-ads-diagnosis/` | Meta 投放诊断/巡检/SOP（S4/S6/S7/S8） |
| `fundamentals/` | 行业通用广告机制与策略（S9/S10/S11） |
| `competitor-analysis/` | 竞品调研（S12–S15） |

新源先判断「内部项目 / 行业通用 / 竞品」三类再归集群；跨类主题优先归主要类，`source_docs` 保留全部溯源。

## 6. 验证清单（每批必跑）

- [ ] `raw/` 快照齐全（含派生源）
- [ ] SOURCES.md 新行 + 批次注记（提取方式/权限缺口/口径差异）
- [ ] 新卡 frontmatter 六字段齐全
- [ ] INDEX.md 卡片行 + 速查行更新
- [ ] glossary.md 新术语（中英对照+出处）
- [ ] 链接校验 0 断链：

```bash
cd docs/knowledge/ad-agent-qa && python3 -c "
import re, os
broken=[]
for root,_,files in os.walk('.'):
    for f in files:
        if f.endswith('.md'):
            p=os.path.join(root,f)
            for m in re.finditer(r'\]\(([^)#\s]+\.md)', open(p).read()):
                if not os.path.exists(os.path.normpath(os.path.join(root,m.group(1)))):
                    broken.append((p,m.group(1)))
print('broken:',len(broken), broken[:10])
"
```

## 7. 当前待办缺口（2026-11-26 快照）

- 5 篇无权限文档（S14/S15 引用）：3 会议纪要 + 2 wiki，授权后补抓
- S1 画板 `[待确认]` 残留：Loop 2 独立节点、Creative Matching 职责、飞轮英文名对应等——需原图人工终核
- S16 业务细化调研表为空模板，等业务填数据后重跑
- 全部 17 卡 `status: review`，待人工验收后批量转 `stable`
- 跨源矛盾 17 项登记于 [CONFLICTS.md](CONFLICTS.md)，待业务裁决
