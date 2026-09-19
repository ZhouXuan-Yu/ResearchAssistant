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
2. ~~**ffmpeg / ffprobe 未安装**~~ —— **已解决（2026-09-19 19:32）**：以官方上游便携构建装入 `C:\Users\ZhouXuan\tools\ffmpeg\bin`，用户级 PATH 已追加，端到端编码与探测均已验证通过。详见 `foundation/docs/ffmpeg-install.md`。注意生效条件：HanaAgent 重启后其子进程才能看到新的 PATH。
3. 该配置是绕过，不是根治。根治需修 `lib/command-runner.js` 的引号拼接；插件升级后需复核配置是否仍被保留。

---

## 2. 右侧 Git 面板（git-save-load）不显示

### 结论（已定位到确定成因）
插件本身没有被禁用、没有被隐藏、权限门槛也通过了。面板不出现的直接原因是：宿主渲染层在**窗口启动时**拉取一次插件 UI 清单（store 字段 `pluginWidgets`），而本窗口启动在前、插件安装在后 —— 清单里从来没有 git-save-load。

### 服务端事实（全部实测，2026-09-19 当晚）
| 检查项 | 结果 |
| --- | --- |
| `GET /api/plugins/widgets` | `[{pluginId:"git-save-load", title:"Git", routeUrl:"/api/plugins/git-save-load/widget", hostCapabilities:["external.open","clipboard.writeText"]}]` |
| `GET /api/plugins/git-save-load/widget` | 200，61505 字节（`<title>Save/Load</title>`，`data-hana-widget="1"`） |
| `GET /api/preferences/plugin-ui` | `{"hiddenWidgets":[],"hiddenTabs":[],"tabOrder":[]}` —— 没有被隐藏 |
| `~/.hanako/user/preferences.json` | `allow_full_access_plugins: true`、`disabled_plugins: []` —— 全权限门槛已开，且不在禁用名单 |
| 插件目录 | 根目录仅 `manifest.json / assets / docs / routes / tools / *.md`，**没有 `index.js`** |

### "Activation: none" 是什么（重要，易误读）
插件详情里那行 Activation 显示 `none`，容易被读成"没激活所以用不了"。宿主实现如下：

```js
async _activatePluginEntry(t, r = {}, n = t._loadToken) {
  if (!t.hasLifecycle || t.activationState === "activated") return t;   // ← 无生命周期入口，直接返回
  ...
}
```

`hasLifecycle` 取决于插件根目录是否存在生命周期入口（`index.js`）。git-save-load 没有 → 宿主**按设计跳过**激活 → `activationState` 永远停在 `none`。它的工具在**加载阶段**就已注册（`_loadTools`），widget 路由由宿主静态托管，二者都不依赖激活。

对照：hanako-hyperframes 带 `index.js` 且 `activationEvents:["onStartup"]`，所以显示 `activated`。

**结论：`none` 不是开关、不是缺陷、也不是面板不显示的原因，修改不了也不需要修改。**

### Git 面板的入口位置（渲染层实证）
渲染层 `ChatPage` 标题栏右侧按钮组（`tb-right-group`，与"预览"开关同一排）：

```js
h.jsxs("div",{className:"tb-right-group",children:[ f && h.jsx(X0,{}), d && a && h.jsx("button",{className:"tb-toggle tb-toggle-preview",...}) ]})
```

而 `X0()` 的第一句是硬门槛：

```js
if (s !== "chat" || n.length === 0) return null;   // s = currentTab，n = pluginWidgets
```

即：**必须停在聊天页，且 `pluginWidgets` 非空**，按钮才会渲染。该插件未提供 icon，按钮以标题文字 "Git" 呈现；点击后把右侧栏切到 `jianView = "widget:git-save-load"`（`openWidget(pluginId)`）。

### 处置（已执行，免重启）
宿主在插件安装/卸载/启停/权限变更时都会广播 `plugin_ui_changed`；渲染层 WebSocket 处理器收到后重新拉取清单：

```js
case "plugin_ui_changed": import("./plugin-ui-actions-....js").then(n => n.refreshPluginUI()); break;
```

因此对当前窗口执行一次幂等的启用即可触发刷新：

```
PUT /api/plugins/git-save-load/enabled   body {"enabled":true}
→ 200 {"ok":true}     # enablePlugin 内部 emit({type:"plugin_ui_changed"})
```

已执行；执行后 `GET /api/plugins/widgets` 仍正确返回该 widget。

**未自证**：该 WebSocket 消息在运行窗口中的接收与最终渲染结果属窗口内状态，外部不可观测。若聊天页标题栏仍未出现 "Git" 按钮，重载窗口（Ctrl+R）或重启 HanaAgent 后再点。

补充（客户端刷新路径亦已查明）：`plugin-ui-actions` 导出的 `refreshPluginUI()` 在启动时以及收到 `plugin_ui_changed` 时调用；`hiddenWidgets` 为空的插件按钮按标题文字渲染，"Hidden plugins → Show" 仅对已隐藏项出现。

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
| 组件显隐偏好 | `GET/PUT /api/preferences/plugin-ui`（字段 `hiddenWidgets,hiddenTabs,tabOrder`） |
| 刷新客户端插件 UI | 服务端广播 WS 消息 `plugin_ui_changed` → 渲染层 `refreshPluginUI()` |
| 插件自检 | `GET /api/plugins/hanako-hyperframes/api/diagnostics` |
| 启动/停止预览 | `POST / DELETE /api/plugins/hanako-hyperframes/api/projects/:id/preview` |

鉴权：token 与端口读自 `~/.hanako/server-info.json`，同时以 `?token=` 与 `Authorization: Bearer` 传递。

关键路径：
- 插件目录 `~/.hanako/plugins/<id>`
- 插件配置 `~/.hanako/plugin-data/<id>/config.json`
- 安装登记 `~/.hanako/plugin-installs.json`
- 桌面主程序 `~/AppData/Local/Programs/HanaAgent/resources/app.asar`
