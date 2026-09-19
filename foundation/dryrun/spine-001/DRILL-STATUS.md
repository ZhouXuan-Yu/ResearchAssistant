# 演练闸门第二轮状态（spine-001 · 评审修订后）

| 项 | 值 |
|---|---|
| 阶段 | Foundation Stage / 演练闸门（步骤 3）+ 独立评审（步骤 1） |
| 日期 | 2026-09-19 |
| 执行者 | 科研助手（agent-mu42qzfz） |
| 演练材料 | 公开通用主题（高效视觉 Transformer），**非用户研究方向** |
| 本轮性质 | 修复门控契约缺陷 + 落地独立盲评 + 按评审批次修订 |

---

## 1. 本轮修复清单（每条含根因与证据）

| # | 问题 | 根因 | 处置 | 证据 |
|---|---|---|---|---|
| F1 | `citation_quality_audit` 读到 0 条、判 FAIL | 支撑库表只有 4 列，脚本要求 ≥6 列且列名可识别 | 重建为 11 列（candidate id / reference / year / recency / supports section / support claim sentence / why this paper fits / source / source channel / verified / verification note） | 审计由 0 条 → **25 条、18 条核验通过、88/100 PASS** |
| F2 | `writing_rationale_matrix` 被报"缺表/表太薄" | 缺 8 个契约列、行数不足、终检列未以 PASS/FAIL 开头 | 重建为 8 行 × 8 列，逐格补足论证，终检列以 PASS 开头 | artifact_check 该文件相关条目**全部消失** |
| F3 | `structured_review.md` 缺失（artifact_check Missing） | 独立评审未做 | 派发独立子代理盲评并落盘；同时由脚本产出评审骨架 | Missing 列表为空 |
| F4 | `figure_body_contract.json` 9 项不符 | 契约缺 11 个镜像字段，asset/source 写成字符串而非带 sha256 的对象 | 由 `figure_requests.json` 镜像重建并写入真实 sha256 | 契约相关条目**全部消失** |
| F5 | 图 1(c)"披露完备度"与证据库冲突（无一条同时给出三项，却被标为"完整 3 条"） | 分类为手工标定，无逐条台账 | **重新取回 6 条带摘要记录的摘要**，建立 E-A 逐条台账，按台账重绘图 1(c) | 实测：参数量 3 条 / 算力 1 条 / 精度 3 条 / **三项俱全 0 条** / 仅定性 2 条 |
| F6 | 评审发现的稿件内部不一致（16 vs 18、缺 GAP-4、标题年份、载体计数、依赖标注等） | 生成阶段的手工标定错误 | 逐条修订 manuscript 与 5 个伴随台账文件 | 见第 3 节映射 |

---

## 2. 门控前后对比

| 脚本 | 本轮前 | 本轮后 | 变化 |
|---|---|---|---|
| `artifact_check.py` | FAIL（Missing: structured_review.md；内容问题 6） | FAIL（Missing: 无；内容问题 **3**） | 内容问题由 6 降到 3，且 3 条同源 |
| `citation_bank_check.py` | PASS | PASS（25 行 / 24 唯一源） | 无变化 |
| `citation_quality_audit.py` | **FAIL（0 条 / 0 分）** | **PASS（25 条 / 18 核验 / 88 分）** | **修复** |
| `contribution_check.py` | PASS | PASS | 无变化 |
| `results_validation_check.py` | PASS（7/7） | PASS（7/7） | 无变化 |
| `figure_story_check.py` | FAIL（5 项） | FAIL（3 项） | 链路类 2 项已消除 |
| `figure_reference_check.py` | FAIL（1 项） | FAIL（1 项） | 无变化（同一条） |
| `visual_readiness_check.py` | FAIL | FAIL（项数增加） | 见第 3 节 V1/V2 |
| `usage_ledger.py` | UNAVAILABLE 但通过诚实检查 | 同 | 无变化 |
| `integrity_audit.py` | 5 项 | 5 项 | 无变化 |

---

## 3. 仍未关闭项（逐条说明为什么本轮关不掉）

