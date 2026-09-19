# 科研技能治理清单（Skills Governance）

> 维护者：科研助手（agent-mu42qzfz）｜创建：2026-09-16｜状态：生效中
> 本文件是所有已装科研技能的唯一权威登记处。任何安装、更新、回滚都必须先更新本文件。

---

## 1. 治理规则（用户既定）

1. 每个技能必须登记：来源仓库、固定提交版本、许可证、依赖、权限、成熟度、适用范围、重叠分组、回滚位置。
2. **每周**执行只读更新检查；**发现更新不得自动安装或覆盖生产版本**。
3. **每月**检查内容同质化、触发冲突与权限变化。
4. **每季度**运行完整回归基准。
5. 更新必须经过：差异审查 → 安全检查 → 隔离测试 → 回归验证 → 用户批准。
6. 无法检查上游时标记为「检查失败」，不得视为「无更新」。
7. 计划中的 Skill 不等于已安装；调用前必须检查安装状态、依赖、权限与版本。
8. **新技能准入分类（强制）**：任何新技能启用前，必须登记进 `foundation/routing/skill-taxonomy.yaml`（恰好一个功能组 + ≥1 用途类型 + 一个角色），与同组主选冲突须裁决，并跑 `check_taxonomy.py` 至 0 未分类。未分类不得启用。分类总表与路由规则见 `foundation/routing/`。

---

## 2. 上游来源登记

### 来源 A：nature-skills

