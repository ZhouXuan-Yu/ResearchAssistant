# 最终产物清单（final_artifact_manifest）

| 产物 | 路径 | 类别 | 生成方式 | 状态 |
|---|---|---|---|---|
| 正文单源 | `final_paper/manuscript.md` | required | 手写（唯一语义源） | 完成 |
| Word | `final_paper/paper.docx` | optional-word | pandoc md 转 docx | 完成 |
| LaTeX | `final_paper/main.tex` | required | pandoc md 转 latex | 完成，**未编译**（无 TeX 引擎） |
| HTML | `final_paper/manuscript.html` | pro-extra | 自建转换 | 完成 |
| PDF | `final_paper/paper.pdf` | required | Edge headless print-to-pdf | 完成（1,562,526 B） |
| 图 1 | `final_paper/figures/fig1_evidence_landscape.png` | required | matplotlib 300 dpi | 完成 |
| 图源 | `final_paper/figures/fig1.py` | required | 可编辑源 | 完成 |

## 单一语义源声明

上述各交付面**全部由 `manuscript.md` 机械派生**，不存在第二份手写内容源。
布局差异来自渲染器，不来自内容分叉。

## 修订记录

| 日期 | 改动 | 触发 |
|---|---|---|
| 2026-09-19 | 全部交付面按修订后的 manuscript.md 重新派生；PDF 由 1,846,228 B 变为 1,562,526 B（段落合并渲染） | 独立盲评修订后重出；与 main.tex 同步 |
| 2026-09-19 | HTML 渲染器修复：合并硬换行段落、渲染引用块，消除 HTML/PDF 与 markdown 源的分叉 | 交付面一致性核验 |
| 2026-09-19 | 正文 §5 标题由“三项”改为“四项”，GAP-1 改为受限样本表述 | 自查发现修订引入的新矛盾 |
| 2026-09-19 | 补类别标签列 | artifact_check 提示 |

## 未完成项（如实登记）

- `visual_audit_manifest.json` 的逐页收据：**未生成**。本机缺 poppler（`pdfinfo` / `pdftoppm`）
  与 PyMuPDF，`visual_readiness_check.py --prepare` 无法渲染 PDF 页面；**未写任何目视 PASS**。
- `structured_review.md` 与 `reviewer_audit.md`：**已由独立评审者产出**（见二文件），
  但评审对象为**修订前**版本；修订后须再评审一轮方可判定收口。
- `reviewer_audit.md` 的核验附录由科研助手补写，非评审者原文，已在文首区分标注。
