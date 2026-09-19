# AgenticNav：把视觉语言导航重塑为 Agent 工具调用

**来源**：arXiv 2606.10577，2026/6/9 提交  
**作者**：Yijian Li, Changze Li, Hantian Shi, Jiaying Luo, Jiyuan Cai, Ming Yang, Tong Qin  
**标签**：VLN / Agent / Tool-Calling / Zero-Shot / Robotics

---

## 核心思路

传统零样本 VLN-CE（连续环境视觉语言导航）依赖预训练的 waypoint predictor 来生成候选导航点，action space 受限，深度信息未被有效利用，记忆机制也粗糙（长文本/视觉历史堆积或跨 episode 检索）。

AgenticNav 换了一个视角：把 VLM 与环境之间的交互重新设计成 **agent 工具调用接口**。三个工具：

| 工具 | 功能 | 巧思 |
|------|------|------|
| Action Tool | VLM 直接在 RGB 图上选目标像素点，转物理运动 | 抛弃 waypoint predictor，行动空间连续自由 |
| Depth Tool | 按需查询任意像素的深度 | 只在对决策关键的地方才取深度，不喂整张深度图 |
| Memory Tool | 紧凑轨迹地图 + 按需回看历史帧 | 避免 prompt 膨胀，选择性召回视觉历史 |

## 实验结果

- R2R-CE 上同 VLM 骨架下 **新 SOTA**（零样本方法中）
- 真机验证 zero-shot 泛化优于现有方法
- 消融实验：pixel action > waypoint predictor；depth tool + agentic memory 均有增益

## 与 ZhouXuan 论文的关联

ZhouXuan 论文方向是"基于深度学习的智能导航与识别系统"。AgenticNav 提供了一个前沿视角：

1. **导航即 agent 任务**：把 VLN 从"感知→规划→控制"管道重构为 VLM 作为 agent 调度工具的范式，这和当前 agent 技术主流趋势一致
2. **工具调用的泛化能力**：用 tool-calling 接口而非固定 pipeline，天然支持 zero-shot 泛化，不需要针对新环境 finetune
3. **记忆管理的工程启发**：compact map + recall tool 的设计在 prompt 预算受限时很有实用价值
4. **像素级 action**：跳过 waypoint 预测直接选像素，思路简洁有力

可以考虑作为论文相关工作或前沿展望的引用素材。
