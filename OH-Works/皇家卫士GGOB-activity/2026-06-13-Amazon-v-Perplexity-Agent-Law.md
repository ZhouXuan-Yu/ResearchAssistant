# Amazon v. Perplexity: CFAA 与 AI Agent 法律边界

> **来源**: 多源综合（Courthouse News, Eric Goldman Blog, Endcap Brief, Jones Day, Goodwin Law）
> **日期**: 口头辩论 2026-06-11，第九巡回法院，西雅图
> **标签**: #Agent法律 #CFAA #AgenticCommerce #Perplexity #Amazon

## 事件概要

第九巡回上诉法院听取 Amazon.com v. Perplexity AI 口头辩论——**首个联邦上诉法院直接审查 AI Agent 是否受 CFAA（计算机欺诈和滥用法）约束**。

核心问题：一个用户明确授权的 AI Agent，在平台单方面撤销授权后继续访问用户的登录账户，是否构成"未经授权的计算机访问"？

## 案件时间线

| 日期 | 事件 |
|------|------|
| 2025-11 | Amazon 起诉 Perplexity，指控其 Comet 浏览器违反 CFAA |
| 2026-03-09 | 地区法官 Chesney 颁发初步禁令，认定 Amazon 可能胜诉 |
| 2026-03-18 | 法院在上诉期间暂时解除禁令 |
| 2026-06-11 | 第九巡回法院听取口头辩论（西雅图） |
| 预计数周/月后 | 书面裁决 |

## 争议焦点

### 1. Comet 是什么？
Perplexity 的 Comet 浏览器可以**登录用户自己的 Amazon 账户，代替用户完成购物**。它不是被动浏览器，而是具有"agentic capabilities"——能够自主查找信息并执行操作。

### 2. Amazon 的立场
- Comet 进入的是**密码保护的账户**，虽然有用户许可，但**没有 Amazon 的授权**
- 参照 Facebook v. Power Ventures 先例：平台可以撤销第三方访问权
- Comet 的 Agent 收集数据造成"技术性损害"

### 3. Perplexity 的立场
- 用户明确指示 Agent 行动，Agent 是用户意图的延伸
- 使用 Comet 类似于通过 Safari 或 Chrome 访问 Amazon
- CFAA 是针对黑客行为的法律，不应成为平台控制互操作性的工具
- ACLU 和 Knight 第一修正案研究所提出了第一修正案挑战

### 4. 法官关注的三个核心问题
- **Van Buren 判例**如何适用于 Agent 流量（用户授权 vs 平台授权）
- **Power Ventures 先例**（针对第三方抓取平台数据）能否延伸到 Agent 代理用户执行指令
- **§502 主张**能否经受第一修正案挑战

## 四种可能的裁决结果

1. **维持禁令**: Amazon 的 C&D 信撤销了授权，Comet 被封
2. **推翻禁令**: 用户授权优于平台 C&D，Agent 可继续运行
3. **发回重审**: 地区法院的 Van Buren 分析不足，退回重审
4. **窄裁决**: 仅基于加州 §502 或第一修正案裁决，回避联邦 CFAA 问题

## 法律学者分析

Eric Goldman（Technology & Marketing Law Blog）：
> "如果 Power Ventures 意味着平台可以否决任何第三方 Agent，那么 CFAA 就变成了 Agent Web 的平台控制法案。但 Power Ventures 不可能永远适用于 Agentic AI——法院迟早要承认，人们应该被允许将自己合法可以做的事情委托给软件。"

## 与已有 Agent 支付生态的关联

Goodwin Law（2026-06）关于 Agentic Payments 授权的分析补充了另一个维度：
- **EFTA/Regulation E**: 消费者向 Agent 提供凭证即推定授权，即使 Agent 超出预期范围
- **TILA/Regulation Z**: 信用卡支付以"实际/暗示/表见代理权限"为标准
- **Visa 新规**: Agent 支付提供商必须注册、建立可防御的授权链、强制交易控制
- **Mastercard**: 类似的 Agentic 交易治理框架

关键缺口：当 Agent 超出授权范围行事时，用户与 Agent 提供商之间的责任分配仍无明确法律依据，需逐案判断。

## 战略意义

| 维度 | 影响 |
|------|------|
| **Agent 合规** | 若 CFAA 适用于 Agent，所有 Agent 产品都需要平台级授权机制 |
| **Agentic Commerce** | 零售平台获得法律工具选择哪些 AI 中介可以在其网站上交易 |
| **用户权利** | 用户是否有权将合法操作委托给 Agent？法律尚未回答 |
| **行业格局** | 大平台可用 CFAA 作为"法律大棒"阻止不喜欢的互操作性 |

## 与 ZhouXuan 体系的关联

- **Agent 技术**: ZhouXuan 的多平台 Agent 体系（Cursor/Codex/Claude Code/HanaAgent/OpenClaw）在技术层面运行良好，但法律层面 Agent 的"授权边界"正在被首次正式审判
- **已有文档线**: Visa/Mastercard Agent Pay + Pine Labs P3P + Coinbase for Agents 构成 Agent 商业化线，本案是该线的**法律基础设施事件**
- **论文方向**: 智能导航系统若涉及 Agent 代理用户执行任务，可能间接受此类判例影响
