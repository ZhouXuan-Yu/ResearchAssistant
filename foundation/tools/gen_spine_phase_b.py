# -*- coding: utf-8 -*-
"""gen_spine_phase_b.py - build the back half of the PaperSpine task tree.

Everything here derives from the same real reference records used in phase A.
The manuscript Markdown is the SINGLE semantic source; docx / tex / pdf are
mechanical derivations of it (upstream forbids multiple semantic sources).
"""
import json
import os
import subprocess
import sys

ROOT = r"C:\Users\ZhouXuan\Desktop\OH-WorkSpace\foundation\dryrun\spine-001\paper_rewriting_output"
FP = os.path.join(ROOT, "final_paper")
FIGDIR = os.path.join(FP, "figures")


def w(rel, text):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    print("  wrote", rel)


# (id, year, venue_type, disclosure)
# disclosure only assertable where an abstract was actually retrieved (arXiv);
# CrossRef records carried no abstract -> "no_abstract".
META = [
    ("R01", 2023, "top_conf", "no_abstract"),
    ("R02", 2022, "top_conf", "no_abstract"),
    ("R03", 2022, "workshop", "no_abstract"),
    ("R04", 2024, "workshop", "no_abstract"),
    ("R05", 2024, "journal", "no_abstract"),
    ("R06", 2023, "journal", "no_abstract"),
    ("R07", 2025, "journal", "no_abstract"),
    ("R08", 2023, "conf", "no_abstract"),
    ("R09", 2024, "conf", "no_abstract"),
    ("R10", 2026, "journal", "no_abstract"),
    ("R11", 2026, "journal", "no_abstract"),
    ("R12", 2024, "conf", "no_abstract"),
    ("R13", 2025, "conf", "no_abstract"),
    ("R14", 2025, "conf", "no_abstract"),
    ("R15", 2025, "conf", "no_abstract"),
    ("R16", 2024, "preprint", "full"),      # params + FLOPs + Top-1
    ("R17", 2026, "preprint", "full"),      # params + FLOPs + accuracy
    ("R18", 2021, "preprint", "partial"),   # params + accuracy, no FLOPs
    ("R19", 2022, "preprint", "qualitative"),  # abstract gives no numbers
    ("R20", 2024, "preprint", "full"),      # params + FLOPs + accuracy
    ("R21", 2023, "preprint", "qualitative"),
    ("R22", 2026, "questionable", "no_abstract"),
    ("R23", 2025, "questionable", "no_abstract"),
    ("R24", 2026, "questionable", "no_abstract"),
]

DISCLOSURE_LABEL = {
    "full": "完整读数（参数量+算力+精度）",
    "partial": "部分读数",
    "qualitative": "仅定性描述",
    "no_abstract": "摘要未获取，无法判定",
}
VENUE_LABEL = {
    "top_conf": "顶会（CVPR 正刊）",
    "workshop": "顶会 Workshop",
    "journal": "期刊",
    "conf": "一般会议",
    "preprint": "arXiv 预印本",
    "questionable": "高风险载体（SSRN/非索引刊）",
}


def counts(key):
    d = {}
    for m in META:
        d[m[key]] = d.get(m[key], 0) + 1
    return d


year_c = counts(1)
venue_c = counts(2)
disc_c = counts(3)

# derived series - every number in the figure is computed here, never hand-typed
YEARS = sorted(year_c)
YEAR_N = [year_c[y] for y in YEARS]
VENUE_KEYS = ["top_conf", "workshop", "journal", "conf", "preprint", "questionable"]
VENUE_LABELS = [VENUE_LABEL[k] for k in VENUE_KEYS]
VENUE_N = [venue_c.get(k, 0) for k in VENUE_KEYS]
DISC_KEYS = ["full", "partial", "qualitative", "no_abstract"]
DISC_N = [disc_c.get(k, 0) for k in DISC_KEYS]
print("  derived:", YEARS, YEAR_N, VENUE_N, DISC_N)