| 项 | 值 |
|---|---|
| 仓库 | https://github.com/Yuan1z0825/nature-skills |
| 固定提交 | `2375e0abdf42158ef149256f2c64b1f759a0d274`（2026-09-16 16:50:46 +08:00） |
| 许可证 | Apache License 2.0 |
| 本地克隆 | `C:\Users\ZhouXuan\Desktop\OH-WorkSpace\research-skills-setup\nature-skills` |
| 安装位置 | `C:\Users\ZhouXuan\.hanako\skills\<skill-name>\` |
| 依赖 | `nature-shared`（共享支持包，随套件一并安装） |
| 权限/风险 | 含 `scripts/`（Python/Shell），部分技能会调用外部库与网络；无安装钩子 |
| 成熟度 | 活跃维护（当日有提交）；作者含商业化运营内容，属第三方供应链，需持续观察 |

已安装（20 项，均来自上述提交）：

```
nature-shared            nature-academic-search   nature-citation
nature-data              nature-downloader        nature-experiment-log
nature-figure            nature-image2ppt         nature-literature-pipeline
nature-paper-card        nature-paper-to-patent   nature-paper2ppt
nature-polishing         researchwrite *          nature-reader
nature-ref-verifier      nature-response          nature-reviewer
nature-statistics        nature-writing
```

\* 目录名 `nature-proposal-writer`，frontmatter 注册名 `researchwrite`。

### 来源 B：academic-research-skills（ARS）

| 项 | 值 |
|---|---|
| 仓库 | https://github.com/imbad0202/academic-research-skills |
| 固定提交 | `3c546bc08c56f79e0068f1ea4f0acedf5bf69b5e`（2026-09-16 11:18:50 +08:00） |
| 许可证 | **CC-BY-NC-4.0（署名-非商业性使用）** — 个人科研可用，商业用途受限 |
| 本地克隆 | `C:\Users\ZhouXuan\Desktop\OH-WorkSpace\research-skills-setup\academic-research-skills` |
| 安装位置 | `C:\Users\ZhouXuan\.hanako\skills\<skill-name>\` |
| 版本 | v3.22.0（plugin.json） |

已安装（2 项，自包含，无插件外部依赖）：

```
academic-paper-reviewer    deep-research
```

**未安装（依赖插件内 `shared/` 契约，单独安装会失效，暂缓）**：
`academic-paper`、`academic-pipeline`。若后续要启用 ARS 完整管线，需整体安装该插件（含 `shared/`、`agents/`、`hooks/`），并重新做安全审查。

### 来源 C：scipilot-figure-skill

| 项 | 值 |
|---|---|
| 仓库 | https://github.com/Haojae/scipilot-figure-skill |
| 固定提交 | `43098ddb9e6a6d142218540c114f9ed38922fc42`（2026-06-15 11:40:49 +08:00） |
| 许可证 | MIT |
| 本地克隆 | `C:\Users\ZhouXuan\Desktop\OH-WorkSpace\research-skills-setup\scipilot-figure-skill` |
| 安装位置 | `C:\Users\ZhouXuan\.hanako\skills\scipilot-figure-skill\`（47 个文件） |
| Python 依赖 | matplotlib≥3.7、seaborn≥0.13、plotly≥5.18、Pillow≥10、numpy≥1.24、pandas≥2.0、scipy≥1.10；可选 SciencePlots/pypdf/kaleido/PyMuPDF |
| 已补装依赖 | `seaborn 0.13.2`、`scienceplots`（`python -m pip install`，本机 Python 3.14） |
| 权限/风险 | 脚本仅用标准绘图库与本地模块，无网络、无 subprocess/exec；安全审查通过 |
| 成熟度 | 单人维护，v2.1.0；第三方供应链，持续观察 |
| 适用范围 | 纯数据图（折线/柱/散点/箱线/热力/误差棒/分布/相关矩阵/多面板）；先剖析数据与选图再绘制；覆盖 Nature/Science/IEEE/Elsevier/PNAS 及中文期刊 |

已安装（1 项）：`scipilot-figure-skill`。

**路由约定（本方案核心）**：

| 场景 | 走哪个 |
|---|---|
| 数据图、中文期刊配图、需要“先判断图型”的场合 | `scipilot-figure-skill` |
| AI 图形摘要、机制示意图、Nature 系投稿图、需要 R 后端 | `nature-figure` |

该分工为约定，非平台强制；若触发歧义，以用户显式指定优先。

### 来源 D：自建（Skill Forge）

| 项 | 值 |
|---|---|
| 仓库 | 无（自建） |
| 版本 | v0.1（2026-09-18） |
| 许可证 | —（自有） |
| 安装位置 | `C:\Users\ZhouXuan\.hanako\skills\hana-agent-ops\`（4 个文件） |
| 源码留档 | `OH-WorkSpace\foundation\skill-forge\candidates\hana-agent-ops\` |
| 依赖 | Python 3 标准库；脚本无网络、无副作用（health_check 只读） |
| 适用范围 | HanaAgent 环境自检、模型链路诊断、记忆故障定位、技能治理与冒烟、备份回滚、凭据权限核查 |
| 回滚 | 删除目录 + 从 `skills.enabled` 移除 |
| 生成依据 | `gap-report.md`：环境运维意图 20 次命中、`exec_command` 200 次调用，且此前无现成技能覆盖 |
| 治理 | 自建技能与外部技能同一套标准；协议见 `foundation\skill-forge\PROTOCOL.md` |

已安装（3 项，均自建）：`hana-agent-ops`、`research-os-router`、`idea-forge`。

- `research-os-router`（v0.1）：科研任务编排与新技能准入门禁；随带 `references/`（分类总表、路由规则、功能地图）与 `scripts/check_taxonomy.py`。
- `idea-forge`（v0.1，2026-09-19）：阶段 S1 选题生成与新颖性判定。
  | 项 | 值 |
  |---|---|
  | 安装位置 | `C:\Users\ZhouXuan\.hanako\skills\idea-forge\`（SKILL.md + references/novelty-rubric.md）|
  | 依赖 | 无脚本、无网络、无 subprocess；纯指令 + 评分细则 |
  | 适用范围 | 候选研究问题生成、新颖性判定、可行性三筛、falsifier 书写 |
  | 权限/风险 | 无执行权限；仅产出文档 |
  | 回滚 | 删除目录 + 从 `skills.enabled` 移除 |
  | 生成依据 | Research OS 扩展方案 §5：8 阶段中唯一的“选题”缺口（现有 A 组技能偏计划书撰写，不产出可核验的差异评估）|
  | 契约 | 产出 `idea_options.md` / `novelty_check.md`；阶段契约见 `research/00-governance/contracts.md` |

---

## 3. 计划技能 → 实际落地映射

| 计划技能 | 落地情况 |
|---|---|
| academic-research-suite | 仅有内容为空的 stub（1 个 SKILL.md）；真正的编排器 `academic-pipeline` 待整体安装 |
| research-os-router | ✅ 已自建（v0.1，2026-09-18）|
| scientific-brainstorming | 由自建 `idea-forge` 覆盖选题与新颖性判定（2026-09-19）|
| nature-academic-search | ✅ 已装 |
| nature-reader | ✅ 已装 |
| nature-paper-card | ✅ 已装 |
| literature-review | 由 `nature-literature-pipeline` 覆盖 |
| citation-management | 由 `nature-citation` + `nature-ref-verifier` 覆盖 |
| pyzotero | 无独立技能；`nature-ref-verifier` 已含 pyzotero 写入路径 |
| experiment-agent | **无上游对应**，未安装 |
| experimental-design | **无上游对应**，未安装 |
| statistical-analysis | 由 `nature-statistics` 覆盖 |
| statistical-power | **无上游对应**，未安装 |
| nature-statistics | ✅ 已装 |
| scientific-visualization | 由 `nature-figure` 覆盖 |
| nature-figure | ✅ 已装 |
| nature-writing | ✅ 已装 |
| nature-polishing | ✅ 已装 |
| academic-paper-reviewer | ✅ 已装（ARS） |
| nature-reviewer | ✅ 已装 |
| nature-response | ✅ 已装 |
| nature-data | ✅ 已装 |
| nature-paper2ppt | ✅ 已装 |
| venue-templates | **无上游对应**，未安装（`nature-writing` 内含投稿要求检查） |

**尚未覆盖的计划项**：experiment-agent、experimental-design、statistical-power、venue-templates。这些目前无公开上游，需自建或另找来源。（选题项已由 `idea-forge` 覆盖；`research-os-router` 已建成）

---

## 4. 重叠分组（每月复核）

- **文献获取**：nature-academic-search / nature-citation / nature-ref-verifier / nature-downloader / nature-literature-pipeline — 按「检索 / 论断支撑 / 元数据核验 / 全文获取 / 系统综述」分工，勿重复触发。
- **精读**：nature-reader（中英对照阅读器）vs nature-paper-card（结构化精读卡）— 前者偏呈现，后者偏解析。
- **写作**：nature-writing（结构论证）/ nature-polishing（语言润色）/ researchwrite（计划书）— 阶段不同。
- **审查**：nature-reviewer（Nature 方向模拟审稿）vs academic-paper-reviewer（预投稿审查）— 独立二次审查与主流程，均应保留。
- **与既有库重叠**：`paper-deep-reading`、`navi-deep-research`、`deep-research` 三者均涉文献深读，需在月检中厘清优先级。
- **科研绘图（已路由隔离）**：`scipilot-figure-skill`（数据图 + 中文期刊 + 先判断图型）vs `nature-figure`（AI 图形摘要 / 机制示意图 / Nature 系 / R 后端）— 触发歧义时以用户显式指定优先。

---

## 5. 回滚位置

- 原始克隆保存在 `research-skills-setup\`（含 `.git`），可 `git checkout <commit>` 回到任一固定版本。
- 卸载单个技能：删除 `C:\Users\ZhouXuan\.hanako\skills\<name>\` 并从 `config.yaml` 的 `skills.enabled` 移除。
- 全量回滚：按来源 A/B 的固定提交重新安装。
- **安装前的 `skills.enabled` 快照**见本目录 `skills-enabled-snapshot-20260916.txt`。

---

## 6. 维护计划

| 频率 | 动作 | 载体 |
|---|---|---|
| 每周 | 只读更新检查（对比远程 HEAD 与固定提交），发现更新只报告不安装 | 定时任务 |
| 每月 | 同质化 / 触发冲突 / 权限变化检查 | 人工或定时任务 |
| 每季度 | 完整回归基准 | 待建设 |

---

## 7. 变更日志

- 2026-09-16：首次建立。安装来源 A 全部 20 项、来源 B 自包含 2 项；建立治理清单与周更检查。
- 2026-09-18：安装来源 C `scipilot-figure-skill`（MIT）；补装 seaborn/scienceplots 依赖；建立与 `nature-figure` 的绘图路由隔离；冒烟测试通过（CJK 字体识别 + PDF/SVG/PNG/灰度四格式导出）。
- 2026-09-18（二）：Skill Forge 上线（`PROTOCOL.md` + `scan_skill_gaps.py` + `gap-report.md`）；安装首个**自建**技能 `hana-agent-ops` v0.1（来源 D）；补装 `python-pptx`；环境自检转为全绿；`studio_job_2` 改造为周检任务（待确认）。
- 2026-09-18（三）：F4 完成——48 个科研技能分为 13 个功能组，输出功能地图与路由规则（22 条意图 + 4 条门禁）；建立 **Skill Taxonomy**（分类总表）与 `check_taxonomy.py` 准入校验；安装自建编排件 `research-os-router` v0.1；确立**新技能必须审核分类后方可启用**的强制规矩。
- 2026-09-19：接手 Research OS 扩展方案 P1a。新增自建技能 `idea-forge` v0.1（S1 选题与新颖性，人主导）；走完准入六步（分类/冲突裁决/登记/校验/双向门禁测试）；A 组 primary 由 `researchwrite` 改为 `idea-forge`（裁决理由见 `routing-rules.yaml`）；修正本文件两处过期断言（research-os-router “未建”、scientific-brainstorming “无上游”）。P1b（`exp-runner`）待定执行边界后开工。
