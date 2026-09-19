# 🗂️ HanaAgent 技能索引

> 超级AI个体 · 全栈编程 + UI设计 + 项目规划
> 最后更新：2026-09-19 · 总计 136 个技能（索引 137 行条目；`code-tour` 跨支援层 S1 / 参考层 R2 重复列示。2026-09-16 新增科研技能 22 项；2026-09-18 新增 scipilot-figure-skill、自建 hana-agent-ops、research-os-router；2026-09-19 新增自建 idea-forge、平台技能 character-creator）

---

## 📖 使用说明

### 分层逻辑

| 层级 | 含义 | 何时查 |
|------|------|--------|
| 🔥 **核心层** | 每次编程/设计/规划任务必须过脑的技能 | 每次都查 |
| ⚡ **支援层** | 高频但非每次都用 | 任务开始时查 |
| 📚 **参考层** | 特定场景偶尔用 | 场景触发时查 |
| 🗄️ **归档层** | 已弃用或几乎不用 | 基本不查 |

### 怎么用这个索引

1. **接到任务** → 先扫 🔥核心层,确认哪些适用
2. **初步规划** → 查 ⚡支援层,匹配子任务
3. **遇到特定场景** → 查 📚参考层
4. **不确定有没有对应技能** → 按 `Ctrl+F` 搜关键词

### 分类图标

| 图标 | 领域 | 说明 |
|------|------|------|
| 🔧 | 编程开发 | 写代码、review、架构、重构 |
| 🎨 | UI/UX设计 | 界面、组件、色彩、排版、动效 |
| 📋 | 项目规划 | 需求澄清、任务拆解、团队协作 |
| 📄 | 文档办公 | 读/写 Word、Excel、PPT、PDF |
| 🧪 | 测试质量 | 测试、验证、上线审计 |
| 🧠 | Agent元技能 | 自我调试、学习、上下文管理 |
| 🏢 | 业务设计 | 品牌、用户旅程、落地页 |
| 📚 | 学习知识 | 论文阅读、持续学习 |

---

## 🔥 核心层(每次任务必考虑)

> 这些技能覆盖了「接到需求→分析→设计→编码→测试→交付」全链路。每次任务至少浏览一遍,确认哪个阶段需要启用。

### 🔧 编程开发

| # | 技能名 | 一句话 | 什么时候用 | 关键词 |
|---|--------|--------|-----------|--------|
| C1 | `code-review-excellence` | 多语言代码审查,含 React/Vue/Angular/Rust/Go/Python/Java 等 | 审查 PR、review 代码、架构评审 | review, PR, 代码审查, pull request |
| C2 | `code-simplifier` | 简化代码,保留功能的同时提高可读性和一致性 | 重构、消除冗余、提升代码清晰度 | simplify, 简化, refactor, 重构 |
| C3 | `error-handling` | TS/Python/Go 三语言的错误处理模式 | 设计错误类型、加重试逻辑、统一 API 错误响应 | error, try-catch, retry, 错误处理 |
| C4 | `karpathy-guidelines` | Karpathy 的 LLM 编码行为准则:先想再写、极简、手术式修改 | 写新代码、重构、审查时自我约束 | think first, simplicity, surgical, 极简 |
| C5 | `codex-ralph-loop` | 循环执行直到完成,每轮 Plan→Act→Check→Fix | 复杂多步任务、需要持续迭代直到通过 | loop, iterate, 循环, 持续, 直到完成 |
| C6 | `tdd-workflow` | 测试驱动开发,80%+覆盖率 | 写新功能、修 bug、重构 | TDD, test first, 测试驱动, red-green-refactor |
| C7 | `andrej-karpathy-skills` | Karpathy LLM编码行为准则合集,减少常见错误 | 写代码、审查、重构时自我约束 | karpathy, coding, 约束, 准则 |

### 🎨 UI/UX设计

