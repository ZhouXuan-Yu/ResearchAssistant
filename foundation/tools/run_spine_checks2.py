# -*- coding: utf-8 -*-
"""run_spine_checks2.py - post-revision gate run.

Same as run_spine_checks.py but with reference_inventory.py removed, because that
script overwrites reference_materials/source_index.md (its own output path) and
would clobber the restored drill bibliography. That collision is recorded in the
drill report.
"""
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
    ("usage_ledger.py", [ROOT, "--markdown", "--write"]),
    ("integrity_audit.py", [ROOT, "--markdown", "--write"]),
]

for name, args in JOBS:
    p = os.path.join(SK, name)
    if not os.path.exists(p):
        print("[%s] MISSING" % name)
        continue
    try:
        r = subprocess.run([sys.executable, "-u", p] + args, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=300, cwd=ROOT)
    except subprocess.TimeoutExpired:
        print("[%s] TIMEOUT" % name)
        continue
    print("=" * 70)
    print("[%s] rc=%s" % (name, r.returncode))
    for line in (r.stdout or "").strip().splitlines()[:16]:
        print("   |", line[:150])
    for line in (r.stderr or "").strip().splitlines()[:4]:
        print("   !", line[:150])
print("ALL DONE")
