# 视觉语言导航（VLN）研究图景速览 · 2026-09-17

> 巡检期间自主整理。本轮网络可用，但本机对 arxiv.org / springer / mdpi / dev.to 等站点的整页抓取被拦截，仅有搜索结果摘要可读。因此本笔记定位为**条目索引**：记录可核实的时间、机构与链接，描述均直接来自检索摘要，未做正文级深读，勿当作论文结论引用。后续需以原文核对。

## 一、主题走向（来自检索摘要的共识性表述）

- VLN 正从"室内、离散步、单智能体"范式，向**长程（long-horizon）、连续环境、多智能体协作、世界模型驱动**迁移。
- "下一阶段"被若干来源概括为**自演化智能体（self-evolving agents）**与统一"世界-动作"建模。
- VLA（视觉-语言-动作）模型与 VLN 的边界在模糊，二者共享"像素+指令 → 动作"的映射内核。

## 二、可核实的具体工作

| 工作 | 时间 | 机构/来源 | 一句话要点（摘要级） | 链接 |
|---|---|---|---|---|
| FutureNav | 2026-06-29 (arXiv:2606.30367) | 清华大学、鹏城实验室 | 基于 VLM 的统一"世界-动作"建模框架，联合建模世界状态与动作，面向连续环境 VLN | https://arxiv.org/abs/2606.30367 |
| CoNavBench | ICLR 2026 (Wang et al.) | 会议论文 | 首个**协作式长程 VLN 基准**，中继式多机器人任务，用 NavCraft 构建 | https://openreview.net/forum?id=bMrH2PFMsi |
| DeCoNav | 2026-04-14 (arXiv:2604.12486) | Zhou et al. | 对话增强的长程协作导航，建立在 CoNavBench 之上 | https://arxiv.org/abs/2604.12486 |
| LHPR-VLN (LH-VLN) | CVPR 2025 | 中山大学 HCPLab-SYSU | 长程规划与推理基准，3260 个任务、平均约 150 步，提出三项子任务级评估指标 | https://github.com/HCPLab-SYSU/LH-VLN |
| Large-Scale Model-Enhanced VLN | 2026 | MDPI Sensors 26(7):2022 (Z Li) | 强调将原始视觉输入转为语义一致的空间表征，形成稳定可解释的智能体表示 | https://www.mdpi.com/1424-8220/26/7/2022 |
| VLN 综述（recent advancements） | 2026 | Springer, J Khan | 覆盖 VLN-CE 等标准基准的近期进展综述 | https://link.springer.com/article/10.1007/s10791-026-09977-z |
| VLA 综述 | 更新至 2026-05 (arXiv:2405.14093) | Survey | 具身 AI 中 VLA 模型的系统性综述 | https://arxiv.org/abs/2405.14093 |

## 三、基础坐标（非 2026 新作，但为对照基线）

- **VLN-CE**：Krantz et al., Meta —— 连续环境中的语言导航任务集，被广泛用作评测基准。https://jacobkrantz.github.io/vlnce/
- **Awesome-VLN**（LLM/VLM 路线论文合集）：https://github.com/NIneeeeeem/Awesome-Vision-Language-Navigation
- **Awesome-VLA**：https://github.com/ai4s-research/awesome-vision-language-action

## 四、对毕业论文的可能接口（待与作者确认，非结论）

1. 若论文题目落在"智能导航与识别"，FutureNav 的"世界-动作统一建模"与 LHPR-VLN 的"子任务级指标"可作为方法/评估章节的对照锚点。
2. 多智能体协作（CoNavBench / DeCoNav）可作为"从单智能体导航到协作导航"的引言演进线索。
3. 需注意：本笔记条目多为 2026 年中发布，引用前务必核对原文与正式出版状态。

## 五、本轮局限

- 整页抓取受限，未能进入论文正文；条目描述为摘要级。
- 未做引文网络与代码可用性核查。

---
*生成于巡检（2026-09-17 19:45 左右），仅作检索线索留存。*

## 六、补充条目（2026-09-18 巡检补录）

> 本轮整页抓取恢复可用，下列三项为昨日索引未收录的新条目。其中 Goal2Pixel、VIL 已读到**逐字摘要**（可信度高于昨日条目）；EvoNav 仅有标题与摘要首句，标注为偏低置信。引用前仍需核对原文与正式出版状态。

### 1. Goal2Pixel — 把 VLN-CE 从「动作预测」改写为「可通行像素接地」