| # | 技能名 | 一句话 | 什么时候用 | 关键词 |
|---|--------|--------|-----------|--------|
| D1 | `frontend-design` | 八大美学锚点(Swiss/Industrial/Brutalist等),锁定CSS令牌 | 设计新页面、选视觉风格 | design, style, aesthetic, 美学, 风格 |
| D2 | `ui-ux-pro-max` | 50+风格/161调色板/57字体配对/99条UX指南 | 设计决策需要参考数据库时 | color, font, typography, style, 配色, 字体 |
| D3 | `ui-design` | 布局、组件、视觉层级、网格系统 | 构建界面、建立设计系统 | layout, grid, hierarchy, 布局, 网格 |
| D4 | `component-patterns` | 现代UI组件模式:复合组件、设计令牌、变体系统 | 设计/实现组件库 | component, token, variant, 组件, 令牌 |
| D5 | `responsive-design` | 移动优先、断点、流式布局、Container Queries | 做响应式布局 | responsive, mobile, breakpoint, 响应式 |
| D6 | `web-typography` | 字体选择/配对/排版比例/行高/流式文字 | 选字体、定义排版系统 | font, typography, type scale, 排版 |

### 📋 项目规划

| # | 技能名 | 一句话 | 什么时候用 | 关键词 |
|---|--------|--------|-----------|--------|
| P1 | `requirements-architect` | 苏格拉底式追问澄清需求,产出架构文档 | 项目启动、需求模糊时 | 需求, 架构, 系统设计, MVP |
| P2 | `planning-with-files` | Manus风格文件规划:task_plan/findings/progress | 复杂多步任务 | plan, planning, 规划, 拆解, 任务 |
| P3 | `agent-teams-playbook` | 多Agent协作编排手册,6阶段工作流 | 需要多个子Agent并行协作 | 多agent, swarm, 分工, team, 团队 |
| P4 | `council` | 四角色决策委员会(架构师+怀疑者+实用主义+批评者) | 决策模糊、多方案选择 | decide, tradeoff, go/no-go, 决策 |

### 🧪 测试质量

| # | 技能名 | 一句话 | 什么时候用 | 关键词 |
|---|--------|--------|-----------|--------|
| T1 | `verification-loop` | 全面验证:构建→类型检查→测试→Lint→打包→安全 | 完成功能/重构后、提PR前 | verify, build, test, lint, 验证 |
| T2 | `ai-regression-testing` | AI辅助开发的回归测试:沙箱API测试、bug检查工作流 | AI改代码后的回归测试 | regression, sandbox, bug-check, 回归 |
| T3 | `e2e-testing` | Playwright E2E、POM、CI/CD集成、flaky策略 | 写端到端测试 | Playwright, e2e, POM, 端到端 |

### 🧠 Agent元技能

| # | 技能名 | 一句话 | 什么时候用 | 关键词 |
|---|--------|--------|-----------|--------|
| M1 | `agent-introspection-debugging` | Agent自调试四阶段:捕获→诊断→恢复→报告 | Agent反复失败、死循环 | debug, self-debug, loop, 自调试 |
| M2 | `strategic-compact` | 在逻辑边界手动压缩上下文,而非自动随机压缩 | 长会话、多阶段任务 | compact, context, 压缩, 上下文 |
| M3 | `superpower` | 技能调用框架,强制先查技能再回复 | 每次对话开始 | skill, superpower, 技能 |

---

## ⚡ 支援层(高频按需调用)

> 按具体任务场景匹配,不必每次都查。

### 🔧 编程开发

