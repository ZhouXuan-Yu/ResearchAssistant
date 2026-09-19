# 变更自动记录（每次 agent 改动写入）

> 由 foundation/tools/git_snapshot.ps1 自动追加；新条目在文件末尾。

## 2026-09-19 18:24:33

**说明**：feat: 每次改动自动提交 + 生成可读变更记录 + 推送到远端

- git_snapshot.ps1 重写：暂存 → 写入 foundation/changelog/auto-changes.md 条目 → 提交 → 推送 origin
- 推送失败不吞错、不阻塞提交（本地提交安全，失败会明确报出）
- 新增本地裸仓库作为远端：C:\Users\ZhouXuan\Desktop\OH-WorkSpace-remote.git（零凭据；可随时换成 GitHub/Gitee）

**变更规模**：3 files changed, 70 insertions(+), 28 deletions(-)

**文件清单**：
- `.gitignore`
- `foundation/tools/_msg.txt`
- `foundation/tools/git_snapshot.ps1`

## 2026-09-19 18:24:44

**说明**：snapshot: 2026-09-19 18:24:44

**变更规模**：1 file changed, 5 deletions(-)

**文件清单**：
- `foundation/tools/_msg.txt`

## 2026-09-19 18:25:09

**说明**：chore: 变更记录加"不含本记录文件"说明；新增 fix_ps1_bom.py

- auto-changes 条目的文件清单注明不含本记录文件自身，避免与 git show --stat 数目看起来矛盾
- fix_ps1_bom.py：批量确保含中文的 .ps1 带 UTF-8 BOM（PS 5.1 无 BOM 会按 ANSI 解码）
- 实测：现有 16 个 .ps1 中 1 个需要 BOM（已有）、15 个为纯 ASCII 无需处理

**变更规模**：2 files changed, 42 insertions(+), 1 deletion(-)

**文件清单**（不含本记录文件自身）：
- `foundation/tools/fix_ps1_bom.py`
- `foundation/tools/git_snapshot.ps1`

## 2026-09-19 18:34:47

**说明**：snapshot: 2026-09-19 18:34:47

**变更规模**：2 files changed, 34 insertions(+)

**文件清单**（不含本记录文件自身）：
- `foundation/tools/_fixmsg.py`
- `foundation/tools/_goodmsg.txt`

## 2026-09-19 18:37:37

**说明**：chore: 接入 GitHub 远端并固化 git 工作流

- origin 切到 https://github.com/ZhouXuan-Yu/ResearchAssistant.git（public，分支 main）
- 保留本地裸仓库为备份远端 local-backup（离线冗余）
- 凭据走 repo 级 credential.helper = !gh auth git-credential，不落盘明文 token
- 提交身份改为 repo 级配置，不动全局
- git_snapshot.ps1 改为双远端推送（origin + local-backup），失败不吞错
- 新增 foundation/docs/git-tracking.md：现状、流程、排除规则、已踩的 5 个坑、历史重写记录
- 清理一次性脚本（_do_rewrite*/_cleanup/_github_setup/_finish_remote/_fixmsg/_goodmsg）

**变更规模**：4 files changed, 69 insertions(+), 43 deletions(-)

**文件清单**（不含本记录文件自身）：
- `foundation/docs/git-tracking.md`
- `foundation/tools/_fixmsg.py`
- `foundation/tools/_goodmsg.txt`
- `foundation/tools/git_snapshot.ps1`

## 2026-09-19 18:47:53

**说明**：chore: 右侧 Git 面板插件 git-save-load v2.3.2 落位并记录用法

**变更规模**：3 files changed, 20 insertions(+), 1 deletion(-)

**文件清单**（不含本记录文件自身）：
- `.gitignore`
- `"OH-Works/\347\232\207\345\256\266\345\215\253\345\243\253GGOB\347\232\204\345\267\241\346\243\200/patrol-log.md"`
- `foundation/docs/git-tracking.md`

## 2026-09-19 19:10:19

**说明**：docs: 记录 HyperFrames 空白页修复（cmd 引号缺陷绕过）与插件面板/安装入口排查结论

**变更规模**：1 file changed, 130 insertions(+)

**文件清单**（不含本记录文件自身）：
- `foundation/docs/plugin-fixes.md`

## 2026-09-19 19:15:11

**说明**：docs(plugins): pin down why the git-save-load widget does not show

- evidence: /api/plugins/widgets registers "Git"; /api/preferences/plugin-ui
  hiddenWidgets empty; allow_full_access_plugins=true; disabled_plugins empty;
  GET /api/plugins/git-save-load/widget -> 200 (61505 bytes)
- host _activatePluginEntry returns early when the plugin has no lifecycle entry
  (no index.js at plugin root) => activationState "none" is by design, not a switch
- widget entry renders in ChatPage titlebar right group (tb-right-group), gated by
  currentTab === "chat" && pluginWidgets.length > 0
- fix applied: idempotent PUT /api/plugins/git-save-load/enabled {enabled:true}
  -> enablePlugin emits plugin_ui_changed -> renderer refreshPluginUI()
- cleanup: removed temporary probe scripts from foundation/tools

**变更规模**：1 file changed, 62 insertions(+), 9 deletions(-)

**文件清单**（不含本记录文件自身）：
- `foundation/docs/plugin-fixes.md`
