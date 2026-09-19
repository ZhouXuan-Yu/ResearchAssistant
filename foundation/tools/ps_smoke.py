# -*- coding: utf-8 -*-
"""ps_smoke.py - smoke test for the installed paper-spine skill.

1) byte-compile every bundled .py (catches syntax errors under this Python)
2) run --help on a few entry scripts under a short timeout
"""
import compileall
import os
import subprocess
import sys

ROOT = r"C:\Users\ZhouXuan\.hanako\skills\paper-spine"
SCRIPTS = os.path.join(ROOT, "scripts")

print("python:", sys.version.split()[0])
print("=" * 60)
print("[1] byte-compile all bundled scripts")
ok = compileall.compile_dir(SCRIPTS, quiet=2, force=True)
print("compileall result:", "OK" if ok else "HAS ERRORS")

print("=" * 60)
print("[2] --help on entry scripts")
SAMPLE = [
    "artifact_check.py",
    "citation_verification_en.py",
    "citation_bank_check.py",
    "figure_story_check.py",
    "figure_reference_check.py",
    "visual_readiness_check.py",
    "usage_ledger.py",
    "reference_inventory.py",
    "contribution_check.py",
    "results_validation_check.py",
]
for name in SAMPLE:
    p = os.path.join(SCRIPTS, name)
    if not os.path.exists(p):
        print(f"  {name}: MISSING")
        continue
    try:
        r = subprocess.run(
            [sys.executable, p, "--help"],
            capture_output=True,
            text=True,
            timeout=45,
            encoding="utf-8",
            errors="replace",
        )
        first = (r.stdout or r.stderr or "").strip().splitlines()
        head = first[0][:90] if first else "(no output)"
        print(f"  {name}: rc={r.returncode} | {head}")
    except subprocess.TimeoutExpired:
        print(f"  {name}: TIMEOUT")
    except Exception as exc:  # noqa: BLE001
        print(f"  {name}: {type(exc).__name__} {str(exc)[:60]}")

print("=" * 60)
print("[3] references present")
refs = os.path.join(ROOT, "references")
n = len(os.listdir(refs)) if os.path.isdir(refs) else -1
print("references entries:", n)
