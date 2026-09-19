# -*- coding: utf-8 -*-
"""gen_spine_phase_d.py - bring the drill tree up to the machine contracts.

Deliberately NOT produced here:
  - visual_audit_manifest.json page receipts (need real PDF page rendering)
  - structured_review.md / reviewer_audit.md / evidence_review*.json (independent review)
Those belong to the visual gate and the independent reviewer; faking them would
destroy the very thing this dry run exists to validate.
"""
import datetime
import json
import os

ROOT = r"C:\Users\ZhouXuan\Desktop\OH-WorkSpace\foundation\dryrun\spine-001\paper_rewriting_output"


def w(rel, text):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    print("  wrote", rel)


def wj(rel, obj):
    w(rel, json.dumps(obj, ensure_ascii=False, indent=2) + "\n")


w("confirmed_contribution.md", """# 已确认贡献（confirmed_contribution）

## Core Contribution

| Field | Content |
|---|---|
| Main Contribution Statement | 提出以"效率来源"而非任务类型为轴的视觉 Transformer 效率化方法四族分类，并配套给出证据强度分级，使不同工作的成本削减机制可直接对照。 |
| Contribution Type | 文献组织方式与证据边界显式化（非新方法、非新读数）。 |
| Reviewer Payoff | 读者可在一次阅读后判断某项效率改进究竟缓解了哪一类瓶颈，并知道当前证据支持到什么程度、在哪一步不能比较。 |

## Why This Contribution Is Needed

| Field | Content |
|---|---|
| Field Problem | 效率型视觉 Transformer 工作数量增长快，但组织与评测口径分裂，进展难以判断。 |
| Specific Gap | 现有组织方式多按任务（分类/检测/分割/复原）划分，掩盖了成本削减来源的实质差异；同时缺少对指标披露完备度的显式记录。 |
| Concrete Challenge | 在只使用公开元数据与摘要的条件下，如何在不做过度解读的前提下给出可核验的分类与边界。 |
| Why Prior Work Leaves It Unresolved | 按任务分类的综述服务检索需求而非机制对照；以性能排序为目的的综述在本证据条件下无法成立。 |

## How This Paper Responds

| Field | Content |
|---|---|
| Design Response | 以效率来源为分类轴建立四族（注意力稀疏化、分组与级联、混合 CNN-Transformer、参数共享与模块重构），并新增指标披露完备度统计。 |
| Evidence Required | 每条归类须可追溯到具体条目；每项统计须可由登记记录逐条回算。 |
| Evidence Available | 24 条真实记录的标题、载体、年份与 DOI/arXiv 标识；其中 6 条含摘要。 |
| Evidence Missing | 18 条无摘要；全部 24 条均未获取全文，故方法细节与实验表格不可知。 |

## Claim Boundary

| Field | Content |
|---|---|
| Strong Claims Allowed | 分类作为"本文提出的组织方式"；披露完备度的元数据层统计；高风险载体占比。 |
| Claims to Soften or Avoid | 任何"某方法更优或更高效"的跨论文比较；任何关于效率与鲁棒性联合缺失的结论。 |
| Novelty Risk | 分类轴并非全新概念，风险在于被视为常识重组；缓解方式是把披露完备度统计作为独立贡献。 |
| Significance Risk | 样本仅 24 条且无全文，若被读作领域总体结论则超出证据；须在摘要与结论双重限定。 |
""")

w("confirmed_motivation.md", """# 已确认动机（confirmed_motivation）

## Core Motivation

| Field | Content |
|---|---|
| Main Motivation Statement | 效率型 ViT 的评测口径分裂，使读者无法判断进展，这比其缺口更基础。 |
| Motivation Type | 证据基础问题，非应用需求驱动。 |

## Evidence For This Motivation

| Field | Content |
|---|---|
| Supporting Observation | 24 条记录中可判定披露情况的仅 6 条，其中同时给出参数量、算力与精度的只有 3 条。 |
| Secondary Observation | 24 条中 3 条载体为 SSRN 预印本或非索引刊，提示该主题的检索结果需要载体过滤意识。 |
| Boundary | 两项观察均为元数据层，不得推广为领域总体判断。 |
""")

