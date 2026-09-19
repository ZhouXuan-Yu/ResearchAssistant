import io, sys, json

P = r"C:\Users\ZhouXuan\.hanako\agents\agent-mu42qzfz\sessions\2026-09-16T13-07-26-778Z_01a0aa54-4dba-7184-95fa-23d95dfc7312.jsonl"
n = int(sys.argv[1]) if len(sys.argv) > 1 else 115
with io.open(P, encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        if i == n:
            print("LEN", len(line))
            print(line[:3000])
            break
