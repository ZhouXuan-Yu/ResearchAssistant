# -*- coding: utf-8 -*-
"""gen_spine_phase_a.py - build the front half of the PaperSpine task tree.

Dry-run subject: efficient Vision Transformer methods (2020-2026), a generic
public CV topic. NOT the user's own research. All references are real records
retrieved through the academic-search MCP (CrossRef / arXiv).
"""
import json
import os

ROOT = r"C:\Users\ZhouXuan\Desktop\OH-WorkSpace\foundation\dryrun\spine-001\paper_rewriting_output"
REF = os.path.join(ROOT, "reference_materials")


def w(rel, text):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    print("  wrote", rel, len(text), "chars")


# ---------------------------------------------------------------- references
REFS = [
    ("R01", "EfficientViT: Memory Efficient Vision Transformer with Cascaded Group Attention",
     "Liu, X.; Peng, H.; Zheng, N.; Yang, Y.; Hu, H. et al.", 2023,
     "IEEE/CVF CVPR 2023", "10.1109/cvpr52729.2023.01386", 863, "venue:top-conf",
     "级联分组注意力降低内存访问开销，是效率型 ViT 的代表性设计。"),
    ("R02", "PatchFormer: An Efficient Point Transformer with Patch Attention",
     "Zhang, C.; Wan, H.; Shen, X.; Wu, Z.", 2022,
     "IEEE/CVF CVPR 2022", "10.1109/cvpr52688.2022.01150", 84, "venue:top-conf",
     "以 patch attention 替代全局注意力，面向点云的高效注意力。"),
    ("R03", "DRT: A Lightweight Single Image Deraining Recursive Transformer",
     "Liang, Y.; Anwar, S.; Liu, Y.", 2022,
     "IEEE/CVF CVPRW 2022", "10.1109/cvprw56347.2022.00074", 78, "venue:workshop",
     "递归共享参数换取轻量化的图像去雨 Transformer。"),
    ("R04", "Reciprocal Attention Mixing Transformer for Lightweight Image Restoration",
     "Choi, H.; Na, C.; Oh, J.; Lee, S.; Kim, J. et al.", 2024,
     "IEEE/CVF CVPRW 2024", "10.1109/cvprw63382.2024.00606", 40, "venue:workshop",
     "互注意力混合块，面向轻量图像复原。"),
    ("R05", "Efficient image analysis with triple attention vision transformer",
     "Li, G.; Zhao, T.", 2024,
     "Pattern Recognition", "10.1016/j.patcog.2024.110357", 13, "venue:sci-q1",
     "三重注意力结构，期刊载体层级较高。"),
    ("R06", "MCANet: Hierarchical cross-fusion lightweight transformer based on multi-ConvHead attention for object detection",
     "Zhao, Z.; Hao, K.; Liu, X.; Zheng, T.; Xu, J. et al.", 2023,
     "Image and Vision Computing", "10.1016/j.imavis.2023.104715", 11, "venue:sci-q2",
     "多卷积头注意力与层级交叉融合，面向检测任务。"),
    ("R07", "AnchorFormer: Differentiable anchor attention for efficient vision transformer",
     "Shan, J.; Wang, J.; Zhao, L.; Cai, L.; Zhang, H. et al.", 2025,
     "Pattern Recognition Letters", "10.1016/j.patrec.2025.07.016", 9, "venue:sci-q2",
     "可微锚点注意力，把注意力计算稀疏化。"),
    ("R08", "Enhanced Vision Transformer with Dual-Dimensional Self-Attention for Image Recognition",
     "Chang, Z.; Cai, Q.", 2023,
     "IEEE PRAI 2023", "10.1109/prai59366.2023.10332027", 3, "venue:conf",
     "双维自注意力的增强型 ViT。"),
    ("R09", "ELiFormer: A hierarchical Transformer based Model with Efficient Encoder and Lightweight Decoder for Semantic Segmentation",
     "Wu, Z.; Zhou, Y.", 2024,
     "ACM ACCVIPR 2024", "10.1145/3663976.3663985", 1, "venue:conf",
     "高效编码器 + 轻量解码器的分割 Transformer。"),
    ("R10", "Efficient ultra-lightweight convolutional attention network for embedded identity document recognition system",
     "Shen, Y.; Wei, J.; Niu, X.; Fu, G.; Cao, Z.", 2026,
     "Image and Vision Computing", "10.1016/j.imavis.2026.105930", 1, "venue:sci-q2",
     "嵌入式证件识别中的超轻量卷积注意力网络。"),
    ("R11", "Lightweight Vision Transformer with CBAM and LSTM for Efficient Violence Detection in Image Sequences",
     "Garg, A.; Nigam, S.; Singh, R.", 2026,
     "Signal, Image and Video Processing", "10.1007/s11760-026-05207-7", 1, "venue:sci-q3",
     "CBAM 与 LSTM 组合的轻量 ViT。"),
    ("R12", "Improvement of Satellite Image Classification Using Attention-Based Vision Transformer",
     "Slimani, N.; Jdey, I.; Kherallah, M.", 2024,
     "ICAART 2024", "10.5220/0012298400003636", 4, "venue:conf",
     "遥感场景下的注意力 ViT 改进。"),
    ("R13", "Lightweight Hybrid MobileNetv1-Vision Transformer Model for Human Activity Recognition",
     "Rani, M.; Kumar, M.", 2025,
     "IEEE ICIIP 2025", "10.1109/iciip68302.2025.11346208", 0, "venue:conf",
     "CNN 与 ViT 的混合轻量结构。"),
    ("R14", "LightFER: A Lightweight Hybrid CNN-Transformer based Model for Efficient Facial Emotion Recognition",
     "Kaur, M.; Kumar, M.", 2025,
     "IEEE ICIIP 2025", "10.1109/iciip68302.2025.11346136", 0, "venue:conf",
     "面部表情识别中的轻量 CNN-Transformer。"),
    ("R15", "EL Former-BEV: an efficient lightweight transformer-based BEV perception method",
     "Li, Y.; Cai, B.", 2025,
     "SPIE CVIPPR 2025", "10.1117/12.3076237", 0, "venue:spie",
     "BEV 感知任务中的轻量 Transformer。"),
    ("R16", "EMOv2: Pushing 5M Vision Model Frontier",
     "Zhang, J.; Hu, T.; He, H.; Xue, Z.; Wang, Y. et al.", 2024,
     "arXiv preprint 2412.06674", "arXiv:2412.06674", 0, "venue:preprint",
     "以统一视角重构轻量模块，给出 72.3/75.8/79.4 Top-1 的 1M/2M/5M 档位。"),
    ("R17", "UtVAA: Ultra-tiny Vision Transformer with Affix Attention for Mobile Image Classification",
     "George, R.; Nishankar, S.; Thuseethan, S.; Ragel, R. G.", 2026,
     "arXiv preprint 2606.14735", "arXiv:2606.14735", 0, "venue:preprint",
     "亚百万参数档：最小变体 204.67K 参数 / 53.95M FLOPs。"),
    ("R18", "Global Interaction Modelling in Vision Transformer via Super Tokens",
     "Farooq, A.; Awais, M.; Ahmed, S.; Kittler, J.", 2021,
     "arXiv preprint 2111.13156", "arXiv:2111.13156", 0, "venue:preprint",
     "Super token 做跨窗通信，ImageNet-1K 83.5%、约 49M 参数。"),
    ("R19", "Frozen CLIP Models are Efficient Video Learners",
     "Lin, Z.; Geng, S.; Zhang, R.; Gao, P.; de Melo, G. et al.", 2022,
     "arXiv preprint 2208.03550", "arXiv:2208.03550", 0, "venue:preprint",
     "冻结骨干 + 轻量解码器，视频识别的高效范式。"),
    ("R20", "PosMLP-Video: Spatial and Temporal Relative Position Encoding for Efficient Video Recognition",
     "Hao, Y.; Zhou, D.; Wang, Z.; Ngo, C.-W.; Wang, M.", 2024,
     "arXiv preprint 2407.02934", "arXiv:2407.02934", 0, "venue:preprint",
     "用相对位置编码替代稠密算子，速度-精度权衡。"),
    ("R21", "SkelVIT: Consensus of Vision Transformers for a Lightweight Skeleton-Based Action Recognition System",
     "Oztimur Karadag, O.", 2023,
     "arXiv preprint 2311.08094", "arXiv:2311.08094", 0, "venue:preprint",
     "多分类器共识的轻量骨架动作识别。"),
    ("R22", "DANTE: A Lightweight Hybrid CNN-Transformer Network for Efficient Image Classification",
     "Sanchez-Brito, M.", 2026,
     "SSRN preprint", "10.2139/ssrn.6811533", 0, "venue:questionable",
     "载体为 SSRN 预印本平台，非同行评审期刊；仅作低质样本登记。"),
    ("R23", "Bc-Vit: Lightweight Transformer with Efficient Attention and Randomized Head for Blood Cells",
     "Zhu, Z.; Lu, S.", 2025,
     "SSRN preprint", "10.2139/ssrn.5123368", 0, "venue:questionable",
     "同上，SSRN 预印本；不用于支撑实质论断。"),
    ("R24", "Lightweight Transformer-Fourier Fusion Framework for Efficient Image Super-Resolution",
     "Okafor, C.", 2026,
     "International Bulletin of Applied Sciences and Technology",
     "10.37547/ibast/volume06issue08-02", 0, "venue:questionable",
     "该刊未被主流索引收录，作者信息单薄，列为高风险载体。"),
]

