#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能分类准入校验（只读）
========================
校验：每个"启用的技能"是否都已在 skill-taxonomy.yaml 中分类（显式或按模式）。
用于执行"新技能必须审核分类后才能留存"这条规矩。

用法:
  python check_taxonomy.py
  python check_taxonomy.py --json report.json
退出码: 0 全部分类; 1 存在未分类/异常
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HANA_HOME = Path(os.environ.get("HANA_HOME", r"C:\Users\ZhouXuan\.hanako"))
WORKSPACE = Path(os.environ.get("HANA_WORKSPACE", r"C:\Users\ZhouXuan\Desktop\OH-WorkSpace"))
TAXONOMY = None
_HERE = Path(__file__).resolve().parent
for _c in (Path(os.environ.get("HANA_TAXONOMY", "")) if os.environ.get("HANA_TAXONOMY") else None,
           WORKSPACE / "foundation" / "routing" / "skill-taxonomy.yaml",
           _HERE.parent / "references" / "taxonomy.yaml"):
    if _c and Path(_c).exists():
        TAXONOMY = Path(_c)
        break
if TAXONOMY is None:
    TAXONOMY = WORKSPACE / "foundation" / "routing" / "skill-taxonomy.yaml"
CONFIG = HANA_HOME / "agents" / "agent-mu42qzfz" / "config.yaml"
SKILLS_DIR = HANA_HOME / "skills"


def enabled_skills() -> list[str]:
    txt = CONFIG.read_text(encoding="utf-8", errors="replace")
    in_skills = in_en = False
    out = []
    for line in txt.splitlines():
        if re.match(r"^[^\s#]", line):
            if in_en:
                break
            in_skills = bool(re.match(r"^skills\s*:", line))
            continue
        if not in_skills:
            continue
        if re.match(r"^\s+enabled\s*:\s*$", line):
            in_en = True
            continue
        if in_en:
            m = re.match(r"^\s+-\s+(\S.*?)\s*$", line)
            if m:
                out.append(m.group(1))
            elif line.strip():
                break
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json")
    args = ap.parse_args()

    try:
        import yaml
    except Exception:
        print("需要 PyYAML：python -m pip install pyyaml")
        return 2

    tax = yaml.safe_load(TAXONOMY.read_text(encoding="utf-8"))
    groups = tax.get("functional_groups", {})
    usages = set(tax.get("usage_types", {}))
    roles = set(tax.get("roles", {}))
    cls = tax.get("classifications", {}) or {}
    patterns = tax.get("patterns", []) or []

    problems, unclassified, matched_by_pattern, not_enabled = [], [], [], []

    on_disk = {d.name for d in SKILLS_DIR.iterdir() if d.is_dir()} if SKILLS_DIR.exists() else set()
    enabled = enabled_skills()

    # 1) 显式分类的字段完整性
    for name, meta in cls.items():
        if meta.get("group") not in groups:
            problems.append(f"{name}: 功能组非法 {meta.get('group')}")
        bad_u = [u for u in (meta.get("usage") or []) if u not in usages]
        if bad_u:
            problems.append(f"{name}: 用途类型非法 {bad_u}")
        if meta.get("role") not in roles:
            problems.append(f"{name}: 角色非法 {meta.get('role')}")
        if name not in enabled:
            not_enabled.append(name)

    # 2) 每个启用技能都要能被分类
    for name in enabled:
        if name in cls:
            continue
        hit = next((p for p in patterns if re.search(p["regex"], name)), None)
        if hit:
            matched_by_pattern.append((name, hit["group"]))
        else:
            unclassified.append(name)

    print("# 技能分类准入校验")
    print(f"- 启用技能: {len(enabled)}")
    print(f"- 显式分类: {len(cls)}")
    print(f"- 模式归类: {len(matched_by_pattern)}")
    print(f"- **未分类: {len(unclassified)}**")
    print(f"- 字段/一致性问题: {len(problems)}")
    print(f"- 已分类但未启用（提示，不算错误）: {len(not_enabled)}")
    if unclassified:
        print("\n## 未分类（必须补入 skill-taxonomy.yaml）")
        for n in unclassified:
            print(f"  - {n}")
    if problems:
        print("\n## 问题")
        for p in problems:
            print(f"  - {p}")
    if not_enabled:
        print("\n## 已分类但未启用")
        for n in not_enabled:
            print(f"  - {n}")
    if not unclassified and not problems:
        print("\n全部技能均已分类，准入规则满足。")

    if args.json:
        Path(args.json).write_text(json.dumps({
            "enabled": len(enabled), "explicit": len(cls),
            "pattern": len(matched_by_pattern), "unclassified": unclassified,
            "problems": problems}, ensure_ascii=False, indent=2), encoding="utf-8")

    return 0 if (not unclassified and not problems) else 1


if __name__ == "__main__":
    raise SystemExit(main())
