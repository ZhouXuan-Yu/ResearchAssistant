# FFmpeg / FFprobe 安装记录（便携构建）

记录时间：2026-09-19 19:31–19:32（本地）
主机：Windows 10.0.26200（win32-x64），用户 ZhouXuan

---

## 背景

HyperFrames 插件要求 `ffmpeg` 与 `ffprobe` 位于 PATH（`plugins/hanako-hyperframes/README.md` 的 Requirements；`lib/command-runner.js` 对二者做 `-version` 自检）。安装前两者在本机均不存在，属于**真实缺口**，与前述 cmd 引号缺陷造成的假阴性是两件事。

## 通道选择

| 通道 | 状态 | 结论 |
| --- | --- | --- |
| winget | 本机不存在 | 不可用 |
| Chocolatey | `C:\ProgramData\chocolatey\bin\choco.exe` 存在 | 安装落系统级目录，通常需管理员；未采用 |
| 第三方程序自带 | `D:\YouNavi\resources\bin\ffmpeg.exe`（6.1.1-essentials）、`D:\影刀\shadowbot-*\ffmpeg.exe` | **同目录无 ffprobe**，且属他程序资产；未采用 |
| 官方上游便携构建 | BtbN `ffmpeg-master-latest-win64-gpl.zip` | **采用** |

选便携构建的理由：不需要管理员权限；只写用户目录；PATH 只改用户级（`HKCU\Environment`）；回滚只需删目录并还原 PATH 备份。

## 执行

- 脚本 `foundation/tools/install_ffmpeg.ps1`，后台执行，日志 `foundation/tools/install_ffmpeg.log`
- 下载 `https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip`
  194553535 字节，19:31:07 → 19:32:02（约 55 秒）
- 解压 `tar.exe -xf`，exit 0；临时目录已清理
- 落盘 `C:\Users\ZhouXuan\tools\ffmpeg\bin\`：`ffmpeg.exe` `ffprobe.exe` `ffplay.exe`
- PATH：追加用户级 PATH；变更前原值备份于 `C:\Users\ZhouXuan\tools\ffmpeg\PATH.user.bak.txt`
- 未修改机器级 PATH，未触碰其他程序自带的 ffmpeg

## 版本

```
ffmpeg  version N-126636-g1ef0d9d701-20260918 (master, gpl)
ffprobe version N-126636-g1ef0d9d701-20260918 (master, gpl)
```

## 验证（`foundation/tools/verify_ffmpeg.ps1`）

| 检查项 | 结果 |
| --- | --- |
| 用户级 PATH 含 bin 目录 | True |
| 当前进程 PATH 含 bin 目录 | **False**（本进程继承旧环境块，符合预期） |
| 端到端编码：`testsrc` → h264 mp4 | exit 0，输出 7341 字节（libx264 可用） |
| `ffprobe -show_entries stream=codec_name,width,height` | exit 0，`codec_name=h264 width=320 height=240` |

两处 `-version` 之外还做了一次真实编码与探测，因此"可用"这一判断有功能证据，不只是版本字符串。

## 生效条件（重要）

Windows 子进程继承父进程的环境块。HanaAgent 主程序启动于 18:28（本次 PATH 变更之前），因此：

- 其子进程（含 HyperFrames 插件拉起的 CLI）在本次变更后仍看不到 ffmpeg，**直到 HanaAgent 重启**。
- 插件诊断面板里 `ffmpeg` / `ffprobe` 可能仍显示 FAIL。推断原因：该自检与 `node` 走同一条带引号缺陷的 `cmd.exe` 包装路径（`checkExecutable({file:"ffmpeg", args:["-version"]})`），属假阴性。此推断基于同一代码路径，未在插件面板上实测。
- 新开的终端与进程会正常看到 ffmpeg。

## 回滚

1. 还原用户级 PATH：

```powershell
[Environment]::SetEnvironmentVariable('Path', (Get-Content 'C:\Users\ZhouXuan\tools\ffmpeg\PATH.user.bak.txt' -Raw).Trim(), 'User')
```

2. 删除 `C:\Users\ZhouXuan\tools\ffmpeg`

## 未做与未决

- 未验证 HyperFrames 的真实渲染链路。需在 HanaAgent 重启后跑一次真实渲染；若仍失败，再查渲染管线内部的 ffmpeg 调用。
- 便携构建不参与系统更新，后续升级需手动替换（同目录覆盖即可）。
