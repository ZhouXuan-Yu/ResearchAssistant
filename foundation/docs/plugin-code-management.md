# 插件代码管理备注（hana-paper-reader / git-save-load）

> 目的：让「后续对这两个插件做需求适配和改造」有确定的落点、流程和可回滚手段。
> 记录约定：**【实测】**=本机实际执行并观察到结果；**【文件】**=读取本地文件；**【上游】**=读取上游仓库或 raw 文件；**【推断】**=未验证，仅作假设列出。
> 最后更新：2026-09-19（本轮补全改造地图，并修正上一版对 `contributes.cards` 的错误判断）

---

## 1. 本机环境事实

| 项 | 值 | 证据 |
| --- | --- | --- |
| HanaAgent 应用版本 | **0.449.0** | 【实测】`GET /api/health` → `{"version":"0.449.0"}` |
| 活动 server 产物 | `artifacts\server\0.449.0-win32-x64` | 【文件】该目录存在；另有旧版 `0.412.7-win32-x64` 并存，**grep 时必须选对目录** |
| 活动 renderer 产物 | `artifacts\renderer\0.449.0` | 【文件】目录存在 |
| 服务端口 | 14500，`networkMode=lan`，监听 `0.0.0.0` | 【实测】`GET /api/health` → `network` 段 |
| 凭据位置 | `~\.hanako\server-info.json`（`token` 字段）**不得入库** | 【文件】 |
| 公开最新发行版 | **v0.450.0**（其后无更高数字 tag） | 【实测】`git ls-remote --tags https://github.com/liliMozi/openhanako.git` 共 436 个 tag，数字版本排序末位为 `v0.450.0` |
| 自动更新通道状态 | stable 清单拉取**失败**：origin 超出 8000ms 竞速预算，mirror 返回 404；beta 最近成功记录停留在 2026-08-03 的 `0.441.3`（低于当前） | 【文件】`artifacts\ota-state.json` |

**结论**：本机能确定取得的最高宿主版本就是 0.450.0，且自动更新通道当前不可用。

---

## 2. 四个目录的分工

| 角色 | 路径 | 是否入库 | 用途 |
| --- | --- | --- | --- |
| 上游克隆（改造落点） | `foundation\vendor\hana-paper-reader`<br>`foundation\vendor\git-save-load` | 否（`.gitignore` 含 `foundation/vendor/`） | 带完整 `.git`，唯一改造落点。可 `git diff`、可 `git checkout` 回到上游状态 |
| 发布的安装包 / 对照解包 | `foundation\external\hana-paper-reader-0.9.0.zip`<br>`foundation\external\hana-paper-reader-0.9.0\` | 否（`.gitignore` 含 `foundation/external/`） | 作者发布基线，用于确认「我们改了什么」 |
| 运行时安装副本 | `~\.hanako\plugins\<pluginId>` | 不在本仓库内 | 宿主真正加载的代码。**不要直接手改**：重装/更新会覆盖，且改动无法追溯 |
| 插件配置数据 | `~\.hanako\plugin-data\<pluginId>\config.json` | 否 | 运行时配置，含敏感项（如 MinerU Token），绝不入库 |

入库的上游基线 SHA：

| 插件 | 版本 | 分支 | HEAD | 提交日期 | LICENSE |
| --- | --- | --- | --- | --- | --- |
| hana-paper-reader | 0.9.0 | main | `d9265aa85c6520631de407a3a26511d70212d248` | 2026-09-07 | 有，MIT |
| git-save-load | 2.3.2 | master | `b5424cb9f0fc36a26747b811f30467a9aa35fcad` | 2026-08-30 | **无 LICENSE 文件** |

> `git-save-load` 无许可证文件，默认按「保留所有权利」处理。自用改造风险低；若将来要分发改造版或把其代码并入可发布产物，需先向作者取得授权。

---

## 3. 宿主插件 API（本机核对）

| 操作 | 调用 |
| --- | --- |
| 列出插件 | `GET /api/plugins` |
| 从本地路径安装 | `POST /api/plugins/install`，body `{"path":"<绝对路径，正斜杠可用；zip 或目录>"}` |
| 读/写配置 | `GET` / `PUT /api/plugins/<id>/config` |
| 启用/禁用（触发 UI 刷新） | `PUT /api/plugins/<id>/enabled`，body `{"enabled":true}` |
| 卸载 | `DELETE /api/plugins/<id>` |
| UI 贡献面 | `GET /api/plugins/pages`、`/api/plugins/widgets`、`/api/plugins/ui-host-capabilities` |
| 鉴权 | `Authorization: Bearer <token>` |

本仓库调用脚本：`foundation\tools\hana_api.ps1`（无参，读同目录 `api_request.json`）：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File C:\Users\ZhouXuan\Desktop\OH-WorkSpace\foundation\tools\hana_api.ps1
```

