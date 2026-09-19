# -*- coding: utf-8 -*-
"""reexport.py - re-derive every delivery surface from the revised manuscript.md.

manuscript.md is the single semantic source. Mechanical derivation only:
  paper.docx / main.tex  <- pandoc
  manuscript.html        <- md_to_html below
  paper.pdf              <- headless Edge print of manuscript.html

Renderer fix (2026-09-19): the earlier converter emitted one <p> per source line,
which split hard-wrapped paragraphs and dropped blockquote notes ('>' lines), so the
HTML/PDF faces diverged from the markdown source. Consecutive wrapped lines are now
joined into one paragraph, list items start a new block, and blockquotes render.
"""
import os
import re
import subprocess
import sys
import shutil

ROOT = r"C:\Users\ZhouXuan\Desktop\OH-WorkSpace\foundation\dryrun\spine-001\paper_rewriting_output"
FP = os.path.join(ROOT, "final_paper")
TOOLS = r"C:\Users\ZhouXuan\Desktop\OH-WorkSpace\foundation\tools"

with open(os.path.join(FP, "manuscript.md"), encoding="utf-8") as fh:
    md = fh.read()

body_md = md.split("---", 2)[2]

HEAD = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>高效视觉 Transformer 的方法学图谱（演练稿）</title>
<style>
  @page { size: A4; margin: 20mm 18mm; }
  body { font-family: "Noto Serif SC","Songti SC",serif; font-size: 10.5pt;
         line-height: 1.75; color: #1a1a1a; max-width: 100%; }
  h1 { font-family: "Noto Sans SC",sans-serif; font-size: 17pt; line-height:1.4;
        border-bottom: 2px solid #333; padding-bottom: 6px; }
  h2 { font-family: "Noto Sans SC",sans-serif; font-size: 13pt; margin-top: 20px; }
  h3 { font-family: "Noto Sans SC",sans-serif; font-size: 11.5pt; }
  table { border-collapse: collapse; width: 100%; font-size: 9.5pt; }
  th, td { border: 1px solid #bbb; padding: 4px 6px; text-align: left; }
  th { background: #f2f2f2; }
  figure { margin: 14px 0; text-align: center; }
  figure img { width: 100%; }
  .bib { font-size: 9pt; line-height: 1.5; }
  .bib p { margin: 3px 0; padding-left: 2em; text-indent: -2em; }
  .note { border-left: 3px solid #ddd; padding: 2px 0 2px 10px; color: #555;
          font-size: 9.5pt; }
  code { font-family: Consolas, "JetBrains Mono", monospace; font-size: 0.92em;
         background: #f4f4f4; padding: 0 2px; border-radius: 2px; }
  .drill { background:#fff8e1; border-left:4px solid #e0a800; padding:8px 12px;
            font-size:9.5pt; margin-bottom:16px; }
</style></head><body>
<div class="drill"><strong>架构演练稿（spine-001）。</strong>
本文件由 PaperSpine 编排脊柱在公开通用主题上跑通，用于验证流程与门控；
<strong>不是用户研究方向的成果</strong>，不含任何实验数据。</div>
"""


def join_lines(lines):
    """Join hard-wrapped markdown lines; keep a space only between two ASCII alnum edges."""
    s = ""
    for ln in lines:
        if s and s[-1].isascii() and s[-1].isalnum() and ln[:1].isascii() and ln[:1].isalnum():
            s += " "
        s += ln
    return s


def bold(txt):
    txt = re.sub(r"`([^`]+)`", r"<code>\1</code>", txt)
    while "**" in txt:
        txt = txt.replace("**", "<strong>", 1).replace("**", "</strong>", 1)
    return txt


def md_to_html(block):
    out, in_tbl, buf = [], [False], []

    def close_tbl():
        if in_tbl[0]:
            out.append("</tbody></table>")
            in_tbl[0] = False

    def flush():
        if buf:
            out.append("<p>" + bold(join_lines(buf)) + "</p>")
            del buf[:]

    for raw in block.splitlines():
        line = raw.rstrip()
        stripped = line.strip()
        if line.startswith("# "):
            flush()
            close_tbl()
            out.append("<h2>" + line[2:] + "</h2>")
            continue
        if line.startswith("|") and set(line) & set("-") and "---" in line:
            flush()
            continue
        if line.startswith("|"):
            flush()
            cells = [c.strip() for c in line.strip("|").split("|")]
            if not in_tbl[0]:
                out.append("<table><tbody>")
                in_tbl[0] = True
                out.append("<tr>" + "".join("<th>" + c + "</th>" for c in cells) + "</tr>")
            else:
                out.append("<tr>" + "".join("<td>" + c + "</td>" for c in cells) + "</tr>")
            continue
        if stripped.startswith("!["):
            flush()
            close_tbl()
            alt = stripped[2:stripped.index("]")]
            src = stripped[stripped.index("(") + 1:stripped.rindex(")")]
            out.append('<figure><img src="' + src + '" alt="' + alt + '"></figure>')
            continue
        if stripped.startswith("[R") and ". " in stripped:
            flush()
            close_tbl()
            out.append('<p class="bib">' + bold(stripped) + "</p>")
            continue
        if stripped.startswith(">"):
            flush()
            out.append('<p class="note">' + bold(stripped.lstrip(">").strip()) + "</p>")
            continue
        if stripped.startswith(("- ", "* ", "1. ", "2. ", "3. ", "4. ", "5. ")):
            flush()
            buf.append(stripped)
            continue
        if not stripped:
            flush()
            close_tbl()
            continue
        buf.append(stripped)

    flush()
    close_tbl()
    return "\n".join(out)


html = HEAD
html += "<h1>高效视觉 Transformer 的方法学图谱（2021–2026）：证据约束小型综述</h1>\n"
html += "<p style='color:#666;font-size:9.5pt;margin-top:-6px'>架构演练稿 · spine-001 · 修订于 2026-09-19</p>\n"
html += md_to_html(body_md)
html += "</body></html>"

hp = os.path.join(FP, "manuscript.html")
with open(hp, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(html)
print("wrote manuscript.html", len(html), "chars")

PANDOC = shutil.which("pandoc") or r"D:\Anaconda\Library\bin\pandoc.EXE"
mdp = os.path.join(FP, "manuscript.md")
for args, out in (
    ([mdp, "-o", os.path.join(FP, "paper.docx"), "--resource-path", FP], "paper.docx"),
    ([mdp, "-o", os.path.join(FP, "main.tex"), "-s", "--resource-path", FP,
      "-V", "CJKmainfont=Microsoft YaHei",
      "-V", "CJKsansfont=Microsoft YaHei",
      "-V", "CJKmonofont=Microsoft YaHei"], "main.tex"),
):
    r = subprocess.run([PANDOC] + args, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=180)
    print("pandoc ->", out, "rc=", r.returncode, (r.stderr or "").strip()[:120])

r = subprocess.run([sys.executable, os.path.join(TOOLS, "html2pdf_edge.py"),
                    hp, os.path.join(FP, "paper.pdf")],
                   capture_output=True, text=True, encoding="utf-8",
                   errors="replace", timeout=240)
print("pdf:", (r.stdout or "").strip()[-200:])
