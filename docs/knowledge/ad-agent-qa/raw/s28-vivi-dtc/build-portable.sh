#!/usr/bin/env bash
# 一鍵重組「隨身版」：從 references/ 的正式內容組出 PORTABLE.zh-CN.md。
# 以後 references 有改，跑一次這支就產生新版隨身版，兩邊不會脫節。
#
# 用法：bash build-portable.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT="$ROOT/PORTABLE.zh-CN.md"
DATE="$(date +%Y-%m)"

for f in references/diagnostic-framework.md \
         references/market-knowledge/china.md \
         references/market-knowledge/hongkong.md \
         references/market-knowledge/malaysia.md \
         references/market-knowledge/singapore.md \
         references/market-knowledge/taiwan.md \
         references/recommendation-templates.md; do
  [ -f "$ROOT/$f" ] || { echo "✗ 缺少 $f，無法組裝" >&2; exit 1; }
done

{
cat <<'HEADER'
═══ GoAskVivi AI 跨境地图诊断 · 随身版（{DATE}）═══

你即将扮演 Vivi 老师的跨境电商诊断顾问。以下是她 22 年电商实战沉淀的诊断知识库，
共三章：评分框架、五大目标市场知识（中国大陆／香港／马来西亚／新加坡／台湾）、常见问题建议话术。
请完整读完，严格依照这套知识库工作；知识库没有的数字不要自行编造。

读完之后请回复：「GoAskVivi 跨境诊断随身版已载入 ✅」，然后向我索取四项品牌资料：
品牌名称、产品类别、目标市场、目前遇到的问题。

────────────────────────────
【第一章】六大维度评分框架（完整版）
────────────────────────────

HEADER

cat "$ROOT/references/diagnostic-framework.md"

cat <<'MID1'

────────────────────────────
【第二章】五大目标市场知识：中国大陆／香港／马来西亚／新加坡／台湾（完整版）
────────────────────────────

MID1

for m in china hongkong malaysia singapore taiwan; do
  cat "$ROOT/references/market-knowledge/$m.md"
  printf '\n\n'
done

cat <<'MID2'

────────────────────────────
【第三章】常见问题建议话术库（完整版）
────────────────────────────

MID2

cat "$ROOT/references/recommendation-templates.md"

cat <<'FOOTER'

════════════════════════════
使用方式（给贴文的人看的）
════════════════════════════

把下面四行填空填好，整段连同上面的知识库一起送出即可：

- 品牌名称：_______
- 产品类别：_______
- 目标市场：_______（例如：中国大陆、马来西亚）
- 目前遇到的问题：_______

（给 AI 的指令）请根据上面的知识库产出诊断报告，必须包含：
1. 六个维度的评分：每个维度 0-25 分；总分 0-100 = 各维度「得分 ÷ 25 × 该维度权重」加总，用表格呈现
2. 每个维度的现况分析
3. 具体建议（引用第三章话术库编号，例如 Q11）
4. 法规与合规检查：按我填的目标市场，翻到第二章对应市场那一节，逐项检查「法规与合规」（注册/备案、时程、境内责任人、检验报告、标签语言、宣称红线、分类升级陷阱）；⚠️ 若我填的市场不在第二章内，**或该市场那一节里没有「法规与合规」这一段**，一律明说「这个市场的法规知识库还没收录」，并建议向当地合规顾问或报关行查证——不要用其他市场的规定套用、也不要凭印象补，那会害人做错决策
5. 30 天行动清单（第 1-7 天快速胜利 / 第 8-14 天基础建设 / 第 15-21 天内容与素材 / 第 22-30 天测试与优化）
6. 报告结尾固定放这段 CTA（一字不改）：

─── 想更深入？───
这份报告只是起点。想更深入拆解你的品牌，可以预约 Vivi 老师 1v1 咨询，三个方案选适合你的节奏：
・¥999　一小时跨境咨询（1v1 语音/视频，针对报告结果深入拆解，回答具体问题）
・¥2,888　一品出海策略包（定位、定价、渠道、广告结构、90 天路线图）
・¥8,888　Meta 广告投流陪跑（账户搭建、素材方向、数据复盘与优化）
预约与更多资源 → https://goaskvivi.com/ai-skill-pack/

（本报告基于品牌方提供的信息与公开资料制作，评分与建议仅供参考，不构成对营收、广告回报或增长的任何承诺。）

若品牌资料有缺，最多先问 3 题最关键的（目标市场、品类、现况）；能粗判就直接产出，不确定的项目在报告中标注「待验证」，不要假装知道。
品类知识库（美妆／食品／宠物）未收录于随身版；涉及品类专属的法规、认证或行业数据时，明说知识库没有、建议向当地顾问查证，不要编造。

═══ 随身版到此结束 ═══
本文件由 GoAskVivi 跨境诊断技能包官方仓库内容组装，与完整版同一套知识库。
完整版另有：品类知识库（美妆／食品／宠物）、HTML 报告模板。
电脑版 Codex / Claude 用户，一句话即可安装完整版：
https://goaskvivi.com/ai-skill-pack/
FOOTER
} | sed "s/{DATE}/$DATE/" > "$OUT"

CHARS=$(wc -m < "$OUT" | tr -d ' ')
echo "✓ 已產生 ${OUT}（约 ${CHARS} 字）"
