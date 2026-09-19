# -*- coding: utf-8 -*-
"""preview_pages.py - rasterise the final PDF for direct visual inspection.

Uses PyMuPDF (available) so pages can be inspected before the Poppler-bound
receipt pass runs. Output is a scratch preview, not a receipt.
"""
import os
import sys

import pymupdf

ROOT = r"C:\Users\ZhouXuan\Desktop\OH-WorkSpace\foundation\dryrun\spine-001\paper_rewriting_output"
OUT = os.path.join(ROOT, "visual_audit", "preview")
DPI = int(sys.argv[1]) if len(sys.argv) > 1 else 96

os.makedirs(OUT, exist_ok=True)
pdf = os.path.join(ROOT, "final_paper", "paper.pdf")

with pymupdf.open(pdf) as doc:
    print("pages:", len(doc))
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=DPI, colorspace=pymupdf.csRGB, alpha=False)
        p = os.path.join(OUT, "page-%02d.png" % (i + 1))
        pix.save(p)
        print("  ", p, pix.width, "x", pix.height, os.path.getsize(p), "bytes")