by_id = {r[0]: r for r in REFS}


def ref_line(r):
    rid, title, auth, year, venue, doi, cites, tag, note = r
    cite = str(cites) if cites else "0"
    return (
        f"| {rid} | {title} | {auth} | {year} | {venue} | `{doi}` | {cite} | {tag} |"
    )


# ------------------------------------------------------------------ config
config = {
    "drill": True,
    "drill_id": "spine-001",
    "note": "架构演练任务，非真实科研产出；主题为公开通用视觉主题，不涉及用户研究方向。",
    "title": "高效视觉 Transformer 的方法学图谱（2020-2026）：证据约束小型综述（演练）",
    "description": "以满足严格计算预算的视觉 Transformer 方法为对象，梳理其效率来源与证据边界。",
    "workflow": "build_from_materials",
    "article_genre": "mini_review",
    "target": "未指定目标期刊（演练不指定载体）",
    "language": "zh",
    "research_mode": "materials_only",
    "reading_depth": 6,
    "learning_sets": {"same_direction": 6, "target_venue": 0},
    "delivery_formats": ["pdf", "docx", "tex"],
    "mechanism_figure": "omit",
    "mechanism_figure_reason": "本综述不主张因果机制；效率来源以结构对照表与真实元数据图呈现更准确。",
    "user_confirmed": False,
    "provenance": "drill_prefill",
    "provenance_note": "本配置由 Agent 按演练预设填写，未经用户逐项确认。上游规则明确：预填不等于保存；真实任务必须由用户确认。",
}
w("paper_spine_config.json", json.dumps(config, ensure_ascii=False, indent=2))

