# -*- coding: utf-8 -*-
"""check_surfaces.py - verify the delivered PDF text against the required content markers.

Reads the real PDF bytes with PyMuPDF and counts markers that must be absent/present.
"""
import os

import pymupdf

ROOT = r"C:\Users\ZhouXuan\Desktop\OH-WorkSpace\foundation\dryrun\spine-001\paper_rewriting_output"
pdf = os.path.join(ROOT, "final_paper", "paper.pdf")

with pymupdf.open(pdf) as doc:
    text = "".join(page.get_text() for page in doc)
    npages = len(doc)

MUST_PRESENT = ["2021", "R24", "四项文献层空白", "GAP-4", "纳入语料全集", "18 条", "同时给出三项者为 0 条", "三项俱全 0 条"]
MUST_ABSENT = ["`", "三项文献层空白", "16 条记录无摘要", "2020", "3 条同时报告参数量", "三、"]

print("pages:", npages)
for s in MUST_PRESENT:
    print("  present  %-22s %s" % (s, text.count(s)))
for s in MUST_ABSENT:
    print("  absent   %-22s %s" % (s, text.count(s)))