| # | 项 | 性质 | 为什么本轮关不掉 | 需要什么 |
|---|---|---|---|---|
| Q1 | `citation_support_bank` 未达 60 行 / 60 唯一源 / 48 近期源 | **上游脚本与自身方法文档冲突** | 脚本内置回退 target=20 → 3x=60；但 `references/citation-support-bank.md` 明写"a fixed multiple of the final citation count is not a completion requirement"，`references/citation.md` 称 `CLOSED_CORPUS_EXHAUSTIVE` 是"a legacy checker marker ... not another host writing gate"。且本演练未指定载体，无解析目标，`citation_bank_check` 自报"coverage not assessed"。 | 用户决策：扩检到 60 源 / 声明演练语料为封闭集 / 记录 `SOURCE_COVERAGE_BLOCKED` 并接受 FAIL。**本轮不填数、不复制行。** |
| Q2 | `figures[0].reference_plan binding is required` | **上游遗留契约** | `references/figure-story.md` 明写该字段属"Legacy compatibility: explicit historical Runner/PaperFigure maintenance only"。补一个空的 reference_plan 只为过检查，属伪造 attestation 链。 | 用户决策：接受性偏差登记 / 若确有参考式制图计划则补真实绑定。 |
| V1 | 目视门未通过（无逐页收据、无渲染页） | **环境能力缺口** | 本机无 poppler（`pdfinfo`/`pdftoppm`）与 PyMuPDF，无法渲染 PDF 页做目视；**未写任何目视 PASS**。 | 安装 poppler（外部二进制，需用户确认）后 `--prepare` 并真实逐页目视。 |
| V2 | "PDF / main.tex / 图资产在检查后发生变化" | 本轮修订的**预期后果** | 本轮重出了交付面与图，manifest 里记录的是修订前的哈希。 | 做完 V1 的真实逐页检查后同步刷新 manifest。 |
| E4 | 正文未按 `fig:evidence-landscape` 标签引用 | 渲染约定 | 图已在正文以"图 1"引用并嵌入；LaTeX 面已可由 pandoc 生成 `\label`。脚本要求正文出现该标签串，属 LaTeX 交叉引用约定，在无 TeX 引擎时无实际作用。 | 若需严格满足，可在正文插入显式标签锚点并再重出一次。 |
| T-ENV | 无 TeX 发行版；`office_html-to-pdf` 打包缺 `new-warm-paper-fonts.css`；无 poppler | **环境缺口** | 前者使 LaTeX 面不可编译；中者已用 Edge headless 绕行；后者阻塞目视门。 | 环境侧决策（安装体积大，需用户确认）。 |
| R1 | 修订后需**再评审一轮** | 流程要求 | 独立盲评的对象是**修订前**版本；修订改变了稿件内容。 | 对修订版再派发一次独立盲评。 |
| R2 | `reference_inventory.py` 会覆盖 `reference_materials/source_index.md` | **本轮新发现的脚本副作用** | 该脚本把 `source_index.md` 当自己的输出路径，运行即覆盖为输出目录清单；本轮已恢复书目表并把冲突写入文件首部。 | 把书目迁到工具不占用的文件名，或把该脚本移出常规门控串。 |

---

## 4. 独立盲评（步骤 1）结果摘要

- 评审者：独立子代理（只读，未修改任何文件），评审对象为 4 份文件。
- 原文：`reviewer_audit.md`（逐字抽取，未经改写）；结构化版本：`structured_review.md`。
- 我的逐条核验见 `reviewer_audit.md` 附表，结论分布：

| 结论 | 条数 | 说明 |
|---|---|---|
| 成立 | 16 | 其中 S1、E1 为阻断级 |
| 部分成立 / 已由本轮修复 | 2 | T1、I2 |
| 已消除 | 1 | I1（引用核验由 0 条修到 18 条通过） |
| 不成立（评审时证据被 `reference_inventory` 覆盖污染） | 3 | T2、I6 及 T1 的成因 |

