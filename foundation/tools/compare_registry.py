# -*- coding: utf-8 -*-
"""compare_registry.py - structural comparison of the two registry copies.

The router reads skills/research-os-router/references/*.yaml while the gate script
prefers foundation/routing/*.yaml. If they disagree, the registry has drifted.
Comparison ignores comments (yaml.safe_load drops them), so it answers the real
question: is the DATA still in sync?
"""
import io

import yaml

A = r"C:\Users\ZhouXuan\.hanako\skills\research-os-router\references"
B = r"C:\Users\ZhouXuan\Desktop\OH-WorkSpace\foundation\routing"


def load(p):
    with io.open(p, encoding="utf-8", errors="replace") as fh:
        return yaml.safe_load(fh)


for name in ("taxonomy.yaml", "routing-rules.yaml"):
    pa = f"{A}\\{name}"
    pb = f"{B}\\" + ("skill-taxonomy.yaml" if name == "taxonomy.yaml" else name)
    a, b = load(pa), load(pb)
    print("=" * 60)
    print("file:", name)
    if name == "taxonomy.yaml":
        ca, cb = a.get("classifications", {}), b.get("classifications", {})
        print("  classifications: skill=%d workspace=%d" % (len(ca), len(cb)))
        only_a = sorted(set(ca) - set(cb))
        only_b = sorted(set(cb) - set(ca))
        diff = sorted(k for k in set(ca) & set(cb) if ca[k] != cb[k])
        print("  only in skill   :", only_a)
        print("  only in workspace:", only_b)
        print("  differing entries:", diff)
        print("  groups equal:", a.get("functional_groups") == b.get("functional_groups"))
        print("  patterns equal:", a.get("patterns") == b.get("patterns"))
    else:
        ia = a.get("intents", [])
        ib = b.get("intents", [])
        ga = a.get("groups", {})
        gb = b.get("groups", {})
        print("  intents: skill=%d workspace=%d" % (len(ia), len(ib)))
        print("  groups : skill=%d workspace=%d" % (len(ga), len(gb)))
        ka = {i.get("skill") for i in ia}
        kb = {i.get("skill") for i in ib}
        print("  skills only in skill   :", sorted(x for x in ka - kb if x))
        print("  skills only in workspace:", sorted(x for x in kb - ka if x))
        print("  guards equal:", a.get("guards") == b.get("guards"))
        print("  groups equal:", ga == gb)