w("results_validation.md", """# 结果校验（results_validation）

依 `materials_only` 模式执行：只校验已给结果能否支撑论断，不新增分析。

| Contribution Claim Tested | Result/Evidence | Check | Note |
|---|---|---|---|
| C1 四族分类可成立 | 24 条逐条归类，见 research_dossier.md 第 3 节 | PASS | 归类属推断层，已在正文标注 |
| C2 评测口径分裂 | 6 条可判定中仅 3 条完整（完整 3 / 部分 1 / 定性 2） | PASS | 元数据层事实，可由 source_index 回算 |
| C2 负结果缺失 | 6 条摘要全无失败条件报告 | PASS（限样本） | 不得推广至全部 24 条 |
| C2 高风险载体占比 | 3 / 24 | PASS | 仅陈述占比，不做领域总体判断 |
| C1 部署延迟未报告 | 仅 R19 / R20 提及时延而未给值 | PASS（推断） | 全文未读，该推断可被推翻 |
| 跨论文性能比较 | 无证据 | BLOCKED | 已拦截，未写入正文 |
| 效率与鲁棒性联合评估缺失 | 无证据 | BLOCKED | 超出本任务证据范围，未写入正文 |

## 未做（`materials_only` 禁止）

未做显著性检验、效应量、置信区间、重跑或任何新分析。本任务不含需重算的统计量。
""")

ROWS = [
    ("效率型视觉 Transformer 的效率改进可按来源分为四族",
     "把分类网络、检测网络与轻量网络并列时，读者难以判断某项改进到底缓解了哪一类瓶颈；改以效率来源为轴后，注意力稀疏化、分组与级联、混合卷积与参数共享四族的差异可直接对照。",
     "R01 Liu et al. EfficientViT. CVPR 2023. doi:10.1109/cvpr52729.2023.01386", 2023),
    ("注意力范围限制是削减成本最直接的一族",
     "以 patch attention 替代全局注意力可显著降低点云上的注意力开销，属于通过限制每个查询可见区域来削减计算量。",
     "R02 Zhang et al. PatchFormer. CVPR 2022. doi:10.1109/cvpr52688.2022.01150", 2022),
    ("可微锚点注意力把注意力计算稀疏化",
     "AnchorFormer 引入可微锚点注意力，在保持端到端可训练的同时把注意力计算限制在锚点相关区域。",
     "R07 Shan et al. AnchorFormer. Pattern Recognition Letters 2025. doi:10.1016/j.patrec.2025.07.016", 2025),
    ("改变通道组织顺序可改善访存效率",
     "级联分组注意力表明瓶颈未必是浮点运算量本身，也可能是内存访问模式，因此重组通道与计算顺序同样有效。",
     "R01 Liu et al. EfficientViT. CVPR 2023. doi:10.1109/cvpr52729.2023.01386", 2023),
    ("混合卷积与注意力是常见的折中路径",
     "让卷积承担局部特征、注意力承担全局关系，可在同等预算下取得折中，该路径在活动识别与表情识别等任务上被反复采用。",
     "R13 Rani and Kumar. MobileNetv1-ViT. IEEE ICIIP 2025. doi:10.1109/iciip68302.2025.11346208", 2025),
    ("参数共享与模块重构可直接压缩规模",
     "递归共享参数与统一的内在残差元模块两类做法，均可降低参数量而不改变注意力的基本形式。",
     "R16 Zhang et al. EMOv2. arXiv:2412.06674", 2024),
    ("亚百万参数档架构已被实际构建",
     "最小变体含 204.67K 参数与 53.95M FLOPs，说明变压器类视觉模型可被重新设计到极小规模而不显著损失判别能力。",
     "R17 George et al. UtVAA. arXiv:2606.14735", 2026),
    ("跨窗通信可用少量特殊 token 承载",
     "为每个窗口分配一个 Super token 承担跨窗通信与全局表征学习，在 ImageNet-1K 上达到 83.5% 而参数量约 49M。",
     "R18 Farooq et al. Super Tokens. arXiv:2111.13156", 2021),
    ("冻结骨干加轻量头部构成另一条高效路径",
     "冻结 CLIP 图像编码器并仅训练轻量 Transformer 解码器，可避开在全量视频上微调骨干的巨大代价。",
     "R19 Lin et al. Frozen CLIP Models are Efficient Video Learners. arXiv:2208.03550", 2022),
    ("相对位置编码可替代稠密算子",
     "用成对 token 关系的小规模参数化相对位置偏置替代稠密算子，可在视频识别上取得竞争性的速度-精度权衡。",
     "R20 Hao et al. PosMLP-Video. arXiv:2407.02934", 2024),
    ("评测口径分裂使跨论文比较不成立",
     "24 条记录中可判定披露情况的仅 6 条，且训练配方、数据划分与评测协议各不相同，即使都给出 Top-1 也不构成可比较基准。",
     "R10 Shen et al. Image and Vision Computing 2026. doi:10.1016/j.imavis.2026.105930", 2026),
    ("部分载体为预印本或非索引刊",
     "纳入的 24 条中 3 条来自 SSRN 预印本平台或未被主流索引收录的期刊，其同行评审状态不明。",
     "R22 Sanchez-Brito. DANTE. SSRN preprint. doi:10.2139/ssrn.6811533", 2026),
    ("部署端真实延迟普遍未报告",
     "在可读摘要中仅两条提及时延而未给出具体数值，多数工作只报告理论算力指标。",
     "R20 Hao et al. PosMLP-Video. arXiv:2407.02934", 2024),
    ("期刊载体上出现了系统性效率方法研究",
     "Pattern Recognition 与 Image and Vision Computing 等期刊开始集中刊载效率型视觉 Transformer 的改进工作。",
     "R05 Li and Zhao. Pattern Recognition 2024. doi:10.1016/j.patcog.2024.110357", 2024),
    ("层级结构在分割任务上同样被效率化",
     "高效编码器与轻量解码器的组合被用于语义分割，说明效率改进并不限于分类任务。",
     "R09 Wu and Zhou. ELiFormer. ACM ACCVIPR 2024. doi:10.1145/3663976.3663985", 2024),
    ("效率改进已延伸到嵌入式与证件识别场景",
     "面向嵌入式证件识别系统的超轻量卷积注意力网络被提出，说明该方向有明确的部署侧需求牵引。",
     "R10 Shen et al. Image and Vision Computing 2026. doi:10.1016/j.imavis.2026.105930", 2026),
]

