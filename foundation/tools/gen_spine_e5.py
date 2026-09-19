# -*- coding: utf-8 -*-
"""gen_spine_e5.py - rebuild the disclosure evidence trail and figure 1(c).

Root cause of the CRITICAL finding: figure 1(c) classified disclosure completeness
by hand, with no itemised evidence trail, and its "full = params + FLOPs + accuracy"
label contradicted evidence_bank E-A (no record reports all three). Fix: re-read the
six abstract-bearing records (arXiv abstracts re-fetched 2026-09-19), itemise what each
actually reports, rebuild E-A, and re-plot panel (c) from the itemised fields.
"""
import io
import os
import subprocess
import sys

ROOT = r"C:\Users\ZhouXuan\Desktop\OH-WorkSpace\foundation\dryrun\spine-001\paper_rewriting_output"
FIGDIR = os.path.join(ROOT, "final_paper", "figures")

# rid: (params numeric?, flops numeric?, accuracy numeric?, what the abstract gives)
ABSTRACT_FACTS = [
    ("R16", True, False, True,
     "1M/2M/5M 档位 Top-1 = 72.3 / 75.8 / 79.4，稳健配方下达 82.9；参数量以 1M/2M/5M 量级表述，未给 FLOPs 数值"),
    ("R17", True, True, False,
     "最小变体 204.67K 参数、53.95M FLOPs；精度仅表述为 competitive accuracy，未给数值"),
    ("R18", True, False, True,
     "ImageNet-1K 83.5% 精度、约 49M 参数；给出吞吐量而非 FLOPs"),
    ("R19", False, False, False,
     "摘要未给任何参数量、算力或精度数值，仅描述冻结骨干加轻量解码器的框架"),
    ("R20", False, False, True,
     "Something-Something V1/V2 top-1 = 59.0% / 70.3%，Kinetics-400 = 82.1%；仅称参数与 FLOPs 更少，未给数值"),
    ("R21", False, False, False,
     "摘要未给任何数值，仅描述三级架构与分类器共识机制"),
]

n_params = sum(1 for r in ABSTRACT_FACTS if r[1])
n_flops = sum(1 for r in ABSTRACT_FACTS if r[2])
n_acc = sum(1 for r in ABSTRACT_FACTS if r[3])
n_all = sum(1 for r in ABSTRACT_FACTS if r[1] and r[2] and r[3])
n_qual = sum(1 for r in ABSTRACT_FACTS if not (r[1] or r[2] or r[3]))

# ---------------------------------------------------------------- evidence_bank
rows = []
for rid, p, f, a, note in ABSTRACT_FACTS:
    rows.append(f"| E-A{int(rid[1:]) - 15} | {rid} | 参数量 {'有' if p else '无'} | 算力 {'有' if f else '无'} | 精度 {'有' if a else '无'} | {note} |")

