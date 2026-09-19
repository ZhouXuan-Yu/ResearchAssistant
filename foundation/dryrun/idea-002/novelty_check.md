# 新颖性核验（novelty_check）— 演练 idea-002

> 产出技能：`idea-forge`（S1）｜核验层级：**仅摘要/题录层**，未读全文
> 检索来源：academic-search MCP（CrossRef / PubMed / arXiv），返回 10 条

## 逐条核验表

| 候选 | 最近邻（含标识） | 来源层级 | 差异点归类 | 差异点（一句） | 核验状态 |
|---|---|---|---|---|---|
| C1 | Faithfulness-Aware Multi-Objective Context Ranking for RAG｜`10.20944/preprints202512.1983.v1`（2025） | 预印本 | **方法 + 评测** | 该工作优化上下文排序层忠实度；C1 问"生成侧区域级归因能否被独立判决性测试判真伪" | **合格** |
| C2 | When Image and Text Disagree: Cross-Modal Evidence Conflict in MM-RAG｜`10.18653/v1/2026.magmar-main.3`（MAGMaR 2026） | 工作坊论文 | **方法** | 该工作刻画跨模态证据冲突；C2 问"冲突能否定位到证据源级且随注入侧翻转" | **待核**（未读全文，无法确认该文是否已含定位能力） |
| C3 | Controlled Evaluation of Graph and Multimodal Augmentation in RAG for Document QA｜arXiv:2607.16604（2026） | 预印本 | **无** | 该文已完成"多模态增益可能源自文本泄漏 / 原始精度高估可归因性能"这一核心论断 | **不合格（已排除）** |

## 关键证据（C3 的排除依据，逐字引用）

> *"…apparent multimodal gains are sensitive to textual leakage. Programmatic checks reveal answer recoverability from captions, corpus text, and model responses generated without complete gold evidence. …raw accuracy can overstate retrieval-attributable performance."*
> —— arXiv:2607.16604 摘要

该引文直接覆盖 C3 的问题设定，故 C3 不给推荐。

## 判定汇总

| 候选 | 新颖性 | 可行性 | 可验证性 | 是否进入推荐 |
|---|---|---|---|---|
| C1 | 合格 | 合格 | 合格 | ✅ 第 1 |
| C2 | **待核** | 合格 | 合格 | ✅ 第 2（须带待核项） |
| C3 | **不合格** | 未评估 | 未评估 | ❌ 已排除 |

## 未完成核验（随产物交付）

1. C1/C2 最近邻**未读全文**：不得据此声称"此前无人研究"；C2 的新颖性因此只到"待核"。
2. 仅一次定向检索，**未做系统检索**；"检索未覆盖 ≠ 不存在"。
3. 数据集/基准许可未核实。
4. 算力与时间估计未校准。
5. C1 的扰动设计可能引入整体退化混杂，需先做对照实验定标。

## 结论

- 可进入 S2 的候选：**C1（优先）、C2（带待核项）**。
- **不代用户选题**：最终由用户决定；也可选择"暂不做"。
- 若用户希望改为在自己的方向上跑本技能，需先提供**约束**（可用数据、算力、时间、是否允许做实验）——缺约束时本技能按规则**先问不猜**。