| # | 技能名 | 一句话 | 什么时候用 |
|---|--------|--------|-----------|
| S1 | `code-tour` | 创建 CodeTour 引导文件,用于代码走读 | 新人入职、架构讲解、PR走读 |
| S2 | `agent-sort` | 按项目实际栈分类技能为 DAILY/LIBRARY | 新项目安装ECC技能时 |
| S3 | `configure-ecc` | ECC 交互式安装向导 | 安装 ECC 技能/规则 |
| S4 | `plankton-code-quality` | 写时代码质量:保存即自动格式化+Lint+AI修复 | 设置代码质量自动检查 |
| S5 | `hookify-rules` | 创建模式匹配的 hook 规则 | 需要自动触发规则时 |
| S6 | `hyperframes` | HTML视频合成框架:创建视频合成、动画、标题卡、叠加层、字幕、配音等 | 创建HTML驱动的视频内容 |
| S7 | `three` | Three.js和WebGL适配器模式,用于HyperFrames的确定性3D场景渲染 | 创建3D视频合成 |
| S8 | `typegpu` | TypeGPU和WebGPU适配器模式,用于HyperFrames的GPU渲染合成 | 创建GPU加速的视频合成 |
| S9 | `css-animations` | CSS动画适配器模式,用于HyperFrames的确定性CSS关键帧动画 | 创建CSS动画效果 |
| S10 | `gsap` | GSAP动画参考,用于HyperFrames的复杂时间线动画 | 创建GSAP动画效果 |
| S11 | `hyperframes-media` | HyperFrames媒体预处理:文本转语音、音频转写、背景移除 | 为视频合成生成媒体资源 |
| S11b | `hookprompt` | 钩子提示词模式,自动化触发与响应 | 需要自动触发提示词时 | hook, prompt, 钩子, 自动 |

### 🎨 UI/UX设计

| # | 技能名 | 一句话 | 什么时候用 |
|---|--------|--------|-----------|
| S12 | `ui-patterns` | 真实产品中的 UI 交互模式:Hero/导航/卡片/定价/CTA/表单/Footer | 设计具体UI元素时 |
| S13 | `color-theory` | 色彩理论:调色板/对比度/色彩心理学/暗色模式/60-30-10 | 配色调色 |
| S14 | `design-trends` | 2026 Q1/Q2 获奖设计趋势 | 设计对标时 |
| S15 | `visual-direction` | 当前视觉方向:调色板、字体配对、布局组合 | 确定视觉语言 |
| S16 | `images-media` | 图片策略/优化/SVG/图标/懒加载 | 处理图片和媒体 |
| S17 | `navigation-design` | 菜单/面包屑/搜索/信息架构 | 设计导航结构 |
| S18 | `accessibility` | WCAG 2.1 AA 无障碍标准 | 无障碍合规 |
| S19 | `usability` | Nielsen启发式评估/表单/错误/转化优化 | 可用性评估 |
| S20 | `ux-design` | 用户研究/交互模式/信息架构/五层模型 | UX整体设计 |
| S21 | `ai-design-workflow` | AI融入设计流程的结构化提示词 | 用AI辅助设计 |
| S22 | `landing-pages` | 落地页设计/CTA/首屏/AB测试 | 做落地页 |
| S23 | `webdesign-review` | 设计评审元技能:协调所有设计域技能 | 做设计全面评审 |
| S24 | `image-generation` | AI生成位图:照片/插图/纹理/Mockup | 需要生成图片素材 |
| S25b | `waapi` | Web Animations API适配器:原生浏览器关键帧动画 | 创建轻量级DOM动画、避免GSAP依赖 |

### 📄 文档办公

| # | 技能名 | 一句话 | 什么时候用 |
|---|--------|--------|-----------|
| S25 | `docx` | 读/写/编辑 Word 文档 | 处理 .docx 文件 |
| S26 | `xlsx` | 读/写/编辑 Excel 电子表格 | 处理 .xlsx/.csv 文件 |
| S27 | `pptx` | 读/写/编辑 PowerPoint | 处理 .pptx 文件 |
| S28 | `pptx-generator` | 从零生成 PPT(PptxGenJS) | 生成演示文稿 |
| S29 | `ppt-master` | AI驱动PPT创建,含图表/布局/品牌模板 | AI辅助做PPT |
| S30 | `pdf` | PDF处理:读/合并/拆分/旋转/水印/OCR | 处理 .pdf 文件 |
| S31 | `office-documents` | Office文档通用处理 | 读/改 PDF/Word/Excel/PPT |

### 🧪 测试质量

