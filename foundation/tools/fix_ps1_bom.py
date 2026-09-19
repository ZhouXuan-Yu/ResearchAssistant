# -*- coding: utf-8 -*-
"""fix_ps1_bom.py - ensure UTF-8-with-BOM on PowerShell scripts.

Why: PowerShell 5.1 decodes a BOM-less UTF-8 .ps1 as ANSI, so any Chinese literal
inside becomes mojibake and usually a parse error. Editing tools commonly write
UTF-8 without BOM, so run this after editing any .ps1 that contains non-ASCII.

Usage: python fix_ps1_bom.py [dir]     (default: foundation/tools)
"""
import io
import os
import sys

DEFAULT = r"C:\Users\ZhouXuan\Desktop\OH-WorkSpace\foundation\tools"
root = sys.argv[1] if len(sys.argv) > 1 else DEFAULT

fixed, ok, ascii_only = [], [], []
for dirpath, _dirs, files in os.walk(root):
    for name in files:
        if not name.lower().endswith(".ps1"):
            continue
        p = os.path.join(dirpath, name)
        raw = open(p, "rb").read()
        if raw.startswith(b"\xef\xbb\xbf"):
            ok.append(name)
            continue
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            print("NOT UTF-8, skipped:", p)
            continue
        if text.isascii():
            ascii_only.append(name)
            continue
        with io.open(p, "w", encoding="utf-8-sig", newline="") as fh:
            fh.write(text)
        fixed.append(name)

print("already had BOM:", len(ok), ok)
print("ascii-only (BOM not needed):", len(ascii_only), ascii_only)
print("BOM added:", len(fixed), fixed)
