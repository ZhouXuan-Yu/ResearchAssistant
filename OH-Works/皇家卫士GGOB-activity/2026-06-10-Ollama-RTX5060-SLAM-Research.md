# 2026-06-10 晨间巡检自学笔记

## 一、Ollama 已正式支持 RTX 5060

Ollama 官方 GPU 支持文档已列出 RTX 5060（Compute Capability 12.0，Blackwell 架构），不再需要 Vulkan 后端绕行。

关键信息：
- RTX 5060 于 2026-05-19 发布，MSRP $299
- 8GB GDDR7，448 GB/s 带宽
- 7B 模型 Q4 约 55 tok/s（Qwen3 7B），流畅运行
- 14B 模型 Q4 需要 ~8.9GB，8GB 显存放不下，只能 Q2 或 CPU offload
- 安装 NVIDIA 驱动 560+ 后 `winget install Ollama.Ollama` 即可自动检测

> ZhouXuan 之前遇到 Ollama 无法识别 RTX 5060 Laptop GPU 的问题（尝试了 Vulkan、CUDA 后端切换、模型调整），现在官方已正式支持，升级 Ollama 版本后应能直接使用 CUDA 后端。

## 二、深度学习 SLAM 最新研究（2026）

与论文方向「基于深度学习的智能导航和识别系统」直接相关：

### 2.1 MGS-SLAM（2026，ICCVM）
**Monocular 3D Gaussian Splatting SLAM with Significance-Guided Pruning**

核心思路：
- 提出 significance-guided pruning 策略，综合 visibility count、opacity、volume coefficient 等多维度指标评估每个 Gaussian 的重要性
- frame-to-model 管线，滑动窗口内联合优化相机位姿和 3D Gaussians
- 在线单目深度估计模型初始化 Gaussian 属性
- 在 Replica 和 TUM 数据集上达到 SOTA 跟踪精度和渲染质量

### 2.2 LeanGate（2026-04，arXiv:2604.08718）
**Accelerating Transformer-Based Monocular SLAM via Geometric Utility Scoring**

核心思路：
- 解决 GFM-based SLAM（如 MASt3R-SLAM）的计算冗余问题
- 在昂贵的 GFM 特征提取之前，用轻量前馈网络预测帧的 geometric utility score
- 过滤 90%+ 的冗余帧，端到端吞吐量提升 5×，跟踪 FLOPs 减少 85%+
- 0.5M ScanNet++ 样本训练，跨数据集泛化良好

### 研究趋势小结

3D Gaussian Splatting + SLAM 正在成为单目场景重建的主流路线，Geometric Foundation Models（DUSt3R、MASt3R、VGGT）作为前端也日趋成熟。关键瓶颈从「能不能做」转向「如何在资源受限平台上实时运行」，LeanGate 的 predictive gating 思路值得关注。