| # | 技能名 | 一句话 | 什么时候用 |
|---|--------|--------|-----------|
| S32 | `eval-harness` | 评估框架:capability/regression evals, pass@k | 评估AI开发质量 |
| S33 | `production-audit` | 生产就绪审计:认证/数据/错误/性能/安全 | 上线前检查 |
| S34 | `webapp-testing` | Playwright 本地 Web App 测试 | 测试本地前端 |
| S35 | `windows-desktop-e2e` | Windows桌面应用E2E(pywinauto/UIA) | 测试WPF/WinForms/Qt |
| S36b | `gstack` | 无头浏览器QA测试:截图/交互/验证/响应式测试 | 网站测试、部署验证、bug报告 |

### 🏢 业务设计

| # | 技能名 | 一句话 | 什么时候用 |
|---|--------|--------|-----------|
| S36 | `branding-identity` | 品牌策略/视觉识别/定位 | 品牌设计 |
| S37 | `customer-journey` | 用户画像/触点映射/旅程阶段模型 | 用户旅程分析 |
| S38 | `design-process` | 设计流程七步骤:简报→概念→线框图→视觉→原型→评审→交付 | 管理设计项目 |
| S39 | `website-audit` | 网站系统分析/改版规划/SEO迁移/内容审计 | 网站改版 |
| S40 | `lark-approval` | 飞书审批:查询与处理待办审批任务，覆盖待本人审批的任务与本人发起的实例 | 处理飞书审批任务 |
| S41 | `wecomcli-contact` | 企业微信通讯录成员查询，获取当前用户可见范围内的通讯录成员，支持按姓名/别名筛选 | 查询企业微信通讯录 |
| S42b | `tmeet-skill` | 腾讯会议CLI:OAuth登录/会议管理/录制转写/问题排查 | 腾讯会议操作、会议录制管理 |

### 🧠 Agent元技能

| # | 技能名 | 一句话 | 什么时候用 |
|---|--------|--------|-----------|
| S42 | `iterative-retrieval` | 渐进式上下文检索,解决子Agent上下文问题 | 子Agent需要分批获取上下文 |
| S43 | `meta-theory` | 可执行治理调度器:意图分类→证据收集→验证 | 治理/重构/多文件/跨模块 |
| S44 | `continuous-learning-v2` | 本能式学习系统:confidence评分+项目隔离 | 从会话中自动学习 |
| S45 | `skill-scout` | 创建新技能前先搜索是否已有 | 想创建新技能时 |
| S46 | `skill-stocktake` | 审计已安装技能的质量 | 定期清理技能库 |
| S47 | `find-skills` | 搜索开源技能市场 | 需要找新技能 |
| S48 | `luban-skill` | 专门升级Skill的Skill,质量评估与优化 | 升级优化现有Skill |
| S48b | `ralph-loop` | 自引用循环直到任务完成,含架构师验证 | 需要持续迭代直到通过 | loop, iterate, 循环, 持续 |
| S48c | `codex-ralph-loop-skill` | Codex版迭代循环:Plan→Act→Check→Fix | Codex环境下的持续迭代 | codex, loop, iterate, 循环 |
| S49 | `pm-skills` | 产品经理技能集合,68个PM技能和42个工作流 | 产品经理工作流 |
| S50 | `quiet-musing` | 深度推理框架:多步骤/高不确定性/权衡决策 | 复杂问题深度思考 |
| S51 | `teach` | 多会话状态化学习,基于 ZPD 理论自动调难度,文件系统持久化学习进度 | 学新框架/新概念/新技能 |
| S52 | `caveman` | 极简通信模式,砍掉 75% 废话 token 保留完整技术精度 | 长会话 token 膨胀时、快速技术问答 |
| S53 | `grill-me` | 一次一问的决策树追问,直到方案每个分支都对齐 | 压力测试方案、快速对齐设计决策 |
| S54 | `token-guard` | Token优化守卫:自动压缩输出、优化工具调用、管理上下文膨胀 | 优化token使用，减少上下文膨胀 |
| S55 | `langfuse-deploy` | Langfuse LLM观测平台部署指南:Docker部署/SDK使用/问题排查 | 部署LLM监控系统、追踪AI调用 |
| S56 | `hana-agent-ops` | 自建环境运维：健康自检/模型链路诊断/记忆故障定位/技能治理与冒烟/备份回滚/凭据权限核查 | 环境自检、模型不通、记忆不工作、技能装不上、配置漂移 |
| S57 | `research-os-router` | 自建科研主编排器：意图→功能组→唯一入口的路由、跨阶段编排、质量门禁(G1-G5)、新技能准入分类校验 | 判断科研任务该用哪些技能、跨环节编排、投稿前检查、新技能归哪一类 |

