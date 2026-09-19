# -*- coding: utf-8 -*-
"""zoom_figure.py - render the figure band of a PDF page at high dpi for legibility review."""
import os
import sys

import pymupdf

ROOT = r"C:\Users\ZhouXuan\Desktop\OH-WorkSpace\foundation\dryrun\spine-001\paper_rewriting_output"
pdf = os.path.join(ROOT, "final_paper", "paper.pdf")
out = os.path.join(ROOT, "visual_audit", "preview", "fig-band-200dpi.png")
page_no = int(sys.argv[1]) if len(sys.argv) > 1 else 3

with pymupdf.open(pdf) as doc:
    page = doc[page_no - 1]
    r = page.rect
    clip = pymupdf.Rect(0.08 * r.width, 0.05 * r.height, 0.95 * r.width, 0.40 * r.height)
    pix = page.get_pixmap(dpi=200, clip=clip, colorspace=pymupdf.csRGB, alpha=False)
    pix.save(out)
    print("wrote", out, pix.width, "x", pix.height, os.path.getsize(out), "bytes")
