# CVPR 2026 强化学习论文

## 概述

在CVPR 2026中，强化学习方向有重要论文。本轮发现一篇与ZhouXuan研究方向（深度学习智能导航与识别系统）相关的论文。

---

## 论文：PALM

### 基本信息
- **标题**: PALM: Progress-Aware Policy Learning via Affordance Reasoning for Long-Horizon Robotic Manipulation
- **作者**: Yuanzhe Liu, Jingyuan Zhu, Yuchen Mo, Gen Li, Xu Cao, Jin Jin, Yifan Shen, Zhengyuan Li, Tianjiao Yu, Wenzhen Yuan, Fangqiang Ding, Ismini Lourentzou
- **页码**: 28096-28110
- **链接**: https://openaccess.thecvf.com/content/CVPR2026/html/Liu_PALM_Progress-Aware_Policy_Learning_via_Affordance_Reasoning_for_Long-Horizon_Robotic_CVPR_2026_paper.html

### 核心问题
视觉-语言-动作（VLA）模型在机器人操作中显示出前景，但它们在长时程、多步骤任务中仍然存在困难。现有方法缺乏内部推理机制来识别任务相关的交互线索或跟踪子任务内的进度，导致关键执行错误，如重复动作、遗漏步骤和过早终止。

### 创新贡献
1. **进度感知策略学习**: 围绕以交互为中心的可供性推理和子任务进度线索构建策略学习
2. **互补可供性表示**: 捕获对象相关性、接触几何、空间放置和运动动力学
3. **连续子任务进度预测**: 预测子任务内的连续进度
4. **无缝子任务过渡**: 实现无缝的子任务过渡

### 技术架构
- **可供性表示**: 捕获对象相关性、接触几何、空间放置、运动动力学
- **任务相关锚点**: 作为视觉运动控制的任务相关锚点
- **进度预测**: 预测子任务内的连续进度
- **子任务过渡**: 实现无缝的子任务过渡

### 性能表现
- **LIBERO-LONG**: 91.8%成功率
- **CALVIN ABC->D**: 平均长度提升12.5%
- **真实世界**: 在三个长时程泛化设置中比真实世界基线提升2倍

### 对ZhouXuan研究的启示
1. **进度感知**: 在策略学习中感知进度
2. **可供性推理**: 利用可供性推理指导控制
3. **长时程任务**: 处理长时程、多步骤任务

---

## 综合分析

### 对ZhouXuan研究方向的启示

#### 技术路线参考
1. **PALM**: 进度感知在策略学习中的应用
2. **可供性推理**: 利用可供性推理指导控制

#### 可能的研究方向
1. **进度感知导航**: 在导航中感知进度
2. **可供性推理**: 利用可供性推理指导导航
3. **长时程导航**: 处理长时程导航任务

---

## 相关资源

- PALM: https://openaccess.thecvf.com/content/CVPR2026/html/Liu_PALM_Progress-Aware_Policy_Learning_via_Affordance_Reasoning_for_Long-Horizon_Robotic_CVPR_2026_paper.html
- 2026年RL在Robotics中的新范式: https://zhuanlan.zhihu.com/p/2002328291592401820

---

*创建时间: 2026-06-21 16:39*
*来源: CVPR 2026论文搜索*
*相关性: 深度学习智能导航与识别系统研究*