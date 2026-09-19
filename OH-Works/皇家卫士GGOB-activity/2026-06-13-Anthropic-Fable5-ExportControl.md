# Anthropic Fable 5 / Mythos 5 遭美国出口管制禁令，全用户停服

> 事件日期：2026-06-13 | 信息源：Reuters, Axios, WIRED, Quartz, BankInfoSecurity, Anthropic 官方声明

## 事件概要

美国商务部部长 Howard Lutnick 于美东时间 6/13（周五）致信 Anthropic CEO Dario Amodei，要求 Anthropic **立即停止向所有外国公民提供 Fable 5 和 Mythos 5 模型的访问权限**，无论该用户身处美国境内还是境外。Anthropic 因无法实时验证每位用户国籍，**被迫对全球所有客户关闭这两个模型**。

这是**首次有前沿 AI 模型被纳入出口管制**。

## 时间线

| 时间 | 事件 |
|------|------|
| 6/9（周一） | Anthropic 发布 Claude Fable 5，首个 Mythos 级公开模型；Mythos 5 限 Project Glasswing 合作伙伴 |
| 6/9-12 | Fable 5 向 Pro/Max/Team/Enterprise 用户免费开放至 6/22 |
| 6/13 周五 17:21 ET | 商务部部长 Lutnick 致信 Amodei，出口管制指令送达（据 Anthropic 和 Neowin 确认） |
| 6/13 周五晚 | Anthropic 宣布全球停服 Fable 5 和 Mythos 5 |
| 6/13 周五晚 | 据 DAWN 报道，政府将 Anthropic 列入**供应链黑名单**（supply chain blacklist） |

**模型仅存活了 3 天即被强制下架。**

## 管制细节

- 商务部要求：向美国境外任何地点、以及美国境内的任何外国公民出口、再出口或国内转让 Fable 5/Mythos 5 均需许可证
- Anthropic 需提交**单独验证许可申请（individually validated licenses）**
- 不遵守将面临**财务和民事处罚**
- 商务部信函**未提供具体国家安全理由**，仅口头说明存在潜在越狱风险

## 起因分析

据 Anthropic 声明、Axios、The Verge、Ars Technica、WSJ、David Sacks 综合报道：

1. **另一家公司声称成功越狱 Fable 5**，引起行政部门警觉（Axios 引用政府官员）
2. **Amazon CEO Andy Jassy 直接向财政部长 Scott Bessent 及其他高级官员举报安全风险**：Amazon 研究人员使用 Claude Fable 5 获取了可用于网络攻击的信息（WSJ 6/13 报道，The Information 和 Reuters 交叉确认）
3. **David Sacks**（前白宫 AI 沙皇，现任总统科技顾问委员会联席主席）披露："一位对 Anthropic 和美国政府都高度可信的合作伙伴站出来提供了越狱信息"，且"行政部门要求 Dario 修复越狱或撤回模型，**Dario 拒绝了**"
4. 商务部长 Lutnick 于 6/12 美东 17:21 发出出口管制信函
5. Anthropic 审查后认为，该越狱涉及的是**窄范围漏洞**（让模型读取特定代码库并识别软件缺陷），且**GPT-5.5 等其他已部署模型具备同等能力**
6. Anthropic 表示不认同"发现窄范围越狱就召回面向数亿用户的商业模型"的做法
7. Anthropic 称政府仅提供了"口头证据"（verbal evidence），且漏洞为"非通用型"（non-universal）
8. Anthropic 此前已与美国政府、英国 AISI、多个第三方组织和内部团队进行了数千小时的红队测试，**尚未发现通用越狱方法**

### Amazon 的角色：最大投资方反手举报

这是事件最戏剧性的维度。Amazon 对 Anthropic 投资超过 **$25B**，持股潜在价值达 **$135B**，是其最大云服务提供商和最大私人投资方。然而 Jassy 选择主动向政府举报自家投资对象的安全风险。

