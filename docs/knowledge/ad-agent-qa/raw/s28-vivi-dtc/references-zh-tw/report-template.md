# HTML 診斷報告模板

> 定義報告的結構、視覺與呈現方式。產出為單檔案 HTML（內聯 CSS + Chart.js CDN），可直接瀏覽器開啟或轉 PDF。
> 檔案命名：`report_{品牌名}_{YYYYMMDD}.html`
> 語言：預設簡體中文；臺灣/香港市場改繁體。

## 報告結構總覽

1. 封面（品牌名、日期、總分、等級徽章）
2. 執行摘要（3 句話結論 + Top 3 優先建議）
3. 六維度雷達圖
4. 六維度詳細分析（每維度：得分、發現、證據、建議）
5. 30 天行動清單（按周分段）
6. 推薦 Skill 指令（下一步可用的工具）
7. CTA + 微信 QR Code（三個價格方案）
8. 免責宣告

---

## 一、封面

- 頂部：GoAskVivi 品牌標識 +「DTC 跨境出海診斷報告」
- 中央：客戶品牌名（大標題）、品類、目標市場
- 總分圓環：大數字總分（0-100）+ 等級徽章（🚨 待加強 / ⚠️ 及格 / ✅ 優秀）
- 底部：診斷日期、報告編號
- 視覺：深色系背景 + 品牌主色點綴，專業感優先

```html
<header class="cover">
  <div class="brand-mark">GoAskVivi · DTC 跨境出海診斷報告</div>
  <h1>{{品牌名}}</h1>
  <p class="meta">{{品類}} · 目標市場：{{市場}} · {{日期}}</p>
  <div class="score-ring">
    <span class="score">{{總分}}</span>
    <span class="grade">{{等級徽章}}</span>
  </div>
</header>
```

## 二、執行摘要

- 3 句話講完整體狀況：「目前處於 ___ 階段，最大優勢是 ___，最優先要補的是 ___」
- Top 3 優先建議（每條一行：問題 → 動作 → 預期改善方向）
- 這一段是給「只看 30 秒」的老闆看的，不堆術語

```html
<section class="exec-summary">
  <h2>診斷結論</h2>
  <p>{{3 句話總結}}</p>
  <ol class="top-priorities">
    <li><strong>{{問題1}}</strong>：{{動作}}（{{預期改善}}）</li>
    <li><strong>{{問題2}}</strong>：{{動作}}（{{預期改善}}）</li>
    <li><strong>{{問題3}}</strong>：{{動作}}（{{預期改善}}）</li>
  </ol>
</section>
```

## 三、六維度雷達圖

- 用 Chart.js radar chart，6 軸：品牌定位、官網健康、SEO/AEO/GEO、廣告準備、私域流量、行動計劃
- 每個維度顯示加權前得分（0-25 分制），懸浮顯示加權後分數（按品牌階段套用對應權重）
- 配色：填充半透明品牌色，網格線淺灰

```html
<section class="radar">
  <h2>六維度健康度</h2>
  <canvas id="radarChart"></canvas>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <script>
    new Chart(document.getElementById('radarChart'), {
      type: 'radar',
      data: {
        labels: ['品牌定位', '官網健康', 'SEO/AEO/GEO', '廣告準備', '私域流量', '行動計劃'],
        datasets: [{
          label: '{{品牌名}}',
          data: [{{品牌定位}}, {{官網健康}}, {{SEO得分}}, {{廣告得分}}, {{私域得分}}, {{計劃得分}}],
          backgroundColor: 'rgba(99, 102, 241, 0.25)',
          borderColor: 'rgba(99, 102, 241, 1)',
          pointBackgroundColor: 'rgba(99, 102, 241, 1)'
        }]
      },
      options: { scales: { r: { min: 0, max: 25 } } }
    });
  </script>
</section>
```

## 四、六維度詳細分析

每個維度一個區塊，結構固定：

- 維度名 + 權重（按品牌階段）+ 得分（帶顏色：低分紅、中分黃、高分綠）
- **關鍵發現**：3-5 條 bullet，每條標註證據來源（截圖/實測/調研）
- **做得好**：1-2 條（有發現才寫，沒有就省略，不硬誇）
- **建議動作**：按優先順序排序，每條含：動作、工具/資源、預計工時、預期改善方向
- 建議話術從 `recommendation-templates.md` 取，按品牌情況改寫

```html
<section class="dimension" id="dim-ads">
  <h3>4. 廣告投放準備度 <span class="weight">權重 {{階段權重}}</span>
    <span class="score score-low">{{得分}}/25</span></h3>
  <h4>關鍵發現</h4>
  <ul>
    <li>Pixel 未設定 Purchase 事件（證據：events-check.png）</li>
    <li>素材庫僅有供應商白底圖，無 UGC 與影片素材</li>
    <li>無自訂受眾與再行銷分層</li>
  </ul>
  <h4>建議動作</h4>
  <ol>
    <li>🔴 用 Event Setup Tool 設好三個標準事件（半天）— 沒設好前不開廣告</li>
    <li>🔴 招募 10 位種子客戶拍開箱影片（2 周）— UGC 素材 CTR 通常為產品圖 2-3 倍</li>
    <li>🟡 建立三組再行銷受眾（半天）</li>
  </ol>
</section>
```

