# 2026-06-21 Cloudflare Flue框架与Agent三层架构

> 来源：Cloudflare Blog 2026-06-17
> 整理时间：2026-06-21 20:47
> 关键词：Flue、Cloudflare Agents SDK、Pi harness、OpenClaw、Agent架构

---

## 核心洞察：2026年是Agent harness进入生产环境的元年

Cloudflare在6月17日发布的博文提出了一个重要的三层架构模型，用于构建生产级AI Agent：

### 三层架构

```
┌─────────────────────────────────────┐
│  框架层 (Framework) — Flue           │  ← 项目结构、约定、集成、CLI、开发体验
├─────────────────────────────────────┤
│  Harness层 — Pi, Project Think      │  ← 调用工具、读取结果、管理上下文、持续执行
├─────────────────────────────────────┤
│  运行时/平台层 (Runtime) — Agents SDK │  ← 计算、状态、存储原语
└─────────────────────────────────────┘
```

**关键洞察**：一个harness无法独立解决生产环境问题，它依赖于底层平台提供的状态、存储和计算能力。

---

## Flue框架（1.0 Beta）

### 基本信息
- **团队**：来自Astro（知名Web框架）团队
- **底层harness**：基于Pi harness构建（**与OpenClaw使用同一harness**）
- **核心理念**：声明式Agent模型——不编写Agent做什么，而是描述Agent知道什么

### 声明式Agent范式
```javascript
// 传统方式：编写编排循环
// Flue方式：定义上下文，Agent自主解决问题
// 一个bug分类Agent：拦截bug报告→沙箱复现→诊断问题，仅需25行代码
```

### 核心特性

#### 1. Anywhere Agents
- 预配置Channels：Slack、GitHub、Linear、Discord
- 自动处理事件验证和分发样板代码

#### 2. Headless但UI-ready
- 可完全无头运行（后台任务）
- `@flue/react`提供原生前端hooks，流式传输Agent状态、工具执行和实时消息

#### 3. 生产级持久化：Durable Streams
- 执行历史中的每个事件添加到append-only日志
- 每个prompt、工具响应和模型选择作为不可变账本处理
- 进程中断时，另一个实例可从精确断点继续

#### 4. 多云部署
- **Node.js**：每个Agent作为长生命周期进程，可部署到任何VM或容器
- **Cloudflare**：每个Agent成为Durable Object，自动扩展，独立存储和计算

---

## Cloudflare Agents SDK 核心原语

### 1. 持久执行（Durable Execution）
- **Fibers**：原生检查点机制
- `runFiber()`记录进度到Durable Object的SQLite存储
- `stash()`在执行过程中检查点
- `onFiberRecovered()`在中断恢复时交付最后检查点

### 2. 代码执行优于工具过载
- **Code Mode**：给模型一个执行代码的工具，而非一堆工具
- 模型编写TypeScript函数调用所需API，harness执行
- 使用`@cloudflare/codemode`包装Dynamic Workers
- Isolates启动<10ms，每次$0.002，比容器启动快且便宜得多

### 3. 虚拟文件系统
- `@cloudflare/shell`在Durable Object内提供持久虚拟文件系统
- 基于SQLite，提供类型化文件操作（read、write、edit、search、grep、diff）
- 大多数Agent文件系统操作是文本，不需要完整Linux容器

---

## 与现有生态的关系

### Pi harness = OpenClaw的底层
- Flue基于Pi harness构建
- OpenClaw也基于Pi harness
- 这意味着Flue和OpenClaw共享相同的底层执行引擎

### Cloudflare Agents SDK = 云原生Agent运行时
- 为任何harness提供持久执行、动态代码执行、持久文件系统
- 类似于Kubernetes对容器的意义，但专为Agent设计

### 与其他框架的对比
| 框架 | 定位 | 底层harness |
|------|------|------------|
| Flue | 声明式Agent框架 | Pi |
| Vercel Eve | 目录即Agent | 自有 |
| Mastra | Harness层 | 自有 |
| Microsoft Agent Framework | 企业级编排 | 自有 |
| OpenClaw | Agent运行时 | Pi |

---

## 对"超级AI个体"构建的启示

1. **三层架构是趋势**：框架层（开发体验）+ Harness层（执行逻辑）+ 运行时层（基础设施）的分层正在成为标准
2. **声明式Agent是方向**：Flue的理念"描述Agent知道什么，而非做什么"与HanaAgent的技能系统有相似之处
3. **OpenClaw的底层是Pi**：这意味着OpenClaw可以利用Flue的生态和Cloudflare的基础设施
4. **Durable Execution是刚需**：生产级Agent必须解决中断恢复问题，Cloudflare的Fibers方案值得关注
5. **Code Mode优于工具过载**：给模型一个代码执行沙箱比给一堆工具更有效，这与HanaAgent的工具设计理念一致

---

*标签：agent-architecture、flue、cloudflare、pi-harness、openclaw、production-agents*
