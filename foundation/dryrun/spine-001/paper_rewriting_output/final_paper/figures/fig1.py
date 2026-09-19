# -*- coding: utf-8 -*-
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

YEARS = [2021, 2022, 2023, 2024, 2025, 2026]
YEAR_N = [1, 3, 4, 6, 5, 5]

VENUE_LABELS = ['顶会（CVPR 正刊）', '顶会 Workshop', '期刊', '一般会议', 'arXiv 预印本', '高风险载体（SSRN/非索引刊）']
VENUE_N = [2, 2, 5, 6, 6, 3]

DISC_LABELS = ["\u53c2\u6570\u91cf\u6570\u503c", "\u7b97\u529b\u6570\u503c", "\u7cbe\u5ea6\u6570\u503c", "\u4e09\u9879\u4ff1\u5168", "\u4ec5\u5b9a\u6027\u63cf\u8ff0"]
DISC_N = [3, 1, 3, 0, 2]

fig, axes = plt.subplots(1, 3, figsize=(11.0, 4.3))

ax = axes[0]
ax.bar([str(y) for y in YEARS], YEAR_N, color="#4C72B0", width=0.62)
for i, v in enumerate(YEAR_N):
    ax.text(i, v + 0.1, str(v), ha="center", va="bottom", fontsize=10)
ax.set_title("(a) \u5e74\u4efd\u5206\u5e03\uff08n=24\uff09", fontsize=12)
ax.set_ylabel("\u6761\u76ee\u6570", fontsize=10)
ax.tick_params(axis="x", labelsize=10)
ax.tick_params(axis="y", labelsize=9)
ax.set_ylim(0, max(YEAR_N) + 1.2)
ax.spines[["top", "right"]].set_visible(False)

ax = axes[1]
ax.barh(VENUE_LABELS[::-1], VENUE_N[::-1], color="#55A868", height=0.6)
for i, v in enumerate(VENUE_N[::-1]):
    ax.text(v + 0.08, i, str(v), va="center", fontsize=10)
ax.set_title("(b) \u8f7d\u4f53\u7c7b\u578b\uff08n=24\uff09", fontsize=12)
ax.set_xlabel("\u6761\u76ee\u6570", fontsize=10)
ax.tick_params(axis="y", labelsize=9)
ax.set_xlim(0, max(VENUE_N) + 1.2)
ax.spines[["top", "right"]].set_visible(False)

ax = axes[2]
colors = ["#4C72B0", "#DD8452", "#C44E52", "#8C8C8C", "#8172B3"]
bars = ax.bar(DISC_LABELS, DISC_N, color=colors, width=0.6)
for b, v in zip(bars, DISC_N):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.08, str(v), ha="center", va="bottom", fontsize=10)
ax.set_title("(c) \u4e09\u7c7b\u6570\u503c\u7684\u62ab\u9732\u8986\u76d6\uff08n=6\uff0c\u53ef\u91cd\u53e0\uff09", fontsize=12)
ax.set_ylabel("\u6761\u76ee\u6570", fontsize=10)
ax.set_ylim(0, max(max(DISC_N), 3) + 0.9)
ax.tick_params(axis="x", labelsize=9)
ax.spines[["top", "right"]].set_visible(False)

fig.tight_layout()
out = "fig1_evidence_landscape.png"
fig.savefig(out, dpi=300, bbox_inches="tight", pad_inches=0.25, facecolor="white")
print("figure written:", out)
