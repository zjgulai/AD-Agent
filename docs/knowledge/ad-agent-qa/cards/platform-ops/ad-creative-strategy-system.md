---
title: 广告创意策略系统 · Hook 三组件、创意策略循环、Meta 51 格式分级与竖屏视频生产规范
doc_type: knowledge
module: ad-agent-qa
topic: ad-creative-strategy-system
status: review
created: 2026-11-27
updated: 2026-11-27
owner: self
source: human+ai
source_docs: [S25]
fetched_at: 2026-11-27
---

# 广告创意策略系统 · Hook 三组件、创意策略循环、Meta 51 格式分级与竖屏视频生产规范

## 核心问题

广告素材创意怎么系统化生产而不是凭灵感？「这条广告为什么不行」怎么定位到具体组件？新格式/新概念怎么排序投入？本卡蒸馏 marketingskills `ad-creative` skill 全套——这是 KB 中 G5「素材创意」缺口的最大单点补齐：从 Hook 生成管线到 Meta 51 格式 S→F 分级到竖屏视频 safe-zone 生产规范。

## 系统解答

### 1. 来源与定位

- **来源**：`github.com/coreyhaines31/marketingskills`（MIT，`raw/s25-marketingskills/skills/ad-creative/`）。SKILL.md v2.13.5 + 11 个 references。
- **框架谱系**：格式分级改编自 Dara Denney（Meta 10 年、~20,000 素材团队）的 51 格式 tier list；竖屏规范改编自 Daniel Hangan 的 reelclaw-templates；部分结构借鉴 Oren John 的 vlog/yapping playbook——**模式署名、描述重写**。
- **与现有 KB 的关系**：`tiktok-content-ads-playbook`（S22）管 TikTok 内容公式/达人策略/广告测试法，本卡管**创意生产系统**（怎么想 hook、怎么排素材优先级、怎么做竖屏视频）——前者是渠道打法，后者是创意工程层；`meta-quantified-decision-engine`（S25 同批）管投放后 kill/keep/scale，本卡管投放前「做什么素材」。

### 2. Grounded Inputs：先有语料库再有创意

规模化 AI 生成广告的失败不在输出质量在**输入 grounding**——无 grounding 的生成产出「看起来对」的广告而非「对这个品牌有效」的广告。Mode 3（规模化静态批量）必须先建持久语料库：

```
inputs/
  winning-ads/   近 90 天高表现广告截图 10-20 张
  reviews/       客户评论 50-100 条（Trustpilot/G2/Amazon/App Store）
  comments/      现有广告的 top 评论——异议、无提示好评、顾客自发角度
brand/           品牌语气文档、色板、logo、产品截图资产
outputs/         按日期的批次目录
```

**三类输入各自的价值**：winning-ads 带已验证的 hook/结构/角度；reviews 带买家描述痛点/转变的**原话**（逐字引用优于改写）；ad comments 是最常被跳过也最高价值的输入——异议（"but does it work for X?"）变 FAQ Card 广告，无提示好评浮现你没写过的角度。

**Grounding 铁律**：每个概念注明语料来源（哪条评论/哪张赢家广告）；**永不发明 claims/stats/证书**；winning-ads 或 reviews 为空时**停下来要用户补料，不许无 grounding 降级生成**；输入会衰减——winning-ads 随新广告 scale 刷新，reviews/comments 每月刷新。

### 3. Hook 系统：Hook 是三组件不是一句话

前三秒决定广告其余部分是否存在。Hook 多样性赚的是增量学习——不同 hook 触达不同受众口袋，近似雷同的开场只是重测同一批人。

**三组件（视频）**：

| 组件 | 是什么 | 职责 |
|------|--------|------|
| Visual action | 0-3 秒屏幕上实际发生的事 | 停住拇指 |
| Spoken line | VO/对话第一句 | 开信息环 |
| Caption text | 屏幕标题/叠加文字 | 给静音观众锚定主张 |

**不重复规则**：三组件必须互补绝不重复——VO 说「我不再付 $200/月健身房」而字幕写「我不再付 $200/月」+ 静态 talking head = 三个槽位浪费两个。强 hook 分工：画面给取消邮件截图、VO 给台词、字幕点名替代方案。**静态图塌缩为两组件**（视觉+headline），同规则：headline 不许给图片配字幕。