w("paper_spine_config.md", f"""# 任务配置（演练）

> **provenance = drill_prefill**：本配置为 Agent 预填，`user_confirmed = false`。
> 上游规则："A prefill is not a save." 真实任务必须由用户确认后才可执行。

| 项 | 值 |
|---|---|
| 任务标题 | {config["title"]} |
| 工作流 | {config["workflow"]} |
| 文体 | {config["article_genre"]} |
| 目标载体 | {config["target"]} |
| 语言 | {config["language"]} |
| 研究模式 | **{config["research_mode"]}** |
| 阅读深度 | {config["reading_depth"]}（同向 6 / 目标刊 0）|
| 交付格式 | {", ".join(config["delivery_formats"])} |
| 机制示意图 | **{config["mechanism_figure"]}**（理由：{config["mechanism_figure_reason"]}）|

## 研究模式的字面含义

`materials_only` **禁止**新增分析、实验、训练、评测与重跑；**允许**文献研读、
忠实提取已给结果、对已给结果绘图与一致性检查。本演练全程遵守该模式：
不做任何实验，所有论断均来自已发表记录。
""")

# -------------------------------------------------------------- source map
w("source_map.md", """# 来源映射（source map）

本任务未接收用户私有材料；全部输入为公开文献记录。

| 输入来源 | 类型 | 用途 | 是否可公开 |
|---|---|---|---|
| academic-search MCP（CrossRef / arXiv）检索结果 | 公开元数据 | 文献集、SOTA 图谱、引用支撑库 | 可公开 |
| 上游论文正文（仅读摘要与元数据） | 公开文献 | 论断支撑，逐条登记 | 可公开 |

**未使用**：用户任何私人材料、秦简相关数据、未公开结果。

## 生成物落点

| 生成物 | 路径 |
|---|---|
| 证据台账 | `evidence_bank.md` |
| 论断登记 | `claim_register.md` |
| 图表资产映射 | `figure_asset_map.md` |
| 正文单源 | `final_paper/manuscript.md` |
| 交付面 | `final_paper/paper.docx`、`final_paper/paper.pdf` |
""")

