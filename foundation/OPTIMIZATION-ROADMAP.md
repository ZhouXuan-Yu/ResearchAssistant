# 科研智能体优化路线（调研驱动）

| 项 | 值 |
|---|---|
| 日期 | 2026-09-18 |
| 制定者 | 科研助手（agent-mu42qzfz） |
| 方法 | 调研 GitHub 顶级项目 + 学术综述 + 评测基准 + MCP 生态 + 中文社区，再对标自身现状 |
| 自身基线 | F0–F7 完成：144 技能（含分类与路由）、质量门禁、记忆、备份回滚、健康自检、技能自进化协议 |
| 证据约定 | 【实】=我核实到的一手来源；【推】=我的判断；【待】=未验证 |

---

## 一、调研结论：业界把"科研智能体"做到了什么程度

### 1.1 研究生命周期已被标准化为 8 阶段 / 4 相位
来源：worldbench《AI for Auto-Research: Roadmap & User Guide》（arXiv 2605.18661，2026）【实】

| 相位 | 阶段 |
|---|---|
| **Creation** | 选题生成、文献综述与检索、编码与实验、表格与图 |
| **Writing** | 稿件撰写与润色 |
| **Validation** | 同行评审（自动生成/匹配/质量评估）、返修与回复 |
| **Dissemination** | 论文转 slides/poster/视频/网站/社媒 |

### 1.2 系统成熟度存在明确分级
来源：清华 THU-KEG《Awesome AI for Research》【实】。其 L3 代表是 **EurekAgent**，特征是：**权限受限执行 + 产物记忆（artifact memory）+ 预算控制 + 人类监督**。

### 1.3 评测锚点已成体系（衡量"是否真的更强"）
来源：同上 Benchmarks 页【实】。清单包括 **PaperBench（OpenAI，复现 20 篇 ICML 2024 论文：读懂→建代码库→跑通实验）**、EXP-Bench、AutoResearchBench、ResearchClawBench、AstaBench（Allen AI）、FrontierScience、MLE-Bench、RE-Bench、ScienceAgentBench、DiscoveryBench、LAB-Bench、PostTrainBench、PaperWritingBench、KernelBench/TritonBench、AutoMat。

### 1.4 技能生态出现了直接对标物
来源：**K-Dense-AI/scientific-agent-skills**【实】。**166 个科研技能**，按学科域组织，遵循开放 Agent Skills 标准，可整包作为插件加载；配套本地 co-scientist（BYOK，100+ 科学数据库，可弹性上云）。有论文：《A Library of Procedural Knowledge for Research Agents》（arXiv 2609.00065）。关键点：**每个技能配的是"精选文档 + 可运行示例"，不是纯指令**。

### 1.5 学术检索基础设施成熟且多可免密钥
【实】OpenAlex 基本使用**无需 API key**；arXiv、Crossref 免密钥；Semantic Scholar 无 key 约 100 请求/5 分钟、有 key 1 RPS。MCP 侧已有 Semantic Scholar / OpenAlex / Crossref / arXiv / PubMed / bioRxiv 等服务器。

### 1.6 反面警示已有专门研究
【实】《Hidden Pitfalls of AI Scientist Systems》（arXiv 2509.08713，附仓库 niharshah/AIScientistPitfalls）。说明该领域的失败模式已被系统梳理。

---

## 二、对标后我的差距（按杠杆排序）

| # | 差距 | 现状 | 业界做法 |
|---|---|---|---|
| **G1** | **检索层是"通用网页搜索"** | 仅 `anysearch_free`；学术库一个未接 | OpenAlex/arXiv/Crossref 免密钥直连 + MCP 学术服务器 |
| **G1b** | **沉睡资产未启用** | **Zotero MCP 连接器已在运行，暴露 53 个工具，我从未使用**【实】 | 文献库是科研 agent 的核心资产 |
| **G2** | **无复现闭环** | 有 `exec_command`，但无 paper→code→run→verify 的沙箱流程与产物管理 | PaperBench 范式；EurekAgent 的 artifact memory |
| **G3** | **无自我评测** | 无法回答"我比上周强了吗" | 用基准（或自建冻结任务集）量化 |
| **G4** | **核验是规则不是机制** | 有 F/L/I/U 与引用登记，但无"论断-来源吻合度"的自动审计 | ARS v3.8 的 claim-faithfulness gate |
| **G5** | **技能"数量够、锚点弱"** | 144 个，多为指令型 | K-Dense：文档 + 可运行示例 + 域内数据源 |
| **G6** | **无预算/权限/产物边界** | exec 权限极宽（实测可写 `.hanako`） | 权限受限执行 + 预算控制 + 人类监督 |
| **G7** | **无多智能体协作** | 已出方案未建 | AI co-scientist、Virtual Lab/Biotech |
| **G8** | **自进化闭环未验证** | skill-forge 已建，无效果证据 | 用指标度量自建技能是否真提升 |
| **G9** | **知识资产层为空** | `research/40-knowledge` 只有规范 | 本体 + 图谱 + 产物记忆 |

