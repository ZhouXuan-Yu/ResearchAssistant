# 整合记录：PaperSpine5（paper-spine）

> 执行：agent-mu42qzfz｜日期：2026-09-18｜状态：**已安装并通过冒烟测试；端到端未验证**

## 1. 来源与完整性

| 项目 | 值 |
|---|---|
| 上游仓库 | `github.com/WUBING2023/PaperSpine`（原版；另有 `PKUMichael/PaperSpine` fork）|
| 发布版本 | `v0.4.0-alpha.1-dev`，2026-09-15 发布，**prerelease（alpha）** |
| 取用资产 | `paperspine5-skill-0.4.0-alpha.1-dev.zip`（715,991 B）|
| SHA-256 | `3fe8f600919714c8…`，**与官方 `checksums.sha256` 校验一致** |
| 许可证 | **MIT License**（Copyright (c) 2026 PaperSpine contributors）|

## 2. 审计结论（准入前）

| 检查项 | 结果 |
|---|---|
| 遥测 | **本地账本**（`paper_rewriting_output/usage_ledger.jsonl`），不外传；不可得时强制写 `telemetry_unavailable` |
| 自动更新 | **默认关闭**；更新须重跑安装器，保留任务数据 |
| 外部动作 | 技能自述"不授权投稿、上传私有材料、付款或外部联系" |
| 私有材料 | 默认本地留存，除非显式授权共享 |
| 反捏造纪律 | 明文禁止虚构数据/指标/引用/图表/作者/伦理/资助/评审结论；要求引用身份与语境双重核验 |
| 自检与独立评审 | 明确"worker 自检不等于独立评审"；缺独立评审时只能交"草稿+待审"，不得称已完成终稿 |

**四项治理红线（来源/许可/自动更新/外部上传）全部合规。**

## 3. 安装结果

| 项目 | 值 |
|---|---|
| 安装路径 | `C:\Users\ZhouXuan\.hanako\skills\paper-spine\` |
| 包内容 | `SKILL.md`、`agents/`(7)、`references/`(85)、`scripts/`(52)、`HANA-ADAPTATION.md` |
| 上游 SKILL.md | **逐字未改**，便于日后与上游 diff |
| 安全审查 | 通过 |

### 3.1 冒烟测试（Python 3.14.0）

- **52 个脚本全部 `compileall` 通过**（无语法/版本不兼容）
- 10 个入口脚本 `--help` 全部 `rc=0`：`artifact_check`、`citation_verification_en`、`citation_bank_check`、`figure_story_check`、`figure_reference_check`、`visual_readiness_check`、`usage_ledger`、`reference_inventory`、`contribution_check`、`results_validation_check`
- 结论：**脚本层在本平台可运行**；未验证的是多脚本串联的完整任务链

## 4. 已知缺口（不得声称已解决）

1. **Web 摄入界面 / MCP 桥不可用。** 上游首步要求启动自带启动器（`launch --no-open`）并经 `paperspine_open_task`/`host wait`/`skill_bridge.web_path` 交互；HanaAgent 无此运行时。
   → 处置：配置与选择阶段改为**对话内文本确认 + 落盘 Markdown**，已写入 `HANA-ADAPTATION.md`。
2. **端到端任务链未跑通验证。** 完整"从材料到成稿"链路属科研执行阶段产物，当前 Foundation Stage 未开闸，故只做脚本级冒烟。
3. **alpha 预发布、无密码学签名。** 上游自述当前为 alpha，无独立签名。

## 5. 体系融合（避免双重调度）

- **分类**：`skill-taxonomy.yaml` 登记为 `L_orchestration`，`usage: [编排, 生产]`，`role: secondary`
  - 归 L 而非 G 的理由：其主产物是**整篇论文**（跨 A→I 全链），不是单阶段文本
- **路由**：`routing-rules.yaml` 的 `L_orchestration.secondary` 加入 `paper-spine`；
  新增意图触发词 `paperspine / 论文全流程 / 从零写一篇论文 / 全流程写论文 / 端到端出稿`
- **冲突裁决**：单点写作 → `nature-writing`；数据图 → `scipilot-figure-skill`；机制图/图形摘要 → `nature-figure`；
  模拟审稿 → `academic-paper-reviewer`。**paper-spine 只在用户显式要求时启用，不抢上述触发。**
- **校验**：`check_taxonomy.py` 复跑通过 → 启用 145 技能，**未分类 0，一致性问题 0**

## 6. 回滚

```powershell
Remove-Item -Recurse -Force "C:\Users\ZhouXuan\.hanako\skills\paper-spine"
```

并还原两处改动：
- `foundation/routing/skill-taxonomy.yaml` 中的 `paper-spine` 条目
- `foundation/routing/routing-rules.yaml` 中的 secondary 项与意图项

备份副本留存于 `foundation/packages/paper-spine/`（组装包）与
`foundation/external/paper-spine-skill/`（原始解包）。

## 7. 引入价值（我认为的实际增益）

1. **科研绘图流程**（`scientific-figure-workflow.md`，38KB）：从"看参考图→拆解结构与编码→映射到本研究数据→目视就绪门"的完整方法论，含**禁止把索引构造或相关性渲染成因果路径**等编码规范。这是现有 `nature-figure`/`scipilot` 未覆盖的深度。
2. **目视就绪门**（`visual-readiness-gate.md`）：逐页检查 PDF/Word 实际渲染、最小标签的物理尺寸、空白页与孤行，且明确"TeX 编译成功不等于视觉合格"。直击我体系里"构建成功即视为完成"的盲点。
3. **引用身份 + 语境双重核验**：与既有 `nature-ref-verifier` 互补。
4. **编排门控思想**：可作为 `research-os-router` 质量门禁的外部参照实现。