# --------------------------------------------------------- reference index
idx = ["# 参考文献索引（reference_materials/source_index.md）", "",
       "全部条目来自检索层返回的真实记录，**未手工编造任何 DOI**。",
       "载体标签为登记用途，非质量裁决。", "",
       "| ID | 标题 | 作者 | 年 | 载体 | DOI/标识 | 被引 | 载体标签 |",
       "|---|---|---|---|---|---|---|---|"]
for r in REFS:
    idx.append(ref_line(r))
idx.append("")
idx.append("## 高风险载体说明（转 citation-quality 门控）")
idx.append("")
for r in REFS:
    if r[7] == "venue:questionable":
        idx.append(f"- **{r[0]}** `{r[5]}`：{r[8]}")
w("reference_materials/source_index.md", "\n".join(idx) + "\n")

# --------------------------------------------------------- research dossier
years = {}
for r in REFS:
    years[r[3]] = years.get(r[3], 0) + 1
venue_types = {}
for r in REFS:
    t = r[7].split(":")[1]
    venue_types[t] = venue_types.get(t, 0) + 1

w("research_dossier.md", f"""# 研究档案（research_dossier）

## 1. 研究问题

视觉 Transformer（ViT）以自注意力替代卷积，在识别精度上取得优势，但其**二次复杂度
与显存访问开销**限制了在移动端与边缘设备上的部署。本演练要回答的是一个**文献层问题**：

> 2020-2026 年间，公开文献中用于压低 ViT 计算成本的**方法族**有哪几类？
> 每一类各自声称付出什么代价、换取什么收益？哪些结论有实测支撑，哪些仅有声明？

这是**综述型问题**，不涉及本研究的实验主张，因此在 `materials_only` 模式下可完成。

## 2. 文献集构成（真实检索结果，共 {len(REFS)} 条）

- 顶会（CVPR 正刊/Workshop）：3 条
- 期刊（Pattern Recognition / Image and Vision Computing / SIViP）：5 条
- 一般会议（IEEE PRAI/ICIIP、ACM、SPIE、ICAART）：5 条
- 预印本（arXiv）：8 条
- **高风险载体（SSRN 预印本、非索引期刊）：3 条** → 不用于支撑实质论断

年份分布：{", ".join(f"{y} 年 {n} 条" for y, n in sorted(years.items()))}

## 3. 方法族初判

按"效率来源"而非按任务划分，可归为四族：

| 族 | 效率来源 | 代表条目 |
|---|---|---|
| **F1 注意力稀疏化/结构化** | 限制注意力范围或改成可微锚点 | R02, R07 |
| **F2 分组与级联注意力** | 把通道分组、级联以降低内存访问 | R01 |
| **F3 混合 CNN-Transformer** | 卷积承担局部、注意力承担全局 | R13, R14, R10 |
| **F4 参数共享与轻量模块重构** | 递归共享、统一元模块、超小参数档 | R03, R16, R17 |

另有 **F5 位置编码替代稠密算子**（R20）与 **F6 冻结大骨干 + 轻量头**（R19）两支，
出现在视频/多模态场景。

## 4. 证据强度分级

| 等级 | 判据 | 条目 |
|---|---|---|
| **A 有可核验读数** | 给出明确数据集与 Top-1/FLOPs 数值 | R16(72.3/75.8/79.4)、R17(204.67K 参数/53.95M FLOPs)、R18(83.5%, 49M) |
| **B 有指标但缺完整设置** | 给出指标但训练配方/划分不完整 | R01, R03, R04 |
| **C 仅方法声明** | 未给出可对比读数 | R02, R08-R15 |
| **D 高风险载体** | 同行评审状态不明 | R22, R23, R24 |

> 说明：本表**只依据检索层返回的元数据与摘要**。摘要未给出的项一律记为"未报告"，
> 不代论文补全。这是本演练的**最大证据边界**。

## 5. 未做的事（不隐藏）

- **未获取全文 PDF**，未逐段核对方法细节与实验表格；
- 因此**所有"方法族"归类均为基于标题与摘要的初步归类**，属推断，不是论文原文主张；
- 未做任何复现或重跑（`materials_only` 禁止）。
""")

