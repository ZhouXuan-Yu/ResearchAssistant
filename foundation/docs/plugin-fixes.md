# 插件故障处置记录

记录时间：2026-09-19（本地）
环境：HanaAgent 0.449.0（desktop，win32-x64），server 端口 14500，Node v24.12.0（D:\Node）

---

## 1. HyperFrames 页面空白 —— 已修复并端到端验证

### 现象
打开 HyperFrames 页面后整页空白。

### 证据
renderer 日志（`~/.hanako/diagnostics/desktop-launch/renderer.log`）在修复前重复出现：

```
did-fail-load  http://127.0.0.1:60619/#project/hyperframes  errorCode -102  ERR_CONNECTION_REFUSED
```

端口每次不同（60619 / 51582 / 64887），说明插件反复尝试拉起 Studio 开发服务器但连不上。

页面外壳本身正常：`GET /api/plugins/hanako-hyperframes/studio` 返回 200，`panel.js`（210849 字节）与 CSS 带 token 均 200（不带 token 一律 403，属预期）。

### 根因
插件 `lib/command-runner.js` 在 Windows 下通过 `cmd.exe /d /s /c` 启动进程时，**对整条命令的每个 token 单独加引号且不加外层包裹**，cmd 的 `/s` 规则会把首尾引号成对剥离，导致命令被破坏。

用插件自己的 `createSpawnInvocation` 复现：`npx`、`npx.cmd`、`node` 全部失败。再用纯 cmd（不经过 Node 转义）复核：

| 形式 | 结果 |
| --- | --- |
| `cmd /d /s /c "node" "--version"` | 失败：`'node" "--version' is not recognized` |
| `cmd /d /s /c node --version` | v24.12.0 |
| `cmd /d /s /c ""node" "--version""` | v24.12.0 |
| `cmd /d /s /c "npx.cmd" "--version"` | 失败 |

结论：该构建方式在本机无法执行**任何**命令，与 `npx` 是否在 PATH 无关。CLI 起不来 → Studio 开发服务器未监听 → iframe 拒连 → 页面空白。

### 处置（配置层绕过 cmd，未改动插件代码）
插件 `hyperframesCommand` 的解析结果是「首 token 作为可执行文件 + 其余作为参数数组」，且当首 token 带非 `.cmd/.bat` 扩展名时不走 cmd 包装（直接 spawn）。因此改为：

```
hyperframesCommand = D:/Node/node.exe D:/Node/node_modules/npm/bin/npx-cli.js --yes hyperframes
```

- 用正斜杠书写：插件的命令行解析把 `\` 当转义符，反斜杠路径无法表达。
- 写入方式：`PUT /api/plugins/hanako-hyperframes/config`，body `{scope:"global", values:{...}}`。
- 落盘确认：`~/.hanako/plugin-data/hanako-hyperframes/config.json` 中 `global.hyperframesCommand` 已更新。
- 随后 `PUT /api/plugins/hanako-hyperframes/enabled` 置 false 再 true，重建 PreviewManager（该实例被缓存，只改配置不会生效）。

### 验证
| 检查项 | 修复前 | 修复后 |
| --- | --- | --- |
| 配置命令可执行 | `'"npx"' 不是内部或外部命令` | 退出码 0，输出 `0.7.22` |
| 插件自检 hyperframes | FAIL | OK，0.7.22 |
| `POST /api/projects/hyperframes/preview` | 无进程 | `status = running` |
| 预览原始地址 | `ERR_CONNECTION_REFUSED` | HTTP 200 |
| 插件代理地址 `/studio-proxy/hyperframes/` | — | HTTP 200（4481 字节） |
| renderer 日志 | 反复 ERR_CONNECTION_REFUSED | `[HyperFrames] ... sourceId: http://127.0.0.1:51287/assets/index-B4h4u7eW.js`（Studio 自身前端脚本已在 iframe 中执行） |

（验证后已调用 `DELETE /api/projects/hyperframes/preview` 停止进程，未残留后台服务。）

