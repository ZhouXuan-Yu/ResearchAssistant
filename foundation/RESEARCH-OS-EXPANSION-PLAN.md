# 科研智能体 · 阶段化扩展方案（Research OS v1）

| 项 | 值 |
|---|---|
| 日期 | 2026-09-19 |
| 制定者 | 科研助手（agent-mu42qzfz） |
| 目标 | 把当前"一条全链路"扩展为 **全链路 + 可拆装模块** 的双形态 |
| 依据 | 联网核验（见 §1）+ 本机既有 taxonomy（A–M 功能组）+ 已验通的演练链路 |
| 证据约定 | 【实】=我核到的一手来源；【推】=我的判断；【待】=未完成验证 |

---

## 0. 结论先行

1. **阶段划分**：科研全流程的权威划分是 **4 相位 / 8 阶段**（Kong et al., arXiv:2605.18661）【实】。
   其中"写论文"这一步本身又可细分为 **5 个子步骤**（prewriting → drafting → revising → editing → publishing）【实】。
2. **架构**：采用 **1 编排器 + 8 阶段智能体 + 契约总线** 三层。编排器已有（`research-os-router`，非空壳，含 A–M 功能组、路由规则、G1–G5 门禁、准入六步）。
3. **可拆装的关键不是"多写几个技能"，而是"阶段之间只通过文件契约交接"**——有契约就能单跑，缺上游就能请求或降级。
4. **真实缺口只有 3 个**：① 选题与新颖性判定 ② 实验执行与可复现 ③ 传播的多形态产出。其余 5 个阶段已被现有技能覆盖。
5. **一条设计红线**（来自主源原文，非我发明）：AI 的可靠性是**阶段依赖**的，必须给每个阶段智能体标**自主度**，而不是统一"自动化"。

---

## 1. 事实核验

### 1.1 主源

> Kong, L., Sun, X., Chow, W., Li, L., Lin, K. Q., Zhang, X. B., … Ooi, W. T. (2026).
> **AI for Auto-Research: Roadmap & User Guide.** arXiv:2605.18661（v1 2026-05-18，v2 2026-07-20）。
> https://arxiv.org/abs/2605.18661　DOI: 10.48550/arXiv.2605.18661

摘要原文（我核实的一手引文）：

> "…organized into four epistemological phases: **Creation** (idea generation, literature review, coding & experiments, tables & figures), **Writing** (paper writing), **Validation** (peer review, rebuttal & revision), and **Dissemination** (posters, slides, videos, social media, project pages, and interactive agents)."

即 **8 阶段**（4+1+2+1）。项目页与仓库描述亦独立印证："Four phases and eight stages" / "eight interconnected stages grouped into four epistemological phases"。

### 1.2 旁证（相互独立）

| 来源 | 阶段划分 |
|---|---|
| Agent Laboratory（Schmidgall et al., arXiv:2501.04227, 2025） | 3 阶段：literature review / experimentation / report writing |
| The AI Scientist（Lu et al., *Nature*, s41586-026-10265-5, 2026） | idea generation + novelty check → 实验执行 → write-up → automated review |
| 通用写作过程模型（EBSCO Research Starters；Scribbr；Univ. of Kansas Writing Center） | 5 步：prewriting → drafting → revising → editing → publishing |

三者在同一方向上互相印证：**构思 → 检索/执行 → 成稿 → 校验 → 发布**。

### 1.3 两条对设计有直接约束的原文结论【实】

1. 存在"**阶段依赖的可靠边界**"：AI 在结构化、检索有据、工具中介的任务上表现好；在**真正新颖的想法、研究级实验、科学判断**上仍然脆弱（"sharp, stage-dependent boundary between reliable assistance and unreliable autonomy"）。
2. "**人主导协作**是最可信的部署范式"（"human-governed collaboration the most credible deployment paradigm"）；更高自动化会**掩盖**而非消除失败模式。

