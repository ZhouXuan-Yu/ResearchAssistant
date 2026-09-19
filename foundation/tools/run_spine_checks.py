# -*- coding: utf-8 -*-
"""run_spine_checks.py - run the paper-spine gate scripts against the drill tree."""
import os
import subprocess
import sys

SK = r"C:\Users\ZhouXuan\.hanako\skills\paper-spine\scripts"
ROOT = r"C:\Users\ZhouXuan\Desktop\OH-WorkSpace\foundation\dryrun\spine-001\paper_rewriting_output"

JOBS = [
    ("artifact_check.py", [ROOT, "--markdown", "--write"]),
    ("contribution_check.py", [ROOT, "--markdown", "--write"]),
    ("citation_bank_check.py", [os.path.join(ROOT, "citation_support_bank.md"), "--markdown", "--write"]),
    ("citation_quality_audit.py", [ROOT, "--markdown", "--write"]),
    ("results_validation_check.py", [ROOT, "--markdown", "--write"]),
    ("figure_story_check.py", [ROOT, "--phase", "final", "--markdown", "--write"]),
    ("figure_reference_check.py", [ROOT, "--phase", "final", "--write"]),
    ("visual_readiness_check.py", [ROOT, "--markdown", "--write"]),
    ("visual_readiness_check.py", [ROOT, "--prepare", "--markdown", "--write"]),
    ("usage_ledger.py", [ROOT, "--markdown", "--write"]),
    ("reference_inventory.py", ["--output-dir", ROOT]),
    ("integrity_audit.py", [ROOT, "--markdown", "--write"]),
]

print("=" * 70)
for name, args in JOBS:
    p = os.path.join(SK, name)
    if not os.path.exists(p):
        print(f"[{name}] MISSING")
        continue
    try:
        r = subprocess.run([sys.executable, p] + args, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=240, cwd=ROOT)
    except subprocess.TimeoutExpired:
        print(f"[{name}] TIMEOUT")
        continue
    out = (r.stdout or "").strip()
    err = (r.stderr or "").strip()
    print(f"[{name}] rc={r.returncode}")
    if out:
        for line in out.splitlines()[:14]:
            print("   |", line[:150])
    if err:
        for line in err.splitlines()[:4]:
            print("   !", line[:150])
    print("-" * 70)
