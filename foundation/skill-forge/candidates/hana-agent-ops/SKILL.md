---
name: hana-agent-ops
description: >-
  HanaAgent 运行环境的自检、故障诊断与配置治理。Use when 环境自检、健康检查、
  记忆不工作、模型不通、技能装不上、配置漂移、备份/回滚、凭据权限、疑似静默失效，
  or when the user reports 智能体"变笨/不响应/记不住/看不到图"。覆盖：健康自检、
  模型链路诊断、记忆故障定位、技能治理与冒烟测试、配置快照与回滚、凭据权限核查。
  不用于：正式科研任务本身、外部技能的功能使用（那是各技能自己的事）。
default-enabled: false
---

# Hana Agent Ops — 环境诊断与治理

> 出处：自建（Skill Forge 首个候选）。源于真实运维证据：环境运维类意图 20 次命中、
> `exec_command` 200 次调用、且此前无任何现成技能覆盖该类工作。
> 建立动机：本环境的视觉链路曾**静默失效两天**无人察觉，说明"能自检"是刚需。

## 何时用

- 用户说：环境/健康/自检/备份/回滚/配置/技能没生效/记忆不工作/模型不通/看不到图。
- Agent 自己发现：某能力疑似静默失效、配置与磁盘不一致、快照过旧。

## 前置脚本（本技能自带）

| 脚本 | 作用 |
|---|---|
| `scripts/health_check.py` | 一键环境自检（技能/依赖/模型/记忆/备份/凭据形态），输出报告 |
| `scripts/scan_skill_gaps.py` | 挖掘会话，产出技能缺口报告 |
| `scripts/snapshot-configs.ps1` | 配置快照（显式排除含凭据文件） |

> 安装到技能池时，这三个脚本从 `OH-WorkSpace\foundation\` 复制进 `scripts/`。

## 诊断剧本

### A. 例行自检（先做这个）
```
python scripts/health_check.py --json last-report.json
```
读报告：`FAIL` 优先处理，`WARN` 记录。报告含六段：Skills / Deps / Models / Memory / Backup / Providers。

### B. 模型不通（"看不到图/回复异常"）
1. 查用量账本 `~/.hanako/usage-ledger.json`，定位失败请求的 `model.provider/modelId` 与 `error.message`。
2. 若错误是账号侧（`usage limit` / 鉴权）→ 换 provider 或提示用户处理额度，**不要**在配置里打转。
3. 若报 `must support image input` → 查能力表 `artifacts/server/<ver>/lib/known-models.json` 该模型 `image` 标记；`false` 则平台不会把图路由过去。
4. 改完模型/能力配置**必须重启**才生效（配置在启动时加载；直接改文件不触发重载）。

### C. 记忆故障（"记不住/记忆报错"）
1. 看 `memory.md` 与 `daily-state.json` 的新鲜度。
2. 搜日志 `[memory-ticker]` / `[memory]` 的 `ERROR`，定位是"模型失败"还是"格式失败"。
3. 记忆模型解析规则 = `models.utility_large || models.chat`；Agent 配置留空则跟随全局 `utility_large_model`。
4. 健康状态残留在内存里，只有该步骤成功跑一次才清；`memory.enabled` 开关切换**不会**触发重跑。

### D. 技能治理与冒烟测试
1. 安装前侦察：来源仓库、许可证、`scripts/` 是否含网络/subprocess、依赖清单。
2. `install_skill` 后**逐个冒烟**：跑一次最小用例，确认可加载、脚本可执行。
3. 登记进 `SKILLS-GOVERNANCE.md`（来源/固定提交/许可证/依赖/回滚）。
4. 有重叠必须显式路由，避免触发竞争。

### E. 备份与回滚
```
powershell -File scripts/snapshot-configs.ps1
```
快照**显式排除**任何含凭据文件；回滚按快照目录逐文件复原；技能级回滚 = 删目录 + 从 `skills.enabled` 移除。

### F. 凭据与权限
- 检查凭据文件 ACL：`Get-Acl`，确认本地沙箱组无读取权。
- 绝不在输出中打印任何密钥/令牌值。

## 铁律

1. 诊断**只读优先**；改动前先建快照。
2. 模型/能力类配置改动后**必须重启验证**，不得声称"改完即生效"。
3. 未验证不得标记完成；未跑通不得报告"已修复"。
4. 任何密钥、令牌、密码一律不出现在报告里。
5. 无法核验的项一律标注"待确认"，不推测。

## 常见误判（避坑）

- **改配置文件后能力没变** → 以为是配置错，其实是运行进程未重载 → 先重启再判断。
- **规则文件被服务端重写** → `models.json` 会在启动时重新生成，手改会被覆盖；真正的源在 `known-models.json` 等能力表。
- **看到"模型不支持图像"就换模型** → 先确认是**能力表**没声明，而非模型真不支持。
