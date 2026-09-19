# ENVIRONMENT_AUDIT.md

| 项 | 值 |
|---|---|
| 审计阶段 | Foundation Stage / F0 环境审计 |
| 审计时间 | 2026-09-16 21:49 (+08:00) |
| 审计者 | 科研助手（agent-mu42qzfz） |
| 审计方式 | 只读（文件读取 + 只读命令），未做任何写操作 |
| 证据范围 | `C:\Users\ZhouXuan\.hanako\` 配置与目录、运行环境命令输出 |

## 0. 约束遵守声明

本次审计遵守全部强制约束：未安装/更新/删除/覆盖任何 Skill；未修改任何配置或既有文件（仅新建本报告）；未创建多 Agent；未启动定时任务；未输出任何密码/令牌/密钥内容；未做秦简文献检索；未创建科研项目；未训练模型；未撰写论文。

## 状态标记定义

- **平台支持**：能力存在，与是否启用无关。
- **已经配置**：当前已生效或被显式开启。
- **尚未配置**：能力存在但未启用/未设置。
- **无法确认（待确认）**：证据不足或存在歧义，不做推测。

---

## 1. HanaAgent 版本与现有功能

| 项目 | 事实 | 状态 |
|---|---|---|
| 服务端运行时版本 | `0.412.7`（`artifacts/server/0.412.7-win32-x64`，`server-info.json.version`） | 已经配置 |
| 桌面客户端版本 | `0.407.15`（`last-update-version`） | 已经配置 |
| 版本一致性 | 服务端 0.412.7 与桌面端 0.407.15 **不一致** | 待确认（是否预期） |
| 更新通道 | `stable` | 已经配置 |
| 平台形态 | 本地进程；`nodeKind=local`、`transport=loopback`、`execution=local_process` | 已经配置 |
| 会话 / 多 Agent / 技能 / 记忆 / 定时任务 / 浏览器 / 计算机控制 / 插件 / 桥接 | 平台均提供对应工具入口 | 平台支持 |
| 桥接（Bridge） | 全局 `channels_enabled=true`，Agent 级 `channels.enabled=false` | 见 §10 冲突 |

## 2. 操作系统与运行时环境

| 项目 | 事实 | 状态 |
|---|---|---|
| 操作系统 | Windows 11 家庭版 中文版，`10.0.26200`，64 位 | 已经配置 |
| PowerShell | `5.1.26100.9444` | 已经配置 |
| Python | `3.14.0`（`python` 与 `py` 均可用） | 已经配置 |
| Node.js | `v24.12.0` | 已经配置 |
| npm / npx | `11.6.2` | 已经配置 |
| Git | `2.55.0.windows.1` | 已经配置 |
| Ollama | `0.34.0` | 已经配置 |
| Python 3.14 兼容性 | 3.14 为较新版本，部分科研/ML 依赖可能缺少预编译 wheel | 待确认 |

## 3. 当前模型提供方与本地模型能力

**云端（`models.json` / `provider-catalog.json` 登记）**：deepseek（`deepseek-v4-pro`、`deepseek-v4-flash`、`deepseek-flash`）、openai-codex（`gpt-5.6-sol`、`gpt-5.6-terra`、`gpt-5.6-luna`、`gpt-5.5`、`gpt-5.4`、`gpt-5.2`）、xai（`grok-4.5` 系列）、sensenova（`sensenova-6.7-flash-lite`、`sensenova-u1-fast`）。

**本地（Ollama 已拉取）**：`qwen3.5:4b`（3.4 GB）、`gemma4:e4b`（9.6 GB）、`gemma3:1b-it-qat`（1.0 GB）、`bge-m3:latest`（1.2 GB，嵌入模型）。

**当前绑定**：

| 角色 | 值 | 状态 |
|---|---|---|
| 本 Agent 聊天模型 | `deepseek / deepseek-v4-flash` | 已经配置 |
| 全局 `utility_model` | `deepseek / deepseek-v4-flash` | 已经配置 |
| 全局 `utility_large_model` | `openai-codex / gpt-5.6-sol` | 已经配置 |
| 全局 `vision_model` | `openai-codex / gpt-5.6-luna` | 已经配置 |
| 检索 provider | `search.provider=auto`，各 `api_keys` 为空 | 已经配置 |
| 本地视觉模型 | `provider-catalog` 登记 `qwen3-vl:8b`（含图像输入），但 `ollama list` 未见该模型 | 待确认 |

## 4. 记忆功能与存储位置

| 项目 | 事实 | 状态 |
|---|---|---|
| 记忆系统 | `memory.enabled=true` | 已经配置 |
| 记忆参数 | `token_budget=2500`、`decay_per_day=0.02`、`hit_bonus=5`、`base_importance=10`、`compile_threshold=4.5`、`forget_speed=1` | 已经配置 |
| 经验库 | `experience.enabled=true` | 已经配置 |
| 存储位置（编译记忆） | `C:\Users\ZhouXuan\.hanako\agents\agent-mu42qzfz\memory\` | 已经配置 |
| ↳ 事实库 | `facts.db`（SQLite，约 36 KB） | 已经配置 |
| ↳ 编译产物 | `memory.md`（123 B，四段均为「暂无」）、`week.md`（0 B）、`daily-state.json` | 已经配置 |
| 存储位置（置顶记忆） | `pinned.md`（3172 B）、`pinned-memory.json`（4006 B） | 已经配置 |
| 嵌入模型 | `models.embedding=""` 且 `embedding_api.provider=""`，但 `embedding_dimensions=1024` 已设 | 尚未配置 |
| 记忆模型解析 | Agent 级 `utility_large=""`，全局 `utility_large_model=gpt-5.6-sol`；据运行时代码规则为 `utility_large || chat` | 待确认（实际生效值） |

## 5. Skills 目录、已安装与候选

| 项目 | 事实 | 状态 |
|---|---|---|
| 技能根目录 | `C:\Users\ZhouXuan\.hanako\skills` | 已经配置 |
| 磁盘技能数 | 284 个不同 `SKILL.md` 名称（166 个一级目录，含 `pm-skills/` 等嵌套包） | 已经配置 |
| 已启用 | `config.yaml skills.enabled` 共 141 条，逐条比对均能在磁盘命中（无失效条目） | 已经配置 |
| 插件技能 | `plugins/hanako-hyperframes/skills`（animejs、lottie、tailwind 等） | 已经配置 |
| 本阶段新增（前序） | nature-skills 全套 20 项 + ARS 自包含 2 项 | 已经配置 |
| 候选（计划内未装） | `scientific-brainstorming`、`experiment-agent`、`experimental-design`、`statistical-power`、`venue-templates` | 尚未配置 |
| 候选（待自建） | `research-os-router` | 尚未配置 |
| 候选（上游存在但依赖未满足） | `academic-pipeline`、`academic-paper`（ARS，依赖插件 `shared/`） | 尚未配置 |
| 本阶段约束 | F0–F8 期间不安装任何技能 | — |

## 6. 工作目录与文件权限

| 项目 | 事实 | 状态 |
|---|---|---|
| 当前工作目录 | `C:\Users\ZhouXuan\Desktop\OH-WorkSpace` | 已经配置 |
| 有效沙箱根 | 仅 `OH-WorkSpace`（`sandboxFolders`） | 已经配置 |
| 额外工作区/授权文件夹 | 无（`workspaceFolders`、`authorizedFolders` 均为空） | 已经配置 |
| ACL（工作区） | `ZhouXuan` FullControl；`SYSTEM`/`Administrators` FullControl；`CodexSandboxUsers` ReadAndExecute | 已经配置 |
| ACL（`.hanako`） | 同上 | 已经配置 |
| 备注 | 沙箱账户对工作区与 `.hanako` 仅只读+执行，无写权限 | 已经配置 |

## 7. 沙箱、命令执行与网络访问边界

| 项目 | 事实 | 状态 |
|---|---|---|
| 本次会话沙箱模式 | `read-all` / `write-scoped` / `network-on`（由运行环境给出） | 已经配置 |
| `preferences.sandbox` | 值为 `false` | 待确认（与上述模式的关系） |
| 命令执行 | 平台支持（本次审计已使用 `exec_command`） | 平台支持 |
| 网络访问 | 平台支持；实测外网可达（`git clone`、`web_search` 成功） | 平台支持 |
| 服务端监听 | `server-network.json`：`mode=lan`、`listenHost=0.0.0.0`、`port=14500` | 已经配置 |
| GitHub 抓取 | `learn_skills.allow_github_fetch=true` | 已经配置 |

## 8. 定时任务能力

| 项目 | 事实 | 状态 |
|---|---|---|
| 定时任务 | 平台支持（cron / every / at） | 平台支持 |
| 现有任务 | 1 个：`studio_job_2`，`cron 0 9 * * *`，label「新的自动化」，`prompt` 为空，`enabled=false`，归属 `hanako`，创建于 2026-06-09 | 已经配置（但未启用） |
| 周更检查任务（前序建议） | 未出现在已确认任务列表中 | 尚未配置 |
| 本阶段动作 | 不启动、不创建任何定时任务 | — |

## 9. 日志、备份与回滚能力

| 项目 | 事实 | 状态 |
|---|---|---|
| 日志目录 | `C:\Users\ZhouXuan\.hanako\logs`（5 个文件，含 `security-audit.jsonl`） | 已经配置 |
| 日志轮转/保留策略 | 配置中未见明确策略 | 待确认 |
| 文件备份 | `file_backup.enabled=true`，`retention_days=1`，`max_file_size_kb=1024` | 已经配置 |
| 快照点 | `checkpoints/`（仅 `session-manifest`，2026-06-26） | 已经配置 |
| 迁移备份 | `migration-backups/`（`provider-catalog` 两份，2026-06-26） | 已经配置 |
| 技能配置快照 | `OH-WorkSpace\skills-enabled-snapshot-20260916.txt`（前序产出） | 已经配置 |
| 整体配置/技能回滚机制 | 无统一快照与一键回滚 | 尚未配置 |

## 10. 当前配置之间可能存在的冲突

| # | 冲突描述 | 证据 | 状态 |
|---|---|---|---|
| C-01 | 桥接开关不一致：全局 `channels_enabled=true`，Agent 级 `channels.enabled=false` | `preferences.json` vs `config.yaml` | 待确认 |
| C-02 | 记忆模型来源不一致：Agent 级 `utility_large=""`，全局 `utility_large_model=gpt-5.6-sol` | `config.yaml` vs `preferences.json` | 待确认 |
| C-03 | 嵌入维度已设（1024）但嵌入模型与 provider 均为空 | `config.yaml` | 待确认 |
| C-04 | 视觉模型已配置（`gpt-5.6-luna`）但历史上出现 `fetch failed`（见日志） | `preferences.json` + `logs` | 待确认 |
| C-05 | 版本号不一致：桌面端 0.407.15 vs 服务端 0.412.7 | `last-update-version` vs `server-info.json` | 待确认 |
| C-06 | 沙箱开关：`preferences.sandbox=false` 与「write-scoped」运行模式并存 | `preferences.json` + 运行环境 | 待确认 |
| C-07 | 高权限项同时开启：`allow_full_access_plugins=true`、`plugin_dev_tools.enabled=true` | `preferences.json` | 已经配置（风险见 RISK_REGISTER） |
| C-08 | 本地视觉模型登记（`qwen3-vl:8b`）与 Ollama 实际已拉取列表不符 | `provider-catalog.json` vs `ollama list` | 待确认 |

## 11. 候选 Skills 之间的功能重叠

| 重叠组 | 成员 | 区分建议 |
|---|---|---|
| 文献检索/获取 | `nature-academic-search`、`nature-citation`、`nature-ref-verifier`、`nature-downloader`、`nature-literature-pipeline`、`deep-research`、`navi-deep-research` | 按「检索 / 论断支撑 / 元数据核验 / 全文获取 / 系统综述 / 深度研究」分工 |
| 论文精读 | `nature-reader`、`nature-paper-card`、`paper-deep-reading` | 呈现 vs 结构化解析 vs 通用深读 |
| 学术写作 | `nature-writing`、`nature-polishing`、`researchwrite`、`academic-paper`(候选)、`grammar-check`、`humanizer` | 结构论证 / 语言润色 / 计划书 / 管线 / 校对 / 去 AI 味 |
| 审稿 | `nature-reviewer`、`academic-paper-reviewer` | 独立二次审查 vs 预投稿主流程 |
| 演示材料 | `nature-paper2ppt`、`nature-image2ppt`、`ppt-master`、`pptx`、`pptx-generator` | 论文转 PPT / 图像重建 / 通用 PPT |
| 统计与图 | `nature-statistics`、`nature-figure` | 统计审查 vs 投稿级绘图 |
| 知识/记忆 | `navi-memory`、`understand-knowledge`、`understand-*` 系列 | 记忆读写 vs 知识图谱分析 |
| 编排 | `academic-research-suite`（现为空壳）、`academic-pipeline`(候选) | 空壳需替换或停用 |

## 12. 凭据是否安全存储（不输出任何值）

| 项目 | 事实 | 状态 |
|---|---|---|
| `models.json` 的 `apiKey` | 采用引用式 `hana-runtime-api-key:<provider>`（非明文）；Ollama 使用占位 `local` | 已经配置 |
| `device-credentials.json` | 含 `secretHash`、`secretSalt`、`secretPrefix` 字段 | 已经配置（哈希存储） |
| `security/` | `execution-leases.json`、`grants.json`、`plugin-*-key`（各 44 B） | 已经配置 |
| `auth.json` | 含 `openai-codex`、`xai-oauth` 条目（OAuth 形态） | 待确认（具体存储形态） |
| `server-info.json` | 含一个明文访问令牌字段（loopback 用途） | 已经配置（风险 R-11） |
| 本报告 | 未包含任何密钥/令牌的具体内容 | — |

## 13. 无法确认清单（统一登记）

1. 桌面端与服务端版本不一致是否为预期（C-05）。
2. 记忆模型的实际生效来源（C-02）。
3. 视觉模型失败的根因是否为 provider 侧（C-04）。
4. 语义/向量记忆是否因嵌入未配置而不可用（C-03）。
5. 沙箱开关与运行模式的确切语义关系（C-06）。
6. `qwen3-vl:8b` 是否可用（C-08）。
7. 日志轮转与保留策略。
8. `auth.json` 中 OAuth 凭据的具体存储形态。
9. 平台层是否提供配置/技能的整体快照与一键回滚。

以上各项一律标记「待确认」，本次不做推测；后续阶段（F1/F7）逐项验证。