两种解读：
- **国家安全立场**：Jassy 作为公民而非仅作为 CEO 判断 Fable 5 构成真实安全威胁（该模型可自主工作时间远超此前任何 Claude，Mythos 已发现数千个零日漏洞）
- **政治定位**：6/2 白宫 AI 行政令建立了审查先进 AI 系统的框架，并要求机构终止与"反复限制政府使用其技术"的公司的合同。在此环境下，公开举报 Anthropic 可能是 AWS 保持与政府良好关系的代价

## Anthropic 的回应要点

- "我们相信这是一个误解，正在努力尽快恢复访问"
- "如果这一标准应用于整个行业，本质上将阻止所有前沿模型提供商的新模型部署"
- 呼吁政府通过**透明、公正、基于技术事实的法定程序**来阻止不安全的部署
- 承诺 24 小时内公布更多技术细节
- AWS 已按要求撤销所有区域的模型访问

## 行业影响与格局

### 直接影响
- **所有 Fable 5/Mythos 5 用户**（包括美国公民）暂时无法使用
- Anthropic 自身的**外国籍员工**（包括联合创始人 Chris Olah、研究员 Andrej Karpathy、哲学家 Amanda Askell）理论上也在限制范围内
- 前白宫官员 Dean Ball 指出："这意味着你可能需要证明自己的公民身份才能使用 Anthropic 模型"

### 深层信号
1. **AI 模型正式进入出口管制体系**，与芯片、军事技术同级对待
2. **五角大楼将 Anthropic 列入供应链黑名单**（太危险政府自己不能用）+ 商务部出口管制（太危险外国人不能用），双重夹击
3. Anthropic 同时被国防部和商务部"两边不讨好"——既不够安全供政府使用，又太强大不能出口
4. 如果 GPT-5.5 不受类似管制，存在**选择性执法**问题
5. 对中国用户影响：**直接丧失 Fable 5/Mythos 5 访问权**，即使通过第三方渠道也面临法律风险

## 与 ZhouXuan 此前文档的关联

- 2026-06-10 文档《Claude Fable 5 Mythos》和《Secret Sabotage》记录了 Fable 5 发布
- 2026-06-11 文档《OpenAI Price War》记录了 Anthropic 面临的竞争压力
- 此次事件将 Anthropic 从"商业竞争"叙事推向**地缘政治博弈**叙事
- 对 ZhouXuan 的启示：DeepSeek 等国产模型的战略价值进一步凸显，自主可控的模型栈更加重要

## 模型定价与可用性参考（MarkTechPost）

| 模型 | 级别 | 当前状态 | 保障措施 | 定价 | 原可用渠道 |
|------|------|----------|----------|------|------------|
| Claude Fable 5 | Mythos-class | 全用户停服 | 完整分类器；回退至 Opus 4.8 | $10/M input, $50/M output | API `claude-fable-5` |
| Claude Mythos 5 | Mythos-class | 全用户停服 | 网络安全保障已解除 | $10/M input, $50/M output | 仅 Glasswing 合作伙伴 |
| Claude Mythos Preview | Mythos-class | 受限（Glasswing） | 有限发布 | 高于 Fable 5 | 自 4 月起受信合作伙伴 |
| Claude Opus 4.8 | Opus-class | **完全可用** | 标准保障 | 标准费率 | 所有渠道，不受影响 |

## 完整对抗时间线（ainvest 补充）

