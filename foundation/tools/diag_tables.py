# -*- coding: utf-8 -*-
"""diag_tables.py - inspect what markdown_tables() actually returns for the bank."""
import sys
from pathlib import Path

sys.path.insert(0, r"C:\Users\ZhouXuan\.hanako\skills\paper-spine\scripts")
from _paper_spine_utils import markdown_tables  # noqa: E402

BANK = Path(r"C:\Users\ZhouXuan\Desktop\OH-WorkSpace\foundation\dryrun\spine-001\paper_rewriting_output\citation_support_bank.md")
txt = BANK.read_text(encoding="utf-8", errors="ignore")
print("chars:", len(txt))
tables = markdown_tables(txt)
print("tables found:", len(tables))
for i, t in enumerate(tables):
    print(f"  table[{i}] rows={len(t)} header={t[0] if t else None}")
    if t and len(t) > 1:
        print("    row1 cells:", len(t[1]), "|", [c[:28] for c in t[1]])
    if t and len(t) > 2:
        print("    row2 cells:", len(t[2]), "|", [c[:28] for c in t[2]])

print("-" * 50)
for i, line in enumerate(txt.splitlines()[:12]):
    print(f"{i:02d} {line[:110]}")
