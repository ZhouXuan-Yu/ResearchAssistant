import json, psycopg2

conn = psycopg2.connect("host=db_postgres dbname=dify user=postgres password=difyai123456")
cur = conn.cursor()

cur.execute("SELECT graph FROM workflows WHERE app_id='22b49776-b615-4a49-bd26-bd5ca8454d5e' AND version='draft'")
row = cur.fetchone()
graph = row[0]

# Find the Code node's code field start
old_code_start = 'import json'
pos = graph.find(old_code_start)
if pos < 0:
    print("NOT FOUND")
    conn.close()
    exit()

# Find the end of the code string (before code_language)
end_pos = graph.find('"code_language":', pos)
if end_pos < 0:
    print("END NOT FOUND")
    conn.close()
    exit()

# Find the actual string end (the closing quote before comma)
# Go backwards from code_language to find the closing quote of the code string
code_end = graph.rfind('"', pos, end_pos)

new_code = '''import json

def main(arg1: str):
    """Parse extractions API response"""
    try:
        if isinstance(arg1, bytes):
            arg1 = arg1.decode("utf-8")
        data = json.loads(arg1) if isinstance(arg1, str) else arg1
    except Exception:
        return {"result": json.dumps({"error": "parse failed", "candidates": []}, ensure_ascii=False)}
    items = data.get("items", [])
    if not items:
        return {"result": json.dumps({"total": 0, "candidates": []}, ensure_ascii=False)}
    candidates = []
    for item in items:
        d = item.get("data", {})
        raw = item.get("raw_text", "")
        candidates.append({
            "name": d.get("name", ""),
            "phone": d.get("phone", ""),
            "email": d.get("email", ""),
            "education": d.get("education", {}),
            "experience": d.get("experience", {}),
            "skills": d.get("skills", []),
            "raw_text": raw[:3000]
        })
    return {"result": json.dumps({"total": len(candidates), "candidates": candidates}, ensure_ascii=False)}'''

new_graph = graph[:pos] + json.dumps(new_code)[1:-1] + graph[code_end:]
cur.execute("UPDATE workflows SET graph = %s WHERE app_id='22b49776-b615-4a49-bd26-bd5ca8454d5e' AND version='draft'", (new_graph,))
conn.commit()
print(f"OK. Old len: {code_end-pos}, New len: {len(new_code)}")
conn.close()