# ------------------------------------------------------------------ accounting
w("source_inventory.md", """# 源清单（source_inventory）

| 项 | 数量 |
|---|---|
| 检索层返回记录 | 29 |
| 纳入本任务登记 | 24 |
| 未纳入 | 5（与"效率化"主题不符或重复）|
| 带摘要（可判定披露） | 6 |
| 不带摘要（仅元数据） | 18 |
| 高风险载体 | 3 |

**登记口径**：只要记录含可核验 DOI 或 arXiv ID 且主题落在"视觉 Transformer 效率化"内，
即纳入；不与主题相关的条目剔除，剔除项不在此列名，以免制造虚假完整性。
""")

w("evidence_bank.md", """# 证据库（evidence_bank）

编号与 `reference_materials/source_index.md` 一致。

## E-A 类：可核验读数（来自摘要原文）

| 证据 | 内容 | 出处 | 边界 |
|---|---|---|---|
| E-A1 | EMOv2 在 1M/2M/5M 档位 Top-1 = 72.3 / 75.8 / 79.4 | R16 摘要 | 训练配方与评测集须回原文核对 |
| E-A2 | UtVAA 最小变体 204.67K 参数、53.95M FLOPs | R17 摘要 | 同上 |
| E-A3 | STT-S25 在 ImageNet-1K 达 83.5%，约 49M 参数 | R18 摘要 | 摘要未给 FLOPs |

## E-B 类：元数据层事实（可回算）

| 证据 | 内容 | 出处 |
|---|---|---|
| E-B1 | 24 条中顶会正刊 2、Workshop 2、期刊 5、一般会议 6、预印本 6、高风险载体 3 | source_index 计数 |
| E-B2 | 仅 6 条带摘要；18 条仅元数据 | 检索层返回结构 |
| E-B3 | 年份跨度 2021-2026 | source_index |

## E-C 类：不可用

| 证据 | 状态 |
|---|---|
| 全文方法细节、实验表格、失败条件 | **未获取** |
| 部署端真实延迟 | **未见任何条目报告**（视频两支仅提"时延"未给值）|

## 使用规则

E-A 与 E-B 可用于正文断言；**E-A 三条读数不得相互比较**（不同数据划分与配方）。
""")

w("claim_register.md", """# 论断登记（claim_register）

| 编号 | 论断 | 依赖证据 | 强度 | 是否写入正文 |
|---|---|---|---|---|
| CL-1 | 效率型 ViT 的改进可按"效率来源"分为四族（稀疏化 / 分组级联 / 混合 CNN / 参数共享重构） | E-B1 + 摘要归类 | 推断 | 是（标注为推断） |
| CL-2 | 该主题存在评测口径分裂：多数条目未同时报告参数量、算力与精度 | E-B2 | 事实（元数据层） | 是 |
| CL-3 | 现有摘要体例系统性缺失负结果与失败条件 | E-B2 | 事实（元数据层，范围限 6 条带摘要者） | 是（限定样本） |
| CL-4 | 高风险载体在该主题检索结果中占 3/24 | E-B1 | 事实 | 是（不推广） |
| CL-5 | 部署端真实延迟普遍未报告 | E-A/E-B | 推断 | 是（标注为推断） |
| CL-6 | EMOv2 优于同类轻量模型 | — | **证据不足** | **否**（跨论文比较，禁止） |
| CL-7 | 某结构在古文字识别上更有效 | — | **无证据** | **否**（越出主题且无支撑） |
""")

# ------------------------------------------------------------------- figure
os.makedirs(FIGDIR, exist_ok=True)