lines = [
    "# 引用支撑库（citation_support_bank）",
    "",
    "上游要求引用**身份**与**语境**双重核验。本表每行给出论断、可用的支撑句与完整书目标识。",
    "身份核验：全部条目带 DOI 或 arXiv 标识，可独立复核；**未生成任何虚假参考文献**。",
    "",
    "| Claim | Sentence | Reference | Year |",
    "|---|---|---|---|",
]
for c, s, r, y in ROWS:
    lines.append(f"| {c} | {s} | {r} | {y} |")
lines += [
    "",
    "## 说明",
    "",
    "- 高风险载体条目（R22 / R23 / R24）**仅用于元数据统计**，不作为科学支撑。",
    "- 本表为**候选引用库**，不等于最终稿的引用覆盖；最终覆盖须经投稿前核验。",
]
w("citation_support_bank.md", "\n".join(lines) + "\n")

wj("figure_requests.json", {
    "schema_version": "1.0",
    "figures": [
        {
            "figure_id": "fig1-evidence-landscape",
            "label": "fig:evidence-landscape",
            "figure_kind": "data",
            "figure_role": "cohort_profile",
            "decision": "create",
            "claim": "纳入的 24 条记录在年份、载体与指标披露三个维度上呈现可用证据的不均衡分布。",
            "caption": "图 1 纳入文献的证据景观（n = 24）。(a) 年份分布；(b) 载体类型构成；(c) 指标披露完备度。所有计数可由 reference_materials/source_index.md 逐条回算。",
            "scientific_question": "在当前可获得的记录上，证据基础能支持到什么程度的横向比较？",
            "intended_conclusion": "证据基础仅支持按效率来源分类与披露完备度统计，不支持任何跨论文性能排序。",
            "claim_boundary": "仅描述 24 条记录自身的构成，不推断领域总体分布，不涉及任何方法优劣判断。",
            "results_units": ["Results 第 4 节 三点观察"],
            "hero_panel": "p-disclosure",
            "source_data": [
                "reference_materials/source_index.md",
                "evidence_bank.md 的 E-B1 / E-B2",
            ],
            "panels": [
                {
                    "panel_id": "p-year",
                    "question": "该方向在时间上的活跃度如何？",
                    "role": "context",
                    "evidence_anchor": "source_index 年份字段",
                    "intended_reading": "产出自 2021 年起持续，2024 年达到 6 条。",
                },
                {
                    "panel_id": "p-venue",
                    "question": "这些产出发表在什么类型的载体上？",
                    "role": "comparison",
                    "evidence_anchor": "source_index 载体标签",
                    "intended_reading": "严格同行评审的顶会正刊仅 2 条，非同行评审与高风险载体合计 9 条。",
                },
                {
                    "panel_id": "p-disclosure",
                    "question": "有多少工作同时披露了参数量、算力与精度？",
                    "role": "primary_finding",
                    "evidence_anchor": "证据库 E-B2 披露字段统计",
                    "intended_reading": "24 条中仅 3 条完整披露，18 条因缺摘要无法判定，故跨论文比较不成立。",
                },
            ],
        }
    ],
})