**设计含义**：每个阶段智能体必须声明自主度等级（可高自主 / 需人确认 / 人主导），并在输出里显式标注；不允许统一按"全自动"设计。

### 1.4 未完成验证【待】

- 只读了摘要与项目页/仓库描述，**未读全文 PDF**，因此 §2 的阶段粒度细化（尤其"表与图"是否独立成阶段）属转述该文，不是我的独立判断。
- 通用写作 5 步模型取自媒体与高校写作中心页面，非学术论文；作为工程惯例参考，不作为学术结论。

---

## 2. 阶段模型（8 阶段 + 横切层）

| # | 阶段 | 相位 | 核心产出 | 可靠自主度 | 复核者 |
|---|---|---|---|---|---|
| S1 | **选题生成**（Idea Generation） | Creation | 候选问题集 + 新颖性/可行性评估 | **人主导** | 用户 |
| S2 | **文献综述与检索**（Literature Review） | Creation | 检索策略、纳入集、证据台账、精读卡 | 可高自主（需可追溯） | 自动核验 + 用户抽检 |
| S3 | **编码与实验**（Coding & Experiments） | Creation | 可运行代码、实验日志、原始结果 | **人主导**（AI 只做执行与复现） | 用户 |
| S4 | **表与图**（Tables & Figures） | Creation | 数据图（含可编辑源）、表、图注 | 可高自主 | 自动自检 + 用户抽检 |
| S5 | **稿件撰写**（Paper Writing） | Writing | 单语义源正文 → 多交付面 | 需人确认（结构与主张） | 用户 + 独立评审 |
| S6 | **同行评审**（Peer Review） | Validation | 结构化评审 + 发现清单 | 可高自主（仅作预审） | 用户 |
| S7 | **返修与回复**（Rebuttal & Revision） | Validation | 逐点回复、修订稿、变更说明 | 需人确认 | 用户 |
| S8 | **传播**（Dissemination） | Dissemination | slides / poster / 视频 / 项目页 | 可高自主 | 用户抽检 |

**S5 的内部细分**（据通用写作 5 步模型）：prewriting（结构与蓝图）→ drafting（首稿）→ revising（论证重构）→ editing（语言与格式）→ publishing（投稿材料）。这可作为 S5 智能体内部的三档模式，而不必拆成 5 个独立智能体。

**横切层**（贯穿全部阶段，不属于任何单一阶段）：

| 层 | 内容 | 现有承载 |
|---|---|---|
| 引用核验 | 每条引用身份 + 语境双核 | `nature-ref-verifier` |
| 统计审查 | 统计表述、多重比较、不确定度 | `nature-statistics` |
| 可复现 | 数据版本、代码提交、随机种子 | 待建（见 §5 缺口②） |
| 证据标注 | 事实/文献/推断/未知四分 | 路由 G5 门禁 |
| 编排与治理 | 路由、准入、回归 | `research-os-router` |

---

## 3. 架构：一主多从 + 契约总线

```
                     ┌───────────────────────────────┐
   用户请求 ──────►  │  L1 编排层                    │
                     │  research-os-router           │
                     │  · 意图→阶段 路由             │
                     │  · G1–G5 质量门禁             │
                     │  · 准入六步 / 回归            │
                     └──────────────┬────────────────┘
                                    │ 只按契约调度
        ┌───────────────┬───────────┼───────────┬───────────────┐
        ▼               ▼           ▼           ▼               ▼
   ┌─────────┐   ┌─────────┐  ┌─────────┐  ┌─────────┐   ┌─────────┐
L2 │ S1 选题 │   │ S2 文献 │  │ S3 实验 │  │ S4 图表 │   │ … S8    │
   │ 智能体  │   │ 智能体  │  │ 智能体  │  │ 智能体  │   │ 智能体  │
   └────┬────┘   └────┬────┘  └────┬────┘  └────┬────┘   └────┬────┘
        │             │            │            │             │
        └─────────────┴──── 契约文件（固定名 + frontmatter）────┘
                                    │
                     ┌──────────────┴────────────────┐
   L3 能力层         │ 已装 skills（nature-* 家族等）  │
                     │ MCP（zotero 53 / academic 16）  │
                     │ 本机工具（poppler / tectonic）  │
                     └───────────────────────────────┘
```

