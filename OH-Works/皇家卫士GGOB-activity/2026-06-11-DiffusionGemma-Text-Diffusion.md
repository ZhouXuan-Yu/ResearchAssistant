# DiffusionGemma：文本生成的 Diffusion 范式转移

> Google DeepMind 2026-06-10 发布 | Apache 2.0 开源 | 26B MoE（3.8B 激活）

## 一句话

Google 把图像 diffusion 的"并行去噪"思路搬到了文本生成上。不再逐 token 打字，而是一次生成 256 token 的整块文本再迭代精炼。速度 4x，消费级 GPU 可跑。

## 为什么这件事重要

目前所有主流 LLM 都是自回归的（autoregressive）：一个 token 接一个 token，从左到右。云端靠批处理掩盖延迟，但本地推理时 GPU 大量时间在等下一个 token，计算单元闲置。

DiffusionGemma 把这个逻辑反过来：一次性给 GPU 塞 256 个 token 的工作量，让 tensor core 吃饱。结果是本地推理速度质的飞跃。

## 核心技术

### Block-Autoregressive Diffusion

分三步走：

1. **Canvas 初始化**：随机初始化 256 个 token 占位符
2. **迭代去噪**：多轮 forward pass，每轮锁定高置信度 token，用它们做上下文继续精炼其余 token
3. **收敛输出**：整块文本收敛后提交到 KV cache，开启下一个 256-token 块

每轮 forward pass 产出 15-20 个确定的 token，256 token 的 canvas 最终收敛。

### Encoder-Denoiser 架构

基于 Gemma 4 26B-A4B 骨干，加了一个 diffusion head：

- **Encoder**（causal attention）：处理 prompt，生成 KV cache
- **Denoiser**（bidirectional attention）：在 canvas 上做双向注意力去噪

妙处在于 Encoder 和 Denoiser 共享同一个 Gemma 4 权重，只是 attention mask 不同。不需要两套模型。

### Uniform State Diffusion

高置信度 token 锁定后帮助相邻位置去噪，整段文本在多轮迭代中逐步"显影"。类似图像 diffusion 从噪声到清晰图片的过程，但应用于离散 token 空间。

### 自适应停止

不是固定步数，模型会在早期收敛时自动终止去噪过程，避免浪费计算。

## 性能数据

| 硬件 | 速度 |
|------|------|
| NVIDIA H100 | 1000+ tok/s |
| RTX 5090 | 700+ tok/s |
| RTX 4090（量化） | 可运行（18GB VRAM 内） |

- 26B 总参数，仅 3.8B 激活（MoE 8/128 experts）
- 256K 上下文窗口
- 原生支持 NVFP4（4-bit 浮点），近无损加速
- 支持多模态输入（文本 + 图像 + 视频）

## 自回归做不到的事

Bidirectional attention 带来的独特能力：

- **实时自纠错**：发现低置信度 token 可以回退重来，自回归模型写出去就改不了
- **代码 infilling**：同时看前后文补全中间
- **复杂格式**：Markdown 嵌套、数学公式等需要"看到全局"的结构
- **数独**：Unsloth 微调后能解数独（自回归模型极难做到，因为每格依赖后续格子）

## 与标准 Gemma 4 的取舍

DiffusionGemma 输出质量低于同尺寸的自回归 Gemma 4。Google 明确说：追求质量用标准 Gemma 4，追求速度用 DiffusionGemma。适合的场景是实时交互、本地编辑、快速迭代。

## 对 ZhouXuan 的意义

1. **llama.cpp 支持即将到来**：官方公告明确写了"arriving soon"。一旦 llama.cpp 集成，Ollama 就能跑
2. **RTX 5060 兼容性**：虽然官方 benchmark 提到的是 4090/5090，但 3.8B 激活参数 + NVFP4 量化意味着 8GB VRAM 也有一战之力
3. **本地实时交互**：如果能跑起来，本地对话体验会从"等几秒出一段"变成"瞬间出整段"，交互模式完全不同
4. **论文相关**：Diffusion 用于离散序列生成是前沿方向，与深度学习、生成模型领域直接挂钩

## 快速上手

- 权重：[Hugging Face](https://huggingface.co/google/diffusiongemma-26B-A4B-it)（Apache 2.0）
- 推理：MLX / vLLM（Red Hat 集成）/ HuggingFace Transformers
- 微调：Unsloth / NVIDIA NeMo / Hackable Diffusion（JAX）
- 深入阅读：[A Visual Guide to DiffusionGemma](https://newsletter.maartengrootendorst.com/p/a-visual-guide-to-diffusiongemma) by Maarten Grootendorst

## 今日另一则值得注意

**Visa × OpenAI**（6/11）：Visa 将支付网络嵌入 ChatGPT，AI Agent 可自主完成购买。支持消费限额、审批步骤、商户白名单。这意味着 Agent 经济从"推荐"迈入"执行"阶段。Mastercard 也在跟进，场景偏 B 端（企业 Agent 采购广告等服务）。

---

*整理时间：2026-06-11 09:30 | 来源：Google Blog、MarkTechPost、Maarten Grootendorst Newsletter*
