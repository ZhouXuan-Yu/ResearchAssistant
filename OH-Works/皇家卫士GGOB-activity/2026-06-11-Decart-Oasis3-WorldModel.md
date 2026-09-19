# Decart Oasis 3：实时世界模型与自动驾驶仿真

**日期**：2026-06-11  
**来源**：TechCrunch、CryptoBriefing、PyPI  
**标签**：#WorldModel #AutonomousDriving #Simulation #ThesisRelated

---

## 一句话

Decart 发布 Oasis 3，首个可通过 API 调用的实时交互式世界模型，专注生成逼真驾驶环境用于自动驾驶仿真测试，Python SDK 已上架 PyPI。

## 核心事实

- **发布时间**：2026-06-10，API + Python SDK 同步开放
- **融资**：2026年5月完成 $300M 融资，估值约 $4B（Radical Ventures 领投，Nvidia/Toyota/Adobe/eBay/Sequoia/Benchmark 跟投）
- **定价**：$0.02/秒（API），企业按需定价
- **公司**：以色列/美国双市场，2023年成立，累计融资 >$450M
- **SDK**：`pip install decart-oasis`，Python 3.10+，MIT 协议

## 技术架构

```
prompt("driving in an urban area")
  → infer([[throttle, steering] × 4])  ← 每次发4组动作
  → 返回 3 路相机帧（left_forward, front, right_forward）
  → 512×768×3 RGB，VP9/JPEG 解码
```

- **自回归生成**：逐帧生成，每帧约 8000 tokens，十帧/秒即数十万 tokens/s
- **底层**：Decart Optimization Stack (DOS 2.0)，垂直优化到硬件层（Nvidia/Amazon/Google）
- **架构**：gRPC 通信，无 torch/ML 依赖，纯客户端
- **成本优势**：声称比竞品便宜一个数量级以上

## 已知局限

| 问题 | 原因 | 解决方向 |
|------|------|----------|
| 长时一致性差 | 自回归架构，context window 快速填满 | 延长记忆 / token 压缩 |
| 物理模拟不准（穿车而过） | 训练数据中事故场景远少于正常驾驶 | 数据失衡——研究级问题 |
| 控制响应迟钝 | 同上，世界模型共性难题 | 团队在攻关 |
| 环境像"梦境流" | 无持久世界状态，每次都是重新生成 | 下一版支持从视频种子生成 |

## 竞争格局

- **Google Genie 3**（研究预览）：通用世界生成，非驾驶专精
- **World Labs Marble**（李飞飞）：商业世界模型，偏通用
- **Runway**：视频生成转向世界模型
- **Luma**：同赛道

Oasis 3 的差异化：垂直整合（硬件到模型全链路优化）+ API-first + 驾驶场景专精。

## 与 ZhouXuan 论文的关联

ZhouXuan 论文方向：**基于深度学习的智能导航与识别系统**

Oasis 3 代表了一条值得关注的技术路线：

1. **仿真数据生成**：智能导航系统的训练和测试需要大量多样化场景。传统仿真器（CARLA、AirSim）需要手工建模，世界模型提供了一种端到端生成方案
2. **架构范式**：自回归视频生成 × 物理一致性，是当前世界模型的核心矛盾。8000 tokens/frame 的 context 管理问题与导航系统的时序建模有共通之处
3. **多相机融合**：三路相机输出（前+双侧）对应实车传感器配置，帧同步和一致性是导航感知的经典问题
4. **边缘场景覆盖**：论文中导航系统测试往往受限于场景多样性，world model 的 "infinite generation" 概念提供了一种补充思路
5. **PyPI 可用**：Python SDK 已就绪，理论上可在论文实验环节做初步对接

## 历史脉络

- 2024-10-31：Decart 首次公开 Oasis，展示 Minecraft-like 开放世界交互
- 2025-2026：Lucy 模型在电商/直播领域积累 10万+ 开发者
- 2026-05：$300M 融资，DOS 2.0 发布
- 2026-06-09：Oasis 3 PyPI SDK v0.0.1
- 2026-06-10：Oasis 3 正式发布，TechCrunch 独家

## 看点与争议

- CEO 类比 "LLM 的 API 时刻"：世界模型能否像语言模型一样通过 API 催生开发者生态，是核心叙事
- $4B 估值对应 $450M 总融资，在三年的公司里属于极快节奏
- 物理一致性的"major research problem"坦率承认，说明赛道仍处早期
- Toyota 的战略投资：整车厂直接押注世界模型赛道
