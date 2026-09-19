# 技能缺口扫描报告  2026-09-18 17:50:19 +0800

- 扫描会话文件：9 个（近 7 天）
- 采集用户消息：45 条
- 已装启用技能：144 个

## 1. 意图分布（用户消息命中次数）

| 意图 | 命中 | 粗判覆盖 |
|---|---|---|
| 环境运维 | 23 | 弱/无 |
| 智能体工程 | 9 | 弱/无 |
| 科研绘图 | 5 | 较强: scipilot-figure-skill, nature-figure |
| 引用核验 | 5 | 较强: nature-ref-verifier, nature-citation |
| 论文写作 | 4 | 较强: nature-writing, nature-polishing, researchwrite |
| 文献检索 | 4 | 较强: nature-academic-search, nature-literature-pipeline, deep-research |
| 实验管理 | 3 | 部分: nature-experiment-log |
| 知识组织 | 1 | 部分: understand-knowledge |

## 2. 工具调用频次

| 工具 | 次数 |
|---|---|
| exec_command | 224 |
| write | 36 |
| update_settings | 29 |
| read | 29 |
| install_skill | 26 |
| edit | 24 |
| web_search | 14 |
| stage_files | 12 |
| web_fetch | 9 |
| automation | 9 |
| grep | 9 |
| todo_write | 8 |
| write_stdin | 8 |
| record_experience | 7 |
| ls | 4 |
| mcp_connectors_status | 4 |
| search_memory | 2 |
| current_status | 2 |
| session_folders | 1 |

## 3. 已装技能被提及次数（近似的使用信号）

| 技能 | 提及 |
|---|---|
| pdf | 17 |
| research-os-router | 13 |
| academic-research-suite | 7 |
| nature-figure | 7 |
| hana-agent-ops | 5 |
| nature-writing | 4 |
| nature-paper2ppt | 4 |
| nature-reader | 4 |
| deep-research | 4 |
| nature-paper-card | 4 |
| nature-reviewer | 4 |
| nature-polishing | 4 |
| academic-paper-reviewer | 4 |
| nature-data | 3 |
| nature-response | 3 |
| nature-statistics | 3 |
| nature-academic-search | 3 |
| nature-ref-verifier | 3 |
| nature-citation | 3 |
| scipilot-figure-skill | 3 |
| paper-deep-reading | 2 |
| navi-deep-research | 2 |
| nature-shared | 2 |
| researchwrite | 2 |
| zotero-pdf-translate | 2 |

## 4. 候选缺口（高命中意图中未被现成技能明确覆盖者）

- **环境运维**：命中 23 次，覆盖偏弱 → 值得评估是否需要自建技能
- **智能体工程**：命中 9 次，覆盖偏弱 → 值得评估是否需要自建技能

> 说明：本报告是**证据**，不是结论。技能是否该自建，由 Agent 结合具体会话内容判断，并经用户批准。