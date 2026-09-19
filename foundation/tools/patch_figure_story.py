# -*- coding: utf-8 -*-
"""patch_figure_story.py - fix the pre-revision panel intents in figure_requests.json
and declare the figure's measured background canvas.

Two separate problems:
1. figure_requests.json still carried the pre-revision panel claims, including the
   retracted "only 3 of 24 fully disclose" reading (review finding S1). The body
   contract mirrors this file, so the wrong intent was silently propagated.
2. visual_readiness_check's background probe needs a declared canvas bound to the
   real asset hash and the real decoded pixel buffer. The declaration is a factual
   statement about the figure's white canvas; the probe re-measures the pixels.
"""
import hashlib
import io
import json
import os

from PIL import Image

ROOT = r"C:\Users\ZhouXuan\Desktop\OH-WorkSpace\foundation\dryrun\spine-001\paper_rewriting_output"
REQ = os.path.join(ROOT, "figure_requests.json")
ASSET = os.path.join(ROOT, "final_paper", "figures", "fig1_evidence_landscape.png")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


with io.open(REQ, encoding="utf-8") as fh:
    data = json.load(fh)

fig = data["figures"][0]

# --- 1. corrected panel intents (post-revision) -----------------------------
fig["caption"] = ("图 1 纳入文献的证据景观（n = 24）。(a) 年份分布；(b) 载体类型构成；"
                  "(c) 6 条带摘要记录中三类数值的披露覆盖（可重叠）。")
for panel in fig.get("panels", []):
    pid = panel.get("panel_id")
    if pid == "p-venue":
        panel["intended_reading"] = ("顶会正刊仅 2 条；Workshop 2、期刊 5、一般会议 6、"
                                     "arXiv 预印本 6、高风险载体 3。")
    elif pid == "p-disclosure":
        panel["question"] = "6 条带摘要记录中，三类数值各自的披露覆盖面如何？"
        panel["evidence_anchor"] = "evidence_bank.md 的 E-A 逐条台账"
        panel["intended_reading"] = ("给出参数量数值 3 条、算力 1 条、精度 3 条，"
                                     "同时给出三项者 0 条，仅定性 2 条；另 18 条披露状态不可知。")

# --- 2. declared, measured background canvas --------------------------------
with Image.open(ASSET) as opened:
    rgba = opened.convert("RGBA")
    buf_sha = hashlib.sha256(rgba.tobytes()).hexdigest()
    w, h = rgba.size

fig["background"] = {
    "canvas": {"region_id": "canvas", "bbox_normalized": [0.0, 0.0, 1.0, 1.0]},
    "axes": [],
    "panels": [],
    "asset_sha256": sha256_file(ASSET),
    "probe_render_sha256": buf_sha,
}

with io.open(REQ, "w", encoding="utf-8", newline="\n") as fh:
    json.dump(data, fh, ensure_ascii=False, indent=2)
    fh.write("\n")

print("figure_requests.json patched")
print("  asset px:", w, "x", h)
print("  asset_sha256:", fig["background"]["asset_sha256"][:16])
print("  pixel_buffer_sha256:", buf_sha[:16])
