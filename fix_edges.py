"""修复迭代内部缺失的连线"""
import psycopg2, json, uuid

conn = psycopg2.connect("host=db_postgres dbname=dify user=postgres password=difyai123456")
cur = conn.cursor()
app_id = '2b6abe8a-ec4e-4ecc-9074-ef280b3cbacc'
ITER_ID = '1782725226412'

cur.execute("SELECT id, type, version, graph FROM workflows WHERE app_id=%s", (app_id,))
for row in cur.fetchall():
    wid, typ, ver, graph_str = row
    graph = json.loads(graph_str) if isinstance(graph_str, str) else graph_str
    
    edges = graph.get('edges', [])
    existing_targets = {e['target'] for e in edges}
    
    added = False
    
    # 添加: 画像标签(1782727041328) → 写回人才库(1782727096984)
    if '1782727096984' not in existing_targets:
        edges.append({
            "id": str(uuid.uuid4()),
            "source": "1782727041328",
            "sourceHandle": "source",
            "target": "1782727096984",
            "targetHandle": "target",
            "type": "custom",
            "zIndex": 1002,
            "data": {
                "isInIteration": True,
                "isInLoop": False,
                "iteration_id": ITER_ID,
                "sourceType": "llm",
                "targetType": "http-request"
            }
        })
        added = True
        print(f"[{wid[:8]}] Added edge: 画像标签 → 写回人才库")
    
    # 添加: iteration-start → 画像标签(1782727041328)
    if '1782727041328' not in existing_targets:
        edges.append({
            "id": str(uuid.uuid4()),
            "source": f"{ITER_ID}start",
            "sourceHandle": "source",
            "target": "1782727041328",
            "targetHandle": "target",
            "type": "custom",
            "zIndex": 1002,
            "data": {
                "isInIteration": True,
                "isInLoop": False,
                "iteration_id": ITER_ID,
                "sourceType": "iteration-start",
                "targetType": "llm"
            }
        })
        added = True
        print(f"[{wid[:8]}] Added edge: iteration-start → 画像标签")
    
    if added:
        new_graph = json.dumps(graph, ensure_ascii=False)
        cur.execute("UPDATE workflows SET graph=%s, updated_at=NOW() WHERE id=%s", (new_graph, wid))

conn.commit()
conn.close()
print("\nDone! 画像标签 和 写回人才库 已接入迭代流程")