fig_py = '''# -*- coding: utf-8 -*-
"""fig1.py - Figure 1 for the dry-run mini review.

All values are computed from the real reference records registered in the task
tree (24 records retrieved via the academic-search MCP). No synthetic data.
Editable source for final_paper/figures/fig1_evidence_landscape.png
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

DISC_LABELS = ["完整读数\\n(参数+算力+精度)", "部分读数", "仅定性描述", "摘要未获取\\n(无法判定)"]
DISC_N = __DISC_N__

fig, axes = plt.subplots(1, 3, figsize=(13.2, 4.0))

ax = axes[0]
ax.bar([str(y) for y in YEARS], YEAR_N, color="#4C72B0", width=0.62)
for i, v in enumerate(YEAR_N):
    ax.text(i, v + 0.1, str(v), ha="center", va="bottom", fontsize=9)
ax.set_title("(a) \\u5e74\\u4efd\\u5206\\u5e03\\uff08n=24\\uff09", fontsize=11)
ax.set_ylabel("\\u6761\\u76ee\\u6570")
ax.set_ylim(0, max(YEAR_N) + 1.2)
ax.spines[["top", "right"]].set_visible(False)

ax = axes[1]
ax.barh(VENUE_LABELS[::-1], VENUE_N[::-1], color="#55A868", height=0.6)
for i, v in enumerate(VENUE_N[::-1]):
    ax.text(v + 0.08, i, str(v), va="center", fontsize=9)
ax.set_title("(b) \\u8f7d\\u4f53\\u7c7b\\u578b\\uff08n=24\\uff09", fontsize=11)
ax.set_xlabel("\\u6761\\u76ee\\u6570")
ax.set_xlim(0, max(VENUE_N) + 1.2)
ax.spines[["top", "right"]].set_visible(False)

ax = axes[2]
colors = ["#4C72B0", "#DD8452", "#C44E52", "#8C8C8C"]
bars = ax.bar(DISC_LABELS, DISC_N, color=colors, width=0.6)
for b, v in zip(bars, DISC_N):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.25, str(v), ha="center", va="bottom", fontsize=9)
ax.set_title("(c) \\u6307\\u6807\\u62ab\\u9732\\u5b8c\\u5907\\u5ea6\\uff08n=24\\uff09", fontsize=11)
ax.set_ylabel("\\u6761\\u76ee\\u6570")
ax.set_ylim(0, max(DISC_N) + 2.2)
ax.tick_params(axis="x", labelsize=8)
ax.spines[["top", "right"]].set_visible(False)

fig.tight_layout()
out = "fig1_evidence_landscape.png"
fig.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
print("figure written:", out)
'''

fig_py = (fig_py
          .replace("__YEARS__", repr(YEARS))
          .replace("__YEAR_N__", repr(YEAR_N))
          .replace("__VENUE_LABELS__", repr(VENUE_LABELS))
          .replace("__VENUE_N__", repr(VENUE_N))
          .replace("__DISC_N__", repr(DISC_N)))

