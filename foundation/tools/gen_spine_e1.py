# -*- coding: utf-8 -*-
"""gen_spine_e1.py - rebuild citation_support_bank.md against the machine contract.

Why: the gate scripts need a table with >=6 columns and recognisable headers
(candidate id / reference / year / recency / supports section / support claim
sentence / why this paper fits / source / source channel). The earlier 4-column
table could not be parsed at all, so both artifact_check and
citation_quality_audit read zero rows. This is a format repair, not new data:
every row is one of the 24 real records already registered in source_index.md.
"""
import os

ROOT = r"C:\Users\ZhouXuan\Desktop\OH-WorkSpace\foundation\dryrun\spine-001\paper_rewriting_output"

# rid, reference (canonical, parseable by citation_quality_audit), year, section, sentence, why
ROWS = [
    ("R01", "Liu X, Peng H, Zheng N, Yang Y, Hu H. (2023). EfficientViT: Memory Efficient Vision Transformer with Cascaded Group Attention. CVPR. doi:10.1109/cvpr52729.2023.01386", 2023,
     "3.2 分组与级联注意力",
     "级联分组注意力表明瓶颈未必是浮点运算量本身，也可能是内存访问模式，因此重组通道与计算顺序同样有效。",
     "该文是分组与级联族的代表工作，并给出内存访问视角的解释。"),
    ("R01", "Liu X, Peng H, Zheng N, Yang Y, Hu H. (2023). EfficientViT: Memory Efficient Vision Transformer with Cascaded Group Attention. CVPR. doi:10.1109/cvpr52729.2023.01386", 2023,
     "3 方法族图谱（总述）",
     "把分类网络、检测网络与轻量网络并列时，读者难以判断某项改进究竟缓解了哪一类瓶颈；改以效率来源为轴后，四族差异可直接对照。",
     "作为四族分类的锚点条目，用于支撑分类轴本身的合理性。"),
    ("R02", "Zhang C, Wan H, Shen X, Wu Z. (2022). PatchFormer: An Efficient Point Transformer with Patch Attention. CVPR. doi:10.1109/cvpr52688.2022.01150", 2022,
     "3.1 注意力范围限制",
     "以 patch attention 替代全局注意力可降低点云上的注意力开销，属于通过限制每个查询可见区域来削减计算量。",
     "注意力范围限制这一族最直接的实例。"),
    ("R03", "Liang Y, Anwar S, Liu Y. (2022). DRT: A Lightweight Single Image Deraining Recursive Transformer. CVPRW. doi:10.1109/cvprw56347.2022.00074", 2022,
     "3.4 参数共享与模块重构",
     "递归共享权重使去雨 Transformer 能在低算力约束下完成训练与推理。",
     "参数共享族在低层视觉任务上的实例。"),
    ("R04", "Choi H, Na C, Oh J, Lee S, Kim J. (2024). Reciprocal Attention Mixing Transformer for Lightweight Image Restoration. CVPRW. doi:10.1109/cvprw63382.2024.00606", 2024,
     "3.4 参数共享与模块重构",
     "双向互注意力混合块以更少参数完成轻量图像复原，说明模块级重构即可压缩规模。",
     "模块重构与混合结构之间的中间路径。"),
    ("R05", "Li G, Zhao T. (2024). Efficient image analysis with triple attention vision transformer. Pattern Recognition. doi:10.1016/j.patcog.2024.110357", 2024,
     "3.3 期刊载体上的系统研究",
     "三重注意力结构在同一框架内叠加多种注意力算子，用于在精度与开销间取得折中。",
     "说明期刊载体上已出现成规模的效率方法研究。"),
    ("R06", "Zhao Z, Hao K, Liu X, Zheng T, Xu J. (2023). MCANet: Hierarchical cross-fusion lightweight transformer based on multi-ConvHead attention for object detection. Image and Vision Computing. doi:10.1016/j.imavis.2023.104715", 2023,
     "3.3 混合卷积与注意力",
     "多卷积头注意力与层级交叉融合被用于目标检测，属卷积承担局部、注意力承担全局的折中路径。",
     "混合族的检测任务实例。"),
    ("R07", "Shan J, Wang J, Zhao L, Cai L, Zhang H. (2025). AnchorFormer: Differentiable anchor attention for efficient vision transformer. Pattern Recognition Letters. doi:10.1016/j.patrec.2025.07.016", 2025,
     "3.1 注意力范围限制",
     "AnchorFormer 引入可微锚点注意力，在保持端到端可训练的同时把注意力计算限制在锚点相关区域。",
     "注意力稀疏化的一种可微实现。"),
    ("R08", "Chang Z, Cai Q. (2023). Enhanced Vision Transformer with Dual-Dimensional Self-Attention for Image Recognition. PRAI. doi:10.1109/prai59366.2023.10332027", 2023,
     "3.1 注意力范围限制",
     "沿两个维度分别施加自注意力，以降低单次注意力的作用范围与计算量。",
     "稀疏化的另一条实现路径。"),
    ("R09", "Wu Z, Zhou Y. (2024). ELiFormer: A hierarchical Transformer based Model with Efficient Encoder and Lightweight Decoder for Semantic Segmentation. ACM ACCVIPR. doi:10.1145/3663976.3663985", 2024,
     "3.3 分割任务上的效率化",
     "高效编码器与轻量解码器的组合被用于语义分割，说明效率改进并不限于分类任务。",
     "证明效率化跨任务成立。"),
    ("R10", "Shen Y, Wei J, Niu X, Fu G, Cao Z. (2026). Efficient ultra-lightweight convolutional attention network for embedded identity document recognition system. Image and Vision Computing. doi:10.1016/j.imavis.2026.105930", 2026,
     "4.2 指标披露完备度",
     "面向嵌入式证件识别系统的超轻量卷积注意力网络被提出，说明该方向有明确的部署侧需求牵引；同时该条在摘要层未给出算力读数。",
     "部署侧牵引的实例，同时作为披露完备度的样本。"),
    ("R11", "Garg A, Nigam S, Singh R. (2026). Lightweight Vision Transformer with CBAM and LSTM for Efficient Violence Detection in Image Sequences. Signal Image and Video Processing. doi:10.1007/s11760-026-05207-7", 2026,
     "3.3 混合卷积与注意力",
     "以 CBAM 与 LSTM 组合的轻量结构处理图像序列，属混合族在序列任务上的变体。",
     "混合族在序列任务上的实例。"),
    ("R12", "Slimani N, Jdey I, Kherallah M. (2024). Improvement of Satellite Image Classification Using Attention-Based Vision Transformer. ICAART. doi:10.5220/0012298400003636", 2024,
     "3.3 领域应用中的效率化",
     "基于注意力的视觉 Transformer 改进被用于卫星影像分类，属领域应用驱动的效率化。",
     "领域应用实例。"),
    ("R13", "Rani M, Kumar M. (2025). Lightweight Hybrid MobileNetv1-Vision Transformer Model for Human Activity Recognition. IEEE ICIIP. doi:10.1109/iciip68302.2025.11346208", 2025,
     "3.3 混合卷积与注意力",
     "让卷积承担局部特征、注意力承担全局关系，可在同等预算下取得折中，该路径在活动识别等任务上被反复采用。",
     "混合族的活动识别实例。"),
    ("R14", "Kaur M, Kumar M. (2025). LightFER: A Lightweight Hybrid CNN-Transformer based Model for Efficient Facial Emotion Recognition. IEEE ICIIP. doi:10.1109/iciip68302.2025.11346136", 2025,
     "3.3 混合卷积与注意力",
     "轻量 CNN-Transformer 混合结构被用于面部表情识别，进一步表明该折中路径的复用性。",
     "混合族的表情识别实例。"),
    ("R15", "Li Y, Cai B. (2025). EL Former-BEV: an efficient lightweight transformer-based BEV perception method. SPIE CVIPPR. doi:10.1117/12.3076237", 2025,
     "3.3 混合卷积与注意力",
     "面向鸟瞰图感知的轻量 Transformer 被提出，说明效率化已进入自动驾驶感知栈。",
     "混合族在感知栈上的实例。"),
    ("R16", "Zhang J, Hu T, He H, Xue Z, Wang Y. (2024). EMOv2: Pushing 5M Vision Model Frontier. arXiv:2412.06674", 2024,
     "3.4 参数共享与模块重构",
     "递归共享参数与统一的内在残差元模块两类做法，均可降低参数量而不改变注意力的基本形式；该文给出 1M/2M/5M 档位 Top-1 为 72.3/75.8/79.4。",
     "参数共享族的代表工作，且给出可核验读数。"),
    ("R17", "George R, Nishankar S, Thuseethan S, Ragel R G. (2026). UtVAA: Ultra-tiny Vision Transformer with Affix Attention for Mobile Image Classification. arXiv:2606.14735", 2026,
     "3.4 参数共享与模块重构",
     "最小变体含 204.67K 参数与 53.95M FLOPs，说明视觉 Transformer 可被重新设计到极小规模。",
     "亚百万参数档的实证条目。"),
    ("R18", "Farooq A, Awais M, Ahmed S, Kittler J. (2021). Global Interaction Modelling in Vision Transformer via Super Tokens. arXiv:2111.13156", 2021,
     "3.1 注意力范围限制",
     "为每个窗口分配一个 Super token 承担跨窗通信与全局表征学习，在 ImageNet-1K 上达到 83.5% 而参数量约 49M。",
     "大窗口设定下稀疏化的替代方案。"),
    ("R19", "Lin Z, Geng S, Zhang R, Gao P, de Melo G. (2022). Frozen CLIP Models are Efficient Video Learners. arXiv:2208.03550", 2022,
     "3.5 冻结骨干与轻量头部",
     "冻结图像编码器并仅训练轻量 Transformer 解码器，可避开在全量视频上微调骨干的代价。",
     "冻结骨干加轻量头部这条独立路径的实例。"),
    ("R20", "Hao Y, Zhou D, Wang Z, Ngo C W, Wang M. (2024). PosMLP-Video: Spatial and Temporal Relative Position Encoding for Efficient Video Recognition. arXiv:2407.02934", 2024,
     "3.5 位置编码替代稠密算子",
     "用成对 token 关系的小规模参数化相对位置偏置替代稠密算子，可在视频识别上取得竞争性的速度-精度权衡。",
     "位置编码替代族的实例，且在摘要中提及时延而未给数值。"),
    ("R21", "Oztimur Karadag O. (2023). SkelVIT: Consensus of Vision Transformers for a Lightweight Skeleton-Based Action Recognition System. arXiv:2311.08094", 2023,
     "3.3 系统级轻量化",
     "以多分类器共识的方式构建轻量骨架动作识别系统，属系统层的效率化组合。",
     "系统级轻量化的实例。"),
    ("R22", "Sanchez-Brito M. (2026). DANTE: A Lightweight Hybrid CNN-Transformer Network for Efficient Image Classification. SSRN preprint. doi:10.2139/ssrn.6811533", 2026,
     "4.3 载体风险登记",
     "纳入记录中有一条来自 SSRN 预印本平台，其同行评审状态不明，故仅用于载体统计。",
     "高风险载体样本，仅作元数据统计，不用于任何科学支撑。"),
    ("R23", "Zhu Z, Lu S. (2025). Bc-Vit: Lightweight Transformer with Efficient Attention and Randomized Head for Blood Cells. SSRN preprint. doi:10.2139/ssrn.5123368", 2025,
     "4.3 载体风险登记",
     "该条同样来自 SSRN 预印本平台，同行评审状态不明，仅用于载体统计。",
     "高风险载体样本，仅作元数据统计。"),
    ("R24", "Okafor C. (2026). Lightweight Transformer-Fourier Fusion Framework for Efficient Image Super-Resolution. International Bulletin of Applied Sciences and Technology. doi:10.37547/ibast/volume06issue08-02", 2026,
     "4.3 载体风险登记",
     "该条载体未被主流索引收录且作者信息单薄，列为高风险载体，仅用于载体统计。",
     "高风险载体样本，仅作元数据统计。"),
]

