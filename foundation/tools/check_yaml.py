# -*- coding: utf-8 -*-
"""check_yaml.py - validate the routing governance YAML files parse and summarise keys."""
import sys

try:
    import yaml
except ImportError:
    print("PyYAML not available")
    sys.exit(2)

BASE = r"C:\Users\ZhouXuan\Desktop\OH-WorkSpace\foundation\routing"

for name, expect in (("routing-rules.yaml", "routing"), ("skill-taxonomy.yaml", "taxonomy")):
    p = BASE + "\\" + name
    print("=" * 60)
    print(name)
    try:
        with open(p, "r", encoding="utf-8") as fh:
            d = yaml.safe_load(fh)
    except Exception as exc:  # noqa: BLE001
        print("  PARSE FAIL:", type(exc).__name__, str(exc)[:200])
        continue
    print("  top keys:", list(d.keys()))
    if expect == "routing":
        g = d.get("groups", {})
        print("  groups:", len(g))
        print("  intents:", len(d.get("intents", [])))
        lor = g.get("L_orchestration", {})
        print("  L_orchestration:", lor)
        hits = [i for i in d.get("intents", []) if i.get("skill") == "paper-spine"]
        print("  paper-spine intents:", len(hits), hits)
    else:
        c = d.get("classifications", {})
        print("  classifications:", len(c))
        print("  paper-spine:", c.get("paper-spine"))
