# -*- coding: utf-8 -*-
"""measure_void.py - report the unused vertical space at the bottom of each PDF page.

Heuristic: last ink row on the page (text blocks + images) versus page height.
"""
import os

import pymupdf

ROOT = r"C:\Users\ZhouXuan\Desktop\OH-WorkSpace\foundation\dryrun\spine-001\paper_rewriting_output"
pdf = os.path.join(ROOT, "final_paper", "paper.pdf")

with pymupdf.open(pdf) as doc:
    for i, page in enumerate(doc, 1):
        h = page.rect.height
        last = 0.0
        for b in page.get_text("blocks"):
            last = max(last, b[3])
        for img in page.get_image_info():
            last = max(last, img["bbox"][3])
        frac = 1.0 - last / h
        print("page %d: last_ink_bottom=%.1fpt  page_h=%.1fpt  trailing_void=%.1f%%" % (i, last, h, frac * 100))
