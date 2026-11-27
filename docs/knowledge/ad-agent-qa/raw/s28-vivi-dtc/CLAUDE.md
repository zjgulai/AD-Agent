# CLAUDE.md — 維護規則

這個 repo 是**公開發佈**的技能包（對外提供下載）。動任何檔案前先讀這頁。

## 這是什麼

`goaskvivi-dtc-diagnostic` 母 Skill 的公開發佈版。
**內部工作副本**在 `~/個人/goaskvivi-studio-skills/goaskvivi-dtc-diagnostic/`，
那份多了 `HANDOFF.md` 與 `VIVI-REVIEW-CHECKLIST.md`（內部文件，**不進這個公開 repo**）。

兩份要手動同步，改完記得兩邊都更新。

## 鐵律

1. **這是公開 repo** — 推任何東西前先掃一次：金鑰、客戶名單、美力／bebetterone 相關內容、
   個人電話信箱、內部話術，一律不可進來。
2. **內容是「通用框架」不是品牌專屬** — 不要放小巴黎（de Balets）的具體商品名稱、
   聯名對象、溝通核心文案。**教學舉例一律用虛構品牌**（目前是 Nordelle／小名「小北」），
   真實品牌案例要引用前必須有事前書面同意。
3. **改內容改简体版 `references/`，再重新轉繁體 `references-zh-tw/`** —
   不要只改單邊。繁體版用 OpenCC 轉（多數 `s2twp`，`market-knowledge/hongkong.md` 用 `s2hk`）。
4. **價格方案是 Vivi 定的，不要自己改**：¥999 一小時諮詢／¥2,888 一品出海策略包／
   ¥8,888 Meta 廣告投流陪跑。
5. **不承諾成效** — 不寫保證營收、ROAS 數字、成長百分比，不寫「前 N 名免費」這類稀缺鉤子。

## 已知待補

- `assets/wechat-qr.png` **尚未提供**。`references/report-template.md` 的 CTA 區塊會引用它，
  圖沒放進來之前，產出的報告那格會是破圖。詳見 `assets/README.md`。

## 動 install.sh 要注意

- ⚠️ **變數後面接全形標點時一定要寫 `${var}`**。macOS 內建的 bash 3.2 會把全形字的位元組
  當成變數名的一部分，`$label：` 會被讀成變數 `label：` → `unbound variable`，整個腳本掛掉。
  改完用 `grep -nP '\$[A-Za-z_][A-Za-z0-9_]*[^\x00-\x7F]' install.sh` 檢查，應該要沒有結果。
- 安裝流程是「組到暫存資料夾 → 成功才換掉舊版」，不要改回「先刪再複製」（中途失敗會毀掉使用者的舊版）。
- 改完至少測這幾種情況：自動偵測、指定 codex／claude、錯誤參數、兩個工具都沒裝、
  重跑一次、以及**從已安裝目錄裡面執行**（來源與目的地相同，不能把來源刪掉）。