| 时间 | 事件 |
|------|------|
| 2026/1 | 五角大楼要求 Anthropic 解除 Claude 在大规模监控和自主武器方面的使用限制，**Anthropic 拒绝** |
| 2026/2/27 | **特朗普下令所有联邦机构立即停止使用 Anthropic 技术**，五角大楼终止 $200M 合同并将 Anthropic 列为供应链风险 |
| 2026/3/26 | 联邦法官 Rita Lin 颁布临时禁令，认定五角大楼行为违反 Anthropic 第一修正案和正当程序权利 |
| 2026/4/8 | 联邦上诉法院驳回 Anthropic 要求撤销供应链标签的动议 |
| 2026/6/2 | **白宫 AI 行政令**签署，建立审查先进 AI 系统框架，要求机构终止与"反复限制政府使用"的公司的合同 |
| 2026/6/9 | Anthropic 发布 Fable 5 和 Mythos 5 |
| 6/9-12 | Fable 5 向 Pro/Max/Team/Enterprise 用户免费开放至 6/22 |
| 6/12 周五 17:21 ET | 商务部部长 Lutnick 致信 Amodei，出口管制指令送达 |
| 6/13 周五晚 | Anthropic 宣布全球停服 Fable 5 和 Mythos 5 |
| 6/13 周五晚 | 据 DAWN 报道，政府将 Anthropic 列入**供应链黑名单**（supply chain blacklist） |
| 2026/6/11 | Anthropic 向联邦法院申请即决判决（summary judgment），称政府"对报复行动的坦率程度令人震惊" |

**格局：** Anthropic 既被国防部视为"太危险不能用"（供应链黑名单），又被商务部视为"太强大不能出口"（出口管制）。两个机构同时施压，Amazon 最大投资方反手举报，凸显 AI 公司在国家安全、技术创新与商业利益间的三角博弈。

## 6/15 更新：Anthropic 派高级技术团队赴华盛顿面谈

> 来源：Republic World, WSWS, buildfastwithai 6/15 汇总

### 新进展

1. **Anthropic 派遣高级工程师团队赴华盛顿进行面对面会谈**，试图修复与白宫的裂痕。此前整个周末双方已进行了虚拟会议，但效果不佳，Anthropic 决定升级为面对面沟通。
2. **白宫 AI 顾问 David Sacks 公开表态**："行政部门的期望是 Anthropic 修复安全问题，出口管制被解除，Fable 5 恢复全面发布"，并补充"行政部门希望这一切尽快发生"。这是政府首次公开释放恢复信号。
3. **Anthropic 提出全球暂停方案**（global pause proposal），试图以安全修复换取管制解除。
4. **Claude 订阅升级退款**：6/9 后升级账户的用户如在 6/20 前取消可获按比例退款。
5. **事件被多家主流媒体社论定性为"竞争对手利用政府权力打击对手旗舰模型"**（Newswav 深度报道），但无人在记录中明确指名。
6. **WSWS 将事件定性为"美国政府首次强制下架已部署的 AI 模型"**，指出周日早间政论节目未提及此事，主流报纸将报道深埋。

### 关键解读

- Sacks 的公开表态是转折点。此前政府立场极度强硬（90分钟最后通牒），现在主动释放"希望恢复"的信号，可能意味着：
  - 政府内部对管制力度存在分歧
  - Anthropic 的华盛顿游说初见成效
  - 即将到来的 IPO 压力迫使政府考虑市场影响
- 但"remediate"一词意味着 Anthropic 必须先证明安全问题已修复，而非政府直接撤回管制
- Anthropic 的"全球暂停"方案本质上是用技术层面的安全增强换取政治层面的出口管制解除

## 后续关注点

- [ ] Anthropic 24 小时内发布的技术细节（承诺 6/14 前公布）
- [ ] 美国政府是否会以同样标准审查 OpenAI GPT-5.5 等模型
- [ ] 是否有其他国家/公司跟进类似管制
- [x] Fable 5/Mythos 5 恢复访问的时间表 → 6/15 Sacks 释放恢复信号，等待 Anthropic 修复方案
- [ ] 此事件对 Anthropic IPO 进程的影响
- [ ] Anthropic v. DoW 案即决判决结果
- [ ] Anthropic 华盛顿面谈结果
- [ ] Claude Sonnet 4.8 是否因 Fable 5 事件推迟（源代码泄露显示 August-September 2026 GA）
