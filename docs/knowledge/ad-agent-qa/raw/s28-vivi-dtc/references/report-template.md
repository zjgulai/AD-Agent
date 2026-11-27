# HTML 诊断报告模板

> 定义报告的结构、视觉与呈现方式。产出为单文件 HTML（内联 CSS + Chart.js CDN），可直接浏览器打开或转 PDF。
> 档案命名：`report_{品牌名}_{YYYYMMDD}.html`
> 语言：默认简体中文；台湾/香港市场改繁体。

## 报告结构总览

1. 封面（品牌名、日期、总分、等级徽章）
2. 执行摘要（3 句话结论 + Top 3 优先建议）
3. 六维度雷达图
4. 六维度详细分析（每维度：得分、发现、证据、建议）
5. 30 天行动清单（按周分段）
6. 推荐 Skill 指令（下一步可用的工具）
7. CTA + 微信 QR Code（三个价格方案）
8. 免责声明

---

## 一、封面

- 顶部：GoAskVivi 品牌标识 +「DTC 跨境出海诊断报告」
- 中央：客户品牌名（大标题）、品类、目标市场
- 总分圆环：大数字总分（0-100）+ 等级徽章（🚨 待加强 / ⚠️ 及格 / ✅ 优秀）
- 底部：诊断日期、报告编号
- 视觉：深色系背景 + 品牌主色点缀，专业感优先

```html
<header class="cover">
  <div class="brand-mark">GoAskVivi · DTC 跨境出海诊断报告</div>
  <h1>{{品牌名}}</h1>
  <p class="meta">{{品类}} · 目标市场：{{市场}} · {{日期}}</p>
  <div class="score-ring">
    <span class="score">{{总分}}</span>
    <span class="grade">{{等级徽章}}</span>
  </div>
</header>
```

## 二、执行摘要

- 3 句话讲完整体状况：「目前处于 ___ 阶段，最大优势是 ___，最优先要补的是 ___」
- Top 3 优先建议（每条一行：问题 → 动作 → 预期改善方向）
- 这一段是给「只看 30 秒」的老板看的，不堆术语

```html
<section class="exec-summary">
  <h2>诊断结论</h2>
  <p>{{3 句话总结}}</p>
  <ol class="top-priorities">
    <li><strong>{{问题1}}</strong>：{{动作}}（{{预期改善}}）</li>
    <li><strong>{{问题2}}</strong>：{{动作}}（{{预期改善}}）</li>
    <li><strong>{{问题3}}</strong>：{{动作}}（{{预期改善}}）</li>
  </ol>
</section>
```

## 三、六维度雷达图

- 用 Chart.js radar chart，6 轴：品牌定位、官网健康、SEO/AEO/GEO、广告准备、私域流量、行动计划
- 每个维度显示加权前得分（0-25 分制），悬浮显示加权后分数（按品牌阶段套用对应权重）
- 配色：填充半透明品牌色，网格线浅灰

```html
<section class="radar">
  <h2>六维度健康度</h2>
  <canvas id="radarChart"></canvas>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <script>
    new Chart(document.getElementById('radarChart'), {
      type: 'radar',
      data: {
        labels: ['品牌定位', '官网健康', 'SEO/AEO/GEO', '广告准备', '私域流量', '行动计划'],
        datasets: [{
          label: '{{品牌名}}',
          data: [{{品牌定位}}, {{官网健康}}, {{SEO得分}}, {{广告得分}}, {{私域得分}}, {{计划得分}}],
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

## 四、六维度详细分析

每个维度一个区块，结构固定：

- 维度名 + 权重（按品牌阶段）+ 得分（带颜色：低分红、中分黄、高分绿）
- **关键发现**：3-5 条 bullet，每条标注证据来源（截图/实测/调研）
- **做得好**：1-2 条（有发现才写，没有就省略，不硬夸）
- **建议动作**：按优先级排序，每条含：动作、工具/资源、预计工时、预期改善方向
- 建议话术从 `recommendation-templates.md` 取，按品牌情况改写

```html
<section class="dimension" id="dim-ads">
  <h3>4. 广告投放准备度 <span class="weight">权重 {{阶段权重}}</span>
    <span class="score score-low">{{得分}}/25</span></h3>
  <h4>关键发现</h4>
  <ul>
    <li>Pixel 未设定 Purchase 事件（证据：events-check.png）</li>
    <li>素材库仅有供应商白底图，无 UGC 与视频素材</li>
    <li>无自订受众与再行销分层</li>
  </ul>
  <h4>建议动作</h4>
  <ol>
    <li>🔴 用 Event Setup Tool 设好三个标准事件（半天）— 没设好前不开广告</li>
    <li>🔴 招募 10 位种子客户拍开箱视频（2 周）— UGC 素材 CTR 通常为产品图 2-3 倍</li>
    <li>🟡 建立三组再行销受众（半天）</li>
  </ol>
