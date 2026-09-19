# -*- coding: utf-8 -*-
"""negtest_contracts.py - prove check_contracts.py actually rejects bad contracts.

A checker that only ever passes is worthless. Each case below violates exactly one
rule from research/00-governance/contracts.md and must be rejected.
"""
import io
import os
import subprocess
import sys

BASE = r"C:\Users\ZhouXuan\Desktop\OH-WorkSpace"
OUT = os.path.join(BASE, "foundation", "tools", "_contract_negtest")
GOOD_ART = "research/00-governance/contracts.md"

HEAD = """contract_version: "1.0"
stage: {stage}
phase: {phase}
autonomy: {autonomy}
produced_by: negtest
produced_at: "2026-09-19T16:30:00+08:00"
upstream: []
inputs: []
artifacts:
  - {artifact}
gates:
{gates}
reproducibility:
  data_version: {dv}
  code_commit: {cc}
  seed: {sd}
unresolved: {unresolved}
"""

CASES = {
    "N1_autonomy_too_strong.yaml": dict(
        stage="S1", phase="Creation", autonomy="可高自主", artifact=GOOD_ART,
        gates="  g: pass", dv='"n/a"', cc='"n/a"', sd='"n/a"', unresolved="[]",
        expect="exceeds the floor"),
    "N2_missing_artifact.yaml": dict(
        stage="S2", phase="Creation", autonomy="可高自主",
        artifact="research/00-governance/does-not-exist.md",
        gates="  g: pass", dv='"n/a"', cc='"n/a"', sd='"n/a"', unresolved="[]",
        expect="artifact does not exist"),
    "N3_s3_empty_reproducibility.yaml": dict(
        stage="S3", phase="Creation", autonomy="人主导", artifact=GOOD_ART,
        gates="  g: pass", dv='"n/a"', cc='"n/a"', sd='"n/a"', unresolved="[]",
        expect="S3 reproducibility triple is incomplete"),
    "N4_gate_fail.yaml": dict(
        stage="S2", phase="Creation", autonomy="可高自主", artifact=GOOD_ART,
        gates="  g: fail", dv='"n/a"', cc='"n/a"', sd='"n/a"', unresolved="[]",
        expect="FAIL (a failing gate"),
    "N5_blocked_without_unresolved.yaml": dict(
        stage="S4", phase="Creation", autonomy="可高自主", artifact=GOOD_ART,
        gates="  g: blocked", dv='"n/a"', cc='"n/a"', sd='"n/a"', unresolved="[]",
        expect="blocked"),
    "N6_phase_mismatch.yaml": dict(
        stage="S5", phase="Creation", autonomy="需人确认", artifact=GOOD_ART,
        gates="  g: pass", dv='"n/a"', cc='"n/a"', sd='"n/a"', unresolved="[]",
        expect="does not match"),
}

os.makedirs(OUT, exist_ok=True)
for name, spec in CASES.items():
    body = HEAD.format(stage=spec["stage"], phase=spec["phase"], autonomy=spec["autonomy"],
                       artifact=spec["artifact"], gates=spec["gates"], dv=spec["dv"],
                       cc=spec["cc"], sd=spec["sd"], unresolved=spec["unresolved"])
    with io.open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(body)

r = subprocess.run([sys.executable, os.path.join(BASE, "foundation", "tools", "check_contracts.py"), OUT],
                   capture_output=True, text=True, encoding="utf-8", errors="replace")
out = r.stdout or ""
print(out)

ok = 0
for name, spec in CASES.items():
    rejected = (f"`{name}`: **FAIL**" in out)
    matched = spec["expect"] in out
    ok += 1 if (rejected and matched) else 0
    print(f"  {'OK ' if (rejected and matched) else 'BAD'} {name} -> rejected={rejected} reason_matched={matched}")

print(f"\nnegative tests passed: {ok}/{len(CASES)}  (validator exit code {r.returncode}, expected 1)")