- 最严重的三条：**摘要核心数字与自身证据库 E-A 冲突**（S1）、**同稿 16 与 18 并存**（E1）、
  **声称"逐条可回算"的源文件不含被回算的数据**（T1/I2）。三条均已在第 1 节处置。

---

## 5. 修订对评审发现的映射

| 评审发现 | 处置 |
|---|---|
| S1 摘要/§4 三项俱全表述 | 改为按 E-A 台账的字段覆盖表述，明确"三项俱全 0 条" |
| S2 未获取摘要等同未披露 | claim_register CL-2 降为"受限样本事实" |
| S3 由 6 条推及体裁 | 正文加"可能…需在全文层进一步检验"；GAP-2 由"24 条摘要"改为"6 条带摘要记录" |
| S4 点云/视频/skeleton 边界 | §2 增加范围边界声明 |
| S5 §4 小标题过强 | 改为"在有摘要子集内…" |
| E1 16 与 18 | §2、§5 统一为 18 |
| E2 缺 GAP-4 | §5 补 GAP-4 |
| E3 摘要负结果无限定 | 结论加"仅基于 6 条带摘要样本" |
| E4 R01–R21 | 改为 R01–R24 |
| E5 严格同行评审未定义 | 明写"仅保留顶会正刊与期刊（共 7 条）" |
| T3 载体构成互斥 | research_dossier 改为 2/2/5/6/6/3 |
| T4 3/1/2 未逐条落地 | 建立 E-A 逐条台账（本轮新取 6 条摘要） |
| T5 延迟定性不一 | E-C、CL-5、GAP-3、results_validation 统一为推断 |
| T6 CL-1 依赖标错 | 改为 E-A + 标题层归类 |
| T7 results_validation 回算源 | 改为指向 E-A 台账，并注明未做 24 条逐条映射 |
| T8 标题年份 | 改为 2021–2026 |
| T9 R18 未引 | E-A 台账已按 R18 标注来源 |
| I3 剔除项未列出 | **未改**：剔除的 5 条当时未留档，无法追补；已在报告登记 |
| I4 载体风险标为事实 | CL-4 降为"判断"，正文注明标准见 §2 |
| I5 书目表性质 | 表首注明"纳入语料全集（24 条）" |

---

## 6. 下一步（供决策）

1. 对修订版**再派发一次独立盲评**（R1），闭环"评审—修订—再评审"。
2. 决定 Q1（引用候选池口径）与 Q2（遗留 reference_plan）的处置方向。
3. 若需目视门，先安装 poppler（需确认）。
4. 若需 LaTeX 交付面可编译，先安装 TeX 发行版（需确认）。

**本轮未做的事**：未开展任何用户研究方向的工作；未训练模型；未做实验；
未写入任何未经验证的读数；未为过检查而填数或伪造任何 attestation。

---

## 7. 第二轮验证（交付面一致性 + 自查）

### 7.1 核验方法

- 用 PDF 文本抽取实际读回 `final_paper/paper.pdf` 逐页内容，与 `manuscript.md` 对账；
- 对 `main.tex`、`manuscript.html` 逐项统计关键词：`四项文献层空白`、`GAP-4`、
  `纳入语料全集`、`三项文献层空白`、`2020`。

结果：`main.tex` 与 `manuscript.html` 均为 1/1/1/0/0；PDF 页 3–4 逐字核对到
标题 `2021‒2026`、`R01‒R24`、`18 条`、`三项俱全 0 条`、四项 GAP、书目表说明。

### 7.2 本轮自查发现并修掉的新问题

| # | 问题 | 性质 | 处置 |
|---|---|---|---|
| N1 | §5 标题写“可成立的三项”，但修订后已列 GAP-1 至 GAP-4 | 修订引入的新矛盾 | 改为“四项” |
| N2 | §5 的 GAP-1 仍写“多数记录未同时披露…元数据层可核”，未同步 S2 的受限样本表述 | 修订不彻底 | 改为“各 3/1/3、三项俱全 0 条；其余 18 条不可知” |
| N3 | HTML 转换器跳过 `>` 引用块、且把硬换行拆成多个段落，导致 HTML/PDF 与 markdown 源分叉（新增的书目表说明在 PDF 中丢失） | **违反单一语义源** | 重写转换器：合并硬换行段落、渲染引用块、列表项独立成段 |

