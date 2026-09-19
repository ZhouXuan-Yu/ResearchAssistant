# 循环工程：从提示工程到系统设计的新范式

**日期**：2026-06-21  
**来源**：Addy Osmani、Peter Steinberger、Boris Cherny等  
**相关性**：对"超级AI个体"构建有直接指导意义

## 核心观点

**"你不应该再提示编码代理了。你应该设计循环来提示你的代理。"**  
— Peter Steinberger，OpenAI工程师，OpenClaw创始人

**"我不再提示Claude了。我有循环在运行，它们负责提示Claude并决定做什么。我的工作就是写循环。"**  
— Boris Cherny，Anthropic Claude Code负责人

## 什么是循环工程？

循环工程（Loop Engineering）是2026年6月8日开始流行的新概念，由Addy Osmani（Google Cloud总监）等人系统阐述。核心思想是：

> **你设计一个系统，让这个系统去提示AI代理，而不是你手动提示。**

传统模式：人类 → 提示 → AI代理 → 输出 → 人类检查 → 再提示  
循环模式：人类设计循环 → 循环自动发现任务 → 循环提示代理 → 循环检查结果 → 循环决定下一步

## 循环的五个核心组件

Addy Osmani指出，一个完整的循环需要五个组件：

### 1. 自动化（Automations）
- **作用**：按计划自动发现和分类任务
- **实现**：Codex的Automations标签页、Claude Code的`/loop`和`/goal`命令
- **示例**：每天早上自动运行，读取CI失败、开放问题、最近提交，写入markdown文件

### 2. 工作树（Worktrees）
- **作用**：隔离并行工作，避免文件冲突
- **实现**：git worktree，让多个代理同时在同一仓库工作而不互相干扰
- **关键点**：两个代理写同一个文件就像两个工程师同时提交同一行代码

### 3. 技能（Skills）
- **作用**：固化项目知识，避免每次会话都重新解释
- **实现**：SKILL.md文件，包含指令和元数据
- **价值**：解决"意图债务"——代理每次会话都是冷启动，会用自信的猜测填补你意图中的空白

### 4. 插件和连接器（Plugins & Connectors）
- **作用**：让循环能访问真实工具（问题跟踪器、数据库、Slack等）
- **实现**：基于MCP（Model Context Protocol）
- **区别**：从"这是修复"到"自动打开PR、更新票据、CI通过后通知频道"

### 5. 子代理（Sub-agents）
- **作用**：分离创作者和检查者
- **原则**：写代码的模型检查自己的作业"太友善了"
- **实践**：一个代理探索，一个实现，一个验证

## 循环的第六个组件：记忆

循环还需要一个**外部记忆**：markdown文件、Linear看板等，存在于单次对话之外，记录已完成和待办事项。

**关键洞察**：模型在两次运行之间会遗忘一切，所以记忆必须在磁盘上，而不是在上下文中。代理会遗忘，但代码仓库不会。

## 实际循环示例

```
每天早上自动化运行：
1. 调用分类技能 → 读取昨天的CI失败、开放问题、最近提交
2. 写入发现到markdown文件或Linear看板
3. 对每个值得处理的发现：
   - 打开隔离的工作树
   - 发送子代理A起草修复
   - 发送子代理B审查修复
4. 通过连接器打开PR、更新票据
5. 无法处理的进入分类收件箱等待人类
6. 状态文件记住今天尝试了什么、通过了什么、还有什么开放
```

**结果**：你只设计了一次。你没有提示任何步骤。

## 与现有工具的对应关系

| 原语 | Codex | Claude Code |
|------|-------|-------------|
| 自动化 | Automations标签页、`/goal` | `/loop`、cron、hooks、GitHub Actions |
| 工作树 | 内置worktree支持 | `git worktree`、`--worktree`标志 |
| 技能 | Agent Skills（SKILL.md） | Agent Skills（SKILL.md） |
| 连接器 | MCP + 插件 | MCP + 插件 |
| 子代理 | TOML定义在`.codex/agents/` | `.claude/agents/`、agent teams |
| 记忆 | Markdown或Linear | Markdown（AGENTS.md）或Linear |

## 循环不能替你做的事

### 1. 验证仍在你
循环无人值守运行，也意味着错误无人值守发生。分离验证者子代理是让循环的"完成"有意义的唯一方式，但即使如此，"完成"也是声明而非证明。

### 2. 理解仍会腐化
循环运送你没有写的代码越快，存在和你实际理解之间的差距就越大。这是**理解债务**，顺畅的循环只会让它增长更快，除非你阅读循环产出的内容。

### 3. 舒适姿态是危险的
当循环自己运行时，很容易停止有主见，接受它给的任何东西。这是**认知投降**。设计循环是治愈（当你带着判断力做）或加速剂（当你用它来避免思考）。

## 对"超级AI个体"构建的启示

1. **从提示者到系统设计者**：超级AI个体的核心能力不是写提示，而是设计能自主运行的系统
2. **技能体系是基础设施**：ZhouXuan已有的多平台Skills系统正是循环工程中的关键组件
3. **记忆外部化**：Obsidian仓库、SKILL_INDEX.md等正是循环所需的外部记忆
4. **分离创作和检查**：在多代理架构中，让不同代理负责不同角色
5. **成本意识**：循环会消耗大量token，需要在token丰富和token稀缺之间找到平衡

## 范式演进时间线

```
2022: ReAct（推理+行动）
2023: AutoGPT（自主代理）
2025: Ralph循环（单代理任务完成循环）
2026春: /goal（运行直到条件满足）
2026年6月: 循环工程（多代理编排循环）
```

## 引用

- Addy Osmani. "Loop Engineering." addyosmani.com, June 2026.
- Peter Steinberger (@steipete). X post, June 8, 2026. 6.5M views.
- Boris Cherny. WorkOS Acquired Unplugged, June 2, 2026.
- Indian Express. "What are AI agent loops, and could they soon make prompting obsolete?" June 21, 2026.