**生成管线（自上而下，跳步的 hook 像所有人的广告）**：

```
Segment → Motivation → Format → Hook（三组件）
```

1. **Segment**：不是整个 ICP，是共享处境的切片（从语料库评论/销售电话语言来）；切片越窄 hook 越锋利；
2. **Motivation**：驱动该切片的单一痛点/欲望/异议，用**他们的原话**——语料库语言永远胜过营销改写；
3. **Format**：先选载体再写词——street interview/POV selfie/屏幕录制/开箱/分屏演示/文字静态/创始人出镜，同一动机在不同形式里读感完全不同；
4. **Hook**：为该 segment×motivation×format 单元写三组件。

**输出为 hook matrix**（覆盖可见）：`| # | Segment | Motivation(原话+出处) | Format | Visual | Spoken | Caption |`——**跨矩阵生成不沿单列**：10 个 segment×motivation 单元各一个 hook 胜过 30 个同一单元的改写。「矩阵多样性=受众多样性」。

**开场动作清单**（像模板库一样轮换不扎堆）：curiosity gap（扣住名词，须广告内兑现否则毒化 CVR）/ bold claim（具体可证伪）/ first-person confession（无真实细节则假）/ contrast-before-after（转化须视觉诚实）/ relatability-POV（**特异性是全部机制**，泛化 POV 隐形）/ question（用他们搜索/问 AI 的原话）/ countdown-gamified（payoff 必须存在）/ proof-first（最强当凭证自己会说话）/ choice（两个选项都须是真实权衡）/ old-vs-new / us-vs-them / false assumption（点名竞品须法务审）/ declaration-then-question（2026-10 从业者仍在测）。后五个是**contrast 一族**——人通过对比理解事物，但好 contrast hook 比较的是受众真权衡的两物，而 AI 套路「it's not X, it's Y」否定的是没人主张过的东西。

**诊断漏斗**（每个指标隔离一个组件，广告不行时读漏斗定位修哪里而非整条扔）：

| 阶段 | 指标 | 弱说明 | 修 |
|------|------|--------|-----|
| 停 | Thumbstop/3s 观看率 | **Visual action**（和 caption）有问题 | 换视觉开场，其余不动 |
| 留 | Hold rate（3s→15s/50%） | **On-ramp**（hook 之后的衔接）有问题 | 重做 3-15 秒，不动 hook |
| 点 | CTR | 广告中段的欲望/offer 清晰度 | 磨尖承诺/CTA/证明 |
| 转 | CVR（点击后） | 不一致——页面没接住广告 | 修落地页或主张（见 cro） |

**两条铁律**：①高 thumbstop ≠ 好广告——clickbait 视觉吸来错的人表现为 thumbstop 高 + hold/CVR 崩，判 hook 前读完整漏斗；②**一次迭代只改一个组件**（视觉或 on-ramp 或 offer 框架）。

**On-ramp 规则**：on-ramp 是 ~3-15 秒从 hook 到正文的桥——**好 on-ramp 逻辑延续 hook 前提，坏的在桥上拐去产品 pitch**。hook 承诺「真正导致这个的是什么」，下一拍必须开始解释原因而非插入品牌故事。**每次 hook 测试同时是 on-ramp 测试**——新 hook 套旧广告正文通常破坏前提桥，每个 hook 要配自己的 on-ramp；hold rate 是 on-ramp 的指标，与 thumbstop 分开诊断。

**Fidelity laddering（保真阶梯）**：直觉假设 → 低保真一两天内出（静态图/文字视频/AI B-roll）；验证过的角度 → 才配高保真（创作者实拍/street interview/棚拍 demo）。**反向都是错**：用贵制作测未验证假设、用一次性静态图测已验证角度。阶梯单向运行。

### 4. 创意策略循环（Creative Strategy Loop）

回答「做什么素材、什么顺序、什么制作成本」——先于生成模式的常驻运营循环：

```
Signals → Concepts(证据分级) → Roadmap(分层+产能校验) → Briefs → [Modes 1-3 生产] → 月度 retro → 回 icebox
```

**第一步 · 三信号**（单一信号会误导——账户只告诉你「试过的里面什么有效」、客户告诉你「为什么买（他们的话）」、「外部有机内容告诉你受众没人付费时选择看什么」）：

