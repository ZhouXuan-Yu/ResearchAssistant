# CVPR 2026 深度估计论文

## 概述

在CVPR 2026中，深度估计方向有多篇重要论文。本轮发现两篇与ZhouXuan研究方向（深度学习智能导航与识别系统）相关的论文。

---

## 论文一：PTC-Depth

### 基本信息
- **标题**: PTC-Depth: Pose-Refined Monocular Depth Estimation with Temporal Consistency
- **作者**: Leezy Han, Seunggyu Kim, Dongseok Shim, Hyeonbeom Lee
- **页码**: 12617-12627
- **链接**: https://openaccess.thecvf.com/content/CVPR2026/html/Han_PTC-Depth_Pose-Refined_Monocular_Depth_Estimation_with_Temporal_Consistency_CVPR_2026_paper.html

### 核心问题
单目深度估计（MDE）已广泛应用于自动驾驶车辆和移动机器人的感知系统。然而，现有方法往往难以在连续帧之间保持深度估计的时间一致性。这种不一致性不仅会导致抖动，还可能在深度范围突然变化时导致估计失败。

### 创新贡献
1. **一致性感知单目深度估计框架**: 利用移动机器人的轮式里程计实现稳定连贯的深度预测
2. **相机位姿和稀疏深度估计**: 使用连续帧之间的光流进行三角测量
3. **递归贝叶斯估计**: 更新度量尺度的递归贝叶斯估计
4. **基础模型重缩放**: 将预训练深度估计基础模型的相对深度重缩放为度量深度

### 技术架构
- **光流三角测量**: 估计相机位姿和稀疏深度
- **递归贝叶斯估计**: 更新度量尺度
- **基础模型重缩放**: 将相对深度转换为度量深度
- **时间一致性**: 保持连续帧之间的深度一致性

### 性能表现
- **数据集**: KITTI、TartanAir、MS2、自建数据集
- **结果**: 鲁棒且准确的深度估计性能

### 对ZhouXuan研究的启示
1. **时间一致性**: 保持深度估计的时间一致性
2. **基础模型利用**: 利用预训练基础模型
3. **度量尺度恢复**: 从相对深度恢复度量深度

---

## 论文二：InfiniDepth

### 基本信息
- **标题**: InfiniDepth: Arbitrary-Resolution and Fine-Grained Depth Estimation with Neural Implicit Fields
- **链接**: https://github.com/daitomanabe/zju3dv--InfiniDepth
- **会议**: CVPR 2026

### 核心问题
现有深度估计方法在分辨率和细粒度方面存在限制。

### 创新贡献
1. **任意分辨率深度估计**: 支持任意分辨率的深度图输出
2. **细粒度深度估计**: 提供细粒度的深度信息
3. **神经隐式场**: 使用神经隐式场表示深度
4. **多能力支持**: 单目深度估计、视图合成、深度传感器增强

### 技术架构
- **神经隐式场**: 表示连续的深度场
- **任意分辨率**: 支持任意分辨率的深度图输出
- **3D高斯泼溅**: 从单张图像生成3D场景

### 性能表现
- **能力**: 相对深度估计、3D高斯泼溅、度量深度估计
- **输入**: 单张RGB图像
- **输出**: 任意分辨率深度图、3D场景

### 对ZhouXuan研究的启示
1. **任意分辨率**: 支持不同分辨率的需求
2. **神经隐式场**: 连续深度场的表示
3. **多能力集成**: 深度估计与3D重建的集成

---

## 综合分析

### 两篇论文对比

| 论文 | 核心创新 | 关键技术 | 应用场景 |
|------|----------|----------|----------|
| **PTC-Depth** | 时间一致性深度估计 | 递归贝叶斯+基础模型重缩放 | 自动驾驶/机器人 |
| **InfiniDepth** | 任意分辨率深度估计 | 神经隐式场 | 3D重建/视图合成 |

### 共同趋势
1. **基础模型利用**: 利用预训练基础模型
2. **度量深度**: 从相对深度恢复度量深度
3. **时间一致性**: 保持连续帧之间的一致性

### 对ZhouXuan研究方向的启示

#### 技术路线参考
1. **PTC-Depth**: 时间一致性在深度估计中的应用
2. **InfiniDepth**: 神经隐式场在深度估计中的应用

#### 可能的研究方向
1. **时间一致性深度**: 在导航中保持深度估计的时间一致性
2. **任意分辨率**: 支持不同分辨率的深度估计
3. **神经隐式场**: 连续深度场的表示

---

## 相关资源

- PTC-Depth: https://openaccess.thecvf.com/content/CVPR2026/html/Han_PTC-Depth_Pose-Refined_Monocular_Depth_Estimation_with_Temporal_Consistency_CVPR_2026_paper.html
- InfiniDepth: https://github.com/daitomanabe/zju3dv--InfiniDepth
- CVPR 2026深度估计论文集: https://cvpr.thecvf.com/virtual/2026/papers.html

---

*创建时间: 2026-06-21 16:39*
*来源: CVPR 2026论文搜索*
*相关性: 深度学习智能导航与识别系统研究*