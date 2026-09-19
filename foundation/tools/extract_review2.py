# -*- coding: utf-8 -*-
"""extract_review2.py - append the round-2 independent review to reviewer_audit.md.

Copied verbatim from the sub-agent session file (no retyping), followed by the
research assistant's per-finding verification.
"""
import io
import json
import os

SRC = r"C:\Users\ZhouXuan\.hanako\agents\agent-mu42qzfz\subagent-sessions\direct\2026-09-19T07-16-00-954Z_01a0b885-a33a-73e1-8d98-ebe4dc15ad14.jsonl"
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

APPENDIX = """
---

### 2.2 科研助手对第二轮发现的独立核验

| 发现 | 核验结论 | 说明 |
|---|---|---|
| N1 摘要承诺证据强度分级而正文无此节 | **成立** | §4 已补分级表（有数值可核 4 / 仅定性 2 / 不可知 18） |
| N2 "标准见第 2 节"为悬空指针 | **成立** | §2 已增写载体分级标准，四处指针落地 |
| N3 research_dossier §4 分级与"仅 6 条有摘要"互斥 | **成立** | 该表将无摘要的 R01/R03/R04 判为"有指标"，且漏列 R05/R06/R07/R19/R20/R21；已按 E-A 重写 |
| N4 confirmed_motivation 残留旧断言 | **成立** | 原文"三项俱全 3 条"与 E-A 冲突，已改 |
| N5 GAP-3 举例与 E-A/E-C 打架 | **成立** | E-A2（R17）已给 FLOPs，E-A4（R19）未记任何数值表述；已改 |
| N6 "12 条未引注"应为 11 | **成立** | 按正文实点为被引 13 / 未引 11；已改 |
| N7 年份未同步至 3 份伴档 | **成立** | 已统一 2021–2026 |
| N8 引用核验残差未入局限；审计表 C01 重复行 | **部分成立** | 局限已补；但 C01 重复属"R01 支撑两条论断"的固有设计（25 行 / 24 唯一源），非计数错误，不按缺陷处理 |
| N9–N13 | **成立** | 均已按建议修改 |
"""

with io.open(OUT, "a", encoding="utf-8", newline="\n") as fh:
    fh.write("\n---\n\n## 二、第二轮评审（对修订版的修复验证）\n\n")
    fh.write("| 项 | 值 |\n|---|---|\n")
    fh.write("| 评审者 | 独立子代理（agent-mqb8td2n，交流者 / mimo-v2.5-pro） |\n")
    fh.write("| 权限 | 只读；未修改任何文件 |\n")
    fh.write("| 评审对象 | 修订后的 manuscript / evidence_bank / claim_register / source_index / structured_review，旁证 8 份 |\n")
    fh.write("| 评审者自述 | 首次读到旧快照，已用 grep 对账并重读，判定以当前磁盘文本为准 |\n")
    fh.write("| 产物 | 修复验证 23 条 + 新问题 13 条（N1–N13） |\n\n")
    fh.write("### 2.1 评审原文（逐字）\n\n")
    fh.write(body.strip() + "\n")
    fh.write(APPENDIX)

print("appended round-2 review, chars:", len(body))