</section>
```

## 五、30 天行动清单

- 按周分四段，每段 2-4 件事，每件事：动作 + 预计工时 + 对应维度
- 第 1 周只放「快赢」（半天到 2 天能完成的）
- 总量控制：30 天内不超过 12 件事，防止「什么都想做」

```html
<section class="action-plan">
  <h2>30 天行动清单</h2>
  <div class="week"><h4>第 1-7 天 · 快速胜利</h4>
    <ul>
      <li>⬜ 设好 Pixel 三个标准事件（半天）· 广告</li>
      <li>⬜ 商品页加运费说明与免运门槛（1 天）· 官网</li>
      <li>⬜ 开通访客结账，字段砍到 5 个（1 天）· 官网</li>
    </ul>
  </div>
  <div class="week"><h4>第 8-14 天 · 基础建设</h4> ... </div>
  <div class="week"><h4>第 15-21 天 · 内容与素材</h4> ... </div>
  <div class="week"><h4>第 22-30 天 · 测试与优化</h4> ... </div>
</section>
```

## 六、推荐 Skill 指令

- 列出客户下一步可以直接使用的指令，引导进入服务生态
- 按诊断结果挑 3-5 条最相关的，不全列

| 场景 | 指令示例 |
|---|---|
| 内容改造 | 「用 AEO/GEO 内容教练帮我改写 FAQ 页」 |
| 广告素材 | 「帮我产出 5 组 UGC 风格素材脚本」 |
| 深度策略 | 「预约 1v1 咨询，针对广告维度深入规划」 |

## 七、CTA + 微信 QR Code（三个价格方案）

- 固定结尾区块，不省略
- 文案：「这份报告只是起点。想更深入拆解你的品牌，扫码预约咨询，三个方案选一个适合你的节奏。」
- 直接列出三个价格方案，不写「前 10 名免费」之类的限量话术：

| 方案 | 价格 | 内容 |
|---|---|---|
| 一小时跨境咨询 | ¥999 | 1v1 语音/视频，针对报告结果深入拆解，回答具体问题 |
| 一品出海策略包 | ¥2,888 | 单一品项完整出海策略：定位、定价、渠道、广告结构、90 天路线图 |
| Meta 广告投流陪跑 | ¥8,888 | 广告投放实战陪跑：账户搭建、素材方向、数据复盘与优化 |

- QR Code 图片：`<img src="assets/wechat-qr.png" alt="微信扫码预约咨询">`，宽度建议 160-200px
- ⚠️ `assets/wechat-qr.png` **不存在时不要输出这个 `<img>`**，改写成文字版：「更多技能包与后续资源：https://goaskvivi.com/ai-skill-pack/ 」。破图比没有图更糟。

```html
<section class="cta">
  <h2>想更深入？</h2>
  <p>这份报告只是起点。想更深入拆解你的品牌，扫码预约咨询，三个方案选一个适合你的节奏。</p>
  <ul class="plans">
    <li><strong>¥999</strong>　一小时跨境咨询</li>
    <li><strong>¥2,888</strong>　一品出海策略包</li>
    <li><strong>¥8,888</strong>　Meta 广告投流陪跑</li>
  </ul>
  <img src="assets/wechat-qr.png" alt="微信扫码预约咨询" class="qr">
</section>
```

## 八、免责声明

固定文案：

> 本报告基于品牌方提供的信息与公开资料制作，评分与建议仅供参考，不构成对营收、广告回报或增长的任何承诺。市场数据截至报告日期，请以最新情况为准。

---

## 视觉规范

- 字体：系统字体栈（`-apple-system, "PingFang SC", "Microsoft YaHei", sans-serif`）
- 主色：深靛蓝 `#4F46E5`；低分红 `#EF4444`、中分黄 `#F59E0B`、高分绿 `#10B981`
- 版面：单栏、最大宽度 860px 居中、打印友善（`@media print` 隐藏导航）
- 移动端可读：字号 ≥ 15px，区块间距 ≥ 32px
- 单文件交付：CSS 内联、Chart.js 走 CDN、图片放 `assets/` 相对路径

## 交付前检查

- [ ] 总分与雷达图数字一致（与 diagnostic-framework.md 的分阶段加权重算核对）
- [ ] 每个扣分项都有证据来源
- [ ] 建议话术已从模板按品牌情况改写，无「贵司」式模板腔残留
- [ ] 30 天清单 ≤ 12 项，第 1 周全是快赢
- [ ] CTA 是三个价格方案（¥999 / ¥2,888 / ¥8,888），没有「前 10 名免费」字样
- [ ] 微信 QR Code 图片可正常显示
- [ ] 简体/繁体符合目标市场
- [ ] 免责声明在报告底部