| 信号 | 拉什么 | 怎么拉 |
|------|--------|--------|
| 账户表现 | 按角度/hook/形式的胜负、各概念漏斗指标、衰退状态 | 各平台 ads CLI |
| 客户/品牌 | 逐字痛点/欲望/异议语言、意外用法、实际买家 vs 定向人群 | Grounded Inputs 语料库+销售电话+客服主题 |
| 外部有机 | 该领域免费内容：top organic 的 hook/形式/词汇、竞品跑得够久 presumed working 的广告 | ad libraries/社媒监听/竞品分析 |

**频率**：每月深潜 60-90 分钟喂月度 roadmap + 每周 ~20 分钟刷新（新胜负/新评论主题/有机尖峰）。**每个洞察必须带凭证**（哪条评论/哪条广告指标/哪条有机帖）——没来源的洞察不进 icebox。每次综合必须以概念收尾不是笔记。

**第二步 · 证据分级概念**（概念=可测试创意假设：segment×motivation×angle×format+证据）：

| 级 | 证据 | 权重 |
|----|------|------|
| 1 | 自家账户：同角度/同受众的转化广告 | 最强——迭代+扩展 |
| 2 | 客户逐字：评论/电话反复出现的语言 | 强——新创意建在其上 |
| 3 | 竞品跑 60+ 天的创意（presumed working） | 好——学角度不学广告 |
| 4 | 领域有机互动（免费播放/收藏） | 中——先低成本验证 |
| 5 | 跨领域模式（相邻品类有效过） | 弱——icebox 等佐证 |
| 6 | 团队直觉无外部信号 | 最弱——低保真测或弃 |

高证据等级赢 roadmap **优先级**（slate 里更早的坑位）；生产层级是另一回事，由验证强度/现有资产/产能/风险定——tier-2 客户语言概念也先低保真直到漏斗信号出现。直觉不禁，但便宜且垫底。

**第三步 · 按账户状态分支**：

- **探索状态**（什么都没成/没有新的成）：**宽不是深**——大部分全新概念跨不同受众+角度，迭代占小头（迭代输家=批量生产输家）；**按单指标重定义「赢」**——没有全漏斗赢家时，任何测试的单指标改善（hold rate/CPC/CVR 任一）都是值得拉的线索；只迭代命中，其余保持探索；常见根因自查：素材无聊（安全但见过）、信息过复杂、offer/UVP 不清、CPM 惩罚太窄受众。
- **放量状态**（一两个概念在盈利转化）：**深挖赢家**——赢家主导 slate：视觉明显不同的变体（同信息新执行——近似重复主要蚕食原广告 reach 且没新信息，变体必须看起来真的不同）+ remix 道（同概念的情绪/语气重执行）+ 子角度探针（往赢家受众内部钻）；保留小额探索配额——赢家会疲劳，下一个赢家很少是当前赢家的迭代；放量窗口有限，速度优先。

**第四步 · Roadmap 工件**（`roadmap.md` 三层）：`## Icebox`（全部概念+证据级+来源，不排期）/`## This quarter`（2-4 个主题=押注+why-now）/`## This month`（slate：概念|证据级|生产级|负责人|状态）。

**生产层级**：T1 迭代=小时（现有素材换 hook/caption/裁剪，给已验证赢家）；T2 remix=天（现有素材/AI 生成新创意，有不错证据或首个低保真信号）；T3 production=周（全新拍摄/创作者/完整制作，**只给自家账户已证或低保真漏斗信号过的角度**）。

**产能校验铁律**：数团队（或 AI 管线）本月能**保质**产出多少，roadmap 对齐这个数——20 概念 slate 对 8 概念真实产能不产 20 条广告，产 20 条妥协货+burnout 团队。**按证据等级砍到 slate 装得下为止**。