### 3.1 契约总线（全链路与可拆装的共同基础）

阶段之间**不通过对话上下文交接，只通过文件契约**。每条契约 = 固定文件名 + YAML frontmatter：

```yaml
---
stage: S2_literature
produced_by: nature-academic-search
produced_at: 2026-09-19T16:00:00+08:00
upstream: [S1]
artifacts:
  - reference_materials/source_index.md
  - evidence_bank.md
claims: [CL-1, CL-2]
reproducibility: {data_version: null, code_commit: null, seed: null}   # 空缺即未达可复现
verification: {checked: 24, unresolved: 6, notes: "6 条仅存 arXiv 标识"}
---
```

### 3.2 "拆开用"的三条机制

| 机制 | 说明 |
|---|---|
| ① 独立触发 | 每个阶段智能体有自己的触发词与入口，不依赖编排器。 |
| ② 缺上游时的策略 | 三选一，且**必须显式声明选了哪个**：`请求上游产物` / `降级自给（并标注证据较弱）` / `拒绝执行`。 |
| ③ 自检门可单跑 | 每个阶段自带一个可独立执行的检查脚本（如引用核验、图注一致性），不跑全链路也能验收。 |

全链路 = 编排器按"契约是否齐备"推进；单模块 = 用户只喂目标阶段的输入契约。

---

## 4. 八个阶段智能体规格

> 形态说明：这里的"智能体"指**技能 + 可选子代理**的组合，不是必然新建 8 个 Agent 实例。优先用"技能"承载，只有在需要独立上下文/独立模型时才升格为子代理。

| # | 名称（暂定） | 触发词 | 输入契约 | 输出契约 | 自检门 | 自主度 |
|---|---|---|---|---|---|---|
| S1 | `idea-forge` | 选题、想题目、找空白、新颖性 | 领域范围 + 用户兴趣/约束 | `idea_options.md`、`novelty_check.md` | 每条想法须给出"与已有工作的差异点 + 可验证性" | 人主导 |
| S2 | `lit-scout` | 检索、综述、找文献、系统综述 | S1 的问题集（或直接给主题） | `search_strategy.md`、`source_index.md`、`evidence_bank.md`、`source_inventory.md` | 纳入/排除可回算；引用身份可核验 | 可高自主 |
| S3 | `exp-runner` | 跑实验、复现、实验日志 | S1/S2 的假设与设计 | `experiment_log.md`、`code_commit`、`raw_results/` | **可复现三元组**（数据版本/代码提交/种子）缺一不得写入结论 | 人主导 |
| S4 | `fig-studio` | 画图、出图、配图、表 | S3 原始结果 | `fig_*.py`、`*.png/svg`、`figure_asset_map.md` | 图注数字可回算；不把相关性画成因果 | 可高自主 |
| S5 | `paper-forge` | 写论文、起草、重构、压缩 | S2–S4 全部契约 | `manuscript.md` + 四交付面 | 单语义源一致性；结论强度与证据量级匹配 | 需人确认 |
| S6 | `peer-sim` | 预审、模拟审稿、投稿前检查 | S5 的稿件 | `structured_review.md`、`reviewer_audit.md` | 撰写者不得自评；发现须给位置与改法 | 可高自主 |
| S7 | `rebuttal-smith` | 回复审稿、返修、逐点回复 | 审稿意见 + S5 稿件 | `response.md`、修订稿、变更说明 | 每条意见必有对应修改或明确理由 | 需人确认 |
| S8 | `disseminate` | 做PPT、海报、讲稿、项目页 | S5 稿件 | `slides.pptx`、`poster.*`、`script.md` | 图表与正文数字同源；不新增未支撑主张 | 可高自主 |

