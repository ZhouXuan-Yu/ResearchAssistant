# -*- coding: utf-8 -*-
"""taxgate_test.py - prove check_taxonomy.py actually gates.

check_taxonomy.py honours HANA_HOME / HANA_WORKSPACE, so the gate can be exercised
in a throwaway sandbox without touching the real registry or config.

Phase A: an enabled skill that is NOT registered  -> must be reported unclassified, exit 1
Phase B: the same skill registered               -> must be clean, exit 0
"""
import io
import os
import shutil
import subprocess
import sys

WS = r"C:\Users\ZhouXuan\Desktop\OH-WorkSpace"
T = os.path.join(WS, "foundation", "tools", "_taxgate_test")
HANA = os.path.join(T, "hana")
WSX = os.path.join(T, "ws")
CONFIG = os.path.join(HANA, "agents", "agent-mu42qzfz", "config.yaml")
TAX = os.path.join(WSX, "foundation", "routing", "skill-taxonomy.yaml")
REAL_TAX = os.path.join(WS, "foundation", "routing", "skill-taxonomy.yaml")
SCRIPT = os.path.join(WS, "foundation", "routing", "check_taxonomy.py")
FAKE = "totally-unregistered-skill"

shutil.rmtree(T, ignore_errors=True)
os.makedirs(os.path.dirname(CONFIG), exist_ok=True)
os.makedirs(os.path.dirname(TAX), exist_ok=True)
os.makedirs(os.path.join(HANA, "skills"), exist_ok=True)

with io.open(CONFIG, "w", encoding="utf-8", newline="\n") as fh:
    fh.write("skills:\n  enabled:\n    - %s\n" % FAKE)
shutil.copy2(REAL_TAX, TAX)

env = dict(os.environ, HANA_HOME=HANA, HANA_WORKSPACE=WSX)


def run():
    r = subprocess.run([sys.executable, SCRIPT], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=env, timeout=120)
    return r.returncode, (r.stdout or "")


rc, out = run()
a_ok = (rc == 1 and "未分类: 1" in out and FAKE in out)
print("PHASE A (unregistered, enabled):")
print("   exit=%s  expect 1 | reported unclassified: %s" % (rc, "未分类: 1" in out))
for line in out.splitlines():
    if "未分类" in line or FAKE in line:
        print("   |", line.strip())
print("   ->", "OK" if a_ok else "BAD")

with io.open(TAX, encoding="utf-8") as fh:
    lines = fh.read().splitlines()
entry = "  %s: {group: A_topic_proposal, usage: [分析], role: secondary}" % FAKE
idx = next((i for i, l in enumerate(lines) if l.startswith("classifications:")), None)
if idx is None:
    raise SystemExit("temp taxonomy has no classifications block")
lines.insert(idx + 1, entry)
with io.open(TAX, "w", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(lines) + "\n")

rc2, out2 = run()
b_ok = (rc2 == 0 and "未分类: 0" in out2)
print("PHASE B (registered):")
print("   exit=%s  expect 0 | unclassified 0: %s" % (rc2, "未分类: 0" in out2))
for line in out2.splitlines():
    if "未分类" in line or "问题" in line:
        print("   |", line.strip())
print("   ->", "OK" if b_ok else "BAD")

print("\ntaxonomy gate test: %s" % ("PASS 2/2" if (a_ok and b_ok) else "FAIL"))