### 残留问题
1. **诊断面板会误报 `node` FAIL**：插件自检用同一套 cmd 包装去 spawn 裸命令 `node`，必然失败。属误报，不影响功能；修它需要改插件源码（上游 bug），改动会被插件更新覆盖。
2. **ffmpeg / ffprobe 未安装**（PATH 中确认不存在）。这是真缺口：视频渲染与媒体探测不可用。与上述引号缺陷无关。
3. 该配置是绕过，不是根治。根治需修 `lib/command-runner.js` 的引号拼接；插件升级后需复核配置是否仍被保留。

---

## 2. 右侧 Git 面板（git-save-load）不显示

### 已验证的服务端事实
- `GET /api/plugins/widgets` 返回：`{pluginId:"git-save-load", title:"Git", routeUrl:"/api/plugins/git-save-load/widget", hostCapabilities:["external.open","clipboard.writeText"]}`。
- `GET /api/plugins/git-save-load/widget` 200，页面 62558 字节；其 `git-asset/*` 子资源带 token 均 200。
- 插件多次加载日志均正常（`loaded "git-save-load" widget`）。

### 推断原因
宿主渲染层在**应用启动时**拉取一次 widget 列表。本窗口启动于 18:27，插件安装于 18:44，即当前窗口从未看到该插件。

### 处置
重载应用窗口（Ctrl+R / F5）或重启 HanaAgent，然后在右侧面板的组件列表中选 Git。
未能自证：面板的实际视觉渲染只能由用户确认。

---

## 3. 设置 → 插件 拖放区「导入文件夹或 zip」无反应

### 界面定位
文案 `settings.plugins.dropzone` = "Drag plugin folder or .zip here to install, or click to select"。

### 真实代码（`artifacts/renderer/0.449.0/assets/SettingsContent-*.js`）

```js
x = async (D) => { await hanaFetch("/api/plugins/install", {method:"POST", body: JSON.stringify({path: D})}) ... }
$ = async () => { const D = await Wn?.selectPlugin?.(); D && await x(D) }              // 点击拖放区
I = async (e) => { ...; const j = Wn?.getFilePath?.(e.dataTransfer.files[0]) || ...; j && await x(j) }  // 拖入
```

两条路径都用可选链：桥接方法返回空值就**静默返回**，不弹窗、不报错、不提示。这与「没有反应」的表现一致。

### 已查明的两侧实现
- 桌面 preload（app.asar）确实暴露：`selectPlugin: () => ipcRenderer.invoke("select-plugin")`、`getFilePath: (f) => webUtils.getPathForFile(f)`。
- 主进程确实实现 `select-plugin`：`dialog.showOpenDialog({properties:["openFile","openDirectory"], filters:[{name:"Plugin", extensions:["zip"]}, ...]})`。
- 另存在一份 web 回退实现（非桌面外壳时使用），其中 `selectPlugin: async () => null`、`getFilePath: () => null` —— 命中它就会完全无反应。

### 未决
运行中的窗口实际绑定的是哪一份桥接，属窗口内状态，无法从外部检查，故不下结论。
判别方法：点击拖放区——弹出文件对话框则桥接正常（失败时会有红色 toast「插件安装失败」）；不弹对话框则桥接为空值，走 API 安装可绕开（本机已验证可行）。

---

## 4. 附：本次用到的接口与位置

| 用途 | 调用 |
| --- | --- |
| 安装插件 | `POST /api/plugins/install`，body `{path}` |
| 插件配置读写 | `GET/PUT /api/plugins/:id/config` |
| 插件启停 | `PUT /api/plugins/:id/enabled`，body `{enabled}` |
| 卸载插件 | `DELETE /api/plugins/:id` |
| widget 列表 | `GET /api/plugins/widgets` |
| 页面列表 | `GET /api/plugins/pages` |
| 插件自检 | `GET /api/plugins/hanako-hyperframes/api/diagnostics` |
| 启动/停止预览 | `POST / DELETE /api/plugins/hanako-hyperframes/api/projects/:id/preview` |

鉴权：token 与端口读自 `~/.hanako/server-info.json`，同时以 `?token=` 与 `Authorization: Bearer` 传递。

关键路径：
- 插件目录 `~/.hanako/plugins/<id>`
- 插件配置 `~/.hanako/plugin-data/<id>/config.json`
- 安装登记 `~/.hanako/plugin-installs.json`
- 桌面主程序 `~/AppData/Local/Programs/HanaAgent/resources/app.asar`
