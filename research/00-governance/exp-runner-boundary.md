# `exp-runner`（S3 实验与复现）执行边界清单 · 待确认

| 项 | 值 |
|---|---|
| 状态 | **待用户确认**（本文档不执行任何代码） |
| 日期 | 2026-09-19 |
| 上游 | `foundation/RESEARCH-OS-EXPANSION-PLAN.md` §5 缺口② |
| 契约 | 阶段契约 v1.0（`research/00-governance/contracts.md`），S3 特则 |
| 自主度 | **人主导**（契约不允许更高：AI 在研究级实验上不可靠，见 arXiv:2605.18661） |

---

## 0. 本机隔离手段实测（2026-09-19）

| 手段 | 实测结果 | 可用性判断 |
|---|---|---|
| conda | `D:\Anaconda\Scripts\conda.exe` 可用；已建 `spine-tools` / `spine-tex` 两个独立环境 | **可用**，且已验证可整删 |
| Docker | CLI 在 `C:\Program Files\Docker\...`；但 `com.docker.service` **Stopped**、WSL 发行版 `docker-desktop` **Stopped** | 需**你启动 Docker Desktop** 才可用；首次拉镜像还受网络限制 |
| WSL | `wsl.exe` 存在，仅 `docker-desktop` 一个发行版且已停止 | 同上 |
| Python | `C:\Python314\python.exe` + 用户级 pip | 可用 |
| git | 可用（mingw64） | 可用，但见下 |
| **工作区 git 状态** | **`OH-WorkSpace` 不是 git 仓库**（`fatal: not a git repository`） | **关键约束**：代码版本不能用提交号 |

> 上表最后一行直接改变了"可复现三元组"的实现方式（见决策项 C）。

---

## 决策项 A：沙箱形态

| 方案 | 内容 | 优点 | 缺点 |
|---|---|---|---|
| **A3（推荐）** | conda 专用环境（如 `exp-<runid>`）+ 实验写入**仅限工作区内 run 目录** + 网络默认关闭 + 不读凭据 | 本机已验证可行、可整删、零系统改动 | 隔离强度弱于容器（仍与宿主共享文件系统） |
| A2 | Docker 容器（挂载 run 目录） | 隔离最强、环境可复现性最好 | 需你启动 Docker Desktop；首次拉镜像可能被网络卡住 |
| A1 | 当前环境直跑 | 零准备 | 污染宿主环境、无隔离，**不推荐** |

**推荐 A3**，并把 A2 列为 P1b 之后的升级项（等 Docker 可用且你确认后再评估）。

A3 的三条硬约束：
1. **写白名单**：只允许写 `research/50-experiments/<runid>/`；其他路径只读。
2. **网络默认关**：实验默认不得联网；确需联网（如拉取公开数据集）须**单次显式申请**并记入日志。
3. **凭据隔离**：禁止读取 `auth.json`、`device-credentials.json`、`security/*` 等；由巡检脚本定期核查。

---

## 决策项 B：允许的命令范围

### B1 白名单（默认允许，逐条登记）

| 类别 | 允许 | 备注 |
|---|---|---|
| 运行 | `python <run 目录内脚本>` | 脚本必须落在 run 目录内 |
| 依赖 | `pip install <已审清单内包>` | **清单外新增需你逐次批准**；安装后记录 `pip freeze` |
| 文件 | 列目录 / 读取 / 写入**限 run 目录** | 写入工作区外一律拒绝 |
| 版本 | `git status/diff/log/rev-parse`（只读） | 不得 `commit/push/reset` |
| 计算 | 限定单次前台 ≤ 30s；超出改后台 + 短轮询 | 与既有命令通道约束一致 |

### B2 黑名单（硬拦，不做例外）

- 系统级安装与配置：`choco` / `winget` / `msiexec` / `reg` / `sc` / `net`
- 凭据与密钥：读取或复制任何凭据文件
- 破坏性操作：删除 run 目录以外的文件、覆盖既有产物、清空目录
- 任意外网下载：`curl/wget/Invoke-WebRequest` 指向未登记域名
- 提权：任何需要管理员权限的命令

