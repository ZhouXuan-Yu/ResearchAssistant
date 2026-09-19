# 科研技能功能地图与路由规则

> 建立：2026-09-18｜阶段：F4（路由与冲突）｜维护：科研助手（agent-mu42qzfz）
> 目的：让 48 个科研相关技能**各司其职**，消除"该用哪个"的歧义与触发竞争。
> 方法说明：Hana **无原生技能触发遥测**，因此这是**规范级**的路由（描述"应当用哪个"），
> 不是运行时埋点统计。触发竞争通过"显式命名优先 + 组内唯一主选"来压制。

---

## 1. 分类总览（按功能需求）

| 组 | 成员 | 主选 | 备选 |
|---|---|---|---|
| A 选题与立项 | researchwrite、quiet-musing、deep-research | `researchwrite` | `quiet-musing`（复杂权衡时） |
| B 文献检索与获取 | nature-academic-search、nature-literature-pipeline、nature-downloader、nature-citation、deep-research、navi-deep-research | `nature-academic-search`（检索）／`nature-literature-pipeline`（系统综述） | `deep-research` |
| C 文献精读与解析 | nature-reader、nature-paper-card、paper-deep-reading、pdf/docx/doc/office-documents、zotero-pdf-translate | 见 §2-C | |
| D 引用核验 | nature-ref-verifier、nature-citation | `nature-ref-verifier` | `nature-citation`（找支撑） |
| E 统计与绘图 | nature-statistics、scipilot-figure-skill、nature-figure | 统计=`nature-statistics`；数据图=`scipilot-figure-skill`；图形摘要/机制图=`nature-figure` | |
| F 实验与复现 | nature-experiment-log、hana-agent-ops | `nature-experiment-log` | `hana-agent-ops`（环境侧） |
| G 写作与润色 | nature-writing、nature-polishing、researchwrite | 结构=`nature-writing`；语言=`nature-polishing`；计划书=`researchwrite` | |
| H 审稿与返修 | nature-reviewer、academic-paper-reviewer、nature-response | 见 §2-H | |
| I 投稿与数据共享 | nature-data、nature-paper-to-patent、academic-research-suite | `nature-data` | — |
| J 知识组织与记忆 | understand-knowledge、navi-memory、navi-notes、navi-context、obsidian-cli | 见 §2-J | |
| K 演示与汇报 | nature-paper2ppt、nature-image2ppt | 论文=`nature-paper2ppt`；图像=`nature-image2ppt` | |
| L 编排与治理 | academic-research-suite(stub)、hana-agent-ops、skill-creator、luban、token-guard | 见 §2-L | |
| M 通用底座 | pdf、docx、doc、xlsx、office-documents、image-generation、images-media、user-guide、teach | 按格式选 | |

---

## 2. 逐组路由规则

### A 选题与立项
- **要写**计划书/开题/项目申报 → `researchwrite`。
- **只是想清楚**一个问题（多方案权衡、高不确定性）→ `quiet-musing`（推理框架，不是产出器）。
- **要一轮深度调研**形成判断 → `deep-research`。

### B 文献检索与获取
- 单点检索、检索式构造、跨库查 → `nature-academic-search`。
- **系统综述/研究现状全梳理**（需穷尽性与可复现检索策略）→ `nature-literature-pipeline`。
- **合法获取全文**（含机构访问）→ `nature-downloader`。
- 为**某句论断**找支撑文献 → `nature-citation`（与 D 组联动）。
- 规则：**普通检索不进 literature-pipeline**，避免重流程压轻任务。

### C 文献精读与解析（三层，按粒度）
| 需求 | 用 |
|---|---|
| 要一份可读的**中英对照全文** | `nature-reader` |
| 要**结构化精读卡**（方法/证据链/边界/局限） | `nature-paper-card` |
| 只是**快速吃透**一篇、不要正式产物 | `paper-deep-reading` |
| 只是**读文件内容**（PDF/Word） | `pdf` / `docx` / `office-documents`（底座，不是分析） |
- 规则：先看用户要"产物"还是"理解"。要产物走 nature-*，只要理解走 paper-deep-reading。

### D 引用核验
- **批量核验**引用真伪与元数据 → `nature-ref-verifier`。
- **找**能支撑某论断的文献 → `nature-citation`。
- 铁律：未核验的引用不入稿（见 `research/60-writing/references.md`）。

### E 统计与绘图
- 统计表述/p 值/效应量/多重比较审查 → `nature-statistics`。
- **数据图**（折线/柱/散点/箱线/热力/误差棒/多面板，含中文期刊）→ `scipilot-figure-skill`。
- **AI 图形摘要 / 机制示意图 / Nature 系投稿图 / 需 R 后端** → `nature-figure`。
- 规则：同一张图只走一条路，不叠加两个绘图技能。

### F 实验与复现
- 记录实验（可复现的前提）→ `nature-experiment-log`，落到 `research/50-experiments/`。
- 环境/依赖/模型层面的诊断 → `hana-agent-ops`。

### G 写作与润色
- **organize 结构、论证、章节** → `nature-writing`。
- **只改语言，不动术语/数值/结论边界** → `nature-polishing`。
- 计划书写作 → `researchwrite`（与 A 同源，不重复触发）。

### H 审稿与返修（三个不同阶段）
| 阶段 | 用 |
|---|---|
| 投稿前**自审**（主流程） | `academic-paper-reviewer` |
| 想要**独立二次审查**（Nature 视角） | `nature-reviewer` |
| 收到**真实审稿意见**后写回复 | `nature-response` |
- 规则：模拟审稿可同时用前两者（互为独立视角）；**回复**只用 nature-response。