## 五、30 天行動清單

- 按周分四段，每段 2-4 件事，每件事：動作 + 預計工時 + 對應維度
- 第 1 周只放「快贏」（半天到 2 天能完成的）
- 總量控制：30 天內不超過 12 件事，防止「什麼都想做」

```html
<section class="action-plan">
  <h2>30 天行動清單</h2>
  <div class="week"><h4>第 1-7 天 · 快速勝利</h4>
    <ul>
      <li>⬜ 設好 Pixel 三個標準事件（半天）· 廣告</li>
      <li>⬜ 商品頁加運費說明與免運門檻（1 天）· 官網</li>
      <li>⬜ 開通訪客結賬，欄位砍到 5 個（1 天）· 官網</li>
    </ul>
  </div>
  <div class="week"><h4>第 8-14 天 · 基礎建設</h4> ... </div>
  <div class="week"><h4>第 15-21 天 · 內容與素材</h4> ... </div>
  <div class="week"><h4>第 22-30 天 · 測試與最佳化</h4> ... </div>
</section>
```

## 六、推薦 Skill 指令

- 列出客戶下一步可以直接使用的指令，引導進入服務生態
- 按診斷結果挑 3-5 條最相關的，不全列

| 場景 | 指令示例 |
|---|---|
| 內容改造 | 「用 AEO/GEO 內容教練幫我改寫 FAQ 頁」 |
| 廣告素材 | 「幫我產出 5 組 UGC 風格素材指令碼」 |
| 深度策略 | 「預約 1v1 諮詢，針對廣告維度深入規劃」 |

## 七、CTA + 微信 QR Code（三個價格方案）

- 固定結尾區塊，不省略
- 文案：「這份報告只是起點。想更深入拆解你的品牌，掃碼預約諮詢，三個方案選一個適合你的節奏。」
- 直接列出三個價格方案，不寫「前 10 名免費」之類的限量話術：

| 方案 | 價格 | 內容 |
|---|---|---|
| 一小時跨境諮詢 | ¥999 | 1v1 語音/影片，針對報告結果深入拆解，回答具體問題 |
| 一品出海策略包 | ¥2,888 | 單一品項完整出海策略：定位、定價、渠道、廣告結構、90 天路線圖 |
| Meta 廣告投流陪跑 | ¥8,888 | 廣告投放實戰陪跑：賬戶搭建、素材方向、資料覆盤與最佳化 |

- QR Code 圖片：`<img src="assets/wechat-qr.png" alt="微信掃碼預約諮詢">`，寬度建議 160-200px
- ⚠️ `assets/wechat-qr.png` **不存在時不要輸出這個 `<img>`**，改寫成文字版：「更多技能包與後續資源：https://goaskvivi.com/ai-skill-pack/ 」。破圖比沒有圖更糟。

```html
<section class="cta">
  <h2>想更深入？</h2>
  <p>這份報告只是起點。想更深入拆解你的品牌，掃碼預約諮詢，三個方案選一個適合你的節奏。</p>
  <ul class="plans">
    <li><strong>¥999</strong>　一小時跨境諮詢</li>
    <li><strong>¥2,888</strong>　一品出海策略包</li>
    <li><strong>¥8,888</strong>　Meta 廣告投流陪跑</li>
  </ul>
  <img src="assets/wechat-qr.png" alt="微信掃碼預約諮詢" class="qr">
</section>
```

## 八、免責宣告

固定文案：

> 本報告基於品牌方提供的資訊與公開資料製作，評分與建議僅供參考，不構成對營收、廣告回報或增長的任何承諾。市場資料截至報告日期，請以最新情況為準。

---

## 視覺規範

- 字型：系統字型棧（`-apple-system, "PingFang SC", "Microsoft YaHei", sans-serif`）
- 主色：深靛藍 `#4F46E5`；低分紅 `#EF4444`、中分黃 `#F59E0B`、高分綠 `#10B981`
- 版面：單欄、最大寬度 860px 居中、列印友善（`@media print` 隱藏導航）
- 移動端可讀：字號 ≥ 15px，區塊間距 ≥ 32px
- 單檔案交付：CSS 內聯、Chart.js 走 CDN、圖片放 `assets/` 相對路徑

## 交付前檢查

- [ ] 總分與雷達圖數字一致（與 diagnostic-framework.md 的分階段加權重算核對）
- [ ] 每個扣分項都有證據來源
- [ ] 建議話術已從模板按品牌情況改寫，無「貴司」式模板腔殘留
- [ ] 30 天清單 ≤ 12 項，第 1 周全是快贏
- [ ] CTA 是三個價格方案（¥999 / ¥2,888 / ¥8,888），沒有「前 10 名免費」字樣
- [ ] 微信 QR Code 圖片可正常顯示
- [ ] 簡體/繁體符合目標市場
- [ ] 免責宣告在報告底部
