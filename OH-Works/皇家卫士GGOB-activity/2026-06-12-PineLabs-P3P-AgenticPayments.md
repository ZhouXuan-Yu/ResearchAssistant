# Pine Labs P3P：AI Agent 自主支付的 UPI 落地

**日期**：2026-06-12  
**来源**：Pine Labs 官方公告 (6/11)、CNBC TV18、Economic Times BFSI  
**标签**：#AgentPayments #UPI #AgenticCommerce #India

## 一句话

Pine Labs 发布 P3P（Pine Labs Payment Protocol），基于印度 UPI 的 mandate 框架实现 AI Agent 无需人工实时认证即可完成支付，是 Agentic Commerce 的首个 UPI 级落地。

## 核心技术机制

- 用户预先授权一次性 mandate（消费上限、条件约束）
- AI Agent 在预设条件触发时自主发起 UPI 交易
- 无需人工 PIN 码或实时确认
- 身份验证和授权控制由 Grantex 提供
- 支持 HTTP 402 机器可读支付请求标准
- 包含审计追踪、消费限额、用户可随时撤销授权

## 已部署案例

| 合作伙伴 | 场景 |
|----------|------|
| **Gullak**（数字黄金储蓄） | 用户设定金价阈值，Agent 自动买入 |
| **Vijay Sales**（电子产品零售） | POC 阶段，Agent 在目标价格触发时自动下单 |

## 定位：Agent Payments 第三条路线

此前已覆盖两条 Agent Payment 路线：

1. **Visa × OpenAI**（6/11）：信用卡网络嵌入 Agent 支付能力
2. **Mastercard AP4M**（6/11）：多智能体支付协议
3. **Pine Labs P3P（本次）**：UPI 公共基础设施上的 Agent 支付

P3P 的独特之处在于它是基于**国家级公共数字支付基础设施**（UPI）构建的，而非私有卡网络。这使其天然具备大规模覆盖的基础——UPI 月活交易量超过 150 亿笔。

## 与 Google AP2 的对比

Google 此前发布的 AP2（Agent Payments Protocol）走区块链 + A2A/MCP 协议路线，面向全球但生态尚在早期。P3P 直接落在已有 4 亿月活用户的 UPI 基础设施上，落地速度更快但局限于印度市场。

## 关键问题（未回答）

- Agent 之间的协商协议细节未公开（如何确定"交易达成"）
- 差错处理机制：Agent 错误购买由谁负责？
- 跨平台 Agent 互操作性：不同供应商的 Agent 如何对等支付？

## 对 ZhouXuan 的意义

Agent 基础设施正在从"能思考"走向"能行动"。支付是行动的终极形式。P3P 表明 Agentic Commerce 的支付瓶颈正在被逐个突破——从 Visa/Mastercard 的信用卡路线到 UPI 的公共基础设施路线，再到 Google AP2 的区块链路线，三条路径并行推进。Agent 自主完成经济交易的能力正在成为现实而非概念。