> 与现有技能的映射：S2 由 `nature-academic-search`（主）+ `nature-reader`/`nature-paper-card`（辅）承担；
> S4 由 `scipilot-figure-skill`（主）+ `nature-figure` 承担；S5 由 `nature-writing`（主）+ `nature-polishing` 承担；
> S6 由 `academic-paper-reviewer`（主）+ `nature-reviewer` 承担；S7 由 `nature-response` 承担；
> S8 由 `nature-paper2ppt`（主）+ `nature-image2ppt` 承担。**这些不需要新建，只需补契约封装。**

---

## 5. 覆盖矩阵与真实缺口

| 阶段 | 现有覆盖 | 缺口 |
|---|---|---|
| S1 选题 | `researchwrite`（A 组 primary）、`quiet-musing`、`deep-research` 引导模式 | **缺"新颖性判定 + 可行性过滤"**：现有技能偏计划书撰写，不产出可核验的差异化评估 |
| S2 文献 | B 组 5 个 + C 组 4 个 + zotero/academic MCP | 覆盖充分；改进点是**契约化**（本轮已验证 24 条记录的台账写法） |
| S3 实验 | 仅 `nature-experiment-log`（记录）| **缺"执行 + 可复现封套"**：无沙箱执行、无数据版本/提交/种子绑定、无结果落盘规范 |
| S4 图表 | E 组 3 个 | 覆盖充分 |
| S5 写作 | G 组 2 个 + `paper-spine` | 覆盖充分；已验通四交付面 |
| S6 评审 | H 组 3 个 | 覆盖充分；已验通两轮独立盲评 |
| S7 返修 | `nature-response` | 覆盖够用；缺"修订前后的差异对照"自动生成 |
| S8 传播 | `nature-paper2ppt`、`nature-image2ppt` | **缺 poster / 视频 / 项目页**（主源把这三类明确列为该阶段产出） |

**缺口清单（3 个 + 1 个增强）**：`idea-forge`、`exp-runner`、`disseminate(扩展形态)`，加 S7 的"差异对照"增强。

---

## 6. 落地路线（分阶段、带验收门与回滚）

| 阶段 | 内容 | 验收门 | 回滚 |
|---|---|---|---|
| **P0 契约冻结** | 定 8 条阶段契约的字段与文件名；写入 `research/00-governance/contracts.md` | 8 条契约样例齐全，且能用本练演练产物填出 S2/S4/S5 三条 | 契约文件可整删，不影响现有技能 |
| **P1 补缺口①②** | 建 `idea-forge`、`exp-runner` 两个技能 | 各自跑通一次最小用例；`check_taxonomy.py` 未分类=0；准入六步完成 | 停用即回滚（技能可禁用） |
| **P2 补缺口③** | 扩展 S8（poster / 项目页） | 用演练稿生成一份 poster 与一个项目页，数字与正文同源 | 同上 |
| **P3 编排串联** | 在 `research-os-router` 里注册 8 条路由 + 阶段推进规则 | 全链路跑一次（可用公开材料），且**每一阶段都能单独触发成功** | routing-rules.yaml 有版本备份 |
| **P4 回归** | 冻结任务集，量化"比上一版强在哪" | 回归 pytest + 人工抽检 | 回到 P3 快照 |

**禁止**：P1/P2 不得批量安装；每个新技能单独走准入六步（审核→分类→登记→冲突裁决→校验→冒烟），未完成不得标记"已接入"。

---

## 7. 风险与红线

