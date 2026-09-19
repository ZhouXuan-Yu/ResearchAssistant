# Xiaomi MiMo Code V0.1.0 — 开源终端编程 Agent

**日期**：2026-06-11
**来源**：Gizmochina / Xiaomi 官方
**标签**：#Agent #Coding #OpenSource #Terminal

## 概述

小米开源了 MiMo Code V0.1.0，基于 OpenCode 项目、MIT 协议。定位是**终端内的长程编程 Agent**，核心卖点是解决「时间越久 AI 越健忘」的问题。

## 关键特性

### 持久记忆系统
- **后台子代理**持续管理和存储上下文
- 主对话接近上下文窗口上限时，子代理自动将历史浓缩为结构化摘要
- 主代理无缝继续，不丢失前置决策

### /dream 自动维护
- 每 7 天自动触发一次
- 启动独立维护代理审查旧会话和记忆文件
- 去重、校验文件路径、压缩为更新的长期记忆

### Compose 模式
- 按 Tab 键激活
- 用户给粗略目标和想法，Agent 完成完整工作流：规划 → 设计 → 编码 → 测试 → 审查
- 小米声称可产出「工业级成品」

### Harness 系统
- 专为 MiMo 模型构建的框架
- 直接利用模型底层能力，而非将 AI 当作通用 API 端点

## 性能基准

| 基准 | 分数 | 对比 |
|------|------|------|
| SWE-Bench Pro | 62% | 超 Claude Code ~5pp（同底层模型） |
| Terminal Bench 2 | 73% | 超 Claude Code ~5pp |

## 模型支持

- 内置免费 MiMo-V2.5（无需注册）
- 可接入第三方：**DeepSeek**、Kimi、GLM
- 内置 MiMo-V2.5-ASR 语音输入

## 安装

- macOS/Linux：单条终端命令
- Windows：npm 安装
- 启动：终端输入 `mimo`

## 与 ZhouXuan 工具链的关联

ZhouXuan 现有编码平台：Cursor（主力）+ Claude Code（重型工程）+ Reasonix（低成本迭代）。MiMo Code 的差异化在于：
1. **持久记忆机制**：后台子代理自动浓缩上下文，对齐 Codex Ralph Loop 思路
2. **/dream 自动维护**：7 天周期的记忆垃圾回收，类似 continuous-learning 的自动化版
3. **DeepSeek 支持**：与 ZhouXuan 使用的国内 API 兼容
4. **MIT 协议**：无商业限制，可在现有工具链中尝试

不需要立刻替换任何现有工具，但记忆管理架构值得研究和借鉴。