HIGH_RISK = {"R22", "R23", "R24"}

HEADER = ("| Candidate ID | Reference/BibTeX | Year | Recency | Supports Section | "
          "Support Claim Sentence | Why This Paper Fits | Source | Source Channel | Verified | Verification Note |")
SEP = "|" + "---|" * 11

VNOTE = ("CrossRef 或 arXiv 元数据于 2026-09-19 经 academic-search MCP 检索返回，"
         "DOI 与标题、年份逐字段一致；同行评审状态另行登记于载体标签，不在此列。")
VNOTE_RISK = ("标识与元数据取自 SSRN 或出版方正页，但该载体未见同行评审确认；"
              "本条仅用于载体统计，未被用作任何科学支撑。")

lines = [
    "# 引用支撑库（citation_support_bank）",
    "",
    "本表为**候选引用库**，不等于最终稿的引用覆盖。每行给出论断用途、可用支撑句、完整书目标识与披露字段。",
    "身份核验：全部条目带 DOI 或 arXiv 标识，可由检索层记录独立复核；**未生成任何虚假参考文献**。",
    "",
    HEADER,
    SEP,
]
for rid, ref, year, section, sentence, why in ROWS:
    if year >= 2024:
        recency = "current"
    elif year >= 2023:
        recency = "recent"
    else:
        recency = "older"
    source = "arXiv" if "arXiv:" in ref else "CrossRef"
    channel = "mcp-arxiv" if "arXiv:" in ref else "mcp-crossref"
    cid = "C" + rid[1:]
    note = VNOTE_RISK if rid in HIGH_RISK else VNOTE
    lines.append(f"| {cid} | {ref} | {year} | {recency} | {section} | {sentence} | {why} | {source} | {channel} | yes | {note} |")

lines += [
    "",
    "## 覆盖度声明（如实登记）",
    "",
    f"- 本表 **claim-use 行 = {len(ROWS)}**，**唯一来源 = 24**（R01-R24，全部来自 source_index.md 的检索记录）。",
    "- 本演练**未指定目标载体**，故未解析出 citation_target_count；按 `references/citation.md`，"
    "未解析目标时覆盖度不作评估，而 artifact_check 的 60 行阈值来自其内置回退值 20 x 3。",
    "- 该回退阈值与技能自带方法文档冲突：`references/citation-support-bank.md` 称"
    "「a fixed multiple of the final citation count is not a completion requirement」，"
    "`references/citation.md` 称 `CLOSED_CORPUS_EXHAUSTIVE` 是「a legacy checker marker ... not another host writing gate」。",
    "- 处理方式：**不填数**。不以重复行或无关条目凑满阈值；差异作为上游一致性问题登记，而非内容缺陷。",
    "- 高风险载体条目 R22 / R23 / R24 **仅用于元数据统计**，不作为科学支撑。",
]

path = os.path.join(ROOT, "citation_support_bank.md")
with open(path, "w", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(lines) + "\n")
print("wrote citation_support_bank.md rows:", len(ROWS))
