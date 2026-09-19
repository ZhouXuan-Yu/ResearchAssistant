import json, io
from collections import Counter

P = r"C:\Users\ZhouXuan\.hanako\agents\agent-mu42qzfz\sessions\2026-09-16T13-07-26-778Z_01a0aa54-4dba-7184-95fa-23d95dfc7312.jsonl"
names = Counter()
sample = []
first = []

def walk(node):
    if isinstance(node, dict):
        if node.get("type") == "toolCall":
            nm = node.get("name") or node.get("toolName")
            names[str(nm)] += 1
            if len(first) < 1:
                first.append(node)
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
            walk(json.loads(line))
        except Exception:
            continue

print("SAMPLE KEYS:", list(first[0].keys()) if first else None)
print(json.dumps(first[0], ensure_ascii=False)[:800] if first else "")
print("----")
for k, v in names.most_common():
    print(v, k)
