# Google Gemini Agentic RAG — 多智能体检索增强生成

**来源**: Google Research Blog, 2026-06-05  
**作者**: Cyrus Rashtchian (Research Scientist), Da-Cheng Juan (Engineering Manager)

## 核心创新：Sufficient Context Agent

传统 RAG 搜不到就放弃或瞎猜。Google 的方案加了一个「充分性检查」环节：

- 检索到片段后，先草拟一个中间回答
- Sufficient Context Agent 对比草稿和原问题，判断是否遗漏
- 如果缺信息，生成具体的「缺了什么」反馈，驱动新一轮搜索
- 循环直到信息充分，才交给 Synthesis Agent 生成最终回答

## 架构（多 Agent 流水线）

```
Root Agent → Planner Agent → Query Rewriter → RAG Agent → Sufficient Context Agent → Synthesis Agent
                                                              ↑___________________________|
                                                              信息不足时循环
```

- **Planner Agent**: 把复杂问题拆成子任务，决定查哪些数据源
- **Query Rewriter**: 把自然语言改写成精准搜索词
- **RAG Agent**: 执行检索，支持跨语料库（cross-corpus）
- **Sufficient Context Agent**: 质量检查，判断信息是否充分
- **Synthesis Agent**: 综合生成最终答案

## 实验结果

| 场景 | 准确率 |
|------|--------|
| Vanilla RAG (单语料) | 基线 |
| Agentic RAG (单语料) | +34% |
| Agentic RAG (跨语料, 4个库选1个) | 90.1% |

跨语料场景的延迟仅比单语料多 3%，意味着路由开销很小。

## 一个具体例子

医生查询：「John Doe 膝盖手术后用了什么药、饮食限制、有无过敏反应?」

- 标准 RAG: 找到药物和饮食，过敏信息没找到→要么瞎编要么放弃
- Agentic RAG: 发现缺过敏信息→Sufficient Context Agent 反馈「去找皮疹、不良反应相关记录」→重新搜索→找到→完整回答

## 为什么值得关注

1. **与 ZhouXuan 论文方向相关**：智能系统如何保证回答的可靠性，是这个框架的核心命题
2. **Agent 工具链的参考**：多 Agent 协作 + 循环验证的模式，对于 AgentBox/Hermes 这类系统有架构参考价值
3. **「充分性」概念**：不是追求完美的上下文，而是判断「什么时候够了」，这是一个被低估的工程问题
4. **已在 Gemini Enterprise Agent Platform 公开预览**，有实际产品落地

---

*巡检自学笔记 · 2026-06-10 02:33*
