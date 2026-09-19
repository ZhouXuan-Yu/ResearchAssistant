# CVPR 2026 医学影像论文

## 概述

在CVPR 2026中，医学影像方向有重要论文。本轮发现一篇与ZhouXuan研究方向（深度学习智能导航与识别系统）间接相关的论文。

---

## 论文：HistoSelect

### 基本信息
- **标题**: Act Like a Pathologist: Tissue-Aware Whole Slide Image Reasoning
- **作者**: Wentao Huang, Weimin Lyu, Peiliang Lou, Qingqiao Hu, Xiaoling Hu, Shahira Abousamra, Wenchao Han, Ruifeng Guo, Jiawei Zhou, Chao Chen, Chen Wang
- **页码**: 6972-6981
- **链接**: https://openaccess.thecvf.com/content/CVPR2026/html/Huang_Act_Like_a_Pathologist_Tissue-Aware_Whole_Slide_Image_Reasoning_CVPR_2026_paper.html
- **代码**: https://github.com/winston52/HistoSelect

### 核心问题
计算病理学近年来发展迅速，由领域特定图像编码器和使用视觉语言模型回答疾病自然语言问题的兴趣推动。然而，病理学问答背后的核心问题仍未解决，考虑到千兆像素切片包含的信息远多于给定问题所需的信息。

### 创新贡献
1. **问题引导、组织感知、粗到细检索框架**: HistoSelect
2. **组采样器**: 识别问题相关的组织区域
3. **补丁选择器**: 在这些区域中检索最具信息量的补丁
4. **效率提升**: 平均减少70%的视觉token使用

### 技术架构
- **组采样器**: 识别问题相关的组织区域
- **补丁选择器**: 检索最具信息量的补丁
- **粗到细检索**: 从粗粒度到细粒度的检索
- **人类化搜索模式**: 模仿病理学家的搜索和注意力模式

### 性能表现
- **数据集**: 356,000个问答对
- **效率**: 减少70%的视觉token使用
- **准确性**: 在三个病理学QA任务中提升准确性
- **可解释性**: 产生基于可解释、病理学家一致区域的答案

### 对ZhouXuan研究的启示
1. **粗到细检索**: 从粗粒度到细粒度的检索策略
2. **效率优化**: 减少视觉token使用
3. **人类化搜索**: 模仿人类的搜索和注意力模式

---

## 综合分析

### 对ZhouXuan研究方向的启示

#### 技术路线参考
1. **HistoSelect**: 粗到细检索在视觉理解中的应用
2. **效率优化**: 减少视觉token使用

#### 可能的研究方向
1. **粗到细导航**: 在导航中实现粗到细的检索
2. **效率优化**: 减少导航系统的计算开销
3. **人类化搜索**: 模仿人类的搜索模式

---

## 相关资源

- HistoSelect: https://github.com/winston52/HistoSelect
- CVPR 2026医学影像AI趋势: https://finance.sina.com.cn/stock/t/2026-05-28/doc-inhzmihu0279688.shtml

---

*创建时间: 2026-06-21 16:39*
*来源: CVPR 2026论文搜索*
*相关性: 深度学习智能导航与识别系统研究（间接相关）*