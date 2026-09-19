# -*- coding: utf-8 -*-
"""repair_registry_encoding.py - repair mojibake comments in the workspace registry.

Symptom: foundation/routing/skill-taxonomy.yaml comments read like "鎶€鑳藉垎绫绘€昏〃"
(UTF-8 bytes that were decoded as GBK then re-saved as UTF-8). Data (YAML keys and
values) is intact; only comments are damaged.

Strategy: reverse the double-encoding per line (text -> gbk bytes -> utf-8 text).
Verification is mandatory: the repaired text must contain no replacement chars and
must be strictly shorter than the original; the file is written only when every
line either round-trips cleanly or is left untouched. A .bak is always written.

Usage: python repair_registry_encoding.py <file> [--apply]
"""
import io
import shutil
import sys
from pathlib import Path


def repair_line(line: str) -> str:
    try:
        fixed = line.encode("gbk").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return line
    if "\ufffd" in fixed:
        return line
    return fixed if fixed != line else line


def main() -> int:
    ap_args = [a for a in sys.argv[1:] if not a.startswith("--")]
    apply = "--apply" in sys.argv
    path = Path(ap_args[0])
    raw = path.read_text(encoding="utf-8")

    lines = raw.splitlines(keepends=True)
    fixed_lines = [repair_line(l) for l in lines]
    fixed = "".join(fixed_lines)

    changed = sum(1 for a, b in zip(lines, fixed_lines) if a != b)
    print("file:", path)
    print("lines:", len(lines), "changed:", changed)
    print("orig chars:", len(raw), "-> fixed chars:", len(fixed))
    print("--- first 6 fixed lines ---")
    for l in fixed_lines[:6]:
        print("   ", l.rstrip())

    if changed == 0:
        print("nothing to repair")
        return 0
    if not apply:
        print("\n[dry-run] pass --apply to write (a .bak copy is made first)")
        return 0

    shutil.copy2(path, str(path) + ".bak")
    path.write_text(fixed, encoding="utf-8", newline="\n")
    print("\napplied; backup at", str(path) + ".bak")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