# ---------------------------------------------------- exemplar learning
w("exemplar_learning_dossier.md", """# 范例学习档案（exemplar_learning_dossier）

## 定位

上游要求"打开目标刊真实 PDF、逐页看版式与图"。**本演练不指定目标刊**，
因此不存在"目标刊范例集"。这是**诚实缺口**，不是已完成项。

## 实际做了什么

仅对同向文献的**摘要层**做了问题-方法-证据结构提取（共 24 条），记录如下维度：

| 维度 | 观察 |
|---|---|
| 标题构式 | "Lightweight/Efficient + 结构名词 + for 任务"占多数（R10-R15） |
| 摘要骨架 | 问题（二次复杂度/参数多）→ 结构改动 → 数据集与读数 → 代码链接 |
| 读数披露 | 顶会与部分期刊给出 Top-1 与 FLOPs；一般会议常只给精度 |
| 失败披露 | **无一条摘要报告负结果或失败条件**，属于该体裁系统性偏倚 |

## 明确未完成

- 未阅读任何全文 PDF，未做版式、图型与页面设计层面的范例学习；
- 因此**不得**声称完成"目标场景学习"（上游第 5 步要求的是 PDF 级阅读）。
""")

# ----------------------------------------------------------- style profile
w("style_profile.md", """# 风格画像（style_profile）

由于未获取全文 PDF，本画像**仅基于摘要语料**，置信度低，标记为 **inferred**。

| 项 | 观察（低置信） |
|---|---|
| 时态 | 方法与结果多用一般现在时；贡献声明用现在完成时 |
| 人称 | 摘要避免第一人称；正文常见 "we propose" |
| 句长 | 中长句为主，从句嵌套密度中等 |
| 术语习惯 | 倾向复用既有命名（如 cascaded group attention）而非新造词 |
| 数值披露 | 精度保留一位小数，参数量用 M/K，算力用 FLOPs/GFLOPs |

**用途限制**：本画像不得用于声称"已学习目标期刊风格"。上游明确：仅凭摘要或标题列表
不构成版式/风格学习。
""")

