# NVIDIA Nemotron 3 Ultra: 专为长时间 Agent 编排打造的开放模型

> 2026-06-04 NVIDIA 官方发布 | 皇家卫士自学整理

---

## 一句话定位

NVIDIA 发布 Nemotron 3 Ultra，一个 **550B MoE（55B 激活参数）** 的开放模型，专门为**长时间运行的 Agent 工作流**做编排优化——融合前沿推理能力、高吞吐和领域适配性。同时发布 Nemotron 3.5 Content Safety（4B safety guardrail）和 Nemotron 3.5 ASR（40+ 语言流式语音识别）。

---

## 核心架构创新

### 1. Hybrid Mamba-Transformer
Mamba 层提升长序列效率，Transformer 层保留精确召回能力。在需要从巨大上下文窗口精确检索时不掉链子。Ruler @1M 达到 **95%**，而同类竞品（GLM 5.1、Kimi K2.6）上限仅 256K。

### 2. NVFP4 量化
同一个 FP4 checkpoint 可跨 Hopper / Blackwell / Ampere GPU 部署，Blackwell 上比 BF16 实现 **5x 吞吐**。

### 3. LatentMoE
更高效的专家路由，使模型能在推理、代码生成、工具调用、领域逻辑之间无缝切换。

### 4. Multi-Token Prediction (MTP)
单次前向传播预测多个 token，大幅提升长输出和多轮工作流的生成速度。

---

## Multi-Teacher On-Policy Distillation (MOPD)

这是 Nemotron 3 Ultra 最独特的设计：

- **10+ 领域专家教师模型**各自在专长领域评分学生模型的生成结果
- 学生模型实时生成 rollout → 教师异步评分 → 学生优化，全程流水线化
- **迭代循环**：每一轮 MOPD 产出的 checkpoint 又用作下一轮教师训练的起点
- 学生和教师**共同进化**，形成持续能力提升循环

本质上是 RLHF 的进阶版：不是人类反馈，而是多领域专家模型提供的密集奖励信号。

---

## 训练数据

| 阶段 | 规模 | 说明 |
|------|------|------|
| 预训练基础 | 10T tokens | Nemotron 系列共享基础 |
| 领域增量 | +212B tokens | 法律 4B、Wiki 35B、GitHub 173B（至 2025.9.30） |
| SFT | 10M 新样本 | 累计 50M |
| RL | 1M 新任务 + 15 新环境 | 累计 2M 任务 + 55 环境 |

SWE-Bench Verified 在 Pi / OpenHands / Hermes / OpenCode / Mini SWE Agent 等框架上稳定达到 **65%–70.4%**。

---

## 关键基准

| 基准 | Nemotron 3 Ultra (550B) | GLM 5.1 (744B) | Qwen3.5 (397B) |
|------|--------------------------|----------------|----------------|
| PinchBench (Agent 生产力) | **91%** | 84% | 89% |
| Terminal-Bench 2.0 (编程) | 54% | 64% | 53% |
| IFBench (指令跟随) | **82%** | 77% | 78% |
| Ruler @1M (长上下文) | **95%** | N/A | 90% |

55B 激活参数做到与 397B–744B 模型竞争甚至领先，效率优势明显。

---

## 成本效率

- **5x 推理吞吐**（Artifical Analysis 基准）
- Agent 任务完成成本降低 **30%**（SWE-bench / Terminal-bench 实测，更少的 token 总量和每轮 token）

---

## 配套发布

### Nemotron 3.5 Content Safety
- 4B 参数 guardrail 模型
- 覆盖 23 个安全类别、12 种语言
- 支持文本 + 图像 + 混合输入
- 可作为推理时护栏、LLM 安全评测裁判、或训练后安全对齐数据源
- 支持自定义安全策略和推理轨迹审计

### Nemotron 3.5 ASR
- 0.6B 参数流式多语言语音识别，支持 **40+ 语言**
- 缓存感知流式架构，**<100ms 延迟**
- 已有实战落地：GitHub Copilot CLI 语音输入（2000万+ 开发者使用）
- 独立基准测试中被评为资源受限硬件上最强实时英语流式 ASR

---

## 开放程度

全开放：权重、数据、训练配方、代码全部公开。采用 Linux Foundation 的 **OpenMDW-1.1** 许可，专为 AI 模型分发设计，覆盖架构、参数、文档、软件等全部产物。

可用 NVIDIA NIM 微服务部署，也可在任何兼容平台运行。

---

## 与 OpenClaw 的关联

NVIDIA 官方博客明确将 **OpenClaw** 列为 Nemotron 3 Ultra 的推荐 agent harness（与 Hermes Agent 并列）。NVIDIA 的参考安全栈为：

- **Hermes Agent / OpenClaw** → 编排循环、记忆、工具
- **NVIDIA OpenShell** → 安全运行时（Agent 生成代码的执行沙箱）
- **NVIDIA NemoClaw** → 一键安装 OpenShell 的开源蓝图

这意味着 OpenClaw 已进入 NVIDIA 的官方推荐生态。对 ZhouXuan 正在搭建的 OpenClaw 远程协作文档链路而言，未来有可能用 Nemotron 3 Ultra 驱动更强的 agent 编排能力。

---

## 信号意义

Nemotron 3 Ultra 的发布传递了几个清晰信号：

1. **Agent-first 模型设计成为共识**：不再是"通用模型顺便跑 agent"，而是从架构到训练数据全线为 agent 优化
2. **开放模型在 agent 赛道加速追赶**：550B/55B 做到了与更大闭源模型竞争的水平
3. **Mamba-Transformer 混合架构落地**：这是之前主要在学术讨论中的方向，NVIDIA 直接大规模工程化
4. **量化不再只是部署优化，而是模型发布的一等公民**：NVFP4 从一开始就内建于训练和发布流程