| 风险 | 说明 | 应对 |
|---|---|---|
| **契约漂移** | 脚本覆盖产物（本轮已实测：`reference_inventory.py` 覆盖 `source_index.md`，还污染了一轮盲评） | 契约文件路径**避开品控脚本的输出路径**；每次写入后回读校验 |
| **自主度越界** | 把"需人确认"的阶段做成全自动 | 每个阶段契约里带 `autonomy` 字段，越界即拒绝执行 |
| **同源断言分裂** | 同一断言藏在多个伴随文件（本轮"三项俱全 3 条"三处冒头） | 修改任何断言时必须全局 grep 同源 |
| **技能重叠** | 新技能与同组 primary 能力重复 | 走准入第 4 步冲突裁决，否则不得启用 |
| **过度建设** | 为"看起来完整"而建不需要的技能 | 只建 3 个缺口；能用现有技能 + 契约封装解决的，不新建 |

**红线（不可越过）**：研究问题、方法选择、结果解释、核心学术主张始终由用户决定；AI 不生成虚假文献/DOI/数据；相关不表述为因果；缺失标"待确认"。

---

## 8. 本方案的未完成项（不隐藏）

- 主源**全文未读**，阶段粒度细化属转述【待】。
- 通用写作 5 步模型来源为教学/媒体页面，非学术文献。
- 3 个缺口技能的具体实现形态（纯技能 vs 技能+子代理 vs 独立 Agent）**尚未定稿**，需在 P1 前按实际上下文需求决定。
- 未估算工作量与所需权限；P1 涉及代码执行，需单独评估执行边界。

---

## 9. P0 执行结果（契约冻结，2026-09-19）

### 9.1 产出物

| 文件 | 作用 |
|---|---|
| `research/00-governance/contracts.md` | **契约规范 v1.0**：15 字段、阶段-相位对照表、自主度下限表、7 条校验规则 |
| `foundation/tools/check_contracts.py` | **可执行验收门**（存在性校验 + 规则引擎） |
| `foundation/tools/negtest_contracts.py` | 6 条负例测试（证明校验器会拒绝坏契约） |
| `foundation/dryrun/spine-001/contracts/S2_literature.yaml` | 用演练产物实填的样例 |
| `foundation/dryrun/spine-001/contracts/S4_figures.yaml` | 同上 |
| `foundation/dryrun/spine-001/contracts/S5_writing.yaml` | 同上 |

### 9.2 验收结果

- **正例**：`check_contracts.py` 对 3 条演练样例 → **3/3 PASS**（artifact 路径逐个存在性校验通过）。
- **负例**：6 条故意破坏的契约 → **6/6 被正确拒绝**，且拒绝理由与预期一致：
  自主度越界 / artifact 不存在 / S3 可复现三元组为空 / gate=fail / blocked 未写进 unresolved / phase 与 stage 不符。

### 9.3 P0 过程中发现并修掉的一个真 bug（值得单列）

- 首轮负例测试后，**N1（S1 声明“可高自主”，越过“人主导”下限）未被拒绝**。
- 根因：校验器里自主度强度映射写反（把“人主导”当成最强）。一行修复后 6/6 全中。
- 结论：**门禁必须有负例测试**。没有负例的“全绿”不构成证据——这与“绿色的 CI 会撒谎”同源。

### 9.4 P0 的一个设计增量

- 门禁状态由 3 态扩为 4 态：增加 **`blocked`**（做了且已定位阻塞原因）。
- 动机：没有 `blocked` 时，只能把“图 1 目视背景探针受阻”谎报为 `n_a`（不适用）或 `pass`（通过）。
- 强制规则：出现 `blocked` 必须在 `unresolved` 里写下来，否则校验失败。

### 9.5 P0 未决

- S1 / S3 / S6 / S7 / S8 的契约样例**尚未填写**（P0 验收只要求 S2/S4/S5 三条）。
- `foundation/dryrun/spine-001/contracts/` **尚未接入** `research-os-router`（属 P3）。
- 负例测试目录 `foundation/tools/_contract_negtest/` 为测试夹具，**不得**混入正式契约目录。

---

## 10. P1a 执行结果（建设 `idea-forge`，2026-09-19）

### 10.1 产出

