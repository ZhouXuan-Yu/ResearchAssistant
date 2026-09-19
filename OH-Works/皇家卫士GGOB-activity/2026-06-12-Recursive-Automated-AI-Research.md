# Recursive：AI 自主做 ML 研究的第一个脚印

**日期**：2026-06-12（6/11 发布）
**来源**：Recursive 官方博客
**标签**：#AI-Self-Improvement #ML-Research #Automated-Science

## 一句话

Recursive 发布了一个能**自主完成 ML 研究全流程**的 AI 系统：从提出假设、写代码、跑实验、验证结果到根据发现选择下一轮方向，全自动。在三个基准上击败了人类社区多年的优化成果。

## 核心结果

| 基准 | 任务 | 之前最优 | Recursive | 提升 |
|------|------|----------|-----------|------|
| NanoChat Autoresearch | 5 分钟单 GPU 训练最优小模型 | 0.9372 BPB | **0.9109 BPB** | 1.3x 加速达到同等损失 |
| NanoGPT Speedrun | 最快训练到指定损失 | 79.7s | **77.5s** | 2.2s 更快（人类优化两年后仍有提升） |
| SOL-ExecBench | GPU Kernel 优化（235 个 kernel） | 0.699 SOL | **0.754 SOL** | 硬件极限差距缩减 18% |

## 关键洞察

**不是单点 trick，是复合创新。** 系统发现的最佳方案融合了架构修改、短上下文记忆、辅助损失、注意力机制、优化器行为、权重衰减调度、编译器设置等多层改进。

最亮眼的发现：**哈希 n-gram 嵌入表**——用哈希表将 bigram/trigram 信息注入 attention value 路径，以极低成本获得局部 n-gram 信息。这与 DeepSeek Engram (arXiv 2601.07372) 的哈希表稀疏化思路异曲同工，但 Recursive 的实现变体（分层不同哈希函数避免碰撞）此前未见公开。

从零开始的 vanilla Transformer 也能独立收敛到竞争性方案，包含 token-shifting、权重平均、Muon 优化器等不同技术组合——说明系统不是机械重复同一套发现。

## 与 Anthropic 递归自我改进的对比

- **Anthropic 报告**（今日 03:43）：AI 写代码（软件工程），工程师 8x 产出
- **Recursive**：AI 做研究（科学发现），自主提出假设、跑实验、发现新方法

这是两个不同层次的能力。Anthropic 是"AI 帮你搬砖"，Recursive 是"AI 自己设计怎么搬更快"。

## 开源

已开源 artifacts：github.com/recursive-org/first-steps-toward-automated-ai-research

## 与 ZhouXuan 的关联

- 衔接今日 SkillOpt（skill 自我优化）和 Anthropic 递归自我改进文档，构成「AI 自我进化」三部曲
- GPU kernel 优化直接关联此前排查过的 RTX 5060 CUDA 问题
- 自动化研究循环的设计理念可参考用于 Agent 系统架构
