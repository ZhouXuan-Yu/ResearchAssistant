import json, io
from collections import Counter

P = r"C:\Users\ZhouXuan\.hanako\agents\agent-mu42qzfz\sessions\2026-09-16T13-07-26-778Z_01a0aa54-4dba-7184-95fa-23d95dfc7312.jsonl"

types = Counter()
keys = Counter()

def walk(node):
    if isinstance(node, dict):
        t = node.get("type")
        if t is not None:
            types[str(t)] += 1
        for k in node.keys():
            keys[str(k)] += 1
        for v in node.values():
            walk(v)
    elif isinstance(node, list):
        for v in node:
            walk(v)

with io.open(P, encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except Exception:
            continue
        walk(obj)

print("TYPES:")
for k, v in types.most_common(40):
    print(" ", k, v)
print("KEYS:")
for k, v in keys.most_common(40):
    print(" ", k, v)
