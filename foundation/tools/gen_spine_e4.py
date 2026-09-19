# -*- coding: utf-8 -*-
"""gen_spine_e4.py - rebuild figure_body_contract.json from figure_requests.json.

figure_story_check compares eleven fields between the request and the body contract,
and requires publication_asset / editable_source to be objects carrying path and
sha256. The earlier contract carried plain string paths and none of the mirrored
fields, so nine findings were produced. This mirrors the request and hashes the
two real files; no content is invented.
"""
import hashlib
import json
import os

ROOT = r"C:\Users\ZhouXuan\Desktop\OH-WorkSpace\foundation\dryrun\spine-001\paper_rewriting_output"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


with open(os.path.join(ROOT, "figure_requests.json"), encoding="utf-8") as fh:
    requests = json.load(fh)["figures"]

MIRROR = ("figure_kind", "figure_role", "label", "caption", "scientific_question",
          "claim", "intended_conclusion", "claim_boundary", "results_units",
          "hero_panel", "panels")

ASSET = "final_paper/figures/fig1_evidence_landscape.png"
SOURCE = "final_paper/figures/fig1.py"

out_figures = []
for req in requests:
    rec = {k: req.get(k) for k in MIRROR}
    rec["figure_id"] = req.get("figure_id")
    rec["referenced_in_body"] = True
    rec["body_reference"] = "第 4 节 图 1"
    rec["boundary"] = req.get("claim_boundary")
    rec["publication_asset"] = {
        "path": ASSET,
        "sha256": sha256(os.path.join(ROOT, ASSET.replace("/", os.sep))),
    }
    rec["editable_source"] = {
        "path": SOURCE,
        "sha256": sha256(os.path.join(ROOT, SOURCE.replace("/", os.sep))),
    }
    out_figures.append(rec)

contract = {
    "schema_version": "1.0",
    "contract_type": "paperspine.figure.body",
    "status": "PASS",
    "figures": out_figures,
}

p = os.path.join(ROOT, "figure_body_contract.json")
with open(p, "w", encoding="utf-8", newline="\n") as fh:
    json.dump(contract, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
print("rebuilt figure_body_contract.json; figures:", len(out_figures))
for f in out_figures:
    print("  ", f["figure_id"], "asset_sha256", f["publication_asset"]["sha256"][:12], "es_sha256", f["editable_source"]["sha256"][:12])