**第五步 · 月度创意 retro**（`retros/YYYY-MM.md`）：`## Winners`（概念+漏斗数+为什么赢——哪个元素挣的）/`## Losers`（概念+死在漏斗哪段+假设）/`## Metric wins`（全漏斗输但单指标强——是线索不是输）/`## Learnings`（模式级笔记→写回 icebox）/`## Kills`（退役概念+理由）/`## Next slate`（下月初稿+更新证据级）。规则：**评概念不评广告**（同概念三执行全败=概念错，一败=执行错）；读漏斗不读 ROAS 列；数据够再下结论（两天读数是抛硬币）；**每条 learning 必须落地**（icebox 更新/证据重排/kill）——没改 roadmap 的 retro 是开会不是复盘。

### 5. Meta 创意格式分类法（51 格式 S→F 分级）

**唯一排序问题：这是 unicorn scaler 还是 supporting cast？**

- **Unicorn scaler**：刺穿**冷的净新增**受众且扛得住放量——稀缺，值得 disproportionate 投入；
- **Supporting cast**：转化已在中/低漏斗的人——有用必要，但无论投多少钱都打不开新受众。

格式不是「差」而是「角色不对」——别指望 supporting cast 去开冷受众。**建组合**：少数 unicorn scaler 负责刺穿，一排 supporting cast 负责转化。

**为什么 creator-fronted 格式霸榜（Andromeda）**：Andromeda 按 **persona** 定向——创作者 fronted 格式原生触达 persona（该 persona 本来就关注并信任这个创作者），partnership ad 的种子受众字面上就是创作者自己的受众。**信号**：rolling MoM reach 下降=当前受众饱和→上 creator-fronted 格式（尤其 partnership ads）恢复净新增。

**S 级（unicorn scaler，优先投）**：
- **Founder content**（低-中复杂度）：任何制作水平下可靠的第一赢家——讲「为什么创这个品牌」，自动连接同问题买家；无已验证创意时最早用；
- **Partnership ads**（中）：**当前 #1 投资优先级**，「不做 partnership ads 是拿黄油刀打枪战」；最佳 persona+净新增路径；rolling reach 下降时部署；
- **VSL**（中-高）：需要前置教育的品类（健康/保健/复杂机制）top tier；冲动型低决策商品跳过；剧本即广告。

**A 级**：amateur investigation（怀疑是门槛的品类）、yapper（高上限难驾驭，casting 是瓶颈）、David&Goliath（有真实反派时）、grid-style statics（多 SKU/组合，**最低门槛先测**）、authority ads（信任门槛高的 niche：保健品/美妆，须真实资质+合规审）、green-screen commentary（尤其服装+教育角度）、catalog/DPA（**被低估的事实**：不只再营销，DABA 冷启动也能跑）。

**B 级**（solid supporting cast）：TikTok love letter、real short、callout、before/after（盯宣称）、progression、tweet/Reddit statics（做第一帧好）、headline ads（需惊艳文案）、us-vs-them、hot-girl IG stories、creator low-fi statics（partnership 配套）、objection-handling（常进 top-15）、founder's letter static、conversation、educational infographics、mood board、comment-reply、challenging-your-beliefs、ugly/handwriting/post-it（促销期 crush）。

**C 级**（ situational/操作复杂）：AI animation、statistics ads（奢侈/零售+awareness 目标非 D2C ROI）、celebrity、AI avatar（法务免责下曾 scale 但正被真实创作者替代）、warehouse、street interview（**伪造/重现常优于实拍**）、duet/reaction/stitch（要原作者授权）、ASMR、regular UGC（**制造感 problem-solution VO+B-roll UGC 普遍疲劳**）。

**D/E/F 级**：breaking-news、AI billboard、GRWM（日常 organic-native 不 scale）/ text-only、testimonial statics（除非金句测评）、listicles（已死）、carousel（汁不值 squeeze）/ **press ads（版权噩梦，Vogue 会找你）、podcast ads（除非创始人上真知名播客）、notes-app/UX fake-native（看着 native 但不转化——UI 太熟悉人人停但筛不出对的人还搞糊涂算法，坚决跳过）**。

**横切原则**：portfolio 不是银弹——只有 founder/partnership/authority/investigation/VSL/grid-static 可靠 scale 冷流量；fake it when honest capture is painful（street interview/duet 可重现别等完美真实瞬间）；**疲劳真实存在**于过度教学格式，新鲜度本身是 edge——新颖但诚实的格式胜过饱和的「最佳实践」。

### 6. 竖屏视频生产规范（9:16 全平台）