### 7.3 重出与复跑

- 交付面重出：`paper.docx` / `main.tex` / `manuscript.html` / `paper.pdf`
  （**1,562,526 B**，`%PDF-`；因段落合并而变小）。
- `artifact_check`：缺失项 **0**，内容问题 **3**（同源引用池配额），**警告 0**。
- `figure_story_check`：FAIL（3 条：遗留 `reference_plan` / 目视收据 / LaTeX 交叉引用）。

### 7.4 本轮判定为“不追”的项

- **LaTeX 正文交叉引用**（要求在 `main.tex` 正文出现 `\ref{fig:...}`）：pandoc 的
  markdown 路径无交叉引用语法，强写需插原始 LaTeX 跨度，会污染 docx/html 两面。
  且该条不影响门控结果（仍有两条结构性 FAIL）。判定为**需 TeX 工具链才有意义**，不追。
- **图注内行内代码后的空格**：中文排版下不需空格，仅记录不修。

### 7.5 已派发

- 第二轮独立盲评（对修订版做修复验证）已派出，结果待回。

---

## 8. 第三轮（安装授权后：目视门）

### 8.1 环境事实与安装

| 项 | 状态 |
|---|---|
| 管理员权限 | **无**（choco 已装但不可用，故不走系统级安装） |
| PyMuPDF | **已装** `1.28.2`（`pip install --user pymupdf`，用户级，可用 `pip uninstall` 回滚） |
| poppler（便携版） | **已下载并解压**：官方 `oschwartz10612/poppler-windows` `Release-26.09.0-0.zip`，解压至 `foundation\tools\poppler\`，不写系统目录 |

### 8.2 已完成的目视验证（不依赖 poppler）

- `visual_readiness_check.py --inspect-pdf`：**5/5 页，无布局信号**（像素层无裁切/异常空白告警）。
- 用 PyMuPDF 将 5 页全部渲染为 96 dpi 图像并**逐页读取**；另将图 1 区域以 200 dpi 重新渲染复核图内读数。

| 页 | 目视结论 |
|---|---|
| 1 | 演练横幅、标题（2021–2026）、摘要数字（6 条带摘要；参数量 3 / 算力 1 / 精度 3 / 三项俱全 0；18 条无摘要）、关键词、§1、§2 起，均完整无裁切 |
| 2 | 范围边界（3D 点云/视频/skeleton）与 18 条均正确；尾部空白实测 **9.3%**，属正常页边距 |
| 3 | 图 1 三面板与图注；200 dpi 复核读数 (a) 1/3/4/6/5/5、(b) 2/2/5/6/6/3、(c) 3/1/3/0/2，与 `evidence_bank.md` 一致；§5 已列 GAP-1 至 GAP-4 |
| 4 | GAP-4/GAP-5、四项局限、§6 结论（含受限样本限定）、书目表首说明均在 |
| 5 | 书目 R08–R24 完整；页尾空白 20.1%（末页，正常） |

### 8.3 第三轮修掉的问题

| # | 问题 | 性质 | 处置 |
|---|---|---|---|
| N4 | 图 1 在 A4 版面里被缩至约 5.6 cm/面板，8 pt 标签印出偏小 | 版式可读性 | 画布收窄为 11.0×4.3 in，字号上调（标题 12、刻度 9–10、数值 10），重绘并重出 |
| N5 | HTML 转换器不处理行内代码，反引号在 PDF 中**原样打印**（如 `` `materials_only` ``） | 交付面格式缺陷 | 转换器增加行内代码解析与 `code` 样式，重出 |

### 8.4 交付面复核（新增工具 `check_surfaces.py`，直读 PDF 字节）

- 必现项均命中：`2021`×3、`R24`×2、`四项文献层空白`、`GAP-4`、`纳入语料全集`、`18 条`、`同时给出三项者为 0 条`×2
- 必消项均为 0：反引号、`三项文献层空白`、`16 条记录无摘要`、`2020`、`3 条同时报告参数量`
- 页尾空白实测：p1 12.1% / p2 9.3% / p3 10.2% / p4 8.6% / p5 20.1%

### 8.5 收据绑定（待 poppler 就绪）

1. 把便携版 poppler 的 `bin` 加入本次会话 PATH；
2. 跑 `visual_readiness_check.py <ROOT> --prepare` 生成逐页/逐图渲染与待填收据；
3. 逐页读取渲染图，把每项 `pending` 如实改写为 `pass`/`fail` 并注理由；
4. 跑校验；若背景像素探针为 FAIL，则修图背景而非改收据。

---

## 9. 第二轮盲评回收与第四轮修订

### 9.1 评审结果

- 修复验证 23 条：已修复 14、部分修复 6（S1/E2/T8/I1/I4/I5）、已解决非缺陷 2（T2/I6）、未修复但已登记 1（I3）。
- 新问题 13 条（N1–N13），其中 MAJOR 4 条、MEDIUM 1 条、MINOR 8 条。
- 评审者自己声明：首次读到的是旧快照（§5 未更新），已重读并以当前磁盘文本为准；未写入任何文件。

### 9.2 我的逐条核验

| 发现 | 核验 |
|---|---|
| N1 摘要承诺证据强度分级、正文无此节 | **成立**，已补 |
| N2 “标准见第 2 节”是悬空指针（跳 4 个文件） | **成立**，已补标准 |
| N3 research_dossier §4 分级与“仅 6 条有摘要”互斥 | **成立**，已重写 |
| N4 confirmed_motivation 残留旧断言（三项俱全 3 条） | **成立**，已改 |
| N5 GAP-3 举例与 E-A/E-C 打架 | **成立**，已改 |
| N6 “12 条未引注”应为 11 | **成立**，已改 |
| N7 年份未同步到 3 份伴档 | **成立**，已改 |
| N8 引用核验残差未入局限 | **部分成立**：局限已补；但“C01 重复行”属 25 行/24 源的固有设计（R01 支撑两条论断），非错误 |
| N9 摘要 3/1/3 未标“可重叠” | **成立**，已改 |
| N10 §6 未带样本限度 | **成立**，已改 |
| N11 R21 入范围却无族别 | **成立**，已补说明 |
| N12 载体归并规则未声明 | **成立**，已补 |
| N13 CL-1 依赖不精确 | **成立**，已改 |

### 9.3 本轮修订（对应 N1–N13）

| 文件 | 改动 |
|---|---|
| `final_paper/manuscript.md` | 摘要承诺改为“可判定样本的证据强度分级”；§2 新增**载体分级标准**；§3 补 R21 未归族说明；§4 新增**证据强度分级表**（4/2/18）并在图注补归并规则；§5 GAP-3 去掉“仅 R19/R20”并改指 E-A、局限由四项改为**五项**（新增引用核验残差）；§6 评测口径分裂加样本限度；书目表改为 11 条 |
| `confirmed_motivation.md` | Supporting Observation 改为字段覆盖表述（三项俱全 0 条） |
| `research_dossier.md` | §4 分级表按 E-A 重写（4/2/18 + 高风险另列维度）；年份统一为 2021–2026 |
| `claim_register.md` | CL-1 依赖精确化为“标题层归类（全 24 条）+ E-A（仅 6 条边界核对）”，并补修订记录 |
| `paper_spine_config.json/.md` | 标题年份 2020→2021 |

### 9.4 重出与复核

- 交付面重出：PDF **1,594,918 B**、**6 页**（新增分级表）；`check_surfaces.py` 必现项全中、必消项全 0。
- `artifact_check`：缺失项 0，内容问题仍为 **3 条同源配额项**，警告 0。
- 目视复核：页 3 分级表（4/2/18）与归并规则、页 4 GAP-1..GAP-4、**五项局限**均已在渲染图中确认。

---

## 10. 第五轮（目视门收据绑定）

### 10.1 网络绕行

- GitHub release CDN 在本环境不可达（release 资产下载中途超时）；用户确认环境无法翻墙。
- 改走 **conda-forge**（Anaconda 自有 CDN 可达）：`conda create -y -n spine-tools --override-channels -c conda-forge poppler`
  → **poppler 26.09.0** 装入 `D:\Anaconda\envs\spine-tools`（**独立环境，不碰 base**，可用 `conda env remove -n spine-tools` 删除）。
- `pdftoppm` / `pdfinfo` 实测可用；未写入系统 PATH。

### 10.2 收据绑定

- `--prepare` 生成：6 页渲染（`visual_audit/pages/page-1..6.png`）+ 图渲染 + 待填收据。
- 逐页读取 poppler 渲染图并逐项核过；图内读数在 300 dpi 资产上复核。
- 已填：页 6 页 × 5 项、图 9 项、面板 3 项；**不适用项（基线/数据集/指标）显式标注为不适用**，不静默跳过。
- 校验收敛：从 40+ 条 findings → **1 条**。

### 10.3 本轮又修到的一个真问题

| # | 问题 | 处置 |
|---|---|---|
| N14 | `figure_requests.json` 的面板意图仍是**修订前的旧断言**（“24 条中仅 3 条完整披露”——即被推翻的 S1），且 body contract 镜像它会静默传播错误意图 | 已改为与 E-A 台账一致的表述；图注同步 |
| N15 | 图无外白边，画布边缘带含文字，背景探针无法判定为纯白 | 重绘时加 `pad_inches=0.25`，画布边缘真为白 |

### 10.4 唯一剩余 finding（不伪造）

- `figure fig:evidence-landscape actual canvas/axes/panel background probe is not PASS`。
- 原因：背景规格只能放在 `figure_requests.json` 所引用的 **`final_mapping` 文件**里（需自哈希 `mapping_sha256` 绑定），
  而该文件属于与 `reference_plan` 同一类的**遗留契约**。事后补造会让声明顺序倒置（先声后出变成先出后补），
  与此前定下的“不伪造 attestation 链”一致，**本抮不补**，留 Q2 裁决。

### 10.5 门控现状（终态）

| 脚本 | 状态 | 剩余项 |
|---|---|---|
| `artifact_check` | FAIL | 3 条同源（引用池配额）|
| `citation_bank_check` | PASS | — |
| `citation_quality_audit` | PASS（25 条 / 18 核验 / 88 分）| 6 条 arXiv pending、1 条 DOI 匹配存疑（已写入正文局限）|
| `contribution_check` / `results_validation_check` | PASS | — |
| `figure_story_check` | FAIL | 2 条：遗留 `reference_plan`；正文未出现标签串 |
| `figure_reference_check` | FAIL | 1 条：遗留 `reference_plan` |
| `visual_readiness_check` | FAIL | **1 条**：背景探针需 `final_mapping` |
| `usage_ledger` / `integrity_audit` | PASS / 无新增 | — |

**结论：除“引用池配额”“遗留 reference_plan/final_mapping”“LaTeX 正文交叉引用”三类外，门控已全部收敛。**

---

## 11. 第六轮：授权后定案与执行

### 11.1 三项决策（用户授予全部权限后选定）

| # | 事项 | 定案 | 核验依据 |
|---|---|---|---|
| Q1 | 引用池配额（60 行/60 源/48 近期） | **记 `SOURCE_COVERAGE_BLOCKED` + 接受 FAIL，不填数** | 扩到 60 源会连带推翻 n=24 的语料设计与全部派生数字（图 1、摘要、§4），属**重新设计**而非修补；且方法文档自述 3x 配额不是完成要求 |
| Q2 | 遗留 `reference_plan` / `final_mapping` | **不补，登记为接受性偏差** | 实测：`references/` 方法文档目录**零处**提及 `final_mapping`（仅两个脚本引用），属未定义产物；事后补造会倒置“先声明后出图”的顺序 |
| Q3 | LaTeX 交付面 | 装 **tectonic** 实编译 | 这是真实长期能力（写论文要用），且能把“未编译”从缺口转为已验证或已定性 |

### 11.2 Q1 执行结果

- `citation_support_bank.md` 覆盖度声明已加入 **`SOURCE_COVERAGE_BLOCKED`** 标记与真实计数（25 行 / 24 唯一源）。
- 复跑 `citation_bank_check`：**仍为 PASS**（target 未解析时它自报 coverage not assessed）。
- 未修改任何行数据，未重复行，未改分母。

### 11.3 Q2 判定依据

- `grep final_mapping` 于 `skills/paper-spine/references/`（全部方法文档）→ **无匹配**；仅 `scripts/figure_reference_check.py`、`scripts/visual_readiness_check.py` 引用。
- 因此 `final_mapping` 与 `reference_plan` 同属**未写入方法文档的旧契约**，不得事后补造。
- 后果：`figure_story_check`（参考计划 + 正文标签）、`figure_reference_check`（参考计划）、
  `visual_readiness_check`（背景探针需 final_mapping）均会保留 1–2 条无法在诚实前提下关闭的项。

### 11.4 LaTeX 面：从“不可构建”到“已验证可用”（并抳出一个真缺陷）

- 安装：`conda create -y -n spine-tex --override-channels -c conda-forge tectonic latexmk`
  → **tectonic 0.17.0**（单文件引擎）+ latexmk，装入 `D:\Anaconda\envs\spine-tex`（独立环境，可删）。
- **首轮编译成功但发现阻断级缺陷**：`main.tex` 无任何 CJK 字体设置（只有 babel + lmodern），
  编译虽通过，但汉字全部被丢弃：
  `Missing character: There is no 径 (U+5F84) in font [lmroman10-regular]`，产物仅 188,449 B → PDF 内容不可用。
- 根因：pandoc 在未收到 `CJKmainfont` 时只写 documentclass 的 `chinese` 选项，**不会加载 xeCJK**。
- 修复：`reexport.py` 的 tex 分支显式传 `-V CJKmainfont/CJKsansfont/CJKmonofont=Microsoft YaHei`；
  重生成后 `main.tex` 已含 `\usepackage{xeCJK}` + `\setCJKmainfont[]{Microsoft YaHei}`。
- 复编译：**Missing character 警告 = 0**，PDF 由 188 KB → **487 KB**（字形真嵌入）；
  渲染 main.pdf 第 1 页目视确认：标题、摘要、关键词、§1 引言均为正常中文排版。
- 后果：`main.tex` 改变使目视收据失效，已**重跑 `--prepare` 并重新填写收据**（非沿用旧收据）。

### 11.5 临时目录与可回滚声明

| 新增物 | 位置 | 回滚 |
|---|---|---|
| PyMuPDF 1.28.2 | 用户级 pip | `pip uninstall pymupdf` |
| poppler 26.09.0 | `D:\Anaconda\envs\spine-tools` | `conda env remove -n spine-tools` |
| tectonic 0.17.0 + latexmk | `D:\Anaconda\envs\spine-tex` | `conda env remove -n spine-tex` |
| tectonic 宏包缓存 | `%LOCALAPPDATA%\Tectonic` | 直接删除 |
| LaTeX 产物 | `dryrun\spine-001\texbuild\` | 删除即可 |

### 11.6 沉淀的防复发规则

1. **不要占用品控脚本的输出路径**（`reference_inventory.py` 会覆盖 `source_index.md`）——自建产物另名。
2. **交付面必须与单一语义源对齐**：任何 HTML/PDF 渲染器都必须处理 `>` 引用块、行内代码、硬换行段落，否则会产生“正文改了、交付面没改”的静默分叉。
3. **一处事实断言可能在多个伴随文件里重复**（本例“三项俱全 3 条”在正文、`confirmed_motivation`、`figure_requests` 三处先后暴露）——修一处时必须全局 grep 同源断言。
4. **过检与诚实冲突时，先记录再交人裁决**，不补空绑定、不凑数。
