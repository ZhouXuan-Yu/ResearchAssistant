# 交付面报告（word_report）

## 单一语义源

`final_paper/manuscript.md` 是唯一内容源。以下各面**均为其机械派生**：

| 交付面 | 生成方式 | 状态 |
|---|---|---|
| `final_paper/paper.docx` | pandoc `md -> docx` | 已生成 |
| `final_paper/main.tex` | pandoc `md -> latex (standalone)` | 已生成，**未编译** |
| `final_paper/manuscript.html` | 自建转换（表格/图/引用） | 已生成 |
| `final_paper/paper.pdf` | Chromium 打印 `manuscript.html` | 见运行记录 |

## 一致性要求

各面共享同一份数字、引用与图注。布局差异仅来自渲染器，不来自内容分叉。
