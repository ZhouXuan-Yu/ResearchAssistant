# 2026年6月最新AI Agent框架进展

> 创建时间：2026-06-21 16:08
> 主题：AI Agent开发框架、工具链、智能体架构

## 1. Vercel Eve：目录即Agent的TypeScript框架

**发布时间**：2026年6月17日（Ship 26大会，伦敦）

**核心理念**：像Next.js为Web应用所做的那样，Eve为Agent提供标准化的构建方式。

**架构设计**：
- **Agent即目录**：每个Agent是一个文件目录
  - `instructions.md`：系统提示词
  - `agent/tools/`：TypeScript工具定义
  - `agent/skills/`：Markdown技能文件
- **部署方式**：编译为Vercel Functions上的持久化服务
- **模型无关**：通过Vercel AI Gateway路由请求，支持任何模型提供商

**内置6大生产级功能**：
1. **持久执行**：会话状态通过Vercel Workflow持久化和重放
2. **沙盒计算**：Vercel Sandbox隔离执行环境
3. **人工审批**：Human-in-the-loop审批工作流
4. **子Agent**：支持Agent嵌套和委托
5. **OpenTelemetry追踪**：内置可观测性
6. **评估系统**：内置evals测试框架

**技术细节**：
- 许可证：Apache 2.0
- 当前版本：eve@0.11.8（2026-06-20发布）
- GitHub星标：1826（截至6月20日）
- 主要语言：TypeScript (96.6%)
- 创建时间：2026-06-16

**行业背景**：
- Vercel CEO Guillermo Rauch表示，Agent现在触发了平台上超过一半的提交
- 6个月前这个比例还不到3%
- Eve的定位是防止这种增长回归到一次性基础设施搭建

**对"超级AI个体"构建的参考价值**：
- 目录即Agent的设计理念与HanaAgent的技能系统有相似之处
- TypeScript原生适合前端/全栈开发者
- 内置的持久化和可观测性解决了Agent开发的常见痛点

---

## 2. Mastra Harness：Agent harness层的开源实现

**发布时间**：2026年6月

**核心概念**：Harness是Agent循环外层的封装，提供对话管理、记忆、存储、工具控制等能力。

**主要特性**：
1. **Session管理**：跨轮次持久化状态
2. **线程生命周期**：创建、切换、重命名、删除、克隆
3. **子Agent生成**：包括fork重用缓存前缀
4. **多轮对话**：follow-up队列 + steer()方法
5. **用户交互**：内置ask_user工具，暂停执行等待用户输入
6. **模式切换**：plan和build模式，各有独立的工具、模型和指令

**事件系统**：
- 发布/订阅架构
- 35个信号，包括：agent_start、tool_input_delta、tool_suspended、subagent_text_delta、follow_up_queued、usage_update、thread_changed等

**审批机制**：
- 工具调用审批可跨会话保持
- 可针对单个工具或整个类别授予权限
- 授予后Agent不再重复询问

**版本要求**：@mastra/core@1.43.0或更高

**技术特点**：
- TypeScript原生
- 由MastraCode（TUI编码Agent）发展而来
- Y Combinator支持的创业项目

---

## 3. Microsoft Agent Framework：企业级Agent编排

**发布时间**：2026年4月3日GA（Python和.NET同时发布1.0）

**定位**：AutoGen和Semantic Kernel的统一继任者

**技术架构**：
- 结合AutoGen的对话式多Agent抽象
- 融合Semantic Kernel的企业特性（会话状态管理、中间件、遥测、类型安全）
- 新增基于图的工作流，显式控制多Agent执行路径

**配置方式**：
- 声明式YAML Agent配置
- 支持版本控制部署
- 从Semantic Kernel和AutoGen的迁移助手

**集成能力**：
- Azure AI Foundry负责任AI护栏
- 双运行时支持（Python + .NET）

**适用场景**：
- 已在Microsoft技术栈中的团队
- 需要企业级Agent编排
- 需要图形化工作流控制

---

## 4. 其他主流框架对比（2026年6月状态）

| 框架 | 类型 | 开源 | 最佳适用场景 |
|------|------|------|--------------|
| **LangChain** | LLM应用框架 | MIT | 快速原型化复杂Agent工作流 |
| **LangGraph** | Agent运行时 | MIT | 需要精确控制的复杂Agent |
| **Deep Agents** | Agent harness | MIT | 长时间运行的工作流 |
| **CrewAI** | 多Agent编排框架 | MIT | 基于角色的Agent工作流快速原型 |
| **LlamaIndex Workflows** | Agent工作流框架 | MIT | 文档中心、事件驱动的多Agent系统 |
| **Google ADK** | Agent开发框架 | Apache 2.0 | GCP原生团队，开箱即用的Agent运行时 |
| **OpenAI Agents SDK** | 多Agent工作流SDK | MIT | 紧凑的助手和委托工作流 |
| **Mastra** | AI Agent应用框架 | 部分开源 | TypeScript团队构建生产级自定义Agent |
| **Vercel Eve** | Agent框架 | Apache 2.0 | TypeScript原生，Vercel平台部署 |

---

## 5. 技术趋势分析

### 5.1 Agent-as-Code成为主流
- Eve的"Agent即目录"理念
- 声明式配置（YAML/Markdown）降低认知负担
- 代码即Agent，Agent即代码

### 5.2 持久化与可观测性成为标配
- 会话状态持久化
- OpenTelemetry集成
- 内置评估系统

### 5.3 人工审批成为标准功能
- Human-in-the-loop不再是可选
- 工具调用审批机制
- 安全性与控制权的平衡

### 5.4 TypeScript生态崛起
- Eve、Mastra、Inngest AgentKit等TypeScript原生框架
- 与前端/全栈开发者的契合度更高
- 边缘部署优势

---

## 6. 对ZhouXuan"超级AI个体"构建的启示

### 6.1 框架选择建议
- **HanaAgent已有成熟架构**：不需要完全迁移，但可借鉴Eve的目录结构设计理念
- **技能系统优化**：参考Eve的skills/目录组织方式
- **可观测性增强**：考虑集成OpenTelemetry或Langfuse

### 6.2 工具链整合思路
- **多框架协作**：不同框架解决不同问题
- **标准化接口**：借鉴MCP协议的工具标准化思路
- **本地优先**：保持对本地模型（Ollama）的支持

### 6.3 下一步行动建议
1. **研究Vercel Eve源码**：学习其目录即Agent的设计
2. **评估Mastra Harness**：了解其事件系统和审批机制
3. **关注Microsoft Agent Framework**：企业级场景的参考
4. **保持框架多样性**：不同项目可能需要不同框架

---

## 7. 相关资源

**官方文档**：
- Vercel Eve: https://vercel.com/eve
- Mastra: https://mastra.ai
- Microsoft Agent Framework: https://learn.microsoft.com/en-us/semantic-kernel/

**GitHub仓库**：
- vercel/eve: https://github.com/vercel/eve
- mastra-ai/mastra: https://github.com/mastra-ai/mastra

**行业分析**：
- LangChain框架对比: https://www.langchain.com/resources/ai-agent-frameworks
- JetBrains框架评测: https://blog.jetbrains.com/pycharm/2026/06/top-agentic-frameworks-for-building-applications-2026/

---

*笔记创建于2026年6月21日下午，基于网络恢复后的最新AI Agent框架动态整理。*