### I 投稿与数据共享
- Data/Code Availability、数据仓储、FAIR → `nature-data`。
- 成果转专利 → `nature-paper-to-patent`。
- `academic-research-suite`：**当前为空壳，不启用其触发**，编排职责留给待建的 `research-os-router`。

### J 知识组织与记忆
- 知识图谱/实体关系分析 → `understand-knowledge`。
- 长期记忆读写 → `navi-memory`。
- 笔记 → `navi-notes`；外部库 → `obsidian-cli`。
- 会议相关（navi-pull-meeting / navi-transcribe / navi-context）→ 仅在会议场景。

### K 演示与汇报
- 论文 → 中文组会 PPT → `nature-paper2ppt`。
- 幻灯片/扫描件图像 → 重建可编辑演示 → `nature-image2ppt`。

### L 编排与治理
- 环境自检/故障诊断 → `hana-agent-ops`。
- 造新技能 → `skill-creator`；打磨已有技能 → `luban`。
- token 优化 → `token-guard`。
- **编排器 `research-os-router`：待建**（见 §5）。

### M 通用底座
- 文档解析按格式选：`.pdf`→`pdf`，`.docx`→`docx`，`.xlsx`→`xlsx`，混合 Office→`office-documents`。
- 生图 → `image-generation`；产品介绍 → `user-guide` / `teach`。

---

## 3. 冲突清单与裁决（F4 核心）

| # | 竞争 | 风险 | 裁决 |
|---|---|---|---|
| C1 | nature-reader vs nature-paper-card vs paper-deep-reading | 都触发"读论文" | 按**产物粒度**分流（§2-C） |
| C2 | nature-academic-search vs nature-literature-pipeline vs deep-research vs navi-deep-research | 都触发"查文献/调研" | 单点=`academic-search`；穷尽综述=`literature-pipeline`；开放调研=`deep-research`；`navi-deep-research` 仅在已用 navi 家族时 |
| C3 | scipilot-figure-skill vs nature-figure | 绘图双触发 | 数据图 vs 图形摘要（§2-E），已在治理清单登记 |
| C4 | nature-writing vs nature-polishing | 都触发"改论文" | 结构 vs 语言；改语言时**不得**顺手改结构 |
| C5 | nature-reviewer vs academic-paper-reviewer | 都触发"审稿" | 阶段不同（§2-H），可并用但用途区分 |
| C6 | nature-paper2ppt vs nature-image2ppt | 都触发"做 PPT" | 文本源 vs 图像源 |
| C7 | nature-citation（B/D 跨组） | 归属模糊 | 归属 D（核验），检索触发时由 B 调起 |
| C8 | pdf vs docx vs office-documents | 都触发"读文档" | 按扩展名选；混合格式用 office-documents |
| C9 | researchwrite 同属 A/G | 双触发 | 归 A；写作阶段不重复调用 |
| C10 | academic-research-suite（空壳） | 误触发、给空指引 | **不主动使用**，待被 research-os-router 取代 |

**压制触发竞争的总原则**：
1. **用户显式命名优先**——用户点名哪个就用哪个。
2. **组内唯一主选**——同组默认只走主选。
3. **不叠加**——同类产物不叠加两个技能（尤其绘图、润色）。
4. **有歧义先问**——无法判断粒度/阶段时，先确认再动手。

---

## 4. 任务 → 技能速查（意图 → 唯一入口）

| 用户怎么说 | 走 |
|---|---|
| 帮我查一下 XX 的文献 | nature-academic-search |
| 做一份 XX 的系统综述 | nature-literature-pipeline |
| 把这篇 PDF 做成中英对照 | nature-reader |
| 精读这篇，出结构化卡片 | nature-paper-card |
| 核一下这些引用是不是真的 | nature-ref-verifier |
| 审一下我论文的统计 | nature-statistics |
| 把这组数据画成论文图 | scipilot-figure-skill |
| 做个图形摘要 | nature-figure |
| 记一下这次实验 | nature-experiment-log |
| 润色这段（别改数字） | nature-polishing |
| 帮我搭论文结构 | nature-writing |
| 从审稿人视角评估这篇 | academic-paper-reviewer（+ nature-reviewer 二次） |
| 根据审稿意见写回复 | nature-response |
| 写数据可用性声明 | nature-data |
| 做成组会汇报 PPT | nature-paper2ppt |
| 环境/记忆出问题了 | hana-agent-ops |

---

## 5. 与待建 `research-os-router` 的关系

本文件是 `research-os-router` 的**规格来源**。路由器将承担：
1. **意图识别** → 查 §4 速查表 → 定唯一入口。
2. **阶段门禁** → 例如投稿前强制过统计审查与引用核验。
3. **质量门禁** → 结论必须标 F/L/I/U；引用未核验不得入稿。
4. **状态记录** → 把任务状态写进 `research/`。

机器可读规则见同目录 `routing-rules.yaml`。

---

## 6. 未覆盖的缺口（与缺口报告一致）

- **实验设计 / 统计功效 / 投稿格式模板**：无技能覆盖，属计划中"无上游"项。
- **智能体工程**：无技能覆盖（`hana-agent-ops` 只覆盖运维侧）。
- 这两块是 `research-os-router` 建成后需要考虑自建或补源的方向。
