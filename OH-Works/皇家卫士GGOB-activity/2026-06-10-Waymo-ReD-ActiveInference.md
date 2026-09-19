# Waymo ReD：基于主动推理的驾驶认知模型

**来源**：Nature Communications，2026-06-10 发表  
**作者**：Waymo × TU Delft (Arkady Zgonnikov 团队)  
**定位**：自动驾驶安全评估的"行为碰撞假人"

---

## 一句话概要

Waymo 联合代尔夫特理工大学在 Nature Communications 发表 Reference Driver（ReD）模型，用计算神经科学的"主动推理"（Active Inference）框架构建了一个能模拟人类驾驶员碰撞规避行为的认知模型。Karl Friston 评价其为 "technical tour de force"。模型已开源。

---

## 核心思路

传统自动驾驶安全模型只模拟"最后一秒的应急反应"，Waymo 认为这不够。ReD 的核心突破在于：

**从"事后反应"升级为"事前预期"**：模型持续计算"意外程度"（surprise），在冲突升级前就主动调整驾驶策略，实现 proactive avoidance。

---

## 技术架构：四层认知模拟

ReD 叠加了四个人类驾驶的认知特征：

### 1. Looming 威胁感知
人类判断纵向威胁依赖"looming"——目标在视野中的扩张速率。ReD 模拟了这一特性：远距离时对速度判断模糊，物体越近感知越精确，与真实人类完全一致。

### 2. 交通规范过滤
模型内置"交通规范"偏差——默认假设其他车辆遵守规则，直到直接观测到违规行为才切换预期。这解释了人类驾驶员"信任但验证"的行为模式。

### 3. Surprise 触发重评估
当环境偏离预期的程度超过阈值，模型判定"当前计划已失效"，触发全局重规划。这个 surprise 阈值模拟了人类从"觉得不对劲"到"采取行动"的决策拐点。

### 4. 生理约束建模
模拟人类单脚操作油门/刹车的物理限制：切换踏板时有 0.2 秒延迟。这种细节层面的 fidelity 在以往模型中从未出现过。

---

## 理论根基：Active Inference

Active Inference 由 Karl Friston 提出，核心主张是：

> 大脑是一个"意外最小化机器"——所有感知和行动都服务于一个目标：减少对外部世界的预测误差（prediction error），即最小化自由能（free energy）。

在驾驶场景中：驾驶员持续生成对未来状态的预测，同时采取行动使实际感知与预测保持一致。当预测误差（surprise）超过阈值，触发行为调整。

ReD 是 Active Inference 在自动驾驶领域的首次工业级落地。

---

## 对比：ReD vs 传统安全模型

| 维度 | 传统模型 | ReD |
|------|---------|-----|
| 时间范围 | 仅模拟碰撞瞬间反应 | 覆盖碰撞前完整行为链 |
| 认知基础 | 纯运动学/动力学 | 计算神经科学驱动 |
| 预测能力 | 被动响应 | 主动规避（proactive avoidance） |
| 可扩展性 | 场景有限 | 可适配数千种场景 |
| 人类 fidelity | 粗糙近似 | 多层级认知模拟 |
| 开源性 | 通常是黑箱 | 学术非商业许可开源 |

---

## 实际案例：Santa Monica 学童碰撞

2026 年 1 月，Waymo 无人车在学校附近撞到一名儿童。当时 Waymo 用旧模型声称"人类驾驶员在相同场景下碰撞速度会达 14 mph，Waymo 仅 6 mph"。该事故目前仍在 NHTSA 和 NTSB 调查中。

ReD 模型的出现恰逢其时的背景：Waymo 正在加速向更多城市扩张，面临更严格的监管审查。一个更精确的人类驾驶基准模型，对于说服监管机构和公众至关重要。

---

## 对智能导航研究的启示

ReD 虽非深度学习路线，但对 ZhouXuan 的"智能导航与识别系统"论文有三重参考价值：

1. **方法论层面**：Active Inference 与深度学习的互补——前者擅长认知建模与可解释性，后者擅长感知与端到端学习。两者的融合是前沿方向。
2. **评估基准**：ReD 提供了一种"人类驾驶行为标准答案"的生成方式。任何导航系统的避障决策，都可以与 ReD 输出的"合理人类反应"进行对比。
3. **Surprise 机制**：ReD 的 surprise 驱动重规划机制，与 CVPR 2026 导航论文中 IntentNav 的意图推理、TrajRAG 的检索增强有结构上的呼应——都在解决"何时需要重新思考路径"这个核心问题。

---

## 参考文献

- Waymo ReD 论文：Nature Communications, 2026-06-10
- Active Inference 理论基础：Friston, K. et al. "The free-energy principle: a unified brain theory?" Nature Reviews Neuroscience, 2010
- Waymo 安全研究页面：https://waymo.com/safety/research/
- ReD 模型代码：开源（学术非商业许可）
