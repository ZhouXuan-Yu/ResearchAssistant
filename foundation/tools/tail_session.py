import json, io

P = r"C:\Users\ZhouXuan\.hanako\agents\agent-mu42qzfz\sessions\2026-09-16T13-07-26-778Z_01a0aa54-4dba-7184-95fa-23d95dfc7312.jsonl"

lines = []
with io.open(P, encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line:
            lines.append(line)

print("total lines", len(lines))

def brief(obj):
    m = obj.get("message")
    if not isinstance(m, dict):
        return "[" + str(obj.get("type")) + "]"
    role = m.get("role")
    c = m.get("content")
    parts = []
    if isinstance(c, list):
        for b in c:
            if not isinstance(b, dict):
                parts.append(str(b)[:120])
                continue
            t = b.get("type")
            if t == "text":
                parts.append("TEXT:" + b.get("text", "")[:400].replace("\n", " "))
            elif t == "thinking":
                parts.append("THINK:" + (b.get("thinking", "") or "")[:150].replace("\n", " "))
            elif t == "toolCall":
                parts.append("CALL:" + str(b.get("name")) + " " + json.dumps(b.get("arguments"), ensure_ascii=False)[:300])
            else:
                parts.append(str(t) + ":" + json.dumps(b, ensure_ascii=False)[:200])
    elif isinstance(c, str):
        parts.append("TEXT:" + c[:400].replace("\n", " "))
    return (role or "?") + " | " + " || ".join(parts)

for line in lines[-14:]:
    try:
        obj = json.loads(line)
    except Exception:
        continue
    print("-" * 70)
    print(obj.get("timestamp"), brief(obj)[:900])