# ------------------------------------------------------------ sota gap map
w("sota_gap_map.md", f"""# SOTA 与空白图谱（sota_gap_map）

## 1. 已报告读数（仅列真实记录中出现过的数字）

| 条目 | 报告读数 | 来源层级 |
|---|---|---|
| R16 EMOv2 | 1M/2M/5M 档位 Top-1 = 72.3 / 75.8 / 79.4 | 预印本 |
| R17 UtVAA | 最小变体 204.67K 参数、53.95M FLOPs | 预印本 |
| R18 STT-S25 | ImageNet-1K 83.5%，约 49M 参数 | 预印本 |

> **禁止外推**：三条读数来自不同论文、不同训练配方与不同评测协议，
> **不可横向比较**，本表不做排序、不画统一柱状对比。

## 2. 已识别的空白（基于文献层可见信息）

| 编号 | 空白 | 依据 | 是否可在本演练内验证 |
|---|---|---|---|
| GAP-1 | 效率改进的**评测口径不统一**（有的报 FLOPs、有的报参数量、有的只报精度） | R10-R15 多只报精度 | 可（元数据层） |
| GAP-2 | **负结果系统性缺失**：24 条摘要无一报告失败条件 | 全语料统计 | 可（元数据层） |
| GAP-3 | 轻量模型的**部署端真实延迟**普遍未报告，只有理论 FLOPs | 仅 R19/R20 提及时延 | 可（元数据层） |
| GAP-4 | 高风险载体（SSRN、非索引刊）在效率类主题上占比不低 | R22, R23, R24 | 可（元数据层） |
| GAP-5 | 效率与**鲁棒性/分布外泛化**的联合评估缺失 | 语料中未见此类报告 | **不可**（需全文/实验） |

## 3. 边界声明

GAP-1 至 GAP-4 属**元数据层**可核验的空白；**GAP-5 不可在本任务内成立**，需全文与实验，
本演练不主张。任何把 GAP-5 写成结论的做法都属越界。
""")

# ------------------------------------------------ contribution / motivation
w("contribution_options_after_research.md", """# 贡献选项（contribution_options_after_research）

| 选项 | 贡献声明 | 证据支撑 | 风险 |
|---|---|---|---|
| **C1** | 提出一个以"效率来源"为轴的方法族分类，替代按任务分类的常见做法 | 24 条真实记录的归类 | 归类基于摘要，颗粒度粗 |
| **C2** | 给出效率类文献的**证据强度分级**，暴露"只报精度不报算力"的口径问题 | R10-R15 的实际披露情况 | 样本量小（24 条） |
| **C3** | 量化高风险载体在该主题上的占比 | R22/R23/R24 | 检索式偏倚未控制 |

**未列入的选项**：任何声称"某方法最优"或"某结构更高效"的选项——证据不支持跨论文比较。
""")

w("confirmed_contribution.md", """# 已确认贡献（confirmed_contribution）

**确认方式**：演练内由 Agent 依 `materials_only` 范围自行选定，并在本文件记录该委托。
**这不是用户点击确认**，属上游允许的 explicitly delegated automatic run，须显式留痕。

## 选定

**C1 + C2 合并**：以"效率来源"为轴给出方法族分类，并配套给出证据强度分级，
暴露口径不一致问题。

## 主张边界（claim boundary）

- 本贡献是**文献组织方式**的贡献，不是新方法、不是新读数、不主张性能优劣。
- 分类与分级**仅基于标题与摘要**，属推断层结论，须在正文中显式标注。
- **不主张**任何跨论文的数值比较。
""")

w("motivation_options_after_research.md", """# 动机选项（motivation_options_after_research）

| 选项 | 动机表述 | 强度 |
|---|---|---|
| **M1** | 效率型 ViT 数量增长快但评测口径分裂，读者难以判断进展 | 高（有元数据支撑） |
| **M2** | 该主题上非同行评审载体占比不低，检索结果需要载体过滤意识 | 中（样本小） |
| **M3** | 综述普遍按任务分类，掩盖了"效率来自哪里"这一实质差异 | 中（属方法论主张） |
""")

w("confirmed_motivation.md", """# 已确认动机（confirmed_motivation）

**选定：M1 为主，M2 为辅。**

- M1 直接由元数据支撑（24 条中仅 8 条给 FLOPs，6 条仅给精度）。
- M2 作为次级提醒，措辞保持克制，不推广为"该领域充斥低质文献"这类总体断言。

M3 降级为讨论段的一句方法论观察，不作为动机主线。
""")

print("phase A done")
