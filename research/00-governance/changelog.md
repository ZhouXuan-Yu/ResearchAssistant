# 科研工作区变更日志

> 追加式，不删旧行。规则见 `70-templates/changelog.md`。

| 日期 | 类型 | 对象 | 说明 | 影响 | 回滚方式 |
|---|---|---|---|---|---|
| 2026-09-18 | 配置 | research/ 骨架 | 建立方向无关科研工作区（8 层目录 + 5 类模板 + F/L/I/U 证据约定） | 后续研究资产全部落此 | 删除 `research/` 目录 |
| 2026-09-18 | 决策 | ADR-0001 | 采纳"按证据产生顺序分层"方案 | 目录结构定稿 | 见 ADR-0001 回滚节 |
| 2026-09-18 | 实验 | E2E-001 | 端到端验收演练（公开材料 arXiv:1706.03762） | 验证闭环可跑通、可回滚 | 删除 `50-experiments/log/E2E-001-*.md` 与 R-001 条目 |
| 2026-09-18 | 数据 | R-001 | 登记验收演练用参考条目（非研究引用） | 仅为验证引用登记流程 | 删除 `references.md` 中 R-001 |
| 2026-09-18 | 配置 | MCP academic-search | 注册连接器（技能自带 MCP）；修 `arxiv.py` 的 defusedxml 兼容 bug；启动后 16 工具可用 | 检索层从"仅网页搜索"变为 CrossRef/PubMed/arXiv 有源检索 | 删除连接器配置项；`arxiv.py` 删除补丁行 |
| 2026-09-18 | 配置 | MCP 按-Agent 授权 | 为 agent-mu42qzfz 开启 zotero(53)+academic-search(16) 共 69 工具 | 工具变为可调用（**真因是调用名需带 `mcp_<connector>_` 前缀**） | 取消授权 |
| 2026-09-18 | 文档 | `foundation/routing/MCP-CAPABILITIES.md` | 新建 MCP 能力登记（与技能分类体系独立） | 路由可引用真实工具路径 | 删除文件 |
| 2026-09-18 | 配置 | `routing-rules.yaml` | B/D 两组挂 MCP，新增 `mcp_capabilities` 段 | 检索/核验路由反映真实能力 | 回退该文件 |
| 2026-09-18 | 基准 | AGENT-BENCH-v0 | 新建智能体能力评测基准（10 题 + 2 硬门禁）；跑 R1 | R1 = 8/10（T-07/T-10 未执行）；自评不独立 | 删除 `foundation/benchmark/` |
| 2026-09-18 | 诊断 | scite 可达性 | 首轮 scite 两工具超时；确认根因是境外网络不可达（非工具故障），代理启用后通过 | scite 类核验需代理 | 无（诊断记录） |
| 2026-09-18 | 技能 | paper-spine (PaperSpine5 v0.4.0-alpha.1) | 引入论文全流程编排技能；MIT；官方 Release SHA-256 校验一致；52 脚本在 Py3.14 冒烟通过；归 L_orchestration/secondary 并加意图路由 | 新增跨阶段编排、科研绘图流程与目视就绪门 | 删除 `skills\paper-spine` 并还原 taxonomy/routing 两处；详见 INTEGRATION-paper-spine.md |
| 2026-09-18 | 配置 | Zotero 分类「入门」 | 建顶层分类 `CRFTWXNP`，按 DOI 入库 6 条含 npj Heritage Science 对标项 | 库从 1 条扩至 7 条，具备对标文献 | 删除该分类 |
| 2026-09-18 | 配置 | Better Notes v3.3.3 | 安装并启用；证实 Zotero 10 对侧载插件有硬性门禁，需界面确认一次 | Zotero 具备学术笔记工作流 | 删除 `<profile>\extensions\Knowledge4Zotero@windingwind.com` |
| 2026-09-18 | 调研 | 导师组与方向 | 建立 supervisor-survey：导师主页/校新闻网/CrossRef 一手证据；含金量口径 + 分方向难度对比 | 为首篇论文选题提供证据基础 | 删除 `research/00-governance/supervisor-survey-2026-09-18.md` |
| 2026-09-18 | 配置 | PUBMED_EMAIL | 写入邮箱（仅邮箱，**不含任何密码**） | PubMed 源恢复（重启 Hana 后生效） | 置空该字段 |
| 2026-09-18 | 技能 | paper-spine 平台适配 | 在 SKILL.md 顶部加 HanaAgent 运行约定，取代“首步必须启动 Web 界面”硬规则；方法学正文不动 | 技能在本平台可实际运行，不再因缺启动器而中止 | 从 `foundation/packages/paper-spine/SKILL.md` 恢复 |
| 2026-09-18 | 决策 | ARCHITECTURE-SPINE | 定“单一脊柱 + 外接模块”三层架构：L0 决策守门 / L1 paper-spine 主框架 / L2 外接执行 | 体系从 145 技能扁平路由转为脊柱化，编排单一化 | 删除该文件并还原 routing/taxonomy 两处 |
| 2026-09-18 | 技能 | paper-spine 升格 | taxonomy 由 L_orchestration/secondary 升为 primary；routing 新增 `spine` 字段 | 确立主框架地位，但仍非默认入口 | 改回 secondary |
