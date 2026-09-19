# Langfuse 仓库导航摘要

## 它是什么

Langfuse (YC W23) 是一个开源 LLM 工程平台，覆盖开发、监控、评估、调试 AI 应用的全生命周期。核心功能：Trace 追踪 API 调用链、Prompt 管理与版本控制、Evaluation 自动评估输出质量、Observability 以 Wide Events 为核心的列式分析。

仓库版本：**v3.182.0** | License: MIT | Runtime: Node 24 + pnpm 11

## 架构全貌

```
langfuse/
├── web/                     # Next.js 前端 + tRPC + Public REST API
├── worker/                  # 队列消费者，后台处理
├── packages/shared/         # 共享领域模型、DB Schema、队列契约
│   ├── prisma/schema.prisma     # Postgres 主库 Schema
│   ├── clickhouse/migrations/   # ClickHouse 列存迁移
│   └── src/server/queues.ts     # 队列负载定义
├── ee/                      # 企业版功能包
├── fern/                    # API 定义源（生成 OpenAPI/多语言 SDK）
└── generated/               # 自动生成的 API 客户端（禁止手动修改）
```

依赖方向：
- `web` → `@langfuse/shared` + `@langfuse/ee`
- `worker` → `@langfuse/shared`
- `@langfuse/ee` → `@langfuse/shared`
- `@langfuse/shared` 不依赖任何业务包（单向依赖根节点）

## 技术栈速览

- **前端**：Next.js (Turbopack) + tRPC + shadcn/ui + Storybook
- **后端核心**：Node 24 + TypeScript + Prisma (Postgres) + ClickHouse
- **队列**：BullMQ / Redis 系列
- **构建**：pnpm workspace + Turbo (monorepo 编排)
- **测试**：Vitest (单元/集成) + Playwright (E2E)
- **部署**：Docker Compose 全套开发基础设施

## 架构哲学（来源于生产规模实践）

核心思想：**Wide Events 而非拆散的 Metric/Log/Trace 三元组**。

- 以 Observation（观测点）为主要分析单元，Trace 只是相关 Observation 的关联句柄
- 保留高基数上下文字段，让用户用任意维度切片、过滤、调试未知问题
- 偏向不可变/追加式事件记录，避免更新操作带来的隐藏查询成本
- 列式存储 + 时间范围扫描 + 有序键 + 数据裁剪构建查询路径
- 成本与运维简洁性是架构约束，每多一个数据库/队列/物化视图都要论证其价值

## 与 ZhouXuan 的 AI 工具链的关系

Langfuse 对"超级 AI 个体"工具链的潜在价值：

1. **跨平台 Trace**：追踪 Cursor/Codex/HanaAgent/OpenClaw 各平台的 API 调用链路
2. **Token 消耗可视化**：正好解决之前讨论的 token 优化需求，有精确的用量 + 成本面板
3. **Prompt 版本管理**：各平台 skill 的 prompt 可统一管理、A/B 测试、回滚
4. **输出评估**：对 AI 生成内容进行自动化质量打分（准确性、相关性、毒性等）
5. **自托管**：支持 Docker Compose 本地部署，数据完全自主

## 探索起点建议

如果你要深入看代码，高信号入口：

- 领域模型：`packages/shared/src/domain/{observations,traces,scores}.ts`
- 数据库设计：`packages/shared/prisma/schema.prisma`
- 队列设计：`packages/shared/src/server/queues.ts`
- 架构原则：`.agents/ARCHITECTURE_PRINCIPLES.md`
- 快速启动：`pnpm run dx`（全栈开发环境一键拉起，需要 Docker）

## 补充：2026-03 架构简化

Langfuse 在 2026 年 3 月做了一次大规模简化重构，核心变动是砍掉了多余的中间层和物化视图，回归「Wide Events + ClickHouse 列式直查」的简洁路线。官方博文：[Simplifying Langfuse for Scale](https://langfuse.com/blog/2026-03-10-simplify-langfuse-for-scale)，如果你想理解为什么这个架构是现在这个样子，这篇值得一读。