### B3 运行日志（每次实验必须留下）

每条命令一行：

```json
{"t":"2026-09-19T18:05:12+08:00","cwd":"...\\50-experiments\\r001","cmd":"python train.py --seed 17",
 "exit":0,"stdout_sha256":"...","stderr_sha256":"...","artifacts":["metrics.json#sha256:..."]}
```

日志本身即"实验做了什么"的不可事后编织的证据。

---

## 决策项 C：版本绑定（可复现三元组的可执行定义）

阶段契约 v1.0 要求 S3 的 `reproducibility` 三个键**非空且不得为 n/a**，校验器已强制。但"填什么才算数"需要定义：

| 键 | 定义（可执行） | 本机适配 |
|---|---|---|
| `data_version` | 输入数据文件的**内容哈希清单**（`sha256` 逐文件），不是路径 | 直接可用 |
| `code_commit` | 若代码目录是 git 仓库 → 提交哈希；**否则** → `tree:<sha256>`，即对排序后的「相对路径+文件哈希」清单整体取哈希 | **必须走 tree 模式**，因工作区非 git 仓库 |
| `seed` | 显式记录：框架侧 seed + 数据打乱 seed + 数据划分 seed（有几个记几个） | 直接可用 |
| （附加）`env_lock` | `conda env export` 或 `pip freeze` 快照，随 run 存档 | 直接可用 |

**判定规则**：三者任一缺失或写作 `n/a` → S3 契约 FAIL；且路由门禁 **G3** 拦截"实验结果写入结论"。

---

## 决策项 D：`exp-runner` 的能力边界

**只做**：
- 按**已定设计**执行实验并记录（命令、环境、种子、产物哈希）
- 产出可复现 run 包（脚本 + 环境快照 + 数据哈希 + 日志 + 原始结果）
- 做完整性自检（三元组齐全？产物哈希可回算？日志无缺行？）

**不做**（这些是人的活）：
- 不设计实验、不定超参搜索空间（属 S1/S3 的人判断）
- 不解释结果、不下结论（属用户）
- 不把结果写进稿件（属 S5，且必须过 G3）
- 不自动重试失败实验以"凑出"好看结果

---

## 决策项 E：契约（S3）与门禁对接

```yaml
stage: S3
phase: Creation
autonomy: 人主导            # 契约强制的下限
gates:
  env_locked: pass
  data_hashed: pass
  code_versioned: pass
  seed_recorded: pass
  network_off_by_default: pass
reproducibility:
  data_version: "sha256:<清单哈希>"
  code_commit: "tree:<sha256>"      # 非 git 仓库时
  seed: "torch=17;split=17"
```

任一 gate 为 `fail` → 契约 FAIL；为 `blocked` → 必须写入 `unresolved`（校验器强制）。

---

## 决策项 F：回滚与急停

| 项 | 方式 |
|---|---|
| 单次实验回滚 | 删除 `research/50-experiments/<runid>/`（run 包自包含） |
| 环境回滚 | `conda env remove -n exp-<runid>` |
| 依赖回滚 | 每次 pip 安装前记录 `pip freeze` 快照，可逐条还原 |
| 急停 | 停止进程 + **保留日志**（不得删除日志后重跑） |

---

## 待你确认清单

| # | 事项 | 我的建议 |
|---|---|---|
| 1 | 沙箱形态选 A1 / A2 / A3？ | **A3**（conda + run 目录 + 网络默认关 + 不读凭据） |
| 2 | pip 安装是否只需"清单内免批，清单外逐次批准"？ | 是 |
| 3 | 实验写白名单是否就限 `research/50-experiments/<runid>/`？ | 是 |
| 4 | 网络是否默认关闭、按需单次申请？ | 是 |
| 5 | `code_commit` 是否接受 `tree:<sha256>`（因工作区非 git 仓库）？ | 是；或你要求我对实验目录单独 `git init` |
| 6 | 急停是否以"停进程 + 保日志"为准？ | 是 |

**在你逐条确认前，`exp-runner` 只做契约与文档，不写执行代码、不跑任何实验。**
