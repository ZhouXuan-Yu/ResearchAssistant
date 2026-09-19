# 科研体系架构：单一脊柱 + 外接模块

> 定稿：2026-09-18｜owner: agent-mu42qzfz｜状态：**架构已定，执行未开闸**
> 上位约束：Foundation Stage（见 pinned memory 与 `IMPLEMENTATION_PLAN.md`）

## 0. 设计原则

1. **一条脊柱 + 若干外接。** 编排单一化，能力模块化。禁止两个技能在同一阶段争夺调度权。
2. **门控不可自证。** 任何"通过"必须来自独立于产出者的检查。
3. **证据可追溯、实验可复现、配置可回滚。** 三者缺一，结论不得进入稿件。
4. **成本受控。** 主框架体量大，**不默认全量启用**；局部任务走外接技能。

## 1. 三层结构

```
L0  决策与守门层
    ├─ research-os-router   该不该走、走哪条链、技能准入
    └─ hana-agent-ops       环境自检、配置治理、备份回滚

L1  编排脊柱层（主框架）
    └─ paper-spine          跨阶段调度、阶段门控、产物契约、独立评审调度

L2  外接执行层
    ├─ 科研外接技能（按阶段挂载，见下表）
    └─ MCP 工具（academic-search / zotero，调用名 mcp_<connector>_<tool>）
```

**为什么脊柱与决策分离**：主框架当前是 **alpha 未签名预发布**。让它做编排（失败可回退到手工流程），但**不让它独自掌握"是否走该流程"的判断权**——那由 L0 按证据与阶段判定。

## 2. 外接清单（按科研阶段）

| 阶段 | 功能组 | 外接技能 | 备注 |
|---|---|---|---|
| 选题立项 | A | `researchwrite`（主）、`quiet-musing` | — |
| 文献检索 | B | `nature-academic-search`（主）+ MCP `academic-search`、`nature-literature-pipeline`、`nature-downloader`、`deep-research` | 中文库（CNKI/维普）尚缺通道 |
| 精读解析 | C | `nature-paper-card`（主）、`nature-reader`、`paper-deep-reading`、`zotero-pdf-translate` | 笔记外接：Zotero + Better Notes |
| 引用核验 | D | `nature-ref-verifier`（主）、`nature-citation`、MCP `zotero.scite_*` | 身份 + 语境双核 |
| 统计绘图 | E | `nature-statistics`（统计）、`scipilot-figure-skill`（数据图）、`nature-figure`（机制图/图形摘要） | 脊柱的绘图流程统领此三项 |
| 实验复现 | F | `nature-experiment-log` | 缺复现闭环（差距 G2） |
| 写作润色 | G | `nature-writing`（主）、`nature-polishing`、`researchwrite` | 脊柱的第 4 阶段调用 |
| 审稿返修 | H | `academic-paper-reviewer`（主）、`nature-reviewer`、`nature-response` | 独立评审的候选执行者 |
| 投稿数据 | I | `nature-data`、`nature-paper-to-patent` | 外部动作须单独授权 |
| 知识组织 | J | `understand-knowledge`、`navi-memory`、`navi-notes`、`obsidian-cli` | 知识层目前为空（差距 G9） |
| 演示汇报 | K | `nature-paper2ppt`、`nature-image2ppt` | — |
| 通用底座 | M | `office-documents`、`pdf`、`docx`、`image-generation` | 被上层调用 |

## 3. 硬门禁（G 组，全部不可自证）

| 门禁 | 触发 | 要求 | 执行者 |
|---|---|---|---|
| G1 引用身份核验 | 稿件进入投稿准备 | 全部引用经外部源核验；未核验须标"尚未完成外部验证" | `nature-ref-verifier` 或 MCP |
| G2 统计与结果校验 | 稿件含定量结果 | 经 `nature-statistics` 审查；结果不得超出数据支持范围 | `nature-statistics` |
| G3 目视就绪门 | 产出 PDF/DOCX | **逐页**检查实际渲染、最小标签物理尺寸、空白页与孤行；编译成功 ≠ 视觉合格 | 脊柱第 5 阶段 |
| G4 独立评审 | 声明"已评审" | 评审者必须独立于撰写者；**自检不算**。缺独立评审只能交"草稿+待审" | `academic-paper-reviewer` / 其他 Agent |
| G5 反捏造 | always | 不生成虚假文献/DOI/数据；相关不表述为因果；缺失标"待确认" | L0 + 脊柱 |
| G6 可复现 | 任何实验结果入稿 | 实验日志含数据版本、代码提交、随机种子；否则不得写入结论 | `nature-experiment-log` |

## 4. 产物契约

各阶段产物落 `research/` 对应层，脊柱不另建平行目录树：

| 脊柱阶段 | 落点 |
|---|---|
| 摄入与清点 | `research/10-data/` |
| 文献与引用 | `research/60-writing/references.md` |
| 贡献与动机 | `research/00-governance/decisions/`（ADR） |
| 统计与绘图 | `research/30-benchmark/`、图源随实验记录 |
| 实验与复现 | `research/50-experiments/` |
| 成稿 | `research/60-writing/` |

## 5. 启用策略（成本控制）

- **主框架非默认入口。** 仅当（a）用户显式点名 PaperSpine，或（b）约定触发词命中，或（c）用户要求"全流程出稿"时启用。
- **局部任务走外接。** 只要一段文字、要一张图、要一次审稿，直接走 G/E/H 的 primary，不启动脊柱。
- **脊柱可中断可续跑**：任一步失败时回退到手工分阶段执行，不因工具失败而废弃整条任务。

## 6. 风险与缓解

| 风险 | 严重度 | 缓解 |
|---|---|---|
| 主框架为 **alpha 未签名** | 高 | 版本固定 `v0.4.0-alpha.1-dev`；禁自动更新；组装包与原始解包留档；记录 SHA-256 |
| 自带 **Web 启动器/MCP 桥缺失** | 高 | 已在 `SKILL.md` 顶部加 HanaAgent 适配块，改为对话内配置；方法学正文不动 |
| 与 `nature-*`/`scipilot` **触发冲突** | 中 | 显式触发 + 分阶段路由裁决；定期巡检 |
| **token 成本高** | 中 | 默认不启用；局部任务不启动脊柱 |
| 单点故障：脊柱坏了全链停 | 中 | L0 决策层与脊柱解耦；可回退手工流程 |

## 7. 当前状态与下一步

**已落地**：外接清单、硬门禁、产物契约、启用策略、风险台账均已成文。

**未落地（须用户开闸或另行授权）**：
- 端到端跑通一次真实论文任务（属科研执行阶段）
- 中文文献通道（CNKI/维普）
- 独立评审者的实际指派机制（候选：`agent-mqb8td2n` 交流者 / `hanako` 皇家卫士）
- 知识层填充（差距 G9）