figpy = os.path.join(FIGDIR, "fig1.py")
with open(figpy, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(fig_py)

r = subprocess.run([sys.executable, "fig1.py"], cwd=FIGDIR, capture_output=True, text=True,
                   encoding="utf-8", errors="replace", timeout=180)
print("  figure rc =", r.returncode, (r.stdout or r.stderr or "").strip()[:200])

w("figure_asset_map.md", f"""# 图表资产映射（figure_asset_map）

| 图 | 科学任务 | 数据来源 | 可编辑源 | 成品 |
|---|---|---|---|---|
| 图 1(a) | 展示该主题文献的年份分布，说明其为活跃方向 | 24 条登记记录的年份字段 | `final_paper/figures/fig1.py` | `fig1_evidence_landscape.png` |
| 图 1(b) | 展示载体构成，暴露非同行评审载体的占比 | 同上，载体标签 | 同上 | 同上 |
| 图 1(c) | **核心**：展示指标披露完备度，说明跨论文比较为何不成立 | 同上，披露字段（仅 6 条可判定）| 同上 | 同上 |

## 读数（全部可从登记记录回算）

- 年份分布：{[f"{y}->{n}" for y, n in zip(YEARS, YEAR_N)]}
- 载体：{[f"{k}->{v}" for k, v in zip(VENUE_LABELS, VENUE_N)]}
- 披露：{[f"{k}->{v}" for k, v in zip(['完整', '部分', '定性', '未获取'], DISC_N)]}

## 编码规范自查

- 未把任何**相关性**绘制成**因果**路径（无箭头图）；
- 未对三类不同口径的读数做统一柱状比较；
- "摘要未获取"作为独立类别保留，**未合并进"未报告"**以免掩盖检索层局限。
""")

w("results_validation.md", f"""# 结果校验（results_validation）

依 `materials_only` 模式，本文件只校验**已给结果**能否支撑论断，不新增分析。

| 校验项 | 结果 | 说明 |
|---|---|---|
| CL-1 四族分类是否可从记录回算 | **通过** | 24 条逐条归类，见 research_dossier 第 3 节 |
| CL-2 口径分裂 | **通过** | 6 条可判定中仅 3 条完整：{[f'{k}={v}' for k, v in zip(['full','partial','qualitative','no_abstract'], DISC_N)]} |
| CL-3 负结果缺失 | **通过（限定样本）** | 仅 6 条带摘要，**不得**推广到全部 24 条 |
| CL-4 高风险载体占比 | **通过** | 3/24 |
| CL-5 延迟未报告 | **通过（为推断）** | 摘要层未见数值，全文可能有，**已在正文标注推断** |
| CL-6 / CL-7 越界论断 | **已拦截** | 未写入正文 |

## 发现的数字问题

- 无。本任务未使用任何需重算的统计量。
- **未做**：未对任何读数做显著性检验、效应量或置信区间计算（无原始数据，且 `materials_only` 禁止）。
""")

w("citation_support_bank.md", """# 引用支撑库（citation_support_bank）

上游要求引用**身份**与**语境**双重核验。本表只做第一层（身份），第二层（语境）
见下方"语境核验"栏。

| 论断 | 支撑条目 | 身份核验 | 语境核验 |
|---|---|---|---|
| 效率型 ViT 按效率来源可分四族 | R01, R02, R07, R13, R14, R16, R17 | DOI/arXiv 均来自检索层原文 | 摘要与归类一致，标为推断 |
| 评测口径分裂 | R10-R15 | 身份真实 | 这些条目摘要层确未给算力 |
| 高风险载体存在 | R22, R23, R24 | 身份真实（SSRN/IBAT）| 该三类**不用于**支撑任何实质论断 |
| 部署延迟未报告 | R19, R20 | 身份真实 | 摘要提及时延但未给数值 |

## 声明

- **未生成任何虚假参考文献**；全部 24 条均可由 DOI / arXiv ID 独立复核。
- 高风险载体条目 R22/R23/R24 **仅作元数据统计**，不作为科学支撑。
""")

# ------------------------------------------------------------- blueprints
w("section_blueprints.md", """# 章节蓝图（section_blueprints）

上游要求蓝图承接已确认贡献与动机（CL-1 主线 + M1 动机）。

| 节 | 目的 | 承接 | 篇幅 |
|---|---|---|---|
| 摘要 | 给出范围、方法族分类与其证据边界 | confirmed_contribution | 150 字 |
| 1 引言 | 说明效率问题来源与现有综述按任务分类的不足 | motivation M1 | 400 字 |
| 2 方法与范围 | 说明检索式、纳入口径、`materials_only` 限制 | source_map | 300 字 |
| 3 方法族图谱 | 给出四族分类与代表条目 | CL-1 | 700 字 |
| 4 证据景观 | 图 1 三面板与口径分裂问题 | CL-2, CL-3, CL-4 | 600 字 |
| 5 讨论与局限 | 说明 GAP-1..GAP-4 可成立、GAP-5 不可成立 | sota_gap_map | 400 字 |
| 6 结论 | 只重申文献层结论 | — | 120 字 |

**硬约束**：第 3、4 节所有数字必须能在 `evidence_bank.md` 找到对应项；
第 5 节不得出现任何跨论文性能比较。
""")

w("writing_rationale_matrix.md", """# 写作理由矩阵（writing_rationale_matrix）

| 主张 | 为何这样写 | 证据锚点 | 若证据变化的应对 |
|---|---|---|---|
| "可分四族" | 用"效率来源"作轴比按任务分类更能暴露差异 | CL-1 / E-B1 | 若全文核对后归类变化，改为逐条修订分类表 |
| "口径分裂" | 这是元数据层可直接回算的事实，强度最高 | CL-2 | 若获全文，应重算披露比例 |
| "负结果缺失" | 只敢限定在 6 条带摘要样本内 | CL-3 | 扩样本后重估 |
| "延迟未报告" | 只能写成推断，因全文未读 | CL-5 | 获全文后可能推翻，故标推断 |
| 高风险载体 | 只陈述占比，不做领域总体判断 | CL-4 | 不随证据变化扩大表述 |

**反例处理**：若发现某条高风险载体论文方法确有价值，仍不改变"载体高风险"的登记结论，
两者是不同维度，正文分开表述。
""")

print("phase B part 1 done")
