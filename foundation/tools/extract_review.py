# -*- coding: utf-8 -*-
"""extract_review.py - land the independent blind review verbatim.

The review text is copied out of the sub-agent session file, not retyped, so the
artifact is byte-faithful to what the independent reviewer returned. A verification
appendix records my own check of every finding.
"""
import io
import json
import os

SRC = r"C:\Users\ZhouXuan\.hanako\agents\agent-mu42qzfz\subagent-sessions\direct\2026-09-19T07-05-41-243Z_01a0b87c-2e7b-7ca2-bf12-dfdafad1c3bc.jsonl"
OUT = r"C:\Users\ZhouXuan\Desktop\OH-WorkSpace\foundation\dryrun\spine-001\paper_rewriting_output\reviewer_audit.md"

texts = []
with io.open(SRC, encoding="utf-8") as fh:
    for line in fh:
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except Exception:
            continue
        msg = obj.get("message")
        if not isinstance(msg, dict) or msg.get("role") != "assistant":
            continue
        content = msg.get("content")
        if isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text" and block.get("text"):
                    texts.append(block["text"])

body = texts[-1] if texts else "(no assistant text found)"

VERDICT = """
---

## 附：科研助手对每条发现的独立核验

核验方式：逐条回到 `final_paper/manuscript.md`、`evidence_bank.md`、`claim_register.md`、
`research_dossier.md`、`sota_gap_map.md` 与 `reference_materials/source_index.md` 对账，
并把载体与年份构成按书目表逐条重点数。

| 发现 | 核验结论 | 说明 |
|---|---|---|
| S1 | **成立** | 本库 E-A1/E-A2/E-A3 无一条同时含参数量、算力与精度，正文与摘要的表述超出自身证据表。 |
| S2 | **成立** | 18 条无摘要者的披露状态不可知，正文将其并入披露判断，属把推断写成事实。 |
| S3 | **成立** | 由 6 条推及体裁属过度外推；且 `sota_gap_map.md` 的 GAP-2 把 6 条误写为 24 条。 |
| S4 | **成立** | R02 为点云、R19/R20 为视频、R21 为 skeleton，纳入口径未声明边界。 |
| S5 | **成立** | 小标题把 6 条子集结论写成一般结论。 |
| E1 | **成立** | §2、§5 写 16，摘要、§4、E-B2 写 18，6+18=24 才闭合。 |
| E2 | **成立** | §5 缺 GAP-4，而 sota_gap_map 与写作矩阵均要求覆盖 GAP-1 至 GAP-4。 |
| E3 | **成立** | 摘要的负结果表述未带 6 条限定。 |
| E4 | **成立** | §1 区间引注止于 R21，书目至 R24。 |
| E5 | **成立** | 缩减一半以上依赖未言明的严格同行评审定义。 |
| T1 | **部分成立，且已被本轮修复** | 评审时 `source_index.md` 已被 reference_inventory.py 覆盖为 REF001-037，故评审读到的是错文件；本轮已恢复 24 条书目表。 |
| T2 | **不成立（评审时证据被污染）** | 按恢复后的书目表实点，年份分布为 2021:1、2022:3、2023:4、2024:6、2025:5（含 R23）、2026:5（含 R22/R24），与图 1(a) 一致；评审据以判断的文件不含这些年份。 |
| T3 | **成立** | 按书目表实点为顶会正刊 2、Workshop 2、期刊 5、一般会议 6、预印本 6、高风险 3；`research_dossier.md` 的 3/5/5/8/3 有误，正文与 E-B1 正确。 |
| T4 | **成立** | 3/1/2 四个子计数未逐条落地；本轮未修，需重读 6 条带摘要记录的字段。 |
| T5 | **成立** | 部署延迟在三处定性不一致（E-C 未见、GAP-3 标可核、正文标推断）。 |
| T6 | **成立** | CL-1 依赖标为 E-B1，与分类无关。 |
| T7 | **成立** | `results_validation.md` 引用不可执行的回算源。 |
| T8 | **成立** | 标题写 2020-2026，实际跨度为 2021-2026。 |
| T9 | **成立** | E-A3 出自 R18，正文未引 R18。 |
| I1 | **已消除** | 评审时 citation_quality_audit 仍为 0 条 FAIL；本轮修复后为 25 条、18 条核验通过、PASS 88/100。 |
| I2 | **部分成立** | 同 T1，指向的文件在评审时已被覆盖；恢复后年份与载体可回算，披露字段仍不可回算。 |
| I3 | **成立** | 剔除的 5 条与检索式未列出。 |
| I4 | **成立** | 高风险载体为判断而非事实，CL-4 却标事实；R24 的非索引刊定性无来源。 |
| I5 | **成立** | 书目表混排 12 条正文未引用条目，未声明其性质。 |
| I6 | **不成立（评审时证据被污染）** | 同 T2，R22/R23/R24 的年份存在于恢复后的书目表。 |

**总评**：本次盲评在证据对账层面有效，最该拦下的三类问题（摘要数字与自身证据表冲突、
同稿计数不一致、声称可回算而源文件不含数据）均命中。其中 T1/T2/I2/I6 的成因是本演练自身
的一个缺陷：`reference_inventory.py` 会覆盖 `reference_materials/source_index.md`。
该缺陷已记录，并把恢复前后的状态一并留痕，以免把污染结果当作稿件缺陷。
"""

with io.open(OUT, "w", encoding="utf-8", newline="\n") as fh:
    fh.write("# 独立评审者盲评记录（reviewer_audit）\n\n")
    fh.write("| 项 | 值 |\n|---|---|\n")
    fh.write("| 评审者 | 独立子代理（agent-mqb8td2n，交流者 / mimo-v2.5-pro） |\n")
    fh.write("| 权限 | 只读；未修改任何文件 |\n")
    fh.write("| 评审时间 | 2026-09-19 15:02-15:05 (+08:00) |\n")
    fh.write("| 评审对象 | `final_paper/manuscript.md`、`claim_register.md`、`evidence_bank.md`、`reference_materials/source_index.md` |\n")
    fh.write("| 评审有效性 | **有效**，但评审时 source_index.md 已被 reference_inventory.py 覆盖，见核验表 T1/T2/I2/I6 |\n")
    fh.write("| 原文来源 | 子代理会话记录，逐字抽取，未经改写 |\n\n")
    fh.write("## 一、评审原文（逐字）\n\n")
    fh.write(body.strip() + "\n")
    fh.write(VERDICT)

print("wrote reviewer_audit.md, review chars:", len(body))
