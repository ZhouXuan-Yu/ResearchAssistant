import json, io

P = r"C:\Users\ZhouXuan\.hanako\agents\agent-mu42qzfz\sessions\2026-09-16T13-07-26-778Z_01a0aa54-4dba-7184-95fa-23d95dfc7312.jsonl"

rows = []

def walk(node, ts, ln):
    if isinstance(node, dict):
        if node.get("type") == "toolCall" and node.get("name") == "todo_write":
            rows.append((ln, ts, node.get("arguments")))
        for v in node.values():
            walk(v, ts, ln)
    elif isinstance(node, list):
        for v in node:
            walk(v, ts, ln)

with io.open(P, encoding="utf-8") as f:
    for ln, line in enumerate(f, 1):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except Exception:
            continue
        walk(obj, obj.get("timestamp"), ln)

print("todo_write calls:", len(rows))
for ln, ts, arg in rows:
    print("=" * 72)
    print("line", ln, "| ts", ts)
    try:
        print(json.dumps(arg, ensure_ascii=False, indent=1))
    except Exception as e:
        print("err", e, str(arg)[:600])