**画布**：1080×1920 (9:16)、30fps、MP4；任意分辨率素材 center-crop 填充。

**Safe zone（最常被忽略的约束）**：平台 UI（操作栏/字幕栈/音乐键/账号行）压在视频上——文字和关键画面放边缘会被盖。**跨平台最坏情况安全带**：上 220px、下 500px、左 180px、右 180px → **中央 720×1200 文字安全带（y=220 到 y=1420）**，所有字幕和承重画面必须在带内。大推前用 safe-zone overlay 预览（数字随 app 更新漂移，偶尔复核）。

**字幕配方（经典 TikTok 风）**：白字黑描边无底色 pill=原生感；`paint-order: stroke fill` 保字形锐利；静态字幕（无入场/出场动画——动画字幕读作「品牌制作」）；自动缩字号（~58px 起每次缩 2px 到安全带，地板 ~26px，长 hook 墙是合法输入会自动缩）；字体加载完再量（`document.fonts.ready`）。

**音频决策**：默认静音各 clip 音轨让单条音乐轨承载；结尾 ~0.8s 音乐淡出（硬切静音=坏片）。**有机 vs 烘焙**：organic TikTok/Reels 常**不烘音乐**、在 app 内挂 trending sound——算法奖励原生/热门音频且他人可 attach；付费广告或无法挂原生音的平台**烘进视频**。这一个决策显著影响 organic reach。

**确定性渲染**：无时钟/无随机/无运行时网络请求——同输入同 MP4（Remotion/HyperFrames/ffmpeg 通用）。

### 7. Creator 短视频格式库（结构非剧本）

| 格式 | 级 | 形态 |
|------|----|------|
| Reaction + Demo (hard cut) | A | 创作者 reaction~3s 带 hook 字幕 → **硬切** app demo 全程 ~9-12s；hook 字幕是全部卖点写成内心独白（"i was about to hit it and this app talked me out of it"）非产品宣称；硬切是机制无转场；reaction 真实性是瓶颈 |
| "No Yapping" Split-Screen 教程 | B | 全静音快教程：全屏 intro → 50/50 分屏（输入|实时结果）步骤字幕在接缝处；沉默是卖点（静音观看者+高意向筛选）；字幕承载步骤有序静态 |
| Greenscreen Reaction | A | 全屏视频+创作者抠像叠加边看边评；可从居中 shrink 到角落让内容接管（签名节拍）；双音轨共存（底层视频+创作者声） |
| Yapper | A | 一人对镜讲个人故事落到产品 ~20-60s；开场用故事钩非产品宣称；结构=hook→故事→产品作为转折出现；casting 是瓶颈——错的人比错的剧本更致命 |
| Amateur Investigation | A | 创作者「调查」产品/niche：真实腿活 footage → 产品作为调查结论自然浮现（非赞助位）；怀疑是门槛的品类最强 |
| David & Goliath | A | 品牌=David 对具体反派（臃肿 incumbent/行业乱象）；反派必须真实——制造假反派格式即死 |
| Authority | A | 持证专家（医生/皮肤科/工程师）出镜；信任门槛高 niche（保健品/美妆/受监管）专用；**合规红线**：专家必须真实、宣称必须属实可证，健康/医疗/金融宣称走法务审，绝不虚构资质 |
| VSL | S | 60s-数分钟长视频：problem→mechanism→proof→offer；需教育的品类专用；剧本是广告本体，beat-by-beat 工程化留存（open loops/中段新事实转折） |
| Green-Screen Commentary | A | 创作者在全屏素材上口播教学（区别于 reaction：这是教学叠加非反应）；服装+教育角度强 |

### 8. 写作质量标准（防 AI 痕迹 + 可输的测试假设）

**Test hypotheses that can lose**：概念出厂必须带可证伪假设——「会引起租客共鸣」不能输，「在租客中 CTR 超对照 +15%」能输。写明指标（CTR/CVR/CPA/thumb-stop）+对比对象（哪个对照/兄弟概念、哪个受众）+预期方向+有基线时给幅度。假设要从角度动机推得——赢或输都教你受众什么，不只是素材什么。

