# Agent框架新进展（2026-06-21 巡检补充）

> 周日下午17:10，网络稳定运行约18.5小时后发现的三个重要Agent框架更新。

---

## 1. OpenRath：以Session为核心的多Agent运行时

**发布团队**: 清华大学 + 中山大学（Rath Team）
**版本**: v1.2.1（PyPI可安装）
**协议**: BSD-3-Clause

### 核心理念：MAMS（Multi-Agent Multi-Session）

传统框架以Agent为中心，OpenRath认为真正需要被管理的是**Session数据流**。

**Session Graph**是关键创新：
- 支持fork（分叉）、detach（断父链）、merge（合并）
- 序列化为JSONL可交给下一个Workflow
- 从实现细节升格为集群的**可观测层与控制层**
- 路由、复现、回滚、审计全在同一张图上完成

### 版本演进

| 版本 | 解决的问题 |
|------|-----------|
| v1.1 | 持久Session：把干活的证据完整留下 |
| v1.2 | Session从单Agent记录升级为多Agent可路由对象 |

### 技术亮点

- 一行代码即可实现Session路由
- 类PyTorch的API设计（`pip install openrath`）
- 事件驱动异步通信引擎

### 对"超级AI个体"构建的启示

Session Graph的设计思路值得借鉴。当多个AI平台（Cursor、Claude Code、HanaAgent等）协作时，如何追踪"这个结论是哪个Agent、走哪条分支、调哪次工具产出的"是一个核心问题。

---

## 2. Hermes Agent v0.17.0 "The Reach Release"

**发布时间**: 2026-06-19
**规模**: 1475次提交、约800个合并PR、1693个文件变更、235390行新增代码

### 核心更新

**1. iMessage原生接入**
- 运行`photon login`用设备码认证
- 无需Mac服务器或BlueBubbles桥接
- 直接在Hermes中收发iMessage

**2. 异步子Agent（`delegate_task(background=true)`）**
- 子Agent后台运行，立即返回句柄
- 完成时以新回合形式自动注入对话
- 解决了"委派任务=阻塞等待"的传统问题

**3. Cursor模型直调**
- 通过xAI Grok订阅调用grok-composer-2.5-fast
- 无需单独API Key
- 支持200K上下文

**4. Dashboard完整配置构建器**
- 浏览器中选择模型、安装Skills、挂载MCP
- 告别手写config.yaml

**5. Skills Hub全面改版**
- 接入多家社区Hub
- 安装前安全扫描

**6. WhatsApp Business Cloud API**
- 官方第一方适配
- 无需自建桥接进程

### 对"超级AI个体"构建的启示

Hermes v0.17.0的定位正在清晰化：
- **异步任务编排**: delegate_task(background=true)的模式
- **多平台接入**: iMessage + WhatsApp + Telegram
- **模型路由**: 通过订阅调用商业模型

---

## 3. AWorld：蚂蚁集团多Agent训练框架

**发布时间**: 2026-06-18
**团队**: inclusionAI（蚂蚁集团）
**定位**: 工业级全链路多智能体训练与编排框架

### 核心能力

**全生命周期闭环**: 智能体搭建 → 环境交互 → 分布式数据采集 → 强化学习迭代 → 效果评测

**三大技术支柱**：
1. **事件驱动多Agent通信引擎**: 发布-订阅架构
2. **分布式Rollout并行调度**: 单任务并行32次交互尝试
3. **统一模型与工具抽象**: 标准化Agent交互协议

### 性能指标

- GAIA通用智能体基准榜单开源项目排名第一
- 同等算力下数据采集效率提升14.6倍
- Qwen3-32B模型经AWorld训练后指标提升10.6个百分点

### 对"超级AI个体"构建的启示

AWorld的分布式训练思路对于优化个人Agent系统有参考价值：
- **并行采样**: 多个Agent同时尝试解决问题
- **反思优化**: 任务规划→工具调用→结果验证→反思优化的闭环
- **标准化评测**: 可复现的性能基准

---

## 综合分析：Agent框架的三个趋势

| 趋势 | 代表 | 核心价值 |
|------|------|----------|
| Session为中心 | OpenRath | 可观测性、可追溯性 |
| 异步任务编排 | Hermes v0.17.0 | 非阻塞、多平台接入 |
| 全链路训练 | AWorld | 工业级、可扩展 |

### 对个人AI工具链的启示

1. **Session管理**: 需要考虑如何在多平台间追踪任务流
2. **异步模式**: delegate_task模式可应用到HanaAgent与其他平台的协作
3. **训练闭环**: 如果要持续优化Agent能力，需要建立评测和迭代机制

---

*创建时间: 2026-06-21 17:10*
*来源: web_search搜索*
*相关性: "超级AI个体"构建、Agent框架演进、Hermes平台定位*