原因：本机命令通道对内联参数不可靠（`-Named value` 会被错误绑定），所以统一走「请求描述文件」。

上游比对脚本：`foundation\tools\plugin_source_diff.ps1 -LocalDir <A> -UpstreamDir <B>`。输出四类：仅本地 / 仅上游 / 内容真不同 / **仅行尾不同**。行尾归一化是必要的，否则会把 CRLF/LF 差异误报成「每个文件都改了」。

---

## 4. 改造纪律

1. **只在 `foundation\vendor\<plugin>` 里改**，不动 `~\.hanako\plugins\` 下的运行时副本。
2. 动手前记录基线：`git -C foundation\vendor\<plugin> rev-parse HEAD`。
3. 改完存补丁：`git -C foundation\vendor\<plugin> diff > foundation\patches\<plugin>\<描述>.patch`。补丁可被 git 跟踪、可在上游更新后重放，体积远小于整棵源码树。
4. 验证三件套：`node --check <改动的 js/mjs>` → `node --test foundation\vendor\<plugin>\tests` → 重装到宿主后 `GET /api/plugins` 确认 `status=loaded`、`error=null`，再打开界面做一次目标交互。
5. 生效方式：`POST /api/plugins/install` 指向 `vendor` 目录（或用 `DELETE` 卸载后重装）；仅需宿主重读时用 `PUT .../enabled` 关再开。
6. 回滚：`git -C foundation\vendor\<plugin> checkout -- .` 后重装；或直接装回 `foundation\external\` 里的原始发布包。
7. 凭据（MinerU Token 等）只写在 `plugin-data\<id>\config.json` 或宿主界面，不进源码、不进补丁、不进日志。

---

## 5. hana-paper-reader：当前版本在本机装不上（结论 + 三重证据）

**结论：0.9.0 无法装在 0.449.0 上，且这不是配置问题，也不是本机环境损坏。已实测尝试安装，被宿主拒绝，本机未发生任何安装副作用。**

### 证据 1：宿主硬拒绝（实测）

```
POST /api/plugins/install  {"path":".../foundation/external/hana-paper-reader-0.9.0.zip"}
→ HTTP 409
{"error":"requires app v0.686.15+, current v0.449.0","code":"PLUGIN_VERSION_INCOMPATIBLE"}
```

`GET /api/plugins` 仍只有 `git-save-load`、`hanako-hyperframes`；`GET /api/plugins/hana-paper-reader/card` → 404。即**确实没装上**。

门槛代码（0.449.0 bundle）：`gL/gT` 做 semver 比较（`index.js:16023-16032`）；加载期置 `status="incompatible"` 并告警（`16433`）；启用期同样置 `incompatible`（`17025`）；安装路径直接抛 409（`92703`、`93120`）。没有「忽略版本门槛」的配置开关。

### 证据 2：UI 贡献类型不匹配（实测 grep）

0.449.0 的 server bundle 只认三种插件 UI 贡献：`contributes?.page`（`16885`）、`contributes?.widget`（`16907`）、`contributes?.settingsTab`（`16929`）。

- 在 0.449.0 server bundle 中检索 `cards` / `cardForm` / `realization` / `functionPanel`：**0 命中**。
- 在 renderer 0.449.0 资源中检索同一组关键字：**0 命中**。

而 hana-paper-reader 的 `manifest.json` 只贡献了一个 `cards` 条目（`id: reader`，`route: /card`，`realization: page`，`functionPanel: paper-reader-panel`）。也就是说：**即使绕过版本门槛装进去，这个插件在本机也没有可显示的界面入口。**

> 上一版本文档曾写「`contributes.cards` 具备（git-save-load 用同一形态）」，该判断**错误**，在此更正。事实是：git-save-load 的 manifest 同时声明了 `contributes.widget`（`route: /widget`）和 `contributes.cards`；本机能看到的只是它的 **widget** 面板（`GET /api/plugins/widgets` 返回 `git-save-load` → `/api/plugins/git-save-load/widget`），它的 `cards` 条目同样被宿主忽略。可见宿主对不认识的贡献类型是**静默忽略**，而非报错。

### 证据 3：版本门槛不可能通过公开渠道满足（上游 + 实测）

上游各 tag 的 `minAppVersion`（【上游】逐个取 `raw.githubusercontent.com/.../<tag>/manifest.json`）：

| tag | 版本 | minAppVersion | capabilities | 备注 |
| --- | --- | --- | --- | --- |
| v0.4.2 / v0.5.0 / v0.6.1 / v0.6.2 / v0.6.3 | 同左 | **0.358.0** | session, agent, model.sample, network.fetch | 缺 `provider.read` |
| v0.7.0 / v0.7.1 / v0.8.0 / v0.9.0 | 同左 | **0.686.15** | + `provider.read` | 门槛在 0.7.0 一次抬高 |

而公开宿主最高只有 **v0.450.0**（证据 1/第 1 节）。作者自己的 README 也写明「环境要求：HanaAgent `0.686.15` 或更高版本」；`RELEASE_NOTES_0.9.0.md` 记录的实机回归环境是 **HanaAgent 0.769.0**。即：**插件瞄准的是尚未公开发布的宿主版本**。

### 那么能不能「只把门槛改小」？

不建议，理由是可核验的：门槛虽能改，但证据 2 的能力缺口改不掉（cards/functionPanel 不被支持），结果是「装上了、启用了、界面上什么都没有」。这属于把不兼容伪装成可用，不做。
若你明确要求做这个实验，做法是在 `foundation\external\` 下的**副本**里改 `minAppVersion`（原始发行包保持不动），在文档中标注「本地强制放开，非作者支持配置」，测完用 `DELETE /api/plugins/hana-paper-reader` 完全撤销。

### 什么时候能装（一步到位命令）

宿主升到 ≥0.686.15 后：

```powershell
# 修改 foundation\tools\api_request.json 为：
# {"method":"POST","path":"/api/plugins/install","body":{"path":"C:/Users/ZhouXuan/Desktop/OH-WorkSpace/foundation/external/hana-paper-reader-0.9.0.zip"}}
powershell -NoProfile -ExecutionPolicy Bypass -File C:\Users\ZhouXuan\Desktop\OH-WorkSpace\foundation\tools\hana_api.ps1
# 然后启用：PUT /api/plugins/hana-paper-reader/enabled {"enabled":true}
```

装完必做：在阅读器右上角 MinerU 设置里填 `mineruApiToken`（**只能由你提供，我不会编造**），否则 PDF 解析不可用（0.9.0 只支持 MinerU API 解析，本地解析已移除）。

---

## 6. 发布包与上游的精确差异（实测哈希比对）

比对方式：`plugin_source_diff.ps1`，逐文件 SHA-256，文本扩展名另做行尾归一化。

**hana-paper-reader**：包内 53 个文件，上游 68 个。

- 运行时代码（`index.js`、`routes/*`、`lib/*`、`assets/panel.js`、`assets/panel.css`、`assets/research-tools.*`、`assets/pdfjs.mjs`、`assets/sha256.js`）：**与上游 HEAD `d9265aa` 逐字节一致**。这意味着「上游仓库 = 安装包代码」，改造时以上游仓库为准即可。
- 仅上游有：`.github/workflows/release.yml`、`scripts/build-release.ps1`、`RELEASE_NOTES_0.6.1~0.8.0.md`、`REAL_DEVICE_VERIFICATION.md`、7 张文档截图。属于打包时剔除的 CI/发版/历史材料。
- 内容不同：`README.md`（本地版与上游版内容不同，均存在）。
- 仅本地有：`assets/hana-paper-reader-workspace.png`。

**git-save-load**：安装副本 `~\.hanako\plugins\git-save-load` 56 个文件，上游 57 个。

- **内容真不同：0 个文件**。
- 仅行尾不同：44 个文件（CRLF/LF 差异，非代码差异）。
- 仅上游有：`scripts/release.ps1`（发版脚本，属打包剔除项）。

即：**本机运行的 git-save-load 2.3.2 与上游 HEAD `b5424cb` 代码等价**。

---

## 7. 改造地图：hana-paper-reader

### 7.1 文件清单与角色

| 文件 | 体量 | 角色 |
| --- | --- | --- |
| `manifest.json` | 3.6 KB | 插件声明：id/version/minAppVersion/trust=`full-access`、capabilities、network.allowedHosts、configuration 9 项、一个 `cards` 贡献 |
| `index.js` | 618 B | 生命周期入口。`onload` 注册总线处理器 `hana-paper-reader:status`；`onunload` 记日志。真正的逻辑不在这里 |
| `routes/ui.js` | 4.4 KB | 两个 HTML 外壳路由：`GET /card`、`GET /page`。注入 `hana-css`/`hana-theme`/`hana-asset-base` 查询参数，`sanitizeAssetBase` 只接受同源且路径等于默认资源根的基址（保留宿主注入的 surface session 凭据） |
| `routes/api.js` | 103 KB / 2168 行 | 后端主体，约 45 个 API。另导出 `recentWorkspacePaper`、`saveFileToDisk` |
| `lib/mineru.js` | 32.9 KB | MinerU API 客户端（建任务、轮询、取 zip、资源读取） |
| `lib/paper-workspace.js` | 62 KB / 1236 行 | 工作区核心：`createPaperWorkspace({dataDir})` → `getPaper / persist / mutate / putAnchored / refreshFromDisk / enqueueMutation / assetBytesForPaper`；另导出 `buildOutline(blocks)`、`searchBlocks(blocks, query, opts)`、`sha256(buf)` |
| `lib/paper-storage.js` | 13 KB | 存储布局 `per-paper-v1`：`papers/<hash>/{paper.json, research.json, translations.json, tasks.json}` + 索引；多文件原子事务 + 失败回滚 |
| `lib/paper-path-guard.js` | 2 KB | `verifyNoSymlinks`，防越权路径 |
| `lib/paper-identity.js` | 1.7 KB | paperHash 规范化与合法性断言 |
| `lib/paper-metadata.js` | 2.6 KB | 作者/年份/标签/显示文本规范化 |
| `lib/paper-evidence.js` | 6 KB | 证据记录（四类证据型笔记） |
| `lib/paper-export.js` | 14 KB | `generatePaperMarkdown` 导出 |
| `lib/paper-csv.js` | 2 KB | 表格 HTML → CSV，含公式注入转义 |
| `lib/qa-log.js` | 2.8 KB | 前端上报的 QA 事件日志 |
| `assets/panel.js` | 241 KB / 4843 行 | 前端应用（**未压缩、可读**）：通过 `post/event/request` 走宿主 postMessage 桥，`pluginApiUrl/pluginApiFetch` 调本插件 API；负责标签页、文库、阅读视图、翻译、MinerU 设置、模型选择 |
| `assets/research-tools.js` + `.css` | 82 KB + 17 KB | 研究工作流（笔记/证据/大纲/进度/术语）前端 |
| `assets/panel.css` | 43.5 KB | 主样式 |
| `assets/pdfjs.mjs` | 1.63 MB | 内置 PDF.js（见 `licenses/PDFJS-APACHE-2.0.txt`） |
| `assets/sha256.js` | 3.9 KB | 浏览器端哈希 |
| `tests/` | 20 个 `.test.mjs` + `tests/fixtures/regression/` | 自带测试；作者记录 0.9.0 为 75/75 通过 |

### 7.2 后端 API 分区（`routes/api.js`）

| 分区 | 端点 |
| --- | --- |
| MinerU 配置 | `GET/POST /api/mineru-settings` |
| MinerU 资源 | `GET /api/mineru-asset`（仅当资产被论文块引用时才放行） |
| 宿主能力代理 | `GET /api/agents`、`GET /api/models` |
| 解析与生成 | `POST /api/parse-pdf`（**仅 MinerU**，非 mineru 直接 400）、`POST /api/translate`、`POST /api/ask-agent` |
| 会话投递 | `GET /api/session-targets`、`POST /api/send-to-session`、`POST /api/create-session-and-send` |
| 研究工作区 | `GET/POST/DELETE /api/research/{recent,library,library/metadata,paper,snapshot,storage,cleanup,backup,restore,csv,search,evidence,outline,progress,glossary,translation-cache,export,parse-cache/check}`、`/api/research/parse-status/tasks[/:taskId[/update|cancel]]` |
| 诊断 | `GET/POST /api/diagnostics/log` |

### 7.3 与宿主的耦合点（改造时的主要风险面）

全部经 `bus.request(...)`（【实测 grep】）：

| 总线调用 | 用途 | 所需 capability |
| --- | --- | --- |
| `provider:models-by-type` `{type:"chat"}` | 读聊天模型目录（模型选择器） | `provider.read` |
| `model:sample-text` | 翻译、证据问答 | `model.sample` |
| `session:create` / `session:update` | 建/改会话（含模型覆盖参数） | `session` |
| `session:list` / `session:get` / `session:history` | 会话列表与历史（会话目标、去重） | `session` |
| `session:send` | 把选中的论文内容投递给指定会话 | `session` |

数据面：工作区根为 `ctx.dataDir`（`createPaperWorkspace({dataDir: ctx.dataDir})`），导出临时文件写在 `ctx.dataDir/exports`；读取宿主助手目录 `~\.hanako\agents\<id>`（用于助手头像/列表）。网络出口只有 `network.allowedHosts` 白名单内的 MinerU 域名。

### 7.4 常见改造落点

- 加一个后端能力：在 `routes/api.js` 的 `registerApiRoutes` 里加路由 → 前端 `assets/panel.js` 的 `pluginApiFetch` 调用 → 补 `tests/research-api.test.mjs` 风格用例。
- 改存储结构：只动 `lib/paper-storage.js`；注意 `STORAGE_LAYOUT = "per-paper-v1"` 是兼容开关，改值会触发旧数据不迁移（`load()` 在 `storageLayout` 不匹配时返回 `split:false`）。
- 改阅读/翻译/问答逻辑：`lib/paper-workspace.js` + `routes/api.js` 对应端点。
- 改界面：`assets/panel.js`（可读代码，4843 行）；样式在 `assets/panel.css`。
- 换解析后端（若将来要脱离 MinerU）：`lib/mineru.js` 与 `POST /api/parse-pdf`，同时要改 `manifest.network.allowedHosts`（白名单是宿主强制的，改代码不改清单会被拦）。

---

## 8. 改造地图：git-save-load

| 层 | 文件 | 体量 |
| --- | --- | --- |
| 声明 | `manifest.json` | 2.9 KB。`minAppVersion 0.159.0`、trust `full-access`、hostCapabilities `external.open` + `clipboard.writeText`；贡献 `widget`（`/widget`）+ `cards`（`/git`）+ configuration（`repoPath`、`stashMode`、`pushMode`、`pullMode`、`defaultDiffMode`、`theme`、`paperTexture`、`remoteSettings`） |
| 后端路由 | `routes/*.js` 共 16 个 | `git.js` 24.6 KB、`history-edit.js` 40.3 KB、`github.js` 18 KB、`remote-push.js` 13.3 KB、`remote-edit.js` 10.9 KB、`remote-sync.js` 9.9 KB、`remote-query.js` 9.7 KB、`local-git.js` 9 KB、`repository.js`、`branch.js`、`stash.js`、`diff-conflicts.js`、`config.js`、`history.js`、`misc.js` |
| 前端 | `assets/git.html`（64.8 KB）、`assets/git.css`（43.4 KB）、`assets/git/*.js` 28 个模块 | `remotes.js` 42 KB、`commit-edit.js` 17.5 KB、`gh-repos.js` 15.8 KB、`branch-actions.js` 14.6 KB、`commit-actions.js` 14 KB、`branch-canvas.js`、`repo-path.js`、`log-view.js`、`gh-panel.js`、`settings.js`、`hana-select.js`、`refresh.js`、`card-drag.js`、`state.js`、`status-card.js`、`reset.js`、`conflicts.js`、`identity.js`、`repo-init.js`、`walkthrough.js`、`main.js`、`ctx-menu.js`、`confirm-modal.js`、`env.js`、`gh-connect.js`、`diff-view.js` |
| Agent 工具 | `tools/*.js` 5 个 | `git_status`、`git_log`、`git_commit`、`git_reset`、`_helpers`。**这是本仓库 git 追踪流程可以改进的接口面** |
| 文档 | `README.md` 24.9 KB、`DESIGN.md`、`linear.DESIGN.md` 24.9 KB、`docs/踩坑记录.md`、`docs/架构文档.md`、`docs/简易使用文档.md` | |

改造落点：新增/调整 Git 能力 → `routes/<主题>.js` + `assets/git/<模块>.js`；想让它「每次改动自动提交」→ 优先动 `tools/git_commit.js` 与后端 `routes/git.js`，而不是前端按钮。

---

## 9. 未验证与待办

- 未验证：是否存在非公开的 HanaAgent 内测通道可拿到 ≥0.686.15（本机 OTA 通道已坏，无法自查）。
- 未验证：`contributes.cards` 是否会随宿主升级出现（结论基于 0.449.0 产物，宿主升级后需重测）。
- 待办：宿主升到 ≥0.686.15 后，按 §5 的命令安装 + 填 MinerU Token + 打开卡片做一次实机验收。
- 待办：`foundation\patches\` 目录尚未建立（第一次真正改插件时建立）。
