# AI 跨境地图诊断 Skill

> 一个 AI 技能包，帮你生成专属的「跨境出海诊断报告」。
> 由 Vivi（GoAskVivi）建立，内含 22 年跨境电商与 Meta 广告实战经验。

[繁體中文](README.md) ｜ 简体中文

---

## 这是什么？

把这个技能包装进你的 AI（Codex、Claude 或任何模型），它就会用一套固定的框架帮你的品牌做健检，产出一份诊断报告，包含：

| 诊断维度 | 看什么 |
|---|---|
| 品牌定位 | 品牌名差异化、视觉识别一致性、品牌主张 |
| 官网健康度 | 多币别、支付、物流、移动体验、速度 |
| SEO / AEO / GEO | 结构化内容、开门见山、外部引用、图片 ALT |
| 广告投放准备度 | Pixel / GA4、素材、受众、预算测试、落地页 |
| 私域流量 | 平台覆盖、会员制度、互动频率、复购引导 |
| 行动计划 | 优先级、资源盘点、30 天快速胜利项目 |

报告会给每个维度 0–100 分、现况分析、具体建议，以及一份 30 天行动清单。

**权重会依品牌阶段调整**——第一年的品牌看「官网 + 广告」，第二年以后的品牌看「品牌 + 私域」。详见 `references/diagnostic-framework.md`。

---

## 如何使用？

### 方法 1：Codex / Claude Code 用户（推荐）

下载后跑安装脚本，它会自动检测你装的是 Codex 还是 Claude Code：

```bash
git clone https://github.com/vivi911/goaskvivi-dtc-diagnostic-skill.git
cd goaskvivi-dtc-diagnostic-skill
bash install.sh
```

安装完重开你的 AI 工具，然后直接说：

```
帮我做跨境出海诊断
```

它会反问你品牌资料，然后产出报告。

> 手动安装也可以：把整个文件夹复制到
> `~/.codex/skills/goaskvivi-dtc-diagnostic/`（Codex）或
> `~/.claude/skills/goaskvivi-dtc-diagnostic/`（Claude Code）。

> **访问 GitHub 不方便？** 不用下载也能用——直接看下面的「方法 3」，
> 把那段咒语复制贴进任何 AI 就能开始诊断。

### 方法 2：ChatGPT / Claude 网页版用户

1. 下载这个 repo（右上角 **Code → Download ZIP**）
2. 打开 `references/` 文件夹，把里面的 `.md` 文件内容复制起来
3. 贴到对话框，跟 AI 说：「请根据这些内容，帮我生成跨境出海诊断报告」

建议至少贴这三个文件：`diagnostic-framework.md`、对应你品类的 `industry-knowledge/*.md`、对应你市场的 `market-knowledge/*.md`。

### 方法 3：任何 AI 模型（免下载 · 随身版）

适合国内模型（Kimi、DeepSeek、豆包等网页/App）：不用下载、不用安装，复制贴上就能用。

1. 打开仓库根目录的 **`PORTABLE.zh-CN.md`（随身版）**
2. 全选复制，贴进任何 AI 的对话框
3. 填好末尾的四行品牌资料，送出

随身版由脚本 `build-portable.sh` 从 `references/` 正式内容自动组装（评分框架 + 大陆市场与法规 + 25 条建议话术），
与完整版同一套知识库；references 更新后跑一次脚本即可重组，不会脱节。

---

## 文件结构

```
.
├── SKILL.md                        # Skill 定义与工作流程
├── install.sh                      # 一键安装到 Codex / Claude Code
├── PORTABLE.zh-CN.md               # 随身版：任何 AI 免安装，复制贴上即用
├── build-portable.sh               # 从 references/ 一键重组随身版
├── assets/                         # 报告用图片（微信二维码放这里）
├── references/                     # 简体中文（默认）
│   ├── diagnostic-framework.md     # 6 大维度评分框架（分阶段权重）
│   ├── checklists/                 # 5 个维度的细部检查清单
│   ├── industry-knowledge/         # 品类知识库（宠物／美妆／食品）
│   ├── market-knowledge/           # 市场知识库（台湾／马来西亚／新加坡／香港／中国大陆）
│   ├── recommendation-templates.md # 25 个常见问题的建议话术
│   ├── tool-integrations.md        # 工具串接定义
│   └── report-template.md          # HTML 报告模板
└── references-zh-tw/               # 繁体中文镜像（台湾／香港市场）
```

想扩充品类或市场？`industry-knowledge/_template.md` 与 `market-knowledge/_template.md` 是通用模板，照着填就能加新的一份。

---

## 语言版本

- `references/`：简体中文 — 产出简体报告时读这套
- `references-zh-tw/`：繁体中文 — 产出繁体报告时读这套

⚠️ 两套内容一一对应。**要修改请改简体版 `references/`，再重新转换繁体版**，避免两边不同步。

---

## 这个诊断不会做的事

- 不承诺具体营收数字、ROAS 目标或增长百分比
- 不虚构竞品数据、市场规模或客户见证
- 资料不足时会先反问，不会硬掰

诊断是健检，不是保证书。它帮你找出「现在最该补的洞」，实际执行还是要靠你自己或找人陪跑。

---

## 想再深入一点？

这份诊断是自助工具，帮你找出「现在最该补的洞」。

其他技能包与后续资源都在 👉 **https://goaskvivi.com/ai-skill-pack/**

---

## 授权

本 Skill 由 Vivi（GoAskVivi）建立，开放个人学习与自用，**不得转售或作为商业服务内容贩售**。
欢迎分享链接，转载请注明出处。

## 联系方式

- 官网：https://goaskvivi.com
- 技能包页面：https://goaskvivi.com/ai-skill-pack/