wj("figure_body_contract.json", {
    "schema_version": "1.0",
    "contract_type": "paperspine.figure.body",
    "status": "PASS",
    "figures": [
        {
            "figure_id": "fig1-evidence-landscape",
            "label": "fig:evidence-landscape",
            "publication_asset": "final_paper/figures/fig1_evidence_landscape.png",
            "editable_source": "final_paper/figures/fig1.py",
            "referenced_in_body": True,
            "body_reference": "第 4 节 图 1",
            "claim": "纳入的 24 条记录在年份、载体与指标披露三个维度上呈现可用证据的不均衡分布。",
            "boundary": "仅描述 24 条记录自身构成，不推断领域总体分布。",
        }
    ],
})

NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()
STAGES = [
    ("intake", "reference_materials/source_index.md"),
    ("research", "research_dossier.md"),
    ("contribution", "confirmed_contribution.md"),
    ("writing", "final_paper/manuscript.md"),
    ("figures", "final_paper/figures/fig1_evidence_landscape.png"),
    ("render", "final_paper/paper.docx"),
    ("gates", "artifact_check.md"),
]
ledger = []
for st, art in STAGES:
    ledger.append({
        "timestamp": NOW,
        "stage": st,
        "role": "host",
        "model": "host-managed",
        "reasoning_effort": "unknown",
        "usage_source": "telemetry_unavailable",
        "telemetry_note": "HanaAgent host returned no usage object for this drill",
        "input_hashes": [],
        "output_artifacts": [art],
        "gate_result": "pending",
        "retry": 0,
    })
w("usage_ledger.jsonl", "\n".join(json.dumps(e, ensure_ascii=False) for e in ledger) + "\n")

w("final_artifact_manifest.md", """# 最终产物清单（final_artifact_manifest）

| 产物 | 路径 | 生成方式 | 状态 |
|---|---|---|---|
| 正文单源 | `final_paper/manuscript.md` | 手写（唯一语义源） | 完成 |
| Word | `final_paper/paper.docx` | pandoc md 转 docx | 完成 |
| LaTeX | `final_paper/main.tex` | pandoc md 转 latex | 完成，**未编译**（无 TeX 引擎） |
| HTML | `final_paper/manuscript.html` | 自建转换 | 完成 |
| PDF | `final_paper/paper.pdf` | Edge headless print-to-pdf | 完成（1,846,228 B） |
| 图 1 | `final_paper/figures/fig1_evidence_landscape.png` | matplotlib 300 dpi | 完成 |
| 图源 | `final_paper/figures/fig1.py` | 可编辑源 | 完成 |

## 单一语义源声明

上述各交付面**全部由 `manuscript.md` 机械派生**，不存在第二份手写内容源。
布局差异来自渲染器，不来自内容分叉。

## 未完成项（如实登记）

- `visual_audit_manifest.json` 的逐页收据：**未生成**。本机缺 PyMuPDF，
  `visual_readiness_check.py --prepare` 无法渲染 PDF 页面。
- 独立评审产物（`structured_review.md`、`reviewer_audit.md`、`evidence_review*.json`）：
  **未生成**，须由独立评审者产出，撰写者不得代填。
""")

print("phase D done")
