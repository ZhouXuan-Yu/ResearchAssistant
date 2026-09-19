# Zotero 环境配置状态（Better Notes + 图书馆）

> 建立：2026-09-18｜执行：agent-mu42qzfz｜状态：**已完成**

## 1. 环境事实 [一手]

| 项目 | 值 |
|---|---|
| Zotero 主程序 | `D:\Zotero\zotero.exe`（文件版本 10.0.3）|
| 数据目录 | `C:\Users\ZhouXuan\Zotero`（`useDataDir=true`）|
| 配置文件目录 | `C:\Users\ZhouXuan\AppData\Roaming\Zotero\Zotero\Profiles\8lzj7o3p.default` |
| 本地 API | 已启用，监听 `127.0.0.1:23119` |
| 本地写入 | 可用（local 模式，密钥已持有）|

## 2. 已完成

### 2.1 Better Notes 插件
- 版本 **v3.3.3**（2026-08-24），addon id `Knowledge4Zotero@windingwind.com`
- 兼容区间 `8.0-beta.21` ~ `10.99.99`，与 Zotero 10 兼容
- 安装包留存：`foundation\downloads\better-notes-for-zotero-3.3.3.xpi`
- 安装方式：解包至 `<profile>\extensions\Knowledge4Zotero@windingwind.com\`
- **最终状态：`active=True`** —— 已启用生效（用户在 Zotero 界面完成启用）

> 关键事实：Zotero 10 对侧载插件有硬性启用门禁，`extensions.autoDisableScopes=0`、
> 手改 `extensions.json` 的 `userDisabled/seen`、删除注册记录后重扫，**均无效**。
> 唯一可靠路径是用户在图形界面中启用一次。此后切勿重复尝试上述绕过手段。

### 2.2 Zotero 图书馆分类
- 顶层分类 **「入门」**，key = `CRFTWXNP`
- 已入库 6 条，全部按 DOI 从 CrossRef 取正式元数据：

| Key | 题目 | 年份 | 归属 |
|---|---|---|---|
| `E9BX6SKC` | SwinGAN: GAN-based algorithm for generating Qin bamboo slips character images | 2023 | 导师组 |
| `P39YEQY2` | Research on the Qin bamboo slip character images inpainting algorithm based on the context encoder model | 2024 | 导师组 |
| `VCBTSRC2` | Method for Qin Bamboo Slip Text Detection Based on an Enhanced DBNet Model | 2024 | 导师组 |
| `2BU4FFFS` | ResFormer diffusion: latent diffusion model with residual transformer for Qin bamboo character image expansion | 2025 | 导师组 |
| `AB3E22Z5` | Semi-supervised restoration of damaged characters in Liye Qin bamboo slips | 2026 | 他组（npj Heritage Science）|
| `XDUEJ3DA` | Intelligent Fault Diagnosis Method for Complex Equipment Based on Knowledge Graph | 2024 | 导师组（非秦简）|

- **未入库**：《现代电子技术》2025 年第 17 期《基于改进条件扩散模型的残简文字修复方法》（谭俊毅等）。该刊无 DOI，CrossRef/OpenAlex 不覆盖，属检索盲区，需 CNKI 通道手工录入。

## 3. 我改动过的文件与回滚

| 文件 | 改动 | 回滚 |
|---|---|---|
| `<profile>\extensions\` | 新增 `Knowledge4Zotero@windingwind.com\` 目录 | 删除该目录 |
| `<profile>\extensions.json` | 试验中曾改写，已还原 | 备份 `.bak3` / `.bak4` |
| `<profile>\prefs.js` | 试验中曾插入 `autoDisableScopes`，已移除 | 备份 `_hana_backup\prefs.js.bak2` |
| Zotero 数据目录 | 无改动 | — |

## 4. 待办
- [ ] Better Notes 内配置模板与导出目录
- [ ] 《现代电子技术》那篇中文论文手工入库
- [ ] 入库条目未附 PDF（`attach_mode=none` 以规避网络抖动）
