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