---

## 三、优化路线（分阶段）

### P0 · 打通学术检索层 【最高杠杆，立即可做】
- **动作**
  1. **盘点 Zotero MCP 的 53 个工具**（沉睡资产，可能已能查库、取元数据、写条目）。
  2. 自建 `academic-search` 脚本：直连 **OpenAlex + arXiv**（免密钥），支持关键词检索、元数据抽取、引用关系、DOI 解析。
  3. 把结果接进既有 `nature-academic-search` / `nature-ref-verifier` 流程。
- **产出**：`foundation/academic-search/` 脚本 + 检索能力进入路由表
- **验收**：给定一个主题，能从 OpenAlex 取回真实论文元数据，且每条带 DOI 与来源 URL，可用 `nature-ref-verifier` 核验
- **依赖**：无（免密钥）；Semantic Scholar 若要提速率需你提供 key
- **风险**：限流 → 脚本内做退避与缓存

### P1 · 复现与实验层（PaperBench 范式的最小可用版）
- **动作**：沙箱化代码执行 + 实验编排 + **产物记忆**（每次运行的代码/日志/结果可回溯）+ 复现检查清单
- **验收**：能对一篇**自选开源论文**的某个小实验做「读→写码→跑→对表」并留下可复现记录
- **风险**：算力与环境隔离；先做"小实验"而非整篇复现

### P2 · 自动化核验机制
- **动作**：把"论断 ↔ 来源"的吻合度审计做成脚本（抓取来源 → 比对论断 → 输出 supported/partial/unsupported），接入 G1 门禁
- **验收**：故意写一条"来源不支持"的论断，审计必须报 unsupported

### P3 · 个人评测基准 v0
- **动作**：冻结一组**方向无关**的科研任务（检索、核验、统计审查、绘图、复现），定义打分与阈值；每次改动前后跑一遍
- **验收**：能产出"本周 vs 上周"的分数对比
- **说明**：不追 PaperBench（需复现 20 篇顶会论文，成本过高）；自建冻结集更现实

### P4 · 技能质量升级（对齐 K-Dense 标准）
- **动作**：对核心科研技能补"精选文档 + 可运行示例 + 域内数据源"，而非纯指令；建立技能质量分级
- **验收**：核心技能里"可直接运行示例覆盖率"达标

### P5 · 边界与安全（对齐 EurekAgent）
- **动作**：预算控制（token/调用次数上限）、权限受限执行、人类监督节点
- **动机**：实测 exec 权限过宽（可写 `.hanako`），需边界

### P6 · 多智能体与自进化验证
- **动作**：按需引入分工 agent；用 P3 基准验证自建技能是否真提升效果

### P7 · 知识资产层
- **动作**：本体 + 图谱 + 产物记忆，填充 `research/40-knowledge`

---

## 四、本轮建议立刻做的三件事

1. **盘点 Zotero MCP 的 53 个工具**（零成本，可能直接补上文献层一大块）
2. **建 OpenAlex + arXiv 免密钥检索脚本**（P0 核心）
3. **建个人评测基准 v0 的任务清单**（P3 的起点，先定义再实现）

## 五、需要你决定

| 项 | 选项 |
|---|---|
| 学术 API | 免密钥（OpenAlex/arXiv/Crossref）可直接上；Semantic Scholar 是否需要你提供 key 提速 |
| Zotero 库 | 是否允许我读写你的 Zotero 文献库 |
| MCP 学术服务器 | 是否允许新增（如 arXiv / OpenAlex MCP） |
| 评测基准 | 是否同意以"自建冻结任务集"替代 PaperBench 这类重型基准 |

---

## 六、诚实边界

1. 本路线基于**文档与综述调研**，我**没有实测**这些系统的性能，也没与之做基准对比【待】。
2. PaperBench 等基准我没跑过，且其成本（复现 20 篇顶会论文）超出当前条件【待】。
3. Zotero MCP 的 53 个工具**我尚未能枚举其名称**，能力边界待盘点后确认【待】。
4. K-Dense 的 166 技能是**他域（生信/化学/临床）偏重**，与你的方向未必对口，参考其**工程范式**而非照搬内容。
