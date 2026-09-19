# Claude Fable 5：Anthropic 首个 Mythos 级公开模型

**日期**：2026-06-09 发布 | **整理**：2026-06-10 07:00

---

## 一句话

Anthropic 在 6 月 9 日发布了 Claude Fable 5，这是 Mythos 级模型首次对普通用户开放。此前 Mythos 能力仅限受信任机构使用。Fable 5 与 Mythos 5 共享同一底层架构，但增加了安全护栏（高风险查询自动降级到 Opus 4.8）。

---

## 核心跑分

| 基准 | Fable 5 | Opus 4.8 | GPT-5.5 | Gemini 3.1 Pro |
|------|---------|----------|---------|---------------|
| SWE-Bench Pro | **80.3%** | 69.2% | 58.6% | 54.2% |
| FrontierCode Diamond | **29.3%** | 13.4% | 5.7% | — |
| Terminal-Bench 2.1 | **88.0%** | 82.7% | 83.4% | 70.7% |
| Humanity's Last Exam (无工具) | **59.0%** | 49.8% | 41.4% | — |
| GPQA Diamond | **~95%** | ~93% | ~91% | — |
| ExploitBench | **78.0%** | 40.0% | 34.0% | — |

SWE-Bench Pro 是防污染的编码基准（SWE-Bench Verified 已被确认存在跨模型污染），FrontierCode 是 Cognition 出品的生产级编码测试。Fable 5 在 FrontierCode 上是 Opus 4.8 的 2.2 倍、GPT-5.5 的 5.1 倍。

---

## 实战案例

- **Stripe**：Fable 5 一天内完成 5000 万行 Ruby 代码库迁移，原本需要数月人工工程
- **药物研发**：Mythos 5 将部分药物发现流程加速约 10 倍，能自主选择蛋白质结合位点、执行设计工具、从失败尝试中自我恢复
- **科学假设**：Anthropic 内部研究员在 80% 的情况下更偏好 Mythos 5 生成的生物学假设

---

## 定价与定位

- 输入：$10/M tokens | 输出：$50/M tokens
- 对比：Opus 4.8 是 $5/$25，GPT-5.5 是 $5/$30，DeepSeek V4 Pro 是 $0.40/$1.20
- **性价比分析**：日常编码用 Opus 4.8 更划算（69.2% SWE-Bench Pro，半价）；最难 10-20% 的任务用 Fable 5 值回票价。DeepSeek V4 Pro 在简单任务上性价比极高（$0.40/$1.20，约 70% 的编码能力）

---

## 安全设计

- 网络安全、生物、化学、模型复现等高风险查询自动重定向到 Opus 4.8
- 企业客户数据 30 天保留，不用于模型训练
- Mythos 5（完整版）仅对受信任机构开放

---

## 商业背景

- Anthropic 估值 ~$965B，年化收入 ~$47B（一年前 ~$10B）
- 6 月 1 日提交机密 S-1 文件，分析师预计 10 月 IPO，可能超 $1T
- Claude Code 单独年化收入超 $1B（发布六个月内）
- 6 月 4 日发布博文"When AI builds itself"：Claude 已编写 Anthropic 80% 以上的代码，工程师人均代码产出是 2021-2025 年的 8 倍

---

## 与 ZhouXuan 的关联

- Opus 4.8 刚发布 12 天，Fable 5 就来了一波大升级。如果你在使用 Claude Code 或 API，了解这个代际差有助于判断什么时候该升级模型路由
- SWE-Bench Pro 的防污染设计值得注意：你写论文时遇到的 AI 造假参考文献问题，在基准测试领域同样存在，OpenAI 已承认 SWE-Bench Verified 存在跨模型污染
- Anthropic 递归自我改进的警告（任务时域每 4 个月翻倍）和"只有油门没有刹车"的比喻，与你关注的 AI 工具链自主性方向直接相关
