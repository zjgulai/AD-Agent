# AI 跨境地圖診斷 Skill

> 一個 AI 技能包，幫你生成專屬的「跨境出海診斷報告」。
> 由 Vivi（GoAskVivi）建立，內含 22 年跨境電商與 Meta 廣告實戰經驗。

繁體中文 ｜ [简体中文](README.zh-CN.md)

---

## 這是什麼？

把這個技能包裝進你的 AI（Codex、Claude 或任何模型），它就會用一套固定的框架幫你的品牌做健檢，產出一份診斷報告，包含：

| 診斷維度 | 看什麼 |
|---|---|
| 品牌定位 | 品牌名差異化、視覺識別一致性、品牌主張 |
| 官網健康度 | 多幣別、金流、物流、行動體驗、速度 |
| SEO / AEO / GEO | 結構化內容、開門見山、外部引用、圖片 ALT |
| 廣告投放準備度 | Pixel / GA4、素材、受眾、預算測試、落地頁 |
| 私域流量 | 平台覆蓋、會員制度、互動頻率、回購引導 |
| 行動計畫 | 優先級、資源盤點、30 天快速勝利項目 |

報告會給每個維度 0–100 分、現況分析、具體建議，以及一份 30 天行動清單。

**權重會依品牌階段調整**——第一年的品牌看「官網 + 廣告」，第二年以後的品牌看「品牌 + 私域」。詳見 `references/diagnostic-framework.md`。

---

## 如何使用？

### 方法 1：Codex / Claude Code 使用者（推薦）

下載後跑安裝腳本，它會自動偵測你裝的是 Codex 還是 Claude Code：

```bash
git clone https://github.com/vivi911/goaskvivi-dtc-diagnostic-skill.git
cd goaskvivi-dtc-diagnostic-skill
bash install.sh
```

安裝完重開你的 AI 工具，然後直接說：

```
幫我做跨境出海診斷
```

它會反問你品牌資料，然後產出報告。

> 手動安裝也可以：把整個資料夾複製到
> `~/.codex/skills/goaskvivi-dtc-diagnostic/`（Codex）或
> `~/.claude/skills/goaskvivi-dtc-diagnostic/`（Claude Code）。

### 方法 2：ChatGPT / Claude 網頁版使用者

1. 下載這個 repo（右上角 **Code → Download ZIP**）
2. 打開 `references/` 資料夾，把裡面的 `.md` 檔內容複製起來
3. 貼到對話框，跟 AI 說：「請根據這些內容，幫我生成跨境出海診斷報告」

建議至少貼這三個檔案：`diagnostic-framework.md`、對應你品類的 `industry-knowledge/*.md`、對應你市場的 `market-knowledge/*.md`。

### 方法 3：任何 AI 模型（免下載 · 隨身版）

適合國內模型（Kimi、DeepSeek、豆包等網頁/App）：不用下載、不用安裝，複製貼上就能用。

1. 打開倉庫根目錄的 **`PORTABLE.zh-CN.md`（隨身版）**
2. 全選複製，貼進任何 AI 的對話框
3. 填好末尾的四行品牌資料，送出

隨身版由腳本 `build-portable.sh` 從 `references/` 正式內容自動組裝（評分框架 + 大陸市場與法規 + 25 條建議話術），
與完整版同一套知識庫；references 更新後跑一次腳本即可重組，不會脫節。

---

## 檔案結構

```
.
├── SKILL.md                        # Skill 定義與工作流程
├── install.sh                      # 一鍵安裝到 Codex / Claude Code
├── PORTABLE.zh-CN.md               # 隨身版：任何 AI 免安裝，複製貼上即用
├── build-portable.sh               # 從 references/ 一鍵重組隨身版
├── assets/                         # 報告用圖片（微信 QR Code 放這裡）
├── references/                     # 简体中文（大陸受眾預設）
│   ├── diagnostic-framework.md     # 6 大維度評分框架（分階段權重）
│   ├── checklists/                 # 5 個維度的細部檢查清單
│   ├── industry-knowledge/         # 品類知識庫（寵物／美妝／食品）
│   ├── market-knowledge/           # 市場知識庫（台灣／馬來西亞／新加坡／香港／中國大陸）
│   ├── recommendation-templates.md # 25 個常見問題的建議話術
│   ├── tool-integrations.md        # 工具串接定義
│   └── report-template.md          # HTML 報告模板
└── references-zh-tw/               # 繁體中文鏡像（台灣／香港市場）
```

想擴充品類或市場？`industry-knowledge/_template.md` 與 `market-knowledge/_template.md` 是通用模板，照著填就能加新的一份。

---

## 語言版本

- `references/`：简体中文 — 產出簡體報告時讀這套
- `references-zh-tw/`：繁體中文 — 產出繁體報告時讀這套

⚠️ 兩套內容一一對應。**要修改請改简体版 `references/`，再重新轉換繁體版**，避免兩邊不同步。

---

## 這個診斷不會做的事

- 不承諾具體營收數字、ROAS 目標或成長百分比
- 不虛構競品數據、市場規模或客戶見證
- 資料不足時會先反問，不會硬掰

診斷是健檢，不是保證書。它幫你找出「現在最該補的洞」，實際執行還是要靠你自己或找人陪跑。

---

## 想再深入一點？

這份診斷是自助工具，幫你找出「現在最該補的洞」。

其他技能包與後續資源都在 👉 **https://goaskvivi.com/ai-skill-pack/**

---

## 授權

本 Skill 由 Vivi（GoAskVivi）建立，開放個人學習與自用，**不得轉售或作為商業服務內容販售**。
歡迎分享連結，轉載請註明出處。

## 聯絡方式

- 官網：https://goaskvivi.com
- 技能包頁面：https://goaskvivi.com/ai-skill-pack/