**No AI tells**（批量生成会放大任何口头禅）：禁「It's not X, it's Y」对比揭示、禁否定排比「No X, no Y, no Z」、禁尾随堆砌、禁自问自答/冒号揭示、禁 stock phrases（"Say goodbye to"/"reimagined"/"Unlock the power of"）、禁 em dash；广告特有：为塞字符堆叠否定、泛化 hook slop（"POV:"/"Stop scrolling"须 hyper-specific 才成立）、泛化 CTA slop（"Get started today"）。批次内变化句式——十条变体同开头读作生成物。

**角度多样性**：先定 3-5 个不同动机角度再各自产多变体；迭代时赢家主题加深+1-2 个未试新角度+避开输家模式；记录 Iteration Log（轮次/日期/胜者指标/获胜模式/新变体数/新测角度/退役角度）。

### 9. 平台字符规范速查

| 平台 | 元素 | 限制 |
|------|------|------|
| Google RSA | Headline 30 字符×15 / Description 90×4 / 路径 15×2 | 标题须独立成立且任意组合通顺；≥1 关键词向+≥1 利益向+≥1 CTA；pin 位置会降优化 |
| Meta | 主文案 125 可见(2200 上限，hook 前置) / Headline 40 / Description 30 / 链接 40 | |
| LinkedIn | Intro 150(600) / Headline 70(200) / Desc 100(300) | |
| TikTok | Ad text 80(100) / Display name 40 | |
| X | Tweet 280 / Headline 70 / Desc 200 | |

交付前逐条过字符校验，超限给裁剪版。

## 高频问答索引

- **Q：广告 hook 怎么系统化生成，不是拍脑袋？**
  A：管线 Segment→Motivation→Format→Hook 三组件（视觉动作/口播/字幕不重复分工）；输出 hook matrix 跨单元覆盖；动机用客户原话；先选形式再写词。诊断时读漏斗：thumbstop 弱改视觉、hold 弱改 on-ramp(3-15s)、CTR 弱改中段承诺、CVR 弱修落地页一致性。
- **Q：新素材概念怎么排序？先做哪个格式？**
  A：先按证据分级（自家转化广告>客户逐字>竞品 60 天+>有机互动>跨领域>直觉），再问格式是 unicorn scaler（刺穿冷受众）还是 supporting cast（只转化中低漏斗）——S 级 founder content/partnership ads/VSL 优先；Meta 51 格式 S→F 分级完整表见卡。产能校验：按团队真实产能砍 slate。
- **Q：为什么 partnership ads 和 creator 内容在 Andromeda 时代最重要？**
  A：Andromeda 按 persona 定向不按兴趣列表——创作者粉丝=预组装画像种子，partnership ad 从创作者 handle 投放继承该种子让算法向外扩展，是触达净新增受众的第一杠杆；rolling MoM reach 下降=受众饱和信号→部署 creator-fronted 格式。选人按画像重合度不看粉丝数。
- **Q：竖屏广告视频的安全区怎么避开平台 UI？**
  A：1080×1920 画布中央留 720×1200 文字安全带（上 220px/下 500px/左右各 180px——动作栏/字幕栈/音乐键都压在边缘）；字幕白字黑描边无 pill、静态不动画、自动缩字号到带内；有机内容不烘音乐 app 内挂 trending sound 赚算法加权，付费广告烘进视频。
- **Q：AI 批量生成广告文案怎么避免「一看就是 AI」？**
  A：禁对比揭示「It's not X, it's Y」、否定排比、stock phrases、em dash、泛化 hook/CTA；批次内变化句式；测试假设必须可证伪（指名指标+对比对象+预期方向）；每条创意溯源到语料库（评论原话/赢家广告/评论区异议），无来源不进 icebox，语料为空停下来要料不许无 grounding 降级生成。

## 相关卡片

- [meta-quantified-decision-engine.md](../meta-ads-diagnosis/meta-quantified-decision-engine.md) — Meta 量化决策引擎（S25；本卡管投放前素材生产，决策引擎管投放后 kill/keep/scale）
- [tiktok-content-ads-playbook.md](./tiktok-content-ads-playbook.md) — TikTok 内容×广告打法（S22；渠道层 vs 本卡创意工程层）
- [influencer-boost-loop-overview.md](../influencer-boost/influencer-boost-loop-overview.md) — 红人素材加推 Loop（S2；partnership ads 的自家实现路径）