| 文件 | 作用 |
|---|---|
| `skills/idea-forge/SKILL.md` | S1 选题与新颖性判定；6 条硬规则；自主度人主导 |
| `skills/idea-forge/references/novelty-rubric.md` | 三筛评分细则 + 差异点五归类 + 阈值 |
| `foundation/dryrun/idea-001/` | 冒烟测试（公开主题，最近邻仅到摘要层） |
| `foundation/dryrun/idea-002/` | **真实选题演练**（真实检索，含一条被排除的候选） |
| `foundation/tools/sync_registry.py` | 注册表两份副本的同步/检查（本轮发现的漂移缺陷） |
| `foundation/tools/taxgate_test.py` | 准入门双向测试 |

### 10.2 准入六步（全部完成）

| 步 | 结果 |
|---|---|
| ① 审核 | 自建；无脚本、无网络、无 subprocess、无依赖 |
| ② 分类 | `A_topic_proposal`，usage `[分析, 生产]`，role `primary` |
| ③ 登记 | `SKILLS-GOVERNANCE.md` 来源 D + §3 映射 + §7 变更日志 |
| ④ 冲突裁决 | A 组 primary 由 `researchwrite` 改为 `idea-forge`（裁决理由已写入 routing-rules.yaml）|
| ⑤ 校验 | `check_taxonomy.py`：未分类 0 / 问题 0；启用后 146 项全绿 |
| ⑥ 冒烟测试 | idea-001（3 候选→2 过 1 排除）+ idea-002（真实检索版） |

### 10.3 过程中发现并修掉的缺陷

| # | 缺陷 | 处置 |
|---|---|---|
| D1 | **注册表副本漂移**：技能包内 `references/taxonomy.yaml` 与工作区 `foundation/routing/skill-taxonomy.yaml` 是同一注册表的两个副本，已分叉（工作区为超集，多了 paper-spine）；且门禁脚本读的是**工作区那份** | 写 `sync_registry.py`（--check / --apply），实测 DRIFTED → apply → in sync |
| D2 | `SKILLS-GOVERNANCE.md` 两处**过期断言**：`research-os-router` 写“未建”、`scientific-brainstorming` 写“无上游” | 已订正 |
| D3 | **我的误判**：曾报告工作区注册表“中文注释乱码”，实际是 PowerShell 控制台渲染问题；dry-run 脚本（changed: 0）当场否掉 | 已收回并写进经验库 |
| D4 | 自建校验器**自主度强度映射写反**，导致 S1 越权（可高自主）被静默放行 | 负例测出后修复；已沉淀“门禁必须有负例”规则 |

### 10.4 真实选题演练（idea-002）结果

主题：MM-RAG 中的视觉证据归因（**公开领域，非用户选题提案**）。真实检索（academic-search MCP，10 条）后：

| 候选 | 判定 |
|---|---|
| C1 区域级视觉归因能否被判真伪 | 合格（方法+评测） |
| C2 跨模态冲突能否定位到证据源 | **待核**（最近邻未读全文） |
| C3 “多模态增益多少来自文本泄漏” | **不合格，已排除** —— 最近邻 arXiv:2607.16604 摘要已完成该论断（逐字引用存档） |

这一步的价值：**演示了新颖性门真的会否掉想法**，而且否掉时给出了可核验的原文依据。

### 10.5 P1a 未决

- `idea-forge` 的实际启用由用户在 UI 完成（技能启停不在设置 API 内）；实测已生效（启用数 145→146）。
- 契约尚未接入 `research-os-router`（属 P3）。
- **P1b（`exp-runner`）未开工**：需先定三条执行边界（沙箱形态 / 允许的命令范围 / 数据·代码版本绑定）。
  → 草案已出：`research/00-governance/exp-runner-boundary.md`（6 条待用户确认；确认前不写执行代码）。
  实测约束：本机工作区**不是 git 仓库**，故 `code_commit` 需走 `tree:<sha256>` 而非提交号；Docker 服务当前已停止，容器方案需用户启动后才能评估。