- **来源/时间**：arXiv:2606.01621（v2），2026 年
- **链接**：https://arxiv.org/abs/2606.01621 ·https://www.alphaxiv.org/abs/2606.01621
- **核心主张（摘要级）**：将 VLN-CE 重新表述为「可导航像素接地（navigable pixel grounding）」。不再预测离散低级动作，而把**图像平面**作为 VLM 推理与机器人运动之间的统一空间接口：模型预测一个可见的可通行像素，回投影为 3D 航点供前进；左/右/下三个辅助指令区分别解释为左转、右转、停止。长程靠「可见性感知关键帧记忆（visibility-aware keyframe memory）」维持紧凑历史；用语义嵌入与坐标感知辅助损失适配预训练 VLM。
- **实测数字**：R2R-CE Val-Unseen 上 SR 54.1%、SPL 52.5%，每回合仅 7.75 次 VLM 调用；对照组「直接动作预测」需 46.62 次调用、SR 仅 32.9%。即约 1/6 的查询量换来更高成功率。
- **对自己论文的接口（推断，非结论）**：若论文涉及 VLM 驱动导航的推理开销与动作空间设计，「像素接地 vs 动作预测」是一组干净的对照轴；其「图像平面即统一接口」的思路与导航识别中的空间表征问题同源。

### 2. VIL / V²-VLNCE — 视角不变的后训练框架（RA-L 2026）

- **来源/时间**：arXiv:2507.08831（v1 2025-07-05，v4 2026-02-20），**已接收 RA-L 2026**
- **作者**：Josh Qixuan Sun, Huaiyuan Weng, Xiaoying Xing, Chul Min Yeum, Mark Crowley（滑铁卢大学）
- **链接**：https://arxiv.org/abs/2507.08831 ·代码 https://github.com/realjoshqsun/V2-VLNCE
- **核心主张（摘要级）**：提出更一般的场景 V²-VLNCE（视角可变：相机高度与俯仰角变化），并给出视角不变后训练框架 VIL。手段有二：对比学习学稀疏且视角不变的特征；对 VLN-CE 基线中标准的「航点预测模块」用教师-学生蒸馏，把视角相关的教师知识注入视角不变的学生；端到端联合优化。
- **实测数字**：V²-VLNCE 设置下，R2R-CE 与 RxR-CE 两个基准的 SR 提升 8–15%；在标准 VLN-CE 设置下多数不降反升，RxR-CE 上各项指标达 SOTA；对 Stretch RE-1、LoCoBot 等真实机器人相机配置亦有一致提升，并有两个物理环境的实机概念验证（全景 RGB + LiDAR）。
- **对自己论文的接口（推断，非结论）**：作为「即插即用后训练」的鲁棒性增强件，可放进「评测/鲁棒性」讨论；视角不变性这条线，对识别系统在传感器位姿扰动下的稳定性有类比价值。

### 3. EvoNav — 零样本 VLN-CE 的「未来思考 + 历史经验」自演化智能体（CVPR 2026）

- **来源/时间**：CVPR 2026 · 海报 2026-06-06（Guangzhao Dai, Shuo Wang, Zihan Wang, Guo-Sen Xie, Yang Yang, Jinshan Pan, Qianru Sun, Xiangbo Shu；新加坡管理大学 SMU 等）
- **链接**：https://openaccess.thecvf.com/content/CVPR2026/html/Dai_History_to_Future_Evolving_Agent_with_Experience_and_Thought_for_CVPR_2026_paper.html ·海报页 https://cvpr.thecvf.com/virtual/2026/poster/39872 ·SMU 库全文 https://ink.library.smu.edu.sg/cgi/viewcontent.cgi?article=12200&context=sis_research
- **核心主张（已读全文摘要，可信度提升）**：针对 LLM 零样本 VLN-CE 中「朴素推理、缺乏反馈」（初始失误任务会持续失败）的缺陷，提出 EvoNav 新范式，由两条链协同演化决策：
  1. **F-CoT（Future Chain-of-Thought，未来思考链）**：预测未来的**动作与地标**作为「思考」，用于辅助导航进度估计与方向选择；
  2. **H-CoE（History Chain-of-Experience，历史经验链）**：总结历史轨迹与场景作为「经验」，提升导航决策可靠性。
  F-CoT 与 H-CoE 协作共演化智能体决策；在**仿真器与真实环境**中均验证有效，源代码将开源。
- **待办**：仍为摘要级，未做正文级方法/实验深读；具体指标待核对原文。

### 与昨日图景的关系

昨日条目偏「世界-动作统一建模 / 多智能体协作 / 长程基准」；本轮三条则集中在**接口设计（像素接地）、鲁棒性（视角不变）、零样本自演化**三个正交方向，恰好补上「如何让既有策略更稳、更省、更可迁移」这一层，可与 FutureNav（统一建模）、CoNavBench（协作）拼成更完整的一张图。

---
*补录于巡检（2026-09-18 15:2X，EvoNav 摘要于 16:5X 补全），三条均已读到完整摘要；仍未做正文级深读与指标核对，勿当结论引用。*
