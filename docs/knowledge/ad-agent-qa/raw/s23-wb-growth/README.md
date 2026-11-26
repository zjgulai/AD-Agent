# 跨境电商增长（Cross-border Growth）

> 选品调研、Listing 优化、广告竞品分析、评论洞察四线协作，覆盖亚马逊运营全链路。

## 概览

| 项 | 值 |
|---|---|
| 类型 | **Team 型**（1 主理人 + 4 成员） |
| 分类 ID | `07-SalesCommerce`（销售电商） |
| 内嵌技能 | 15 个（含 amazon-skill 聚合包展开的 9 个子技能） |
| 覆盖平台 | 亚马逊各站点、TikTok Shop |
| 头像 | `avatars/`（512×512 PNG，单张 ≤ 500KB） |

## 什么时候用它

**适合**
- 「想卖某个品类，不知道选什么」→ 类目调研与选品
- 「选好了，验证一下值不值得做」→ 多源交叉验证
- 「已上架但卖不动」→ Listing 诊断与改写
- 「想抢竞品流量」→ 广告结构与竞品拆解
- 「差评突然变多」→ 评论洞察与产品迭代

**不适合**
- 国内电商（淘宝/拼多多）→ 本团队的 skill 全部面向跨境
- 独立站 DTC 品牌营销 → 不在覆盖范围
- 只要一个 Listing 标题润色 → 直接找 `listing-optimizer` 单点即可，不必进全流程

## 团队成员分工

| 成员 | Agent ID | 名字 | 职责 | 主要调用的 skill |
|---|---|---|---|---|
| 增长操盘手 | `cross-border-growth-team-lead` | 贺出海 | 锁定目标与卡点、按 SOP 调度、汇总结论 | 统筹，不亲自跑数据 |
| 选品调研员 | `market-researcher` | 甄好卖 | 类目调研、选品、关键词库、外贸市场 | `exa-foreign-trade-research`、`sorftime-rpa`、`sellersprite-rpa`、`fastmoss-rpa`、`category-selection` |
| Listing 优化师 | `listing-optimizer` | 章达标 | Listing 检查评分、标题五点 A+ 改写 | `amazon-listing-builder`、`amazon-listing-alexa-optimizer`、`keyword-research` |
| 竞品广告策略师 | `ads-strategist` | 简知彼 | 竞品拆解、广告策略、流量结构、投放监控 | `amazon-analyse`、`xiyou-insight`、`product-research` |
| 评论洞察分析师 | `review-insight-analyst` | 闻心声 | 评论情感归因、痛点聚类、产品迭代建议 | `simple-review-analyzer`、`review-analysis` |

## 工作流（SOP）

主理人先做 **Phase 0**：明确站点与品类、判断当前卡点，卡点不同路线完全不同。

```
卡点判断
   ├─ 还没选品        → Workflow A（选品优先）
   ├─ 选好了要验证    → Workflow B（验证优先）
   └─ 已上架卖不动    → Workflow C（诊断优先）
```

**Workflow A · 选品优先**
1. `market-researcher` 跑宏观趋势与准入门槛（先扫合规风险）
2. 跑类目大盘，把红海 / 蓝海用数字标出来
3. 在候选类目挖爆款 ASIN，交叉验证 BSR 走势与评论拐点
4. 输出：主推 1 个 / 备选 2 个 / 放弃 N 个，理由各一句

**Workflow B · 验证优先**
1. `market-researcher` 复核竞争密度与利润空间
2. `listing-optimizer` 按 Alexa 购物时代标准预检文案
3. `review-insight-analyst` 挖同类目差评，把痛点前置进文案

**Workflow C · 诊断优先**
1. `ads-strategist` 先用 `amazon-analyse` 拉历史数据复盘（**不复盘就新建是浪费预算**）
2. `listing-optimizer` 按数据改文案（没有数据支撑就不改）
3. `review-insight-analyst` 查差评是否集中在某个 SKU 子型号/某月份 —— 可能是质量或供应链事故

## 内嵌技能清单（15 个）

**市场调研与选品**

| skill | 用途 |
|---|---|
| `exa-foreign-trade-research` | 目标国家 + 产品领域的宏观调研：品牌商/制造商/经销商、定价策略、渠道与进入建议 |
| `sorftime-rpa` | Sorftime 类目大盘 RPA，一个技能覆盖 11 个板块 |
| `sellersprite-rpa` | 卖家精灵 RPA，5 大数据板块统一 CLI |
| `sellersprite-amazon-research` | 卖家精灵全链路：43 个 MCP 工具覆盖选品、关键词、竞品、广告、蓝海挖掘 |
| `fastmoss-rpa` | FastMoss（TikTok Shop）RPA，7 大榜单：商品/小店/达人/视频/直播等 |
| `sif-amazon-research` | Sif 亚马逊调研：市场验证、竞品分析、流量诊断、关键词策略 |
| `category-selection` | 亚马逊品类五维评分模型，自动生成 Markdown 调研报告 |
| `product-research` | 深度选品：数据采集 → 属性标注 → 交叉分析 → 竞品 VOC → 壁垒评估 |
| `keyword-research` | 关键词深度调研，2000+ 词按 8 维度智能分类（否定/品牌/材质/场景/属性/功能/核心） |