bank = f"""# 证据库（evidence_bank）

编号与 `reference_materials/source_index.md` 一致。

## E-A 类：带摘要记录的逐条披露台账

检索层共返回 {len(ABSTRACT_FACTS)} 条带摘要记录（其余 18 条仅元数据，其披露状态**不可知**）。
下表逐条列出每条摘要实际给出的数值字段，图 1(c) 与该台账同源。

| 证据 | 记录 | 参数量 | 算力 | 精度 | 摘要实际给出 |
|---|---|---|---|---|---|
{os.linesep.join(rows)}

**汇总**：给出参数量数值 {n_params} 条，给出算力数值 {n_flops} 条，给出精度数值 {n_acc} 条；
**同时给出三项者 {n_all} 条**；未给任何数值者 {n_qual} 条。

> 使用规则：上表各条来自不同数据划分与训练配方，**不得相互比较**，也不得据此作"谁更高效"的判断。

## E-B 类：元数据层事实（可回算）

| 证据 | 内容 | 出处 |
|---|---|---|
| E-B1 | 24 条中顶会正刊 2、Workshop 2、期刊 5、一般会议 6、arXiv 预印本 6、高风险载体 3 | source_index.md 逐条计数 |
| E-B2 | 带摘要 6 条；仅元数据 18 条（6+18=24） | 检索层返回结构 |
| E-B3 | 年份跨度 2021-2026；分布 2021:1、2022:3、2023:4、2024:6、2025:5、2026:5 | source_index.md 逐条计数 |
| E-B4 | 披露字段覆盖：参数量 {n_params}、算力 {n_flops}、精度 {n_acc}、三项俱全 {n_all}、仅定性 {n_qual}（样本为 6 条带摘要记录） | E-A 台账汇总 |

## E-C 类：不可用

| 证据 | 状态 |
|---|---|
| 全文方法细节、实验表格、失败条件 | **未获取** |
| 部署端真实延迟 | **未在可读摘要中给出数值**（视频两支仅表述为更少参数与算力） |

## 使用规则

E-A 与 E-B 可用于正文断言；**E-A 各条读数不得相互比较**（不同数据划分与配方）。
"""
with io.open(os.path.join(ROOT, "evidence_bank.md"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write(bank)
print("rewrote evidence_bank.md; params/flops/acc/all/qual =", n_params, n_flops, n_acc, n_all, n_qual)

# -------------------------------------------------------------------- figure 1
fig_py = '''# -*- coding: utf-8 -*-
"""fig1.py - Figure 1 for the dry-run mini review.

All values are computed from the real reference records registered in the task
tree (24 records retrieved via the academic-search MCP). No synthetic data.
Panel (c) is driven by the itemised disclosure ledger in evidence_bank.md.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Noto Sans SC", "Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

YEARS = __YEARS__
YEAR_N = __YEAR_N__

VENUE_LABELS = __VENUE_LABELS__
VENUE_N = __VENUE_N__

DISC_LABELS = ["\\u53c2\\u6570\\u91cf\\u6570\\u503c", "\\u7b97\\u529b\\u6570\\u503c", "\\u7cbe\\u5ea6\\u6570\\u503c", "\\u4e09\\u9879\\u4ff1\\u5168", "\\u4ec5\\u5b9a\\u6027\\u63cf\\u8ff0"]
DISC_N = __DISC_N__

fig, axes = plt.subplots(1, 3, figsize=(11.0, 4.3))

ax = axes[0]
ax.bar([str(y) for y in YEARS], YEAR_N, color="#4C72B0", width=0.62)
for i, v in enumerate(YEAR_N):
    ax.text(i, v + 0.1, str(v), ha="center", va="bottom", fontsize=10)
ax.set_title("(a) \\u5e74\\u4efd\\u5206\\u5e03\\uff08n=24\\uff09", fontsize=12)
ax.set_ylabel("\\u6761\\u76ee\\u6570", fontsize=10)
ax.tick_params(axis="x", labelsize=10)
ax.tick_params(axis="y", labelsize=9)
ax.set_ylim(0, max(YEAR_N) + 1.2)
ax.spines[["top", "right"]].set_visible(False)

ax = axes[1]
ax.barh(VENUE_LABELS[::-1], VENUE_N[::-1], color="#55A868", height=0.6)
for i, v in enumerate(VENUE_N[::-1]):
    ax.text(v + 0.08, i, str(v), va="center", fontsize=10)
ax.set_title("(b) \\u8f7d\\u4f53\\u7c7b\\u578b\\uff08n=24\\uff09", fontsize=12)
ax.set_xlabel("\\u6761\\u76ee\\u6570", fontsize=10)
ax.tick_params(axis="y", labelsize=9)
ax.set_xlim(0, max(VENUE_N) + 1.2)
ax.spines[["top", "right"]].set_visible(False)

ax = axes[2]
colors = ["#4C72B0", "#DD8452", "#C44E52", "#8C8C8C", "#8172B3"]
bars = ax.bar(DISC_LABELS, DISC_N, color=colors, width=0.6)
for b, v in zip(bars, DISC_N):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.08, str(v), ha="center", va="bottom", fontsize=10)
ax.set_title("(c) \\u4e09\\u7c7b\\u6570\\u503c\\u7684\\u62ab\\u9732\\u8986\\u76d6\\uff08n=6\\uff0c\\u53ef\\u91cd\\u53e0\\uff09", fontsize=12)
ax.set_ylabel("\\u6761\\u76ee\\u6570", fontsize=10)
ax.set_ylim(0, max(max(DISC_N), 3) + 0.9)
ax.tick_params(axis="x", labelsize=9)
ax.spines[["top", "right"]].set_visible(False)

fig.tight_layout()
out = "fig1_evidence_landscape.png"
fig.savefig(out, dpi=300, bbox_inches="tight", pad_inches=0.25, facecolor="white")
print("figure written:", out)
'''

fig_py = (fig_py
          .replace("__YEARS__", "[2021, 2022, 2023, 2024, 2025, 2026]")
          .replace("__YEAR_N__", "[1, 3, 4, 6, 5, 5]")
          .replace("__VENUE_LABELS__", repr(['顶会（CVPR 正刊）', '顶会 Workshop', '期刊', '一般会议', 'arXiv 预印本', '高风险载体（SSRN/非索引刊）']))
          .replace("__VENUE_N__", "[2, 2, 5, 6, 6, 3]")
          .replace("__DISC_N__", repr([n_params, n_flops, n_acc, n_all, n_qual])))

with io.open(os.path.join(FIGDIR, "fig1.py"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write(fig_py)

r = subprocess.run([sys.executable, "fig1.py"], cwd=FIGDIR, capture_output=True, text=True,
                   encoding="utf-8", errors="replace", timeout=180)
print("figure rc =", r.returncode, (r.stdout or r.stderr or "").strip()[:200])
