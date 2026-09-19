# -*- coding: utf-8 -*-
"""ps_stage.py - assemble a HanaAgent-installable paper-spine skill package."""
import os
import shutil

PKG = r"C:\Users\ZhouXuan\Desktop\OH-WorkSpace\foundation\external\paper-spine-skill\paperspine5-skill-0.4.0-alpha.1-dev"
SRC = os.path.join(PKG, "core", "01_PaperSpine4", "src")
OUT = r"C:\Users\ZhouXuan\Desktop\OH-WorkSpace\foundation\packages\paper-spine"

ADAPT = """# HanaAgent 适配说明（本地附加文件，非上游内容）

本文件由 HanaAgent 侧附加，用于记录上游技能与本平台的差异。
**上游 `SKILL.md` 未作任何改动**，以便日后与本仓库 diff。

## 平台差异

上游 `paper-spine` 假定宿主具备：

1. 自带启动器（`launch --no-open` 返回服务 URL）；
2. 与启动器配套的 MCP/REST 桥（`paperspine_open_task`、`host wait`、
   `skill_bridge.web_path`）；
3. `.paperspine5` profile 与 `paper_rewriting_output/` 任务树。

HanaAgent 不具备 (1)(2)。因此：

- **跳过** "启动 Web 摄入界面" 相关步骤；配置与选择改为在对话内以文本确认，
  并落盘到任务目录的 Markdown 文件。
- 其余方法学章节（研究方法、贡献与证据契约、写作、**科研绘图流程**、
  渲染与目视就绪门、独立评审、交付与返修）**照常适用**，且是引入本技能的主要价值。
- `scripts/` 下 Python 工具多数可直接运行；依赖缺失时按方法论手工执行同等检查。

## 与既有技能的分工（避免双重调度）

| 领域 | 归属 | 说明 |
|---|---|---|
| 论文全流程编排 | **本技能** | 仅在用户明确要求走 PaperSpine 流程时启用 |
| 单点写作/润色 | nature-writing / nature-polishing | 局部文字任务优先用它们 |
| 数据图与期刊配图 | scipilot-figure-skill / nature-figure | 常规出图优先用它们 |
| 模拟审稿 | nature-reviewer / academic-paper-reviewer | 审稿任务优先用它们 |

本技能的价值在于**跨阶段编排 + 硬门控（目视就绪门、引用身份核验、独立评审不可自代）**，
不在替代上述窄领域技能。

## 许可证

上游 MIT License，Copyright (c) 2026 PaperSpine contributors。
本适配文件不改变上游许可。
"""


def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)

    for name in ("SKILL.md",):
        shutil.copy2(os.path.join(SRC, "skill", name), os.path.join(OUT, name))
    for name in ("references", "agents"):
        shutil.copytree(os.path.join(SRC, "skill", name), os.path.join(OUT, name))
    shutil.copytree(os.path.join(SRC, "scripts"), os.path.join(OUT, "scripts"))

    with open(os.path.join(OUT, "HANA-ADAPTATION.md"), "w", encoding="utf-8") as fh:
        fh.write(ADAPT)

    total = 0
    for root, dirs, files in os.walk(OUT):
        total += len(files)
    print("staged files:", total)
    for e in sorted(os.listdir(OUT)):
        p = os.path.join(OUT, e)
        n = 0
        if os.path.isdir(p):
            for _, _, fs in os.walk(p):
                n += len(fs)
            print(f"  {e}/  ({n} files)")
        else:
            print(f"  {e}  ({os.path.getsize(p)} B)")


if __name__ == "__main__":
    main()