---

## 📚 参考层(特定场景触发)

| # | 技能名 | 一句话 | 适用场景 |
|---|--------|--------|----------|
| R1 | `agent-ui-design` | 聊天界面/Agent UX/流式渲染/工具可视化 | 设计 AI Agent 前端界面 |
| R2 | `code-tour` | CodeTour .tour 文件 | 代码引导 walkthrough |
| R3 | `humanizer` | 去除AI写作痕迹 | 润色AI生成的文字 |

### 📚 学习/知识

| # | 技能名 | 一句话 | 适用场景 |
|---|--------|--------|----------|
| R4 | `paper-deep-reading` | 学术论文深度阅读 | 读论文 PDF |
| R5 | `academic-research-suite` | 学术研究全流程 | 文献搜索/论文分析/引用管理 |

### 📚 YouNavi 套件

| # | 技能名 | 一句话 | 适用场景 |
|---|--------|--------|----------|
| R6 | `navi-deep-research` | YouNavi深度研究 | 主题深度研究 |
| R7 | `navi-notes` | YouNavi笔记 | 记录/查看笔记 |
| R8 | `navi-pull-meeting` | YouNavi会议拉取 | 获取会议录音 |
| R9 | `navi-transcribe` | YouNavi音频转写 | 转写音频 |
| R10 | `navi-context` | 同步YouNavi用户上下文（记忆、最近会话、会议）到当前agent | 了解用户背景和最近活动 |
| R11 | `navi-memory` | 读取或更新YouNavi记忆文件 | 记住重要信息，更新记忆 |

### 📚 Understand 系列

| # | 技能名 | 一句话 | 适用场景 |
|---|--------|--------|----------|
| R12 | `understand` | 代码库知识图谱 | 分析项目架构 |
| R13 | `understand-chat` | 基于知识图谱的代码问答 | 理解代码库 |
| R14 | `understand-dashboard` | 知识图谱可视化面板 | 可视化架构 |
| R15 | `understand-diff` | Git Diff 影响分析 | PR审查 |
| R16 | `understand-domain` | 业务领域知识提取 | 理解业务逻辑 |
| R17 | `understand-explain` | 深度解释文件/函数/模块 | 理解具体代码 |
| R18 | `understand-onboard` | 生成新人入职指南 | 新人入职 |
| R19 | `understand-knowledge` | 分析Karpathy模式LLM知识库，生成交互式知识图谱 | 分析知识库结构 |
| R19b | `findskill` | 搜索并安装Agent技能 | 用户询问如何做某事时 | find, skill, 搜索, 安装 |

### 📚 其他

| # | 技能名 | 一句话 | 适用场景 |
|---|--------|--------|----------|
| R20 | `obsidian-cli` | Obsidian CLI | 操作 Obsidian 笔记 |
| R21 | `find-skills-windows` | Windows 版本技能搜索 | Windows 环境搜索技能 |

### 📚 科研技能（nature-skills 20 项 + ARS 2 项，2026-09-16 安装；scipilot-figure-skill，2026-09-18 安装；自建 idea-forge，2026-09-19 安装）

> 本表仅作查找索引；版本、固定提交、许可、依赖与回滚信息的唯一权威登记处是工作台根目录 `SKILLS-GOVERNANCE.md`。

