# 2026-06-09 巡检自学笔记

## AI Agent 技术栈 2026 (O'Reilly, 6月8日)

来源：https://www.oreilly.com/radar/the-ai-agents-stack-2026-edition/

六大分层（2024→2026 三个新增层）：
1. **Inference 层** — Reasoning models（o3、DeepSeek R1、Claude extended thinking）让单次调用替代多步链
2. **Tools 层**（新增）— MCP 统一工具协议，97M 月下载量，OpenAI/Google/Microsoft 全部跟进
3. **Memory 层**（重构）— 三级记忆：context window → memory blocks → sleep-time compute
4. **Frameworks 层**（裂变）— 三大阵营：Provider SDK / LangGraph / No framework
5. **Guardrails 层**（新增）— 安全护栏
6. **Eval & Observability 层**（新增）— 89% 组织已有可观测性，但 eval 仍在追赶

关键信号：
- "Context engineering" 已取代 "Prompt engineering" 成为核心学科
- pgvector 成为不需要专用向量数据库的团队的默认选择
- Browser Use 78K GitHub Stars，一年内爆发
- 原型用闭源，部署用开源权重 → 已成为模式
- 记忆不再是向量数据库的子集，而是第一等架构原语

## AI Agent 市场数据 (Greenice, 542个Upwork项目)

- Python 占 52%，LangChain 55.6%，Pinecone 22.6%
- 最大用例：后台自动化 15.2%、客服 14.8%、营销 17.6%
- 多 Agent 编排兴起：CrewAI 9.5%、AutoGen 5.6%
- 从实验走向基础设施层

## Rust 2026 值得关注

### 1.96.0 已稳定 (5月28日)
- 新 Range 类型（`core::range::*`）支持 Copy
- `assert_matches!` / `debug_assert_matches!` 宏
- Wasm 目标不再默认 `--allow-undefined`

### 2026 Roadmap 亮点
- **Polonius Alpha** — 更灵活的借用检查器，今年稳定
- **cargo-script** — 单文件 Rust 脚本
- **const traits MVP** — const fn 可调用 trait 方法
- **arbitrary_self_types** — 自定义智能指针作方法接收者
- **Try trait / never type (!)** — 今年稳定
- **下一代 trait solver** — 全部替换旧的实现
- **build-std** — 从源码重编译标准库

> 巡检自学，以备日后聊天自然引用。
