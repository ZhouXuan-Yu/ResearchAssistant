# -*- coding: utf-8 -*-
"""gen_spine_e2.py - rebuild writing_rationale_matrix.md against the machine contract.

Why: artifact_check requires eight named columns (manuscript unit, contribution
promise, motivation alignment, reference/SOTA pattern, target scene/venue norm,
evidence/citation anchor, planned text move, final text check), at least eight
rows, and a substantial rationale per row. The earlier 4-column matrix could not
be matched at all. This is a format repair with real content: each row is one
writing unit of the drill manuscript.
"""
import os

ROOT = r"C:\Users\ZhouXuan\Desktop\OH-WorkSpace\foundation\dryrun\spine-001\paper_rewriting_output"

HEADER = (u"| Manuscript Unit 写作单元 | Contribution Promise 贡献承诺 | Motivation Alignment 动机对齐 | "
          u"Reference/SOTA Pattern 参考样例 | Target Scene/Venue Norm 目标场景规范 | "
          u"Evidence/Citation Anchor 证据引用锚点 | Planned Text Move 计划写法 | Final Text Check 最终检查 |")
SEP = "|" + "---|" * 8

R = [
    # 1 whole-work framework
    (u"全文框架与主线（演练稿）",
     u"承诺：提供一条以效率来源为轴的分类主线，让四族差异可直接对照，并配套给出证据强度分级。",
     u"动机对齐：效率型 ViT 数量增长快但评测口径分裂，读者无法判断进展，因此主线必须服务判断而非罗列。",
     u"参考样例：既有综述多按任务（分类、检测、分割、复原）组织，本文改按其组织轴的反面来做。",
     u"目标场景规范：本演练不指定载体，故按综述体裁的一般规范处理，即范围、纳入口径与边界须前置声明。",
     u"证据引用锚点：24 条真实检索记录（R01-R24），元数据层可逐条回算，见 source_index.md 与 evidence_bank.md。",
     u"计划写法：先立分类轴，再以证据景观收束，全文以证据边界为主线前后呼应，不让任何一节越过元数据层。",
     u"最终检查：全文是否只由该主线与证据边界构成，是否出现跨论文性能比较。"),
    # 2 abstract
    (u"摘要",
     u"承诺：在一段内交代范围、四族分类结论与其证据边界，不承诺任何性能优劣。",
     u"动机对齐：呼应口径分裂这一动机，摘要即限定结论强度，避免读者误读为领域总体判断。",
     u"参考样例：综述摘要的常见骨架是范围、组织方式、主要观察、边界，此处照该骨架写。",
     u"目标场景规范：不指定载体，故按最保守口径，摘要中出现的每个数字都须能在正文找到出处。",
     u"证据引用锚点：引用 evidence_bank.md 的 E-B1 与 E-B2，即年份分布与披露完备度两项统计。",
     u"计划写法：把结论句写成限定式，用范围短语收束，避免出现更优或更高效这类比较词。",
     u"最终检查：摘要与结论是否互相矛盾，数字是否与证据库一致。"),
    # 3 introduction
    (u"第 1 节 引言",
     u"承诺：说明效率问题的来源与既有组织方式的不足，把读者的判断需求立起来。",
     u"动机对齐：直接承接动机 M1，即口径分裂使进展难以判断，必须在引言就点明。",
     u"参考样例：对照顶会效率类论文的引言写法，即问题、既有做法、缺口、本文做法四段式。",
     u"目标场景规范：不指定载体，按综述引言惯例处理，避免在引言提出任何未经证据的主张。",
     u"证据引用锚点：引用 R01 与 R10 说明效率与披露两个问题并存，均来自 source_index.md。",
     u"计划写法：先写问题，再写归类轴的必要性，用对照句把任务分类与效率来源分类的区别放在同一段内。",
     u"最终检查：引言中的每句主张是否都能落到具体条目，是否出现未标注的推断。"),
    # 4 method and scope
    (u"第 2 节 方法与范围",
     u"承诺：交代检索式、纳入口径与 materials_only 限制，使结论可追溯到过程。",
     u"动机对齐：动机要求判断可信，因此必须先把范围与限制说明白，避免读者高估证据基础。",
     u"参考样例：对照同向论文的方法小节写法，即数据来源、纳入排除、评价口径三项齐备。",
     u"目标场景规范：不指定载体，按可复现的最低要求写，检索式与记录数一并给出。",
     u"证据引用锚点：引用 source_index.md 的 24 条记录与检索层来源，标注通道为 mcp-crossref 与 mcp-arxiv。",
     u"计划写法：用清单式句式列出纳入与排除，把未获取全文这一限制放在小节末尾显式收束。",
     u"最终检查：范围声明是否与实际记录一致，是否遗漏材料未获全文的限制。"),
    # 5 family map
    (u"第 3 节 方法族图谱",
     u"承诺：给出四族分类并与代表条目绑定，使每一项归类可被读者逐条复核。",
     u"动机对齐：承接主线，把按任务分类掩盖的差异重新暴露出来。",
     u"参考样例：参考 R01 的级联分组注意力与 R02 的 patch attention 的表述方式，用结构词汇而非效果词汇。",
     u"目标场景规范：不指定载体，按综述正文惯例要求每条归类可追溯到条目编号。",
     u"证据引用锚点：引用 R01、R02、R07、R16 等条目，均见 source_index.md 与 evidence_bank.md。",
     u"计划写法：每族一段，段末用一句对照句点出该族付出的代价，避免把声明写成结论。",
     u"最终检查：是否每条归类都标注了推断属性，是否混入效果比较。"),
    # 6 evidence landscape
    (u"第 4 节 证据景观",
     u"承诺：给出年份、载体与披露完备度三项统计，并说明其为何不足以支撑横向比较。",
     u"动机对齐：这正是动机 M1 的量化落点，把口径分裂从说法变成可回算的计数。",
     u"参考样例：对照数据型图表的呈现惯例，即图注须自含读数与样本量。",
     u"目标场景规范：不指定载体，按图注自含的最低要求写，并注明 n 与数据来源文件。",
     u"证据引用锚点：引用 E-B1 的年份计数与 E-B2 的披露计数，以及图 1 的三面板读数。",
     u"计划写法：先给图，再用一段解释为何三条读数不可比较，用对照句把可比较与不可比较并列。",
     u"最终检查：图注与正文数字是否一致，披露统计是否只限定在带摘要样本内。"),
    # 7 discussion and limitations
    (u"第 5 节 讨论与局限",
     u"承诺：区分元数据层可成立的空白与需全文或实验才能成立的空白，并显式放弃后者。",
     u"动机对齐：动机要求判断边界清晰，因此讨论节承担划定不能比较范围的责任。",
     u"参考样例：参考综述讨论节的常见写法，即先给可成立观察，再给不可成立观察与原因。",
     u"目标场景规范：不指定载体，按最保守口径处理，凡不可验证者一律写明不主张。",
     u"证据引用锚点：引用 sota_gap_map.md 的 GAP-1 至 GAP-4 与 GAP-5 的不可成立说明。",
     u"计划写法：用可成立与不可成立两组并列，对 GAP-5 明确写出需全文与实验，本文不主张。",
     u"最终检查：是否存在把不可成立项写成结论的句子，是否遗漏高风险载体的限定。"),
    # 8 conclusion
    (u"第 6 节 结论",
     u"承诺：只重申文献层结论，不新增任何主张，也不引入前文未出现的数字。",
     u"动机对齐：收束主线，让读者带走分类轴与证据边界两个要点，而不是性能排序。",
     u"参考样例：对照综述结论段的克制写法，通常只重申贡献与边界，不展望未验证结论。",
     u"目标场景规范：不指定载体，按最保守口径收束，避免出现优于或不足这类比较词。",
     u"证据引用锚点：回指第 3 节的四族分类与第 4 节的披露统计，均可由证据库回算。",
     u"计划写法：用前后呼应的写法回收引言提出的问题，并以前瞻一句收束限制而非承诺。",
     u"最终检查：结论是否与摘要一致，是否出现任何跨论文比较或新数字。"),
]

lines = [
    u"# 写作理由矩阵（writing_rationale_matrix）",
    "",
    u"本矩阵把演练稿拆为 8 个写作单元，逐单元记录贡献承诺、动机对齐、参考样例、目标场景规范、证据锚点、计划写法与最终检查。",
    u"首行为全文框架行，用于在进入节级写作前先钉住控制结构。",
    "",
    HEADER,
    SEP,
]
for row in R:
    lines.append("| " + " | ".join(row) + " |")
lines += [
    "",
    u"## 反例处理",
    "",
    u"若发现某条高风险载体论文的方法确有价值，仍不改变其载体风险登记结论；载体风险与方法价值是不同维度，正文分开表述。",
]

path = os.path.join(ROOT, "writing_rationale_matrix.md")
with open(path, "w", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(lines) + "\n")
print("wrote writing_rationale_matrix.md rows:", len(R))
