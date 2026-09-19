# Microsoft SkillOpt：像训练神经网络一样训练 Agent Skills

**来源**：Microsoft Research | arXiv: 2605.23904 | v0.1.0 PyPI (2026-06-02) | MIT License  
**GitHub**：microsoft/SkillOpt | ⭐ 5,737 | 20 contributors  
**项目页**：microsoft.github.io/SkillOpt

---

## 一句话

SkillOpt 把 SKILL.md 当作可训练对象，用"rollout → 反思 → 聚合 → 筛选 → 更新 → 验证"的闭环，在不改模型权重的前提下自动优化 Agent Skill 文档。部署产物是一个 300~2000 token 的精简 `best_skill.md`，推理时零额外调用开销。

---

## 为什么值得关注

ZhouXuan 目前拥有 88+ 个 skill，分布在 5 个平台（Cursor / Codex / Claude Code / HanaAgent / OpenClaw）。这些 skill 全部是人工编写或一次性 LLM 生成的——和所有 agent skill 生态的现状一样。SkillOpt 提出的是一个根本性的范式转换：**Skill 不应该是一次性产物，而应该像模型权重一样在反馈循环中持续进化。**

---

## 核心机制

### 训练闭环

```
初始 skill.md
    ↓
rollout（目标模型执行一批任务，产出生轨迹）
    ↓
reflect（优化器模型分析成败，找出系统性问题）
    ↓
propose（提出 bounded add/delete/replace 编辑）
    ↓
validate（在 held-out 验证集上跑目标模型）
    ↓
如果验证分数提升 → 接受编辑 → 新 skill
如果验证分数下降 → 拒绝编辑 → 进入 rejected buffer（负反馈）
    ↓
下一轮 epoch
```

### 关键设计决策

- **优化器模型 ≠ 目标模型**：用一个强模型（如 GPT-5.5）做优化器，目标模型可以是任意规模（GPT-5.4-mini、Qwen3.5-4B 等都测过）
- **文本学习率预算**：每轮只允许有限 token 量的编辑，防止 skill 膨胀
- **严格验证门控**：不接受任何不提升 held-out 分数的编辑
- **Rejected buffer**：失败编辑被保留作为负反馈，避免重复犯错
- **Slow/meta update**：跨 epoch 保持长期规律性

### 部署零成本

优化后的 `best_skill.md` 直接替换原 skill，推理时不需要额外的优化器调用。这是 SkillOpt 与 prompt optimization 方法（如 TextGrad、GEPA）的本质区别。

---

## 性能数据

| 场景 | vs no-skill baseline | vs 最佳竞品 |
|------|---------------------|------------|
| GPT-5.5 + 直接对话 | +23.5 分 | 全胜/平局 |
| GPT-5.5 + Codex CLI | +24.8 分 | 全胜/平局 |
| GPT-5.5 + Claude Code | +19.1 分 | 全胜/平局 |

在全部 **52 个 (模型 × benchmark × harness) 组合**中，SkillOpt 对每个 cell 都是 best or tied。跨模型规模、跨 harness（Codex ↔ Claude Code）、跨近似 benchmark 均可迁移。

---

## SkillOpt-Sleep：夜间自我进化

这是 SkillOpt 最接近 ZhouXuan 现有体系的部分。6 月 8 日发布的 **SkillOpt-Sleep** 给本地 coding agent 加了一个"睡眠周期"：

```
采集会话 transcript → 挖掘重复任务 → 离线回放
    → 整合（反思 → bounded edit → 在真实 held-out 任务上验证门控）
    → 生成提案 → 用户审核 → 采纳
```

已有插件支持三个平台：
- **Claude Code**：`/plugin marketplace add` → `/sleep`
- **Codex**：`bash plugins/codex/install.sh` → `/sleep`
- **Copilot**：MCP server 注册

在公开的 gbrain-evals skillopt-v1 benchmark 上，deficient skills 从 0.00 提升到 1.00（held-out），4 个 seed 全部复现，gate 机制成功拦截了所有回归。

---

## 与 ZhouXuan 现有体系的关系

| 维度 | 现有方案 | SkillOpt 的可能角色 |
|------|---------|-------------------|
| Skill 创建 | 人工编写 / install_skill | 自动化优化迭代 |
| Skill 演进 | continuous-learning-v2（instinct → skill） | 系统化训练式优化 |
| 质量控制 | skill-stocktake（审计） | 验证门控（硬性 held-out 分） |
| 夜间学习 | 巡检 + 自学笔记 | Sleep 周期（更结构化） |
| 跨平台 | 人工同步 5 个平台 | 优化结果可跨 harness 迁移 |

**最自然的切入点**：在 Codex（ZhouXuan 的元认知引擎）或 Claude Code（重型工程）上尝试 SkillOpt-Sleep，看看自动优化的 skill 能否在 ZhouXuan 实际使用的 benchmark/任务上战胜手写版本。

---

## 底层哲学

SkillOpt 背后的想法很朴素：既然我们把神经网络的权重当作可训练状态、用梯度下降和验证集来优化它，那为什么对 agent 的 skill 文档不能做同样的事？

区别只在于优化空间从连续参数空间变成了离散文本空间——但优化纪律应该是一样的：有训练循环、有验证门控、有学习率控制、有负反馈缓冲。

论文里有一个很有意思的 observation：传统 prompt optimization 方法（TextGrad、GEPA 等）的问题在于它们缺乏"硬性门控"——一个看起来很好的编辑可能在实际 held-out 测试中表现更差。SkillOpt 的 strict validation gate 解决了这个问题。

---

## 局限与风险

- 依赖于一个足够强的优化器模型（论文用 GPT-5.5），低成本模型做优化器效果未知
- 验证集构造是关键：如果验证集不代表实际使用场景，优化方向会偏
- Sleep 模式需要积累足够的会话轨迹才有意义
- 当前版本（v0.1.0）仍标注 Alpha，生产稳定性待观察

---

*创建于 2026-06-12 00:05 巡检 | 分类：Agent 工具链 / Skill 工程*
