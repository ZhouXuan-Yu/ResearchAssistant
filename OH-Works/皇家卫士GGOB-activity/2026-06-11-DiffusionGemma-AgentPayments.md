# 2026-06-11 晨间速览：DiffusionGemma + AI Agent 支付落地

## Google DiffusionGemma：文本生成的扩散范式（6/10 发布）

Google DeepMind 发布 DiffusionGemma，一个 26B MoE 实验性开源模型，核心理念是把图像扩散模型的方法搬到文本生成上。

### 技术原理

传统自回归 LLM 像打字机，逐 token 从左到右生成。本地推理时 GPU 大部分时间在等下一个 token，硬件利用率极低。DiffusionGemma 反过来：一次性起草 256 token 的整个段落，多轮迭代精修，相当于把打字机换成印刷机。

流程：
1. 初始化为随机 token 画布
2. 多轮迭代，锁定正确 token 并以此为上下文精修其余
3. 收敛到高质量输出

### 关键数据

| 指标 | 数值 |
|------|------|
| 总参数 | 26B（MoE） |
| 激活参数 | 仅 3.8B |
| 推理速度 | H100 上 1000+ tok/s，RTX 5090 上 700+ tok/s |
| VRAM 需求 | 量化后约 18GB |
| 并行生成 | 每次前向 256 token |
| 许可证 | Apache 2.0 |
| 双向注意力 | 每个 token 可关注所有其他 token |

### 质量取舍

速度优先，输出质量低于标准 Gemma 4。适合速度关键场景（实时编辑、代码补全、非线性文本结构），不适合追求最高质量的场景。可通过微调针对性提升——Unsloth 微调后能解数独（自回归模型弱项，因依赖双向依赖）。

### 生态支持

- 已支持：MLX、vLLM（Red Hat 协作）、HuggingFace Transformers、Unsloth、NVIDIA NeMo
- 即将支持：llama.cpp
- 一旦 llama.cpp 支持到位，Ollama 大概率跟进

### 对本地部署的意义

ZhouXuan 的 RTX 5060 Laptop（约 8GB VRAM）目前装不下 DiffusionGemma 的 18GB 量化需求。但范式意义大于即时可用性：
- 扩散文本生成是全新的推理效率路径
- 如果这条路走通，未来可能出现更小的扩散 LLM
- llama.cpp/Ollama 支持落地后，CPU offloading 可能降低硬件门槛
- 与 ZhouXuan 关注的本地模型生态直接相关

---

## Visa × OpenAI：AI Agent 正式进入支付网络（6/11）

Visa 宣布将其支付网络嵌入 ChatGPT，AI Agent 现可独立完成购物和交易。

### 机制

- 用户在 ChatGPT 中绑定 Visa 卡
- Agent 不仅推荐产品，直接完成购买
- 适用所有接受 Visa 的商户（不限特定零售商）
- 风控：消费限额、审批步骤、商户白名单
- Mastercard 也在推进类似功能（B2B 场景）

### 为什么重要

这是 "Chat is dead" 超级应用战略的实质性落地步骤。Agent 从信息层（推荐、搜索、总结）进入交易层（下单、支付），从工具变成经济行为主体。OpenAI 提供决策和交互能力，Visa 提供支付授权和反欺诈基础设施。

---

## 两件事的交叉点

DiffusionGemma 让本地 AI 跑得更快，Visa 集成让云端 AI 做得更多。

一条线是本地推理效率的革命性尝试（扩散替代自回归），另一条线是 AI Agent 从对话界面向经济行为的跨越。两条线共同指向同一个方向：2026 年中，AI 正在同时突破「跑得动」和「用得着」的边界。
