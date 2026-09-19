# git 追踪与推送（工作区版本控制）

## 1. 现状

| 项 | 值 |
|---|---|
| 仓库 | `C:\Users\ZhouXuan\Desktop\OH-WorkSpace`（`main` 分支） |
| 主远端 origin | `https://github.com/ZhouXuan-Yu/ResearchAssistant.git`（public） |
| 备份远端 local-backup | `C:\Users\ZhouXuan\Desktop\OH-WorkSpace-remote.git`（本地裸仓库，离线冗余） |
| 凭据 | repo 级 `credential.helper = !gh auth git-credential`（复用 `gh` 登录，不落盘明文 token） |
| 提交身份 | repo 级 `user.name/email`，不动全局配置 |

查看方式：GitHub 网页 / `foundation/changelog/auto-changes.md`（每次改动的中文摘要） / `git log`。

## 2. 每次改动怎么做（唯一入口）

```powershell
# 1) 把提交信息写进一个 UTF-8 文件（中文务必走文件，不要内联）
#    例：foundation/tools/_msg.txt
# 2) 执行
powershell -NoProfile -ExecutionPolicy Bypass -File foundation\tools\git_snapshot.ps1 -MessageFile foundation\tools\_msg.txt
```

脚本行为：暂存全部 → 向 `foundation/changelog/auto-changes.md` 追加一条可读记录 → 提交 →
推 `origin` 与 `local-backup`。无改动则不提交；推送失败只报错、不吞掉、不影响本地提交。

## 3. 不入库的东西（`.gitignore`）

- **凭据类**：`cookies` / `env_vars.json` / `auth.json` / `security/` / `*.key` / `*.pem`。历史一旦写入无法真正删除，所以这里只进不退。
- 大体积第三方克隆（`codex-skills/`、`research-skills-setup/`、`zotero-translate-final/`、`langfuse/`）、`node_modules/`。
- 下载与包缓存（`foundation/downloads|packages|external|backup/`）、LaTeX 中间产物、`*.bak*`、临时脚本（`_*.txt`）。

判定原则：**能重建的不入库，含凭据的绝不入库，其余尽量入库。**

## 4. 已踩过的坑（复现时先读这段）

1. **PowerShell 5.1 按 ANSI 解码无 BOM 的 UTF-8 `.ps1`**：脚本内中文变乱码并报语法错。
   → 含非 ASCII 的 `.ps1` 必须带 UTF-8 BOM。工具：`python foundation\tools\fix_ps1_bom.py`。
2. **`Get-Content` 默认按 ANSI 读文件**：中文提交信息被双编码写坏（历史真实事故，commit `d11a077` 是修复后的形态）。
   → 一律 `[IO.File]::ReadAllText($p, [Text.Encoding]::UTF8)`。
3. **`$a..$b` 在 PowerShell 里不可靠**：`$bad..$tip` 曾导致传给 git 的区间左端被吞掉、从根提交开始重放。
   → 显式拼接：`$range = "" + $bad + ".." + $tip`。
4. **`cherry-pick` 残留 sequencer 状态**：失败一次后下次直接报 "already in progress"。
   → 重做前先 `git cherry-pick --quit`；区间必须排除起点提交，否则第一个 pick 就是空提交。
5. **`gc --prune=now` 清不掉旧提交**：`refs/remotes/origin/master` 仍指向旧链，旧对象一直可达。
   → 先 `git update-ref -d refs/remotes/origin/<stale>`，再 `reflog expire --expire=now --all`，最后 `gc --prune=now`。验证：`git cat-file -e <old-sha>` 必须失败。

## 5. 历史重写（已执行一次）

`d11a077`（原 `15b116f`）的提交信息曾被双编码写坏。修复方式：检出该提交 → `git commit --amend -F <utf8 消息文件>` →
`git cherry-pick <bad>..<tip>` 重放其后的 6 个提交 → `git branch -f` → 清理旧对象 → 强推两端。

验收标准：`git diff <old-tip> <new-tip>` **必须为空**（内容字节级一致，只换消息）。本次结果为空，通过。

回滚：重写前旧链可由 reflog / `refs/original` 找回；本次已 gc 清理，旧链不再可达。若需再次重写，务必先打 tag 或备份裸仓库。

## 6. 右侧 Git 面板（插件 `git-save-load`）

- 来源：用户提供的 `git-save-load-v2.3.2.zip`（上游 GitHub `H-i-m-s/git-save-load`，v2.3.2）。
- 安装方式：**走宿主正式接口** `POST /api/plugins/install`，body `{"path":"<zip 绝对路径>"}`，`Authorization: Bearer <server-info.json 的 token>`。
  教训：手工把文件放进 `%USERPROFILE%\.hanako\plugins\` **不会**被 `plugin-installs.json` 注册，宿主只在启动时扫描目录——必须用这个接口。
- 落位：`%USERPROFILE%\.hanako\plugins\git-save-load`；注册项 `source: "local"`（平台自身取值），`installedVersion: 2.3.2`。
- 数据目录：`%USERPROFILE%\.hanako\plugin-data\git-save-load`。
- 已预置配置：`repoPath = C:\Users\ZhouXuan\Desktop\OH-WorkSpace`（通过 `PUT /api/plugins/git-save-load/config`，body `{scope:"global",values:{...}}`）。
- 表面：`contributes.widget` 已注册（右侧挂件 “Git”，`/api/plugins/git-save-load/widget`）；
  `contributes.cards`（整页 `/git`）在当前宿主版本诊断中 `routes.pages` 为空，**未注册**。
- Agent 工具：`git-save-load_git_status` / `_git_commit` / `_git_log` / `_git_reset`。
- 卸载：`DELETE /api/plugins/git-save-load?token=...`（或界面删除）；重新安装需保留 workspace 里的 zip，因为它被记为 `sourcePath`。
- ⚠️ 上游仓库**没有 LICENSE 文件**：本地自用可以，二次分发授权状态不明。
- ⚠️ `trust: full-access`，且带 Agent 工具，会以当前用户权限执行 git 命令。