**Listing 与广告**

| skill | 用途 |
|---|---|
| `amazon-listing-builder` | 爆款 Listing 打造（Cosmo 语义算法 + Alexa/Rufus 对话式购物趋势） |
| `amazon-listing-alexa-optimizer` | 按 Alexa for Shopping / AI 购物时代标准检查并优化 Listing |
| `amazon-analyse` | 竞品 Listing 全维度穿透：文案逻辑、评论、关键词、市场动态 → Markdown 报告 |
| `xiyou-insight` | 西柚洞察：广告监控、流量缺口、竞品打法拆解、关键词库搭建（7 大场景） |

**评论洞察**

| skill | 用途 |
|---|---|
| `review-analysis` | 评论深度分析：痛点识别、退货原因、改进建议、客服回复模板 |
| `simple-review-analyzer` | 22 维度智能标签 + 用户画像识别 + 可视化看板 |

## 使用示例

```
帮我调研美国站宠物用品类目，找出有利润空间且竞争度低的细分品
```

```
检查这个 Amazon Listing，按 Alexa 购物时代的要求给评分和改写建议
```

```
分析这款竞品的广告投放策略和流量结构
```

## 团队铁律

1. **不在没有 sorftime 大盘数据的情况下推荐具体 ASIN** —— 凭直觉选品是上一个十年亚马逊卖家的老毛病，今天已废。
2. **同一类目至少 2 个数据源交叉**，确认后再下结论。
3. **没有 `amazon-analyse` 历史数据时不新建广告计划** —— 你不知道这个词之前的天花板在哪。
4. **没有数据支撑就不改 Listing 文案** —— 改动必须是可归因的。
5. **每条评论洞察结论必须有 ≥ 3 条买家原话支撑** —— 单条评论不足以下结论。
6. 不为「打曝光」做不设上限的竞品词投放，所有词必须给出目标 ACOS。
7. 复盘结论要落到具体行动（哪几个词降价、哪个 Listing 改文案），不能停在「我们发现 ACOS 偏高」。

## 目录结构

```
cross-border-growth/
├── .codebuddy-plugin/
│   └── plugin.json          # 专家元数据（含 members / quickPrompts）
├── agents/                  # 5 个 agent 定义
│   ├── cross-border-growth-team-lead.md
│   ├── market-researcher.md
│   ├── listing-optimizer.md
│   ├── ads-strategist.md
│   └── review-insight-analyst.md
├── skills/                  # 15 个内嵌技能
├── avatars/                 # 头像
└── README.md
```

## 安装

将专家包目录放到专家目录下：

```
C:\Users\49707\.workbuddy\plugins\marketplaces\my-experts\plugins\cross-border-growth\
```

然后运行注册命令使其可见（必须用 Windows 风格路径）：

```bash
python "D:\WorkBuddy\resources\app.asar.unpacked\resources\plugins\workbuddy-builtin\skills\expert-manager\scripts\register_expert.py" "C:/Users/49707/.workbuddy/plugins/marketplaces/my-experts/plugins/cross-border-growth"
```

修改 `plugin.json` 后可用校验脚本自查：

```bash
python "D:\WorkBuddy\resources\app.asar.unpacked\resources\plugins\workbuddy-builtin\skills\expert-manager\scripts\validate_expert.py" "C:/Users/49707/.workbuddy/plugins/marketplaces/my-experts/plugins/cross-border-growth"
```

## 打包分享

> 打包要点：zip 根目录必须是专家目录本身（内含 `.codebuddy-plugin/`），不要多包一层。

```bash
cd "C:\Users\49707\.workbuddy\plugins\marketplaces\my-experts\plugins"
zip -r cross-border-growth.zip cross-border-growth/
```

## 平台校验注意事项

平台解析 zip 报「解析失败」时，优先检查这几条（都是踩过的）：

- `defaultInitPrompt.zh/en` 必须与 `quickPrompts[0].zh/en` **逐字一致**
- Team 型 `members[].name` 的 `en` / `zh` **均为必填**
- `profession.zh` 必须等于 `displayName.zh`（否则 warn）
- 中文文案里不要用裸半角双引号，会断 JSON —— 用全角「」或转义 `\"`
