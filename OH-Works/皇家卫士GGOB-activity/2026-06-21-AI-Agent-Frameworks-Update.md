# AI Agent框架进展补充（2026-06-21）

## 概述

在2026-06-21的巡检中，发现AI Agent框架领域有新的重要进展，作为上午整理的AI Agent框架笔记的补充。

---

## 1. Amazon Bedrock AgentCore Harness正式发布

**发布时间**: 2026年6月（从Preview转为GA）

**核心更新**:
- **两个API调用即可创建Agent**: CreateHarness（定义Agent）+ InvokeHarness（运行Agent）
- **隔离执行环境**: 每个Agent运行在独立的沙盒环境中，包含文件系统和shell
- **跨会话记忆**: 记住用户和对话，跨会话保持上下文
- **技能系统**: 支持AWS策划的技能目录
- **Web浏览**: 内置浏览器能力
- **工具调用**: 通过Gateway或MCP调用工具
- **模型切换**: 会话中可切换模型提供商，不丢失上下文
- **实时流式输出**: 每个步骤实时流式返回
- **自动追踪**: 自动追踪到CloudWatch

**新功能**:
- **版本管理**: 每次UpdateHarness创建不可变版本，支持回滚
- **Step Functions集成**: Harness调用成为AWS Step Functions中的原生状态
- **Web Search on AgentCore**: 通过Gateway暴露Web搜索能力

**技术亮点**:
- 无需编写编排代码或构建容器
- 配置而非构建（configure rather than build）
- 支持A/B测试提示词和描述变更

**对"超级AI个体"构建的参考价值**:
- 企业级Agent基础设施的标杆
- 隔离执行环境的设计值得借鉴
- 版本管理和回滚机制

---

## 2. Microsoft Agent Framework python-1.9.0

**发布时间**: 2026-06-18

**核心更新**:
- **AgentLoopMiddleware**: 支持Agent循环运行中间件
- **工具审批集成**: 将工具审批集成到harness agent中
- **Shell工具集成**: 将shell工具集成到harness agent中
- **AG-UI线程快照持久化**: 可选的AG-UI线程快照持久化和水合
- **采样防护栏**: MCP工具的采样防护栏，默认拒绝服务器发起的采样

**Breaking Changes**:
- MCP工具采样防护栏：默认拒绝服务器发起的采样
- FileAccess工具对齐.NET：添加目录发现和递归搜索
- 声明式工作流执行的额外修复

**技术亮点**:
- 工具审批中间件
- Shell工具集成
- 采样防护栏安全机制

**对"超级AI个体"构建的参考价值**:
- 工具审批机制的设计
- Shell工具的集成方式
- 采样防护栏的安全考虑

---

## 3. LangChain AI Agent框架对比

**发布时间**: 2026年6月

**对比框架**:
- LangChain
- LangGraph
- CrewAI
- Microsoft Agent Framework
- 以及其他

**评价维度**:
- 编排能力
- 可观测性
- 生产就绪度

**关键洞察**:
- 每个框架都有其最佳适用场景
- 编排、可观测性、生产就绪度是核心评价维度
- 选择框架需根据具体需求

---

## 4. JetBrains Top Agentic Frameworks

**发布时间**: 2026年6月2日

**对比框架**:
- LangChain
- CrewAI
- Microsoft Agent Framework
- 其他

**关键洞察**:
- AI Agent框架正在快速演进
- 每个框架都有其独特优势
- 选择合适的框架对项目成功至关重要

---

## 综合分析

### AI Agent框架发展趋势

1. **Harness层抽象**: 从手动编排到配置驱动（Amazon Bedrock AgentCore）
2. **工具审批机制**: 安全考虑日益重要（Microsoft Agent Framework）
3. **隔离执行环境**: 沙盒化成为标配（Amazon Bedrock AgentCore）
4. **版本管理与回滚**: 生产级Agent的必备能力
5. **可观测性**: 内置追踪和监控

### 对"超级AI个体"构建的启示

1. **基础设施选择**: Amazon Bedrock AgentCore提供企业级基础设施
2. **安全机制**: 工具审批和采样防护栏的设计值得借鉴
3. **可观测性**: 内置追踪和监控是生产级Agent的必备
4. **版本管理**: 支持回滚和A/B测试

### 技术栈建议

- **轻量级Agent**: Vercel Eve（TypeScript原生）
- **企业级Agent**: Amazon Bedrock AgentCore（AWS生态）
- **开源Agent**: Microsoft Agent Framework（Python/.NET）
- **编排复杂工作流**: LangGraph

---

## 相关资源

- Amazon Bedrock AgentCore: https://aws.amazon.com/blogs/machine-learning/amazon-bedrock-agentcore-harness-is-now-generally-available-go-from-idea-to-production-grade-agent-in-minutes/
- Microsoft Agent Framework: https://github.com/microsoft/agent-framework/releases/tag/python-1.9.0
- LangChain框架对比: https://www.langchain.com/resources/ai-agent-frameworks
- JetBrains框架对比: https://blog.jetbrains.com/pycharm/2026/06/top-agentic-frameworks-for-building-applications-2026/

---

*创建时间: 2026-06-21 16:39*
*来源: AI Agent框架搜索*
*相关性: "超级AI个体"构建、Agent开发框架*