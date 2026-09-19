# -*- coding: utf-8 -*-
"""check_contracts.py - validate stage contracts against Stage Contracts v1.0.

Spec: research/00-governance/contracts.md
Usage:
    python check_contracts.py <file-or-dir> [--base <project-root>] [--markdown]

Exit code 0 only when every contract passes. A "fail" gate, a missing artifact,
a stage whose autonomy is below the floor, or an empty S3 reproducibility triple
all fail the contract.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

PHASE_OF = {
    "S1": "Creation", "S2": "Creation", "S3": "Creation", "S4": "Creation",
    "S5": "Writing", "S6": "Validation", "S7": "Validation", "S8": "Dissemination",
}
AUTONOMY_FLOOR = {
    "S1": "人主导", "S2": "可高自主", "S3": "人主导", "S4": "可高自主",
    "S5": "需人确认", "S6": "可高自主", "S7": "需人确认", "S8": "可高自主",
}
# 自主度强度：数值越大 = AI 自主性越强；声明值不得强于下限
STRENGTH = {"可高自主": 2, "需人确认": 1, "人主导": 0}
REQUIRED = ("contract_version", "stage", "phase", "autonomy", "produced_by",
            "produced_at", "upstream", "inputs", "artifacts", "gates",
            "reproducibility", "unresolved")
GATE_VALUES = {"pass", "fail", "n_a", "blocked"}
REPRO_KEYS = ("data_version", "code_commit", "seed")
N_A_TOKENS = {"n/a", "na", "none", "", "-"}


def check_one(path: Path, base: Path) -> tuple[bool, list[str]]:
    findings: list[str] = []
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        return False, [f"YAML parse error: {exc}"]
    if not isinstance(data, dict):
        return False, ["contract must be a mapping"]

    for key in REQUIRED:
        if key not in data:
            findings.append(f"missing required field: {key}")
    if findings:
        return False, findings

    stage = str(data["stage"]).strip().upper()
    if stage not in PHASE_OF:
        findings.append(f"invalid stage: {stage}")
        return False, findings

    if str(data["phase"]).strip() != PHASE_OF[stage]:
        findings.append(f"phase {data['phase']!r} does not match {stage} (expected {PHASE_OF[stage]})")

    autonomy = str(data["autonomy"]).strip()
    floor = AUTONOMY_FLOOR[stage]
    if autonomy not in STRENGTH:
        findings.append(f"invalid autonomy: {autonomy}")
    elif STRENGTH[autonomy] > STRENGTH[floor]:
        findings.append(f"autonomy {autonomy} exceeds the floor for {stage} (max {floor})")

    arts = data["artifacts"]
    if not isinstance(arts, list) or not arts:
        findings.append("artifacts must be a non-empty list")
    else:
        for rel in arts:
            if not (base / str(rel)).exists():
                findings.append(f"artifact does not exist: {rel}")

    gates = data["gates"]
    if not isinstance(gates, dict) or not gates:
        findings.append("gates must be a non-empty mapping")
    else:
        for name, value in gates.items():
            v = str(value).strip()
            if v not in GATE_VALUES:
                findings.append(f"gate {name}: invalid value {value!r}")
            elif v == "fail":
                findings.append(f"gate {name}: FAIL (a failing gate invalidates the contract)")
        if any(str(v).strip() == "blocked" for v in gates.values()):
            if not data.get("unresolved"):
                findings.append("a gate is 'blocked' but unresolved is empty; a blocked gate must be written down")

    repro = data["reproducibility"]
    if not isinstance(repro, dict):
        findings.append("reproducibility must be a mapping")
    else:
        for key in REPRO_KEYS:
            if key not in repro:
                findings.append(f"reproducibility missing key: {key}")
        if stage == "S3":
            weak = [k for k in REPRO_KEYS if str(repro.get(k, "")).strip().lower() in N_A_TOKENS]
            if weak:
                findings.append("S3 reproducibility triple is incomplete: " + ", ".join(weak))

    if not isinstance(data["unresolved"], list):
        findings.append("unresolved must be a list (use [] when nothing is outstanding)")

    return (not findings), findings


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--base", default=r"C:\Users\ZhouXuan\Desktop\OH-WorkSpace")
    ap.add_argument("--markdown", action="store_true")
    args = ap.parse_args()

    target = Path(args.path)
    base = Path(args.base)
    files = sorted(target.glob("*.yaml")) + sorted(target.glob("*.yml")) if target.is_dir() else [target]
    if not files:
        print("no contract files found")
        return 2

    ok_all = True
    lines = ["# Stage Contract Check", ""]
    for f in files:
        ok, findings = check_one(f, base)
        ok_all = ok_all and ok
        status = "PASS" if ok else "FAIL"
        lines.append(f"- `{f.name}`: **{status}**")
        for item in findings:
            lines.append(f"    - {item}")
    lines += ["", f"Total: {len(files)} | Failed: {sum(1 for f in files if not check_one(f, base)[0])}", ""]
    text = "\n".join(lines)
    print(text)
    if args.markdown:
        Path("contract_check.md").write_text(text, encoding="utf-8")
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