| # | 技能名 | 一句话 | 适用场景 |
|---|--------|--------|----------|
| R22 | `nature-academic-search` | 多源文献检索、引文核对、MeSH 策略与引用影响力审计 | 找文献、核对引用 |
| R23 | `nature-citation` | 为稿件论断匹配并核验 Nature/CNS 系列支撑文献 | 分段补引用 |
| R24 | `nature-ref-verifier` | 参考文献多源交叉验证，逐字段比对作者/年份/卷期/页码 | 论文/开题报告参考文献校验 |
| R25 | `nature-downloader` | 合法获取全文：OA、出版商 API、CNKI 机构访问、补充材料 | 下载论文全文 |
| R26 | `nature-literature-pipeline` | 自动文献发现管线：多源检索→评分→精读→交付→归档 | 系统化文献追踪 |
| R27 | `nature-reader` | 生成中英对照、图文表公式对齐的论文阅读器 | 全文翻译、精读 |
| R28 | `nature-paper-card` | 单篇论文精读卡：方法拆解、证据链、局限与想法 | 论文精读卡 |
| R29 | `nature-writing` | 从作者自有证据起草或重构手稿论证与章节 | 论文写作、首投材料 |
| R30 | `nature-polishing` | 学术文本润色、翻译、精简，保留事实与术语边界 | 论文润色、学术翻译 |
| R31 | `nature-response` | 审稿意见逐点回复、返修信、标注稿修订 | 返修、rebuttal |
| R32 | `nature-reviewer` | Nature 风格模拟审稿：重要性、有效性、major/minor | 投稿前自审 |
| R33 | `nature-statistics` | 审查或改进稿件统计报告：实验单元、重复、不确定度、检验 | 统计审查、图注统计 |
| R34 | `nature-figure` | Python/R 论文配图创建、修订、审计与导出 | 科研绘图、多面板图 |
| R35 | `nature-data` | 起草或审计 Data/Code Availability 声明与 FAIR 元数据 | 数据可用性声明 |
| R36 | `nature-experiment-log` | 由图片/语音/文字生成带 frontmatter 的实验日志 | 实验记录（可选飞书/Obsidian） |
| R37 | `nature-paper2ppt` | 由论文或笔记生成中文学术 PPTX，含原图与讲者备注 | 组会/答辩 PPT |
| R38 | `nature-image2ppt` | 把截图/扫描 PDF/图片型 PPTX 还原为可编辑 PPT | 图片转可编辑 PPT |
| R39 | `nature-paper-to-patent` | 由论文或发明材料生成中文专利交底书与申请稿 | 专利撰写 |
| R40 | `researchwrite` | 研究计划、开题报告、项目申请书的撰写与审校 | 写开题/申请 |
| R41 | `nature-shared` | Nature 套件内部共享引用包，供其他技能按需加载 | 不单独调用，属依赖项 |
| R42 | `academic-paper-reviewer` | 多视角论文评审：5 席位角色分离评审组 | 预投稿审查 |
| R43 | `deep-research` | 13-Agent 深度研究管线，8 种模式（含系统综述） | 通用深度研究 |
| R44 | `scipilot-figure-skill` | 数据图绘制：先剖析数据、判断图型，再出图；覆盖 Nature/Science/IEEE/Elsevier/PNAS 及中文期刊，支持 PDF/SVG/PNG/灰度导出 | 折线/柱/散点/箱线/热力/误差棒/分布/相关矩阵/多面板等纯数据图；与 `nature-figure` 分工见 SKILLS-GOVERNANCE.md |
| R45 | `idea-forge` | 自建 S1 选题与新颖性判定：候选研究问题生成、新颖性 rubric、可行性三筛、falsifier 书写；纯指令无脚本，产出 `idea_options.md` / `novelty_check.md` | 选题、判断想法是否新颖、研究问题筛选（阶段契约见 `research/00-governance/contracts.md`）|

---

## 🗄️ 归档层

| # | 技能名 | 说明 | 原因 |
|---|--------|------|------|
| A1 | `continuous-learning` | v1 会话模式提取 | 已有 v2 替代 |
| A2 | `hana-plugin-creator` | Hana 插件开发 | 平台专属,非通用 |
| A3 | `user-guide` | HanaAgent 用户说明书 | 平台专属 |
| A4 | `skill-creator` | 技能创建器(系统内置) | 系统默认可用 |
| A5 | `character-creator` | 角色创建向导:采访→人格底座→技能→头像→角色卡打包 | 平台专属,默认未启用 |

