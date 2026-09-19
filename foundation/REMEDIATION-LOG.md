# REMEDIATION-LOG.md

| 项 | 值 |
|---|---|
| 阶段 | Foundation Stage（基础设施整改） |
| 时间 | 2026-09-16 21:54 (+08:00) |
| 执行者 | 科研助手（agent-mu42qzfz） |
| 回滚点 | `foundation\backup\snapshots\20260916-215409`（整改前快照） |
| 密钥声明 | 本记录不含任何密钥/令牌的具体内容 |

## 整改结论总览

| # | 问题 | 结论 | 状态 |
|---|---|---|---|
| 1 | 视觉模型失效 | 用户侧设置项，我无法改 | 待用户处理 |
| 2 | 嵌入模型未配置 | 用户侧设置项，我无法改 | 待用户处理 |
| 3 | 高权限项同时开启 | 执行边界控制，只能用户调整 | 待用户处理 |
| 4 | 备份薄弱 | 已建快照机制；保留期需用户改 | 部分完成 |
| 5 | 遗留定时任务 studio_job_2 | 工具无删除动作 | 待用户处理 |
| 6 | 凭据明文令牌暴露 | 已收紧文件权限 | **已完成** |

---

## 1. 视觉模型失效

**诊断（已实测）**：读取图片返回 `Auxiliary vision failed: fetch failed`。`vision_model = openai-codex/gpt-5.6-luna`，该模型在服务端启动时**已加载**（启动日志「找到 20 个模型」列表中包含它）。因此排除「模型未登记」，指向 **provider 侧调用失败**（网络不可达或授权失效）。

**为什么我没改**：`update_settings` 仅暴露 `memory.enabled`、`memory.facts`、`file_backup`、`models.chat`，不含视觉模型键；属用户侧设置。

**建议操作（二选一）**：
- 首选：把辅助视觉模型改为本地模型 `ollama/gemma4:e4b`（支持图像输入、已拉取、不依赖外网）。
- 备选：排查 `openai-codex` 通道（网络/登录态）。

**状态**：待用户处理。

## 2. 嵌入模型未配置

**诊断**：`models.embedding=""` 且 `embedding_api.provider=""`，但 `embedding_dimensions=1024` 已设。语义/向量记忆很可能不可用（影响面待确认）。

**为什么我没改**：同上，无对应可写设置键。

**建议操作**：把嵌入模型设为 `ollama/bge-m3:latest`（本地已拉取，输出 1024 维，与 `embedding_dimensions` 匹配），provider 设为 `ollama`。

**状态**：待用户处理。

## 3. 高权限项同时开启

**诊断**：`allow_full_access_plugins=true` 且 `plugin_dev_tools.enabled=true`。

**为什么我没改**：插件全权与开发槽属**执行边界/安全控制**，按平台约定只能由用户在设置中调整，Agent 不代为变更。

**建议操作**：若当前无插件开发需求，关闭 `plugin_dev_tools`；`allow_full_access_plugins` 评估后按需关闭。是否需要保留取决于你是否有正在开发的插件。

**状态**：待用户处理（需你决定取舍）。

## 4. 备份薄弱

**已完成（机制）**：
- 新增可复用快照脚本 `foundation\backup\snapshot-configs.ps1`。
- 生成首份快照 `foundation\backup\snapshots\20260916-215409`，含 `config.yaml`、`preferences.json`、`models.json`、`provider-catalog.json`、`server-network.json`、`pinned.md`、`pinned-memory.json`。
- 脚本**显式排除**任何可能含凭据的文件（`server-info.json`、`auth.json`、`device-credentials.json`、`security\*`），并把排除清单写入 `MANIFEST.json`。
- 自动保留最近 30 份快照。

**未完成（需你操作）**：`file_backup` 的保留期（当前 1 天）与单文件上限（当前 1 MB）需在设置中调整；我可切换其开关，但改不了这两个数值。

**状态**：部分完成。

## 5. 遗留定时任务 studio_job_2

**诊断**：`cron 0 9 * * *`，`prompt` 为空，`enabled=false`，归属 `hanako`，创建于 2026-06-09。当前为惰性（已禁用），风险仅在误启用时空跑。

**为什么我没改**：`automation` 工具只提供 list/create/update，**没有删除动作**。

**建议操作（二选一）**：
- 在自动化页面直接删除该任务；
- 或授权我把它改造成「每周只读更新检查」任务（需你明确同意后才会创建/启用）。

**状态**：待用户处理。

## 6. 凭据明文令牌暴露

**诊断**：`server-info.json`（含明文访问令牌）、`auth.json`（OAuth 凭据）、`device-credentials.json`（含哈希）三者的读权限均**继承自 `.hanako`**，允许本地组 `CodexSandboxUsers`（成员 `CodexSandboxOffline`、`CodexSandboxOnline`）读取。

**已执行**：对三个文件禁用继承并移除 `CodexSandboxUsers` 的读权限。执行后核对，三者仅剩 `SYSTEM`、`Administrators`、`ZhouXuan` 可访问。自身读取与服务进程均正常。

**回滚方式**：`icacls "<文件>" /inheritance:e`（恢复正常继承）。

**状态**：**已完成**。

---

## 附：本次新增发现

| 发现 | 说明 | 状态 |
|---|---|---|
| E-01 | `exec_command` 实际可写 `C:\Users\ZhouXuan\.hanako`（探针验证通过），比 `session_folders` 报告的沙箱范围（仅 OH-WorkSpace）更宽 | 待确认（是否为预期） |
| E-02 | PowerShell 5.1 会把**无 BOM 的 UTF-8 中文注释**脚本解析失败，脚本需 ASCII 化或带 BOM | 已确认 |
| E-03 | `.hanako` 根的 `CodexSandboxUsers` 读权限是**显式 ACE**（非继承），影响其下全部文件 | 已确认（本次仅对凭据文件做外科式收紧，未动根目录） |

## 未做的事（遵守约束）

未改动任何用户侧安全/模型设置；未创建或启用任何定时任务；未创建多 Agent；未输出任何凭据内容；未开展科研。
