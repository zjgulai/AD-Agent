# references（簡體中文版）

這個目錄是診斷知識庫的**主檔**，報告預設讀這一套。

- 繁體版映象在 `../references-zh-tw/`，內容一一對應、檔案結構一致。
- 繁體版由 OpenCC 轉換：大部分檔案用 `s2twp`（臺灣用詞），`market-knowledge/hongkong.md` 用 `s2hk`（香港用字）。
- **要修改內容請改這裡，再重新轉換繁體版**，不要只改單邊，避免兩邊不同步。

## 目錄

| 檔案 | 內容 |
|---|---|
| `diagnostic-framework.md` | 6 大維度評分框架、分階段權重 |
| `checklists/` | 5 個維度的細部檢查清單 |
| `industry-knowledge/` | 品類知識庫（寵物用品／美妝保養／食品零食） |
| `market-knowledge/` | 市場知識庫（臺灣／馬來西亞／新加坡／香港／中國大陸） |
| `recommendation-templates.md` | 25 個常見問題的建議話術 |
| `tool-integrations.md` | 工具串接定義 |
| `report-template.md` | HTML 報告模板 |

要新增品類或市場，照著 `industry-knowledge/_template.md`、`market-knowledge/_template.md` 填即可。