---

## 🗺️ 任务场景速查

### "我要写一个新功能"
→ `requirements-architect` → `planning-with-files` → `karpathy-guidelines` → `tdd-workflow` → `codex-ralph-loop` → `verification-loop`

### "我要设计一个页面"
→ `frontend-design` → `ui-ux-pro-max` → `ui-design` → `component-patterns` → `responsive-design` → `web-typography` → `color-theory` → `webdesign-review`

### "我要审查一段代码"
→ `code-review-excellence` → `code-simplifier` → `error-handling` → `ai-regression-testing`

### "我要启动一个新项目"
→ `requirements-architect` → `planning-with-files` → `council`(如有决策卡点) → `agent-teams-playbook`(如需要多Agent协作)

### "我要重构代码"
→ `karpathy-guidelines` → `code-simplifier` → `tdd-workflow` → `verification-loop`

### "我要做生产上线"
→ `production-audit` → `verification-loop` → `e2e-testing` → `error-handling`

### "我要做个PPT/文档"
→ `pptx-generator` / `docx` / `xlsx` → `ppt-master` → `pdf`

### "我要做产品经理工作"
→ `pm-skills`(/discover, /strategy, /write-prd, /plan-launch, /north-star) → 如需优化现有PM技能 → `luban-skill`

### "我要做科研/写论文"
→ `research-os-router`(先路由：判功能组/排阶段/过质量门禁) → `idea-forge`(S1 选题与新颖性判定) → `nature-academic-search`(找文献) → `nature-reader`/`nature-paper-card`(精读) → `nature-writing`(起草) → 图表：数据图/中文期刊用 `scipilot-figure-skill`、机制图/Nature 系用 `nature-figure`，统计用 `nature-statistics` → `nature-polishing`(润色) → `nature-reviewer`/`academic-paper-reviewer`(自审) → `nature-response`(返修)；研究计划用 `researchwrite`，通用深研用 `deep-research`

### "AI卡住了/循环了"
→ `agent-introspection-debugging` → `strategic-compact` → `iterative-retrieval`

### "环境不对/看不到图/记不住/技能没生效"
→ `hana-agent-ops`(先跑 `health_check.py` 自检，再按诊断剧本 A–F 定位) → 必要时 `agent-introspection-debugging`

---

## 🔄 索引维护约定

### 添加新技能的流程

1. 安装技能到 `C:\Users\ZhouXuan\.hanako\skills\`
2. 在本文件中找到对应层级和分类位置
3. 按表格格式添加一行
4. 如果技能值得加入「场景速查」,更新对应链路
5. 更新页首的「最后更新」日期

### 格式约定

```
| 编号 | `技能名` | 一句话描述 | 什么时候用/适用场景 |
```

编号规则:
- `C1-Cn` 🔧 核心编程
- `D1-Dn` 🎨 核心设计
- `P1-Pn` 📋 核心规划
- `T1-Tn` 🧪 核心测试
- `M1-Mn` 🧠 核心元技能
- `S1-Sn` ⚡ 支援层
- `R1-Rn` 📚 参考层
- `A1-An` 🗄️ 归档层

### 定期维护

- **每周**:检查是否有新技能可以升级(参考→支援、支援→核心)
- **每月**:清理归档层,删除超过3个月未使用的技能
- **安装新技能时**:立刻加入索引,否则不装

---

> 索引在手,遇事不慌。先查索引,再动手。
>
> ## 📌 各平台 Skills 存放路径速查
>
> | 平台 | 路径 |
> |------|------|
> | **HanaAgent** | `C:\Users\ZhouXuan\.hanako\skills\` |
> | **Codex** | `C:\Users\ZhouXuan\.codex\skills\` |
> | **Claude Code** | `C:\Users\ZhouXuan\.claude\skills\` |
> | **OpenClaw** | `C:\Users\ZhouXuan\.openclaw\skills\` |
| **Hermes** | `C:\Users\ZhouXuan\.hermes\skills\` |
>
> 安装新技能时,四个目录都要同步。
