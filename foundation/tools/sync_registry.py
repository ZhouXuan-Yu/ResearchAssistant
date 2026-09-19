# -*- coding: utf-8 -*-
"""sync_registry.py - keep the two registry copies from drifting apart.

The router documents point at skills/research-os-router/references/*.yaml, while
check_taxonomy.py prefers foundation/routing/*.yaml. They are two copies of one
registry and had already diverged (the workspace copy had paper-spine registered,
the packaged copy did not).

Canonical = foundation/routing/  (it is the copy the gate actually reads and the
copy that receives new registrations). The packaged copy is a mirror.

Usage:
  python sync_registry.py --check    # report drift only; exit 1 when out of sync
  python sync_registry.py --apply    # mirror canonical -> packaged, then verify
"""
import argparse
import shutil
import sys
from pathlib import Path

WS = Path(r"C:\Users\ZhouXuan\Desktop\OH-WorkSpace")
CANON = WS / "foundation" / "routing"
MIRROR = Path(r"C:\Users\ZhouXuan\.hanako\skills\research-os-router\references")

PAIRS = (
    ("skill-taxonomy.yaml", "taxonomy.yaml"),
    ("routing-rules.yaml", "routing-rules.yaml"),
    ("RESEARCH-SKILL-MAP.md", "RESEARCH-SKILL-MAP.md"),
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    if not (args.check or args.apply):
        ap.error("pass --check or --apply")

    drift = []
    for src_name, dst_name in PAIRS:
        src, dst = CANON / src_name, MIRROR / dst_name
        if not src.exists():
            print(f"  canonical missing: {src}")
            return 1
        same = dst.exists() and src.read_bytes() == dst.read_bytes()
        print(f"  {src_name} -> references/{dst_name}: {'in sync' if same else 'DRIFTED'}")
        if not same:
            drift.append((src, dst))

    if not drift:
        print("registry in sync")
        return 0
    if args.check:
        print(f"OUT OF SYNC: {len(drift)} file(s); run --apply to mirror canonical -> packaged")
        return 1

    for src, dst in drift:
        shutil.copy2(src, dst)
        print("  mirrored:", dst)
    bad = [d for s, d in drift if s.read_bytes() != d.read_bytes()]
    print("apply verified" if not bad else f"STILL DIFFERENT: {bad}")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
