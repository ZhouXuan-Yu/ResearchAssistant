# 2026-06-09 巡检自学：Claude Opus 4.8 & 动态工作流

## Claude Opus 4.8 (5月28日发布)

来源：Anthropic 官方 + Releasebot + Bind AI

- 相比 4.7 全面提升基准，SWE-bench DeepSWE 评分 58%
- 同价：$5/M input / $25/M output
- 新增 **Effort Control**：claude.ai 和 Cowork 中可选 low/medium/high/xhigh/max
  - Claude Code 中对应 `ultracode` 模式（xhigh effort）
- 新增 **动态工作流 (Dynamic Workflows)**：Claude Code 支持并行数百个子 Agent，验证后再汇报
  - 8号已 GA，适用于 Max/Team/Enterprise 及 API
  - 场景：跨代码库迁移、安全审计、并行 Bug 搜索
  - 中断后可断点续跑，token 消耗量大
- Fast mode 比前代便宜 3 倍：$10/M input / $50/M output
- Messages API 支持 system entries 插入消息数组中间，不中断 prompt cache

## Claude Code 定价改版 (6月15日生效)

重大变化：程序化使用（agentic 任务）从订阅通用算力池分离到独立信用额度池，按 API 全价计费。

| 方案 | 月费 | Claude Code 额度 | 约交互次数 |
|------|------|-----------------|-----------|
| Pro | $20 | $20 | ~1,450 |
| Max 5x | $100 | $100 | ~7,250 |
| Max 20x | $200 | $200 | ~14,500 |

关键点：
- 额度用完后 agentic 功能暂停，直到下个计费周期或购买额外额度
- claude.ai 交互式聊天不受影响
- Opus 4.8 tokenizer 比前代多 35% token，实际成本更高
- 建议策略：日常用 Opus 4.8 fast mode，复杂任务才用全能力
- JetBrains 2026 调查：Claude Code 在小公司中采用率 75%，#1

> 对 ZhouXuan 的影响：如果常用 Claude Code 做 agentic 工作，6月15日后需关注额度使用。ultracode 模式配合动态工作流是大杀器，但 token 开销也大。
