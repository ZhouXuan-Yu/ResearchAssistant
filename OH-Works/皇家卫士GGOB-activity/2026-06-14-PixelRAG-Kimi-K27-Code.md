# PixelRAG + Kimi K2.7-Code 速览

> 巡检日期：2026-06-14 00:04
> 事件日期：2026-06-12 发布

---

## 一、PixelRAG：视觉截图替代文本解析的 RAG 新范式

**发布方**：UC Berkeley、Princeton、EPFL、Databricks 联合研究
**论文**：[GitHub StarTrail-org/PixelRAG](https://github.com/StarTrail-org/PixelRAG)

### 核心思路

传统 RAG 流程：网页/PDF → 文本解析 → 向量检索 → LLM 生成。PixelRAG 跳过文本解析，直接将页面渲染为截图，建立视觉索引，用 VLM（视觉语言模型）读取检索到的截图 tile。

**关键数据**：
- 测试规模：3000万截图 tile（覆盖全部 Wikipedia）
- SimpleQA 准确率：78.8% vs 文本解析 71.6%（+7.2pp）
- 结构化表格查询：48.8% vs 42.5%（+6.3pp）
- Agent token 成本：3.6M prompt tokens vs 文本检索 37.5M（**降 10 倍**）
- 六项基准全面超越文本 RAG，最高准确率提升 18.1%

### 技术架构（四阶段）

1. **渲染**：将源材料渲染为截图 tile
2. **视觉嵌入**：建立保留布局、表格结构、设计信号的视觉索引
3. **检索**：查询时检索最相关 tile
4. **VLM 读取**：将 tile 送入视觉语言模型，同时解读视觉和文本信息

### 关键洞察

- VLM 可以像人类一样"看"渲染后的页面，保留布局和结构信息
- 需要 Qwen3-VL-4B 级别以上模型才能获益，小模型落后文本检索 12.5pp+
- 作者建议混合部署（hybrid）为最实用近中期路径，视觉检索叠加在现有文本系统之上

### 与用户方向的关联

用户正在撰写深度学习智能导航论文，PixelRAG 的视觉检索思路（绕过文本解析直接处理视觉信号）与视觉导航的"直接感知"范式有共通之处：都强调保留原始视觉信息而非过度抽象化。

---

## 二、Kimi K2.7-Code：Moonshot 开源编码专用模型

**发布方**：Moonshot AI（月之暗面）
**发布日期**：2026-06-12
**权重**：[Hugging Face moonshotai/Kimi-K2.7-Code](https://huggingface.co/moonshotai/Kimi-K2.7-Code)

### 模型规格

| 属性 | 值 |
|------|-----|
| 总参数 | 1T |
| 活跃参数 | 32B（MoE 架构，384 experts） |
| 上下文窗口 | 256K |
| 许可证 | Modified MIT（开源） |
| API 价格 | $0.95/M input, $4.00/M output |
| 缓存命中 | $0.19/M input |

### 基准对比（官方数据）

| 基准 | K2.6 | K2.7-Code | GPT-5.5 | Claude Opus 4.8 | K2.7 vs K2.6 |
|------|------|-----------|---------|-----------------|--------------|
| Kimi Code Bench v2 | 50.9 | 62.0 | 69.0 | 67.4 | +21.8% |
| Program Bench | 48.3 | 53.6 | 69.1 | 63.8 | +11.0% |
| MLS Bench Lite | 26.7 | 35.1 | 35.5 | 42.8 | +31.5% |
| MCP Atlas | 69.4 | 76.0 | 79.4 | 81.3 | +9.5% |
| MCP Mark Verified | 72.8 | 81.1 | 92.9 | 76.4 | +11.4% |

### 关键特点

1. **推理 token 减少 30%**：专为"不过度思考"训练，减少推理开销
2. **长视野编码**：擅长规划、编辑、工具调用、多步调试
3. **价格杀手**：输出价格仅为 Claude Fable 5 的 1/12
4. **必须开启思考模式**：不支持 non-thinking mode，固定 temperature 1.0
5. **即将到来**：6x 高速模式、原生 INT4 量化

### 市场定位

K2.7-Code 在标准编码基准上落后 GPT-5.5 和 Opus 4.8，但在实际 Agent 场景（MCP Mark Verified）上击败 Opus 4.8。这反映了"专用优化 vs 通用能力"的路线选择：Moonshot 选择在编码 Agent 领域做深做透，而非追求全面超越。

### 价格对比

| 模型 | Input/M | Output/M |
|------|---------|----------|
| **Kimi K2.7-Code** | **$0.95** | **$4.00** |
| GPT-5.5 | $5.00 | $30.00 |
| Claude Opus 4.8 | $5.00 | $25.00 |
| Claude Fable 5 | $10.00 | $50.00 |

---

## 三、附加信号：Claude API 6/15 退役提醒

Anthropic 将于 2026-06-15 退役两个原始 Claude 4 模型：
- `claude-sonnet-4`（API 字符串）
- 对应的旧版模型

使用这些字符串的代码需要迁移到新版本。对 DeepSeek 用户影响有限。

---

## 四、与其他近期文档的关联

| 文档 | 关联 |
|------|------|
| CVPR 2026 VLN 论文五条支线 | PixelRAG 的"视觉直接感知"与视觉导航"直接感知"范式共通 |
| AgenticNav | K2.7-Code 的 Agent 工具调用能力可支撑 Agentic 工作流 |
| Anthropic Fable5 出口管制 | K2.7-Code 作为开源替代在价格和可用性上形成对照 |
| Recursive 自动化研究 | K2.7-Code 的长视野编码能力与自动化研究流程互补 |
